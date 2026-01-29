# Use containers for Java development and more

# Use containers for Java development

> Learn how to develop your application locally.

# Use containers for Java development

   Table of contents

---

## Prerequisites

Work through the steps to containerize your application in [Containerize your app](https://docs.docker.com/guides/java/containerize/).

## Overview

In this section, you’ll walk through setting up a local development environment
for the application you containerized in the previous section. This includes:

- Adding a local database and persisting data
- Creating a development container to connect a debugger
- Configuring Compose to automatically update your running Compose services as
  you edit and save your code

## Add a local database and persist data

You can use containers to set up local services, like a database. In this section, you'll update the `docker-compose.yaml` file to define a database service and a volume to persist data. Also, this particular application uses a system property to define the database type, so you'll need to update the `Dockerfile` to pass in the system property when starting the app.

In the cloned repository's directory, open the `docker-compose.yaml` file in an IDE or text editor. Your Compose file has an example database service, but it'll require a few changes for your unique app.

In the `docker-compose.yaml` file, you need to do the following:

- Uncomment all of the database instructions. You'll now use a database service
  instead of local storage for the data.
- Remove the top-level `secrets` element as well as the element inside the `db`
  service. This example uses the environment variable for the password rather than secrets.
- Remove the `user` element from the `db` service. This example specifies the
  user in the environment variable.
- Update the database environment variables. These are defined by the Postgres
  image. For more details, see the
  [Postgres Official Docker Image](https://hub.docker.com/_/postgres).
- Update the healthcheck test for the `db` service and specify the user. By
  default, the healthcheck uses the root user instead of the `petclinic` user
  you defined.
- Add the database URL as an environment variable in the `server` service. This
  overrides the default value defined in
  `spring-petclinic/src/main/resources/application-postgres.properties`.

The following is the updated `docker-compose.yaml` file. All comments have been removed.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

Open the `Dockerfile` in an IDE or text editor. In the `ENTRYPOINT` instruction,
update the instruction to pass in the system property as specified in the
`spring-petclinic/src/resources/db/postgres/petclinic_db_setup_postgres.txt`
file.

```diff
- ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
+ ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

Save and close all the files.

Now, run the following `docker compose up` command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at [http://localhost:8080](http://localhost:8080). You should see a simple app for a pet clinic. Browse around the application. Navigate to **Veterinarians** and verify that the application is connected to the database by being able to list veterinarians.

In the terminal, press `ctrl`+`c` to stop the application.

## Dockerfile for development

The Dockerfile you have now is great for a small, secure production image with
only the components necessary to run the application. When developing, you may
want a different image that has a different environment.

For example, in the development image you may want to set up the image to start
the application so that you can connect a debugger to the running Java process.

Rather than managing multiple Dockerfiles, you can add a new stage. Your
Dockerfile can then produce a final image which is ready for production as well
as a development image.

Replace the contents of your Dockerfile with the following.

```dockerfile
# syntax=docker/dockerfile:1

FROM eclipse-temurin:21-jdk-jammy as deps
WORKDIR /build
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

FROM deps as package
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

FROM package as extract
WORKDIR /build
RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

FROM extract as development
WORKDIR /build
RUN cp -r /build/target/extracted/dependencies/. ./
RUN cp -r /build/target/extracted/spring-boot-loader/. ./
RUN cp -r /build/target/extracted/snapshot-dependencies/. ./
RUN cp -r /build/target/extracted/application/. ./
ENV JAVA_TOOL_OPTIONS -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000
CMD [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]

FROM eclipse-temurin:21-jre-jammy AS final
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./
EXPOSE 8080
ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

Save and close the `Dockerfile`.

In the `Dockerfile` you added a new stage labeled `development` based on the `extract` stage. In this stage, you copy the extracted files to a common directory, then run a command to start the application. In the command, you expose port 8000 and declare the debug configuration for the JVM so that you can attach a debugger.

## Use Compose to develop locally

The current Compose file doesn't start your development container. To do that, you must update your Compose file to target the development stage. Also, update the port mapping of the server service to provide access for the debugger.

Open the `docker-compose.yaml` and add the following instructions into the file.

```yaml
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

Now, start your application and to confirm that it's running.

```console
$ docker compose up --build
```

Finally, test your API endpoint. Run the following curl command:

```console
$ curl  --request GET \
  --url http://localhost:8080/vets \
  --header 'content-type: application/json'
```

You should receive the following response:

```json
{
  "vetList": [
    {
      "id": 1,
      "firstName": "James",
      "lastName": "Carter",
      "specialties": [],
      "nrOfSpecialties": 0,
      "new": false
    },
    {
      "id": 2,
      "firstName": "Helen",
      "lastName": "Leary",
      "specialties": [{ "id": 1, "name": "radiology", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 3,
      "firstName": "Linda",
      "lastName": "Douglas",
      "specialties": [
        { "id": 3, "name": "dentistry", "new": false },
        { "id": 2, "name": "surgery", "new": false }
      ],
      "nrOfSpecialties": 2,
      "new": false
    },
    {
      "id": 4,
      "firstName": "Rafael",
      "lastName": "Ortega",
      "specialties": [{ "id": 2, "name": "surgery", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 5,
      "firstName": "Henry",
      "lastName": "Stevens",
      "specialties": [{ "id": 1, "name": "radiology", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 6,
      "firstName": "Sharon",
      "lastName": "Jenkins",
      "specialties": [],
      "nrOfSpecialties": 0,
      "new": false
    }
  ]
}
```

## Connect a Debugger

You’ll use the debugger that comes with the IntelliJ IDEA. You can use the community version of this IDE. Open your project in IntelliJ IDEA, go to the **Run** menu, and then **Edit Configuration**. Add a new Remote JVM Debug configuration similar to the following:

![Java Connect a Debugger](https://docs.docker.com/guides/java/images/connect-debugger.webp)  ![Java Connect a Debugger](https://docs.docker.com/guides/java/images/connect-debugger.webp)

Set a breakpoint.

Open `src/main/java/org/springframework/samples/petclinic/vet/VetController.java` and add a breakpoint inside the `showResourcesVetList` function.

To start your debug session, select the **Run** menu and then **DebugNameOfYourConfiguration**.

![Debug menu](https://docs.docker.com/guides/java/images/debug-menu.webp)  ![Debug menu](https://docs.docker.com/guides/java/images/debug-menu.webp)

You should now see the connection in the logs of your Compose application.

![Compose log file ](https://docs.docker.com/guides/java/images/compose-logs.webp)  ![Compose log file ](https://docs.docker.com/guides/java/images/compose-logs.webp)

You can now call the server endpoint.

```console
$ curl --request GET --url http://localhost:8080/vets
```

You should have seen the code break on the marked line and now you are able to use the debugger just like you would normally. You can also inspect and watch variables, set conditional breakpoints, view stack traces and a do bunch of other stuff.

![Debugger code breakpoint](https://docs.docker.com/guides/java/images/debugger-breakpoint.webp)  ![Debugger code breakpoint](https://docs.docker.com/guides/java/images/debugger-breakpoint.webp)

Press `ctrl+c` in the terminal to stop your application.

## Automatically update services

Use Compose Watch to automatically update your running Compose services as you
edit and save your code. For more details about Compose Watch, see
[Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `docker-compose.yaml` file in an IDE or text editor and then add the
Compose Watch instructions. The following is the updated `docker-compose.yaml`
file.

```yaml
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Open a web browser and view the application at [http://localhost:8080](http://localhost:8080). You should see the Spring Pet Clinic home page.

Any changes to the application's source files on your local machine will now be automatically reflected in the running container.

Open `spring-petclinic/src/main/resources/templates/fragments/layout.html` in an IDE or text editor and update the `Home` navigation string by adding an exclamation mark.

```diff
-   <li th:replace="~{::menuItem ('/','home','home page','home','Home')}">
+   <li th:replace="~{::menuItem ('/','home','home page','home','Home!')}">
```

Save the changes to `layout.html` and then you can continue developing while the container automatically rebuilds.

After the container is rebuilt and running, refresh [http://localhost:8080](http://localhost:8080) and then verify that **Home!** now appears in the menu.

Press `ctrl+c` in the terminal to stop Compose Watch.

## Summary

In this section, you took a look at running a database locally and persisting the data. You also created a development image that contains the JDK and lets you attach a debugger. Finally, you set up your Compose file to expose the debugging port and configured Compose Watch to live reload your changes.

Related information:

- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)

## Next steps

In the next section, you’ll take a look at how to run unit tests in Docker.

---

# Run your Java tests

> How to build and run your Java tests

# Run your Java tests

   Table of contents

---

## Prerequisites

Complete all the previous sections of this guide, starting with [Containerize a Java application](https://docs.docker.com/guides/java/containerize/).

## Overview

Testing is an essential part of modern software development. Testing can mean a lot of things to different development teams. There are unit tests, integration tests and end-to-end testing. In this guide you'll take a look at running your unit tests in Docker.

### Multi-stage Dockerfile for testing

In the following example, you'll pull the testing commands into your Dockerfile.
Replace the contents of your Dockerfile with the following.

```dockerfile
# syntax=docker/dockerfile:1

FROM eclipse-temurin:21-jdk-jammy as base
WORKDIR /build
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/

FROM base as test
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw test

FROM base as deps
WORKDIR /build
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw dependency:go-offline -DskipTests

FROM deps as package
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

FROM package as extract
WORKDIR /build
RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

FROM extract as development
WORKDIR /build
RUN cp -r /build/target/extracted/dependencies/. ./
RUN cp -r /build/target/extracted/spring-boot-loader/. ./
RUN cp -r /build/target/extracted/snapshot-dependencies/. ./
RUN cp -r /build/target/extracted/application/. ./
ENV JAVA_TOOL_OPTIONS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000"
CMD [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]

FROM eclipse-temurin:21-jre-jammy AS final
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./
EXPOSE 8080
ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

First, you added a new base stage. In the base stage, you added common instructions that both the test and deps stage will need.

Next, you added a new test stage labeled `test` based on the base stage. In this
stage you copied in the necessary source files and then specified `RUN` to run
`./mvnw test`. Instead of using `CMD`, you used `RUN` to run the tests. The
reason is that the `CMD` instruction runs when the container runs, and the `RUN`
instruction runs when the image is being built. When using `RUN`, the build will
fail if the tests fail.

Finally, you updated the deps stage to be based on the base stage and removed
the instructions that are now in the base stage.

Run the following command to build a new image using the test stage as the target and view the test results. Include `--progress=plain` to view the build output, `--no-cache` to ensure the tests always run, and `--target test` to target the test stage.

Now, build your image and run your tests. You'll run the `docker build` command and add the `--target test` flag so that you specifically run the test build stage.

```console
$ docker build -t java-docker-image-test --progress=plain --no-cache --target=test .
```

You should see output containing the following

```console
...

#15 101.3 [WARNING] Tests run: 45, Failures: 0, Errors: 0, Skipped: 2
#15 101.3 [INFO]
#15 101.3 [INFO] ------------------------------------------------------------------------
#15 101.3 [INFO] BUILD SUCCESS
#15 101.3 [INFO] ------------------------------------------------------------------------
#15 101.3 [INFO] Total time:  01:39 min
#15 101.3 [INFO] Finished at: 2024-02-01T23:24:48Z
#15 101.3 [INFO] ------------------------------------------------------------------------
#15 DONE 101.4s
```

## Next steps

In the next section, you’ll take a look at how to set up a CI/CD pipeline using
GitHub Actions.

---

# Java language

> Containerize Java apps using Docker

# Java language-specific guide

---

The Java getting started guide teaches you how to create a containerized Spring Boot application using Docker. In this module, you’ll learn how to:

- Containerize and run a Spring Boot application with Maven
- Set up a local development environment to connect a database to the container, configure a debugger, and use Compose Watch for live reload
- Run your unit tests inside a container
- Configure a CI/CD pipeline for your application using GitHub Actions
- Deploy your containerized application locally to Kubernetes to test and debug your deployment

After completing the Java getting started modules, you should be able to containerize your own Java application based on the examples and instructions provided in this guide.

Get started containerizing your first Java app.

## Modules

1. [Containerize your app](https://docs.docker.com/guides/java/containerize/)
  Learn how to containerize a Java application.
2. [Develop your app](https://docs.docker.com/guides/java/develop/)
  Learn how to develop your application locally.
3. [Run your tests](https://docs.docker.com/guides/java/run-tests/)
  How to build and run your Java tests
4. [Configure CI/CD](https://docs.docker.com/guides/java/configure-ci-cd/)
  Learn how to Configure CI/CD for your Java application
5. [Test your deployment](https://docs.docker.com/guides/java/deploy/)
  Learn how to develop locally using Kubernetes

---

# Data science with JupyterLab

> Run, develop, and share data science projects using JupyterLab and Docker

# Data science with JupyterLab

   Table of contents

---

Docker and JupyterLab are two powerful tools that can enhance your data science
workflow. In this guide, you will learn how to use them together to create and
run reproducible data science environments. This guide is based on
[Supercharging AI/ML Development with JupyterLab and
Docker](https://www.docker.com/blog/supercharging-ai-ml-development-with-jupyterlab-and-docker/).

In this guide, you'll learn how to:

- Run a personal Jupyter Server with JupyterLab on your local machine
- Customize your JupyterLab environment
- Share your JupyterLab notebook and environment with other data scientists

## What is JupyterLab?

[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) is an open source application built around the concept of a computational notebook document. It enables sharing and executing code, data processing, visualization, and offers a range of interactive features for creating graphs.

## Why use Docker and JupyterLab together?

By combining Docker and JupyterLab, you can benefit from the advantages of both tools, such as:

- Containerization ensures a consistent JupyterLab environment across all
  deployments, eliminating compatibility issues.
- Containerized JupyterLab simplifies sharing and collaboration by removing the
  need for manual environment setup.
- Containers offer scalability for JupyterLab, supporting workload distribution
  and efficient resource management with platforms like Kubernetes.

## Prerequisites

To follow along with this guide, you must install the latest version of
[Docker Desktop](https://docs.docker.com/get-started/get-docker/).

## Run and access a JupyterLab container

In a terminal, run the following command to run your JupyterLab container.

```console
$ docker run --rm -p 8889:8888 quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

The following are the notable parts of the command:

- `-p 8889:8888`: Maps port 8889 from the host to port 8888 on the container.
- `start-notebook.py --NotebookApp.token='my-token'`: Sets an access token
  rather than using a random token.

For more details, see the [Jupyter Server Options](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#jupyter-server-options) and the
[docker run CLI reference](https://docs.docker.com/reference/cli/docker/container/run/).

If this is the first time you are running the image, Docker will download and
run it. The amount of time it takes to download the image will vary depending on
your network connection.

After the image downloads and runs, you can access the container. To access the
container, in a web browser navigate to
[localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token).

To stop the container, in the terminal press `ctrl`+`c`.

To access an existing notebook on your system, you can use a
[bind mount](https://docs.docker.com/storage/bind-mounts/). Open a terminal and
change directory to where your existing notebook is. Then,
run the following command based on your operating system.

```console
$ docker run --rm -p 8889:8888 -v "$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

```console
$ docker run --rm -p 8889:8888 -v "%cd%":/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

```console
$ docker run --rm -p 8889:8888 -v "$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

```console
$ docker run --rm -p 8889:8888 -v "/$(pwd):/home/jovyan/work" quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

The `-v` option tells Docker to mount your current working directory to
`/home/jovyan/work` inside the container. By default, the Jupyter image's root
directory is `/home/jovyan` and you can only access or save notebooks to that
directory in the container.

Now you can access [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token) and open notebooks contained in the bind mounted directory.

To stop the container, in the terminal press `ctrl`+`c`.

Docker also has volumes, which are the preferred mechanism for persisting
data generated by and used by Docker containers. While bind mounts are dependent
on the directory structure and OS of the host machine, volumes are completely
managed by Docker.

## Save and access notebooks

When you remove a container, all data in that container is deleted. To save
notebooks outside of the container, you can use a
[volume](https://docs.docker.com/engine/storage/volumes/).

### Run a JupyterLab container with a volume

To start the container with a volume, open a terminal and run the following command

```console
$ docker run --rm -p 8889:8888 -v jupyter-data:/home/jovyan/work quay.io/jupyter/base-notebook start-notebook.py --NotebookApp.token='my-token'
```

The `-v` option tells Docker to create a volume named `jupyter-data` and mount it in the container at `/home/jovyan/work`.

To access the container, in a web browser navigate to
[localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token).
Notebooks can now be saved to the volume and will accessible even when
the container is deleted.

### Save a notebook to the volume

For this example, you'll use the [Iris Dataset](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html) example from scikit-learn.

1. Open a web browser and access your JupyterLab container at [localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token).
2. In the **Launcher**, under **Notebook**, select **Python 3**.
3. In the notebook, specify the following to install the necessary packages.
  ```console
  !pip install matplotlib scikit-learn
  ```
4. Select the play button to run the code.
5. In the notebook, specify the following code.
  ```python
  from sklearn import datasets
  iris = datasets.load_iris()
  import matplotlib.pyplot as plt
  _, ax = plt.subplots()
  scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
  ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
  _ = ax.legend(
     scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
  )
  ```
6. Select the play button to run the code. You should see a scatter plot of the
  Iris dataset.
7. In the top menu, select **File** and then **Save Notebook**.
8. Specify a name in the `work` directory to save the notebook to the volume.
  For example, `work/mynotebook.ipynb`.
9. Select **Rename** to save the notebook.

The notebook is now saved in the volume.

In the terminal, press `ctrl`+ `c` to stop the container.

Now, any time you run a Jupyter container with the volume, you'll have access to the saved notebook.

When you do run a new container, and then run the data plot code again, it'll
need to run `!pip install matplotlib scikit-learn` and download the packages.
You can avoid reinstalling packages every time you run a new container by
creating your own image with the packages already installed.

## Customize your JupyterLab environment

You can create your own JupyterLab environment and build it into an image using
Docker. By building your own image, you can customize your JupyterLab
environment with the packages and tools you need, and ensure that it's
consistent and reproducible across different deployments. Building your own
image also makes it easier to share your JupyterLab environment with others, or
to use it as a base for further development.

### Define your environment in a Dockerfile

In the previous Iris Dataset example from [Save a notebook to the volume](#save-a-notebook-to-the-volume), you had to install the dependencies, `matplotlib` and `scikit-learn`, every time you ran a new container. While the dependencies in that small example download and
install quickly, it may become a problem as your list of dependencies grow.
There may also be other tools, packages, or files that you always want in your
environment.

In this case, you can install the dependencies as part of the environment in the
image. Then, every time you run your container, the dependencies will always be
installed.

You can define your environment in a Dockerfile. A Dockerfile is a text file
that instructs Docker how to create an image of your JupyterLab environment. An
image contains everything you want and need when running JupyterLab, such as
files, packages, and tools.

In a directory of your choice, create a new text file named `Dockerfile`. Open the `Dockerfile` in an IDE or text editor and then add the following contents.

```dockerfile
# syntax=docker/dockerfile:1

FROM quay.io/jupyter/base-notebook
RUN pip install --no-cache-dir matplotlib scikit-learn
```

This Dockerfile uses the `quay.io/jupyter/base-notebook` image as the base, and then runs `pip` to install the dependencies. For more details about the instructions in the Dockerfile, see the
[Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

Before you proceed, save your changes to the `Dockerfile`.

### Build your environment into an image

After you have a `Dockerfile` to define your environment, you can use `docker build` to build an image using your `Dockerfile`.

Open a terminal, change directory to the directory where your `Dockerfile` is
located, and then run the following command.

```console
$ docker build -t my-jupyter-image .
```

The command builds a Docker image from your `Dockerfile` and a context. The
`-t` option specifies the name and tag of the image, in this case
`my-jupyter-image`. The `.` indicates that the current directory is the context,
which means that the files in that directory can be used in the image creation
process.

You can verify that the image was built by viewing the `Images` view in Docker Desktop, or by running the `docker image ls` command in a terminal. You should see an image named `my-jupyter-image`.

## Run your image as a container

To run your image as a container, you use the `docker run` command. In the
`docker run` command, you'll specify your own image name.

```console
$ docker run --rm -p 8889:8888 my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

To access the container, in a web browser navigate to
[localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token).

You can now use the packages without having to install them in your notebook.

1. In the **Launcher**, under **Notebook**, select **Python 3**.
2. In the notebook, specify the following code.
  ```python
  from sklearn import datasets
  iris = datasets.load_iris()
  import matplotlib.pyplot as plt
  _, ax = plt.subplots()
  scatter = ax.scatter(iris.data[:, 0], iris.data[:, 1], c=iris.target)
  ax.set(xlabel=iris.feature_names[0], ylabel=iris.feature_names[1])
  _ = ax.legend(
     scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
  )
  ```
3. Select the play button to run the code. You should see a scatter plot of the Iris dataset.

In the terminal, press `ctrl`+ `c` to stop the container.

## Use Compose to run your container

Docker Compose is a tool for defining and running multi-container applications.
In this case, the application isn't a multi-container application, but Docker
Compose can make it easier to run by defining all the `docker run` options in a
file.

### Create a Compose file

To use Compose, you need a `compose.yaml` file. In the same directory as your
`Dockerfile`, create a new file named `compose.yaml`.

Open the `compose.yaml` file in an IDE or text editor and add the following
contents.

```yaml
services:
  jupyter:
    build:
      context: .
    ports:
      - 8889:8888
    volumes:
      - jupyter-data:/home/jovyan/work
    command: start-notebook.py --NotebookApp.token='my-token'

volumes:
  jupyter-data:
    name: jupyter-data
```

This Compose file specifies all the options you used in the `docker run` command. For more details about the Compose instructions, see the
[Compose file reference](https://docs.docker.com/reference/compose-file/).

Before you proceed, save your changes to the `compose.yaml` file.

### Run your container using Compose

Open a terminal, change directory to where your `compose.yaml` file is located, and then run the following command.

```console
$ docker compose up --build
```

This command builds your image and runs it as a container using the instructions
specified in the `compose.yaml` file. The `--build` option ensures that your
image is rebuilt, which is necessary if you made changes to your `Dockerfile`.

To access the container, in a web browser navigate to
[localhost:8889/lab?token=my-token](http://localhost:8889/lab?token=my-token).

In the terminal, press `ctrl`+ `c` to stop the container.

## Share your work

By sharing your image and notebook, you create a portable and replicable
research environment that can be easily accessed and used by other data
scientists. This process not only facilitates collaboration but also ensures
that your work is preserved in an environment where it can be run without
compatibility issues.

To share your image and data, you'll use [Docker Hub](https://hub.docker.com/). Docker Hub is a cloud-based registry service that lets you share and distribute container images.

### Share your image

1. [Sign up](https://www.docker.com/pricing?utm_source=docker&utm_medium=webreferral&utm_campaign=docs_driven_upgrade) or sign in to [Docker Hub](https://hub.docker.com).
2. Rename your image so that Docker knows which repository to push it to. Open a
  terminal and run the following `docker tag` command. Replace `YOUR-USER-NAME`
  with your Docker ID.
  ```console
  $ docker tag my-jupyter-image YOUR-USER-NAME/my-jupyter-image
  ```
3. Run the following `docker push` command to push the image to Docker Hub.
  Replace `YOUR-USER-NAME` with your Docker ID.
  ```console
  $ docker push YOUR-USER-NAME/my-jupyter-image
  ```
4. Verify that you pushed the image to Docker Hub.
  1. Go to [Docker Hub](https://hub.docker.com).
  2. Select **My Hub** > **Repositories**.
  3. View the **Last pushed** time for your repository.

Other users can now download and run your image using the `docker run` command. They need to replace `YOUR-USER-NAME` with your Docker ID.

```console
$ docker run --rm -p 8889:8888 YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

### Share your volume

This example uses the Docker Desktop graphical user interface. Alternatively, in the command line interface you can
[back up the volume](https://docs.docker.com/engine/storage/volumes/#back-up-a-volume) and then
[push it using the ORAS CLI](https://docs.docker.com/docker-hub/repos/manage/hub-images/oci-artifacts/#push-a-volume).

1. Sign in to Docker Desktop.
2. In the Docker Dashboard, select **Volumes**.
3. Select the **jupyter-data** volume by selecting the name.
4. Select the **Exports** tab.
5. Select **Quick export**.
6. For **Location**, select **Registry**.
7. In the text box under **Registry**, specify your Docker ID, a name for the
  volume, and a tag. For example, `YOUR-USERNAME/jupyter-data:latest`.
8. Select **Save**.
9. Verify that you exported the volume to Docker Hub.
  1. Go to [Docker Hub](https://hub.docker.com).
  2. Select **My Hub** > **Repositories**.
  3. View the **Last pushed** time for your repository.

Other users can now download and import your volume. To import the volume and then run it with your image:

1. Sign in to Docker Desktop.
2. In the Docker Dashboard, select **Volumes**.
3. Select **Create** to create a new volume.
4. Specify a name for the new volume. For this example, use `jupyter-data-2`.
5. Select **Create**.
6. In the list of volumes, select the **jupyter-data-2** volume by selecting the
  name.
7. Select **Import**.
8. For **Location**, select **Registry**.
9. In the text box under **Registry**, specify the same name as the repository
  that you exported your volume to. For example,
  `YOUR-USERNAME/jupyter-data:latest`.
10. Select **Import**.
11. In a terminal, run `docker run` to run your image with the imported volume.
  Replace `YOUR-USER-NAME` with your Docker ID.

```console
$ docker run --rm -p 8889:8888 -v jupyter-data-2:/home/jovyan/work YOUR-USER-NAME/my-jupyter-image start-notebook.py --NotebookApp.token='my-token'
```

## Summary

In this guide, you learned how to leverage Docker and JupyterLab to create
reproducible data science environments, facilitating the development and sharing
of data science projects. This included, running a personal JupyterLab server,
customizing the environment with necessary tools and packages, and sharing
notebooks and environments with other data scientists.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Jupyter Docker Stacks docs](https://jupyter-docker-stacks.readthedocs.io/en/latest/)
