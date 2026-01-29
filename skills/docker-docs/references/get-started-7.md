# Image and more

# Image

> Tips for building images for your application

# Image-building best practices

   Table of contents

---

## Image layering

Using the `docker image history` command, you can see the command that was used
to create each layer within an image.

1. Use the `docker image history` command to see the layers in the `getting-started` image you
  created.
  ```console
  $ docker image history getting-started
  ```
  You should get output that looks something like the following.
  ```plaintext
  IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
  a78a40cbf866        18 seconds ago      /bin/sh -c #(nop)  CMD ["node" "src/index.j…    0B
  f1d1808565d6        19 seconds ago      /bin/sh -c npm install --omit=dev               85.4MB
  a2c054d14948        36 seconds ago      /bin/sh -c #(nop) COPY dir:5dc710ad87c789593…   198kB
  9577ae713121        37 seconds ago      /bin/sh -c #(nop) WORKDIR /app                  0B
  b95baba1cfdb        13 days ago         /bin/sh -c #(nop)  CMD ["node"]                 0B
  <missing>           13 days ago         /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B
  <missing>           13 days ago         /bin/sh -c #(nop) COPY file:238737301d473041…   116B
  <missing>           13 days ago         /bin/sh -c apk add --no-cache --virtual .bui…   5.35MB
  <missing>           13 days ago         /bin/sh -c addgroup -g 1000 node     && addu…   74.3MB
  <missing>           13 days ago         /bin/sh -c #(nop)  ENV NODE_VERSION=12.14.1     0B
  <missing>           13 days ago         /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
  <missing>           13 days ago         /bin/sh -c #(nop) ADD file:e69d441d729412d24…   5.59MB
  ```
  Each of the lines represents a layer in the image. The display here shows the base at the bottom with
  the newest layer at the top. Using this, you can also quickly see the size of each layer, helping
  diagnose large images.
2. You'll notice that several of the lines are truncated. If you add the `--no-trunc` flag, you'll get the
  full output.
  ```console
  $ docker image history --no-trunc getting-started
  ```

## Layer caching

Now that you've seen the layering in action, there's an important lesson to learn to help decrease build
times for your container images. Once a layer changes, all downstream layers have to be recreated as well.

Look at the following Dockerfile you created for the getting started app.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:24-alpine
WORKDIR /app
COPY . .
RUN npm install --omit=dev
CMD ["node", "src/index.js"]
EXPOSE 3000
```

Going back to the image history output, you see that each command in the Dockerfile becomes a new layer in the image.
You might remember that when you made a change to the image, the dependencies had to be reinstalled. It doesn't make much sense to ship around the same dependencies every time you build.

To fix it, you need to restructure your Dockerfile to help support the caching
of the dependencies. For Node-based applications, those dependencies are defined
in the `package.json` file. You can copy only that file in first, install the
dependencies, and then copy in everything else. Then, you only recreate the
dependencies if there was a change to the `package.json`.

1. Update the Dockerfile to copy in the `package.json` first, install dependencies, and then copy everything else in.
  ```dockerfile
  # syntax=docker/dockerfile:1
  FROM node:24-alpine
  WORKDIR /app
  COPY package.json package-lock.json ./
  RUN npm install --omit=dev
  COPY . .
  CMD ["node", "src/index.js"]
  ```
2. Build a new image using `docker build`.
  ```console
  $ docker build -t getting-started .
  ```
  You should see output like the following.
  ```plaintext
  [+] Building 16.1s (10/10) FINISHED
  => [internal] load build definition from Dockerfile
  => => transferring dockerfile: 175B
  => [internal] load .dockerignore
  => => transferring context: 2B
  => [internal] load metadata for docker.io/library/node:24-alpine
  => [internal] load build context
  => => transferring context: 53.37MB
  => [1/5] FROM docker.io/library/node:24-alpine
  => CACHED [2/5] WORKDIR /app
  => [3/5] COPY package.json package-lock.json ./
  => [4/5] RUN npm install --omit=dev
  => [5/5] COPY . .
  => exporting to image
  => => exporting layers
  => => writing image     sha256:d6f819013566c54c50124ed94d5e66c452325327217f4f04399b45f94e37d25
  => => naming to docker.io/library/getting-started
  ```
3. Now, make a change to the `src/static/index.html` file. For example, change the `<title>` to "The Awesome Todo App".
4. Build the Docker image now using `docker build -t getting-started .` again. This time, your output should look a little different.
  ```plaintext
  [+] Building 1.2s (10/10) FINISHED
  => [internal] load build definition from Dockerfile
  => => transferring dockerfile: 37B
  => [internal] load .dockerignore
  => => transferring context: 2B
  => [internal] load metadata for docker.io/library/node:24-alpine
  => [internal] load build context
  => => transferring context: 450.43kB
  => [1/5] FROM docker.io/library/node:24-alpine
  => CACHED [2/5] WORKDIR /app
  => CACHED [3/5] COPY package.json package-lock.json ./
  => CACHED [4/5] RUN npm install
  => [5/5] COPY . .
  => exporting to image
  => => exporting layers
  => => writing image     sha256:91790c87bcb096a83c2bd4eb512bc8b134c757cda0bdee4038187f98148e2eda
  => => naming to docker.io/library/getting-started
  ```
  First off, you should notice that the build was much faster. And, you'll see
  that several steps are using previously cached layers. Pushing and pulling
  this image and updates to it will be much faster as well.

## Multi-stage builds

Multi-stage builds are an incredibly powerful
tool to help use multiple stages to create an image. There are several advantages for them:

- Separate build-time dependencies from runtime dependencies
- Reduce overall image size by shipping only what your app needs to run

### Maven/Tomcat example

When building Java-based applications, you need a JDK to compile the source code to Java bytecode. However,
that JDK isn't needed in production. Also, you might be using tools like Maven or Gradle to help build the app.
Those also aren't needed in your final image. Multi-stage builds help.

```dockerfile
# syntax=docker/dockerfile:1
FROM maven AS build
WORKDIR /app
COPY . .
RUN mvn package

FROM tomcat
COPY --from=build /app/target/file.war /usr/local/tomcat/webapps
```

In this example, you use one stage (called `build`) to perform the actual Java build using Maven. In the second
stage (starting at `FROM tomcat`), you copy in files from the `build` stage. The final image is only the last stage
being created, which can be overridden using the `--target` flag.

### React example

When building React applications, you need a Node environment to compile the JS code (typically JSX), SASS stylesheets,
and more into static HTML, JS, and CSS. If you aren't doing server-side rendering, you don't even need a Node environment
for your production build. You can ship the static resources in a static nginx container.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:24-alpine AS build
WORKDIR /app
COPY package* ./
RUN npm install
COPY public ./public
COPY src ./src
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

In the previous Dockerfile example, it uses the `node:24-alpine` image to perform the build (maximizing layer caching) and then copies the output
into an nginx container.

> Tips
>
> This React example is for illustration purposes. The getting-started todo app is a `Node.js` backend application, not a React frontend.

## Summary

In this section, you learned a few image building best practices, including layer caching and multi-stage builds.

Related information:

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/)

## Next steps

In the next section, you'll learn about additional resources you can use to continue learning about containers.

[What next](https://docs.docker.com/get-started/workshop/10_what_next/)

---

# What next after the Docker workshop

> Explore what to do next after completing the Docker workshop, including securing your images, AI development, and language-specific guides.

# What next after the Docker workshop

---

Congratulations on completing the Docker workshop. You've learned how to containerize applications, work with multi-container setups, use Docker Compose, and apply image-building best practices.

Here's what to explore next.

## Secure your images

Take your image-building skills to the next level with Docker Hardened Images—secure, minimal, and production-ready base images that are now free for everyone.

[What are Docker Hardened Images?Understand secure, minimal, production-ready base images with near-zero CVEs.](https://docs.docker.com/dhi/explore/what/)[Get started with DHIPull and run your first Docker Hardened Image in minutes.](https://docs.docker.com/dhi/get-started/)[Use hardened imagesLearn how to use DHI in your Dockerfiles and CI/CD pipelines.](https://docs.docker.com/dhi/how-to/use/)[Explore the DHI catalogBrowse available hardened images, variants, and security attestations.](https://docs.docker.com/dhi/how-to/explore/)

## Build with AI

Docker makes it easy to run AI models locally and build agentic AI applications. Explore Docker's AI tools and start building AI-powered apps.

[Docker Model RunnerRun and manage AI models locally using familiar Docker commands with OpenAI-compatible APIs.](https://docs.docker.com/ai/model-runner/)[MCP ToolkitSet up, manage, and run containerized MCP servers to power your AI agents.](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)[Build AI agents with cagentCreate teams of specialized AI agents that collaborate to solve complex problems.](https://docs.docker.com/ai/cagent/)[Use AI models in ComposeDefine AI model dependencies in your Docker Compose applications.](https://docs.docker.com/compose/how-tos/model-runner/)

## Language-specific guides

Apply what you've learned to your preferred programming language with hands-on tutorials.

[Node.jsLearn how to containerize and develop Node.js applications.](https://docs.docker.com/guides/language/nodejs/)[PythonBuild and run Python applications in containers.](https://docs.docker.com/guides/language/python/)[JavaContainerize Java applications with best practices.](https://docs.docker.com/guides/language/java/)[GoDevelop and deploy Go applications using Docker.](https://docs.docker.com/guides/language/golang/)

---

# Overview of the Docker workshop

> Get started with the Docker basics in this workshop, You'll learn about containers, images, and how to containerize your first application.

# Overview of the Docker workshop

   Table of contents

---

This 45-minute workshop contains step-by-step instructions on how to get started with Docker. This workshop shows you how to:

- Build and run an image as a container.
- Share images using Docker Hub.
- Deploy Docker applications using multiple containers with a database.
- Run applications using Docker Compose.

> Note
>
> For a quick introduction to Docker and the benefits of containerizing your
> applications, see
> [Getting started](https://docs.docker.com/get-started/introduction/).

## What is a container?

A container is a sandboxed process running on a host machine that is isolated from all other processes running on that host machine. That isolation leverages [kernel namespaces and cgroups](https://medium.com/@saschagrunert/demystifying-containers-part-i-kernel-space-2c53d6979504),
features that have been in Linux for a long time. Docker makes these capabilities approachable and easy to use. To summarize, a container:

- Is a runnable instance of an image. You can create, start, stop, move, or delete a container using the Docker API or CLI.
- Can be run on local machines, virtual machines, or deployed to the cloud.
- Is portable (and can be run on any OS).
- Is isolated from other containers and runs its own software, binaries, configurations, etc.

If you're familiar with `chroot`, then think of a container as an extended version of `chroot`. The filesystem comes from the image. However, a container adds additional isolation not available when using chroot.

## What is an image?

A running container uses an isolated filesystem. This isolated filesystem is provided by an image, and the image must contain everything needed to run an application - all dependencies, configurations, scripts, binaries, etc. The image also contains other configurations for the container, such as environment variables, a default command to run, and other metadata.

## Next steps

In this section, you learned about containers and images.

Next, you'll containerize a simple application and get hands-on with the concepts.

[Containerize an application](https://docs.docker.com/get-started/workshop/02_our_app/)
