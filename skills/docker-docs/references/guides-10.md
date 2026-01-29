# Containerize a generative AI application and more

# Containerize a generative AI application

> Learn how to containerize a generative AI (GenAI) application.

# Containerize a generative AI application

   Table of contents

---

## Prerequisites

> Note
>
> GenAI applications can often benefit from GPU acceleration. Currently Docker Desktop supports GPU acceleration only on
> [Windows with the WSL2 backend](https://docs.docker.com/desktop/features/gpu/#using-nvidia-gpus-with-wsl2). Linux users can also access GPU acceleration using a native installation of the
> [Docker Engine](https://docs.docker.com/engine/install/).

- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/) or, if you are a Linux user and are planning to use GPU acceleration,
  [Docker Engine](https://docs.docker.com/engine/install/). Docker adds new features regularly and some parts of this guide may work only with the latest version of Docker Desktop.
- You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

## Overview

This section walks you through containerizing a generative AI (GenAI) application using Docker Desktop.

> Note
>
> You can see more samples of containerized GenAI applications in the [GenAI Stack](https://github.com/docker/genai-stack) demo applications.

## Get the sample application

The sample application used in this guide is a modified version of the PDF Reader application from the [GenAI Stack](https://github.com/docker/genai-stack) demo applications. The application is a full stack Python application that lets you ask questions about a PDF file.

The application uses [LangChain](https://www.langchain.com/) for orchestration, [Streamlit](https://streamlit.io/) for the UI, [Ollama](https://ollama.ai/) to run the LLM, and [Neo4j](https://neo4j.com/) to store vectors.

Clone the sample application. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/craig-osterhout/docker-genai-sample
```

You should now have the following files in your `docker-genai-sample` directory.

```text
├── docker-genai-sample/
│ ├── .gitignore
│ ├── app.py
│ ├── chains.py
│ ├── env.example
│ ├── requirements.txt
│ ├── util.py
│ ├── LICENSE
│ └── README.md
```

## Initialize Docker assets

Now that you have an application, you can use `docker init` to create the necessary Docker assets to containerize your application. Inside the `docker-genai-sample` directory, run the `docker init` command. `docker init` provides some default configuration, but you'll need to answer a few questions about your application. For example, this application uses Streamlit to run. Refer to the following `docker init` example and use the same answers for your prompts.

```console
$ docker init
Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use? Python
? What version of Python do you want to use? 3.11.4
? What port do you want your app to listen on? 8000
? What is the command to run your app? streamlit run app.py --server.address=0.0.0.0 --server.port=8000
```

You should now have the following contents in your `docker-genai-sample`
directory.

```text
├── docker-genai-sample/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── app.py
│ ├── chains.py
│ ├── compose.yaml
│ ├── env.example
│ ├── requirements.txt
│ ├── util.py
│ ├── Dockerfile
│ ├── LICENSE
│ ├── README.Docker.md
│ └── README.md
```

To learn more about the files that `docker init` added, see the following:

- [Dockerfile](https://docs.docker.com/reference/dockerfile/)
- [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
- [compose.yaml](https://docs.docker.com/reference/compose-file/)

## Run the application

Inside the `docker-genai-sample` directory, run the following command in a
terminal.

```console
$ docker compose up --build
```

Docker builds and runs your application. Depending on your network connection, it may take several minutes to download all the dependencies. You'll see a message like the following in the terminal when the application is running.

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8000
server-1  |
```

Open a browser and view the application at [http://localhost:8000](http://localhost:8000). You should see a simple Streamlit application. The application may take a few minutes to download the embedding model. While the download is in progress, **Running** appears in the top-right corner.

The application requires a Neo4j database service and an LLM service to
function. If you have access to services that you ran outside of Docker, specify
the connection information and try it out. If you don't have the services
running, continue with this guide to learn how you can run some or all of these
services with Docker.

In the terminal, press `ctrl`+`c` to stop the application.

## Summary

In this section, you learned how you can containerize and run your GenAI
application using Docker.

Related information:

- [docker init CLI reference](https://docs.docker.com/reference/cli/docker/init/)

## Next steps

In the next section, you'll learn how you can run your application, database, and LLM service all locally using Docker.

---

# Use containers for generative AI development

> Learn how to develop your generative AI (GenAI) application locally.

# Use containers for generative AI development

   Table of contents

---

## Prerequisites

Complete [Containerize a generative AI application](https://docs.docker.com/guides/genai-pdf-bot/containerize/).

## Overview

In this section, you'll learn how to set up a development environment to access all the services that your generative AI (GenAI) application needs. This includes:

- Adding a local database
- Adding a local or remote LLM service

> Note
>
> You can see more samples of containerized GenAI applications in the [GenAI Stack](https://github.com/docker/genai-stack) demo applications.

## Add a local database

You can use containers to set up local services, like a database. In this section, you'll update the `compose.yaml` file to define a database service. In addition, you'll specify an environment variables file to load the database connection information rather than manually entering the information every time.

To run the database service:

1. In the cloned repository's directory, rename `env.example` file to `.env`.
  This file contains the environment variables that the containers will use.
2. In the cloned repository's directory, open the `compose.yaml` file in an IDE or text editor.
3. In the `compose.yaml` file, add the following:
  - Add instructions to run a Neo4j database
  - Specify the environment file under the server service in order to pass in the environment variables for the connection
  The following is the updated `compose.yaml` file. All comments have been removed.
  ```yaml
  services:
    server:
      build:
        context: .
      ports:
        - 8000:8000
      env_file:
        - .env
      depends_on:
        database:
          condition: service_healthy
    database:
      image: neo4j:5.11
      ports:
        - "7474:7474"
        - "7687:7687"
      environment:
        - NEO4J_AUTH=${NEO4J_USERNAME}/${NEO4J_PASSWORD}
      healthcheck:
        test: ["CMD-SHELL", "wget --no-verbose --tries=1 --spider localhost:7474 || exit 1"]
        interval: 5s
        timeout: 3s
        retries: 5
  ```
  > Note
  >
  > To learn more about Neo4j, see the [Neo4j Official Docker Image](https://hub.docker.com/_/neo4j).
4. Run the application. Inside the `docker-genai-sample` directory,
  run the following command in a terminal.
  ```console
  $ docker compose up --build
  ```
5. Access the application. Open a browser and view the application at [http://localhost:8000](http://localhost:8000). You should see a simple Streamlit application. Note that asking questions to a PDF will cause the application to fail because the LLM service specified in the `.env` file isn't running yet.
6. Stop the application. In the terminal, press `ctrl`+`c` to stop the application.

## Add a local or remote LLM service

The sample application supports both [Ollama](https://ollama.ai/) and [OpenAI](https://openai.com/). This guide provides instructions for the following scenarios:

- Run Ollama in a container
- Run Ollama outside of a container
- Use OpenAI

While all platforms can use any of the previous scenarios, the performance and
GPU support may vary. You can use the following guidelines to help you choose the appropriate option:

- Run Ollama in a container if you're on Linux, and using a native installation of the Docker Engine, or Windows 10/11, and using Docker Desktop, you
  have a CUDA-supported GPU, and your system has at least 8 GB of RAM.
- Run Ollama outside of a container if you're on an Apple silicon Mac.
- Use OpenAI if the previous two scenarios don't apply to you.

Choose one of the following options for your LLM service.

When running Ollama in a container, you should have a CUDA-supported GPU. While you can run Ollama in a container without a supported GPU, the performance may not be acceptable. Only Linux and Windows 11 support GPU access to containers.

To run Ollama in a container and provide GPU access:

1. Install the prerequisites.
  - For Docker Engine on Linux, install the [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-container-toolkit).
  - For Docker Desktop on Windows 10/11, install the latest [NVIDIA driver](https://www.nvidia.com/Download/index.aspx) and make sure you are using the
    [WSL2 backend](https://docs.docker.com/desktop/features/wsl/#turn-on-docker-desktop-wsl-2)
2. Add the Ollama service and a volume in your `compose.yaml`. The following is
  the updated `compose.yaml`:
  ```yaml
  services:
    server:
      build:
        context: .
      ports:
        - 8000:8000
      env_file:
        - .env
      depends_on:
        database:
          condition: service_healthy
    database:
      image: neo4j:5.11
      ports:
        - "7474:7474"
        - "7687:7687"
      environment:
        - NEO4J_AUTH=${NEO4J_USERNAME}/${NEO4J_PASSWORD}
      healthcheck:
        test:
          [
            "CMD-SHELL",
            "wget --no-verbose --tries=1 --spider localhost:7474 || exit 1",
          ]
        interval: 5s
        timeout: 3s
        retries: 5
    ollama:
      image: ollama/ollama:latest
      ports:
        - "11434:11434"
      volumes:
        - ollama_volume:/root/.ollama
      deploy:
        resources:
          reservations:
            devices:
              - driver: nvidia
                count: all
                capabilities: [gpu]
  volumes:
    ollama_volume:
  ```
  > Note
  >
  > For more details about the Compose instructions, see
  > [Turn on GPU access with Docker Compose](https://docs.docker.com/compose/how-tos/gpu-support/).
3. Add the ollama-pull service to your `compose.yaml` file. This service uses
  the `docker/genai:ollama-pull` image, based on the GenAI Stack's
  [pull_model.Dockerfile](https://github.com/docker/genai-stack/blob/main/pull_model.Dockerfile).
  The service will automatically pull the model for your Ollama
  container. The following is the updated section of the `compose.yaml` file:
  ```yaml
  services:
    server:
      build:
        context: .
      ports:
        - 8000:8000
      env_file:
        - .env
      depends_on:
        database:
          condition: service_healthy
        ollama-pull:
          condition: service_completed_successfully
    ollama-pull:
      image: docker/genai:ollama-pull
      env_file:
        - .env
    # ...
  ```

To run Ollama outside of a container:

1. [Install](https://github.com/jmorganca/ollama) and run Ollama on your host
  machine.
2. Update the `OLLAMA_BASE_URL` value in your `.env` file to
  `http://host.docker.internal:11434`.
3. Pull the model to Ollama using the following command.
  ```console
  $ ollama pull llama2
  ```

> Important
>
> Using OpenAI requires an [OpenAI account](https://platform.openai.com/login). OpenAI is a third-party hosted service and charges may apply.

1. Update the `LLM` value in your `.env` file to
  `gpt-3.5`.
2. Uncomment and update the `OPENAI_API_KEY` value in your `.env` file to
  your [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key).

## Run your GenAI application

At this point, you have the following services in your Compose file:

- Server service for your main GenAI application
- Database service to store vectors in a Neo4j database
- (optional) Ollama service to run the LLM
- (optional) Ollama-pull service to automatically pull the model for the Ollama
  service

To run all the services, run the following command in your `docker-genai-sample`
directory:

```console
$ docker compose up --build
```

If your Compose file has the ollama-pull service, it may take several minutes for the ollama-pull service to pull the model. The ollama-pull service will continuously update the console with its status. After pulling the model, the ollama-pull service container will stop and you can access the application.

Once the application is running, open a browser and access the application at [http://localhost:8000](http://localhost:8000).

Upload a PDF file, for example the [Docker CLI Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf), and ask a question about the PDF.

Depending on your system and the LLM service that you chose, it may take several
minutes to answer. If you are using Ollama and the performance isn't
acceptable, try using OpenAI.

## Summary

In this section, you learned how to set up a development environment to provide
access all the services that your GenAI application needs.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Ollama Docker image](https://hub.docker.com/r/ollama/ollama)
- [Neo4j Official Docker Image](https://hub.docker.com/_/neo4j)
- [GenAI Stack demo applications](https://github.com/docker/genai-stack)

## Next steps

See samples of more GenAI applications in the [GenAI Stack demo applications](https://github.com/docker/genai-stack).

---

# PDF analysis and chat

> Containerize generative AI (GenAI) apps using Docker

# PDF analysis and chat

---

The generative AI (GenAI) guide teaches you how to containerize an existing GenAI application using Docker. In this guide, you’ll learn how to:

- Containerize and run a Python-based GenAI application
- Set up a local environment to run the complete GenAI stack locally for development

Start by containerizing an existing GenAI application.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/genai-pdf-bot/containerize/)
  Learn how to containerize a generative AI (GenAI) application.
2. [Develop your app](https://docs.docker.com/guides/genai-pdf-bot/develop/)
  Learn how to develop your generative AI (GenAI) application locally.

---

# GenAI video transcription and chat

> Explore a generative AI video analysis app that uses Docker, OpenAI, and Pinecone.

# GenAI video transcription and chat

   Table of contents

---

## Overview

This guide presents a project on video transcription and analysis using a set of
technologies related to the
[GenAI Stack](https://www.docker.com/blog/introducing-a-new-genai-stack/).

The project showcases the following technologies:

- [Docker and Docker Compose](#docker-and-docker-compose)
- [OpenAI](#openai-api)
- [Whisper](#whisper)
- [Embeddings](#embeddings)
- [Chat completions](#chat-completions)
- [Pinecone](#pinecone)
- [Retrieval-Augmented Generation](#retrieval-augmented-generation)

> **Acknowledgment**
>
>
>
> This guide is a community contribution. Docker would like to thank
> [David Cardozo](https://www.davidcardozo.com/) for his contribution
> to this guide.

## Prerequisites

- You have an [OpenAI API Key](https://platform.openai.com/api-keys).
  > Note
  >
  > OpenAI is a third-party hosted service and [charges](https://openai.com/pricing) may apply.
- You have a [Pinecone API Key](https://app.pinecone.io/).
- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/). Docker adds new features regularly and some parts of this guide may work only with the latest version of Docker Desktop.
- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## About the application

The application is a chatbot that can answer questions from a video. In
addition, it provides timestamps from the video that can help you find the sources used to answer your question.

## Get and run the application

1. Clone the sample application's repository. In a terminal, run the following
  command.
  ```console
  $ git clone https://github.com/Davidnet/docker-genai.git
  ```
  The project contains the following directories and files:
  ```text
  ├── docker-genai/
  │ ├── docker-bot/
  │ ├── yt-whisper/
  │ ├── .env.example
  │ ├── .gitignore
  │ ├── LICENSE
  │ ├── README.md
  │ └── docker-compose.yaml
  ```
2. Specify your API keys. In the `docker-genai` directory, create a text file
  called `.env` and specify your API keys inside. The following is the contents of the `.env.example` file that you can refer to as an example.
  ```text
  #----------------------------------------------------------------------------
  # OpenAI
  #----------------------------------------------------------------------------
  OPENAI_TOKEN=your-api-key # Replace your-api-key with your personal API key
  #----------------------------------------------------------------------------
  # Pinecone
  #----------------------------------------------------------------------------
  PINECONE_TOKEN=your-api-key # Replace your-api-key with your personal API key
  ```
3. Build and run the application. In a terminal, change directory to your
  `docker-genai` directory and run the following command.
  ```console
  $ docker compose up --build
  ```
  Docker Compose builds and runs the application based on the services defined
  in the `docker-compose.yaml` file. When the application is running, you'll
  see the logs of 2 services in the terminal.
  In the logs, you'll see the services are exposed on ports `8503` and `8504`.
  The two services are complimentary to each other.
  The `yt-whisper` service is running on port `8503`. This service feeds the
  Pinecone database with videos that you want to archive in your knowledge
  database. The following section explores this service.

## Using the yt-whisper service

The yt-whisper service is a YouTube video processing service that uses the OpenAI
Whisper model to generate transcriptions of videos and stores them in a Pinecone
database. The following steps show how to use the service.

1. Open a browser and access the yt-whisper service at [http://localhost:8503](http://localhost:8503).
2. Once the application appears, in the **Youtube URL** field specify a Youtube video URL
  and select **Submit**. The following example uses
  [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU).
  ![Submitting a video in the yt-whisper service](https://docs.docker.com/guides/genai-video-bot/images/yt-whisper.webp)  ![Submitting a video in the yt-whisper service](https://docs.docker.com/guides/genai-video-bot/images/yt-whisper.webp)
  The yt-whisper service downloads the audio of the video, uses Whisper to
  transcribe it into a WebVTT (`*.vtt`) format (which you can download), then
  uses the text-embedding-3-small model to create embeddings, and finally
  uploads those embeddings in to the Pinecone database.
  After processing the video, a video list appears in the web app that informs
  you which videos have been indexed in Pinecone. It also provides a button to
  download the transcript.
  ![A processed video in the yt-whisper service](https://docs.docker.com/guides/genai-video-bot/images/yt-whisper-2.webp)  ![A processed video in the yt-whisper service](https://docs.docker.com/guides/genai-video-bot/images/yt-whisper-2.webp)
  You can now access the dockerbot service on port `8504` and ask questions
  about the videos.

## Using the dockerbot service

The dockerbot service is a question-answering service that leverages both the
Pinecone database and an AI model to provide responses. The following steps show
how to use the service.

> Note
>
> You must process at least one video via the
> [yt-whisper service](#using-the-yt-whisper-service) before using
> the dockerbot service.

1. Open a browser and access the service at
  [http://localhost:8504](http://localhost:8504).
2. In the **What do you want to know about your videos?** text box, ask the
  Dockerbot a question about a video that was processed by the yt-whisper
  service. The following example asks the question, "What is a sugar cookie?".
  The answer to that question exists in the video processed in the previous
  example,
  [https://www.youtube.com/watch?v=yaQZFhrW0fU](https://www.youtube.com/watch?v=yaQZFhrW0fU).
  ![Asking a question to the Dockerbot](https://docs.docker.com/guides/genai-video-bot/images/bot.webp)  ![Asking a question to the Dockerbot](https://docs.docker.com/guides/genai-video-bot/images/bot.webp)
  In this example, the Dockerbot answers the question and
  provides links to the video with timestamps, which may contain more
  information about the answer.
  The dockerbot service takes the question, turns it into an embedding using
  the text-embedding-3-small model, queries the Pinecone database to find
  similar embeddings, and then passes that context into the gpt-4-turbo-preview
  to generate an answer.
3. Select the first link to see what information it provides. Based on the
  previous example, select
  [https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s](https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s).
  In the example link, you can see that the section of video perfectly answers
  the question, "What is a sugar cookie?".

## Explore the application architecture

The following image shows the application's high-level service architecture, which includes:

- yt-whisper: A local service, ran by Docker Compose, that interacts with the
  remote OpenAI and Pinecone services.
- dockerbot: A local service, ran by Docker Compose, that interacts with the
  remote OpenAI and Pinecone services.
- OpenAI: A remote third-party service.
- Pinecone: A remote third-party service.

![Application architecture diagram](https://docs.docker.com/guides/genai-video-bot/images/architecture.webp)  ![Application architecture diagram](https://docs.docker.com/guides/genai-video-bot/images/architecture.webp)

## Explore the technologies used and their role

### Docker and Docker Compose

The application uses Docker to run the application in containers, providing a
consistent and isolated environment for running it. This means the application
will operate as intended within its Docker containers, regardless of the
underlying system differences. To learn more about Docker, see the
[Getting started overview](https://docs.docker.com/get-started/introduction/).

Docker Compose is a tool for defining and running multi-container applications.
Compose makes it easy to run this application with a single command, `docker compose up`. For more details, see the
[Compose overview](https://docs.docker.com/compose/).

### OpenAI API

The OpenAI API provides an LLM service that's known for its cutting-edge AI and
machine learning technologies. In this application, OpenAI's technology is used
to generate transcriptions from audio (using the Whisper model) and to create
embeddings for text data, as well as to generate responses to user queries
(using GPT and chat completions). For more details, see
[openai.com](https://openai.com/product).

### Whisper

Whisper is an automatic speech recognition system developed by OpenAI, designed
to transcribe spoken language into text. In this application, Whisper is used to
transcribe the audio from YouTube videos into text, enabling further processing
and analysis of the video content. For more details, see [Introducing Whisper](https://openai.com/research/whisper).

### Embeddings

Embeddings are numerical representations of text or other data types, which
capture their meaning in a way that can be processed by machine learning
algorithms. In this application, embeddings are used to convert video
transcriptions into a vector format that can be queried and analyzed for
relevance to user input, facilitating efficient search and response generation
in the application. For more details, see OpenAI's
[Embeddings](https://platform.openai.com/docs/guides/embeddings) documentation.

![Embedding diagram](https://docs.docker.com/guides/genai-video-bot/images/embeddings.webp)  ![Embedding diagram](https://docs.docker.com/guides/genai-video-bot/images/embeddings.webp)

### Chat completions

Chat completion, as utilized in this application through OpenAI's API, refers to
the generation of conversational responses based on a given context or prompt.
In the application, it is used to provide intelligent, context-aware answers to
user queries by processing and integrating information from video transcriptions
and other inputs, enhancing the chatbot's interactive capabilities. For more
details, see OpenAI's
[Chat Completions API](https://platform.openai.com/docs/guides/text-generation) documentation.

### Pinecone

Pinecone is a vector database service optimized for similarity search, used for
building and deploying large-scale vector search applications. In this
application, Pinecone is employed to store and retrieve the embeddings of video
transcriptions, enabling efficient and relevant search functionality within the
application based on user queries. For more details, see
[pincone.io](https://www.pinecone.io/).

### Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) is a technique that combines information
retrieval with a language model to generate responses based on retrieved
documents or data. In RAG, the system retrieves relevant information (in this
case, via embeddings from video transcriptions) and then uses a language model
to generate responses based on this retrieved data. For more details, see
OpenAI's cookbook for
[Retrieval Augmented Generative Question Answering with Pinecone](https://cookbook.openai.com/examples/vector_databases/pinecone/gen_qa).

## Next steps

Explore how to
[create a PDF bot application](https://docs.docker.com/guides/genai-pdf-bot/) using
generative AI, or view more GenAI samples in the
[GenAI Stack](https://github.com/docker/genai-stack) repository.

---

# Introduction to GitHub Actions with Docker

# Introduction to GitHub Actions with Docker

   Table of contents

---

This guide provides an introduction to building CI pipelines using Docker and
GitHub Actions. You will learn how to use Docker's official GitHub Actions to
build your application as a Docker image and push it to Docker Hub. By the end
of the guide, you'll have a simple, functional GitHub Actions configuration for
Docker builds. Use it as-is, or extend it further to fit your needs.

## Prerequisites

If you want to follow along with the guide, ensure you have the following:

- A verified Docker account.
- Familiarity with Dockerfiles.

This guide assumes basic knowledge of Docker concepts but provides explanations
for using Docker in GitHub Actions workflows.

## Get the sample app

This guide is project-agnostic and assumes you have an application with a
Dockerfile.

If you need a sample project to follow along, you can use [this sample
application](https://github.com/dvdksn/rpg-name-generator.git), which includes
a Dockerfile for building a containerized version of the app. Alternatively,
use your own GitHub project or create a new repository from the template.

```dockerfile
#syntax=docker/dockerfile:1

# builder installs dependencies and builds the node app
FROM node:lts-alpine AS builder
WORKDIR /src
RUN --mount=src=package.json,target=package.json \
    --mount=src=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN --mount=type=cache,target=/root/.npm \
    npm run build

# release creates the runtime image
FROM node:lts-alpine AS release
WORKDIR /app
COPY --from=builder /src/build .
EXPOSE 3000
CMD ["node", "."]
```

## Configure your GitHub repository

The workflow in this guide pushes the image you build to Docker Hub. To do
that, you must authenticate with your Docker credentials (username and access
token) as part of the GitHub Actions workflow.

For instructions on how to create a Docker access token, see
[Create and manage access tokens](https://docs.docker.com/security/access-tokens/).

Once you have your Docker credentials ready, add the credentials to your GitHub
repository so you can use them in GitHub Actions:

1. Open your repository's **Settings**.
2. Under **Security**, go to **Secrets and variables > Actions**.
3. Under **Secrets**, create a new repository secret named `DOCKER_PASSWORD`,
  containing your Docker access token.
4. Next, under **Variables**, create a `DOCKER_USERNAME` repository variable
  containing your Docker Hub username.

## Set up your GitHub Actions workflow

GitHub Actions workflows define a series of steps to automate tasks, such as
building and pushing Docker images, in response to triggers like commits or
pull requests. In this guide, the workflow focuses on automating Docker builds
and testing, ensuring your containerized application works correctly before
publishing it.

Create a file named `docker-ci.yml` in the `.github/workflows/` directory of
your repository. Start with the basic workflow configuration:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:
```

This configuration runs the workflow on pushes to the main branch and on pull
requests. By including both triggers, you can ensure that the image builds
correctly for a pull request before it's merged.

## Extract metadata for tags and annotations

For the first step in your workflow, use the `docker/metadata-action` to
generate metadata for your image. This action extracts information about your
Git repository, such as branch names and commit SHAs, and generates image
metadata such as tags and annotations.

Add the following YAML to your workflow file:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image
```

These steps prepare metadata to tag and annotate your images during the build
and push process.

- The **Checkout** step clones the Git repository.
- The **Extract Docker image metadata** step extracts Git metadata and
  generates image tags and annotations for the Docker build.

## Authenticate to your registry

Before you build the image, authenticate to your registry to ensure that you
can push your built image to the registry.

To authenticate with Docker Hub, add the following step to your workflow:

```yaml
- name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

This step uses the Docker credentials [configured in the repository settings](#configure-your-github-repository).

## Build and push the image

Finally, build the final production image and push it to your registry. The
following configuration builds the image and pushes it directly to a registry.

```yaml
- name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
```

In this configuration:

- `push: ${{ github.event_name != 'pull_request' }}` ensures that images are
  only pushed when the event is not a pull request. This way, the workflow
  builds and tests images for pull requests but only pushes images for commits
  to the main branch.
- `tags` and `annotations` use the outputs from the metadata action to apply
  consistent tags and
  [annotations](https://docs.docker.com/build/metadata/annotations/) to
  the image automatically.

## Attestations

SBOM (Software Bill of Materials) and provenance attestations improve security
and traceability, ensuring your images meet modern software supply chain
requirements.

With a small amount of additional configuration, you can configure
`docker/build-push-action` to generate Software Bill of Materials (SBOM) and
provenance attestations for the image, at build-time.

To generate this additional metadata, you need to make two changes to your
workflow:

- Before the build step, add a step that uses `docker/setup-buildx-action`.
  This action configures your Docker build client with additional capabilities
  that the default client doesn't support.
- Then, update the **Build and push Docker image** step to also enable SBOM and
  provenance attestations.

Here's the updated snippet:

```yaml
- name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

For more details about attestations, refer to
[the documentation](https://docs.docker.com/build/metadata/attestations/).

## Conclusion

With all the steps outlined in the previous section, here's the full workflow
configuration:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push Docker image
        uses: docker/build-push-action@v6
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

This workflow implements best practices for building and pushing Docker images
using GitHub Actions. This configuration can be used as-is or extended with
additional features based on your project's needs, such as
[multi-platform](https://docs.docker.com/build/building/multi-platform/).

### Further reading

- Learn more about advanced configurations and examples in the
  [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/) section.
- For more complex build setups, you may want to consider
  [Bake](https://docs.docker.com/build/bake/). (See also the
  [Mastering Buildx Bake guide](https://docs.docker.com/guides/bake/).)
- Learn about Docker's managed build service, designed for faster, multi-platform builds, see
  [Docker Build Cloud](https://docs.docker.com/guides/docker-build-cloud/).

---

# Customize a code quality check workflow

> Learn how to customize prompts for specific quality issues, filter by file patterns, set quality thresholds, and integrate your workflow with GitHub Actions for automated code quality checks.

# Customize a code quality check workflow

   Table of contents

---

Now that you understand the basics of automating code quality workflows with
GitHub and SonarQube in E2B sandboxes, you can customize the workflow
for your needs.

## Focus on specific quality issues

Modify the prompt to prioritize certain issue types:

```typescript
const prompt = `Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "${repoPath}" and fix the highest priority issues first.`;
```

```python
prompt = f"""Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "{repo_path}" and fix the highest priority issues first."""
```

## Integrate with CI/CD

Add this workflow to GitHub Actions to run automatically on pull requests:

```yaml
name: Automated quality checks
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "18"
      - run: npm install
      - run: npx tsx 06-quality-gated-pr.ts
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

```yaml
name: Automated quality checks
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.8"
      - run: pip install e2b python-dotenv
      - run: python 06_quality_gated_pr.py
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

## Filter by file patterns

Target specific parts of your codebase:

```typescript
const prompt = `Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only.`;
```

```python
prompt = """Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only."""
```

## Set quality thresholds

Define when PRs should be created:

```typescript
const prompt = `Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation.`;
```

```python
prompt = """Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation."""
```

## Next steps

Learn how to troubleshoot common issues.

---

# Troubleshoot code quality workflows

> Solutions for MCP tools not loading, authentication errors, permission issues, workflow timeouts, and other common problems when building code quality workflows with E2B.

# Troubleshoot code quality workflows

   Table of contents

---

This page covers common issues you might encounter when building code quality
workflows with E2B sandboxes and MCP servers, along with their solutions.

If you're experiencing problems not covered here, check the
[E2B documentation](https://e2b.dev/docs).

## MCP tools not available

Issue: Claude reports `I don't have any MCP tools available`.

Solution:

1. Verify you're using the authorization header:
  ```plaintext
  --header "Authorization: Bearer ${mcpToken}"
  ```
2. Check you're waiting for MCP initialization.
  ```typescript
  // typescript
  await new Promise((resolve) => setTimeout(resolve, 1000));
  ```
  ```python
  # python
  await asyncio.sleep(1)
  ```
3. Ensure credentials are in both `envs` and `mcp` configuration:
  ```typescript
  // typescript
  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
        url: "https://sonarcloud.io",
      },
    },
  });
  ```
  ```python
  # python
  sbx = await AsyncSandbox.beta_create(
      envs={
          "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
          "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
          "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
      },
      mcp={
          "githubOfficial": {
              "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
          },
          "sonarqube": {
              "org": os.getenv("SONARQUBE_ORG"),
              "token": os.getenv("SONARQUBE_TOKEN"),
              "url": "https://sonarcloud.io",
          },
      },
  )
  ```
4. Verify your API tokens are valid and have proper scopes.

## GitHub tools work but SonarQube doesn't

Issue: GitHub MCP tools load but SonarQube tools don't appear.

Solution: SonarQube MCP server requires GitHub to be configured simultaneously.
Always include both servers in your sandbox configuration, even if you're only
testing one.

```typescript
// Include both servers even if only using one
const sbx = await Sandbox.betaCreate({
  envs: {
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
    GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
    SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
  },
  mcp: {
    githubOfficial: {
      githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
    },
    sonarqube: {
      org: process.env.SONARQUBE_ORG!,
      token: process.env.SONARQUBE_TOKEN!,
      url: "https://sonarcloud.io",
    },
  },
});
```

```python
# Include both servers even if only using one
sbx = await AsyncSandbox.beta_create(
    envs={
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
    },
    mcp={
        "githubOfficial": {
            "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
        },
        "sonarqube": {
            "org": os.getenv("SONARQUBE_ORG"),
            "token": os.getenv("SONARQUBE_TOKEN"),
            "url": "https://sonarcloud.io",
        },
    },
)
```

## Claude can't access private repositories

Issue: "I don't have access to that repository".

Solution:

1. Verify your GitHub token has `repo` scope (not just `public_repo`).
2. Test with a public repository first.
3. Ensure the repository owner and name are correct in your `.env`:
  ```plaintext
  GITHUB_OWNER=your_github_username
  GITHUB_REPO=your_repository_name
  ```
  ```plaintext
  GITHUB_OWNER=your_github_username
  GITHUB_REPO=your_repository_name
  ```

## Workflow times out or runs too long

Issue: Workflow doesn't complete or Claude credits run out.

Solutions:

1. Use `timeoutMs: 0` (TypeScript) or `timeout_ms=0` (Python) for complex workflows to allow unlimited time:
  ```typescript
  await sbx.commands.run(
    `echo '${prompt}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0, // No timeout
      onStdout: console.log,
      onStderr: console.log,
    },
  );
  ```
  ```python
  await sbx.commands.run(
      f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
      timeout_ms=0,  # No timeout
      on_stdout=print,
      on_stderr=print,
  )
  ```
2. Break complex workflows into smaller, focused tasks.
3. Monitor your Anthropic API credit usage.
4. Add checkpoints in prompts: "After each step, show progress before continuing".

## Sandbox cleanup errors

Issue: Sandboxes aren't being cleaned up properly, leading to resource exhaustion.

Solution: Always use proper error handling with cleanup in the `finally` block:

```typescript
async function robustWorkflow() {
  let sbx: Sandbox | undefined;

  try {
    sbx = await Sandbox.betaCreate({
      // ... configuration
    });

    // ... workflow logic
  } catch (error) {
    console.error("Workflow failed:", error);
    process.exit(1);
  } finally {
    if (sbx) {
      console.log("Cleaning up sandbox...");
      await sbx.kill();
    }
  }
}
```

```python
async def robust_workflow():
    sbx = None

    try:
        sbx = await AsyncSandbox.beta_create(
            # ... configuration
        )

        # ... workflow logic

    except Exception as error:
        print(f"Workflow failed: {error}")
        sys.exit(1)
    finally:
        if sbx:
            print("Cleaning up sandbox...")
            await sbx.kill()
```

## Environment variable not loading

Issue: Script fails with "undefined" or "None" for environment variables.

Solution:

1. Ensure `dotenv` is loaded at the top of your file:
  ```typescript
  import "dotenv/config";
  ```
2. Verify the `.env` file is in the same directory as your script.
3. Check variable names match exactly (case-sensitive):
  ```typescript
  // .env file
  GITHUB_TOKEN = ghp_xxxxx;
  // In code
  process.env.GITHUB_TOKEN; // Correct
  process.env.github_token; // Wrong - case doesn't match
  ```

1. Ensure `dotenv` is loaded at the top of your file:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```
2. Verify the `.env` file is in the same directory as your script.
3. Check variable names match exactly (case-sensitive):
  ```python
  # .env file
  GITHUB_TOKEN=ghp_xxxxx
  # In code
  os.getenv("GITHUB_TOKEN")  # Correct
  os.getenv("github_token")  # Wrong - case doesn't match
  ```

## SonarQube returns empty results

Issue: SonarQube analysis returns no projects or issues.

Solution:

1. Verify your SonarCloud organization key is correct.
2. Ensure you have at least one project configured in SonarCloud.
3. Check that your SonarQube token has the necessary permissions.
4. Confirm your project has been analyzed at least once in SonarCloud.
