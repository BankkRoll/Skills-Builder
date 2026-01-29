# Why Testcontainers Cloud? and more

# Why Testcontainers Cloud?

> Learn how Testcontainers Cloud by Docker can help you optimize integration testing.

# Why Testcontainers Cloud?

---

Testcontainers Cloud is a powerful cloud-based solution designed to optimize integration testing with Testcontainers by offloading container management to the cloud. It helps developers and teams overcome the limitations of traditional local and CI-based testing, ensuring consistent environments, faster test execution, and scalable workflows. Whether you're new to Testcontainers or looking to enhance your existing setup, Testcontainers Cloud offers a seamless way to manage containerized tests, improving efficiency and reliability in your development pipeline.

Testcontainers Cloud provides several benefits:

- **Offloading to the Cloud:** Frees up local resources by shifting container management to the cloud, keeping your laptop responsive.
- **Consistent Testing Environments:** Ensures that tests run in isolated, reliable environments, reducing inconsistencies across platforms from Dev to CI.
- **Scalability:** Allows running large numbers of containers simultaneously without being limited by local or CI resources.
- **Faster CI/CD Pipelines:** Reduces configuration bottlenecks and speeds up build times by offloading containers to multiple on-demand cloud workers with the Turbo-mode feature.

Testcontainers Cloud streamlines integration testing by offloading container management to the cloud, ensuring consistent environments and faster test execution resulting in reduced resource strain, making it an essential tool for improving the stability of your Testcontainers-based workflows.

---

# Mastering Testcontainers Cloud by Docker: streamlining integration testing with containers

> Testcontainers Cloud by Docker streamlines integration testing by offloading container management to the cloud. It enables faster, consistent tests for containerized services like databases, improving performance and scalability in CI/CD pipelines without straining local or CI resources. Ideal for developers needing efficient, reliable testing environments.

# Mastering Testcontainers Cloud by Docker: streamlining integration testing with containers

Table of contents

---

Testcontainers Cloud is a cloud-based solution designed to streamline and enhance the process of running integration tests using Testcontainers. Testcontainers is the open source framework, which allows developers to easily spin up containerized dependencies such as databases, message brokers, and other services required for testing. By shifting the management of Testcontainers-based services to the cloud, Testcontainers Cloud optimizes performance, reduces resource constraints on local machines or CI servers, and ensures consistent test environments. This solution is particularly beneficial for teams working on complex, distributed systems, as it allows for scalable, isolated, and reliable testing without the typical overhead of managing containers locally.

## What you'll learn

- Understand the fundamentals of Docker Testcontainers Cloud and its role in integration testing.
- Learn how to set up and configure Docker Testcontainers Cloud for automated testing in various environments.
- Explore how Testcontainers Cloud integrates with CI/CD pipelines to streamline testing workflows.

## Tools integration

Works well with Docker Desktop, GitHub Actions, Jenkins, Kubernetes, and other CI solutions

Docker Pro, Team, and Business subscriptions come with Testcontainers Cloud runtime minutes, and additional minutes are available via consumption pricing. Testcontainers Cloud runtime minutes do not rollover month to month.

## Who’s this for?

- Teams that build cloud-native applications and are already using Testcontainers open source.
- DevOps Teams that integrate automated container-based testing into CI/CD pipelines for continuous testing.
- QA Teams that seek scalable and consistent test environments for comprehensive integration and end-to-end testing.
- Developers who need reliable, containerized test environments for testing microservices and databases.

## Modules

1. [Why Testcontainers Cloud?](https://docs.docker.com/guides/testcontainers-cloud/why/)
  Learn how Testcontainers Cloud by Docker can help you optimize integration testing.
2. [Setting up Testcontainers Cloud by Docker](https://docs.docker.com/guides/testcontainers-cloud/demo-local/)
  Set up Testcontainers Cloud by Docker in a local development environment.
3. [Configuring Testcontainers Cloud in the CI Pipeline](https://docs.docker.com/guides/testcontainers-cloud/demo-ci/)
  Use Testcontainers Cloud with GitHub Workflows to automate testing in a CI pipeline.
4. [Common challenges and questions](https://docs.docker.com/guides/testcontainers-cloud/common-questions/)
  Explore common challenges and questions related to Testcontainers Cloud by Docker.

---

# Build a text recognition app

> Learn how to build and run a text recognition application using Python, NLTK, scikit-learn, and Docker.

# Build a text recognition app

   Table of contents

---

## Overview

In this guide, you'll learn how to create and run a text recognition
application. You'll build the application using Python with scikit-learn and the
Natural Language Toolkit (NLTK). Then you'll set up the environment and run the
application using Docker.

The application analyzes the sentiment of a user's input text using NLTK's
SentimentIntensityAnalyzer. It lets the user input text, which is then processed
to determine its sentiment, classifying it as either positive or negative. Also,
it displays the accuracy and a detailed classification report of its sentiment
analysis model based on a predefined dataset.

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

The source code for the text classification application is in the `Docker-NLP/03_text_classification.py` file. Open `03_text_classification.py` in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.
  ```python
  import nltk
  from nltk.sentiment import SentimentIntensityAnalyzer
  from sklearn.metrics import accuracy_score, classification_report
  from sklearn.model_selection import train_test_split
  import ssl
  ```
  - `nltk`: A popular Python library for natural language processing (NLP).
  - `SentimentIntensityAnalyzer`: A component of `nltk` for sentiment analysis.
  - `accuracy_score`, `classification_report`: Functions from scikit-learn for
    evaluating the model.
  - `train_test_split`: Function from scikit-learn to split datasets into
    training and testing sets.
  - `ssl`: Used for handling SSL certificate issues which might occur while
    downloading data for `nltk`.
2. Handle SSL certificate verification.
  ```python
  try:
      _create_unverified_https_context = ssl._create_unverified_context
  except AttributeError:
      pass
  else:
      ssl._create_default_https_context = _create_unverified_https_context
  ```
  This block is a workaround for certain environments where downloading data
  through NLTK might fail due to SSL certificate verification issues. It's
  telling Python to ignore SSL certificate verification for HTTPS requests.
3. Download NLTK resources.
  ```python
  nltk.download('vader_lexicon')
  ```
  The `vader_lexicon` is a lexicon used by the `SentimentIntensityAnalyzer` for
  sentiment analysis.
4. Define text for testing and corresponding labels.
  ```python
  texts = [...]
  labels = [0, 1, 2, 0, 1, 2]
  ```
  This section defines a small dataset of texts and their corresponding labels (0 for positive, 1 for negative, and 2 for spam).
5. Split the test data.
  ```python
  X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
  ```
  This part splits the dataset into training and testing sets, with 20% of data
  as the test set. As this application uses a pre-trained model, it doesn't
  train the model.
6. Set up sentiment analysis.
  ```python
  sia = SentimentIntensityAnalyzer()
  ```
  This code initializes the `SentimentIntensityAnalyzer` to analyze the
  sentiment of text.
7. Generate predictions and classifications for the test data.
  ```python
  vader_predictions = [sia.polarity_scores(text)["compound"] for text in X_test]
  threshold = 0.2
  vader_classifications = [0 if score > threshold else 1 for score in vader_predictions]
  ```
  This part generates sentiment scores for each text in the test set and classifies them as positive or negative based on a threshold.
8. Evaluate the model.
  ```python
  accuracy = accuracy_score(y_test, vader_classifications)
  report_vader = classification_report(y_test, vader_classifications, zero_division='warn')
  ```
  This part calculates the accuracy and classification report for the predictions.
9. Specify the main execution block.
  ```python
  if __name__ == "__main__":
  ```
  This Python idiom ensures that the following code block runs only if this
  script is the main program. It provides flexibility, allowing the script to
  function both as a standalone program and as an imported module.
10. Create an infinite loop for continuous input.
  ```python
  while True:
      input_text = input("Enter the text for classification (type 'exit' to end): ")
        if input_text.lower() == 'exit':
           print("Exiting...")
           break
  ```
  This while loop runs indefinitely until it's explicitly broken. It lets the
  user continuously enter text for entity recognition until they decide to
  exit.
11. Analyze the text.
  ```python
  input_text_score = sia.polarity_scores(input_text)["compound"]
          input_text_classification = 0 if input_text_score > threshold else 1
  ```
12. Print the VADER Classification Report and the sentiment analysis.
  ```python
  print(f"Accuracy: {accuracy:.2f}")
          print("\nVADER Classification Report:")
          print(report_vader)
          print(f"\nTest Text (Positive): '{input_text}'")
          print(f"Predicted Sentiment: {'Positive' if input_text_classification == 0 else 'Negative'}")
  ```
13. Create `requirements.txt`. The sample application already contains the
  `requirements.txt` file to specify the necessary packages that the
  application imports. Open `requirements.txt` in a code or text editor to
  explore its contents.
  ```text
  # 01 sentiment_analysis
  nltk==3.6.5
  ...
  # 03 text_classification
  scikit-learn==1.3.2
  ...
  ```
  Both the `nltk` and `scikit-learn` modules are required for the text
  classification application.

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
  $ docker run -it basic-nlp 03_text_classification.py
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
  - `03_text_classification.py`: This is the script you want to run inside the
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
  Enter the text for classification (type 'exit' to end):
  ```
3. Test the application.
  Enter some text to get the text classification.
  ```console
  Enter the text for classification (type 'exit' to end): I love containers!
  Accuracy: 1.00
  VADER Classification Report:
                precision    recall  f1-score   support
             0       1.00      1.00      1.00         1
             1       1.00      1.00      1.00         1
      accuracy                           1.00         2
     macro avg       1.00      1.00      1.00         2
  weighted avg       1.00      1.00      1.00         2
  Test Text (Positive): 'I love containers!'
  Predicted Sentiment: Positive
  ```

## Summary

In this guide, you learned how to build and run a text classification
application. You learned how to build the application using Python with
scikit-learn and NLTK. Then you learned how to set up the environment and run
the application using Docker.

Related information:

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Python documentation](https://docs.python.org/3/)
- [scikit-learn](https://scikit-learn.org/)

## Next steps

Explore more [natural language processing guides](https://docs.docker.com/guides/).

---

# Build a text summarization app

> Learn how to build and run a text summarization application using Python, Bert Extractive Summarizer, and Docker.

# Build a text summarization app

   Table of contents

---

## Overview

In this guide, you'll learn how to build and run a text summarization
application. You'll build the application using Python with the Bert Extractive
Summarizer, and then set up the environment and run the application using
Docker.

The sample text summarization application uses the Bert Extractive Summarizer.
This tool utilizes the HuggingFace Pytorch transformers library to run
extractive summarizations. This works by first embedding the sentences, then
running a clustering algorithm, finding the sentences that are closest to the
cluster's centroids.

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

The source code for the text summarization application is in the `Docker-NLP/04_text_summarization.py` file. Open `04_text_summarization.py` in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.
  ```python
  from summarizer import Summarizer
  ```
  This line of code imports the `Summarizer` class from the `summarizer`
  package, essential for your text summarization application. The summarizer
  module implements the Bert Extractive Summarizer, leveraging the HuggingFace
  Pytorch transformers library, renowned in the NLP (Natural Language
  Processing) domain. This library offers access to pre-trained models like
  BERT, which revolutionized language understanding tasks, including text
  summarization.
  The BERT model, or Bidirectional Encoder Representations from Transformers,
  excels in understanding context in language, using a mechanism known as
  "attention" to determine the significance of words in a sentence. For
  summarization, the model embeds sentences and then uses a clustering
  algorithm to identify key sentences, those closest to the centroids of these
  clusters, effectively capturing the main ideas of the text.
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
        input_text = input("Enter the text for summarization (type 'exit' to end): ")
        if input_text.lower() == 'exit':
           print("Exiting...")
           break
  ```
  An infinite loop continuously prompts you for text
  input, ensuring interactivity. The loop breaks when you type `exit`, allowing
  you to control the application flow effectively.
4. Create an instance of Summarizer.
  ```python
  bert_model = Summarizer()
  ```
  Here, you create an instance of the Summarizer class named `bert_model`. This
  instance is now ready to perform the summarization task using the BERT model,
  simplifying the complex processes of embedding sentences and clustering into
  an accessible interface.
5. Generate and print a summary.
  ```python
  summary = bert_model(input_text)
  print(summary)
  ```
  Your input text is processed by the bert_model instance, which then returns a
  summarized version. This demonstrates the power of Python's high-level
  libraries in enabling complex operations with minimal code.
6. Create `requirements.txt`. The sample application already contains the
  `requirements.txt` file to specify the necessary modules that the
  application imports. Open `requirements.txt` in a code or text editor to
  explore its contents.
  ```text
  ...
  # 04 text_summarization
  bert-extractive-summarizer==0.10.1
  ...
  torch==2.1.2
  ```
  The `bert-extractive-summarizer` and `torch` modules are required for the
  text summarization application. The summarizer module generates a summary of
  the input text. This requires PyTorch because the underlying BERT model,
  which is used for generating the summary, is implemented in PyTorch.

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
  lets the next command (`RUN pip install`) to install these dependencies
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
  This step is specific to NLP applications that require the spaCy library. It
  downloads the `en_core_web_sm` model, which is a small English language model
  for spaCy. While not needed for this app, it's included for compatibility
  with other NLP applications that might use this Dockerfile.
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
  $ docker run -it basic-nlp 04_text_summarization.py
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
  - `04_text_summarization.py`: This is the script you want to run inside the
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
  Enter the text for summarization (type 'exit' to end):
  ```
3. Test the application.
  Enter some text to get the text summarization.
  ```console
  Enter the text for summarization (type 'exit' to end): Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making. AI technologies can be classified into two main types: narrow or weak AI, which is designed for a particular task, and general or strong AI, which possesses the ability to understand, learn, and apply knowledge across various domains. One of the most popular approaches in AI is machine learning, where algorithms are trained on large datasets to recognize patterns and make predictions.
  Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making.
  ```

## Summary

In this guide, you learned how to build and run a text summarization
application. You learned how to build the application using Python with Bert
Extractive Summarizer, and then set up the environment and run the application
using Docker.

Related information:

- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer)
- [PyTorch](https://pytorch.org/)
- [Python documentation](https://docs.python.org/3/)

## Next steps

Explore more [natural language processing guides](https://docs.docker.com/guides/).

---

# HTTP routing with Traefik

> Use Traefik to easily route traffic between multiple containers or non-containerized workloads

# HTTP routing with Traefik

   Table of contents

---

## Introduction

During local development, it’s quite common to need to run multiple HTTP services. You might have both an API and a frontend app, a WireMock service to mock data endpoints, or a database visualizer (such as phpMyAdmin or pgAdmin). In many development setups, these services are exposed on different ports, which then requires you to remember what’s on what port but can also introduce other problems (such as CORS).

A reverse proxy can dramatically simplify this setup by being the single exposed service and then routing requests to the appropriate service based on the request URL (either by path or hostname). [Traefik](https://traefik.io/traefik/) is a modern, cloud-native reverse proxy and load balancer that makes developing and deploying multi-service applications easier. This guide will show you how to use Traefik with Docker to enhance your development environment.

In this guide, you will learn how to:

1. Start Traefik with Docker
2. Configure routing rules to split traffic between two containers
3. Use Traefik in a containerized development environment
4. Use Traefik to send requests to non-containerized workloads

## Prerequisites

The following prerequisites are required to follow along with this how-to guide:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js](https://nodejs.org/en/download/package-manager) and [yarn](https://yarnpkg.com/)
- Basic of Docker

## Using Traefik with Docker

One of the unique features of Traefik is its ability to be configured in many ways. When using the Docker provider, Traefik gets its configuration from other running containers using [labels](https://docs.docker.com/config/labels-custom-metadata/). Traefik will watch engine events (for container starts and stops), extract the labels, and update its configuration.

While there are [many Traefik-monitored labels](https://doc.traefik.io/traefik/routing/providers/docker/), the two most common will be:

- `traefik.http.routers.<service-name>.rule` - used to indicate the routing rule ([view all of the available rules here](https://doc.traefik.io/traefik/routing/routers/#rule))
- `traefik.http.services.<service-name>.loadbalancer.server.port` - indicates the port Traefik should forward the request to. Note that this container port does not need to be exposed on your host machine ([read about port detection here](https://doc.traefik.io/traefik/providers/docker/#port-detection))

Let’s do a quick demo of starting Traefik and then configuring two additional containers to be accessible using different hostnames.

1. In order for two containers to be able to communicate with each other, they need to be on the same network. Create a network named `traefik-demo` using the `docker network create` command:
  ```console
  $ docker network create traefik-demo
  ```
2. Start a Traefik container using the following command. The command exposes Traefik on port 80, mounts the Docker socket (which is used to monitor containers to update configuration), and passes the `--providers.docker` argument to configure Traefik to use the Docker provider.
  ```console
  $ docker run -d --network=traefik-demo -p 80:80 -v /var/run/docker.sock:/var/run/docker.sock traefik:v3.6.2 --providers.docker
  ```
3. Now, start a simple Nginx container and define the labels Traefik is watching for to configure the HTTP routing. Note that the Nginx container is not exposing any ports.
  ```console
  $ docker run -d --network=traefik-demo --label 'traefik.http.routers.nginx.rule=Host(`nginx.localhost`)' nginx
  ```
  Once the container starts, open your browser to [http://nginx.localhost](http://nginx.localhost) to see the app (all Chromium-based browsers route *.localhost requests locally with no additional setup).
4. Start a second application that will use a different hostname.
  ```console
  $ docker run -d --network=traefik-demo --label 'traefik.http.routers.welcome.rule=Host(`welcome.localhost`)' docker/welcome-to-docker
  ```
  Once the container starts, open your browser to [http://welcome.localhost](http://welcome.localhost). You should see a “Welcome to Docker” website.

## Using Traefik in development

Now that you’ve experienced Traefik, it’s time to try using it in a development environment. In this example, you will use a sample application that has a split frontend and backend. This app stack has the following configuration:

1. All requests to /api to go to the API service
2. All other requests to localhost go to the frontend client
3. Since the app uses MySQL, db.localhost should provide phpMyAdmin to make it easy to access the database during development

![Architecture diagram showing Traefik routing requests to other containers based on the path of the request](https://docs.docker.com/guides/images/traefik-in-development.webp)  ![Architecture diagram showing Traefik routing requests to other containers based on the path of the request](https://docs.docker.com/guides/images/traefik-in-development.webp)

The application can be accessed on GitHub at [dockersamples/easy-http-routing-with-traefik](https://github.com/dockersamples/easy-http-routing-with-traefik).

1. In the `compose.yaml` file, Traefik is using the following configuration:
  ```yaml
  services:
    proxy:
      image: traefik:v3.6.2
      command: --providers.docker
      ports:
        - 80:80
      volumes:
        - /var/run/docker.sock:/var/run/docker.sock
  ```
  Note that this is essentially the same configuration as used earlier, but now in a Compose syntax.
2. The client service has the following configuration, which will start the container and provide it with the labels to receive requests at localhost.
  ```yaml
  services:
    # …
    client:
      image: nginx:alpine
      volumes:
        - "./client:/usr/share/nginx/html"
      labels:
        traefik.http.routers.client.rule: "Host(`localhost`)"
  ```
3. The api service has a similar configuration, but you’ll notice the routing rule has two conditions - the host must be “localhost” and the URL path must have a prefix of “/api”. Since this rule is more specific, Traefik will evaluate it first compared to the client rule.
  ```yaml
  services:
    # …
    api:
      build: ./dev/api
      volumes:
        - "./api:/var/www/html/api"
      labels:
        traefik.http.routers.api.rule: "Host(`localhost`) && PathPrefix(`/api`)"
  ```
4. And finally, the `phpmyadmin` service is configured to receive requests for the hostname “db.localhost”. The service also has environment variables defined to automatically log in, making it a little easier to get into the app.
  ```yaml
  services:
    # …
    phpmyadmin:
      image: phpmyadmin:5.2.1
      labels:
        traefik.http.routers.db.rule: "Host(`db.localhost`)"
      environment:
        PMA_USER: root
        PMA_PASSWORD: password
  ```
5. Before starting the stack, stop the Nginx container if it is still running.

And that’s it. Now, you only need to spin up the Compose stack with a `docker compose up` and all of the services and applications will be ready for development.

## Sending traffic to non-containerized workloads

In some situations, you may want to forward requests to applications not running in containers. In the following architecture diagram, the same application from before is used, but the API and React apps are now running natively on the host machine.

![An architecture diagram showing several components and the routing between them. Traefik is able to send requests to both non-containerized and containerized workloads](https://docs.docker.com/guides/images/traefik-non-containerized-workload-architecture.webp)  ![An architecture diagram showing several components and the routing between them. Traefik is able to send requests to both non-containerized and containerized workloads](https://docs.docker.com/guides/images/traefik-non-containerized-workload-architecture.webp)

To accomplish this, Traefik will need to use another method to configure itself. The [File provider](https://doc.traefik.io/traefik/providers/file/) lets you define the routing rules in a YAML document. Here is an example file:

```yaml
http:
  routers:
    native-api:
      rule: "Host(`localhost`) && PathPrefix(`/api`)"
      service: native-api
    native-client:
      rule: "Host(`localhost`)"
      service: native-client

  services:
    native-api:
      loadBalancer:
        servers:
          - url: "http://host.docker.internal:3000/"
    native-client:
      loadBalancer:
        servers:
          - url: "http://host.docker.internal:5173/"
```

This configuration indicates that requests that for `localhost/api` will be forwarded to a service named `native-api`, which then forwards the request to [http://host.docker.internal:3000](http://host.docker.internal:3000). The hostname `host.docker.internal` is a name that Docker Desktop provides to send requests to the host machine.

With this file, the only change is to the Compose configuration for Traefik. There are specifically two things that have changed:

1. The configuration file is mounted into the Traefik container (the exact destination path is up to you)
2. The `command` is updated to add the file provider and point to the location of the configuration file

```yaml
services:
  proxy:
    image: traefik:v3.6.2
    command: --providers.docker --providers.file.filename=/config/traefik-config.yaml --api.insecure
    ports:
      - 80:80
      - 8080:8080
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./dev/traefik-config.yaml:/config/traefik-config.yaml
```

### Starting the example app

To run the example app that forwards requests from Traefik to native-running apps, use the following steps:

1. If you have the Compose stack still running, stop it with the following command:
  ```console
  $ docker compose down
  ```
2. Start the application using the provided `compose-native.yaml` file:
  ```console
  $ docker compose -f compose-native.yaml up
  ```
  Opening [http://localhost](http://localhost) will return a 502 Bad Gateway because the other apps aren’t running yet.
3. Start the API by running the following steps:
  ```console
  cd api
  yarn install
  yarn dev
  ```
4. Start the frontend by running the following steps in a new terminal (starting from the root of the project):
  ```console
  cd client
  yarn install
  yarn dev
  ```
5. Open the app at [http://localhost](http://localhost). You should see an app that fetches a message from [http://localhost/api/messages](http://localhost/api/messages). You can also open [http://db.localhost](http://db.localhost) to view or adjust the available messages directly from the Mongo database. Traefik will ensure the requests are properly routed to the correct container or application.
6. When you’re done, run `docker compose down` to stop the containers and stop the Yarn apps by hitting `ctrl+c`.

## Recap

Running multiple services doesn’t have to require tricky port configuration and a good memory. With tools like Traefik, it’s easy to launch the services you need and easily access them - whether they’re for the app itself (such as the frontend and backend) or for additional development tooling (such as phpMyAdmin).
