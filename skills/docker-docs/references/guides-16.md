# Developing event and more

# Developing event

> Developing event-driven applications with Kafka and Docker

# Developing event-driven applications with Kafka and Docker

   Table of contents

---

With the rise of microservices, event-driven architectures have become increasingly popular.
[Apache Kafka](https://kafka.apache.org/), a distributed event streaming platform, is often at the
heart of these architectures. Unfortunately, setting up and deploying your own Kafka instance for development
is often tricky. Fortunately, Docker and containers make this much easier.

In this guide, you will learn how to:

1. Use Docker to launch up a Kafka cluster
2. Connect a non-containerized app to the cluster
3. Connect a containerized app to the cluster
4. Deploy Kafka-UI to help with troubleshooting and debugging

## Prerequisites

The following prerequisites are required to follow along with this how-to guide:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager) and [yarn](https://yarnpkg.com/)
- Basic knowledge of Kafka and Docker

## Launching Kafka

Beginning with [Kafka 3.3](https://www.confluent.io/blog/apache-kafka-3-3-0-new-features-and-updates/), the deployment of Kafka was greatly simplified by no longer requiring Zookeeper thanks to KRaft (Kafka Raft). With KRaft, setting up a Kafka instance for local development is much easier. Starting with the launch of [Kafka 3.8](https://www.confluent.io/blog/introducing-apache-kafka-3-8/), a new [kafka-native](https://hub.docker.com/r/apache/kafka-native) Docker image is now available, providing a significantly faster startup and lower memory footprint.

> Tip
>
> This guide will be using the apache/kafka image, as it includes many helpful scripts to manage and work with Kafka. However, you may want to use the apache/kafka-native image, as it starts more quickly and requires fewer resources.

### Starting Kafka

Start a basic Kafka cluster by doing the following steps. This example will launch a cluster, exposing port 9092 onto the host to let a native-running application to connect to it.

1. Start a Kafka container by running the following command:
  ```console
  $ docker run -d --name=kafka -p 9092:9092 apache/kafka
  ```
2. Once the image pulls, you’ll have a Kafka instance up and running within a second or two.
3. The apache/kafka image ships with several helpful scripts in the `/opt/kafka/bin` directory. Run the following command to verify the cluster is up and running and get its cluster ID:
  ```console
  $ docker exec -ti kafka /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server :9092
  ```
  Doing so will produce output similar to the following:
  ```plaintext
  Cluster ID: 5L6g3nShT-eMCtK--X86sw
  ```
4. Create a sample topic and produce (or publish) a few messages by running the following command:
  ```console
  $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
  ```
  After running, you can enter a message per line. For example, enter a few messages, one per line. A few examples might be:
  ```plaintext
  First message
  ```
  And
  ```plaintext
  Second message
  ```
  Press `enter` to send the last message and then press ctrl+c when you’re done. The messages will be published to Kafka.
5. Confirm the messages were published into the cluster by consuming the messages:
  ```console
  $ docker exec -ti kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server :9092 --topic demo --from-beginning
  ```
  You should then see your messages in the output:
  ```plaintext
  First message
  Second message
  ```
  If you want, you can open another terminal and publish more messages and see them appear in the consumer.
  When you’re done, hit ctrl+c to stop consuming messages.

You have a locally running Kafka cluster and have validated you can connect to it.

## Connecting to Kafka from a non-containerized app

Now that you’ve shown you can connect to the Kafka instance from a command line, it’s time to connect to the cluster from an application. In this example, you will use a simple Node project that uses the [KafkaJS](https://github.com/tulios/kafkajs) library.

Since the cluster is running locally and is exposed at port 9092, the app can connect to the cluster at localhost:9092 (since it’s running natively and not in a container right now). Once connected, this sample app will log messages it consumes from the `demo` topic. Additionally, when it runs in development mode, it will also create the topic if it isn’t found.

1. If you don’t have the Kafka cluster running from the previous step, run the following command to start a Kafka instance:
  ```console
  $ docker run -d --name=kafka -p 9092:9092 apache/kafka
  ```
2. Clone the [GitHub repository](https://github.com/dockersamples/kafka-development-node) locally.
  ```console
  $ git clone https://github.com/dockersamples/kafka-development-node.git
  ```
3. Navigate into the project.
  ```console
  cd kafka-development-node/app
  ```
4. Install the dependencies using yarn.
  ```console
  $ yarn install
  ```
5. Start the application using `yarn dev`. This will set the `NODE_ENV` environment variable to `development` and use `nodemon` to watch for file changes.
  ```console
  $ yarn dev
  ```
6. With the application now running, it will log received messages to the console. In a new terminal, publish a few messages using the following command:
  ```console
  $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
  ```
  And then send a message to the cluster:
  ```plaintext
  Test message
  ```
  Remember to press `ctrl+c` when you’re done to stop producing messages.

## Connecting to Kafka from both containers and native apps

Now that you have an application connecting to Kafka through its exposed port, it’s time to explore what changes are needed to connect to Kafka from another container. To do so, you will now run the application out of a container instead of natively.

But before you do that, it’s important to understand how Kafka listeners work and how those listeners help clients connect.

### Understanding Kafka listeners

When a client connects to a Kafka cluster, it actually connects to a “broker”. While brokers have many roles, one of them is to support load balancing of clients. When a client connects, the broker returns a set of connection URLs the client should then use for the client to connect for the producing or consuming of messages. How are these connection URLs configured?

Each Kafka instance has a set of listeners and advertised listeners. The “listeners” are what Kafka binds to and the “advertised listeners” configure how clients should connect to the cluster. The connection URLs a client receives is based on which listener a client connects to.

### Defining the listeners

To help this make sense, let’s look at how Kafka needs to be configured to support two connection opportunities:

1. Host connections (those coming through the host’s mapped port) - these will need to connect using localhost
2. Docker connections (those coming from inside the Docker networks) - these can not connect using localhost, but the network alias (or DNS address) of the Kafka service

Since there are two different methods clients need to connect, two different listeners are required - `HOST` and `DOCKER`. The `HOST` listener will tell clients to connect using localhost:9092, while the `DOCKER` listener will inform clients to connect using `kafka:9093`. Notice this means Kafka is listening on both ports 9092 and 9093. But, only the host listener needs to be exposed to the host.

![Diagram showing the DOCKER and HOST listeners and how they are exposed to the host and Docker networks](https://docs.docker.com/guides/images/kafka-1.webp)  ![Diagram showing the DOCKER and HOST listeners and how they are exposed to the host and Docker networks](https://docs.docker.com/guides/images/kafka-1.webp)

In order to set this up, the `compose.yaml` for Kafka needs some additional configuration. Once you start overriding some of the defaults, you also need to specify a few other options in order for KRaft mode to work.

```yaml
services:
  kafka:
    image: apache/kafka-native
    ports:
      - "9092:9092"
    environment:
      # Configure listeners for both docker and host communication
      KAFKA_LISTENERS: CONTROLLER://localhost:9091,HOST://0.0.0.0:9092,DOCKER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,DOCKER://kafka:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,DOCKER:PLAINTEXT,HOST:PLAINTEXT

      # Settings required for KRaft mode
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9091

      # Listener to use for broker-to-broker communication
      KAFKA_INTER_BROKER_LISTENER_NAME: DOCKER

      # Required for a single node cluster
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

Give it a try using the steps below.

1. If you have the Node app running from the previous step, go ahead and stop it by pressing `ctrl+c` in the terminal.
2. If you have the Kafka cluster running from the previous section, go ahead and stop that container using the following command:
  ```console
  $ docker rm -f kafka
  ```
3. Start the Compose stack by running the following command at the root of the cloned project directory:
  ```console
  $ docker compose up
  ```
  After a moment, the application will be up and running.
4. In the stack is another service that can be used to publish messages. Open it by going to [http://localhost:3000](http://localhost:3000). As you type in a message and submit the form, you should see the log message of the message being received by the app.
  This helps demonstrate how a containerized approach makes it easy to add additional services to help test and troubleshoot your application.

## Adding cluster visualization

Once you start using containers in your development environment, you start to realize the ease of adding additional services that are solely focused on helping development, such as visualizers and other supporting services. Since you have Kafka running, it might be helpful to visualize what’s going on in the Kafka cluster. To do so, you can run the [Kafbat UI web application](https://github.com/kafbat/kafka-ui).

To add it to your own project (it’s already in the demo application), you only need to add the following configuration to your Compose file:

```yaml
services:
  kafka-ui:
    image: kafbat/kafka-ui:main
    ports:
      - 8080:8080
    environment:
      DYNAMIC_CONFIG_ENABLED: "true"
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9093
    depends_on:
      - kafka
```

Then, once the Compose stack starts, you can open your browser to [http://localhost:8080](http://localhost:8080) and navigate around to view additional details about the cluster, check on consumers, publish test messages, and more.

## Testing with Kafka

If you’re interested in learning how you can integrate Kafka easily into your integration tests, check out the [Testing Spring Boot Kafka Listener using Testcontainers guide](https://testcontainers.com/guides/testing-spring-boot-kafka-listener-using-testcontainers/). This guide will teach you how to use Testcontainers to manage the lifecycle of Kafka containers in your tests.

## Conclusion

By using Docker, you can simplify the process of developing and testing event-driven applications with Kafka. Containers simplify the process of setting up and deploying the various services you need to develop. And once they’re defined in Compose, everyone on the team can benefit from the ease of use.

In case you missed it earlier, all of the sample app code can be found at dockersamples/kafka-development-node.

---

# Deploy to Kubernetes

> Learn how to describe and deploy a simple application on Kubernetes.

# Deploy to Kubernetes

   Table of contents

---

## Prerequisites

- Download and install Docker Desktop as described in
  [Get Docker](https://docs.docker.com/get-started/get-docker/).
- Work through containerizing an application in [Part 2](https://docs.docker.com/get-started/workshop/02_our_app/).
- Make sure that Kubernetes is turned on in Docker Desktop:
  If Kubernetes isn't running, follow the instructions in [Orchestration](https://docs.docker.com/guides/orchestration/) to finish setting it up.

## Introduction

Now that you've demonstrated that the individual components of your application run as stand-alone containers, it's time to arrange for them to be managed by an orchestrator like Kubernetes. Kubernetes provides many tools for scaling, networking, securing and maintaining your containerized applications, above and beyond the abilities of containers themselves.

In order to validate that your containerized application works well on Kubernetes, you'll use Docker Desktop's built in Kubernetes environment right on your development machine to deploy your application, before handing it off to run on a full Kubernetes cluster in production. The Kubernetes environment created by Docker Desktop is *fully featured*, meaning it has all the Kubernetes features your app will enjoy on a real cluster, accessible from the convenience of your development machine.

## Describing apps using Kubernetes YAML

All containers in Kubernetes are scheduled as pods, which are groups of co-located containers that share some resources. Furthermore, in a realistic application you almost never create individual pods. Instead, most of your workloads are scheduled as deployments, which are scalable groups of pods maintained automatically by Kubernetes. Lastly, all Kubernetes objects can and should be described in manifests called Kubernetes YAML files. These YAML files describe all the components and configurations of your Kubernetes app, and can be used to create and destroy your app in any Kubernetes environment.

You already wrote a basic Kubernetes YAML file in the Orchestration overview part of this tutorial. Now, you can write a slightly more sophisticated YAML file to run and manage your Todo app, the container `getting-started` image created in [Part 2](https://docs.docker.com/get-started/workshop/02_our_app/) of the Quickstart tutorial. Place the following in a file called `bb.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bb-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      bb: web
  template:
    metadata:
      labels:
        bb: web
    spec:
      containers:
        - name: bb-site
          image: getting-started
          imagePullPolicy: Never
---
apiVersion: v1
kind: Service
metadata:
  name: bb-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    bb: web
  ports:
    - port: 3000
      targetPort: 3000
      nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

- A `Deployment`, describing a scalable group of identical pods. In this case, you'll get just one `replica`, or copy of your pod, and that pod (which is described under the `template:` key) has just one container in it, based off of your `getting-started` image from the previous step in this tutorial.
- A `NodePort` service, which will route traffic from port 30001 on your host to port 3000 inside the pods it routes to, allowing you to reach your Todo app from the network.

Also, notice that while Kubernetes YAML can appear long and complicated at first, it almost always follows the same pattern:

- The `apiVersion`, which indicates the Kubernetes API that parses this object
- The `kind` indicating what sort of object this is
- Some `metadata` applying things like names to your objects
- The `spec` specifying all the parameters and configurations of your object.

## Deploy and check your application

1. In a terminal, navigate to where you created `bb.yaml` and deploy your application to Kubernetes:
  ```console
  $ kubectl apply -f bb.yaml
  ```
  You should see output that looks like the following, indicating your Kubernetes objects were created successfully:
  ```shell
  deployment.apps/bb-demo created
  service/bb-entrypoint created
  ```
2. Make sure everything worked by listing your deployments:
  ```console
  $ kubectl get deployments
  ```
  if all is well, your deployment should be listed as follows:
  ```shell
  NAME      READY   UP-TO-DATE   AVAILABLE   AGE
  bb-demo   1/1     1            1           40s
  ```
  This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services:
  ```console
  $ kubectl get services
  NAME            TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
  bb-entrypoint   NodePort    10.106.145.116   <none>        3000:30001/TCP   53s
  kubernetes      ClusterIP   10.96.0.1        <none>        443/TCP          138d
  ```
  In addition to the default `kubernetes` service, we see our `bb-entrypoint` service, accepting traffic on port 30001/TCP.
3. Open a browser and visit your Todo app at `localhost:30001`. You should see your Todo application, the same as when you ran it as a stand-alone container in [Part 2](https://docs.docker.com/get-started/workshop/02_our_app/) of the tutorial.
4. Once satisfied, tear down your application:
  ```console
  $ kubectl delete -f bb.yaml
  ```

## Conclusion

At this point, you have successfully used Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. You can now add other components to your app and taking advantage of all the features and power of Kubernetes, right on your own machine.

In addition to deploying to Kubernetes, you have also described your application as a Kubernetes YAML file. This simple text file contains everything you need to create your application in a running state. You can check it in to version control and share it with your colleagues. This let you distribute your applications to other clusters (like the testing and production clusters that probably come after your development environments).

## Kubernetes references

Further documentation for all new Kubernetes objects used in this article are available here:

- [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)

---

# Build a language translation app

> Learn how to build and run a language translation application using Python, Googletrans, and Docker.

# Build a language translation app

   Table of contents

---

## Overview

This guide walks you through building and running a language translation
application. You'll build the application using Python with Googletrans, and
then set up the environment and run the application using Docker.

The application demonstrates a simple but practical use of the Googletrans
library for language translation, showcasing basic Python and Docker concepts.
Googletrans is a free and unlimited Python library that implements the Google
Translate API. It uses the Google Translate Ajax API to make calls to such
methods as detect and translate.

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

The source code for the application is in the
`Docker-NLP/05_language_translation.py` file. Open `05_language_translation.py`
in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.
  ```python
  from googletrans import Translator
  ```
  This line imports the `Translator` class from `googletrans`.
  Googletrans is a Python library that provides an interface to Google
  Translate's AJAX API.
2. Specify the main execution block.
  ```python
  if __name__ == "__main__":
  ```
  This Python idiom ensures that the following code block runs only if this
  script is the main program. It provides flexibility, allowing the script to
  function both as a standalone program and as an imported module.
3. Create an infinite loop for continuous input.
  ```python
  while True:
        input_text = input("Enter the text for translation (type 'exit' to end): ")
        if input_text.lower() == 'exit':
           print("Exiting...")
           break
  ```
  An infinite loop is established here to continuously prompt you for text
  input, ensuring interactivity. The loop breaks when you type `exit`, allowing
  you to control the application flow effectively.
4. Create an instance of Translator.
  ```python
  translator = Translator()
  ```
  This creates an instance of the Translator class, which
  performs the translation.
5. Translate text.
  ```python
  translated_text = translator.translate(input_text, dest='fr').text
  ```
  Here, the `translator.translate` method is called with the user input. The
  `dest='fr'` argument specifies that the destination language for translation
  is French. The `.text` attribute gets the translated string. For more details
  about the available language codes, see the
  [Googletrans docs](https://py-googletrans.readthedocs.io/en/latest/).
6. Print the original and translated text.
  ```python
  print(f"Original Text: {input_text}")
        print(f"Translated Text: {translated_text}")
  ```
  These two lines print the original text entered by the user and the
  translated text.
7. Create `requirements.txt`. The sample application already contains the
  `requirements.txt` file to specify the necessary modules that the
  application imports. Open `requirements.txt` in a code or text editor to
  explore its contents.
  ```text
  ...
  # 05 language_translation
  googletrans==4.0.0-rc1
  ```
  Only `googletrans` is required for the language translation application.

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
  Dockerfile
  (like `COPY` and `RUN`) are executed in this directory. This also helps in
  organizing your Docker image, as all application-related files are contained
  in a specific directory.
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
  This step is specific to NLP applications that require the spaCy library. It downloads the `en_core_web_sm` model, which is a small English language model for spaCy. While not needed for this app, it's included for compatibility with other NLP applications that might use this Dockerfile.
6. Copy the application code into the image.
  ```dockerfile
  COPY *.py /app
  COPY entrypoint.sh /app
  ```
  These commands copy your Python scripts and the `entrypoint.sh` script into the image's `/app` directory. This is crucial because the container needs these scripts to run the application. The `entrypoint.sh` script is particularly important as it dictates how the application starts inside the container.
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
  $ docker run -it basic-nlp 05_language_translation.py
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
  - `05_language_translation.py`: This is the script you want to run inside the
    Docker container. It gets passed to the `entrypoint.sh` script, which runs
    it when the container starts.
  For more details, see the
  [docker run CLI reference](https://docs.docker.com/reference/cli/docker/container/run/).
  > Note
  >
  > For Windows users, you may get an error when running the container. Verify
  > that the line endings in the `entrypoint.sh` are `LF` (`\n`) and not `CRLF` (`\r\n`),
  > then rebuild the image. For more details, see [Avoid unexpected syntax errors, use Unix style line endings for files in containers](/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers).
  You will see the following in your console after the container starts.
  ```console
  Enter the text for translation (type 'exit' to end):
  ```
3. Test the application.
  Enter some text to get the text summarization.
  ```console
  Enter the text for translation (type 'exit' to end): Hello, how are you doing?
  Original Text: Hello, how are you doing?
  Translated Text: Bonjour comment allez-vous?
  ```

## Summary

In this guide, you learned how to build and run a language translation
application. You learned how to build the application using Python with
Googletrans, and then set up the environment and run the application using
Docker.

Related information:

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Googletrans](https://github.com/ssut/py-googletrans)
- [Python documentation](https://docs.python.org/3/)

## Next steps

Explore more [natural language processing guides](https://docs.docker.com/guides/).
