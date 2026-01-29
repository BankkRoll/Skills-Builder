# Laravel Production Setup with Docker Compose and more

# Laravel Production Setup with Docker Compose

> Set up a production-ready environment for Laravel using Docker Compose.

# Laravel Production Setup with Docker Compose

   Table of contents

---

This guide demonstrates how to set up a production-ready Laravel environment using Docker and Docker Compose. This configuration is designed for streamlined, scalable, and secure Laravel application deployments.

> Note
>
> To experiment with a ready-to-run configuration, download the [Laravel Docker Examples](https://github.com/dockersamples/laravel-docker-examples) repository. It contains pre-configured setups for both development and production.

## Project structure

```plaintext
my-laravel-app/
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── docker/
│   ├── common/
│   │   └── php-fpm/
│   │       └── Dockerfile
│   ├── development/
│   ├── production/
│   │   ├── php-fpm/
│   │   │   └── entrypoint.sh
│   │   └── nginx
│   │       ├── Dockerfile
│   │       └── nginx.conf
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .env
├── vendor/
├── ...
```

This layout represents a typical Laravel project, with Docker configurations stored in a unified `docker` directory. You’ll find **two** Compose files — `compose.dev.yaml` (for development) and `compose.prod.yaml` (for production) — to keep your environments separate and manageable.

## Create a Dockerfile for PHP-FPM (production)

For production, the `php-fpm` Dockerfile creates an optimized image with only the PHP extensions and libraries your application needs. As demonstrated in the [GitHub example](https://github.com/dockersamples/laravel-docker-examples), a single Dockerfile with multi-stage builds maintains consistency and reduces duplication between development and production. The following snippet shows only the production-related stages:

```dockerfile
# Stage 1: Build environment and Composer dependencies
FROM php:8.4-fpm AS builder

# Install system dependencies and PHP extensions for Laravel with MySQL/PostgreSQL support.
# Dependencies in this stage are only required for building the final image.
# Node.js and asset building are handled in the Nginx stage, not here.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    opcache \
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the working directory inside the container
WORKDIR /var/www

# Copy the entire Laravel application code into the container
# -----------------------------------------------------------
# In Laravel, `composer install` may trigger scripts
# needing access to application code.
# For example, the `post-autoload-dump` event might execute
# Artisan commands like `php artisan package:discover`. If the
# application code (including the `artisan` file) is not
# present, these commands will fail, leading to build errors.
#
# By copying the entire application code before running
# `composer install`, we ensure that all necessary files are
# available, allowing these scripts to run successfully.
# In other cases, it would be possible to copy composer files
# first, to leverage Docker's layer caching mechanism.
# -----------------------------------------------------------
COPY . /var/www

# Install Composer and dependencies
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# Stage 2: Production environment
FROM php:8.4-fpm AS production

# Install only runtime libraries needed in production
# libfcgi-bin and procps are required for the php-fpm-healthcheck script
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    libfcgi-bin \
    procps \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Download and install php-fpm health check script
RUN curl -o /usr/local/bin/php-fpm-healthcheck \
    https://raw.githubusercontent.com/renatomefi/php-fpm-healthcheck/master/php-fpm-healthcheck \
    && chmod +x /usr/local/bin/php-fpm-healthcheck

# Copy the initialization script
COPY ./docker/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy the initial storage structure
COPY ./storage /var/www/storage-init

# Copy PHP extensions and libraries from the builder stage
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# Use the recommended production PHP configuration
# -----------------------------------------------------------
# PHP provides development and production configurations.
# Here, we replace the default php.ini with the production
# version to apply settings optimized for performance and
# security in a live environment.
# -----------------------------------------------------------
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Enable PHP-FPM status page by modifying zz-docker.conf with sed
RUN sed -i '/\[www\]/a pm.status_path = /status' /usr/local/etc/php-fpm.d/zz-docker.conf
# Update the variables_order to include E (for ENV)
#RUN sed -i 's/variables_order = "GPCS"/variables_order = "EGPCS"/' "$PHP_INI_DIR/php.ini"

# Copy the application code and dependencies from the build stage
COPY --from=builder /var/www /var/www

# Set working directory
WORKDIR /var/www

# Ensure correct permissions
RUN chown -R www-data:www-data /var/www

# Switch to the non-privileged user to run the application
USER www-data

# Change the default command to run the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]
```

## Create a Dockerfile for PHP-CLI (production)

For production, you often need a separate container to run Artisan commands, migrations, and other CLI tasks. In most cases you can run these commands by reusing existing PHP-FPM container:

```console
$ docker compose -f compose.prod.yaml exec php-fpm php artisan route:list
```

If you need a separate CLI container with different extensions or strict separation of concerns, consider a php-cli Dockerfile:

```dockerfile
# Stage 1: Build environment and Composer dependencies
FROM php:8.4-cli AS builder

# Install system dependencies and PHP extensions required for Laravel + MySQL/PostgreSQL support
# Some dependencies are required for PHP extensions only in the build stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    opcache \
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set the working directory inside the container
WORKDIR /var/www

# Copy the entire Laravel application code into the container
COPY . /var/www

# Install Composer and dependencies
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && composer install --no-dev --optimize-autoloader --no-interaction --no-progress --prefer-dist

# Stage 2: Production environment
FROM php:8.4-cli

# Install client libraries required for php extensions in runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libicu-dev \
    libzip-dev \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy PHP extensions and libraries from the builder stage
COPY --from=builder /usr/local/lib/php/extensions/ /usr/local/lib/php/extensions/
COPY --from=builder /usr/local/etc/php/conf.d/ /usr/local/etc/php/conf.d/
COPY --from=builder /usr/local/bin/docker-php-ext-* /usr/local/bin/

# Use the default production configuration for PHP runtime arguments
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Copy the application code and dependencies from the build stage
COPY --from=builder /var/www /var/www

# Set working directory
WORKDIR /var/www

# Ensure correct permissions
RUN chown -R www-data:www-data /var/www

# Switch to the non-privileged user to run the application
USER www-data

# Default command: Provide a bash shell to allow running any command
CMD ["bash"]
```

This Dockerfile is similar to the PHP-FPM Dockerfile, but it uses the `php:8.4-cli` image as the base image and sets up the container for running CLI commands.

## Create a Dockerfile for Nginx (production)

Nginx serves as the web server for the Laravel application. You can include static assets directly to the container. Here's an example of possible Dockerfile for Nginx:

```dockerfile
# docker/nginx/Dockerfile
# Stage 1: Build assets
FROM debian AS builder

# Install Node.js and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    nodejs \
    npm \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set working directory
WORKDIR /var/www

# Copy Laravel application code
COPY . /var/www

# Install Node.js dependencies and build assets
RUN npm install && npm run build

# Stage 2: Nginx production image
FROM nginx:alpine

# Copy custom Nginx configuration
# -----------------------------------------------------------
# Replace the default Nginx configuration with our custom one
# that is optimized for serving a Laravel application.
# -----------------------------------------------------------
COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy Laravel's public assets from the builder stage
# -----------------------------------------------------------
# We only need the 'public' directory from our Laravel app.
# -----------------------------------------------------------
COPY --from=builder /var/www/public /var/www/public

# Set the working directory to the public folder
WORKDIR /var/www/public

# Expose port 80 and start Nginx
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

This Dockerfile uses a multi-stage build to separate the asset building process from the final production image. The first stage installs Node.js and builds the assets, while the second stage sets up the Nginx production image with the optimized configuration and the built assets.

## Create a Docker Compose configuration for production

To bring all the services together, create a `compose.prod.yaml` file that defines the services, volumes, and networks for the production environment. Here's an example configuration:

```yaml
services:
  web:
    build:
      context: .
      dockerfile: ./docker/production/nginx/Dockerfile
    restart: unless-stopped # Automatically restart unless the service is explicitly stopped
    volumes:
      # Mount the 'laravel-storage' volume to '/var/www/storage' inside the container.
      # -----------------------------------------------------------
      # This volume stores persistent data like uploaded files and cache.
      # The ':ro' option mounts it as read-only in the 'web' service because Nginx only needs to read these files.
      # The 'php-fpm' service mounts the same volume without ':ro' to allow write operations.
      # -----------------------------------------------------------
      - laravel-storage-production:/var/www/storage:ro
    networks:
      - laravel-production
    ports:
      # Map port 80 inside the container to the port specified by 'NGINX_PORT' on the host machine.
      # -----------------------------------------------------------
      # This allows external access to the Nginx web server running inside the container.
      # For example, if 'NGINX_PORT' is set to '8080', accessing 'http://localhost:8080' will reach the application.
      # -----------------------------------------------------------
      - "${NGINX_PORT:-80}:80"
    depends_on:
      php-fpm:
        condition: service_healthy # Wait for php-fpm health check

  php-fpm:
    # For the php-fpm service, we will create a custom image to install the necessary PHP extensions and setup proper permissions.
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: production # Use the 'production' stage in the Dockerfile
    restart: unless-stopped
    volumes:
      - laravel-storage-production:/var/www/storage # Mount the storage volume
    env_file:
      - .env
    networks:
      - laravel-production
    healthcheck:
      test: ["CMD-SHELL", "php-fpm-healthcheck || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
    # The 'depends_on' attribute with 'condition: service_healthy' ensures that
    # this service will not start until the 'postgres' service passes its health check.
    # This prevents the application from trying to connect to the database before it's ready.
    depends_on:
      postgres:
        condition: service_healthy

  # The 'php-cli' service provides a command-line interface for running Artisan commands and other CLI tasks.
  # -----------------------------------------------------------
  # This is useful for running migrations, seeders, or any custom scripts.
  # It shares the same codebase and environment as the 'php-fpm' service.
  # -----------------------------------------------------------
  php-cli:
    build:
      context: .
      dockerfile: ./docker/php-cli/Dockerfile
    tty: true # Enables an interactive terminal
    stdin_open: true # Keeps standard input open for 'docker exec'
    env_file:
      - .env
    networks:
      - laravel

  postgres:
    image: postgres:18
    restart: unless-stopped
    user: postgres
    ports:
      - "${POSTGRES_PORT}:5432"
    environment:
      - POSTGRES_DB=${POSTGRES_DATABASE}
      - POSTGRES_USER=${POSTGRES_USERNAME}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres-data-production:/var/lib/postgresql
    networks:
      - laravel-production
    # Health check for PostgreSQL
    # -----------------------------------------------------------
    # Health checks allow Docker to determine if a service is operational.
    # The 'pg_isready' command checks if PostgreSQL is ready to accept connections.
    # This prevents dependent services from starting before the database is ready.
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    restart: unless-stopped # Automatically restart unless the service is explicitly stopped
    networks:
      - laravel-production
    # Health check for Redis
    # -----------------------------------------------------------
    # Checks if Redis is responding to the 'PING' command.
    # This ensures that the service is not only running but also operational.
    # -----------------------------------------------------------
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  # Attach the service to the 'laravel-production' network.
  # -----------------------------------------------------------
  # This custom network allows all services within it to communicate using their service names as hostnames.
  # For example, 'php-fpm' can connect to 'postgres' by using 'postgres' as the hostname.
  # -----------------------------------------------------------
  laravel-production:

volumes:
  postgres-data-production:
  laravel-storage-production:
```

> Note
>
> Ensure you have an `.env` file at the root of your Laravel project with the necessary configurations (e.g., database and Xdebug settings) to match the Docker Compose setup.

## Running your production environment

To start the production environment, run:

```console
$ docker compose -f compose.prod.yaml up --build -d
```

This command will build and start all the services in detached mode, providing a scalable and production-ready setup for your Laravel application.

## Summary

By setting up a Docker Compose environment for Laravel in production, you ensure that your application is optimized for performance, scalable, and secure. This setup makes deployments consistent and easier to manage, reducing the likelihood of errors due to differences between environments.

---

# Develop and Deploy Laravel applications with Docker Compose

> A guide on using Docker Compose to manage Laravel applications for development and production, covering container configurations and service management.

# Develop and Deploy Laravel applications with Docker Compose

Table of contents

---

Laravel is a popular PHP framework that allows developers to build web applications quickly and effectively. Docker Compose simplifies the management of development and production environments by defining essential services, like PHP, a web server, and a database, in a single YAML file. This guide provides a streamlined approach to setting up a robust Laravel environment using Docker Compose, focusing on simplicity and efficiency.

> **Acknowledgment**
>
>
>
> Docker would like to thank [Sergei Shitikov](https://github.com/rw4lll) for
> his contribution to this guide.

The demonstrated examples can be found in [this GitHub repository](https://github.com/dockersamples/laravel-docker-examples). Docker Compose offers a straightforward approach to connecting multiple containers for Laravel, though similar setups can also be achieved using tools like Docker Swarm, Kubernetes, or individual Docker containers.

This guide is intended for educational purposes, helping developers adapt and optimize configurations for their specific use cases. Additionally, there are existing tools that support Laravel in containers:

- [Laravel Sail](https://laravel.com/docs/12.x/sail): An official package for easily starting Laravel in Docker.
- [Laradock](https://github.com/laradock/laradock): A community project that helps run Laravel applications in Docker.

## What you’ll learn

- How to use Docker Compose to set up a Laravel development and production environment.
- Defining services that make Laravel development easier, including PHP-FPM, Nginx, and database containers.
- Best practices for managing Laravel environments using containerization.

## Who’s this for?

- Developers who work with Laravel and want to streamline environment management.
- DevOps engineers seeking efficient ways to manage and deploy Laravel applications.

## Modules

1. [Prerequisites for Setting Up Laravel with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/prerequisites/)
  Ensure you have the required tools and knowledge before setting up Laravel with Docker Compose.
2. [Laravel Production Setup with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/production-setup/)
  Set up a production-ready environment for Laravel using Docker Compose.
3. [Laravel Development Setup with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/development-setup/)
  Set up a Laravel development environment using Docker Compose.
4. [Common Questions on Using Laravel with Docker](https://docs.docker.com/guides/frameworks/laravel/common-questions/)
  Find answers to common questions about setting up and managing Laravel environments with Docker Compose, including troubleshooting and best practices.

---

# Generate Docker Compose Files with Claude Code and Docker MCP Toolkit

> Learn how to use Claude Code with Docker MCP Toolkit to generate production-ready Docker Compose files from natural language using the Docker Hub MCP server.

# Generate Docker Compose Files with Claude Code and Docker MCP Toolkit

   Table of contents

---

This guide introduces how to use Claude Code together with Docker MCP Toolkit so Claude can search Docker Hub in real time and generate a complete `docker-compose.yaml` from natural language.

Instead of manually writing YAML or looking for image tags, you describe your stack once — Claude uses the Model Context Protocol (MCP) to query Docker Hub and build a production-ready Compose file.

In this guide, you’ll learn how to:

- Enable Docker MCP Toolkit in Docker Desktop
- Add the Docker Hub MCP server
- Connect Claude Code to the MCP Gateway (GUI or CLI)
- Verify MCP connectivity inside Claude
- Ask Claude to generate and save a Compose file for a Node.js + PostgreSQL app
- Deploy it instantly with `docker compose up`

---

## Use Claude Code and Docker MCP Toolkit to generate a Docker Compose file from natural language

- **Setup**: Enable MCP Toolkit → Add Docker Hub MCP server → Connect Claude Code
- **Use Claude**: Describe your stack in plain English
- **Automate**: Claude queries Docker Hub via MCP and builds a complete `docker-compose.yaml`
- **Deploy**: Run `docker compose up` → Node.js + PostgreSQL live on `localhost:3000`
- **Benefit**: Zero YAML authoring. Zero image searching. Describe once → Claude builds it.

**Estimated time**: ~15 minutes

---

## 1. What you are building

The goal is simple: use Claude Code together with the Docker MCP Toolkit to search Docker Hub images and generate a complete Docker Compose file for a Node.js and PostgreSQL setup.

The Model Context Protocol (MCP) bridges Claude Code and Docker Desktop, giving Claude real-time access to Docker's tools. Instead of context-switching between Docker, terminal commands, and YAML editors, you describe your requirements once and Claude handles the infrastructure details.

**Why this matters:** This pattern scales to complex multi-service setups, database migrations, networking, security policies — all through conversational prompts.

---

## 2. Prerequisites

Make sure you have:

- Docker Desktop installed
- Enable Docker Desktop updated with [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/#setup) support
- Claude Code installed

---

## 3. Install the Docker Hub MCP server

1. Open **Docker Desktop**
2. Select **MCP Toolkit**
3. Go to the **Catalog** tab
4. Search for **Docker Hub**
5. Select the **Docker Hub**MCP server
6. Add the MCP server, then open the **Configuration** tab
7. Enter your Docker Hub username
8. [Create a read-only personal access token](https://docs.docker.com/security/access-tokens/#create-a-personal-access-token) and enter your access token under **Secrets**
9. Save the configuration

![Docker Hub](https://docs.docker.com/guides/genai-claude-code-mcp/Images/catalog_docker_hub.avif)Docker Hub ![Docker Hub](https://docs.docker.com/guides/genai-claude-code-mcp/Images/catalog_docker_hub.avif)

Public images work without credentials. For private repositories, you can add your Docker Hub username and token later.

![Docker Hub Secrets](https://docs.docker.com/guides/genai-claude-code-mcp/Images/dockerhub_secrets.avif)Docker Hub Secrets ![Docker Hub Secrets](https://docs.docker.com/guides/genai-claude-code-mcp/Images/dockerhub_secrets.avif)

---

## 4. Connect Claude Code to Docker MCP Toolkit

You can connect from Docker Desktop or using the CLI.

### Option A. Connect with Docker Desktop

1. Open **MCP Toolkit**
2. Go to the **Clients** tab
3. Locate **Claude Code**
4. Select **Connect**

![Docker Connection](https://docs.docker.com/guides/genai-claude-code-mcp/Images/docker-connect-claude.avif)  ![Docker Connection](https://docs.docker.com/guides/genai-claude-code-mcp/Images/docker-connect-claude.avif)

### Option B. Connect using the CLI

```console
$ claude mcp add MCP_DOCKER -s user -- docker mcp gateway run
```

---

## 5. Verify MCP servers inside Claude Code

1. Navigate to your project folder:

```console
$ cd /path/to/project
```

1. Start Claude Code:

```console
$ claude
```

1. In the input box, type:

```console
/mcp
```

You should now see:

- The MCP gateway (for example `MCP_DOCKER`)
- Tools provided by the Docker Hub MCP server

![mcp-docker](https://docs.docker.com/guides/genai-claude-code-mcp/Images/mcp-servers.avif)  ![mcp-docker](https://docs.docker.com/guides/genai-claude-code-mcp/Images/mcp-servers.avif)

If not, restart Claude Code or check Docker Desktop to confirm the connection.

---

## 6. Create a basic Node.js app

Claude Code generates more accurate Compose files when it can inspect a real project. Set up the application code now so the agent can bind mount it later.

Inside project folder, create a folder named `app`:

```console
$ mkdir app
$ cd app
$ npm init -y
$ npm install express
```

Create `index.js`:

```console
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send("Node.js, Docker, and MCP Toolkit are working together!");
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

Add a start script to `package.json`:

```console
"scripts": {
  "start": "node index.js"
}
```

Return to your project root (`cd ..`) once the app is ready.

---

## 7. Ask Claude Code to design your Docker Compose stack

Paste this message into Claude Code:

```console
Using the Docker Hub MCP server:

Search Docker Hub for an official Node.js image and a PostgreSQL image.
Choose stable, commonly used tags such as the Node LTS version and a recent major Postgres version.

Generate a Docker Compose file (`docker-compose.yaml`) with:
- app:
  - runs on port 3000
  - bind mounts the existing ./app directory into /usr/src/app
  - sets /usr/src/app as the working directory and runs `npm install && npm start`
- db: running on port 5432 using a named volume

Include:
- Environment variables for Postgres
- A shared bridge network
- Healthchecks where appropriate
- Pin the image version using the tag + index digest
```

Claude will search images through MCP, inspect the `app` directory, and generate a Compose file that mounts and runs your local code.

---

## 8. Save the generated Docker Compose file

Tell Claude:

```console
Save the final Docker Compose file (docker-compose.yaml) into the current project directory.
```

You should see something like this:

```console
services:
  app:
    image: node:<tag>
    working_dir: /usr/src/app
    volumes:
      - .:/usr/src/app
    ports:
      - "3000:3000"
    depends_on:
      - db
    networks:
      - app-net

  db:
    image: postgres:18
    environment:
      POSTGRES_USER: example
      POSTGRES_PASSWORD: example
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql
    ports:
      - "5432:5432"
    networks:
      - app-net

volumes:
  db-data:

networks:
  app-net:
    driver: bridge
```

---

## 9. Run the Docker Compose stack

From your project root:

```console
$ docker compose up
```

Docker will:

- Pull the Node and Postgres images selected through Docker Hub MCP
- Create networks and volumes
- Start the containers

Open your browser:

```console
http://localhost:3000
```

![Local Host](https://docs.docker.com/guides/genai-claude-code-mcp/Images/Localhost.avif)  ![Local Host](https://docs.docker.com/guides/genai-claude-code-mcp/Images/Localhost.avif)

Your Node.js app should now be running.

---

## Conclusion

By combining Claude Code with the Docker MCP Toolkit, Docker Desktop, and the Docker Hub MCP server, you can describe your stack in natural language and let MCP handle the details. This removes context switching and replaces it with a smooth, guided workflow powered by model context protocol integrations.

---

### Next steps

- Explore the 220+ MCP servers available in the [Docker MCP catalog](https://hub.docker.com/mcp)
- Connect Claude Code to your databases, internal APIs, and team tools
- Share your MCP setup with your team so everyone works consistently

The future of development is not about switching between tools. It is about tools working together in a simple, safe, and predictable way. The Docker MCP Toolkit brings that future into your everyday workflow.

## Learn more

- **Explore the MCP Catalog:** Discover containerized, security-hardened MCP servers
- **Get started with MCP Toolkit in Docker Desktop:** Requires version 4.48 or newer to launch automatically
- **Read the MCP Horror Stories series:** Learn about common MCP security pitfalls and how to avoid them

---

# Leveraging RAG in GenAI to teach new information

> This guide walks through the process of setting up and utilizing a GenAI stack with Retrieval-Augmented Generation (RAG) systems and graph databases. Learn how to integrate graph databases like Neo4j with AI models for more accurate, contextually-aware responses.

# Leveraging RAG in GenAI to teach new information

   Table of contents

---

## Introduction

Retrieval-Augmented Generation (RAG) is a powerful framework that enhances large language models (LLMs) by integrating information retrieval from external knowledge sources. This guide focuses on a specialized RAG implementation using graph databases like Neo4j, which excel in managing highly connected, relational data. Unlike traditional RAG setups with vector databases, combining RAG with graph databases offers better context-awareness and relationship-driven insights.

In this guide, you will:

- Explore the advantages of integrating graph databases into a RAG framework.
- Configure a GenAI stack with Docker, incorporating Neo4j and an AI model.
- Analyze a real-world case study that highlights the effectiveness of this approach for handling specialized queries.

## Understanding RAG

RAG is a hybrid framework that enhances the capabilities of large language models by integrating information retrieval. It combines three core components:

- **Information retrieval** from an external knowledge base
- **Large Language Model (LLM)** for generating responses
- **Vector embeddings** to enable semantic search

In a RAG system, vector embeddings are used to represent the semantic meaning of text in a way that a machine can understand and process. For instance, the words "dog" and "puppy" will have similar embeddings because they share similar meanings. By integrating these embeddings into the RAG framework, the system can combine the generative power of large language models with the ability to pull in highly relevant, contextually-aware data from external sources.

The system operates as follows:

1. Questions get turned into mathematical patterns that capture their meaning
2. These patterns help find matching information in a database
3. The LLM generates responses that blend the model's inherent knowledge with the this extra information.

To hold this vector information in an efficient manner, we need a special type of database.

## Introduction to Graph databases

Graph databases, such as Neo4j, are specifically designed for managing highly connected data. Unlike traditional relational databases, graph databases prioritize both the entities and the relationships between them, making them ideal for tasks where connections are as important as the data itself.

Graph databases stand out for their unique approach to data storage and querying. They use nodes (or vertices) to represent entities and edges to represent the relationships between these entities. This structure allows for efficient handling of highly connected data and complex queries, which are difficult to manage in traditional database systems.

SQL databases and graph databases differ significantly in their data models. SQL databases use a tabular structure with rows and columns, where relationships between entities are established using foreign keys. This approach works well for structured data and predefined relationships. In contrast, graph databases represent data as nodes (entities) and edges (relationships), making the representation of relationships more intuitive and flexible. This structure is particularly advantageous for complex, interconnected data.

Another key difference lies in schema flexibility. SQL databases operate on a rigid schema, meaning any changes to the data structure, such as adding new columns or altering relationships, typically require careful planning and migration processes. Graph databases, however, are schema-optional, allowing for much greater flexibility. New nodes, edges, or properties can be introduced without disrupting existing data, enabling faster adaptation to changing requirements.

## Practical implementation: testing RAG effectiveness

To illustrate the power of RAG systems in practice, let's examine a real-world implementation using Apache NiFi as our subject matter. This case study demonstrates how RAG can enhance an AI's ability to provide accurate, contextual information about specialized technical topics.

### Teaching AI about new technologies

Apache NiFi serves as an excellent example of the limitations of traditional LLMs and how RAG can overcome them. As a relatively recent technology, many LLMs have limited or outdated knowledge about it, making it a perfect candidate for demonstrating RAG's capabilities.

Without RAG, the LLM may provide broad responses or acknowledge its limited knowledge when asked about information that is beyond its cutoff date. The following example demonstrates this.

```text
Question: What important events happened in 2024?
RAG: Disabled
I'm happy to help! Unfortunately, I'm a large language model, I don't have access to real-time information or events that occurred after my training data cutoff in 2024. Therefore, I cannot provide you with any important events that happened in 2024. My apologize for any inconvenience this may cause. Is there anything else I can help you with?
```

## Setting up GenAI stack with GPU acceleration on Linux

To set up and run the GenAI stack on a Linux host, execute one of the following commands, either for GPU or CPU powered:

### GPU powered

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux-gpu up -d
mv env.example .env
nano .env
```

In the `.env` file, make sure following lines are commented out. Set your own credentials for security

```txt
NEO4J_URI=neo4j://database:7687
  NEO4J_USERNAME=neo4j
  NEO4J_PASSWORD=password
  OLLAMA_BASE_URL=http://llm-gpu:11434
```

### CPU powered

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux up -d
mv env.example .env
nano .env
```

In the `.env` file, make sure following lines are commented out. Set your own credentials for security

```txt
NEO4J_URI=neo4j://database:7687
  NEO4J_USERNAME=neo4j
  NEO4J_PASSWORD=password
  OLLAMA_BASE_URL=http://llm:11434
```

### Setting up on other platforms

For instructions on how to set up the stack on other platforms, refer to [this page](https://github.com/docker/genai-stack).

### Initial startup

The first startup may take some time because the system needs to download a large language model.

### Monitoring progress

We can monitor the download and initialization progress by viewing the logs. Run the following command to view the logs:

```bash
docker compose logs
```

Wait for specific lines in the logs indicating that the download is complete and the stack is ready. These lines typically confirm successful setup and initialization.

```text
pull-model-1 exited with code 0
  database-1    | 2024-12-29 09:35:53.269+0000 INFO  Started.
  pdf_bot-1     |   You can now view your Streamlit app in your browser.
  loader-1      |   You can now view your Streamlit app in your browser.
  bot-1         |   You can now view your Streamlit app in your browser.
```

You can now access the interface at [http://localhost:8501/](http://localhost:8501/) to ask questions. For example, you can try the sample question:

When we see those lines in the logs, web apps are ready to be used.

Since our goal is to teach AI about things it does not yet know, we begin by asking it a simple question about Nifi at
[http://localhost:8501/](http://localhost:8501/).

![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image.png)  ![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image.png)

```text
Question: What is Apache Nifi?
RAG: Disabled
Hello! I'm here to help you with your question about Apache NiFi. Unfortunately, I don't know the answer to that question. I'm just an AI and my knowledge cutoff is December 2022, so I may not be familiar with the latest technologies or software. Can you please provide more context or details about Apache NiFi? Maybe there's something I can help you with related to it.
```

As we can see, AI does not know anything about this subject because it did not exist during the time of its training, also known as the information cutoff point.

Now it's time to teach the AI some new tricks. First, connect to [http://localhost:8502/](http://localhost:8502/). Instead of using the "neo4j" tag, change it to the "apache-nifi" tag, then select the **Import** button.

![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image-1.png)  ![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image-1.png)

After the import is successful, we can access Neo4j to verify the data.

After logging in to [http://localhost:7474/](http://localhost:7474/) using the credentials from the `.env` file, you can run queries on Neo4j. Using the Neo4j Cypher query language, you can check for the data stored in the database.

To count the data, run the following query:

```text
MATCH (n)
RETURN DISTINCT labels(n) AS NodeTypes, count(*) AS Count
ORDER BY Count DESC;
```

To execute this query, write in the box on the top and select the blue run button.

![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image-2.png)  ![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image-2.png)

Results will appear below. What we are seeing here is the information system downloaded from Stack Overflow and saved in the graph database. RAG will utilize this information to enhance its responses.

You can also run the following query to visualize the data:

```text
CALL db.schema.visualization()
```

To check the relationships in the database, run the following query:

```text
CALL db.relationshipTypes()
```

Now, we are ready to enable our LLM to use this information. Go back to [http://localhost:8501/](http://localhost:8501/), enable the **RAG** checkbox, and ask the same question again. The LLM will now provide a more detailed answer.

![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image-3.png)  ![alt text](https://docs.docker.com/guides/genai-leveraging-rag/image-3.png)

The system delivers comprehensive, accurate information by pulling from current technical documentation.

```text
Question: What is Apache Nifi?
RAG: Enabled

Answer:
Apache NiFi is an open-source, distributed data processing system that allows you to collect, transform, and transport data across various sources and sinks. It provides a graphical user interface for designing and managing data flows, as well as a set of APIs for integrating with other systems.
According to this Stack Overflow question, the free Neo4J JDBC driver doesn't understand SQL, only Cypher, so you would need to use a non-free BI Connector to connect to Neo4j from Apache Drill.
Additionally, this Stack Overflow question suggests that Apache POI does work in a Neo4j User Defined Function. However, there may be an unknown glitch in the standalone UDF mentioned in the initial question.
To export data from Neo4j to Excel using APOC Extended procedures, you can use apoc.export.xls.query which takes a Cypher query and exports the results to an Excel file.

References:
How to connect and query Neo4j Database on Apache Drill?
Is a Neo4j UDF compatible with Apache POI?
```

Keep in mind that new questions will be added to Stack Overflow, and due to the inherent randomness in most AI models, the answers may vary and won't be identical to those in this example.

Feel free to start over with another [Stack Overflow tag](https://stackoverflow.com/tags). To drop all data in Neo4j, you can use the following command in the Neo4j Web UI:

```txt
MATCH (n)
DETACH DELETE n;
```

For optimal results, choose a tag that the LLM is not familiar with.

### When to leverage RAG for optimal results

Retrieval-Augmented Generation (RAG) is particularly effective in scenarios where standard Large Language Models (LLMs) fall short. The three key areas where RAG excels are knowledge limitations, business requirements, and cost efficiency. Below, we explore these aspects in more detail.

#### Overcoming knowledge limitations

LLMs are trained on a fixed dataset up until a certain point in time. This means they lack access to:

- Real-time information: LLMs do not continuously update their knowledge, so they may not be aware of recent events, newly released research, or emerging technologies.
- Specialized knowledge: Many niche subjects, proprietary frameworks, or industry-specific best practices may not be well-documented in the model’s training corpus.
- Accurate contextual understanding: LLMs can struggle with nuances or evolving terminologies that frequently change within dynamic fields like finance, cybersecurity, or medical research.

By incorporating RAG with a graph database such as Neo4j, AI models can access and retrieve the latest, relevant, and highly connected data before generating a response. This ensures that answers are up-to-date and grounded in factual information rather than inferred approximations.

#### Addressing business and compliance needs

Organizations in industries like healthcare, legal services, and financial analysis require their AI-driven solutions to be:

- Accurate: Businesses need AI-generated content that is factual and relevant to their specific domain.
- Compliant: Many industries must adhere to strict regulations regarding data usage and security.
- Traceable: Enterprises often require AI responses to be auditable, meaning they need to reference source material.

By using RAG, AI-generated answers can be sourced from trusted databases, ensuring higher accuracy and compliance with industry standards. This mitigates risks such as misinformation or regulatory violations.

#### Enhancing cost efficiency and performance

Training and fine-tuning large AI models can be computationally expensive and time-consuming. However, integrating RAG provides:

- Reduced fine-tuning needs: Instead of retraining an AI model every time new data emerges, RAG allows the model to fetch and incorporate updated information dynamically.
- Better performance with smaller models: With the right retrieval techniques, even compact AI models can perform well by leveraging external knowledge efficiently.
- Lower operational costs: Instead of investing in expensive infrastructure to support large-scale retraining, businesses can optimize resources by utilizing RAG’s real-time retrieval capabilities.

By following this guide, you now have the foundational knowledge to implement RAG with Neo4j, enabling your AI system to deliver more accurate, relevant, and insightful responses. The next step is experimentation—choose a dataset, configure your stack, and start enhancing your AI with the power of retrieval-augmented generation.
