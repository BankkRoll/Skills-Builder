# Build, tag, and publish an image and more

# Build, tag, and publish an image

> This concept page will teach you how to build, tag, and publish an image to Docker Hub or any other registry

# Build, tag, and publish an image

   Table of contents

---

## Explanation

In this guide, you will learn the following:

- Building images - the process of building an image based on a `Dockerfile`
- Tagging images - the process of giving an image a name, which also determines where the image can be distributed
- Publishing images - the process to distribute or share the newly created image using a container registry

### Building images

Most often, images are built using a Dockerfile. The most basic `docker build` command might look like the following:

```bash
docker build .
```

The final `.` in the command provides the path or URL to the [build context](https://docs.docker.com/build/concepts/context/#what-is-a-build-context). At this location, the builder will find the `Dockerfile` and other referenced files.

When you run a build, the builder pulls the base image, if needed, and then runs the instructions specified in the Dockerfile.

With the previous command, the image will have no name, but the output will provide the ID of the image. As an example, the previous command might produce the following output:

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED                                              docker:desktop-linux
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 308B                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.12                                  0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [1/6] FROM docker.io/library/python:3.12                                                    0.0s
 => [internal] load build context                                                               0.0s
 => => transferring context: 123B                                                               0.0s
 => [2/6] WORKDIR /usr/local/app                                                                0.0s
 => [3/6] RUN useradd app                                                                       0.1s
 => [4/6] COPY ./requirements.txt ./requirements.txt                                            0.0s
 => [5/6] RUN pip install --no-cache-dir --upgrade -r requirements.txt                          3.2s
 => [6/6] COPY ./app ./app                                                                      0.0s
 => exporting to image                                                                          0.1s
 => => exporting layers                                                                         0.1s
 => => writing image sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00    0.0s
```

With the previous output, you could start a container by using the referenced image:

```console
docker run sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00
```

That name certainly isn't memorable, which is where tagging becomes useful.

### Tagging images

Tagging images is the method to provide an image with a memorable name. However, there is a structure to the name of an image. A full image name has the following structure:

```text
[HOST[:PORT_NUMBER]/]PATH[:TAG]
```

- `HOST`: The optional registry hostname where the image is located. If no host is specified, Docker's public registry at `docker.io` is used by default.
- `PORT_NUMBER`: The registry port number if a hostname is provided
- `PATH`: The path of the image, consisting of slash-separated components. For Docker Hub, the format follows `[NAMESPACE/]REPOSITORY`, where namespace is either a user's or organization's name. If no namespace is specified, `library` is used, which is the namespace for Docker Official Images.
- `TAG`: A custom, human-readable identifier that's typically used to identify different versions or variants of an image. If no tag is specified, `latest` is used by default.

Some examples of image names include:

- `nginx`, equivalent to `docker.io/library/nginx:latest`: this pulls an image from the `docker.io` registry, the `library` namespace, the `nginx` image repository, and the `latest` tag.
- `docker/welcome-to-docker`, equivalent to `docker.io/docker/welcome-to-docker:latest`: this pulls an image from the `docker.io` registry, the `docker` namespace, the `welcome-to-docker` image repository, and the `latest` tag
- `ghcr.io/dockersamples/example-voting-app-vote:pr-311`: this pulls an image from the GitHub Container Registry, the `dockersamples` namespace, the `example-voting-app-vote` image repository, and the `pr-311` tag

To tag an image during a build, add the `-t` or `--tag` flag:

```console
docker build -t my-username/my-image .
```

If you've already built an image, you can add another tag to the image by using the [docker image tag](https://docs.docker.com/engine/reference/commandline/image_tag/) command:

```console
docker image tag my-username/my-image another-username/another-image:v1
```

### Publishing images

Once you have an image built and tagged, you're ready to push it to a registry. To do so, use the [docker push](https://docs.docker.com/engine/reference/commandline/image_push/) command:

```console
docker push my-username/my-image
```

Within a few seconds, all of the layers for your image will be pushed to the registry.

> **Requiring authentication**
>
>
>
> Before you're able to push an image to a repository, you will need to be authenticated.
> To do so, simply use the [docker login](https://docs.docker.com/engine/reference/commandline/login/) command.

## Try it out

In this hands-on guide, you will build a simple image using a provided Dockerfile and push it to Docker Hub.

### Set up

1. Get the sample application.
  If you have Git, you can clone the repository for the sample application. Otherwise, you can download the sample application. Choose one of the following options.
  Use the following command in a terminal to clone the sample application repository.
  ```console
  $ git clone https://github.com/docker/getting-started-todo-app
  ```
  Download the source and extract it.
  [Download the source](https://github.com/docker/getting-started-todo-app/raw/cd61f824da7a614a8298db503eed6630eeee33a3/app.zip)
2. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.
3. If you don't have a Docker account yet, [create one now](https://hub.docker.com/). Once you've done that, sign in to Docker Desktop using that account.

### Build an image

Now that you have a repository on Docker Hub, it's time for you to build an image and push it to the repository.

1. Using a terminal in the root of the sample app repository, run the following command. Replace `YOUR_DOCKER_USERNAME` with your Docker Hub username:
  ```console
  $ docker build -t YOUR_DOCKER_USERNAME/concepts-build-image-demo .
  ```
  As an example, if your username is `mobywhale`, you would run the command:
  ```console
  $ docker build -t mobywhale/concepts-build-image-demo .
  ```
2. Once the build has completed, you can view the image by using the following command:
  ```console
  $ docker image ls
  ```
  The command will produce output similar to the following:
  ```plaintext
  REPOSITORY                             TAG       IMAGE ID       CREATED          SIZE
  mobywhale/concepts-build-image-demo    latest    746c7e06537f   24 seconds ago   354MB
  ```
3. You can actually view the history (or how the image was created) by using the
  [docker image history](https://docs.docker.com/reference/cli/docker/image/history/) command:
  ```console
  $ docker image history mobywhale/concepts-build-image-demo
  ```
  You'll then see output similar to the following:
  ```plaintext
  IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
  f279389d5f01   8 seconds ago   CMD ["node" "./src/index.js"]                   0B        buildkit.dockerfile.v0
  <missing>      8 seconds ago   EXPOSE map[3000/tcp:{}]                         0B        buildkit.dockerfile.v0
  <missing>      8 seconds ago   WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
  <missing>      4 days ago      /bin/sh -c #(nop)  CMD ["node"]                 0B
  <missing>      4 days ago      /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B
  <missing>      4 days ago      /bin/sh -c #(nop) COPY file:4d192565a7220e13…   20.5kB
  <missing>      4 days ago      /bin/sh -c apk add --no-cache --virtual .bui…   7.92MB
  <missing>      4 days ago      /bin/sh -c #(nop)  ENV YARN_VERSION=1.22.19     0B
  <missing>      4 days ago      /bin/sh -c addgroup -g 1000 node     && addu…   126MB
  <missing>      4 days ago      /bin/sh -c #(nop)  ENV NODE_VERSION=20.12.0     0B
  <missing>      2 months ago    /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
  <missing>      2 months ago    /bin/sh -c #(nop) ADD file:d0764a717d1e9d0af…   8.42MB
  ```
  This output shows the layers of the image, highlighting the layers you added and those that were inherited from your base image.

### Push the image

Now that you have an image built, it's time to push the image to a registry.

1. Push the image using the
  [docker push](https://docs.docker.com/reference/cli/docker/image/push/) command:
  ```console
  $ docker push YOUR_DOCKER_USERNAME/concepts-build-image-demo
  ```
  If you receive a `requested access to the resource is denied`, make sure you are both logged in and that your Docker username is correct in the image tag.
  After a moment, your image should be pushed to Docker Hub.

## Additional resources

To learn more about building, tagging, and publishing images, visit the following resources:

- [What is a build context?](https://docs.docker.com/build/concepts/context/#what-is-a-build-context)
- [docker build reference](https://docs.docker.com/engine/reference/commandline/image_build/)
- [docker image tag reference](https://docs.docker.com/engine/reference/commandline/image_tag/)
- [docker push reference](https://docs.docker.com/engine/reference/commandline/image_push/)
- [What is a registry?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/)

## Next steps

Now that you have learned about building and publishing images, it's time to learn how to speed up the build process using the Docker build cache.

[Using the build cache](https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/)

---

# Multi

> This concept page will teach you about the purpose of the multi-stage build and its benefits

# Multi-stage builds

   Table of contents

---

## Explanation

In a traditional build, all build instructions are executed in sequence, and in a single build container: downloading dependencies, compiling code, and packaging the application. All those layers end up in your final image. This approach works, but it leads to bulky images carrying unnecessary weight and increasing your security risks. This is where multi-stage builds come in.

Multi-stage builds introduce multiple stages in your Dockerfile, each with a specific purpose. Think of it like the ability to run different parts of a build in multiple different environments, concurrently. By separating the build environment from the final runtime environment, you can significantly reduce the image size and attack surface. This is especially beneficial for applications with large build dependencies.

Multi-stage builds are recommended for all types of applications.

- For interpreted languages, like JavaScript or Ruby or Python, you can build and minify your code in one stage, and copy the production-ready files to a smaller runtime image. This optimizes your image for deployment.
- For compiled languages, like C or Go or Rust, multi-stage builds let you compile in one stage and copy the compiled binaries into a final runtime image. No need to bundle the entire compiler in your final image.

Here's a simplified example of a multi-stage build structure using pseudo-code. Notice there are multiple `FROM` statements and a new `AS <stage-name>`. In addition, the `COPY` statement in the second stage is copying `--from` the previous stage.

```dockerfile
# Stage 1: Build Environment
FROM builder-image AS build-stage
# Install build tools (e.g., Maven, Gradle)
# Copy source code
# Build commands (e.g., compile, package)

# Stage 2: Runtime environment
FROM runtime-image AS final-stage
#  Copy application artifacts from the build stage (e.g., JAR file)
COPY --from=build-stage /path/in/build/stage /path/to/place/in/final/stage
# Define runtime configuration (e.g., CMD, ENTRYPOINT)
```

This Dockerfile uses two stages:

- The build stage uses a base image containing build tools needed to compile your application. It includes commands to install build tools, copy source code, and execute build commands.
- The final stage uses a smaller base image suitable for running your application. It copies the compiled artifacts (a JAR file, for example) from the build stage. Finally, it defines the runtime configuration (using `CMD` or `ENTRYPOINT`) for starting your application.

## Try it out

In this hands-on guide, you'll unlock the power of multi-stage builds to create lean and efficient Docker images for a sample Java application. You'll use a simple “Hello World” Spring Boot-based application built with Maven as your example.

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.
2. Open this [pre-initialized project](https://start.spring.io/#!type=maven-project&language=java&platformVersion=4.0.1&packaging=jar&configurationFileFormat=properties&jvmVersion=21&groupId=com.example&artifactId=spring-boot-docker&name=spring-boot-docker&description=Demo%20project%20for%20Spring%20Boot&packageName=com.example.spring-boot-docker&dependencies=web) to generate a ZIP file. Here’s how that looks:
  ![A screenshot of Spring Initializr tool selected with Java 21, Spring Web and Spring Boot 3.4.0](https://docs.docker.com/get-started/docker-concepts/building-images/images/multi-stage-builds-spring-initializer.webp)  ![A screenshot of Spring Initializr tool selected with Java 21, Spring Web and Spring Boot 3.4.0](https://docs.docker.com/get-started/docker-concepts/building-images/images/multi-stage-builds-spring-initializer.webp)
  [Spring Initializr](https://start.spring.io/) is a quickstart generator for Spring projects. It provides an extensible API to generate JVM-based projects with implementations for several common concepts — like basic language generation for Java, Kotlin, Groovy, and Maven.
  Select **Generate** to create and download the zip file for this project.
  For this demonstration, you’ve paired Maven build automation with Java, a Spring Web dependency, and Java 21 for your metadata.
3. Navigate the project directory. Once you unzip the file, you'll see the following project directory structure:
  ```plaintext
  spring-boot-docker
  ├── HELP.md
  ├── mvnw
  ├── mvnw.cmd
  ├── pom.xml
  └── src
      ├── main
      │   ├── java
      │   │   └── com
      │   │       └── example
      │   │           └── spring_boot_docker
      │   │               └── SpringBootDockerApplication.java
      │   └── resources
      │       ├── application.properties
      │       ├── static
      │       └── templates
      └── test
          └── java
              └── com
                  └── example
                      └── spring_boot_docker
                          └── SpringBootDockerApplicationTests.java
  15 directories, 7 files
  ```
  The `src/main/java` directory contains your project's source code, the `src/test/java` directory
  contains the test source, and the `pom.xml` file is your project’s Project Object Model (POM).
  The `pom.xml` file is the core of a Maven project's configuration. It's a single configuration file that
  contains most of the information needed to build a customized project. The POM is huge and can seem
  daunting. Thankfully, you don't yet need to understand every intricacy to use it effectively.
4. Create a RESTful web service that displays "Hello World!".
  Under the `src/main/java/com/example/spring_boot_docker/` directory, you can modify your
  `SpringBootDockerApplication.java` file with the following content:
  ```java
  package com.example.spring_boot_docker;
  import org.springframework.boot.SpringApplication;
  import org.springframework.boot.autoconfigure.SpringBootApplication;
  import org.springframework.web.bind.annotation.RequestMapping;
  import org.springframework.web.bind.annotation.RestController;
  @RestController
  @SpringBootApplication
  public class SpringBootDockerApplication {
      @RequestMapping("/")
          public String home() {
          return "Hello World";
      }
  	public static void main(String[] args) {
  		SpringApplication.run(SpringBootDockerApplication.class, args);
  	}
  }
  ```
  The `SpringbootDockerApplication.java` file starts by declaring your `com.example.spring_boot_docker` package and importing necessary Spring frameworks. This Java file creates a simple Spring Boot web application that responds with "Hello World" when a user visits its homepage.

### Create the Dockerfile

Now that you have the project, you’re ready to create the `Dockerfile`.

1. Create a file named `Dockerfile` in the same folder that contains all the other folders and files (like src, pom.xml, etc.).
2. In the `Dockerfile`, define your base image by adding the following line:
  ```dockerfile
  FROM eclipse-temurin:21.0.8_9-jdk-jammy
  ```
3. Now, define the working directory by using the `WORKDIR` instruction. This will specify where future commands will run and the directory files will be copied inside the container image.
  ```dockerfile
  WORKDIR /app
  ```
4. Copy both the Maven wrapper script and your project's `pom.xml` file into the current working directory `/app` within the Docker container.
  ```dockerfile
  COPY .mvn/ .mvn
  COPY mvnw pom.xml ./
  ```
5. Execute a command within the container. It runs the `./mvnw dependency:go-offline` command, which uses the Maven wrapper (`./mvnw`) to download all dependencies for your project without building the final JAR file (useful for faster builds).
  ```dockerfile
  RUN ./mvnw dependency:go-offline
  ```
6. Copy the `src` directory from your project on the host machine to the `/app` directory within the container.
  ```dockerfile
  COPY src ./src
  ```
7. Set the default command to be executed when the container starts. This command instructs the container to run the Maven wrapper (`./mvnw`) with the `spring-boot:run` goal, which will build and execute your Spring Boot application.
  ```dockerfile
  CMD ["./mvnw", "spring-boot:run"]
  ```
  And with that, you should have the following Dockerfile:
  ```dockerfile
  FROM eclipse-temurin:21.0.8_9-jdk-jammy
  WORKDIR /app
  COPY .mvn/ .mvn
  COPY mvnw pom.xml ./
  RUN ./mvnw dependency:go-offline
  COPY src ./src
  CMD ["./mvnw", "spring-boot:run"]
  ```

### Build the container image

1. Execute the following command to build the Docker image:
  ```console
  $ docker build -t spring-helloworld .
  ```
2. Check the size of the Docker image by using the `docker images` command:
  ```console
  $ docker images
  ```
  Doing so will produce output like the following:
  ```console
  REPOSITORY          TAG       IMAGE ID       CREATED          SIZE
  spring-helloworld   latest    ff708d5ee194   3 minutes ago    880MB
  ```
  This output shows that your image is 880MB in size. It contains the full JDK, Maven toolchain, and more. In production, you don’t need that in your final image.

### Run the Spring Boot application

1. Now that you have an image built, it's time to run the container.
  ```console
  $ docker run -p 8080:8080 spring-helloworld
  ```
  You'll then see output similar to the following in the container log:
  ```plaintext
  [INFO] --- spring-boot:3.3.4:run (default-cli) @ spring-boot-docker ---
  [INFO] Attaching agents: []
       .   ____          _            __ _ _
      /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
     ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
      \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
       '  |____| .__|_| |_|_| |_\__, | / / / /
      =========|_|==============|___/=/_/_/_/
      :: Spring Boot ::                (v3.3.4)
  2024-09-29T23:54:07.157Z  INFO 159 --- [spring-boot-docker] [           main]
  c.e.s.SpringBootDockerApplication        : Starting SpringBootDockerApplication using Java
  21.0.2 with PID 159 (/app/target/classes started by root in /app)
   ….
  ```
2. Access your “Hello World” page through your web browser at [http://localhost:8080](http://localhost:8080), or via this curl command:
  ```console
  $ curl localhost:8080
  Hello World
  ```

### Use multi-stage builds

1. Consider the following Dockerfile:
  ```dockerfile
  FROM eclipse-temurin:21.0.8_9-jdk-jammy AS builder
  WORKDIR /opt/app
  COPY .mvn/ .mvn
  COPY mvnw pom.xml ./
  RUN ./mvnw dependency:go-offline
  COPY ./src ./src
  RUN ./mvnw clean install
  FROM eclipse-temurin:21.0.8_9-jre-jammy AS final
  WORKDIR /opt/app
  EXPOSE 8080
  COPY --from=builder /opt/app/target/*.jar /opt/app/*.jar
  ENTRYPOINT ["java", "-jar", "/opt/app/*.jar"]
  ```
  Notice that this Dockerfile has been split into two stages.
  - The first stage remains the same as the previous Dockerfile, providing a Java Development Kit (JDK) environment for building the application. This stage is given the name of builder.
  - The second stage is a new stage named `final`. It uses a slimmer `eclipse-temurin:21.0.2_13-jre-jammy` image, containing just the Java Runtime Environment (JRE) needed to run the application. This image provides a Java Runtime Environment (JRE) which is enough for running the compiled application (JAR file).
  > For production use, it's highly recommended that you produce a custom JRE-like runtime using jlink. JRE images are available for all versions of Eclipse Temurin, but `jlink` allows you to create a minimal runtime containing only the necessary Java modules for your application. This can significantly reduce the size and improve the security of your final image. [Refer to this page](https://hub.docker.com/_/eclipse-temurin) for more information.
  With multi-stage builds, a Docker build uses one base image for compilation, packaging, and unit tests and then a separate image for the application runtime. As a result, the final image is smaller in size since it doesn’t contain any development or debugging tools. By separating the build environment from the final runtime environment, you can significantly reduce the image size and increase the security of your final images.
2. Now, rebuild your image and run your ready-to-use production build.
  ```console
  $ docker build -t spring-helloworld-builder .
  ```
  This command builds a Docker image named `spring-helloworld-builder` using the final stage from your `Dockerfile` file located in the current directory.
  > Note
  >
  > In your multi-stage Dockerfile, the final stage (final) is the default target for building. This means that if you don't explicitly specify a target stage using the `--target` flag in the `docker build` command, Docker will automatically build the last stage by default. You could use `docker build -t spring-helloworld-builder --target builder .` to build only the builder stage with the JDK environment.
3. Look at the image size difference by using the `docker images` command:
  ```console
  $ docker images
  ```
  You'll get output similar to the following:
  ```console
  spring-helloworld-builder latest    c5c76cb815c0   24 minutes ago      428MB
  spring-helloworld         latest    ff708d5ee194   About an hour ago   880MB
  ```
  Your final image is just 428 MB, compared to the original build size of 880 MB.
  By optimizing each stage and only including what's necessary, you were able to significantly reduce the overall image size while still achieving the same functionality. This not only improves performance but also makes your Docker images more lightweight, more secure, and easier to manage.

## Additional resources

- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Base images](https://docs.docker.com/build/building/base-images/)
- [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker)

---

# Understanding the image layers

> This concept page will teach you about the layers of container image.

# Understanding the image layers

   Table of contents

---

## Explanation

As you learned in [What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/), container images are composed of layers. And each of these layers, once created, are immutable. But, what does that actually mean? And how are those layers used to create the filesystem a container can use?

### Image layers

Each layer in an image contains a set of filesystem changes - additions, deletions, or modifications. Let’s look at a theoretical image:

1. The first layer adds basic commands and a package manager, such as apt.
2. The second layer installs a Python runtime and pip for dependency management.
3. The third layer copies in an application’s specific requirements.txt file.
4. The fourth layer installs that application’s specific dependencies.
5. The fifth layer copies in the actual source code of the application.

This example might look like:

![screenshot of the flowchart showing the concept of the image layers](https://docs.docker.com/get-started/docker-concepts/building-images/images/container_image_layers.webp)  ![screenshot of the flowchart showing the concept of the image layers](https://docs.docker.com/get-started/docker-concepts/building-images/images/container_image_layers.webp)

This is beneficial because it allows layers to be reused between images. For example, imagine you wanted to create another Python application. Due to layering, you can leverage the same Python base. This will make builds faster and reduce the amount of storage and bandwidth required to distribute the images. The image layering might look similar to the following:

![screenshot of the flowchart showing the benefits of the image layering](https://docs.docker.com/get-started/docker-concepts/building-images/images/container_image_layer_reuse.webp)  ![screenshot of the flowchart showing the benefits of the image layering](https://docs.docker.com/get-started/docker-concepts/building-images/images/container_image_layer_reuse.webp)

Layers let you extend images of others by reusing their base layers, allowing you to add only the data that your application needs.

### Stacking the layers

Layering is made possible by content-addressable storage and union filesystems. While this will get technical, here’s how it works:

1. After each layer is downloaded, it is extracted into its own directory on the host filesystem.
2. When you run a container from an image, a union filesystem is created where layers are stacked on top of each other, creating a new and unified view.
3. When the container starts, its root directory is set to the location of this unified directory, using `chroot`.

When the union filesystem is created, in addition to the image layers, a directory is created specifically for the running container. This allows the container to make filesystem changes while allowing the original image layers to remain untouched. This enables you to run multiple containers from the same underlying image.

## Try it out

In this hands-on guide, you will create new image layers manually using the [docker container commit](https://docs.docker.com/reference/cli/docker/container/commit/) command. Note that you’ll rarely create images this way, as you’ll normally [use a Dockerfile](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/). But, it makes it easier to understand how it’s all working.

### Create a base image

In this first step, you will create your own base image that you will then use for the following steps.

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.
2. In a terminal, run the following command to start a new container:
  ```console
  $ docker run --name=base-container -ti ubuntu
  ```
  Once the image has been downloaded and the container has started, you should see a new shell prompt. This is running inside your container. It will look similar to the following (the container ID will vary):
  ```console
  root@d8c5ca119fcd:/#
  ```
3. Inside the container, run the following command to install Node.js:
  ```console
  $ apt update && apt install -y nodejs
  ```
  When this command runs, it downloads and installs Node inside the container. In the context of the union filesystem, these filesystem changes occur within the directory unique to this container.
4. Validate if Node is installed by running the following command:
  ```console
  $ node -e 'console.log("Hello world!")'
  ```
  You should then see a “Hello world!” appear in the console.
5. Now that you have Node installed, you’re ready to save the changes you’ve made as a new image layer, from which you can start new containers or build new images. To do so, you will use the [docker container commit](https://docs.docker.com/reference/cli/docker/container/commit/) command. Run the following command in a new terminal:
  ```console
  $ docker container commit -m "Add node" base-container node-base
  ```
6. View the layers of your image using the `docker image history` command:
  ```console
  $ docker image history node-base
  ```
  You will see output similar to the following:
  ```console
  IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
  9e274734bb25   10 seconds ago   /bin/bash                                       157MB     Add node
  cd1dba651b30   7 days ago       /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
  <missing>      7 days ago       /bin/sh -c #(nop) ADD file:6089c6bede9eca8ec…   110MB
  <missing>      7 days ago       /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
  <missing>      7 days ago       /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
  <missing>      7 days ago       /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
  <missing>      7 days ago       /bin/sh -c #(nop)  ARG RELEASE                  0B
  ```
  Note the “Add node” comment on the top line. This layer contains the Node.js install you just made.
7. To prove your image has Node installed, you can start a new container using this new image:
  ```console
  $ docker run node-base node -e "console.log('Hello again')"
  ```
  With that, you should get a “Hello again” output in the terminal, showing Node was installed and working.
8. Now that you’re done creating your base image, you can remove that container:
  ```console
  $ docker rm -f base-container
  ```

> **Base image definition**
>
>
>
> A base image is a foundation for building other images. It's possible to use any images as a base image. However, some images are intentionally created as building blocks, providing a foundation or starting point for an application.
>
>
>
> In this example, you probably won’t deploy this `node-base` image, as it doesn’t actually do anything yet. But it’s a base you can use for other builds.

### Build an app image

Now that you have a base image, you can extend that image to build additional images.

1. Start a new container using the newly created node-base image:
  ```console
  $ docker run --name=app-container -ti node-base
  ```
2. Inside of this container, run the following command to create a Node program:
  ```console
  $ echo 'console.log("Hello from an app")' > app.js
  ```
  To run this Node program, you can use the following command and see the message printed on the screen:
  ```console
  $ node app.js
  ```
3. In another terminal, run the following command to save this container’s changes as a new image:
  ```console
  $ docker container commit -c "CMD node app.js" -m "Add app" app-container sample-app
  ```
  This command not only creates a new image named `sample-app`, but also adds additional configuration to the image to set the default command when starting a container. In this case, you are setting it to automatically run `node app.js`.
4. In a terminal outside of the container, run the following command to view the updated layers:
  ```console
  $ docker image history sample-app
  ```
  You’ll then see output that looks like the following. Note the top layer comment has “Add app” and the next layer has “Add node”:
  ```console
  IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
  c1502e2ec875   About a minute ago   /bin/bash                                       33B       Add app
  5310da79c50a   4 minutes ago        /bin/bash                                       126MB     Add node
  2b7cc08dcdbb   5 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
  <missing>      5 weeks ago          /bin/sh -c #(nop) ADD file:07cdbabf782942af0…   69.2MB
  <missing>      5 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
  <missing>      5 weeks ago          /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B
  <missing>      5 weeks ago          /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH     0B
  <missing>      5 weeks ago          /bin/sh -c #(nop)  ARG RELEASE                  0B
  ```
5. Finally, start a new container using the brand new image. Since you specified the default command, you can use the following command:
  ```console
  $ docker run sample-app
  ```
  You should see your greeting appear in the terminal, coming from your Node program.
6. Now that you’re done with your containers, you can remove them using the following command:
  ```console
  $ docker rm -f app-container
  ```

## Additional resources

If you’d like to dive deeper into the things you learned, check out the following resources:

- [docker image history](https://docs.docker.com/reference/cli/docker/image/history/)
- [docker container commit](https://docs.docker.com/reference/cli/docker/container/commit/)

## Next steps

As hinted earlier, most image builds don’t use `docker container commit`. Instead, you’ll use a Dockerfile which automates these steps for you.

[Writing a Dockerfile](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)

---

# Using the build cache

> This concept page will teach you about the build cache, what changes invalidate the cache and how to effectively use the build cache.

# Using the build cache

   Table of contents

---

## Explanation

Consider the following Dockerfile that you created for the [getting-started](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/) app.

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "./src/index.js"]
```

When you run the `docker build` command to create a new image, Docker executes each instruction in your Dockerfile, creating a layer for each command and in the order specified. For each instruction, Docker checks whether it can reuse the instruction from a previous build. If it finds that you've already executed a similar instruction before, Docker doesn't need to redo it. Instead, it’ll use the cached result. This way, your build process becomes faster and more efficient, saving you valuable time and resources.

Using the build cache effectively lets you achieve faster builds by reusing results from previous builds and skipping unnecessary work.
In order to maximize cache usage and avoid resource-intensive and time-consuming rebuilds, it's important to understand how cache invalidation works.
Here are a few examples of situations that can cause cache to be invalidated:

- Any changes to the command of a `RUN` instruction invalidates that layer. Docker detects the change and invalidates the build cache if there's any modification to a `RUN` command in your Dockerfile.
- Any changes to files copied into the image with the `COPY` or `ADD` instructions. Docker keeps an eye on any alterations to files within your project directory. Whether it's a change in content or properties like permissions, Docker considers these modifications as triggers to invalidate the cache.
- Once one layer is invalidated, all following layers are also invalidated. If any previous layer, including the base image or intermediary layers, has been invalidated due to changes, Docker ensures that subsequent layers relying on it are also invalidated. This keeps the build process synchronized and prevents inconsistencies.

When you're writing or editing a Dockerfile, keep an eye out for unnecessary cache misses to ensure that builds run as fast and efficiently as possible.

## Try it out

In this hands-on guide, you will learn how to use the Docker build cache effectively for a Node.js application.

### Build the application

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.
2. Open a terminal and [clone this sample application](https://github.com/dockersamples/todo-list-app).
  ```console
  $ git clone https://github.com/dockersamples/todo-list-app
  ```
3. Navigate into the `todo-list-app` directory:
  ```console
  $ cd todo-list-app
  ```
  Inside this directory, you'll find a file named `Dockerfile` with the following content:
  ```dockerfile
  FROM node:22-alpine
  WORKDIR /app
  COPY . .
  RUN yarn install --production
  EXPOSE 3000
  CMD ["node", "./src/index.js"]
  ```
4. Execute the following command to build the Docker image:
  ```console
  $ docker build .
  ```
  Here’s the result of the build process:
  ```console
  [+] Building 20.0s (10/10) FINISHED
  ```
  The first line indicates that the entire build process took *20.0 seconds*. The first build may take some time as it installs dependencies.
5. Rebuild without making changes.
  Now, re-run the `docker build` command without making any change in the source code or Dockerfile as shown:
  ```console
  $ docker build .
  ```
  Subsequent builds after the initial are faster due to the caching mechanism, as long as the commands and context remain unchanged. Docker caches the intermediate layers generated during the build process. When you rebuild the image without making any changes to the Dockerfile or the source code, Docker can reuse the cached layers, significantly speeding up the build process.
  ```console
  [+] Building 1.0s (9/9) FINISHED                                                                            docker:desktop-linux
   => [internal] load build definition from Dockerfile                                                                        0.0s
   => => transferring dockerfile: 187B                                                                                        0.0s
   ...
   => [internal] load build context                                                                                           0.0s
   => => transferring context: 8.16kB                                                                                         0.0s
   => CACHED [2/4] WORKDIR /app                                                                                               0.0s
   => CACHED [3/4] COPY . .                                                                                                   0.0s
   => CACHED [4/4] RUN yarn install --production                                                                              0.0s
   => exporting to image                                                                                                      0.0s
   => => exporting layers                                                                                                     0.0s
   => => exporting manifest
  ```
  The subsequent build was completed in just 1.0 second by leveraging the cached layers. No need to repeat time-consuming steps like installing dependencies.
  | Steps | Description | Time Taken (1st Run) | Time Taken (2nd Run) |
  | --- | --- | --- | --- |
  | 1 | Load build definition from Dockerfile | 0.0 seconds | 0.0 seconds |
  | 2 | Load metadata for docker.io/library/node:22-alpine | 2.7 seconds | 0.9 seconds |
  | 3 | Load .dockerignore | 0.0 seconds | 0.0 seconds |
  | 4 | Load build context(Context size: 4.60MB) | 0.1 seconds | 0.0 seconds |
  | 5 | Set the working directory (WORKDIR) | 0.1 seconds | 0.0 seconds |
  | 6 | Copy the local code into the container | 0.0 seconds | 0.0 seconds |
  | 7 | Run yarn install --production | 10.0 seconds | 0.0 seconds |
  | 8 | Exporting layers | 2.2 seconds | 0.0 seconds |
  | 9 | Exporting the final image | 3.0 seconds | 0.0 seconds |
  Going back to the `docker image history` output, you see that each command in the Dockerfile becomes a new layer in the image. You might remember that when you made a change to the image, the `yarn` dependencies had to be reinstalled. Is there a way to fix this? It doesn't make much sense to reinstall the same dependencies every time you build, right?
  To fix this, restructure your Dockerfile so that the dependency cache remains valid unless it really needs to be invalidated. For Node-based applications, dependencies are defined in the `package.json` file. You'll want to reinstall the dependencies if that file changes, but use cached dependencies if the file is unchanged. So, start by copying only that file first, then install the dependencies, and finally copy everything else. Then, you only need to recreate the yarn dependencies if there was a change to the `package.json` file.
6. Update the Dockerfile to copy in the `package.json` file first, install dependencies, and then copy everything else in.
  ```dockerfile
  FROM node:22-alpine
  WORKDIR /app
  COPY package.json yarn.lock ./
  RUN yarn install --production
  COPY . .
  EXPOSE 3000
  CMD ["node", "src/index.js"]
  ```
7. Create a file named `.dockerignore` in the same folder as the Dockerfile with the following contents.
  ```plaintext
  node_modules
  ```
8. Build the new image:
  ```console
  $ docker build .
  ```
  You'll then see output similar to the following:
  ```console
  [+] Building 16.1s (10/10) FINISHED
  => [internal] load build definition from Dockerfile                                               0.0s
  => => transferring dockerfile: 175B                                                               0.0s
  => [internal] load .dockerignore                                                                  0.0s
  => => transferring context: 2B                                                                    0.0s
  => [internal] load metadata for docker.io/library/node:22-alpine                                  0.0s
  => [internal] load build context                                                                  0.8s
  => => transferring context: 53.37MB                                                               0.8s
  => [1/5] FROM docker.io/library/node:22-alpine                                                    0.0s
  => CACHED [2/5] WORKDIR /app                                                                      0.0s
  => [3/5] COPY package.json yarn.lock ./                                                           0.2s
  => [4/5] RUN yarn install --production                                                           14.0s
  => [5/5] COPY . .                                                                                 0.5s
  => exporting to image                                                                             0.6s
  => => exporting layers                                                                            0.6s
  => => writing image
  sha256:d6f819013566c54c50124ed94d5e66c452325327217f4f04399b45f94e37d25        0.0s
  => => naming to docker.io/library/node-app:2.0                                                 0.0s
  ```
  You'll see that all layers were rebuilt. Perfectly fine since you changed the Dockerfile quite a bit.
9. Now, make a change to the `src/static/index.html` file (like change the title to say "The Awesome Todo App").
10. Build the Docker image. This time, your output should look a little different.
  ```console
  $ docker build -t node-app:3.0 .
  ```
  You'll then see output similar to the following:
  ```console
  [+] Building 1.2s (10/10) FINISHED
  => [internal] load build definition from Dockerfile                                               0.0s
  => => transferring dockerfile: 37B                                                                0.0s
  => [internal] load .dockerignore                                                                  0.0s
  => => transferring context: 2B                                                                    0.0s
  => [internal] load metadata for docker.io/library/node:22-alpine                                  0.0s
  => [internal] load build context                                                                  0.2s
  => => transferring context: 450.43kB                                                              0.2s
  => [1/5] FROM docker.io/library/node:22-alpine                                                    0.0s
  => CACHED [2/5] WORKDIR /app                                                                      0.0s
  => CACHED [3/5] COPY package.json yarn.lock ./                                                    0.0s
  => CACHED [4/5] RUN yarn install --production                                                     0.0s
  => [5/5] COPY . .                                                                                 0.5s
  => exporting to image                                                                             0.3s
  => => exporting layers                                                                            0.3s
  => => writing image
  sha256:91790c87bcb096a83c2bd4eb512bc8b134c757cda0bdee4038187f98148e2eda       0.0s
  => => naming to docker.io/library/node-app:3.0                                                 0.0s
  ```
  First off, you should notice that the build was much faster. You'll see that several steps are using previously cached layers. That's good news; you're using the build cache. Pushing and pulling this image and updates to it will be much faster as well.

By following these optimization techniques, you can make your Docker builds faster and more efficient, leading to quicker iteration cycles and improved development productivity.

## Additional resources

- [Optimizing builds with cache management](https://docs.docker.com/build/cache/)
- [Cache Storage Backend](https://docs.docker.com/build/cache/backends/)
- [Build cache invalidation](https://docs.docker.com/build/cache/invalidation/)

## Next steps

Now that you understand how to use the Docker build cache effectively, you're ready to learn about Multi-stage builds.

[Multi-stage builds](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)
