# FastAPI in Containers and more

# FastAPI in Containers

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# FastAPI in Containers - Docker¶

When deploying FastAPI applications a common approach is to build a **Linux container image**. It's normally done using [Docker](https://www.docker.com/). You can then deploy that container image in one of a few possible ways.

Using Linux containers has several advantages including **security**, **replicability**, **simplicity**, and others.

Tip

In a hurry and already know this stuff? Jump to the [Dockerfilebelow 👇](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi).

   Dockerfile Preview 👀

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]
```

## What is a Container¶

Containers (mainly Linux containers) are a very **lightweight** way to package applications including all their dependencies and necessary files while keeping them isolated from other containers (other applications or components) in the same system.

Linux containers run using the same Linux kernel of the host (machine, virtual machine, cloud server, etc). This just means that they are very lightweight (compared to full virtual machines emulating an entire operating system).

This way, containers consume **little resources**, an amount comparable to running the processes directly (a virtual machine would consume much more).

Containers also have their own **isolated** running processes (commonly just one process), file system, and network, simplifying deployment, security, development, etc.

## What is a Container Image¶

A **container** is run from a **container image**.

A container image is a **static** version of all the files, environment variables, and the default command/program that should be present in a container. **Static** here means that the container **image** is not running, it's not being executed, it's only the packaged files and metadata.

In contrast to a "**container image**" that is the stored static contents, a "**container**" normally refers to the running instance, the thing that is being **executed**.

When the **container** is started and running (started from a **container image**) it could create or change files, environment variables, etc. Those changes will exist only in that container, but would not persist in the underlying container image (would not be saved to disk).

A container image is comparable to the **program** file and contents, e.g. `python` and some file `main.py`.

And the **container** itself (in contrast to the **container image**) is the actual running instance of the image, comparable to a **process**. In fact, a container is running only when it has a **process running** (and normally it's only a single process). The container stops when there's no process running in it.

## Container Images¶

Docker has been one of the main tools to create and manage **container images** and **containers**.

And there's a public [Docker Hub](https://hub.docker.com/) with pre-made **official container images** for many tools, environments, databases, and applications.

For example, there's an official [Python Image](https://hub.docker.com/_/python).

And there are many other images for different things like databases, for example for:

- [PostgreSQL](https://hub.docker.com/_/postgres)
- [MySQL](https://hub.docker.com/_/mysql)
- [MongoDB](https://hub.docker.com/_/mongo)
- [Redis](https://hub.docker.com/_/redis), etc.

By using a pre-made container image it's very easy to **combine** and use different tools. For example, to try out a new database. In most cases, you can use the **official images**, and just configure them with environment variables.

That way, in many cases you can learn about containers and Docker and reuse that knowledge with many different tools and components.

So, you would run **multiple containers** with different things, like a database, a Python application, a web server with a React frontend application, and connect them together via their internal network.

All the container management systems (like Docker or Kubernetes) have these networking features integrated into them.

## Containers and Processes¶

A **container image** normally includes in its metadata the default program or command that should be run when the **container** is started and the parameters to be passed to that program. Very similar to what would be if it was in the command line.

When a **container** is started, it will run that command/program (although you can override it and make it run a different command/program).

A container is running as long as the **main process** (command or program) is running.

A container normally has a **single process**, but it's also possible to start subprocesses from the main process, and that way you will have **multiple processes** in the same container.

But it's not possible to have a running container without **at least one running process**. If the main process stops, the container stops.

## Build a Docker Image for FastAPI¶

Okay, let's build something now! 🚀

I'll show you how to build a **Docker image** for FastAPI **from scratch**, based on the **official Python** image.

This is what you would want to do in **most cases**, for example:

- Using **Kubernetes** or similar tools
- When running on a **Raspberry Pi**
- Using a cloud service that would run a container image for you, etc.

### Package Requirements¶

You would normally have the **package requirements** for your application in some file.

It would depend mainly on the tool you use to **install** those requirements.

The most common way to do it is to have a file `requirements.txt` with the package names and their versions, one per line.

You would of course use the same ideas you read in [About FastAPI versions](https://fastapi.tiangolo.com/deployment/versions/) to set the ranges of versions.

For example, your `requirements.txt` could look like:

```
fastapi[standard]>=0.113.0,<0.114.0
pydantic>=2.7.0,<3.0.0
```

And you would normally install those package dependencies with `pip`, for example:

```
pip install -r requirements.txt
```

Info

There are other formats and tools to define and install package dependencies.

### Create theFastAPICode¶

- Create an `app` directory and enter it.
- Create an empty file `__init__.py`.
- Create a `main.py` file with:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

### Dockerfile¶

Now in the same project directory create a file `Dockerfile` with:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

1.
2.
3.
4.
5.
6.

Tip

Review what each line does by clicking each number bubble in the code. 👆

Warning

Make sure to **always** use the **exec form** of the `CMD` instruction, as explained below.

#### UseCMD- Exec Form¶

The [CMD](https://docs.docker.com/reference/dockerfile/#cmd) Docker instruction can be written using two forms:

✅ **Exec** form:

```
# ✅ Do this
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

⛔️ **Shell** form:

```
# ⛔️ Don't do this
CMD fastapi run app/main.py --port 80
```

Make sure to always use the **exec** form to ensure that FastAPI can shutdown gracefully and [lifespan events](https://fastapi.tiangolo.com/advanced/events/) are triggered.

You can read more about it in the [Docker docs for shell and exec form](https://docs.docker.com/reference/dockerfile/#shell-and-exec-form).

This can be quite noticeable when using `docker compose`. See this Docker Compose FAQ section for more technical details: [Why do my services take 10 seconds to recreate or stop?](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop).

#### Directory Structure¶

You should now have a directory structure like:

```
.
├── app
│   ├── __init__.py
│   └── main.py
├── Dockerfile
└── requirements.txt
```

#### Behind a TLS Termination Proxy¶

If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, add the option `--proxy-headers`, this will tell Uvicorn (through the FastAPI CLI) to trust the headers sent by that proxy telling it that the application is running behind HTTPS, etc.

```
CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]
```

#### Docker Cache¶

There's an important trick in this `Dockerfile`, we first copy the **file with the dependencies alone**, not the rest of the code. Let me tell you why is that.

```
COPY ./requirements.txt /code/requirements.txt
```

Docker and other tools **build** these container images **incrementally**, adding **one layer on top of the other**, starting from the top of the `Dockerfile` and adding any files created by each of the instructions of the `Dockerfile`.

Docker and similar tools also use an **internal cache** when building the image, if a file hasn't changed since the last time building the container image, then it will **reuse the same layer** created the last time, instead of copying the file again and creating a new layer from scratch.

Just avoiding the copy of files doesn't necessarily improve things too much, but because it used the cache for that step, it can **use the cache for the next step**. For example, it could use the cache for the instruction that installs dependencies with:

```
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
```

The file with the package requirements **won't change frequently**. So, by copying only that file, Docker will be able to **use the cache** for that step.

And then, Docker will be able to **use the cache for the next step** that downloads and install those dependencies. And here's where we **save a lot of time**. ✨ ...and avoid boredom waiting. 😪😆

Downloading and installing the package dependencies **could take minutes**, but using the **cache** would **take seconds** at most.

And as you would be building the container image again and again during development to check that your code changes are working, there's a lot of accumulated time this would save.

Then, near the end of the `Dockerfile`, we copy all the code. As this is what **changes most frequently**, we put it near the end, because almost always, anything after this step will not be able to use the cache.

```
COPY ./app /code/app
```

### Build the Docker Image¶

Now that all the files are in place, let's build the container image.

- Go to the project directory (in where your `Dockerfile` is, containing your `app` directory).
- Build your FastAPI image:

```
docker build -t myimage .
```

Tip

Notice the `.` at the end, it's equivalent to `./`, it tells Docker the directory to use to build the container image.

In this case, it's the same current directory (`.`).

### Start the Docker Container¶

- Run a container based on your image:

```
docker run -d --name mycontainer -p 80:80 myimage
```

## Check it¶

You should be able to check it in your Docker container's URL, for example: [http://192.168.99.100/items/5?q=somequery](http://192.168.99.100/items/5?q=somequery) or [http://127.0.0.1/items/5?q=somequery](http://127.0.0.1/items/5?q=somequery) (or equivalent, using your Docker host).

You will see something like:

```
{"item_id": 5, "q": "somequery"}
```

## Interactive API docs¶

Now you can go to [http://192.168.99.100/docs](http://192.168.99.100/docs) or [http://127.0.0.1/docs](http://127.0.0.1/docs) (or equivalent, using your Docker host).

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

## Alternative API docs¶

And you can also go to [http://192.168.99.100/redoc](http://192.168.99.100/redoc) or [http://127.0.0.1/redoc](http://127.0.0.1/redoc) (or equivalent, using your Docker host).

You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Rebilly/ReDoc)):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Build a Docker Image with a Single-File FastAPI¶

If your FastAPI is a single file, for example, `main.py` without an `./app` directory, your file structure could look like this:

```
.
├── Dockerfile
├── main.py
└── requirements.txt
```

Then you would just have to change the corresponding paths to copy the file inside the `Dockerfile`:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/

CMD ["fastapi", "run", "main.py", "--port", "80"]
```

1.
2.

When you pass the file to `fastapi run` it will detect automatically that it is a single file and not part of a package and will know how to import it and serve your FastAPI app. 😎

## Deployment Concepts¶

Let's talk again about some of the same [Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/) in terms of containers.

Containers are mainly a tool to simplify the process of **building and deploying** an application, but they don't enforce a particular approach to handle these **deployment concepts**, and there are several possible strategies.

The **good news** is that with each different strategy there's a way to cover all of the deployment concepts. 🎉

Let's review these **deployment concepts** in terms of containers:

- HTTPS
- Running on startup
- Restarts
- Replication (the number of processes running)
- Memory
- Previous steps before starting

## HTTPS¶

If we focus just on the **container image** for a FastAPI application (and later the running **container**), HTTPS normally would be handled **externally** by another tool.

It could be another container, for example with [Traefik](https://traefik.io/), handling **HTTPS** and **automatic** acquisition of **certificates**.

Tip

Traefik has integrations with Docker, Kubernetes, and others, so it's very easy to set up and configure HTTPS for your containers with it.

Alternatively, HTTPS could be handled by a cloud provider as one of their services (while still running the application in a container).

## Running on Startup and Restarts¶

There is normally another tool in charge of **starting and running** your container.

It could be **Docker** directly, **Docker Compose**, **Kubernetes**, a **cloud service**, etc.

In most (or all) cases, there's a simple option to enable running the container on startup and enabling restarts on failures. For example, in Docker, it's the command line option `--restart`.

Without using containers, making applications run on startup and with restarts can be cumbersome and difficult. But when **working with containers** in most cases that functionality is included by default. ✨

## Replication - Number of Processes¶

If you have a cluster of machines with **Kubernetes**, Docker Swarm Mode, Nomad, or another similar complex system to manage distributed containers on multiple machines, then you will probably want to **handle replication** at the **cluster level** instead of using a **process manager** (like Uvicorn with workers) in each container.

One of those distributed container management systems like Kubernetes normally has some integrated way of handling **replication of containers** while still supporting **load balancing** for the incoming requests. All at the **cluster level**.

In those cases, you would probably want to build a **Docker image from scratch** as [explained above](https://fastapi.tiangolo.com/deployment/docker/#dockerfile), installing your dependencies, and running **a single Uvicorn process** instead of using multiple Uvicorn workers.

### Load Balancer¶

When using containers, you would normally have some component **listening on the main port**. It could possibly be another container that is also a **TLS Termination Proxy** to handle **HTTPS** or some similar tool.

As this component would take the **load** of requests and distribute that among the workers in a (hopefully) **balanced** way, it is also commonly called a **Load Balancer**.

Tip

The same **TLS Termination Proxy** component used for HTTPS would probably also be a **Load Balancer**.

And when working with containers, the same system you use to start and manage them would already have internal tools to transmit the **network communication** (e.g. HTTP requests) from that **load balancer** (that could also be a **TLS Termination Proxy**) to the container(s) with your app.

### One Load Balancer - Multiple Worker Containers¶

When working with **Kubernetes** or similar distributed container management systems, using their internal networking mechanisms would allow the single **load balancer** that is listening on the main **port** to transmit communication (requests) to possibly **multiple containers** running your app.

Each of these containers running your app would normally have **just one process** (e.g. a Uvicorn process running your FastAPI application). They would all be **identical containers**, running the same thing, but each with its own process, memory, etc. That way you would take advantage of **parallelization** in **different cores** of the CPU, or even in **different machines**.

And the distributed container system with the **load balancer** would **distribute the requests** to each one of the containers with your app **in turns**. So, each request could be handled by one of the multiple **replicated containers** running your app.

And normally this **load balancer** would be able to handle requests that go to *other* apps in your cluster (e.g. to a different domain, or under a different URL path prefix), and would transmit that communication to the right containers for *that other* application running in your cluster.

### One Process per Container¶

In this type of scenario, you probably would want to have **a single (Uvicorn) process per container**, as you would already be handling replication at the cluster level.

So, in this case, you **would not** want to have a multiple workers in the container, for example with the `--workers` command line option. You would want to have just a **single Uvicorn process** per container (but probably multiple containers).

Having another process manager inside the container (as would be with multiple workers) would only add **unnecessary complexity** that you are most probably already taking care of with your cluster system.

### Containers with Multiple Processes and Special Cases¶

Of course, there are **special cases** where you could want to have **a container** with several **Uvicorn worker processes** inside.

In those cases, you can use the `--workers` command line option to set the number of workers that you want to run:

```
FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
```

1.

Here are some examples of when that could make sense:

#### A Simple App¶

You could want a process manager in the container if your application is **simple enough** that can run it on a **single server**, not a cluster.

#### Docker Compose¶

You could be deploying to a **single server** (not a cluster) with **Docker Compose**, so you wouldn't have an easy way to manage replication of containers (with Docker Compose) while preserving the shared network and **load balancing**.

Then you could want to have **a single container** with a **process manager** starting **several worker processes** inside.

---

The main point is, **none** of these are **rules written in stone** that you have to blindly follow. You can use these ideas to **evaluate your own use case** and decide what is the best approach for your system, checking out how to manage the concepts of:

- Security - HTTPS
- Running on startup
- Restarts
- Replication (the number of processes running)
- Memory
- Previous steps before starting

## Memory¶

If you run **a single process per container** you will have a more or less well-defined, stable, and limited amount of memory consumed by each of those containers (more than one if they are replicated).

And then you can set those same memory limits and requirements in your configurations for your container management system (for example in **Kubernetes**). That way it will be able to **replicate the containers** in the **available machines** taking into account the amount of memory needed by them, and the amount available in the machines in the cluster.

If your application is **simple**, this will probably **not be a problem**, and you might not need to specify hard memory limits. But if you are **using a lot of memory** (for example with **machine learning** models), you should check how much memory you are consuming and adjust the **number of containers** that runs in **each machine** (and maybe add more machines to your cluster).

If you run **multiple processes per container** you will have to make sure that the number of processes started doesn't **consume more memory** than what is available.

## Previous Steps Before Starting and Containers¶

If you are using containers (e.g. Docker, Kubernetes), then there are two main approaches you can use.

### Multiple Containers¶

If you have **multiple containers**, probably each one running a **single process** (for example, in a **Kubernetes** cluster), then you would probably want to have a **separate container** doing the work of the **previous steps** in a single container, running a single process, **before** running the replicated worker containers.

Info

If you are using Kubernetes, this would probably be an [Init Container](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/).

If in your use case there's no problem in running those previous steps **multiple times in parallel** (for example if you are not running database migrations, but just checking if the database is ready yet), then you could also just put them in each container right before starting the main process.

### Single Container¶

If you have a simple setup, with a **single container** that then starts multiple **worker processes** (or also just one process), then you could run those previous steps in the same container, right before starting the process with the app.

### Base Docker Image¶

There used to be an official FastAPI Docker image: [tiangolo/uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker). But it is now deprecated. ⛔️

You should probably **not** use this base Docker image (or any other similar one).

If you are using **Kubernetes** (or others) and you are already setting **replication** at the cluster level, with multiple **containers**. In those cases, you are better off **building an image from scratch** as described above: [Build a Docker Image for FastAPI](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi).

And if you need to have multiple workers, you can simply use the `--workers` command line option.

Technical Details

The Docker image was created when Uvicorn didn't support managing and restarting dead workers, so it was needed to use Gunicorn with Uvicorn, which added quite some complexity, just to have Gunicorn manage and restart the Uvicorn worker processes.

But now that Uvicorn (and the `fastapi` command) support using `--workers`, there's no reason to use a base Docker image instead of building your own (it's pretty much the same amount of code 😅).

## Deploy the Container Image¶

After having a Container (Docker) Image there are several ways to deploy it.

For example:

- With **Docker Compose** in a single server
- With a **Kubernetes** cluster
- With a Docker Swarm Mode cluster
- With another tool like Nomad
- With a cloud service that takes your container image and deploys it

## Docker Image withuv¶

If you are using [uv](https://github.com/astral-sh/uv) to install and manage your project, you can follow their [uv Docker guide](https://docs.astral.sh/uv/guides/integration/docker/).

## Recap¶

Using container systems (e.g. with **Docker** and **Kubernetes**) it becomes fairly straightforward to handle all the **deployment concepts**:

- HTTPS
- Running on startup
- Restarts
- Replication (the number of processes running)
- Memory
- Previous steps before starting

In most cases, you probably won't want to use any base image, and instead **build a container image from scratch** based on the official Python Docker image.

Taking care of the **order** of instructions in the `Dockerfile` and the **Docker cache** you can **minimize build times**, to maximize your productivity (and avoid boredom). 😎

---

# FastAPI Cloud¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# FastAPI Cloud¶

You can deploy your FastAPI app to [FastAPI Cloud](https://fastapicloud.com) with **one command**, go and join the waiting list if you haven't. 🚀

## Login¶

Make sure you already have a **FastAPI Cloud** account (we invited you from the waiting list 😉).

Then log in:

```
fastapi login
```

## Deploy¶

Now deploy your app, with **one command**:

```
fastapi deploy
```

That's it! Now you can access your app at that URL. ✨

## About FastAPI Cloud¶

**FastAPI Cloud** is built by the same author and team behind **FastAPI**.

It streamlines the process of **building**, **deploying**, and **accessing** an API with minimal effort.

It brings the same **developer experience** of building apps with FastAPI to **deploying** them to the cloud. 🎉

It will also take care of most of the things you would need when deploying an app, like:

- HTTPS
- Replication, with autoscaling based on requests
- etc.

FastAPI Cloud is the primary sponsor and funding provider for the *FastAPI and friends* open source projects. ✨

## Deploy to other cloud providers¶

FastAPI is open source and based on standards. You can deploy FastAPI apps to any cloud provider you choose.

Follow your cloud provider's guides to deploy FastAPI apps with them. 🤓

## Deploy your own server¶

I will also teach you later in this **Deployment** guide all the details, so you can understand what is going on, what needs to happen, or how to deploy FastAPI apps on your own, also with your own servers. 🤓

---

# About HTTPS¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# About HTTPS¶

It is easy to assume that HTTPS is something that is just "enabled" or not.

But it is way more complex than that.

Tip

If you are in a hurry or don't care, continue with the next sections for step by step instructions to set everything up with different techniques.

To **learn the basics of HTTPS**, from a consumer perspective, check [https://howhttps.works/](https://howhttps.works/).

Now, from a **developer's perspective**, here are several things to keep in mind while thinking about HTTPS:

- For HTTPS, **the server** needs to **have "certificates"** generated by a **third party**.
  - Those certificates are actually **acquired** from the third party, not "generated".
- Certificates have a **lifetime**.
  - They **expire**.
  - And then they need to be **renewed**, **acquired again** from the third party.
- The encryption of the connection happens at the **TCP level**.
  - That's one layer **below HTTP**.
  - So, the **certificate and encryption** handling is done **before HTTP**.
- **TCP doesn't know about "domains"**. Only about IP addresses.
  - The information about the **specific domain** requested goes in the **HTTP data**.
- The **HTTPS certificates** "certify" a **certain domain**, but the protocol and encryption happen at the TCP level, **before knowing** which domain is being dealt with.
- **By default**, that would mean that you can only have **one HTTPS certificate per IP address**.
  - No matter how big your server is or how small each application you have on it might be.
  - There is a **solution** to this, however.
- There's an **extension** to the **TLS** protocol (the one handling the encryption at the TCP level, before HTTP) called **SNI**.
  - This SNI extension allows one single server (with a **single IP address**) to have **several HTTPS certificates** and serve **multiple HTTPS domains/applications**.
  - For this to work, a **single** component (program) running on the server, listening on the **public IP address**, must have **all the HTTPS certificates** in the server.
- **After** obtaining a secure connection, the communication protocol is **still HTTP**.
  - The contents are **encrypted**, even though they are being sent with the **HTTP protocol**.

It is a common practice to have **one program/HTTP server** running on the server (the machine, host, etc.) and **managing all the HTTPS parts**: receiving the **encrypted HTTPS requests**, sending the **decrypted HTTP requests** to the actual HTTP application running in the same server (the **FastAPI** application, in this case), take the **HTTP response** from the application, **encrypt it** using the appropriate **HTTPS certificate** and sending it back to the client using **HTTPS**. This server is often called a **TLS Termination Proxy**.

Some of the options you could use as a TLS Termination Proxy are:

- Traefik (that can also handle certificate renewals)
- Caddy (that can also handle certificate renewals)
- Nginx
- HAProxy

## Let's Encrypt¶

Before Let's Encrypt, these **HTTPS certificates** were sold by trusted third parties.

The process to acquire one of these certificates used to be cumbersome, require quite some paperwork and the certificates were quite expensive.

But then **Let's Encrypt** was created.

It is a project from the Linux Foundation. It provides **HTTPS certificates for free**, in an automated way. These certificates use all the standard cryptographic security, and are short-lived (about 3 months), so the **security is actually better** because of their reduced lifespan.

The domains are securely verified and the certificates are generated automatically. This also allows automating the renewal of these certificates.

The idea is to automate the acquisition and renewal of these certificates so that you can have **secure HTTPS, for free, forever**.

## HTTPS for Developers¶

Here's an example of how an HTTPS API could look like, step by step, paying attention mainly to the ideas important for developers.

### Domain Name¶

It would probably all start by you **acquiring** some **domain name**. Then, you would configure it in a DNS server (possibly your same cloud provider).

You would probably get a cloud server (a virtual machine) or something similar, and it would have a fixed **public IP address**.

In the DNS server(s) you would configure a record (an "`A record`") to point **your domain** to the public **IP address of your server**.

You would probably do this just once, the first time, when setting everything up.

Tip

This Domain Name part is way before HTTPS, but as everything depends on the domain and the IP address, it's worth mentioning it here.

### DNS¶

Now let's focus on all the actual HTTPS parts.

First, the browser would check with the **DNS servers** what is the **IP for the domain**, in this case, `someapp.example.com`.

The DNS servers would tell the browser to use some specific **IP address**. That would be the public IP address used by your server, that you configured in the DNS servers.

![image](https://fastapi.tiangolo.com/img/deployment/https/https01.drawio.svg)

### TLS Handshake Start¶

The browser would then communicate with that IP address on **port 443** (the HTTPS port).

The first part of the communication is just to establish the connection between the client and the server and to decide the cryptographic keys they will use, etc.

![image](https://fastapi.tiangolo.com/img/deployment/https/https02.drawio.svg)

This interaction between the client and the server to establish the TLS connection is called the **TLS handshake**.

### TLS with SNI Extension¶

**Only one process** in the server can be listening on a specific **port** in a specific **IP address**. There could be other processes listening on other ports in the same IP address, but only one for each combination of IP address and port.

TLS (HTTPS) uses the specific port `443` by default. So that's the port we would need.

As only one process can be listening on this port, the process that would do it would be the **TLS Termination Proxy**.

The TLS Termination Proxy would have access to one or more **TLS certificates** (HTTPS certificates).

Using the **SNI extension** discussed above, the TLS Termination Proxy would check which of the TLS (HTTPS) certificates available it should use for this connection, using the one that matches the domain expected by the client.

In this case, it would use the certificate for `someapp.example.com`.

![image](https://fastapi.tiangolo.com/img/deployment/https/https03.drawio.svg)

The client already **trusts** the entity that generated that TLS certificate (in this case Let's Encrypt, but we'll see about that later), so it can **verify** that the certificate is valid.

Then, using the certificate, the client and the TLS Termination Proxy **decide how to encrypt** the rest of the **TCP communication**. This completes the **TLS Handshake** part.

After this, the client and the server have an **encrypted TCP connection**, this is what TLS provides. And then they can use that connection to start the actual **HTTP communication**.

And that's what **HTTPS** is, it's just plain **HTTP** inside a **secure TLS connection** instead of a pure (unencrypted) TCP connection.

Tip

Notice that the encryption of the communication happens at the **TCP level**, not at the HTTP level.

### HTTPS Request¶

Now that the client and server (specifically the browser and the TLS Termination Proxy) have an **encrypted TCP connection**, they can start the **HTTP communication**.

So, the client sends an **HTTPS request**. This is just an HTTP request through an encrypted TLS connection.

![image](https://fastapi.tiangolo.com/img/deployment/https/https04.drawio.svg)

### Decrypt the Request¶

The TLS Termination Proxy would use the encryption agreed to **decrypt the request**, and would transmit the **plain (decrypted) HTTP request** to the process running the application (for example a process with Uvicorn running the FastAPI application).

![image](https://fastapi.tiangolo.com/img/deployment/https/https05.drawio.svg)

### HTTP Response¶

The application would process the request and send a **plain (unencrypted) HTTP response** to the TLS Termination Proxy.

![image](https://fastapi.tiangolo.com/img/deployment/https/https06.drawio.svg)

### HTTPS Response¶

The TLS Termination Proxy would then **encrypt the response** using the cryptography agreed before (that started with the certificate for `someapp.example.com`), and send it back to the browser.

Next, the browser would verify that the response is valid and encrypted with the right cryptographic key, etc. It would then **decrypt the response** and process it.

![image](https://fastapi.tiangolo.com/img/deployment/https/https07.drawio.svg)

The client (browser) will know that the response comes from the correct server because it is using the cryptography they agreed using the **HTTPS certificate** before.

### Multiple Applications¶

In the same server (or servers), there could be **multiple applications**, for example, other API programs or a database.

Only one process can be handling the specific IP and port (the TLS Termination Proxy in our example) but the other applications/processes can be running on the server(s) too, as long as they don't try to use the same **combination of public IP and port**.

![image](https://fastapi.tiangolo.com/img/deployment/https/https08.drawio.svg)

That way, the TLS Termination Proxy could handle HTTPS and certificates for **multiple domains**, for multiple applications, and then transmit the requests to the right application in each case.

### Certificate Renewal¶

At some point in the future, each certificate would **expire** (about 3 months after acquiring it).

And then, there would be another program (in some cases it's another program, in some cases it could be the same TLS Termination Proxy) that would talk to Let's Encrypt, and renew the certificate(s).

![image](https://fastapi.tiangolo.com/img/deployment/https/https.drawio.svg)

The **TLS certificates** are **associated with a domain name**, not with an IP address.

So, to renew the certificates, the renewal program needs to **prove** to the authority (Let's Encrypt) that it indeed **"owns" and controls that domain**.

To do that, and to accommodate different application needs, there are several ways it can do it. Some popular ways are:

- **Modify some DNS records**.
  - For this, the renewal program needs to support the APIs of the DNS provider, so, depending on the DNS provider you are using, this might or might not be an option.
- **Run as a server** (at least during the certificate acquisition process) on the public IP address associated with the domain.
  - As we said above, only one process can be listening on a specific IP and port.
  - This is one of the reasons why it's very useful when the same TLS Termination Proxy also takes care of the certificate renewal process.
  - Otherwise, you might have to stop the TLS Termination Proxy momentarily, start the renewal program to acquire the certificates, then configure them with the TLS Termination Proxy, and then restart the TLS Termination Proxy. This is not ideal, as your app(s) will not be available during the time that the TLS Termination Proxy is off.

All this renewal process, while still serving the app, is one of the main reasons why you would want to have a **separate system to handle HTTPS** with a TLS Termination Proxy instead of just using the TLS certificates with the application server directly (e.g. Uvicorn).

## Proxy Forwarded Headers¶

When using a proxy to handle HTTPS, your **application server** (for example Uvicorn via FastAPI CLI) doesn't known anything about the HTTPS process, it communicates with plain HTTP with the **TLS Termination Proxy**.

This **proxy** would normally set some HTTP headers on the fly before transmitting the request to the **application server**, to let the application server know that the request is being **forwarded** by the proxy.

Technical Details

The proxy headers are:

- [X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)
- [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto)
- [X-Forwarded-Host](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Host)

Nevertheless, as the **application server** doesn't know it is behind a trusted **proxy**, by default, it wouldn't trust those headers.

But you can configure the **application server** to trust the *forwarded* headers sent by the **proxy**. If you are using FastAPI CLI, you can use the *CLI Option* `--forwarded-allow-ips` to tell it from which IPs it should trust those *forwarded* headers.

For example, if the **application server** is only receiving communication from the trusted **proxy**, you can set it to `--forwarded-allow-ips="*"` to make it trust all incoming IPs, as it will only receive requests from whatever is the IP used by the **proxy**.

This way the application would be able to know what is its own public URL, if it is using HTTPS, the domain, etc.

This would be useful for example to properly handle redirects.

Tip

You can learn more about this in the documentation for [Behind a Proxy - Enable Proxy Forwarded Headers](https://fastapi.tiangolo.com/advanced/behind-a-proxy/#enable-proxy-forwarded-headers)

## Recap¶

Having **HTTPS** is very important, and quite **critical** in most cases. Most of the effort you as a developer have to put around HTTPS is just about **understanding these concepts** and how they work.

But once you know the basic information of **HTTPS for developers** you can easily combine and configure different tools to help you manage everything in a simple way.

In some of the next chapters, I'll show you several concrete examples of how to set up **HTTPS** for **FastAPI** applications. 🔒
