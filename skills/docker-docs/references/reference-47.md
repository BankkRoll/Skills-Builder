# Glossary and more

# Glossary

> Glossary of terms used around Docker

# Glossary

> Tip
>
> Looking for a definition that's not listed or need a more context-aware
> explanation?
>
>
>
> Try .

| Term | Definition |
| --- | --- |
| Docker CLI | The Docker CLI is the command-line interface for interacting with the Docker
Engine. It provides commands likedocker run,docker build,docker ps,
and others to manage Docker containers, images, and services. |
| Docker Compose | Docker Compose is a tool for defining and running multi-container Docker
applications using a YAML file (compose.yaml). With a single command, you
can start all services defined in the configuration. |
| Docker Desktop | Docker Desktop is an easy-to-install application for Windows, macOS, and Linux
that provides a local Docker development environment. It includes Docker
Engine, Docker CLI, Docker Compose, and a Kubernetes cluster. |
| Docker Engine | Docker Engine is the client-server technology that creates and runs Docker
containers. It includes the Docker daemon (dockerd), REST API, and the
Docker CLI client. |
| Docker Hub | Docker Hub is Docker’s public registry service where users can store, share,
and manage container images. It hosts Docker Official Images, Verified
Publisher content, and community-contributed images. |
| base image | A base image is an image you designate in aFROMdirective in a Dockerfile.
It defines the starting point for your build.
Dockerfile instructions create additional layers on top of the base image.
A Dockerfile with theFROM scratchdirective uses an empty base image. |
| build | Build is the process of building Docker images using a Dockerfile. The build
uses a Dockerfile and a "context". The context is the set of files in the
directory in which the image is built. |
| container | A container is a runnable instance of an image. You can start, stop, move, or
delete a container using the Docker CLI or API. Containers are isolated from
one another and the host system but share the OS kernel. They provide a
lightweight and consistent way to run applications. |
| context | A Docker context contains endpoint configuration for the Docker CLI to connect
to different Docker environments, such as remote Docker hosts or Docker
Desktop. Usedocker context useto switch between contexts. |
| image | An image is a read-only template used to create containers. It typically
includes a base operating system and application code packaged together using
a Dockerfile. Images are versioned using tags and can be pushed to or pulled
from a container registry like Docker Hub. |
| layer | In an image, a layer is a modification represented by an instruction in the
Dockerfile. Layers are applied in sequence to the base image to create the
final image. Unchanged layers are cached, making image builds faster and more
efficient. |
| multi-architecture image | A multi-architecture image is a Docker image that supports multiple CPU
architectures, likeamd64orarm64. Docker automatically pulls the correct
architecture image for your platform when using a multi-arch image. |
| persistent storage | Persistent storage or volume storage provides a way for containers to retain
data beyond their lifecycle. This storage can exist on the host machine or an
external storage system and is not tied to the container's runtime. |
| registry | A registry is a storage and content delivery system for Docker images. The
default public registry is Docker Hub, but you can also set up private
registries using Docker Distribution. |
| volume | A volume is a special directory within a container that bypasses the Union
File System. Volumes are designed to persist data independently of the
container lifecycle. Docker supports host, anonymous, and named volumes. |

---

# Agentic AI samples

> Docker samples for agentic AI.

# Agentic AI samples

| Name | Description |
| --- | --- |
| Agent-to-Agent | This app is a modular AI agent runtime built on Google's Agent Development Kit (ADK) and the A2A (Agent-to-Agent) protocol. It wraps a large language model (LLM)-based agent in an HTTP API and uses structured execution flows with streaming responses, memory, and tools. It is designed to make agents callable as network services and composable with other agents. |
| ADK Multi-Agent Fact Checker | This project demonstrates a collaborative multi-agent system built with the Agent Development Kit (ADK), where a top-level Auditor agent coordinates the workflow to verify facts. The Critic agent gathers evidence via live internet searches using DuckDuckGo through the Model Context Protocol (MCP), while the Reviser agent analyzes and refines the conclusion using internal reasoning alone. The system showcases how agents with distinct roles and tools can collaborate under orchestration. |
| DevDuck agents | A multi-agent system for Go programming assistance built with Google Agent Development Kit (ADK). This project features a coordinating agent (DevDuck) that manages two specialized sub-agents (Bob and Cerebras) for different programming tasks. |
| Agno | This app is a multi-agent orchestration system powered by LLMs (like Qwen and OpenAI) and connected to tools via a Model Control Protocol (MCP) gateway. Its purpose is to retrieve, summarize, and document GitHub issues—automatically creating Notion pages from the summaries. It also supports file content summarization from GitHub. |
| CrewAI | This project showcases an autonomous, multi-agent virtual marketing team built with CrewAI. It automates the creation of a high-quality, end-to-end marketing strategy — from research to copywriting — using task delegation, web search, and creative synthesis. |
| SQL Agent with LangGraph | This project demonstrates a zero-config AI agent that uses LangGraph to answer natural language questions by querying a SQL database — all orchestrated with Docker Compose. |
| Langchaingo Brave Search Example - Model Context Protocol (MCP) | This example demonstrates how to create a Go Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses the official Go SDK for Model Context Protocol servers and clients, to set up the MCP client. |
| Spring AI Brave Search Example - Model Context Protocol (MCP) | This example demonstrates how to create a Spring AI Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses Spring Boot autoconfiguration to set up the MCP client through configuration files. |
| MCP UI with Vercel AI SDK | Start an MCP UI application that uses the Vercel AI SDK to provide a chat interface for local models, provided by the Docker Model Runner, with access to MCPs from the Docker MCP Catalog. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# AI/ML samples

> Docker samples for AI/ML.

# AI/ML samples

| Name | Description |
| --- | --- |
| AI/ML with Docker | Get started with AI and ML using Docker, Neo4j, LangChain, and Ollama |
| Agent-to-Agent | This app is a modular AI agent runtime built on Google's Agent Development Kit (ADK) and the A2A (Agent-to-Agent) protocol. It wraps a large language model (LLM)-based agent in an HTTP API and uses structured execution flows with streaming responses, memory, and tools. It is designed to make agents callable as network services and composable with other agents. |
| ADK Multi-Agent Fact Checker | This project demonstrates a collaborative multi-agent system built with the Agent Development Kit (ADK), where a top-level Auditor agent coordinates the workflow to verify facts. The Critic agent gathers evidence via live internet searches using DuckDuckGo through the Model Context Protocol (MCP), while the Reviser agent analyzes and refines the conclusion using internal reasoning alone. The system showcases how agents with distinct roles and tools can collaborate under orchestration. |
| DevDuck agents | A multi-agent system for Go programming assistance built with Google Agent Development Kit (ADK). This project features a coordinating agent (DevDuck) that manages two specialized sub-agents (Bob and Cerebras) for different programming tasks. |
| Agno | This app is a multi-agent orchestration system powered by LLMs (like Qwen and OpenAI) and connected to tools via a Model Control Protocol (MCP) gateway. Its purpose is to retrieve, summarize, and document GitHub issues—automatically creating Notion pages from the summaries. It also supports file content summarization from GitHub. |
| CrewAI | This project showcases an autonomous, multi-agent virtual marketing team built with CrewAI. It automates the creation of a high-quality, end-to-end marketing strategy — from research to copywriting — using task delegation, web search, and creative synthesis. |
| SQL Agent with LangGraph | This project demonstrates a zero-config AI agent that uses LangGraph to answer natural language questions by querying a SQL database — all orchestrated with Docker Compose. |
| Langchaingo Brave Search Example - Model Context Protocol (MCP) | This example demonstrates how to create a Go Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses the official Go SDK for Model Context Protocol servers and clients, to set up the MCP client. |
| Spring AI Brave Search Example - Model Context Protocol (MCP) | This example demonstrates how to create a Spring AI Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses Spring Boot autoconfiguration to set up the MCP client through configuration files. |
| MCP UI with Vercel AI SDK | Start an MCP UI application that uses the Vercel AI SDK to provide a chat interface for local models, provided by the Docker Model Runner, with access to MCPs from the Docker MCP Catalog. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Angular samples

> Docker samples for Angular.

# Angular samples

| Name | Description |
| --- | --- |
| Angular | A sample Angular application. |
| dotnet-album-viewer | West Wind Album Viewer ASP.NET Core and Angular sample. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Cloudflared samples

> Docker samples for cloudflared.

# Cloudflared samples

| Name | Description |
| --- | --- |
| Pi-hole / cloudflared | A sample Pi-hole setup with use of DoH cloudflared service. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Django samples

> Docker samples for Django.

# Django samples

| Name | Description |
| --- | --- |
| Django | A sample Django application. |
| Compose and Django | This quick-start guide demonstrates how to use Docker Compose to set up and run a simple Django/PostgreSQL app. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# .NET samples

> Docker samples for .NET.

# .NET samples

| Name | Description |
| --- | --- |
| ASP.NET / MS-SQL | A sample ASP.NET core application with MS SQL server database. |
| NGINX / ASP.NET / MySQL | A sample Nginx reverse proxy with a C# backend using ASP.NET. |
| example-voting-app | A sample Docker Compose app. |
| dotnet-album-viewer | West Wind Album Viewer ASP.NET Core and Angular sample. |
| aspnet-monitoring | Monitoring ASP.NET Fx applications in Windows Docker containers, using Prometheus. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Elasticsearch / Logstash / Kibana samples

> Docker samples for Elasticsearch, Logstash, and Kibana.

# Elasticsearch / Logstash / Kibana samples

| Name | Description |
| --- | --- |
| Elasticsearch / Logstash / Kibana | A sample Elasticsearch, Logstash, and Kibana stack. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Express samples

> Docker samples for Express.

# Express samples

| Name | Description |
| --- | --- |
| React / Express / MySQL | A sample React application with a Node.js backend and a MySQL database. |
| React / Express / MongoDB | A sample React application with a Node.js backend and a Mongo database. |
| slack-clone-docker | A sample Slack Clone app built with the MERN stack. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# FastAPI samples

> Docker samples for .NET.

# FastAPI samples

| Name | Description |
| --- | --- |
| FastAPI | A sample FastAPI application. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Flask samples

> Docker samples for Flask.

# Flask samples

| Name | Description |
| --- | --- |
| NGINX / Flask / MongoDB | A sample Python/Flask application with Nginx proxy and a Mongo database. |
| NGINX / Flask / MySQL | A sample Python/Flask application with an Nginx proxy and a MySQL database. |
| NGINX / WSGI / Flask | A sample Nginx reverse proxy with a Flask backend using WSGI. |
| Python / Flask / Redis | A sample Python/Flask and a Redis database. |
| Flask | A sample Flask application. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Gitea samples

> Docker samples for Gitea.

# Gitea samples

| Name | Description |
| --- | --- |
| Gitea / PostgreSQL | A sample setup for Gitea. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Go samples

> Docker samples for Go.

# Go samples

| Name | Description |
| --- | --- |
| Go / NGINX / MySQL | A sample Go application with an Nginx proxy and a MySQL database. |
| Go / NGINX / PostgreSQL | A sample Go application with an Nginx proxy and a PostgreSQL database. |
| NGINX / Go | A sample Nginx proxy with a Go backend. |
| Traefik | A sample Traefik proxy with a Go backend. |
| wordsmith | A demo app that runs three containers, including PostgreSQL, Java, and Go. |
| gopher-task-system | A Task System using Go Docker SDK. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Java samples

> Docker samples for Java.

# Java samples

| Name | Description |
| --- | --- |
| Java Spark / MySQL | A sample Java application and a MySQL database. |
| React / Spring / MySQL | A sample React application with a Spring backend and a MySQL database. |
| Spring / PostgreSQL | A sample Java application with Spring framework and a Postgres database. |
| Spark | A sample Spark application. |
| example-voting-app | A sample Docker Compose app. |
| atsea-sample-shop-app | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| wordsmith | A demo app that runs three containers, including PostgreSQL, Java, and Go. |
| Spring AI Brave Search Example - Model Context Protocol (MCP) | This example demonstrates how to create a Spring AI Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses Spring Boot autoconfiguration to set up the MCP client through configuration files. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# JavaScript samples

> Docker samples for JavaScript.

# JavaScript samples

| Name | Description |
| --- | --- |
| NGINX / Node.js / Redis | A sample Node.js application with Nginx proxy and a Redis database. |
| React / Spring / MySQL | A sample React application with a Spring backend and a MySQL database. |
| React / Express / MySQL | A sample React application with a Node.js backend and a MySQL database. |
| React / Express / MongoDB | A sample React application with a Node.js backend and a Mongo database. |
| React / Rust / PostgreSQL | A sample React application with a Rust backend and a Postgres database. |
| React / NGINX | A sample React application with Nginx. |
| VueJS | A sample Vue.js application. |
| docker-swarm-visualizer | A visualizer for Docker Swarm Mode using the Docker Remote API, Node.JS, and D3. |
| atsea-sample-shop-app | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| dotnet-album-viewer | West Wind Album Viewer ASP.NET Core and Angular sample. |
| aspnet-monitoring | Monitoring ASP.NET Fx applications in Windows Docker containers, using Prometheus. |
| slack-clone-docker | A sample Slack Clone app built with the MERN stack. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# MariaDB samples

> Docker samples for MariaDB.

# MariaDB samples

| Name | Description |
| --- | --- |
| Nextcloud / Redis / MariaDB | A sample Nextcloud setup. |
| Compose and WordPress | This quick-start guide demonstrates how to use Compose to set up and run WordPress. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Minecraft samples

> Docker samples for Minecraft.

# Minecraft samples

| Name | Description |
| --- | --- |
| Minecraft server | A sample Minecraft server. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# MongoDB samples

> Docker samples for MongoDB.

# MongoDB samples

| Name | Description |
| --- | --- |
| NGINX / Flask / MongoDB | A sample Python/Flask application with Nginx proxy and a Mongo database. |
| React / Express / MongoDB | A sample React application with a Node.js backend and a Mongo database. |
| slack-clone-docker | A sample Slack Clone app built with the MERN stack. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# MS

> Docker samples for MS-SQL.

# MS-SQL samples

| Name | Description |
| --- | --- |
| ASP.NET / MS-SQL | A sample ASP.NET core application with MS SQL server database. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# MySQL samples

> Docker samples for MySQL.

# MySQL samples

| Name | Description |
| --- | --- |
| Go / NGINX / MySQL | A sample Go application with an Nginx proxy and a MySQL database. |
| Java Spark / MySQL | A sample Java application and a MySQL database. |
| NGINX / ASP.NET / MySQL | A sample Nginx reverse proxy with a C# backend using ASP.NET. |
| NGINX / Flask / MySQL | A sample Python/Flask application with an Nginx proxy and a MySQL database. |
| React / Spring / MySQL | A sample React application with a Spring backend and a MySQL database. |
| React / Express / MySQL | A sample React application with a Node.js backend and a MySQL database. |
| WordPress / MySQL | A sample WordPress setup. |
| dotnet-album-viewer | West Wind Album Viewer ASP.NET Core and Angular sample. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Nextcloud samples

> Docker samples for Nextcloud.

# Nextcloud samples

| Name | Description |
| --- | --- |
| Nextcloud / PostgreSQL | A sample Nextcloud setup. |
| Nextcloud / Redis / MariaDB | A sample Nextcloud setup. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# NGINX samples

> Docker samples for NGINX.

# NGINX samples

| Name | Description |
| --- | --- |
| Go / NGINX / MySQL | A sample Go application with an Nginx proxy and a MySQL database. |
| Go / NGINX / PostgreSQL | A sample Go application with an Nginx proxy and a PostgreSQL database. |
| NGINX / ASP.NET / MySQL | A sample Nginx reverse proxy with a C# backend using ASP.NET. |
| NGINX / Flask / MongoDB | A sample Python/Flask application with Nginx proxy and a Mongo database. |
| NGINX / Flask / MySQL | A sample Python/Flask application with an Nginx proxy and a MySQL database. |
| NGINX / Node.js / Redis | A sample Node.js application with Nginx proxy and a Redis database. |
| NGINX / Go | A sample Nginx proxy with a Go backend. |
| NGINX / WSGI / Flask | A sample Nginx reverse proxy with a Flask backend using WSGI. |
| React / NGINX | A sample React application with Nginx. |
| atsea-sample-shop-app | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| linux_tweet_app | A very simple webapp based on NGINX. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Node.js samples

> Docker samples for Node.js.

# Node.js samples

| Name | Description |
| --- | --- |
| NGINX / Node.js / Redis | A sample Node.js application with Nginx proxy and a Redis database. |
| React / Express / MySQL | A sample React application with a Node.js backend and a MySQL database. |
| React / Express / MongoDB | A sample React application with a Node.js backend and a Mongo database. |
| example-voting-app | A sample Docker Compose app. |
| slack-clone-docker | A sample Slack Clone app built with the MERN stack. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# PHP samples

> Docker samples for PHP.

# PHP samples

| Name | Description |
| --- | --- |
| PHP | A sample PHP application. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Pi

> Docker samples for Pi-hole.

# Pi-hole samples

| Name | Description |
| --- | --- |
| Pi-hole / cloudflared | A sample Pi-hole setup with use of DoH cloudflared service. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Plex samples

> Docker samples for Plex.

# Plex samples

| Name | Description |
| --- | --- |
| Plex | A sample Plex setup. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Portainer samples

> Docker samples for Portainer.

# Portainer samples

| Name | Description |
| --- | --- |
| Portainer | A sample Portainer setup. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# PostgreSQL samples

> Docker samples for PostgreSQL.

# PostgreSQL samples

| Name | Description |
| --- | --- |
| Go / NGINX / PostgreSQL | A sample Go application with an Nginx proxy and a PostgreSQL database. |
| PostgreSQL / pgAdmin | A sample setup for postgreSQL database with pgAdmin web interface. |
| React / Rust / PostgreSQL | A sample React application with a Rust backend and a Postgres database. |
| Spring / PostgreSQL | A sample Java application with Spring framework and a Postgres database. |
| Nextcloud / PostgreSQL | A sample Nextcloud setup. |
| example-voting-app | A sample Docker Compose app. |
| atsea-sample-shop-app | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| wordsmith | A demo app that runs three containers, including PostgreSQL, Java, and Go. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Prometheus samples

> Docker samples for Prometheus.

# Prometheus samples

| Name | Description |
| --- | --- |
| Prometheus / Grafana | A sample Prometheus and Grafana stack. |
| aspnet-monitoring | Monitoring ASP.NET Fx applications in Windows Docker containers, using Prometheus. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Python samples

> Docker samples for Python.

# Python samples

| Name | Description |
| --- | --- |
| NGINX / Flask / MongoDB | A sample Python/Flask application with Nginx proxy and a Mongo database. |
| NGINX / Flask / MySQL | A sample Python/Flask application with an Nginx proxy and a MySQL database. |
| NGINX / WSGI / Flask | A sample Nginx reverse proxy with a Flask backend using WSGI. |
| Python / Flask / Redis | A sample Python/Flask and a Redis database. |
| Flask | A sample Flask application. |
| Django | A sample Django application. |
| FastAPI | A sample FastAPI application. |
| example-voting-app | A sample Docker Compose app. |
| Compose and Django | This quick-start guide demonstrates how to use Docker Compose to set up and run a simple Django/PostgreSQL app. |
| AI/ML with Docker | Get started with AI and ML using Docker, Neo4j, LangChain, and Ollama |
| Agent-to-Agent | This app is a modular AI agent runtime built on Google's Agent Development Kit (ADK) and the A2A (Agent-to-Agent) protocol. It wraps a large language model (LLM)-based agent in an HTTP API and uses structured execution flows with streaming responses, memory, and tools. It is designed to make agents callable as network services and composable with other agents. |
| ADK Multi-Agent Fact Checker | This project demonstrates a collaborative multi-agent system built with the Agent Development Kit (ADK), where a top-level Auditor agent coordinates the workflow to verify facts. The Critic agent gathers evidence via live internet searches using DuckDuckGo through the Model Context Protocol (MCP), while the Reviser agent analyzes and refines the conclusion using internal reasoning alone. The system showcases how agents with distinct roles and tools can collaborate under orchestration. |
| DevDuck agents | A multi-agent system for Go programming assistance built with Google Agent Development Kit (ADK). This project features a coordinating agent (DevDuck) that manages two specialized sub-agents (Bob and Cerebras) for different programming tasks. |
| Agno | This app is a multi-agent orchestration system powered by LLMs (like Qwen and OpenAI) and connected to tools via a Model Control Protocol (MCP) gateway. Its purpose is to retrieve, summarize, and document GitHub issues—automatically creating Notion pages from the summaries. It also supports file content summarization from GitHub. |
| CrewAI | This project showcases an autonomous, multi-agent virtual marketing team built with CrewAI. It automates the creation of a high-quality, end-to-end marketing strategy — from research to copywriting — using task delegation, web search, and creative synthesis. |
| SQL Agent with LangGraph | This project demonstrates a zero-config AI agent that uses LangGraph to answer natural language questions by querying a SQL database — all orchestrated with Docker Compose. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.

---

# Rails samples

> Docker samples for Rails.

# Rails samples

| Name | Description |
| --- | --- |
| Compose and Rails | This Quickstart guide shows you how to use Docker Compose to set up and run a Rails/PostgreSQL app. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

- [Awesome Compose](https://github.com/docker/awesome-compose):
  A curated repository containing over 30 Docker Compose samples. These
  samples offer a starting point for how to integrate different services
  using a Compose file.
- [Docker Samples](https://github.com/dockersamples?q=&type=all&language=&sort=stargazers):
  A collection of over 30 repositories that offer sample containerized
  demo applications, tutorials, and labs.
