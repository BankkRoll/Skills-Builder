# Supply and more

# Supply

> Learn how to extract SBOMs from C++ Docker images.

# Supply-chain security for C++ Docker images

   Table of contents

---

## Prerequisites

- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.
- You have a Docker Desktop installed, with containerd enabled for pulling and storing images (it's a checkbox in **Settings** > **General**). Otherwise, if you use Docker Engine:
  - You have the [Docker SBOM CLI plugin](https://github.com/docker/sbom-cli-plugin) installed. To install it on Docker Engine, use the following command:
    ```bash
    $ curl -sSfL https://raw.githubusercontent.com/docker/sbom-cli-plugin/main/install.sh | sh -s --
    ```
  - You have the [Docker Scout CLI plugin](https://docs.docker.com/scout/install/) installed. To install it on Docker Engine, use the following command:
    ```bash
    $ curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
    ```
  - You have [containerd enabled](https://docs.docker.com/engine/storage/containerd/) for Docker Engine.

## Overview

This section walks you through extracting Software Bill of Materials (SBOMs) from a C++ Docker image using the Docker SBOM CLI plugin. SBOMs provide a detailed list of all the components in a software package, including their versions and licenses. You can use SBOMs to track the provenance of your software and ensure that it complies with your organization's security and licensing policies.

## Generate an SBOM

Here we will use the Docker image that we built in the
[Create a multi-stage build for your C++ application](https://docs.docker.com/guides/language/cpp/multistage/) guide. If you haven't already built the image, follow the steps in that guide to build the image.
The image is named `hello`. To generate an SBOM for the `hello` image, run the following command:

```bash
$ docker sbom hello
```

The command will say "No packages discovered". This is because the final image is a scratch image and doesn't have any packages.
Let's try again with Docker Scout:

```bash
$ docker scout sbom --format=list hello
```

This command will tell you the same thing.

## Generate an SBOM attestation

The SBOM can be generated during the build process and "attached" to the image. This is called an SBOM attestation.
To generate an SBOM attestation for the `hello` image, first let's change the Dockerfile:

```Dockerfile
ARG BUILDKIT_SBOM_SCAN_STAGE=true

FROM ubuntu:latest AS build

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY hello.cpp .

RUN g++ -o hello hello.cpp -static

# --------------------
FROM scratch

COPY --from=build /app/hello /hello

CMD ["/hello"]
```

The first line `ARG BUILDKIT_SBOM_SCAN_STAGE=true` enables SBOM scanning in the build stage.
Now, build the image with the following command:

```bash
$ docker buildx build --sbom=true -t hello:sbom .
```

This command will build the image and generate an SBOM attestation. You can verify that the SBOM is attached to the image by running the following command:

```bash
$ docker scout sbom --format=list hello:sbom
```

Note that the normal `docker sbom` command will not load the SBOM attestation.

## Summary

In this section, you learned how to generate SBOM attestation for a C++ Docker image during the build process.
The normal image scanners will not be able to generate SBOMs from scratch images.

---

# C++ language

> Containerize and develop C++ applications using Docker.

# C++ language-specific guide

---

The C++ getting started guide teaches you how to create a containerized C++ application using Docker. In this guide, you'll learn how to:

> **Acknowledgment**
>
>
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) and [Mohammad-Ali A'râbi](https://twitter.com/MohammadAliEN) for their contribution to this guide.

- Containerize and run a C++ application using a multi-stage Docker build
- Build and run a C++ application using Docker Compose
- Set up a local environment to develop a C++ application using containers
- Configure a CI/CD pipeline for a containerized C++ application using GitHub Actions
- Deploy your containerized application locally to Kubernetes to test and debug your deployment
- Use BuildKit to generate SBOM attestations during the build process

After completing the C++ getting started modules, you should be able to containerize your own C++ application based on the examples and instructions provided in this guide.

Start by containerizing an existing C++ application.

## Modules

1. [Containerize your app using a multi-stage build](https://docs.docker.com/guides/cpp/multistage/)
  Learn how to create a multi-stage build for a C++ application.
2. [Build and run a C++ application using Docker Compose](https://docs.docker.com/guides/cpp/containerize/)
  Learn how to use Docker Compose to build and run a C++ application.
3. [Develop your app](https://docs.docker.com/guides/cpp/develop/)
  Learn how to develop your C++ application locally.
4. [Configure CI/CD](https://docs.docker.com/guides/cpp/configure-ci-cd/)
  Learn how to configure CI/CD using GitHub Actions for your C++ application.
5. [Test your deployment](https://docs.docker.com/guides/cpp/deploy/)
  Learn how to develop locally using Kubernetes
6. [Supply-chain security](https://docs.docker.com/guides/cpp/security/)
  Learn how to extract SBOMs from C++ Docker images.

---

# Use containerized databases

> Learn how to run, connect to, and persist data in a local containerized database.

# Use containerized databases

   Table of contents

---

Using a local containerized database offers flexibility and ease of setup,
letting you mirror production environments closely without the overhead of
traditional database installations. Docker simplifies this process, enabling you
to deploy, manage, and scale databases in isolated containers with just a few
commands.

In this guide, you'll learn how to:

- Run a local containerized database
- Access the shell of a containerized database
- Connect to a containerized database from your host
- Connect to a containerized database from another container
- Persist database data in a volume
- Build a customized database image
- Use Docker Compose to run a database

This guide uses the MySQL image for examples, but the concepts can be applied to other database images.

## Prerequisites

To follow along with this guide, you must have Docker installed. To install Docker, see
[Get Docker](https://docs.docker.com/get-started/get-docker/).

## Run a local containerized database

Most popular database systems, including MySQL, PostgreSQL, and MongoDB, have a
Docker Official Image available on Docker Hub. These images are a curated set
images that follow best practices, ensuring that you have access to the latest
features and security updates. To get started, visit
[Docker Hub](https://hub.docker.com) and search for the database you're
interested in. Each image's page provides detailed instructions on how to run
the container, customize your setup, and configure the database according to
your needs. For more information about the MySQL image used in this guide, see the Docker Hub [MySQL image](https://hub.docker.com/_/mysql) page.

To run a database container, you can use either the Docker Desktop GUI or
CLI.

To run a container using the CLI, run the following command in a terminal:

```console
$ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -d mysql:latest
```

In this command:

- `--name my-mysql` assigns the name my-mysql to your container for easier
  reference.
- `-e MYSQL_ROOT_PASSWORD=my-secret-pw` sets the root password for MySQL to
  my-secret-pw. Replace my-secret-pw with a secure password of your choice.
- `-e MYSQL_DATABASE=mydb` optionally creates a database named mydb. You can
  change mydb to your desired database name.
- `-d` runs the container in detached mode, meaning it runs in the background.
- `mysql:latest` specifies that you want to use the latest version of the MySQL
  image.

To verify that your container is running, run `docker ps` in a terminal

To run a container using the GUI:

1. In the Docker Desktop Dashboard, select the global search at the top of the window.
2. Specify `mysql` in the search box, and select the `Images` tab if not already
  selected.
3. Hover over the `mysql` image and select `Run`.
  The **Run a new container** modal appears.
4. Expand **Optional settings**.
5. In the optional settings, specify the following:
  - **Container name**: `my-mysql`
  - **Environment variables**:
    - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
    - `MYSQL_DATABASE`:`mydb`
  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-1.webp)  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-1.webp)
6. Select `Run`.
7. Open the **Container** view in the Docker Desktop Dashboard to verify that your
  container is running.

## Access the shell of a containerized database

When you have a database running inside a Docker container, you may need to
access its shell to manage the database, execute commands, or perform
administrative tasks. Docker provides a straightforward way to do this using the
`docker exec` command. Additionally, if you prefer a graphical interface, you
can use Docker Desktop's GUI.

If you don't yet have a database container running, see
[Run a local containerized database](#run-a-local-containerized-database).

To access the terminal of a MySQL container using the CLI, you can use the
following `docker exec` command.

```console
$ docker exec -it my-mysql bash
```

In this command:

- `docker exec` tells Docker you want to execute a command in a running
  container.
- `-it` ensures that the terminal you're accessing is interactive, so you can
  type commands into it.
- `my-mysql` is the name of your MySQL container. If you named your container
  differently when you ran it, use that name instead.
- `bash` is the command you want to run inside the container. It opens up a bash
  shell that lets you interact with the container's file system and installed
  applications.

After executing this command, you will be given access to the bash shell inside
your MySQL container, from which you can manage your MySQL server directly. You
can run `exit` to return to your terminal.

1. Open the Docker Desktop Dashboard and select the **Containers** view.
2. In the **Actions** column for your container, select **Show container
  actions** and then select **Open in terminal**.

In this terminal you can access to the shell inside your MySQL container, from
which you can manage your MySQL server directly.

Once you've accessed the container's terminal, you can run any tools available
in that container. The following example shows using `mysql` in the container to
list the databases.

```console
# mysql -u root -p
Enter password: my-secret-pw

mysql> SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

## Connect to a containerized database from your host

Connecting to a containerized database from your host machine involves mapping a
port inside the container to a port on your host machine. This process ensures
that the database inside the container is accessible via the host machine's
network. For MySQL, the default port is 3306. By exposing this port, you can use
various database management tools or applications on your host machine to
interact with your MySQL database.

Before you begin, you must remove any containers you previously ran for this
guide. To stop and remove a container, either:

- In a terminal, run `docker rm --force my-mysql` to remove the container
  named `my-mysql`.
- Or, in the Docker Desktop Dashboard, select the **Delete** icon next to your
  container in the **Containers** view.

Next, you can use either the Docker Desktop GUI or CLI to run the container with
the port mapped.

Run the following command in a terminal.

```console
$ docker run -p 3307:3306 --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -d mysql:latest
```

In this command, `-p 3307:3306` maps port 3307 on the host to port 3306 in the container.

To verify the port is mapped, run the following command.

```console
$ docker ps
```

You should see output like the following.

```console
CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                               NAMES
6eb776cfd73c   mysql:latest   "docker-entrypoint.s…"   17 minutes ago   Up 17 minutes   33060/tcp, 0.0.0.0:3307->3306/tcp   my-mysql
```

To run a container using the GUI:

1. In the Docker Desktop Dashboard, select the global search at the top of the window.
2. Specify `mysql` in the search box, and select the `Images` tab if not already
  selected.
3. Hover over the `mysql` image and select `Run`.
  The **Run a new container** modal appears.
4. Expand **Optional settings**.
5. In the optional settings, specify the following:
  - **Container name**: `my-mysql`
  - **Host port** for the **3306/tcp** port: `3307`
  - **Environment variables**:
    - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
    - `MYSQL_DATABASE`:`mydb`
  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-2.webp)  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-2.webp)
6. Select `Run`.
7. In the **Containers** view, verify that the port is mapped under the
  **Port(s)** column. You should see **3307:3306** for the **my-mysql**
  container.

At this point, any application running on your host can access the MySQL service in the container at `localhost:3307`.

## Connect to a containerized database from another container

Connecting to a containerized database from another container is a common
scenario in microservices architecture and during development processes.
Docker's networking capabilities make it easy to establish this connection
without having to expose the database to the host network. This is achieved by
placing both the database container and the container that needs to access it on
the same Docker network.

Before you begin, you must remove any containers you previously ran for this
guide. To stop and remove a container, either:

- In a terminal, run `docker rm --force my-mysql` to remove the container
  named `my-mysql`.
- Or, in the Docker Desktop Dashboard, select the **Delete** icon next to your
  container in the **Containers** view.

To create a network and run containers on it:

1. Run the following command to create a Docker network named my-network.
  ```console
  $ docker network create my-network
  ```
2. Run your database container and specify the network using the `--network`
  option. This runs the container on the my-network network.
  ```console
  $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb --network my-network -d mysql:latest
  ```
3. Run your other containers and specify the network using the `--network`
  option. For this example, you'll run a phpMyAdmin container that can connect
  to your database.
  1. Run a phpMyAdmin container. Use the `--network` option to specify the
    network, the `-p` option to let you access the container from your host
    machine, and the `-e` option to specify a required environment variable
    for this image.
    ```console
    $ docker run --name my-phpmyadmin -d --network my-network -p 8080:80 -e PMA_HOST=my-mysql phpmyadmin
    ```
4. Verify that the containers can communicate. For this example, you'll access
  phpMyAdmin and verify that it connects to the database.
  1. Open [http://localhost:8080](http://localhost:8080) to access your phpMyAdmin container.
  2. Log in using `root` as the username and `my-secret-pw` as the password.
    You should connect to the MySQL server and see your database listed.

At this point, any application running on your `my-network` container network
can access the MySQL service in the container at `my-mysql:3306`.

## Persist database data in a volume

Persisting database data in a Docker volume is necessary for ensuring that your
data survives container restarts and removals. A Docker volume lets you store
database files outside the container's writable layer, making it possible to
upgrade the container, switch bases, and share data without losing it. Here’s
how you can attach a volume to your database container using either the Docker
CLI or the Docker Desktop GUI.

Before you begin, you must remove any containers you previously ran for this
guide. To stop and remove a container, either:

- In a terminal, run `docker rm --force my-mysql` to remove the container
  named `my-mysql`.
- Or, in the Docker Desktop Dashboard, select the **Delete** icon next to your
  container in the **Containers** view.

Next, you can use either the Docker Desktop GUI or CLI to run the container with a volume.

To run your database container with a volume attached, include the `-v` option
with your `docker run` command, specifying a volume name and the path where the
database stores its data inside the container. If the volume doesn't exist,
Docker automatically creates it for you.

To run a database container with a volume attached, and then verify that the
data persists:

1. Run the container and attach the volume.
  ```console
  $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=mydb -v my-db-volume:/var/lib/mysql -d mysql:latest
  ```
  This command mounts the volume named `my-db-volume` to the `/var/lib/mysql` directory in the container.
2. Create some data in the database. Use the `docker exec` command to run
  `mysql` inside the container and create a table.
  ```console
  $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES ('value');"
  ```
  This command uses the `mysql` tool in the container to create a table named
  `mytable` with a column named `column_name`, and finally inserts a value of
  `value`.
3. Stop and remove the container. Without a volume, the table you created would
  be lost when removing the container.
  ```console
  $ docker rm --force my-mysql
  ```
4. Start a new container with the volume attached. This time, you don't need to
  specify any environment variables as the configuration is saved in the
  volume.
  ```console
  $ docker run --name my-mysql -v my-db-volume:/var/lib/mysql -d mysql:latest
  ```
5. Verify that the table you created still exists. Use the `docker exec` command
  again to run `mysql` inside the container.
  ```console
  $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.mytable;"
  ```
  This command uses the `mysql` tool in the container to select all the
  records from the `mytable` table.
  You should see output like the following.
  ```console
  column_name
  value
  ```

To run a database container with a volume attached, and then verify that the
data persists:

1. Run a container with a volume attached.
  1. In the Docker Desktop Dashboard, select the global search at the top of the window.
  2. Specify `mysql` in the search box, and select the **Images** tab if not
    already selected.
  3. Hover over the **mysql** image and select **Run**.
    The **Run a new container** modal appears.
  4. Expand **Optional settings**.
  5. In the optional settings, specify the following:
    - **Container name**: `my-mysql`
    - **Environment variables**:
      - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
      - `MYSQL_DATABASE`:`mydb`
    - **Volumes**:
      - `my-db-volume`:`/var/lib/mysql`
    ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-3.webp)  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-3.webp)
    Here, the name of the volume is `my-db-volume` and it is mounted in the
    container at `/var/lib/mysql`.
  6. Select `Run`.
2. Create some data in the database.
  1. In the **Containers** view, next to your container select the **Show
    container actions** icon, and then select **Open in terminal**.
  2. Run the following command in the container's terminal to add a table.
    ```console
    # mysql -u root -pmy-secret-pw -e "CREATE TABLE IF NOT EXISTS mydb.mytable (column_name VARCHAR(255)); INSERT INTO mydb.mytable (column_name) VALUES ('value');"
    ```
    This command uses the `mysql` tool in the container to create a table
    named `mytable` with a column named `column_name`, and finally inserts a
    value of value`.
3. In the **Containers** view, select the **Delete** icon next to your
  container, and then select **Delete forever**. Without a volume, the table
  you created would be lost when deleting the container.
4. Run a container with a volume attached.
  1. In the Docker Desktop Dashboard, select the global search at the top of the window.
  2. Specify `mysql` in the search box, and select the **Images** tab if not
    already selected.
  3. Hover over the **mysql** image and select **Run**.
    The **Run a new container** modal appears.
  4. Expand **Optional settings**.
  5. In the optional settings, specify the following:
    - **Container name**: `my-mysql`
    - **Environment variables**:
      - `MYSQL_ROOT_PASSWORD`:`my-secret-pw`
      - `MYSQL_DATABASE`:`mydb`
    - **Volumes**:
      - `my-db-volume`:`/var/lib/mysql`
    ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-3.webp)  ![The optional settings screen with the options specified.](https://docs.docker.com/guides/images/databases-3.webp)
  6. Select `Run`.
5. Verify that the table you created still exists.
  1. In the **Containers** view, next to your container select the **Show
    container actions** icon, and then select **Open in terminal**.
  2. Run the following command in the container's terminal to verify that table
    you created still exists.
    ```console
    # mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.mytable;"
    ```
    This command uses the `mysql` tool in the container to select all the
    records from the `mytable` table.
    You should see output like the following.
    ```console
    column_name
    value
    ```

At this point, any MySQL container that mounts the `my-db-volume` will be able
to access and save persisted data.

## Build a customized database image

Customizing your database image lets you include additional configuration,
scripts, or tools alongside the base database server. This is particularly
useful for creating a Docker image that matches your specific development or
production environment needs. The following example outlines how to build and
run a custom MySQL image that includes a table initialization script.

Before you begin, you must remove any containers you previously ran for this
guide. To stop and remove a container, either:

- In a terminal, run `docker rm --force my-mysql` to remove the container
  named `my-mysql`.
- Or, in the Docker Desktop Dashboard, select the **Delete** icon next to your
  container in the **Containers** view.

To build and run your custom image:

1. Create a Dockerfile.
  1. Create a file named `Dockerfile` in your project directory. For this
    example, you can create the `Dockerfile` in an empty directory of your
    choice. This file will define how to build your custom MySQL image.
  2. Add the following content to the `Dockerfile`.
    ```dockerfile
    # syntax=docker/dockerfile:1
    # Use the base image mysql:latest
    FROM mysql:latest
    # Set environment variables
    ENV MYSQL_DATABASE mydb
    # Copy custom scripts or configuration files from your host to the container
    COPY ./scripts/ /docker-entrypoint-initdb.d/
    ```
    In this Dockerfile, you've set the environment variable for the MySQL
    database name. You can also use the `COPY` instruction to add custom
    configuration files or scripts into the container. In this
    example, files from your host's `./scripts/` directory are copied into the
    container's `/docker-entrypoint-initdb.d/` directory. In this directory,
    `.sh`, `.sql`, and `.sql.gz` scripts are executed when the container is
    started for the first time. For more details about Dockerfiles, see the
    [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).
  3. Create a script file to initialize a table in the database. In the
    directory where your `Dockerfile` is located, create a subdirectory named
    `scripts`, and then create a file named `create_table.sql` with the
    following content.
  ```text
  CREATE TABLE IF NOT EXISTS mydb.myothertable (
    column_name VARCHAR(255)
  );
  INSERT INTO mydb.myothertable (column_name) VALUES ('other_value');
  ```
  You should now have the following directory structure.
  ```text
  ├── your-project-directory/
  │ ├── scripts/
  │ │ └── create_table.sql
  │ └── Dockerfile
  ```
2. Build your image.
  1. In a terminal, change directory to the directory where your `Dockerfile`
    is located.
  2. Run the following command to build the image.
    ```console
    $ docker build -t my-custom-mysql .
    ```
    In this command, `-t my-custom-mysql` tags (names) your new image as
    `my-custom-mysql`. The period (.) at the end of the command specifies the
    current directory as the context for the build, where Docker looks for the
    Dockerfile and any other files needed for the build.
3. Run your image as you did in [Run a local containerized
  database](#run-a-local-containerized-database). This time, specify your
  image's name instead of `mysql:latest`. Also, you no longer need to specify
  the `MYSQL_DATABASE` environment variable as it's now defined by your
  Dockerfile.
  ```console
  $ docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d my-custom-mysql
  ```
4. Verify that your container is running with the following command.
  ```console
  $ docker ps
  ```
  You should see output like the following.
  ```console
  CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS          PORTS                 NAMES
  f74dcfdb0e59   my-custom-mysql   "docker-entrypoint.s…"    2 hours ago    Up 51 minutes   3306/tcp, 33060/tcp   my-mysql
  ```
5. Verify that your initialization script was ran. Run the following command in
  a terminal to show the contents of the `myothertable` table.
  ```console
  $ docker exec my-mysql mysql -u root -pmy-secret-pw -e "SELECT * FROM mydb.myothertable;"
  ```
  You should see output like the following.
  ```console
  column_name
  other_value
  ```

Any container ran using your `my-custom-mysql` image will have the table
initialized when first started.

## Use Docker Compose to run a database

Docker Compose is a tool for defining and running multi-container Docker
applications. With a single command, you can configure all your application's
services (like databases, web apps, etc.) and manage them. In this example,
you'll create a Compose file and use it to run a MySQL database container and a phpMyAdmin container.

To run your containers with Docker Compose:

1. Create a Docker Compose file.
  1. Create a file named `compose.yaml` in your project directory. This file
    will define the services, networks, and volumes.
  2. Add the following content to the `compose.yaml` file.
    ```yaml
    services:
      db:
        image: mysql:latest
        environment:
          MYSQL_ROOT_PASSWORD: my-secret-pw
          MYSQL_DATABASE: mydb
        ports:
          - 3307:3306
        volumes:
          - my-db-volume:/var/lib/mysql
      phpmyadmin:
        image: phpmyadmin/phpmyadmin:latest
        environment:
          PMA_HOST: db
          PMA_PORT: 3306
          MYSQL_ROOT_PASSWORD: my-secret-pw
        ports:
          - 8080:80
        depends_on:
          - db
    volumes:
      my-db-volume:
    ```
    For the database service:
    - `db` is the name of the service.
    - `image: mysql:latest` specifies that the service uses the latest MySQL
      image from Docker Hub.
    - `environment` lists the environment variables used by MySQL to
      initialize the database, such as the root password and the database
      name.
    - `ports` maps port 3307 on the host to port 3306 in the container,
      allowing you to connect to the database from your host machine.
    - `volumes` mounts `my-db-volume` to `/var/lib/mysql` inside the container
      to persist database data.
    In addition to the database service, there is a phpMyAdmin service. By
    default Compose sets up a single network for your app. Each container for
    a service joins the default network and is both reachable by other
    containers on that network, and discoverable by the service's name.
    Therefore, in the `PMA_HOST` environment variable, you can specify the
    service name, `db`, in order to connect to the database service. For more details about Compose, see the
    [Compose file reference](https://docs.docker.com/reference/compose-file/).
2. Run Docker Compose.
  1. Open a terminal and change directory to the directory where your
    `compose.yaml` file is located.
  2. Run Docker Compose using the following command.
    ```console
    $ docker compose up
    ```
    You can now access phpMyAdmin at
    [http://localhost:8080](http://localhost:8080) and connect to your
    database using `root` as the username and `my-secret-pw` as the password.
  3. To stop the containers, press `ctrl`+`c` in the terminal.

Now, with Docker Compose you can start your database and app, mount volumes,
configure networking, and more, all with a single command.

## Summary

This guide introduced you to the essentials of using containerized databases,
specifically focusing on MySQL, to enhance flexibility, ease of setup, and
consistency across your development environments. The use-cases covered in
this guide not only streamline your development workflows but also prepare you
for more advanced database management and deployment scenarios, ensuring your
data-driven applications remain robust and scalable.

Related information:

- [Docker Hub database images](https://hub.docker.com/search?q=database&type=image)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Database samples](https://docs.docker.com/reference/samples/#databases)

---

# Configure CI/CD for your Deno application

> Learn how to configure CI/CD using GitHub Actions for your Deno application.

# Configure CI/CD for your Deno application

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a Deno application](https://docs.docker.com/guides/deno/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

## Overview

In this section, you'll learn how to set up and use GitHub Actions to build and test your Docker image as well as push it to Docker Hub. You will complete the following steps:

1. Create a new repository on GitHub.
2. Define the GitHub Actions workflow.
3. Run the workflow.

## Step one: Create the repository

Create a GitHub repository, configure the Docker Hub credentials, and push your source code.

1. [Create a new repository](https://github.com/new) on GitHub.
2. Open the repository **Settings**, and go to **Secrets and variables** >
  **Actions**.
3. Create a new **Repository variable** named `DOCKER_USERNAME` and your Docker ID as a value.
4. Create a new
  [Personal Access Token (PAT)](https://docs.docker.com/security/access-tokens/#create-an-access-token)for Docker Hub. You can name this token `docker-tutorial`. Make sure access permissions include Read and Write.
5. Add the PAT as a **Repository secret** in your GitHub repository, with the name
  `DOCKERHUB_TOKEN`.
6. In your local repository on your machine, run the following command to change
  the origin to the repository you just created. Make sure you change
  `your-username` to your GitHub username and `your-repository` to the name of
  the repository you created.
  ```console
  $ git remote set-url origin https://github.com/your-username/your-repository.git
  ```
7. Run the following commands to stage, commit, and push your local repository to GitHub.
  ```console
  $ git add -A
  $ git commit -m "my commit"
  $ git push -u origin main
  ```

## Step two: Set up the workflow

Set up your GitHub Actions workflow for building and pushing the image
to Docker Hub.

1. Go to your repository on GitHub and then select the **Actions** tab.
2. Select **set up a workflow yourself**.
  This takes you to a page for creating a new GitHub actions workflow file in
  your repository, under `.github/workflows/main.yml` by default.
3. In the editor window, copy and paste the following YAML configuration and commit the changes.
  ```yaml
  name: ci
  on:
    push:
      branches:
        - main
  jobs:
    build:
      runs-on: ubuntu-latest
      steps:
        -
          name: Login to Docker Hub
          uses: docker/login-action@v3
          with:
            username: ${{ vars.DOCKER_USERNAME }}
            password: ${{ secrets.DOCKERHUB_TOKEN }}
        -
          name: Set up Docker Buildx
          uses: docker/setup-buildx-action@v3
        -
          name: Build and push
          uses: docker/build-push-action@v6
          with:
            platforms: linux/amd64,linux/arm64
            push: true
            tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
  ```
  For more information about the YAML syntax for `docker/build-push-action`,
  refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

## Step three: Run the workflow

Save the workflow file and run the job.

1. Select **Commit changes...** and push the changes to the `main` branch.
  After pushing the commit, the workflow starts automatically.
2. Go to the **Actions** tab. It displays the workflow.
  Selecting the workflow shows you the breakdown of all the steps.
3. When the workflow is complete, go to your
  [repositories on Docker Hub](https://hub.docker.com/repositories).
  If you see the new repository in that list, it means the GitHub Actions
  successfully pushed the image to Docker Hub.

## Summary

In this section, you learned how to set up a GitHub Actions workflow for your Deno application.

Related information:

- [Introduction to GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Next steps

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

---

# Containerize a Deno application

> Learn how to containerize a Deno application.

# Containerize a Deno application

   Table of contents

---

## Prerequisites

- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## Overview

For a long time, Node.js has been the go-to runtime for server-side JavaScript applications. However, recent years have introduced new alternative runtimes, including [Deno](https://deno.land/). Like Node.js, Deno is a JavaScript and TypeScript runtime, but it takes a fresh approach with modern security features, a built-in standard library, and native support for TypeScript.

Why develop Deno applications with Docker? Having a choice of runtimes is exciting, but managing multiple runtimes and their dependencies consistently across environments can be tricky. This is where Docker proves invaluable. Using containers to create and destroy environments on demand simplifies runtime management and ensures consistency. Additionally, as Deno continues to grow and evolve, Docker helps establish a reliable and reproducible development environment, minimizing setup challenges and streamlining the workflow.

## Get the sample application

Clone the sample application to use with this guide. Open a terminal, change
directory to a directory that you want to work in, and run the following
command to clone the repository:

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

You should now have the following contents in your `deno-docker` directory.

```text
├── deno-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── server.ts
│ └── README.md
```

## Understand the sample application

The sample application is a simple Deno application that uses the Oak framework to create a simple API that returns a JSON response. The application listens on port 8000 and returns a message `{"Status" : "OK"}` when you access the application in a browser.

```typescript
// server.ts
import { Application, Router } from "https://deno.land/x/oak@v12.0.0/mod.ts";

const app = new Application();
const router = new Router();

// Define a route that returns JSON
router.get("/", (context) => {
  context.response.body = { Status: "OK" };
  context.response.type = "application/json";
});

app.use(router.routes());
app.use(router.allowedMethods());

console.log("Server running on http://localhost:8000");
await app.listen({ port: 8000 });
```

## Create a Dockerfile

Before creating a Dockerfile, you need to choose a base image. You can either use the [Deno Docker Official Image](https://hub.docker.com/r/denoland/deno) or a Docker Hardened Image (DHI) from the [Hardened Image catalog](https://hub.docker.com/hardened-images/catalog).

Choosing DHI offers the advantage of a production-ready image that is lightweight and secure. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

Docker Hardened Images (DHIs) are available for Deno in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/deno). You can pull DHIs directly from the `dhi.io` registry.

1. Sign in to the DHI registry:
  ```console
  $ docker login dhi.io
  ```
2. Pull the Deno DHI as `dhi.io/deno:2`. The tag (`2`) in this example refers to the version to the latest 2.x version of Deno.
  ```console
  $ docker pull dhi.io/deno:2
  ```

For other available versions, refer to the [catalog](https://hub.docker.com/hardened-images/catalog/dhi/deno).

```dockerfile
# Use the DHI Deno image as the base image
FROM dhi.io/deno:2

# Set the working directory
WORKDIR /app

# Copy server code into the container
COPY server.ts .

# Set permissions (optional but recommended for security)
USER deno

# Expose port 8000
EXPOSE 8000

# Run the Deno server
CMD ["run", "--allow-net", "server.ts"]
```

Using the Docker Official Image is straightforward. In the following Dockerfile, you'll notice that the `FROM` instruction uses `denoland/deno:latest` as the base image.

This is the official image for Deno. This image is [available on the Docker Hub](https://hub.docker.com/r/denoland/deno).

```dockerfile
# Use the official Deno image
FROM denoland/deno:latest

# Set the working directory
WORKDIR /app

# Copy server code into the container
COPY server.ts .

# Set permissions (optional but recommended for security)
USER deno

# Expose port 8000
EXPOSE 8000

# Run the Deno server
CMD ["run", "--allow-net", "server.ts"]
```

In addition to specifying the base image, the Dockerfile also:

- Sets the working directory in the container to `/app`.
- Copies `server.ts` into the container.
- Sets the user to `deno` to run the application as a non-root user.
- Exposes port 8000 to allow traffic to the application.
- Runs the Deno server using the `CMD` instruction.
- Uses the `--allow-net` flag to allow network access to the application. The `server.ts` file uses the Oak framework to create a simple API that listens on port 8000.

## Run the application

Make sure you are in the `deno-docker` directory. Run the following command in a terminal to build and run the application.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8000](http://localhost:8000). You will see a message `{"Status" : "OK"}` in the browser.

In the terminal, press `ctrl`+`c` to stop the application.

### Run the application in the background

You can run the application detached from the terminal by adding the `-d`
option. Inside the `deno-docker` directory, run the following command
in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at [http://localhost:8000](http://localhost:8000).

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

## Summary

In this section, you learned how you can containerize and run your Deno
application using Docker.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore file](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [Docker Compose overview](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Docker Hardened Images](https://docs.docker.com/dhi/)

## Next steps

In the next section, you'll learn how you can develop your application using
containers.
