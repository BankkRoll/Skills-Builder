# Use bind mounts and more

# Use bind mounts

> Using bind mounts in our application

# Use bind mounts

   Table of contents

---

In [part 4](https://docs.docker.com/get-started/workshop/05_persisting_data/), you used a volume mount to persist the
data in your database. A volume mount is a great choice when you need somewhere
persistent to store your application data.

A bind mount is another type of mount, which lets you share a directory from the
host's filesystem into the container. When working on an application, you can
use a bind mount to mount source code into the container. The container sees the
changes you make to the code immediately, as soon as you save a file. This means
that you can run processes in the container that watch for filesystem changes
and respond to them.

In this chapter, you'll see how you can use bind mounts and a tool called
[nodemon](https://npmjs.com/package/nodemon) to watch for file changes, and then restart the application
automatically. There are equivalent tools in most other languages and
frameworks.

## Quick volume type comparisons

The following are examples of a named volume and a bind mount using `--mount`:

- Named volume: `type=volume,src=my-volume,target=/usr/local/data`
- Bind mount: `type=bind,src=/path/to/data,target=/usr/local/data`

The following table outlines the main differences between volume mounts and bind
mounts.

|  | Named volumes | Bind mounts |
| --- | --- | --- |
| Host location | Docker chooses | You decide |
| Populates new volume with container contents | Yes | No |
| Supports Volume Drivers | Yes | No |

## Trying out bind mounts

Before looking at how you can use bind mounts for developing your application,
you can run a quick experiment to get a practical understanding of how bind mounts
work.

1. Verify that your `getting-started-app` directory is in a directory defined in
  Docker Desktop's file sharing setting. This setting defines which parts of your
  filesystem you can share with containers. For details about accessing the setting, see
  [File sharing](https://docs.docker.com/desktop/settings-and-maintenance/settings/#file-sharing).
  > Note
  >
  > The **File sharing** tab is only available in Hyper-V mode, because the files are automatically shared in WSL 2 mode and Windows container mode.
2. Open a terminal and change directory to the `getting-started-app`
  directory.
3. Run the following command to start `bash` in an `ubuntu` container with a
  bind mount.
  ```console
  $ docker run -it --mount type=bind,src=.,target=/src ubuntu bash
  ```
  ```console
  $ docker run -it --mount "type=bind,src=%cd%,target=/src" ubuntu bash
  ```
  ```console
  $ docker run -it --mount type=bind,src="/.",target=/src ubuntu bash
  ```
  ```console
  $ docker run -it --mount "type=bind,src=.,target=/src" ubuntu bash
  ```
  The `--mount type=bind` option tells Docker to create a bind mount, where `src` is the
  current working directory on your host machine (`getting-started-app`), and
  `target` is where that directory should appear inside the container (`/src`).
4. After running the command, Docker starts an interactive `bash` session in the
  root directory of the container's filesystem.
  ```console
  root@ac1237fad8db:/# pwd
  /
  root@ac1237fad8db:/# ls
  bin   dev  home  media  opt   root  sbin  srv  tmp  var
  boot  etc  lib   mnt    proc  run   src   sys  usr
  ```
5. Change directory to the `src` directory.
  This is the directory that you mounted when starting the container. Listing
  the contents of this directory displays the same files as in the
  `getting-started-app` directory on your host machine.
  ```console
  root@ac1237fad8db:/# cd src
  root@ac1237fad8db:/src# ls
  Dockerfile  node_modules  package.json  package-lock.json  spec  src
  ```
6. Create a new file named `myfile.txt`.
  ```console
  root@ac1237fad8db:/src# touch myfile.txt
  root@ac1237fad8db:/src# ls
  Dockerfile  myfile.txt  node_modules  package.json  package-lock.json  spec  src
  ```
7. Open the `getting-started-app` directory on the host and observe that the
  `myfile.txt` file is in the directory.
  ```text
  ├── getting-started-app/
  │ ├── Dockerfile
  │ ├── myfile.txt
  │ ├── node_modules/
  │ ├── package.json
  │ ├── package-lock.json
  │ ├── spec/
  │ └── src/
  ```
8. From the host, delete the `myfile.txt` file.
9. In the container, list the contents of the `app` directory once more. Observe that the file is now gone.
  ```console
  root@ac1237fad8db:/src# ls
  Dockerfile  node_modules  package.json  package-lock.json spec  src
  ```
10. Stop the interactive container session with `Ctrl` + `D`.

That's all for a brief introduction to bind mounts. This procedure
demonstrated how files are shared between the host and the container, and how
changes are immediately reflected on both sides. Now you can use
bind mounts to develop software.

## Development containers

Using bind mounts is common for local development setups. The advantage is that the development machine doesn’t need to have all of the build tools and environments installed. With a single docker run command, Docker pulls dependencies and tools.

### Run your app in a development container

The following steps describe how to run a development container with a bind
mount that does the following:

- Mount your source code into the container
- Install all dependencies
- Start `nodemon` to watch for filesystem changes

You can use the CLI or Docker Desktop to run your container with a bind mount.

1. Make sure you don't have any `getting-started` containers currently running.
2. Run the following command from the `getting-started-app` directory.
  ```console
  $ docker run -dp 127.0.0.1:3000:3000 \
      -w /app --mount type=bind,src=.,target=/app \
      node:24-alpine \
      sh -c "npm install && npm run dev"
  ```
  The following is a breakdown of the command:
  - `-dp 127.0.0.1:3000:3000` - same as before. Run in detached (background) mode and
    create a port mapping
  - `-w /app` - sets the "working directory" or the current directory that the
    command will run from
  - `--mount type=bind,src=.,target=/app` - bind mount the current
    directory from the host into the `/app` directory in the container
  - `node:24-alpine` - the image to use. Note that this is the base image for
    your app from the Dockerfile
  - `sh -c "npm install && npm run dev"` - the command. You're starting a
    shell using `sh` (alpine doesn't have `bash`) and running `npm install` to
    install packages and then running `npm run dev` to start the development
    server. If you look in the `package.json`, you'll see that the `dev` script
    starts `nodemon`.
3. You can watch the logs using `docker logs <container-id>`. You'll know you're
  ready to go when you see this:
  ```console
  $ docker logs -f <container-id>
  nodemon -L src/index.js
  [nodemon] 2.0.20
  [nodemon] to restart at any time, enter `rs`
  [nodemon] watching path(s): *.*
  [nodemon] watching extensions: js,mjs,json
  [nodemon] starting `node src/index.js`
  Using sqlite database at /etc/todos/todo.db
  Listening on port 3000
  ```
  When you're done watching the logs, exit out by hitting `Ctrl`+`C`.

1. Make sure you don't have any `getting-started` containers currently running.
2. Run the following command from the `getting-started-app` directory.
  ```powershell
  $ docker run -dp 127.0.0.1:3000:3000 `
      -w /app --mount "type=bind,src=.,target=/app" `
      node:24-alpine `
      sh -c "npm install && npm run dev"
  ```
  The following is a breakdown of the command:
  - `-dp 127.0.0.1:3000:3000` - same as before. Run in detached (background) mode and
    create a port mapping
  - `-w /app` - sets the "working directory" or the current directory that the
    command will run from
  - `--mount "type=bind,src=.,target=/app"` - bind mount the current
    directory from the host into the `/app` directory in the container
  - `node:24-alpine` - the image to use. Note that this is the base image for
    your app from the Dockerfile
  - `sh -c "npm install && npm run dev"` - the command. You're starting a
    shell using `sh` (alpine doesn't have `bash`) and running `npm install` to
    install packages and then running `npm run dev` to start the development
    server. If you look in the `package.json`, you'll see that the `dev` script
    starts `nodemon`.
3. You can watch the logs using `docker logs <container-id>`. You'll know you're
  ready to go when you see this:
  ```console
  $ docker logs -f <container-id>
  nodemon -L src/index.js
  [nodemon] 2.0.20
  [nodemon] to restart at any time, enter `rs`
  [nodemon] watching path(s): *.*
  [nodemon] watching extensions: js,mjs,json
  [nodemon] starting `node src/index.js`
  Using sqlite database at /etc/todos/todo.db
  Listening on port 3000
  ```
  When you're done watching the logs, exit out by hitting `Ctrl`+`C`.

1. Make sure you don't have any `getting-started` containers currently running.
2. Run the following command from the `getting-started-app` directory.
  ```console
  $ docker run -dp 127.0.0.1:3000:3000 ^
      -w /app --mount "type=bind,src=%cd%,target=/app" ^
      node:24-alpine ^
      sh -c "npm install && npm run dev"
  ```
  The following is a breakdown of the command:
  - `-dp 127.0.0.1:3000:3000` - same as before. Run in detached (background) mode and
    create a port mapping
  - `-w /app` - sets the "working directory" or the current directory that the
    command will run from
  - `--mount "type=bind,src=%cd%,target=/app"` - bind mount the current
    directory from the host into the `/app` directory in the container
  - `node:24-alpine` - the image to use. Note that this is the base image for
    your app from the Dockerfile
  - `sh -c "npm install && npm run dev"` - the command. You're starting a
    shell using `sh` (alpine doesn't have `bash`) and running `npm install` to
    install packages and then running `npm run dev` to start the development
    server. If you look in the `package.json`, you'll see that the `dev` script
    starts `nodemon`.
3. You can watch the logs using `docker logs <container-id>`. You'll know you're
  ready to go when you see this:
  ```console
  $ docker logs -f <container-id>
  nodemon -L src/index.js
  [nodemon] 2.0.20
  [nodemon] to restart at any time, enter `rs`
  [nodemon] watching path(s): *.*
  [nodemon] watching extensions: js,mjs,json
  [nodemon] starting `node src/index.js`
  Using sqlite database at /etc/todos/todo.db
  Listening on port 3000
  ```
  When you're done watching the logs, exit out by hitting `Ctrl`+`C`.

1. Make sure you don't have any `getting-started` containers currently running.
2. Run the following command from the `getting-started-app` directory.
  ```console
  $ docker run -dp 127.0.0.1:3000:3000 \
      -w //app --mount type=bind,src="/.",target=/app \
      node:24-alpine \
      sh -c "npm install && npm run dev"
  ```
  The following is a breakdown of the command:
  - `-dp 127.0.0.1:3000:3000` - same as before. Run in detached (background) mode and
    create a port mapping
  - `-w //app` - sets the "working directory" or the current directory that the
    command will run from
  - `--mount type=bind,src="/.",target=/app` - bind mount the current
    directory from the host into the `/app` directory in the container
  - `node:24-alpine` - the image to use. Note that this is the base image for
    your app from the Dockerfile
  - `sh -c "npm install && npm run dev"` - the command. You're starting a
    shell using `sh` (alpine doesn't have `bash`) and running `npm install` to
    install packages and then running `npm run dev` to start the development
    server. If you look in the `package.json`, you'll see that the `dev` script
    starts `nodemon`.
3. You can watch the logs using `docker logs <container-id>`. You'll know you're
  ready to go when you see this:
  ```console
  $ docker logs -f <container-id>
  nodemon -L src/index.js
  [nodemon] 2.0.20
  [nodemon] to restart at any time, enter `rs`
  [nodemon] watching path(s): *.*
  [nodemon] watching extensions: js,mjs,json
  [nodemon] starting `node src/index.js`
  Using sqlite database at /etc/todos/todo.db
  Listening on port 3000
  ```
  When you're done watching the logs, exit out by hitting `Ctrl`+`C`.

Make sure you don't have any `getting-started` containers currently running.

Run the image with a bind mount.

1. Select the search box at the top of Docker Desktop.
2. In the search window, select the **Images** tab.
3. In the search box, specify the container name, `getting-started`.
  > Tip
  >
  > Use the search filter to filter images and only show **Local images**.
4. Select your image and then select **Run**.
5. Select **Optional settings**.
6. In **Host path**, specify the path to the `getting-started-app` directory on your host machine.
7. In **Container path**, specify `/app`.
8. Select **Run**.

You can watch the container logs using Docker Desktop.

1. Select **Containers** in Docker Desktop.
2. Select your container name.

You'll know you're ready to go when you see this:

```console
nodemon -L src/index.js
[nodemon] 2.0.20
[nodemon] to restart at any time, enter `rs`
[nodemon] watching path(s): *.*
[nodemon] watching extensions: js,mjs,json
[nodemon] starting `node src/index.js`
Using sqlite database at /etc/todos/todo.db
Listening on port 3000
```

### Develop your app with the development container

Update your app on your host machine and see the changes reflected in the container.

1. In the `src/static/js/app.js` file, on line
  109, change the "Add Item" button to simply say "Add":
  ```diff
  - {submitting ? 'Adding...' : 'Add Item'}
  + {submitting ? 'Adding...' : 'Add'}
  ```
  Save the file.
2. Refresh the page in your web browser, and you should see the change reflected
  almost immediately because of the bind mount. Nodemon detects the change and
  restarts the server. It might take a few seconds for the Node server to
  restart. If you get an error, try refreshing after a few seconds.
  ![Screenshot of updated label for Add button](https://docs.docker.com/get-started/workshop/images/updated-add-button.webp)  ![Screenshot of updated label for Add button](https://docs.docker.com/get-started/workshop/images/updated-add-button.webp)
3. Feel free to make any other changes you'd like to make. Each time you make a
  change and save a file, the change is reflected in the container because of
  the bind mount. When Nodemon detects a change, it restarts the app inside the
  container automatically. When you're done, stop the container and build your
  new image using:
  ```console
  $ docker build -t getting-started .
  ```

## Summary

At this point, you can persist your database and see changes in your app as you develop without rebuilding the image.

In addition to volume mounts and bind mounts, Docker also supports other mount
types and storage drivers for handling more complex and specialized use cases.

Related information:

- [docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Manage data in Docker](https://docs.docker.com/storage/)

## Next steps

In order to prepare your app for production, you need to migrate your database
from working in SQLite to something that can scale a little better. For
simplicity, you'll keep using a relational database and switch your application
to use MySQL. But, how should you run MySQL? How do you allow the containers to
talk to each other? You'll learn about that in the next section.

[Multi container apps](https://docs.docker.com/get-started/workshop/07_multi_container/)

---

# Multi container apps

> Using more than one container in your application

# Multi container apps

   Table of contents

---

Up to this point, you've been working with single container apps. But, now you will add MySQL to the
application stack. The following question often arises - "Where will MySQL run? Install it in the same
container or run it separately?" In general, each container should do one thing and do it well. The following are a few reasons to run the container separately:

- There's a good chance you'd have to scale APIs and front-ends differently than databases.
- Separate containers let you version and update versions in isolation.
- While you may use a container for the database locally, you may want to use a managed service
  for the database in production. You don't want to ship your database engine with your app then.
- Running multiple processes will require a process manager (the container only starts one process), which adds complexity to container startup/shutdown.

And there are more reasons. So, like the following diagram, it's best to run your app in multiple containers.

![Todo App connected to MySQL container](https://docs.docker.com/get-started/workshop/images/multi-container.webp)  ![Todo App connected to MySQL container](https://docs.docker.com/get-started/workshop/images/multi-container.webp)

## Container networking

Remember that containers, by default, run in isolation and don't know anything about other processes
or containers on the same machine. So, how do you allow one container to talk to another? The answer is
networking. If you place the two containers on the same network, they can talk to each other.

## Start MySQL

There are two ways to put a container on a network:

- Assign the network when starting the container.
- Connect an already running container to a network.

In the following steps, you'll create the network first and then attach the MySQL container at startup.

1. Create the network.
  ```console
  $ docker network create todo-app
  ```
2. Start a MySQL container and attach it to the network. You're also going to define a few environment variables that the
  database will use to initialize the database. To learn more about the MySQL environment variables, see the "Environment Variables" section in the [MySQL Docker Hub listing](https://hub.docker.com/_/mysql/).
  ```console
  $ docker run -d \
      --network todo-app --network-alias mysql \
      -v todo-mysql-data:/var/lib/mysql \
      -e MYSQL_ROOT_PASSWORD=secret \
      -e MYSQL_DATABASE=todos \
      mysql:8.0
  ```
  ```powershell
  $ docker run -d `
      --network todo-app --network-alias mysql `
      -v todo-mysql-data:/var/lib/mysql `
      -e MYSQL_ROOT_PASSWORD=secret `
      -e MYSQL_DATABASE=todos `
      mysql:8.0
  ```
  ```console
  $ docker run -d ^
      --network todo-app --network-alias mysql ^
      -v todo-mysql-data:/var/lib/mysql ^
      -e MYSQL_ROOT_PASSWORD=secret ^
      -e MYSQL_DATABASE=todos ^
      mysql:8.0
  ```
  In the previous command, you can see the `--network-alias` flag. In a later section, you'll learn more about this flag.
  > Tip
  >
  > You'll notice a volume named `todo-mysql-data` in the above command that is mounted at `/var/lib/mysql`, which is where MySQL stores its data. However, you never ran a `docker volume create` command. Docker recognizes you want to use a named volume and creates one automatically for you.
3. To confirm you have the database up and running, connect to the database and verify that it connects.
  ```console
  $ docker exec -it <mysql-container-id> mysql -u root -p
  ```
  When the password prompt comes up, type in `secret`. In the MySQL shell, list the databases and verify
  you see the `todos` database.
  ```console
  mysql> SHOW DATABASES;
  ```
  You should see output that looks like this:
  ```plaintext
  +--------------------+
  | Database           |
  +--------------------+
  | information_schema |
  | mysql              |
  | performance_schema |
  | sys                |
  | todos              |
  +--------------------+
  5 rows in set (0.00 sec)
  ```
4. Exit the MySQL shell to return to the shell on your machine.
  ```console
  mysql> exit
  ```
  You now have a `todos` database and it's ready for you to use.

## Connect to MySQL

Now that you know MySQL is up and running, you can use it. But, how do you use it? If you run
another container on the same network, how do you find the container? Remember that each container has its own IP address.

To answer the questions above and better understand container networking, you're going to make use of the [nicolaka/netshoot](https://github.com/nicolaka/netshoot) container,
which ships with a lot of tools that are useful for troubleshooting or debugging networking issues.

1. Start a new container using the nicolaka/netshoot image. Make sure to connect it to the same network.
  ```console
  $ docker run -it --network todo-app nicolaka/netshoot
  ```
2. Inside the container, you're going to use the `dig` command, which is a useful DNS tool. You're going to look up
  the IP address for the hostname `mysql`.
  ```console
  $ dig mysql
  ```
  You should get output like the following.
  ```text
  ; <<>> DiG 9.18.8 <<>> mysql
  ;; global options: +cmd
  ;; Got answer:
  ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32162
  ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
  ;; QUESTION SECTION:
  ;mysql.				IN	A
  ;; ANSWER SECTION:
  mysql.			600	IN	A	172.23.0.2
  ;; Query time: 0 msec
  ;; SERVER: 127.0.0.11#53(127.0.0.11)
  ;; WHEN: Tue Oct 01 23:47:24 UTC 2019
  ;; MSG SIZE  rcvd: 44
  ```
  In the "ANSWER SECTION", you will see an `A` record for `mysql` that resolves to `172.23.0.2`
  (your IP address will most likely have a different value). While `mysql` isn't normally a valid hostname,
  Docker was able to resolve it to the IP address of the container that had that network alias. Remember, you used the
  `--network-alias` earlier.
  What this means is that your app only simply needs to connect to a host named `mysql` and it'll talk to the
  database.

## Run your app with MySQL

The todo app supports the setting of a few environment variables to specify MySQL connection settings. They are:

- `MYSQL_HOST` - the hostname for the running MySQL server
- `MYSQL_USER` - the username to use for the connection
- `MYSQL_PASSWORD` - the password to use for the connection
- `MYSQL_DB` - the database to use once connected

> Note
>
> While using env vars to set connection settings is generally accepted for development, it's highly discouraged
> when running applications in production. Diogo Monica, a former lead of security at Docker,
> [wrote a fantastic blog post](https://blog.diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/)
> explaining why.
>
>
>
> A more secure mechanism is to use the secret support provided by your container orchestration framework. In most cases,
> these secrets are mounted as files in the running container. You'll see many apps (including the MySQL image and the todo app)
> also support env vars with a `_FILE` suffix to point to a file containing the variable.
>
>
>
> As an example, setting the `MYSQL_PASSWORD_FILE` var will cause the app to use the contents of the referenced file
> as the connection password. Docker doesn't do anything to support these env vars. Your app will need to know to look for
> the variable and get the file contents.

You can now start your dev-ready container.

1. Specify each of the previous environment variables, as well as connect the container to your app network. Make sure that you are in the `getting-started-app` directory when you run this command.
  ```console
  $ docker run -dp 127.0.0.1:3000:3000 \
    -w /app -v ".:/app" \
    --network todo-app \
    -e MYSQL_HOST=mysql \
    -e MYSQL_USER=root \
    -e MYSQL_PASSWORD=secret \
    -e MYSQL_DB=todos \
    node:24-alpine \
    sh -c "npm install && npm run dev"
  ```
  In Windows, run this command in PowerShell.
  ```powershell
  $ docker run -dp 127.0.0.1:3000:3000 `
    -w /app -v ".:/app" `
    --network todo-app `
    -e MYSQL_HOST=mysql `
    -e MYSQL_USER=root `
    -e MYSQL_PASSWORD=secret `
    -e MYSQL_DB=todos `
    node:24-alpine `
    sh -c "npm install && npm run dev"
  ```
  In Windows, run this command in Command Prompt.
  ```console
  $ docker run -dp 127.0.0.1:3000:3000 ^
    -w /app -v "%cd%:/app" ^
    --network todo-app ^
    -e MYSQL_HOST=mysql ^
    -e MYSQL_USER=root ^
    -e MYSQL_PASSWORD=secret ^
    -e MYSQL_DB=todos ^
    node:24-alpine ^
    sh -c "npm install && npm run dev"
  ```
  ```console
  $ docker run -dp 127.0.0.1:3000:3000 \
    -w //app -v "/.:/app" \
    --network todo-app \
    -e MYSQL_HOST=mysql \
    -e MYSQL_USER=root \
    -e MYSQL_PASSWORD=secret \
    -e MYSQL_DB=todos \
    node:24-alpine \
    sh -c "npm install && npm run dev"
  ```
2. If you look at the logs for the container (`docker logs -f <container-id>`), you should see a message similar to the following, which indicates it's
  using the mysql database.
  ```console
  [nodemon] 3.1.11
  [nodemon] to restart at any time, enter `rs`
  [nodemon] watching path(s): *.*
  [nodemon] watching extensions: js,mjs,cjs,json
  [nodemon] starting `node src/index.js`
  Waiting for mysql:3306.
  Connected!
  Connected to mysql db at host mysql
  Listening on port 3000
  ```
3. Open the app in your browser and add a few items to your todo list.
4. Connect to the mysql database and prove that the items are being written to the database. Remember, the password
  is `secret`.
  ```console
  $ docker exec -it <mysql-container-id> mysql -p todos
  ```
  And in the mysql shell, run the following:
  ```console
  mysql> select * from todo_items;
  +--------------------------------------+--------------------+-----------+
  | id                                   | name               | completed |
  +--------------------------------------+--------------------+-----------+
  | c906ff08-60e6-44e6-8f49-ed56a0853e85 | Do amazing things! |         0 |
  | 2912a79e-8486-4bc3-a4c5-460793a575ab | Be awesome!        |         0 |
  +--------------------------------------+--------------------+-----------+
  ```
  Your table will look different because it has your items. But, you should see them stored there.

## Summary

At this point, you have an application that now stores its data in an external database running in a separate
container. You learned a little bit about container networking and service discovery using DNS.

Related information:

- [docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Networking overview](https://docs.docker.com/engine/network/)

## Next steps

There's a good chance you are starting to feel a little overwhelmed with everything you need to do to start up
this application. You have to create a network, start containers, specify all of the environment variables, expose
ports, and more. That's a lot to remember and it's certainly making things harder to pass along to someone else.

In the next section, you'll learn about Docker Compose. With Docker Compose, you can share your application stacks in a
much easier way and let others spin them up with a single, simple command.

[Use Docker Compose](https://docs.docker.com/get-started/workshop/08_using_compose/)

---

# Use Docker Compose

> Using Docker Compose for multi-container applications

# Use Docker Compose

   Table of contents

---

[Docker Compose](https://docs.docker.com/compose/) is a tool that helps you define and
share multi-container applications. With Compose, you can create a YAML file to define the services
and with a single command, you can spin everything up or tear it all down.

The big advantage of using Compose is you can define your application stack in a file, keep it at the root of
your project repository (it's now version controlled), and easily enable someone else to contribute to your project.
Someone would only need to clone your repository and start the app using Compose. In fact, you might see quite a few projects
on GitHub/GitLab doing exactly this now.

## Create the Compose file

In the `getting-started-app` directory, create a file named `compose.yaml`.

```text
├── getting-started-app/
│ ├── Dockerfile
│ ├── compose.yaml
│ ├── node_modules/
│ ├── package.json
│ ├── package-lock.json
│ ├── spec/
│ └── src/
```

## Define the app service

In [part 6](https://docs.docker.com/get-started/workshop/07_multi_container/), you used the following command to start the application service.

```console
$ docker run -dp 127.0.0.1:3000:3000 \
  -w /app -v ".:/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  node:24-alpine \
  sh -c "npm install && npm run dev"
```

You'll now define this service in the `compose.yaml` file.

1. Open `compose.yaml` in a text or code editor, and start by defining the name and image of the first service (or container) you want to run as part of your application.
  The name will automatically become a network alias, which will be useful when defining your MySQL service.
  ```yaml
  services:
    app:
      image: node:24-alpine
  ```
2. Typically, you will see `command` close to the `image` definition, although there is no requirement on ordering. Add the `command` to your `compose.yaml` file.
  ```yaml
  services:
    app:
      image: node:24-alpine
      command: sh -c "npm install && npm run dev"
  ```
3. Now migrate the `-p 127.0.0.1:3000:3000` part of the command by defining the `ports` for the service.
  ```yaml
  services:
    app:
      image: node:24-alpine
      command: sh -c "npm install && npm run dev"
      ports:
        - 127.0.0.1:3000:3000
  ```
4. Next, migrate both the working directory (`-w /app`) and the volume mapping
  (`-v ".:/app"`) by using the `working_dir` and `volumes` definitions.
  One advantage of Docker Compose volume definitions is you can use relative paths from the current directory.
  ```yaml
  services:
    app:
      image: node:24-alpine
      command: sh -c "npm install && npm run dev"
      ports:
        - 127.0.0.1:3000:3000
      working_dir: /app
      volumes:
        - ./:/app
  ```
5. Finally, you need to migrate the environment variable definitions using the `environment` key.
  ```yaml
  services:
    app:
      image: node:24-alpine
      command: sh -c "npm install && npm run dev"
      ports:
        - 127.0.0.1:3000:3000
      working_dir: /app
      volumes:
        - ./:/app
      environment:
        MYSQL_HOST: mysql
        MYSQL_USER: root
        MYSQL_PASSWORD: secret
        MYSQL_DB: todos
  ```

### Define the MySQL service

Now, it's time to define the MySQL service. The command that you used for that container was the following:

```console
$ docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

1. First define the new service and name it `mysql` so it automatically gets the network alias. Also specify the image to use as well.
  ```yaml
  services:
    app:
      # The app service definition
    mysql:
      image: mysql:8.0
  ```
2. Next, define the volume mapping. When you ran the container with `docker run`, Docker created the named volume automatically. However, that doesn't
  happen when running with Compose. You need to define the volume in the
  top-level `volumes:` section and then specify the mountpoint in the service
  config. By simply providing only the volume name, the default options are
  used.
  ```yaml
  services:
    app:
      # The app service definition
    mysql:
      image: mysql:8.0
      volumes:
        - todo-mysql-data:/var/lib/mysql
  volumes:
    todo-mysql-data:
  ```
3. Finally, you need to specify the environment variables.
  ```yaml
  services:
    app:
      # The app service definition
    mysql:
      image: mysql:8.0
      volumes:
        - todo-mysql-data:/var/lib/mysql
      environment:
        MYSQL_ROOT_PASSWORD: secret
        MYSQL_DATABASE: todos
  volumes:
    todo-mysql-data:
  ```

At this point, your complete `compose.yaml` should look like this:

```yaml
services:
  app:
    image: node:24-alpine
    command: sh -c "npm install && npm run dev"
    ports:
      - 127.0.0.1:3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```

## Run the application stack

Now that you have your `compose.yaml` file, you can start your application.

1. Make sure no other copies of the containers are running first. Use `docker ps` to list the containers and `docker rm -f <ids>` to remove them.
2. Start up the application stack using the `docker compose up` command. Add the
  `-d` flag to run everything in the background.
  ```console
  $ docker compose up -d
  ```
  When you run the previous command, you should see output like the following:
  ```plaintext
  Creating network "app_default" with the default driver
  Creating volume "app_todo-mysql-data" with default driver
  Creating app_app_1   ... done
  Creating app_mysql_1 ... done
  ```
  You'll notice that Docker Compose created the volume as well as a network. By default, Docker Compose automatically creates a network specifically for the application stack (which is why you didn't define one in the Compose file).
3. Look at the logs using the `docker compose logs -f` command. You'll see the logs from each of the services interleaved
  into a single stream. This is incredibly useful when you want to watch for timing-related issues. The `-f` flag follows the
  log, so will give you live output as it's generated.
  If you have run the command already, you'll see output that looks like this:
  ```plaintext
  mysql_1  | 2019-10-03T03:07:16.083639Z 0 [Note] mysqld: ready for connections.
  mysql_1  | Version: '8.0.31'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
  app_1    | Connected to mysql db at host mysql
  app_1    | Listening on port 3000
  ```
  The service name is displayed at the beginning of the line (often colored) to help distinguish messages. If you want to
  view the logs for a specific service, you can add the service name to the end of the logs command (for example,
  `docker compose logs -f app`).
4. At this point, you should be able to open your app in your browser on [http://localhost:3000](http://localhost:3000) and see it running.

## See the app stack in Docker Desktop Dashboard

If you look at the Docker Desktop Dashboard, you'll see that there is a group named **getting-started-app**. This is the project name from Docker
Compose and used to group the containers together. By default, the project name is simply the name of the directory that the
`compose.yaml` was located in.

If you expand the stack, you'll see the two containers you defined in the Compose file. The names are also a little
more descriptive, as they follow the pattern of `<service-name>-<replica-number>`. So, it's very easy to
quickly see what container is your app and which container is the mysql database.

## Tear it all down

When you're ready to tear it all down, simply run `docker compose down` or hit the trash can on the Docker Desktop Dashboard
for the entire app. The containers will stop and the network will be removed.

> Warning
>
> By default, named volumes in your compose file are not removed when you run `docker compose down`. If you want to
> remove the volumes, you need to add the `--volumes` flag.
>
>
>
> The Docker Desktop Dashboard does not remove volumes when you delete the app stack.

## Summary

In this section, you learned about Docker Compose and how it helps you simplify
the way you define and share multi-service applications.

Related information:

- [Compose overview](https://docs.docker.com/compose/)
- [Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Compose CLI reference](https://docs.docker.com/reference/cli/docker/compose/)

## Next steps

Next, you'll learn about a few best practices you can use to improve your Dockerfile.

[Image-building best practices](https://docs.docker.com/get-started/workshop/09_image_best/)
