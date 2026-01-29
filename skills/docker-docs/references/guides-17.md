# Develop and test AWS Cloud applications using LocalStack and Docker and more

# Develop and test AWS Cloud applications using LocalStack and Docker

> How to develop and test AWS Cloud applications using LocalStack and Docker

# Develop and test AWS Cloud applications using LocalStack and Docker

   Table of contents

---

In modern application development, testing cloud applications locally before deploying them to a live environment helps you ship faster and with more confidence. This approach involves simulating services locally, identifying and fixing issues early, and iterating quickly without incurring costs or facing the complexities of a full cloud environment. Tools like [LocalStack](https://www.localstack.cloud/) have become invaluable in this process, enabling you to emulate AWS services and containerize applications for consistent, isolated testing environments.

In this guide, you'll learn how to:

- Use Docker to launch up a LocalStack container
- Connect to LocalStack from a non-containerized application
- Connect to LocalStack from a containerized application

## What is LocalStack?

LocalStack is a cloud service emulator that runs in a single container on your laptop. It provides a powerful, flexible, and cost-effective way to test and develop AWS-based applications locally.

## Why use LocalStack?

Simulating AWS services locally allows you to test how your app interacts with services like S3, Lambda, and DynamoDB without needing to connect to the real AWS cloud. You can quickly iterate on your development, avoiding the cost and complexity of deploying to the cloud during this phase.

By mimicking the behavior of these services locally, LocalStack enables faster feedback loops. Your app can interact with external APIs, but everything runs locally, removing the need to deal with cloud provisioning or network latency.

This makes it easier to validate integrations and test cloud-based scenarios without needing to configure IAM roles or policies in a live environment. You can simulate complex cloud architectures locally and push your changes to AWS only when you’re ready.

## Using LocalStack with Docker

The [official Docker image for LocalStack](https://hub.docker.com/r/localstack/localstack) provides a convenient way to run LocalStack on your development machine. It’s free to use and doesn’t require any API key to run. You can even use [LocalStack Docker Extension](https://www.docker.com/blog/develop-your-cloud-app-locally-with-the-localstack-extension/) to use LocalStack with a graphical user interface.

## Prerequisites

The following prerequisites are required to follow along with this how-to guide:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager)
- [Python and pip](https://www.python.org/downloads/)
- Basic knowledge of Docker

## Launching LocalStack

Launch a quick demo of LocalStack by using the following steps:

1. Start by [cloning a sample application](https://github.com/dockersamples/todo-list-localstack-docker). Open the terminal and run the following command:
  ```console
  $ git clone https://github.com/dockersamples/todo-list-localstack-docker
  $ cd todo-list-localstack-docker
  ```
2. Bring up LocalStack
  Run the following command to bring up LocalStack.
  ```console
  $ docker compose -f compose-native.yml up -d
  ```
  This Compose file also includes specifications for a required Mongo database. You can verify the services are up and running by visiting the Docker Desktop Dashboard.
  ![Diagram showing the LocalStack and Mongo container up and running on Docker Desktop ](https://docs.docker.com/guides/images/launch-localstack.webp)  ![Diagram showing the LocalStack and Mongo container up and running on Docker Desktop ](https://docs.docker.com/guides/images/launch-localstack.webp)
3. Verify that LocalStack is up and running by selecting the container and checking the logs.
  ![Diagram showing the logs of LocalStack container ](https://docs.docker.com/guides/images/localstack-logs.webp)  ![Diagram showing the logs of LocalStack container ](https://docs.docker.com/guides/images/localstack-logs.webp)
4. Creating a Local Amazon S3 Bucket
  When you create a local S3 bucket using LocalStack, you're essentially simulating the creation of an S3 bucket on AWS. This lets you to test and develop applications that interact with S3 without needing an actual AWS account.
  To create Local Amazon S3 bucket, install the [awscli-localCLI](https://github.com/localstack/awscli-local) on your system. The `awslocal` command is a thin wrapper around the AWS command line interface for use with LocalStack. It lets you to test and develop against a simulated environment on your local machine without needing to access the real AWS services.
  ```console
  $ pip install awscli-local
  ```
  Create a new S3 bucket within the LocalStack environment with the following command:
  ```console
  $ awslocal s3 mb s3://mysamplebucket
  ```
  The command `s3 mb s3://mysamplebucket` tells the AWS CLI to create a new S3 bucket (mb stands for `make bucket`) named `mysamplebucket`.
  You can verify if the S3 bucket gets created or not by selecting the LocalStack container on the Docker Desktop Dashboard and viewing the logs. The logs indicates that your LocalStack environment is configured correctly and you can now use the `mysamplebucket` for storing and retrieving objects.
  ![Diagram showing the logs of LocalStack that highlights the S3 bucket being created successfully ](https://docs.docker.com/guides/images/localstack-s3put.webp)  ![Diagram showing the logs of LocalStack that highlights the S3 bucket being created successfully ](https://docs.docker.com/guides/images/localstack-s3put.webp)

## Using LocalStack in development

Now that you've familiarized yourself with LocalStack, it's time to see it in action. In this demonstration, you'll use a sample application featuring a React frontend and a Node.js backend. This application stack utilizes the following components:

- React: A user-friendly frontend for accessing the todo-list application
- Node: A backend responsible for handling the HTTP requests.
- MongoDB: A database to store all the to-do list data
- LocalStack: Emulates the Amazon S3 service and stores and retrieve images.

![Diagram showing the tech stack of the sample todo-list application that includes LocalStack, frontend and backend services ](https://docs.docker.com/guides/images/localstack-arch.webp)  ![Diagram showing the tech stack of the sample todo-list application that includes LocalStack, frontend and backend services ](https://docs.docker.com/guides/images/localstack-arch.webp)

## Connecting to LocalStack from a non-containerized app

Now it’s time to connect your app to LocalStack. The `index.js` file, located in the backend/ directory, serves as the main entry point for the backend application.

The code interacts with LocalStack’s S3 service, which is accessed via the endpoint defined by the `S3_ENDPOINT_URL` environment variable, typically set to `http://localhost:4556` for local development.

The `S3Client` from the AWS SDK is configured to use this LocalStack endpoint, along with test credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) that are also sourced from environment variables. This setup lets the application to perform operations on the locally simulated S3 service as if it were interacting with the real AWS S3, making the code flexible for different environments.

The code uses `multer` and `multer-s3` to handle file uploads. When a user uploads an image through the /upload route, the file is stored directly in the S3 bucket simulated by LocalStack. The bucket name is retrieved from the environment variable `S3_BUCKET_NAME`. Each uploaded file is given a unique name by appending the current timestamp to the original filename. The route then returns the URL of the uploaded file within the local S3 service, making it accessible just as it would be if hosted on a real AWS S3 bucket.

Let’s see it in action. Start by launching the Node.js backend service.

1. Change to the backend/ directory
  ```console
  $ cd backend/
  ```
2. Install the required dependencies:
  ```console
  $ npm install
  ```
3. Setting up AWS environment variables
  The `.env` file located in the backend/ directory already contains placeholder credentials and configuration values that LocalStack uses to emulate AWS services. The `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are placeholder credentials, while `S3_BUCKET_NAME` and `S3_ENDPOINT_URL` are configuration settings. No changes are needed as these values are already correctly set for LocalStack.
  > Tip
  >
  > Given that you’re running Mongo in a Docker container and the backend Node app is running natively on your host, ensure that `MONGODB_URI=mongodb://localhost:27017/todos` is set in your `.env` file.
  ```plaintext
  MONGODB_URI=mongodb://localhost:27017/todos
  AWS_ACCESS_KEY_ID=test
  AWS_SECRET_ACCESS_KEY=test
  S3_BUCKET_NAME=mysamplebucket
  S3_ENDPOINT_URL=http://localhost:4566
  AWS_REGION=us-east-1
  ```
  While the AWS SDK might typically use environment variables starting with `AWS_`, this specific application directly references the following `S3_*` variables in the index.js file (under the `backend/` directory) to configure the S3Client.
  ```js
  const s3 = new S3Client({
    endpoint: process.env.S3_ENDPOINT_URL, // Use the provided endpoint or fallback to defaults
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'default_access_key', // Default values for development
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'default_secret_key',
    },
  });
  ```
4. Start the backend server:
  ```console
  $ node index.js
  ```
  You will see the message that the backend service has successfully started at port 5000.

## Start the frontend service

To start the frontend service, open a new terminal and follow these steps:

1. Navigate to the `frontend` directory:
  ```console
  $ cd frontend
  ```
2. Install the required dependencies
  ```console
  $ npm install
  ```
3. Start the frontend service
  ```console
  $ npm run dev
  ```
  By now, you should see the following message:
  ```console
  VITE v5.4.2  ready in 110 ms
  ➜  Local: http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
  ```
  You can now access the app via [http://localhost:5173](http://localhost:5173). Go ahead, and upload an image by choosing an image file and clicking the **Upload** button.
  ![Diagram showing a working todo-list application](https://docs.docker.com/guides/images/localstack-todolist.webp)  ![Diagram showing a working todo-list application](https://docs.docker.com/guides/images/localstack-todolist.webp)
  You can verify the image is uploaded to the S3 bucket by checking the LocalStack container logs:
  ![Diagram showing the logs of the LocalStack that highlights image uploaded to the emulated S3 bucket](https://docs.docker.com/guides/images/localstack-todolist-s3put.webp)  ![Diagram showing the logs of the LocalStack that highlights image uploaded to the emulated S3 bucket](https://docs.docker.com/guides/images/localstack-todolist-s3put.webp)
  The `200` status code signifies that the `putObject` operation, which involves uploading an object to the S3 bucket, was executed successfully within the LocalStack environment. LocalStack logs this entry to provide visibility into the operations being performed. It helps debug and confirm that your application is interacting correctly with the emulated AWS services.
  Since LocalStack is designed to simulate AWS services locally, this log entry shows that your application is functioning as expected when performing cloud operations in a local sandbox environment.

## Connecting to LocalStack from containerized Node app

Now that you have learnt how to connect a non-containerized Node.js application to LocalStack, it's time to explore the necessary changes to run the complete application stack in a containerized environment. To achieve this, you will create a Compose file specifying all required services - frontend, backend, database, and LocalStack.

1. Examine the Docker Compose file.
  The following Docker Compose file defines four services: `backend`, `frontend`, `mongodb`, and `localstack`. The `backend` and `frontend` services are your Node.js applications, while `mongodb` provides a database and `localstack` simulates AWS services like S3.
  The `backend` service depends on `localstack` and `mongodb` services, ensuring they are running before it starts. It also uses a .env file for environment variables. The frontend service depends on the backend and sets the API URL. The `mongodb` service uses a persistent volume for data storage, and `localstack` is configured to run the S3 service. This setup lets you to develop and test your application locally with AWS-like services.
  ```yaml
  services:
    backend:
      build:
        context: ./backend
        dockerfile: Dockerfile
      ports:
        - 5000:5000
      depends_on:
        - localstack
        - mongodb
      env_file:
        - backend/.env
    frontend:
      build:
        context: ./frontend
        dockerfile: Dockerfile
      ports:
        - 5173:5173
      depends_on:
        - backend
      environment:
        - REACT_APP_API_URL=http://backend:5000/api
    mongodb:
      image: mongo
      container_name: mongodb
      volumes:
        - mongodbdata:/data/db
      ports:
        - 27017:27017
    localstack:
      image: localstack/localstack
      container_name: localstack
      ports:
        - 4566:4566
      environment:
        - SERVICES=s3
        - GATEWAY_LISTEN=0.0.0.0:4566
      volumes:
        - ./localstack:/docker-entrypoint-initaws.d"
  volumes:
    mongodbdata:
  ```
2. Modify the `.env` file under the `backend/` directory to have the resources connect using the internal network names.
  > Tip
  >
  > Given the previous Compose file, the app would connect to LocalStack using the hostname `localstack` while Mongo would connect using the hostname `mongodb`.
  ```plaintext
  MONGODB_URI=mongodb://mongodb:27017/todos
  AWS_ACCESS_KEY_ID=test
  AWS_SECRET_ACCESS_KEY=test
  S3_BUCKET_NAME=mysamplebucket
  S3_ENDPOINT_URL=http://localstack:4566
  AWS_REGION=us-east-1
  ```
3. Stop the running services
  Ensure that you stop the Node frontend and backend service from the previous step by pressing “Ctrl+C” in the terminal. Also, you'll need to stop the LocalStack and Mongo containers by selecting them in the Docker Desktop Dashboard and selecting the "Delete" button.
4. Start the application stack by executing the following command at the root of your cloned project directory:
  ```console
  $ docker compose -f compose.yml up -d --build
  ```
  After a brief moment, the application will be up and running.
5. Create an S3 bucket manually
  The AWS S3 bucket is not created beforehand by the Compose file. Run the following command to create a new bucket within the LocalStack environment:
  ```console
  $ awslocal s3 mb s3://mysamplebucket
  ```
  The command creates an S3 bucket named `mysamplebucket`.
  Open [http://localhost:5173](http://localhost:5173) to access the complete to-do list application and start uploading images to the Amazon S3 bucket.
  > Tip
  >
  > To optimize performance and reduce upload times during development, consider uploading smaller image files. Larger images may take longer to process and could impact the overall responsiveness of the application.

## Recap

This guide has walked you through setting up a local development environment using LocalStack and Docker. You’ve learned how to test AWS-based applications locally, reducing costs and increasing the efficiency of your development workflow.

---

# Build a named entity recognition app

> Learn how to build and run a named entity recognition application using Python, spaCy, and Docker.

# Build a named entity recognition app

   Table of contents

---

## Overview

This guide walks you through building and running a named entity recognition
(NER) application. You'll build the application using Python with
spaCy, and then set up the environment and run the application using Docker.

The application processes input text to identify and print named entities, like people, organizations, or locations.

## Prerequisites

- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/). Docker adds new features regularly and some parts of this guide may work only with the latest version of Docker Desktop.
- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## Get the sample application

1. Open a terminal, and clone the sample application's repository using the
  following command.
  ```console
  $ git clone https://github.com/harsh4870/Docker-NLP.git
  ```
2. Verify that you cloned the repository.
  You should see the following files in your `Docker-NLP` directory.
  ```text
  01_sentiment_analysis.py
  02_name_entity_recognition.py
  03_text_classification.py
  04_text_summarization.py
  05_language_translation.py
  entrypoint.sh
  requirements.txt
  Dockerfile
  README.md
  ```

## Explore the application code

The source code for the name recognition application is in the `Docker-NLP/02_name_entity_recognition.py` file. Open `02_name_entity_recognition.py` in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.
  ```python
  import spacy
  ```
  This line imports the `spaCy` library. `spaCy` is a popular library in Python
  used for natural language processing (NLP).
2. Load the language model.
  ```python
  nlp = spacy.load("en_core_web_sm")
  ```
  Here, the `spacy.load` function loads a language model. The `en_core_web_sm`
  model is a small English language model. You can use this model for various
  NLP tasks, including tokenization, part-of-speech tagging, and named entity
  recognition.
3. Specify the main execution block.
  ```python
  if __name__ == "__main__":
  ```
  This Python idiom ensures that the following code block runs only if this
  script is the main program. It provides flexibility, allowing the script to
  function both as a standalone program and as an imported module.
4. Create an infinite loop for continuous input.
  ```python
  while True:
  ```
  This while loop runs indefinitely until it's explicitly broken. It lets
  the user continuously enter text for entity recognition until they decide
  to exit.
5. Get user input.
  ```python
  input_text = input("Enter the text for entity recognition (type 'exit' to end): ")
  ```
  This line prompts the user to enter text. The program will then perform entity recognition on this text.
6. Define an exit condition.
  ```python
  if input_text.lower() == 'exit':
     print("Exiting...")
     break
  ```
  If the user types something, the program converts the input to lowercase and
  compares it to `exit`. If they match, the program prints **Exiting...** and
  breaks out of the while loop, effectively ending the program.
7. Perform named entity recognition.
  ```python
  doc = nlp(input_text)
  for ent in doc.ents:
     print(f"Entity: {ent.text}, Type: {ent.label_}")
  ```
  - `doc = nlp(input_text)`: Here, the nlp model processes the user-input text. This creates a Doc object which contains various NLP attributes, including identified entities.
  - `for ent in doc.ents:`: This loop iterates over the entities found in the text.
  - `print(f"Entity: {ent.text}, Type: {ent.label_}")`: For each entity, it prints the entity text and its type (like PERSON, ORG, or GPE).
8. Create `requirements.txt`.
  The sample application already contains the `requirements.txt` file to specify the necessary packages that the application imports. Open `requirements.txt` in a code or text editor to explore its contents.
  ```text
  # 02 named_entity_recognition
  spacy==3.7.2
  ...
  ```
  Only the `spacy` package is required for the named recognition application.

## Explore the application environment

You'll use Docker to run the application in a container. Docker lets you
containerize the application, providing a consistent and isolated environment
for running it. This means the application will operate as intended within its
Docker container, regardless of the underlying system differences.

To run the application in a container, a Dockerfile is required. A Dockerfile is
a text document that contains all the commands you would call on the command
line to assemble an image. An image is a read-only template with instructions
for creating a Docker container.

The sample application already contains a `Dockerfile`. Open the `Dockerfile` in a code or text editor to explore its contents.

The following steps explain each part of the `Dockerfile`. For more details, see the
[Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

1. Specify the base image.
  ```dockerfile
  FROM python:3.8-slim
  ```
  This command sets the foundation for the build. `python:3.8-slim` is a
  lightweight version of the Python 3.8 image, optimized for size and speed.
  Using this slim image reduces the overall size of your Docker image, leading
  to quicker downloads and less surface area for security vulnerabilities. This
  is particularly useful for a Python-based application where you might not
  need the full standard Python image.
2. Set the working directory.
  ```dockerfile
  WORKDIR /app
  ```
  `WORKDIR` sets the current working directory within the Docker image. By
  setting it to `/app`, you ensure that all subsequent commands in the
  Dockerfile (like `COPY` and `RUN`) are executed in this directory. This also
  helps in organizing your Docker image, as all application-related files are
  contained in a specific directory.
3. Copy the requirements file into the image.
  ```dockerfile
  COPY requirements.txt /app
  ```
  The `COPY` command transfers the `requirements.txt` file from
  your local machine into the Docker image. This file lists all Python
  dependencies required by the application. Copying it into the container
  lets the next command (`RUN pip install`) install these dependencies
  inside the image environment.
4. Install the Python dependencies in the image.
  ```dockerfile
  RUN pip install --no-cache-dir -r requirements.txt
  ```
  This line uses `pip`, Python's package installer, to install the packages
  listed in `requirements.txt`. The `--no-cache-dir` option disables
  the cache, which reduces the size of the Docker image by not storing the
  unnecessary cache data.
5. Run additional commands.
  ```dockerfile
  RUN python -m spacy download en_core_web_sm
  ```
  This step is specific to NLP applications that require the spaCy library. It downloads the `en_core_web_sm` model, which is a small English language model for spaCy.
6. Copy the application code into the image.
  ```dockerfile
  COPY *.py /app
  COPY entrypoint.sh /app
  ```
  These commands copy your Python scripts and the `entrypoint.sh` script into
  the image's `/app` directory. This is crucial because the container needs
  these scripts to run the application. The `entrypoint.sh` script is
  particularly important as it dictates how the application starts inside the
  container.
7. Set permissions for the `entrypoint.sh` script.
  ```dockerfile
  RUN chmod +x /app/entrypoint.sh
  ```
  This command modifies the file permissions of `entrypoint.sh`, making it
  executable. This step is necessary to ensure that the Docker container can
  run this script to start the application.
8. Set the entry point.
  ```dockerfile
  ENTRYPOINT ["/app/entrypoint.sh"]
  ```
  The `ENTRYPOINT` instruction configures the container to run `entrypoint.sh`
  as its default executable. This means that when the container starts, it
  automatically executes the script.
  You can explore the `entrypoint.sh` script by opening it in a code or text
  editor. As the sample contains several applications, the script lets you
  specify which application to run when the container starts.

## Run the application

To run the application using Docker:

1. Build the image.
  In a terminal, run the following command inside the directory of where the `Dockerfile` is located.
  ```console
  $ docker build -t basic-nlp .
  ```
  The following is a break down of the command:
  - `docker build`: This is the primary command used to build a Docker image
    from a Dockerfile and a context. The context is typically a set of files at
    a specified location, often the directory containing the Dockerfile.
  - `-t basic-nlp`: This is an option for tagging the image. The `-t` flag
    stands for tag. It assigns a name to the image, which in this case is
    `basic-nlp`. Tags are a convenient way to reference images later,
    especially when pushing them to a registry or running containers.
  - `.`: This is the last part of the command and specifies the build context.
    The period (`.`) denotes the current directory. Docker will look for a
    Dockerfile in this directory. The build context (the current directory, in
    this case) is sent to the Docker daemon to enable the build. It includes
    all the files and subdirectories in the specified directory.
  For more details, see the
  [docker build CLI reference](https://docs.docker.com/reference/cli/docker/buildx/build/).
  Docker outputs several logs to your console as it builds the image. You'll
  see it download and install the dependencies. Depending on your network
  connection, this may take several minutes. Docker does have a caching
  feature, so subsequent builds can be faster. The console will
  return to the prompt when it's complete.
2. Run the image as a container.
  In a terminal, run the following command.
  ```console
  $ docker run -it basic-nlp 02_name_entity_recognition.py
  ```
  The following is a break down of the command:
  - `docker run`: This is the primary command used to run a new container from
    a Docker image.
  - `-it`: This is a combination of two options:
    - `-i` or `--interactive`: This keeps the standard input (STDIN) open even
      if not attached. It lets the container remain running in the
      foreground and be interactive.
    - `-t` or `--tty`: This allocates a pseudo-TTY, essentially simulating a
      terminal, like a command prompt or a shell. It's what lets you
      interact with the application inside the container.
  - `basic-nlp`: This specifies the name of the Docker image to use for
    creating the container. In this case, it's the image named `basic-nlp` that
    you created with the `docker build` command.
  - `02_name_entity_recognition.py`: This is the script you want to run inside
    the Docker container. It gets passed to the `entrypoint.sh` script, which
    runs it when the container starts.
  For more details, see the
  [docker run CLI reference](https://docs.docker.com/reference/cli/docker/container/run/).
  > Note
  >
  > For Windows users, you may get an error when running the container. Verify
  > that the line endings in the `entrypoint.sh` are `LF` (`\n`) and not `CRLF` (`\r\n`),
  > then rebuild the image. For more details, see [Avoid unexpected syntax errors, use Unix style line endings for files in containers](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers).
  You will see the following in your console after the container starts.
  ```console
  Enter the text for entity recognition (type 'exit' to end):
  ```
3. Test the application.
  Enter some information to get the named entity recognition.
  ```console
  Enter the text for entity recognition (type 'exit' to end): Apple Inc. is planning to open a new store in San Francisco. Tim Cook is the CEO of Apple.
  Entity: Apple Inc., Type: ORG
  Entity: San Francisco, Type: GPE
  Entity: Tim Cook, Type: PERSON
  Entity: Apple, Type: ORG
  ```

## Summary

This guide demonstrated how to build and run a named entity recognition
application. You learned how to build the application using Python with spaCy,
and then set up the environment and run the application using Docker.

Related information:

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [spaCy](https://spacy.io/)
- [Python documentation](https://docs.python.org/3/)

## Next steps

Explore more [natural language processing guides](https://docs.docker.com/guides/).

---

# Automate your builds with GitHub Actions

> Learn how to configure CI/CD using GitHub Actions for your Node.js application.

# Automate your builds with GitHub Actions

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a Node.js application](https://docs.docker.com/guides/nodejs/containerize/).

You must also have:

- A [GitHub](https://github.com/signup) account.
- A verified [Docker Hub](https://hub.docker.com/signup) account.

---

## Overview

In this section, you'll set up a **CI/CD pipeline** using [GitHub Actions](https://docs.github.com/en/actions) to automatically:

- Build your Node.js application inside a Docker container.
- Run unit and integration tests, and make sure your application meets solid code quality standards.
- Perform security scanning and vulnerability assessment.
- Push production-ready images to [Docker Hub](https://hub.docker.com).

---

## Connect your GitHub repository to Docker Hub

To enable GitHub Actions to build and push Docker images, you'll securely store your Docker Hub credentials in your new GitHub repository.

### Step 1: Connect your GitHub repository to Docker Hub

1. Create a Personal Access Token (PAT) from [Docker Hub](https://hub.docker.com).
  1. From your Docker Hub account, go to **Account Settings → Security**.
  2. Generate a new Access Token with **Read/Write** permissions.
  3. Name it something like `docker-nodejs-sample`.
  4. Copy and save the token — you'll need it in Step 4.
2. Create a repository in [Docker Hub](https://hub.docker.com/repositories/).
  1. From your Docker Hub account, select **Create a repository**.
  2. For the Repository Name, use something descriptive — for example: `nodejs-sample`.
  3. Once created, copy and save the repository name — you'll need it in Step 4.
3. Create a new [GitHub repository](https://github.com/new) for your Node.js project.
4. Add Docker Hub credentials as GitHub repository secrets.
  In your newly created GitHub repository:
  1. From **Settings**, go to **Secrets and variables → Actions → New repository secret**.
  2. Add the following secrets:
  | Name | Value |
  | --- | --- |
  | DOCKER_USERNAME | Your Docker Hub username |
  | DOCKERHUB_TOKEN | Your Docker Hub access token (created in Step 1) |
  | DOCKERHUB_PROJECT_NAME | Your Docker Project Name (created in Step 2) |
  These secrets let GitHub Actions to authenticate securely with Docker Hub during automated workflows.
5. Connect your local project to GitHub.
  Link your local project `docker-nodejs-sample` to the GitHub repository you just created by running the following command from your project root:
  ```console
  $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
  ```
  > Important
  >
  > Replace `{your-username}` and `{your-repository}` with your actual GitHub username and repository name.
  To confirm that your local project is correctly connected to the remote GitHub repository, run:
  ```console
  $ git remote -v
  ```
  You should see output similar to:
  ```console
  origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
  origin  https://github.com/{your-username}/{your-repository-name}.git (push)
  ```
  This confirms that your local repository is properly linked and ready to push your source code to GitHub.
6. Push your source code to GitHub.
  Follow these steps to commit and push your local project to your GitHub repository:
  1. Stage all files for commit.
    ```console
    $ git add -A
    ```
    This command stages all changes — including new, modified, and deleted files — preparing them for commit.
  2. Commit your changes.
    ```console
    $ git commit -m "Initial commit with CI/CD pipeline"
    ```
    This command creates a commit that snapshots the staged changes with a descriptive message.
  3. Push the code to the `main` branch.
    ```console
    $ git push -u origin main
    ```
    This command pushes your local commits to the `main` branch of the remote GitHub repository and sets the upstream branch.

Once completed, your code will be available on GitHub, and any GitHub Actions workflow you've configured will run automatically.

> Note
>
> Learn more about the Git commands used in this step:
>
>
>
> - [Git add](https://git-scm.com/docs/git-add) – Stage changes (new, modified, deleted) for commit
> - [Git commit](https://git-scm.com/docs/git-commit) – Save a snapshot of your staged changes
> - [Git push](https://git-scm.com/docs/git-push) – Upload local commits to your GitHub repository
> - [Git remote](https://git-scm.com/docs/git-remote) – View and manage remote repository URLs

---

### Step 2: Set up the workflow

Now you'll create a GitHub Actions workflow that builds your Docker image, runs tests, and pushes the image to Docker Hub.

1. From your repository on GitHub, select the **Actions** tab in the top menu.
2. When prompted, select **Set up a workflow yourself**.
  This opens an inline editor to create a new workflow file. By default, it will be saved to:
  `.github/workflows/main.yml`
3. Add the following workflow configuration to the new file:

```yaml
name: CI/CD – Node.js Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  test:
    name: Run Node.js Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:18-alpine
        env:
          POSTGRES_DB: todoapp_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache npm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-npm-

      - name: Build test image
        uses: docker/build-push-action@v6
        with:
          context: .
          target: test
          tags: nodejs-app-test:latest
          platforms: linux/amd64
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      - name: Run tests inside container
        run: |
          docker run --rm \
            --network host \
            -e NODE_ENV=test \
            -e POSTGRES_HOST=localhost \
            -e POSTGRES_PORT=5432 \
            -e POSTGRES_DB=todoapp_test \
            -e POSTGRES_USER=postgres \
            -e POSTGRES_PASSWORD=postgres \
            nodejs-app-test:latest
        env:
          CI: true
        timeout-minutes: 10

  build-and-push:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Cache Docker layers
        uses: actions/cache@v4
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: ${{ runner.os }}-buildx-

      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push multi-arch production image
        uses: docker/build-push-action@v6
        with:
          context: .
          target: production
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max
```

This workflow performs the following tasks for your Node.js application:

- Triggers on every `push` or `pull request` to the `main` branch.
- Builds a test Docker image using the `test` stage.
- Runs tests in a containerized environment.
- Stops the workflow if any test fails.
- Caches Docker build layers and npm dependencies for faster runs.
- Authenticates with Docker Hub using GitHub secrets.
- Builds an image using the `production` stage.
- Tags and pushes the image to Docker Hub with `latest` and short SHA tags.

> Note
>
> For more information about `docker/build-push-action`, refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

---

### Step 3: Run the workflow

After adding your workflow file, trigger the CI/CD process.

1. Commit and push your workflow file
  From the GitHub editor, select **Commit changes…**.
  - This push automatically triggers the GitHub Actions pipeline.
2. Monitor the workflow execution
  1. From your GitHub repository, go to the **Actions** tab.
  2. Select the workflow run to follow each step: **test**, **build**, **security**, and (if successful) **push** and **deploy**.
3. Verify the Docker image on Docker Hub
  - After a successful workflow run, visit your [Docker Hub repositories](https://hub.docker.com/repositories).
  - You should see a new image under your repository with:
    - Repository name: `${your-repository-name}`
    - Tags include:
      - `latest` – represents the most recent successful build; ideal for quick testing or deployment.
      - `<short-sha>` – a unique identifier based on the commit hash, useful for version tracking, rollbacks, and traceability.

> Tip
>
> To maintain code quality and prevent accidental direct pushes, enable branch protection rules:
>
>
>
> - From your GitHub repository, go to **Settings → Branches**.
> - Under Branch protection rules, select **Add rule**.
> - Specify `main` as the branch name.
> - Enable options like:
>   - *Require a pull request before merging*.
>   - *Require status checks to pass before merging*.
>
>
>
> This ensures that only tested and reviewed code is merged into `main` branch.

---

## Summary

In this section, you set up a comprehensive CI/CD pipeline for your containerized Node.js application using GitHub Actions.

What you accomplished:

- Created a new GitHub repository specifically for your project.
- Generated a Docker Hub access token and added it as a GitHub secret.
- Created a GitHub Actions workflow that:
  - Builds your application in a Docker container.
  - Run tests in a containerized environment.
  - Pushes an image to Docker Hub if tests pass.
- Verified the workflow runs successfully.

Your Node.js application now has automated testing and deployment.

---

## Related resources

Deepen your understanding of automation and best practices for containerized apps:

- [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/) – Learn how GitHub Actions automate your workflows
- [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/) – Set up container builds with GitHub Actions
- [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) – Full reference for writing GitHub workflows
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) – Learn about GHCR features and usage
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) – Optimize your image for performance and security

---

## Next steps

Next, learn how you can deploy your containerized Node.js application to Kubernetes with production-ready configuration. This helps you ensure your application behaves as expected in a production-like environment, reducing surprises during deployment.
