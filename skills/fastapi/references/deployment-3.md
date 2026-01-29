# Run a Server Manually¶ and more

# Run a Server Manually¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Run a Server Manually¶

## Use thefastapi runCommand¶

In short, use `fastapi run` to serve your FastAPI application:

```
<font color="#4E9A06">fastapi</font> run <u style="text-decoration-style:solid">main.py</u>
```

That would work for most of the cases. 😎

You could use that command for example to start your **FastAPI** app in a container, in a server, etc.

## ASGI Servers¶

Let's go a little deeper into the details.

FastAPI uses a standard for building Python web frameworks and servers called ASGI. FastAPI is an ASGI web framework.

The main thing you need to run a **FastAPI** application (or any other ASGI application) in a remote server machine is an ASGI server program like **Uvicorn**, this is the one that comes by default in the `fastapi` command.

There are several alternatives, including:

- [Uvicorn](https://www.uvicorn.dev/): a high performance ASGI server.
- [Hypercorn](https://hypercorn.readthedocs.io/): an ASGI server compatible with HTTP/2 and Trio among other features.
- [Daphne](https://github.com/django/daphne): the ASGI server built for Django Channels.
- [Granian](https://github.com/emmett-framework/granian): A Rust HTTP server for Python applications.
- [NGINX Unit](https://unit.nginx.org/howto/fastapi/): NGINX Unit is a lightweight and versatile web application runtime.

## Server Machine and Server Program¶

There's a small detail about names to keep in mind. 💡

The word "**server**" is commonly used to refer to both the remote/cloud computer (the physical or virtual machine) and also the program that is running on that machine (e.g. Uvicorn).

Just keep in mind that when you read "server" in general, it could refer to one of those two things.

When referring to the remote machine, it's common to call it **server**, but also **machine**, **VM** (virtual machine), **node**. Those all refer to some type of remote machine, normally running Linux, where you run programs.

## Install the Server Program¶

When you install FastAPI, it comes with a production server, Uvicorn, and you can start it with the `fastapi run` command.

But you can also install an ASGI server manually.

Make sure you create a [virtual environment](https://fastapi.tiangolo.com/virtual-environments/), activate it, and then you can install the server application.

For example, to install Uvicorn:

```
pip install "uvicorn[standard]"
```

A similar process would apply to any other ASGI server program.

Tip

By adding the `standard`, Uvicorn will install and use some recommended extra dependencies.

That including `uvloop`, the high-performance drop-in replacement for `asyncio`, that provides the big concurrency performance boost.

When you install FastAPI with something like `pip install "fastapi[standard]"` you already get `uvicorn[standard]` as well.

## Run the Server Program¶

If you installed an ASGI server manually, you would normally need to pass an import string in a special format for it to import your FastAPI application:

```
uvicorn main:app --host 0.0.0.0 --port 80
```

Note

The command `uvicorn main:app` refers to:

- `main`: the file `main.py` (the Python "module").
- `app`: the object created inside of `main.py` with the line `app = FastAPI()`.

It is equivalent to:

```
from main import app
```

Each alternative ASGI server program would have a similar command, you can read more in their respective documentation.

Warning

Uvicorn and other servers support a `--reload` option that is useful during development.

The `--reload` option consumes much more resources, is more unstable, etc.

It helps a lot during **development**, but you **shouldn't** use it in **production**.

## Deployment Concepts¶

These examples run the server program (e.g Uvicorn), starting **a single process**, listening on all the IPs (`0.0.0.0`) on a predefined port (e.g. `80`).

This is the basic idea. But you will probably want to take care of some additional things, like:

- Security - HTTPS
- Running on startup
- Restarts
- Replication (the number of processes running)
- Memory
- Previous steps before starting

I'll tell you more about each of these concepts, how to think about them, and some concrete examples with strategies to handle them in the next chapters. 🚀

---

# Server Workers

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Server Workers - Uvicorn with Workers¶

Let's check back those deployment concepts from before:

- Security - HTTPS
- Running on startup
- Restarts
- **Replication (the number of processes running)**
- Memory
- Previous steps before starting

Up to this point, with all the tutorials in the docs, you have probably been running a **server program**, for example, using the `fastapi` command, that runs Uvicorn, running a **single process**.

When deploying applications you will probably want to have some **replication of processes** to take advantage of **multiple cores** and to be able to handle more requests.

As you saw in the previous chapter about [Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/), there are multiple strategies you can use.

Here I'll show you how to use **Uvicorn** with **worker processes** using the `fastapi` command or the `uvicorn` command directly.

Info

If you are using containers, for example with Docker or Kubernetes, I'll tell you more about that in the next chapter: [FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/).

In particular, when running on **Kubernetes** you will probably **not** want to use workers and instead run **a single Uvicorn process per container**, but I'll tell you about it later in that chapter.

## Multiple Workers¶

You can start multiple workers with the `--workers` command line option:

 [fastapi](#__tabbed_1_1)[uvicorn](#__tabbed_1_2)

If you use the `fastapi` command:

```
<font color="#4E9A06">fastapi</font> run --workers 4 <u style="text-decoration-style:solid">main.py</u>
```

If you prefer to use the `uvicorn` command directly:

```
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4
```

The only new option here is `--workers` telling Uvicorn to start 4 worker processes.

You can also see that it shows the **PID** of each process, `27365` for the parent process (this is the **process manager**) and one for each worker process: `27368`, `27369`, `27370`, and `27367`.

## Deployment Concepts¶

Here you saw how to use multiple **workers** to **parallelize** the execution of the application, take advantage of **multiple cores** in the CPU, and be able to serve **more requests**.

From the list of deployment concepts from above, using workers would mainly help with the **replication** part, and a little bit with the **restarts**, but you still need to take care of the others:

- **Security - HTTPS**
- **Running on startup**
- **Restarts**
- Replication (the number of processes running)
- **Memory**
- **Previous steps before starting**

## Containers and Docker¶

In the next chapter about [FastAPI in Containers - Docker](https://fastapi.tiangolo.com/deployment/docker/) I'll explain some strategies you could use to handle the other **deployment concepts**.

I'll show you how to **build your own image from scratch** to run a single Uvicorn process. It is a simple process and is probably what you would want to do when using a distributed container management system like **Kubernetes**.

## Recap¶

You can use multiple worker processes with the `--workers` CLI option with the `fastapi` or `uvicorn` commands to take advantage of **multi-core CPUs**, to run **multiple processes in parallel**.

You could use these tools and ideas if you are setting up **your own deployment system** while taking care of the other deployment concepts yourself.

Check out the next chapter to learn about **FastAPI** with containers (e.g. Docker and Kubernetes). You will see that those tools have simple ways to solve the other **deployment concepts** as well. ✨

---

# About FastAPI versions¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# About FastAPI versions¶

**FastAPI** is already being used in production in many applications and systems. And the test coverage is kept at 100%. But its development is still moving quickly.

New features are added frequently, bugs are fixed regularly, and the code is still continuously improving.

That's why the current versions are still `0.x.x`, this reflects that each version could potentially have breaking changes. This follows the [Semantic Versioning](https://semver.org/) conventions.

You can create production applications with **FastAPI** right now (and you have probably been doing it for some time), you just have to make sure that you use a version that works correctly with the rest of your code.

## Pin yourfastapiversion¶

The first thing you should do is to "pin" the version of **FastAPI** you are using to the specific latest version that you know works correctly for your application.

For example, let's say you are using version `0.112.0` in your app.

If you use a `requirements.txt` file you could specify the version with:

```
fastapi[standard]==0.112.0
```

that would mean that you would use exactly the version `0.112.0`.

Or you could also pin it with:

```
fastapi[standard]>=0.112.0,<0.113.0
```

that would mean that you would use the versions `0.112.0` or above, but less than `0.113.0`, for example, a version `0.112.2` would still be accepted.

If you use any other tool to manage your installations, like `uv`, Poetry, Pipenv, or others, they all have a way that you can use to define specific versions for your packages.

## Available versions¶

You can see the available versions (e.g. to check what is the current latest) in the [Release Notes](https://fastapi.tiangolo.com/release-notes/).

## About versions¶

Following the Semantic Versioning conventions, any version below `1.0.0` could potentially add breaking changes.

FastAPI also follows the convention that any "PATCH" version change is for bug fixes and non-breaking changes.

Tip

The "PATCH" is the last number, for example, in `0.2.3`, the PATCH version is `3`.

So, you should be able to pin to a version like:

```
fastapi>=0.45.0,<0.46.0
```

Breaking changes and new features are added in "MINOR" versions.

Tip

The "MINOR" is the number in the middle, for example, in `0.2.3`, the MINOR version is `2`.

## Upgrading the FastAPI versions¶

You should add tests for your app.

With **FastAPI** it's very easy (thanks to Starlette), check the docs: [Testing](https://fastapi.tiangolo.com/tutorial/testing/)

After you have tests, then you can upgrade the **FastAPI** version to a more recent one, and make sure that all your code is working correctly by running your tests.

If everything is working, or after you make the necessary changes, and all your tests are passing, then you can pin your `fastapi` to that new recent version.

## About Starlette¶

You shouldn't pin the version of `starlette`.

Different versions of **FastAPI** will use a specific newer version of Starlette.

So, you can just let **FastAPI** use the correct Starlette version.

## About Pydantic¶

Pydantic includes the tests for **FastAPI** with its own tests, so new versions of Pydantic (above `1.0.0`) are always compatible with FastAPI.

You can pin Pydantic to any version above `1.0.0` that works for you.

For example:

```
pydantic>=2.7.0,<3.0.0
```
