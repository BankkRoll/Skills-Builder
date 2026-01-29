# Build a sentiment analysis app and more

# Build a sentiment analysis app

> Learn how to build and run a sentiment analysis application using Python, NLTK, and Docker.

# Build a sentiment analysis app

   Table of contents

---

## Overview

In this guide, you learn how to build and run a sentiment analysis application.
You'll build the application using Python with the Natural Language Toolkit
(NLTK), and then set up the environment and run the application using Docker.

The application analyzes user input text for sentiment using NLTK's
SentimentIntensityAnalyzer and outputs whether the sentiment is positive,
negative, or neutral.

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

The source code for the sentiment analysis application is in the `Docker-NLP/01_sentiment_analysis.py` file. Open `01_sentiment_analysis.py` in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.
  ```python
  import nltk
  from nltk.sentiment import SentimentIntensityAnalyzer
  import ssl
  ```
  - `nltk`: This is the Natural Language Toolkit library used for working with
    human language data in Python.
  - `SentimentIntensityAnalyzer`: This is a specific tool from NLTK used for
    determining the sentiment of a piece of text.
  - `ssl`: This module provides access to Transport Layer Security (encryption)
    functions used for secure web connections.
2. Handle SSL certificate verification.
  ```python
  try:
      _create_unverified_https_context = ssl._create_unverified_context
  except AttributeError:
      pass
  else:
      ssl._create_default_https_context = _create_unverified_https_context
  ```
  This block is a workaround for certain environments where downloading data through NLTK might fail due to SSL certificate verification issues. It's telling Python to ignore SSL certificate verification for HTTPS requests.
3. Download NLTK resources.
  ```python
  nltk.download('vader_lexicon')
  nltk.download('punkt')
  ```
  - `vader_lexicon`: This is a lexicon used by the `SentimentIntensityAnalyzer`
    for sentiment analysis.
  - `punkt`: This is used by NLTK for tokenizing sentences. It's necessary for
    the `SentimentIntensityAnalyzer` to function correctly.
4. Create a sentiment analysis function.
  ```python
  def perform_semantic_analysis(text):
      sid = SentimentIntensityAnalyzer()
      sentiment_score = sid.polarity_scores(text)
      if sentiment_score['compound'] >= 0.05:
          return "Positive"
      elif sentiment_score['compound'] <= -0.05:
          return "Negative"
      else:
          return "Neutral"
  ```
  - `SentimentIntensityAnalyzer()` creates an instance of the
    analyzer.
  - `polarity_scores(text)` generates a sentiment score for the input text.
  The function returns **Positive**, **Negative**, or **Neutral** based on the
  compound score.
5. Create the main loop.
  ```python
  if __name__ == "__main__":
      while True:
          input_text = input("Enter the text for semantic analysis (type 'exit' to end): ")
          if input_text.lower() == 'exit':
              print("Exiting...")
              break
          result = perform_semantic_analysis(input_text)
          print(f"Sentiment: {result}")
  ```
  This part of the script runs an infinite loop to accept user input for
  analysis. If the user types `exit`, the program terminates. Otherwise, it
  prints out the sentiment of the provided text.
6. Create `requirements.txt`.
  The sample application already contains the
  `requirements.txt` file to specify the necessary packages that the
  application imports. Open `requirements.txt` in a code or text editor to
  explore its contents.
  ```text
  # 01 sentiment_analysis
  nltk==3.6.5
  ...
  ```
  Only the `nltk` package is required for the sentiment analysis application.

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
  This step is specific to NLP applications that require the spaCy library. It downloads the `en_core_web_sm` model, which is a small English language model for spaCy. While not needed for this app, it's included for compatibility with other NLP applications that might use this Dockerfile.
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
  Docker outputs several logs to your console as it builds the image. You'll
  see it download and install the dependencies. Depending on your network
  connection, this may take several minutes. Docker does have a caching
  feature, so subsequent builds can be faster. The console will
  return to the prompt when it's complete.
  For more details, see the
  [docker build CLI reference](https://docs.docker.com/reference/cli/docker/buildx/build/).
2. Run the image as a container.
  In a terminal, run the following command.
  ```console
  $ docker run -it basic-nlp 01_sentiment_analysis.py
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
  - `01_sentiment_analysis.py`: This is the script you want to run inside the
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
  Enter the text for semantic analysis (type 'exit' to end):
  ```
3. Test the application.
  Enter a comment to get the sentiment analysis.
  ```console
  Enter the text for semantic analysis (type 'exit' to end): I love containers!
  Sentiment: Positive
  Enter the text for semantic analysis (type 'exit' to end): I'm still learning about containers.
  Sentiment: Neutral
  ```

## Summary

In this guide, you learned how to build and run a sentiment analysis
application. You learned how to build the application using Python with NLTK,
and then set up the environment and run the application using Docker.

Related information:

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Python documentation](https://docs.python.org/3/)

## Next steps

Explore more [natural language processing guides](https://docs.docker.com/guides/).

---

# Deploy to Swarm

> Learn how to describe and deploy a simple application on Docker Swarm.

# Deploy to Swarm

   Table of contents

---

> Note
>
> Swarm mode is an advanced feature for managing a cluster of Docker daemons.
>
>
>
> Use Swarm mode if you intend to use Swarm as a production runtime environment.
>
>
>
> If you're not planning on deploying with Swarm, use
> [Docker Compose](https://docs.docker.com/compose/) instead.
> If you're developing for a Kubernetes deployment, consider using the
> [integrated Kubernetes feature](https://docs.docker.com/desktop/use-desktop/kubernetes/) in Docker Desktop.

## Prerequisites

- Download and install Docker Desktop as described in
  [Get Docker](https://docs.docker.com/get-started/get-docker/).
- Work through containerizing an application in
  [Docker workshop part 2](https://docs.docker.com/get-started/workshop/02_our_app/)
- Make sure that Swarm is enabled on your Docker Desktop by typing `docker system info`, and looking for a message `Swarm: active` (you might have to scroll up a little).
  If Swarm isn't running, simply type `docker swarm init` in a shell prompt to set it up.

## Introduction

Now that you've demonstrated that the individual components of your application run as stand-alone containers and shown how to deploy it using Kubernetes, you can look at how to arrange for them to be managed by Docker Swarm. Swarm provides many tools for scaling, networking, securing and maintaining your containerized applications, above and beyond the abilities of containers themselves.

In order to validate that your containerized application works well on Swarm, you'll use Docker Desktop's built in Swarm environment right on your development machine to deploy your application, before handing it off to run on a full Swarm cluster in production. The Swarm environment created by Docker Desktop is fully featured, meaning it has all the Swarm features your app will enjoy on a real cluster, accessible from the convenience of your development machine.

## Describe apps using stack files

Swarm never creates individual containers like you did in the previous step of this tutorial. Instead, all Swarm workloads are scheduled as services, which are scalable groups of containers with added networking features maintained automatically by Swarm. Furthermore, all Swarm objects can and should be described in manifests called stack files. These YAML files describe all the components and configurations of your Swarm app, and can be used to create and destroy your app in any Swarm environment.

Now you can write a simple stack file to run and manage your Todo app, the container `getting-started` image created in [Part 2](https://docs.docker.com/get-started/workshop/02_our_app/) of the tutorial. Place the following in a file called `bb-stack.yaml`:

> Note
>
> The `docker stack deploy` command uses the legacy
> [Compose file version 3](https://docs.docker.com/reference/compose-file/legacy-versions/)
> format, used by Compose V1. The latest format, defined by the
> [Compose specification](https://docs.docker.com/reference/compose-file/)
> isn't compatible with the `docker stack deploy` command.
>
>
>
> For more information about the evolution of Compose, see
> [History of Compose](https://docs.docker.com/compose/history/).

```yaml
version: "3.7"

services:
  bb-app:
    image: getting-started
    ports:
      - "8000:3000"
```

In this Swarm YAML file, there is one object, a `service`, describing a scalable group of identical containers. In this case, you'll get just one container (the default), and that container will be based on your `getting-started` image created in [Part 2](https://docs.docker.com/get-started/workshop/02_our_app/) of the tutorial. In addition, you've asked Swarm to forward all traffic arriving at port 8000 on your development machine to port 3000 inside our getting-started container.

> **Kubernetes Services and Swarm Services are very different**
>
>
>
> Despite the similar name, the two orchestrators mean very different things by
> the term 'service'. In Swarm, a service provides both scheduling and
> networking facilities, creating containers and providing tools for routing
> traffic to them. In Kubernetes, scheduling and networking are handled
> separately, deployments (or other controllers) handle the scheduling of
> containers as pods, while services are responsible only for adding
> networking features to those pods.

## Deploy and check your application

1. Deploy your application to Swarm:
  ```console
  $ docker stack deploy -c bb-stack.yaml demo
  ```
  If all goes well, Swarm will report creating all your stack objects with no complaints:
  ```shell
  Creating network demo_default
  Creating service demo_bb-app
  ```
  Notice that in addition to your service, Swarm also creates a Docker network by default to isolate the containers deployed as part of your stack.
2. Make sure everything worked by listing your service:
  ```console
  $ docker service ls
  ```
  If all has gone well, your service will report with 1/1 of its replicas created:
  ```shell
  ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
  il7elwunymbs        demo_bb-app         replicated          1/1                 getting-started:latest   *:8000->3000/tcp
  ```
  This indicates 1/1 containers you asked for as part of your services are up and running. Also, you see that port 8000 on your development machine is getting forwarded to port 3000 in your getting-started container.
3. Open a browser and visit your Todo app at `localhost:8000`; you should see your Todo application, the same as when you ran it as a stand-alone container in [Part 2](https://docs.docker.com/get-started/workshop/02_our_app/) of the tutorial.
4. Once satisfied, tear down your application:
  ```console
  $ docker stack rm demo
  ```

## Conclusion

At this point, you've successfully used Docker Desktop to deploy your application to a fully-featured Swarm environment on your development machine. You can now add other components to your app and taking advantage of all the features and power of Swarm, right on your own machine.

In addition to deploying to Swarm, you've also described your application as a stack file. This simple text file contains everything you need to create your application in a running state; you can check it in to version control and share it with your colleagues, letting you to distribute your applications to other clusters (like the testing and production clusters that probably come after your development environments).

## Swarm and CLI references

Further documentation for all new Swarm objects and CLI commands used in this article are available here:

- [Swarm Mode](https://docs.docker.com/engine/swarm/)
- [Swarm Mode Services](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/)
- [Swarm Stacks](https://docs.docker.com/engine/swarm/stack-deploy/)
- [docker stack *](https://docs.docker.com/reference/cli/docker/stack/)
- [docker service *](https://docs.docker.com/reference/cli/docker/service/)

---

# Face detection with TensorFlow.js

> Learn how to deploy pre-trained models in a TensorFlow.js web applications to perform face detection.

# Face detection with TensorFlow.js

   Table of contents

---

This guide introduces the seamless integration of TensorFlow.js with Docker to
perform face detection. In this guide, you'll explore how to:

- Run a containerized TensorFlow.js application using Docker.
- Implement face detection in a web application with TensorFlow.js.
- Construct a Dockerfile for a TensorFlow.js web application.
- Use Docker Compose for real-time application development and updates.
- Share your Docker image on Docker Hub to facilitate deployment and extend
  reach.

> **Acknowledgment**
>
>
>
> Docker would like to thank [Harsh Manvar](https://github.com/harsh4870) for
> his contribution to this guide.

## Prerequisites

- You have installed the latest version of
  [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
- You have a [Git client](https://git-scm.com/downloads). The examples in this
  guide use a command-line based Git client, but you can use any client.

## What is TensorFlow.js?

[TensorFlow.js](https://www.tensorflow.org/js) is an open-source JavaScript
library for machine learning that enables you to train and deploy ML models in
the browser or on Node.js. It supports creating new models from scratch or using
pre-trained models, facilitating a wide range of ML applications directly in web
environments. TensorFlow.js offers efficient computation, making sophisticated
ML tasks accessible to web developers without deep ML expertise.

## Why Use TensorFlow.js and Docker together?

- Environment consistency and simplified deployment: Docker packages
  TensorFlow.js applications and their dependencies into containers, ensuring
  consistent runs across all environments and simplifying deployment.
- Efficient development and easy scaling: Docker enhances development efficiency
  with features like hot reloading and facilitates easy scaling of -
  TensorFlow.js applications using orchestration tools like Kubernetes.
- Isolation and enhanced security: Docker isolates TensorFlow.js applications in
  secure environments, minimizing conflicts and security vulnerabilities while
  running applications with limited permissions.

## Get and run the sample application

In a terminal, clone the sample application using the following command.

```console
$ git clone https://github.com/harsh4870/TensorJS-Face-Detection
```

After cloning the application, you'll notice the application has a `Dockerfile`.
This Dockerfile lets you build and run the application locally with nothing more
than Docker.

Before you run the application as a container, you must build it into an image.
Run the following command inside the `TensorJS-Face-Detection` directory to
build an image named `face-detection-tensorjs`.

```console
$ docker build -t face-detection-tensorjs .
```

The command builds the application into an image. Depending on your network
connection, it can take several minutes to download the necessary components the
first time you run the command.

To run the image as a container, run the following command in a terminal.

```console
$ docker run -p 80:80 face-detection-tensorjs
```

The command runs the container and maps port 80 in the container to port 80 on
your system.

Once the application is running, open a web browser and access the application
at [http://localhost:80](http://localhost:80). You may need to grant access to
your webcam for the application.

In the web application, you can change the backend to use one of the following:

- WASM
- WebGL
- CPU

To stop the application, press `ctrl`+`c` in the terminal.

## About the application

The sample application performs real-time face detection using
[MediaPipe](https://developers.google.com/mediapipe/), a comprehensive framework
for building multimodal machine learning pipelines. It's specifically using the
BlazeFace model, a lightweight model for detecting faces in images.

In the context of TensorFlow.js or similar web-based machine learning
frameworks, the WASM, WebGL, and CPU backends can be used to
execute operations. Each of these backends utilizes different resources and
technologies available in modern browsers and has its strengths and limitations.
The following sections are a brief breakdown of the different backends.

### WASM

WebAssembly (WASM) is a low-level, assembly-like language with a compact binary
format that runs at near-native speed in web browsers. It allows code written in
languages like C/C++ to be compiled into a binary that can be executed in the
browser.

It's a good choice when high performance is required, and either the WebGL
backend is not supported or you want consistent performance across all devices
without relying on the GPU.

### WebGL

WebGL is a browser API that allows for GPU-accelerated usage of physics and
image processing and effects as part of the web page canvas.

WebGL is well-suited for operations that are parallelizable and can
significantly benefit from GPU acceleration, such as matrix multiplications and
convolutions commonly found in deep learning models.

### CPU

The CPU backend uses pure JavaScript execution, utilizing the device's central
processing unit (CPU). This backend is the most universally compatible and
serves as a fallback when neither WebGL nor WASM backends are available or
suitable.

## Explore the application's code

Explore the purpose of each file and their contents in the following sections.

### The index.html file

The `index.html` file serves as the frontend for the web application that
utilizes TensorFlow.js for real-time face detection from the webcam video feed.
It incorporates several technologies and libraries to facilitate machine
learning directly in the browser. It uses several TensorFlow.js libraries,
including:

- tfjs-core and tfjs-converter for core TensorFlow.js functionality and model
  conversion.
- tfjs-backend-webgl, tfjs-backend-cpu, and the tf-backend-wasm script
  for different computational backend options that TensorFlow.js can use for
  processing. These backends allow the application to perform machine learning
  tasks efficiently by leveraging the user's hardware capabilities.
- The BlazeFace library, a TensorFlow model for face detection.

It also uses the following additional libraries:

- dat.GUI for creating a graphical interface to interact with the application's
  settings in real-time, such as switching between TensorFlow.js backends.
- Stats.min.js for displaying performance metrics (like FPS) to monitor the
  application's efficiency during operation.

```html
<style>
  body {
    margin: 25px;
  }

  .true {
    color: green;
  }

  .false {
    color: red;
  }

  #main {
    position: relative;
    margin: 50px 0;
  }

  canvas {
    position: absolute;
    top: 0;
    left: 0;
  }

  #description {
    margin-top: 20px;
    width: 600px;
  }

  #description-title {
    font-weight: bold;
    font-size: 18px;
  }
</style>

<body>
  <div id="main">
    <video
      id="video"
      playsinline
      style="
      -webkit-transform: scaleX(-1);
      transform: scaleX(-1);
      width: auto;
      height: auto;
      "
    ></video>
    <canvas id="output"></canvas>
    <video
      id="video"
      playsinline
      style="
      -webkit-transform: scaleX(-1);
      transform: scaleX(-1);
      visibility: hidden;
      width: auto;
      height: auto;
      "
    ></video>
  </div>
</body>
<script src="https://unpkg.com/@tensorflow/tfjs-core@2.1.0/dist/tf-core.js"></script>
<script src="https://unpkg.com/@tensorflow/tfjs-converter@2.1.0/dist/tf-converter.js"></script>

<script src="https://unpkg.com/@tensorflow/tfjs-backend-webgl@2.1.0/dist/tf-backend-webgl.js"></script>
<script src="https://unpkg.com/@tensorflow/tfjs-backend-cpu@2.1.0/dist/tf-backend-cpu.js"></script>
<script src="./tf-backend-wasm.js"></script>

<script src="https://unpkg.com/@tensorflow-models/blazeface@0.0.5/dist/blazeface.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dat-gui/0.7.6/dat.gui.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/stats.js/r16/Stats.min.js"></script>
<script src="./index.js"></script>
```

### The index.js file

The `index.js` file conducts the facial detection logic. It demonstrates several
advanced concepts in web development and machine learning integration. Here's a
breakdown of some of its key components and functionalities:

- Stats.js: The script starts by creating a Stats instance to monitor and
  display the frame rate (FPS) of the application in real time. This is helpful
  for performance analysis, especially when testing the impact of different
  TensorFlow.js backends on the application's speed.
- TensorFlow.js: The application allows users to switch between different
  computation backends (wasm, webgl, and cpu) for TensorFlow.js through a
  graphical interface provided by dat.GUI. Changing the backend can affect
  performance and compatibility depending on the device and browser. The
  addFlagLabels function dynamically checks and displays whether SIMD (Single
  Instruction, Multiple Data) and multithreading are supported, which are
  relevant for performance optimization in the wasm backend.
- setupCamera function: Initializes the user's webcam using the MediaDevices Web
  API. It configures the video stream to not include audio and to use the
  front-facing camera (facingMode: 'user'). Once the video metadata is loaded,
  it resolves a promise with the video element, which is then used for face
  detection.
- BlazeFace: The core of this application is the renderPrediction function,
  which performs real-time face detection using the BlazeFace model, a
  lightweight model for detecting faces in images. The function calls
  model.estimateFaces on each animation frame to detect faces from the video
  feed. For each detected face, it draws a red rectangle around the face and
  blue dots for facial landmarks on a canvas overlaying the video.

```javascript
const stats = new Stats();
stats.showPanel(0);
document.body.prepend(stats.domElement);

let model, ctx, videoWidth, videoHeight, video, canvas;

const state = {
  backend: "wasm",
};

const gui = new dat.GUI();
gui
  .add(state, "backend", ["wasm", "webgl", "cpu"])
  .onChange(async (backend) => {
    await tf.setBackend(backend);
    addFlagLables();
  });

async function addFlagLables() {
  if (!document.querySelector("#simd_supported")) {
    const simdSupportLabel = document.createElement("div");
    simdSupportLabel.id = "simd_supported";
    simdSupportLabel.style = "font-weight: bold";
    const simdSupported = await tf.env().getAsync("WASM_HAS_SIMD_SUPPORT");
    simdSupportLabel.innerHTML = `SIMD supported: <span class=${simdSupported}>${simdSupported}<span>`;
    document.querySelector("#description").appendChild(simdSupportLabel);
  }

  if (!document.querySelector("#threads_supported")) {
    const threadSupportLabel = document.createElement("div");
    threadSupportLabel.id = "threads_supported";
    threadSupportLabel.style = "font-weight: bold";
    const threadsSupported = await tf
      .env()
      .getAsync("WASM_HAS_MULTITHREAD_SUPPORT");
    threadSupportLabel.innerHTML = `Threads supported: <span class=${threadsSupported}>${threadsSupported}</span>`;
    document.querySelector("#description").appendChild(threadSupportLabel);
  }
}

async function setupCamera() {
  video = document.getElementById("video");

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: { facingMode: "user" },
  });
  video.srcObject = stream;

  return new Promise((resolve) => {
    video.onloadedmetadata = () => {
      resolve(video);
    };
  });
}

const renderPrediction = async () => {
  stats.begin();

  const returnTensors = false;
  const flipHorizontal = true;
  const annotateBoxes = true;
  const predictions = await model.estimateFaces(
    video,
    returnTensors,
    flipHorizontal,
    annotateBoxes,
  );

  if (predictions.length > 0) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < predictions.length; i++) {
      if (returnTensors) {
        predictions[i].topLeft = predictions[i].topLeft.arraySync();
        predictions[i].bottomRight = predictions[i].bottomRight.arraySync();
        if (annotateBoxes) {
          predictions[i].landmarks = predictions[i].landmarks.arraySync();
        }
      }

      const start = predictions[i].topLeft;
      const end = predictions[i].bottomRight;
      const size = [end[0] - start[0], end[1] - start[1]];
      ctx.fillStyle = "rgba(255, 0, 0, 0.5)";
      ctx.fillRect(start[0], start[1], size[0], size[1]);

      if (annotateBoxes) {
        const landmarks = predictions[i].landmarks;

        ctx.fillStyle = "blue";
        for (let j = 0; j < landmarks.length; j++) {
          const x = landmarks[j][0];
          const y = landmarks[j][1];
          ctx.fillRect(x, y, 5, 5);
        }
      }
    }
  }

  stats.end();

  requestAnimationFrame(renderPrediction);
};

const setupPage = async () => {
  await tf.setBackend(state.backend);
  addFlagLables();
  await setupCamera();
  video.play();

  videoWidth = video.videoWidth;
  videoHeight = video.videoHeight;
  video.width = videoWidth;
  video.height = videoHeight;

  canvas = document.getElementById("output");
  canvas.width = videoWidth;
  canvas.height = videoHeight;
  ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgba(255, 0, 0, 0.5)";

  model = await blazeface.load();

  renderPrediction();
};

setupPage();
```

### The tf-backend-wasm.js file

The `tf-backend-wasm.js` file is part of the
[TensorFlow.js library](https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-wasm).
It contains initialization logic for the TensorFlow.js WASM backend, some
utilities for interacting with the WASM binaries, and functions to set custom
paths for the WASM binaries.

### The tfjs-backend-wasm-simd.wasm file

The `tfjs-backend-wasm-simd.wasm` file is part of the
[TensorFlow.js library](https://github.com/tensorflow/tfjs/tree/master/tfjs-backend-wasm).
It's a WASM binary that's used for the WebAssembly
backend, specifically optimized to utilize SIMD (Single Instruction, Multiple
Data) instructions.

## Explore the Dockerfile

In a Docker-based project, the Dockerfile serves as the foundational
asset for building your application's environment.

A Dockerfile is a text file that instructs Docker how to create an image of your
application's environment. An image contains everything you want and
need when running application, such as files, packages, and tools.

The following is the Dockerfile for this project.

```dockerfile
FROM nginx:stable-alpine3.17-slim
WORKDIR /usr/share/nginx/html
COPY . .
```

This Dockerfile defines an image that serves static content using Nginx from an
Alpine Linux base image.

## Develop with Compose

Docker Compose is a tool for defining and running multi-container Docker
applications. With Compose, you use a YAML file to configure your application's
services, networks, and volumes. In this case, the application isn't a
multi-container application, but Docker Compose has other useful features for
development, like
[Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

The sample application doesn't have a Compose file yet. To create a Compose
file, in the `TensorJS-Face-Detection` directory, create a text file named
`compose.yaml` and then add the following contents.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 80:80
    develop:
      watch:
        - action: sync
          path: .
          target: /usr/share/nginx/html
```

This Compose file defines a service that is built using the Dockerfile in the
same directory. It maps port 80 on the host to port 80 in the container. It also
has a `develop` subsection with the `watch` attribute that defines a list of
rules that control automatic service updates based on local file changes. For
more details about the Compose instructions, see the
[Compose file reference](https://docs.docker.com/reference/compose-file/).

Save the changes to your `compose.yaml` file and then run the following command to run the application.

```console
$ docker compose watch
```

Once the application is running, open a web browser and access the application
at [http://localhost:80](http://localhost:80). You may need to grant access to
your webcam for the application.

Now you can make changes to the source code and see the changes automatically
reflected in the container without having to rebuild and rerun the container.

Open the `index.js` file and update the landmark points to be green instead of
blue on line 83.

```diff
-        ctx.fillStyle = "blue";
+        ctx.fillStyle = "green";
```

Save the changes to the `index.js` file and then refresh the browser page. The
landmark points should now appear green.

To stop the application, press `ctrl`+`c` in the terminal.

## Share your image

Publishing your Docker image on Docker Hub streamlines deployment processes for
others, enabling seamless integration into diverse projects. It also promotes
the adoption of your containerized solutions, broadening their impact across the
developer ecosystem. To share your image:

1. [Sign up](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade) or sign in to [Docker Hub](https://hub.docker.com).
2. Rebuild your image to include the changes to your application. This time,
  prefix the image name with your Docker ID. Docker uses the name to determine
  which repository to push it to. Open a terminal and run the following
  command in the `TensorJS-Face-Detection` directory. Replace `YOUR-USER-NAME`
  with your Docker ID.
  ```console
  $ docker build -t YOUR-USER-NAME/face-detection-tensorjs .
  ```
3. Run the following `docker push` command to push the image to Docker Hub.
  Replace `YOUR-USER-NAME` with your Docker ID.
  ```console
  $ docker push YOUR-USER-NAME/face-detection-tensorjs
  ```
4. Verify that you pushed the image to Docker Hub.
  1. Go to [Docker Hub](https://hub.docker.com).
  2. Select **My Hub** > **Repositories**.
  3. View the **Last pushed** time for your repository.

Other users can now download and run your image using the `docker run` command. They need to replace `YOUR-USER-NAME` with your Docker ID.

```console
$ docker run -p 80:80 YOUR-USER-NAME/face-detection-tensorjs
```

## Summary

This guide demonstrated leveraging TensorFlow.js and Docker for face detection
in web applications. It highlighted the ease of running containerized
TensorFlow.js applications, and developing with Docker Compose for real-time
code changes. Additionally, it covered how sharing your Docker image on Docker
Hub can streamline deployment for others, enhancing the application's reach
within the developer community.

Related information:

- [TensorFlow.js website](https://www.tensorflow.org/js)
- [MediaPipe website](https://developers.google.com/mediapipe/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Docker Blog: Accelerating Machine Learning with TensorFlow.js](https://www.docker.com/blog/accelerating-machine-learning-with-tensorflow-js-using-pretrained-models-and-docker/)

---

# Common challenges and questions

> Explore common challenges and questions related to Testcontainers Cloud by Docker.

# Common challenges and questions

   Table of contents

---

### How is Testcontainers Cloud different from the open-source Testcontainers framework?

While the open-source Testcontainers is a library that provides a lightweight APIs for bootstrapping local development and test dependencies with real services wrapped in Docker containers, Testcontainers Cloud provides a cloud runtime for these containers. This reduces the resource strain on local environments and provides more scalability, especially in CI/CD workflows, that enables consistent Testcontainers experience across the organization.

### What types of containers can I run with Testcontainers Cloud?

Testcontainers Cloud supports any containers you would typically use with the Testcontainers framework, including databases (PostgreSQL, MySQL, MongoDB), message brokers (Kafka, RabbitMQ), and other services required for integration testing.

### Do I need to change my existing test code to use Testcontainers Cloud?

No, you don't need to change your existing test code. Testcontainers Cloud integrates seamlessly with the open-source Testcontainers framework. Once the cloud configuration is set up, it automatically manages the containers in the cloud without requiring code changes.

### How do I integrate Testcontainers Cloud into my project?

To integrate Testcontainers Cloud, you need to install the Testcontainers Desktop app and select run with Testcontainers Cloud option in the menu. In CI you’ll need to add a workflow step that downloads Testcontainers Cloud agent. No code changes are required beyond enabling Cloud runtime via the Testcontainers Desktop app locally or installing Testcontainers Cloud agent in CI.

### Can I use Testcontainers Cloud in a CI/CD pipeline?

Yes, Testcontainers Cloud is designed to work efficiently in CI/CD pipelines. It helps reduce build times and resource bottlenecks by offloading containers that you spin up with Testcontainers library to the cloud, making it a perfect fit for continuous testing environments.

### What are the benefits of using Testcontainers Cloud?

The key benefits include reduced resource usage on local machines and CI servers, scalability (run more containers without performance degradation), consistent testing environments, centralized monitoring, ease of CI configuration with removed security concerns of running Docker-in-Docker or a privileged daemon.

### Does Testcontainers Cloud support all programming languages?

Testcontainers Cloud supports any language that works with the open-source Testcontainers libraries, including Java, Python, Node.js, Go, and others. As long as your project uses Testcontainers, it can be offloaded to Testcontainers Cloud.

### How is container cleanup handled in Testcontainers Cloud?

While Testcontainers library automatically handles container lifecycle management, Testcontainers Cloud manages the allocated cloud worker lifetime. This means that containers are spun up, monitored, and cleaned up after tests are completed by Testcontainers library, and the worker where these containers have being running will be removed automatically after the ~35 min idle period by Testcontainers Cloud. This approach frees developers from manually managing containers and associated cloud resources.

### Is there a free tier or pricing model for Testcontainers Cloud?

Pricing details for Testcontainers Cloud can be found on the [pricing page](https://testcontainers.com/cloud/pricing/).

---

# Configuring Testcontainers Cloud in the CI Pipeline

> Use Testcontainers Cloud with GitHub Workflows to automate testing in a CI pipeline.

# Configuring Testcontainers Cloud in the CI Pipeline

---

This demo shows how Testcontainers Cloud can be seamlessly integrated into a
Continuous Integration (CI) pipeline using GitHub Workflows, providing a
powerful solution for running containerized integration tests without
overloading local or CI runner resources. By leveraging GitHub Actions,
developers can automate the process of spinning up and managing containers for
testing in the cloud, ensuring faster and more reliable test execution. With
just a few configuration steps, including setting up Testcontainers Cloud
authentication and adding it to your workflow, you can offload container
orchestration to the cloud. This approach improves the scalability of your
pipeline, ensures consistency across tests, and simplifies resource management,
making it an ideal solution for modern, containerized development workflows.

- Understand how to set up a GitHub Actions workflow to automate the build and testing of a project.
- Learn how to configure Testcontainers Cloud within GitHub Actions to offload containerized testing to the cloud, improving efficiency and resource management.
- Explore how Testcontainers Cloud integrates with GitHub workflows to run integration tests that require containerized services, such as databases and message brokers.

---

# Setting up Testcontainers Cloud by Docker

> Set up Testcontainers Cloud by Docker in a local development environment.

# Setting up Testcontainers Cloud by Docker

---

This demo shows the process of setting up Testcontainers Cloud by Docker to
work in your local development environment using the Testcontainers Desktop
application. By the end of this walkthrough, you'll have Testcontainers Cloud
by Docker up and running, ready to offload container management from your local
machine to the cloud for more efficient testing.

- Install and configure Testcontainers Cloud and the CLI to seamlessly integrate with your local development environment.
- Set up and configure the Testcontainers Desktop application to monitor and manage cloud-based containers during local tests.
- Create and run integration tests using Testcontainers that leverage cloud-based container resources.
- Monitor and manage containers efficiently, understanding how Testcontainers Cloud automates cleanup and ensures consistent testing environments.
- Review options for monitoring and troubleshooting in the Testcontainers Cloud Dashboard.
