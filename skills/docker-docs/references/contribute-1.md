# Writing checklist and more

# Writing checklist

> A helpful writing checklist when creating documentation

# Writing checklist

   Table of contents

---

Use this checklist to communicate in a way that is clear, helpful, and consistent with the rest of Docker Docs.

##### Used active voice

Active voice is specific and removes ambiguity.

In active voice, the subject of the sentence (the customer or the system) does the action.

Sentences that use active voice are easier to read. Active voice makes it clear who has done what and to whom. Plus, active voice keeps sentences direct and more concise.

Helping verbs such as is, was, or would may indicate that you're writing in passive voice. And, if you can add the phrase 'by zombies' after the verb, you're writing in the passive voice.

| Correct | Incorrect |
| --- | --- |
| Increase productivity with Docker Desktop. | Productivity can be increased (by zombies) with Docker Desktop. |
| If you remove items from a grid, charts automatically refresh to display the change. | If items are removed (by zombies) from a grid, charts automatically refresh to display the change. |

##### Written clear sentences that get to the point

Write short, concise sentences. Punchy sentences are faster to read and easier to understand.

##### Used subheadings and bulleted lists to break up the page

This helps find the information they need quickly and easily.

For more information, see the [formatting](https://docs.docker.com/contribute/style/formatting/#headings-and-subheadings) page, or see the [components](https://docs.docker.com/contribute/components/lists/) for examples.

##### Started the title of your page with a verb

For example, 'Install Docker Desktop'.

##### Checked that the left-hand table of contents title in docs.docker.com, matches the title displayed on the page

##### Checked for broken links and images

Use relative links to link to other pages or images within the GitHub repository.

For more information, see the [formatting](https://docs.docker.com/contribute/style/formatting/#links) page, or see the [components](https://docs.docker.com/contribute/components/links/) for examples.

##### Checked that any redirects you may have added, work

For information on how to add redirects, see [Source file conventions](https://docs.docker.com/contribute/file-conventions/#front-matter).

##### Used bold on any UI elements you refer to in your content

##### Completed a final spelling, punctuation, and grammar check

For more in-depth information on our Style Guide, explore the [grammar](https://docs.docker.com/contribute/style/grammar/) or [formatting](https://docs.docker.com/contribute/style/formatting/) guides.

---

# Accordions

> components and formatting examples used in Docker's docs

# Accordions

   Table of contents

---

## Example

```console
$ docker run hello-world
```

## Markup

```markdown
{{< accordion title="Accordion example" >}}

```console
$ docker run hello-world
```

{{< /accordion >}}
```

---

# Badges

> components and formatting examples used in Docker's docs

# Badges

   Table of contents

---

### Examples

blue badge
amber badge
red badge
green badge
violet badge
gray badge

You can also make a badge a link.

[badge with a link](https://docs.docker.com/contribute/)

### Usage guidelines

Use badges to indicate new content and product content in various stages of the release lifecycle:

- The violet badge to highlight new early access or experimental content
- The blue badge to highlight beta content
- The green badge to highlight new content that is either GA or not product-related content, such as guides/learning paths
- The gray badge to highlight deprecated content

Best practice is to use this badge for no longer than 2 months post release of the feature.

### Markup

Inline badge:

```go
{{< badge color=amber text="amber badge" >}}
[{{< badge color="blue" text="badge with a link" >}}](../overview.md)
```

Sidebar badge in frontmatter:

```yaml
---
title: Page title
params:
  sidebar:
    badge:
      color: gray
      text: Deprecated
---
```

---

# Buttons

> components and formatting examples used in Docker's docs

# Buttons

   Table of contents

---

### Examples

[hello](https://example.com/)

### Markup

```go
{{< button url="https://example.com/" text="hello" >}}
```

---

# Callouts

> components and formatting examples used in Docker's docs

# Callouts

   Table of contents

---

We support these broad categories of callouts:

- Alerts: Note, Tip, Important, Warning, Caution

We also support summary bars, which represent a feature's required subscription, version, or Adminstrator role.
To add a summary bar:

Add the feature name to the `/data/summary.yaml` file. Use the following attributes:

| Attribute | Description | Possible values |
| --- | --- | --- |
| subscription | Notes the subscription required to use the feature | All, Personal, Pro, Team, Business |
| availability | Notes what product development stage the feature is in | Experimental, Beta, Early Access, GA, Retired |
| requires | Notes what minimum version is required for the feature | No specific value, use a string to describe the version and link to relevant release notes |
| for | Notes if the feature is intended for IT Administrators | Administrators |

Then, add the `summary-bar` shortcode on the page you want to add the summary bar to. Note, the feature name is case sensitive. The icons that appear in the summary bar are automatically rendered.

## Examples

Subscription: Business Requires: Docker Desktop
[4.36](https://docs.docker.com/desktop/release-notes/#4360) and later For: Administrators

> Note
>
> Note the way the `get_hit_count` function is written. This basic retry
> loop lets us attempt our request multiple times if the redis service is
> not available. This is useful at startup while the application comes
> online, but also makes our application more resilient if the Redis
> service needs to be restarted anytime during the app's lifetime. In a
> cluster, this also helps handling momentary connection drops between
> nodes.

> Tip
>
> For a smaller base image, use `alpine`.

> Important
>
> Treat access tokens like your password and keep them secret. Store your
> tokens securely (for example, in a credential manager).

> Warning
>
> Removing Volumes
>
>
>
> By default, named volumes in your compose file are NOT removed when running
> `docker compose down`. If you want to remove the volumes, you will need to add
> the `--volumes` flag.
>
>
>
> The Docker Desktop Dashboard does not remove volumes when you delete the app stack.

> Caution
>
> Here be dragons.

For both of the following callouts, consult
[the Docker release lifecycle](https://docs.docker.com/release-lifecycle) for more information on when to use them.

## Formatting

```md
{{< summary-bar feature_name="PKG installer" >}}
```

```html
> [!NOTE]
>
> Note the way the `get_hit_count` function is written. This basic retry
> loop lets us attempt our request multiple times if the redis service is
> not available. This is useful at startup while the application comes
> online, but also makes our application more resilient if the Redis
> service needs to be restarted anytime during the app's lifetime. In a
> cluster, this also helps handling momentary connection drops between
> nodes.

> [!TIP]
>
> For a smaller base image, use `alpine`.

> [!IMPORTANT]
>
> Treat access tokens like your password and keep them secret. Store your
> tokens securely (for example, in a credential manager).

> [!WARNING]
>
> Removing Volumes
>
> By default, named volumes in your compose file are NOT removed when running
> `docker compose down`. If you want to remove the volumes, you will need to add
> the `--volumes` flag.
>
> The Docker Desktop Dashboard does not remove volumes when you delete the app stack.

> [!CAUTION]
>
> Here be dragons.
```

---

# Cards

> components and formatting examples used in Docker's docs

# Cards

   Table of contents

---

Cards can be added to a page using the `card` shortcode.
The parameters for this shortcode are:

| Parameter | Description |
| --- | --- |
| title | The title of the card |
| icon | The icon slug of the card |
| image | Use a custom image instead of an icon (mutually exclusive with icon) |
| link | (Optional) The link target of the card, when clicked |
| description | A description text, in Markdown |

> Note
>
> There's a known limitation with the Markdown description of cards,
> in that they can't contain relative links, pointing to other .md documents.
> Such links won't render correctly. Instead, use an absolute link to the URL
> path of the page that you want to link to.
>
>
>
> For example, instead of linking to `../install/linux.md`, write:
> `/engine/install/linux/`.

## Example

[Get your Docker onBuild, share, and run your apps with Docker](https://docs.docker.com/)

## Markup

```go
{{< card
  title="Get your Docker on"
  icon=favorite
  link=https://docs.docker.com/
  description="Build, share, and run your apps with Docker"
>}}
```

### Grid

There's also a built-in `grid` shortcode that generates a... well, grid... of cards.
The grid size is 3x3 on large screens, 2x2 on medium, and single column on small.

[Docker DesktopDocker on your Desktop.](https://docs.docker.com/desktop/)[Docker EngineVrrrrooooommm](https://docs.docker.com/engine/)[Docker BuildClang bang](https://docs.docker.com/build/)[Docker ComposeFiggy!](https://docs.docker.com/compose/)[Docker Hubso much content, oh wow](https://docs.docker.com/docker-hub/)

Grid is a separate shortcode from `card`, but it implements the same component under the hood.
The markup you use to insert a grid is slightly unconventional. The grid shortcode takes no arguments.
All it does is let you specify where on a page you want your grid to appear.

```go
{{< grid >}}
```

The data for the grid is defined in the front matter of the page, under the `grid` key, as follows:

```yaml
# front matter section of a page
title: some page
grid:
  - title: "Docker Engine"
    description: Vrrrrooooommm
    icon: "developer_board"
    link: "/engine/"
  - title: "Docker Build"
    description: Clang bang
    icon: "build"
    link: "/build/"
```

---

# Code blocks

> components and formatting examples used in Docker's docs

# Code blocks

   Table of contents

---

Rouge provides lots of different code block "hints". If you leave off the hint,
it tries to guess and sometimes gets it wrong. These are just a few hints that
we use often.

## Variables

If your example contains a placeholder value that's subject to change,
use the format `<[A-Z_]+>` for the placeholder value: `<MY_VARIABLE>`

```text
export name=MY_NAME
```

This syntax is reserved for variable names, and will cause the variable to
be rendered in a special color and font style.

## Highlight lines

```text
incoming := map[string]interface{}{
    "asdf": 1,
    "qwer": []interface{}{},
    "zxcv": []interface{}{
        map[string]interface{}{},
        true,
        int(1e9),
        "tyui",
    },
}
```

```markdown
```go {hl_lines=[7,8]}
incoming := map[string]interface{}{
    "asdf": 1,
    "qwer": []interface{}{},
    "zxcv": []interface{}{
        map[string]interface{}{},
        true,
        int(1e9),
        "tyui",
    },
}
```
```

## Collapsible code blocks

```dockerfile
# syntax=docker/dockerfile:1

ARG GO_VERSION="1.21"

FROM golang:${GO_VERSION}-alpine AS base
ENV CGO_ENABLED=0
ENV GOPRIVATE="github.com/foo/*"
RUN apk add --no-cache file git rsync openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR /src

FROM base AS vendor
# this step configure git and checks the ssh key is loaded
RUN --mount=type=ssh <<EOT
  set -e
  echo "Setting Git SSH protocol"
  git config --global url."git@github.com:".insteadOf "https://github.com/"
  (
    set +e
    ssh -T git@github.com
    if [ ! "$?" = "1" ]; then
      echo "No GitHub SSH key loaded exiting..."
      exit 1
    fi
  )
EOT
# this one download go modules
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=ssh \
    go mod download -x

FROM vendor AS build
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache \
    go build ...
```

## Bash

Use the `bash` language code block when you want to show a Bash script:

```bash
#!/usr/bin/bash
echo "deb https://download.docker.com/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

If you want to show an interactive shell, use `console` instead.
In cases where you use `console`, make sure to add a dollar character
for the user sign:

```console
$ echo "deb https://download.docker.com/linux/ubuntu noble stable" | sudo tee /etc/apt/sources.list.d/docker.list
```

## Go

```go
incoming := map[string]interface{}{
    "asdf": 1,
    "qwer": []interface{}{},
    "zxcv": []interface{}{
        map[string]interface{}{},
        true,
        int(1e9),
        "tyui",
    },
}
```

## PowerShell

```powershell
Install-Module DockerMsftProvider -Force
Install-Package Docker -ProviderName DockerMsftProvider -Force
[System.Environment]::SetEnvironmentVariable("DOCKER_FIPS", "1", "Machine")
Expand-Archive docker-18.09.1.zip -DestinationPath $Env:ProgramFiles -Force
```

## Python

```python
return html.format(name=os.getenv('NAME', "world"), hostname=socket.gethostname(), visits=visits)
```

## Ruby

```ruby
docker_service 'default' do
  action [:create, :start]
end
```

## JSON

```json
"server": {
  "http_addr": ":4443",
  "tls_key_file": "./fixtures/notary-server.key",
  "tls_cert_file": "./fixtures/notary-server.crt"
}
```

#### HTML

```html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
</head>
</html>
```

## Markdown

```markdown
# Hello
```

If you want to include a triple-fenced code block inside your code block,
you can wrap your block in a quadruple-fenced code block:

```markdown
````markdown
# Hello

```go
log.Println("did something")
```
````
```

## ini

```ini
[supervisord]
nodaemon=true

[program:sshd]
command=/usr/sbin/sshd -D
```

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM ubuntu

RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]
```

## YAML

```yaml
authorizedkeys:
  image: dockercloud/authorizedkeys
  deployment_strategy: every_node
  autodestroy: always
  environment:
    - AUTHORIZED_KEYS=ssh-rsa AAAAB3Nsomelongsshkeystringhereu9UzQbVKy9o00NqXa5jkmZ9Yd0BJBjFmb3WwUR8sJWZVTPFL
  volumes:
    /root:/user:rw
```

---

# Icons

> Icons used across docs

# Icons

---

Below is an inventory of the icons we use to represent different topics or features across docs. To be used with the [cards component](https://docs.docker.com/contribute/components/cards/).

### Install

Icon name = download

### FAQs

Icon name = help

### Onboarding/quickstarts

Icon name = explore

### Release notes

Icon name = note_add

### Feedback

Icon name = sms

### Multi-platform/arch

Icon name = content_copy

### Rootless/ECI

Icon name = security

### Settings management

Icon name = shield_lock

### Processes

Icon name = checklist

### Networking

Icon name = network_node

### Exploring a feature

Icon name = feature_search

### Company

Icon name = apartment

### Organization

Icon name = store

### Additional resources

Icon name = category

### Designing

Icon name = design_services

### Publishing

Icon name = publish

### Interacting

Icon name = multiple_stop

### Storage

Icon name = database

### logs

Icon name = text_snippet

### Prune/cut

Icon name = content_cut

### Configure

Icon name = tune

### Deprecated

Icon name = folder_delete

### RAM

Icon name = home_storage

### IAM

Icon name = photo_library

### Packaging

Icon name = inventory_2

### Multi-stage

Icon name = stairs

### Architecture

Icon name = construction

### Build drivers

Icon name = engineering

### Export

Icon name = output

### Cache

Icon name = cycle

### Bake

Icon name = cake

### Docker ID

Icon name = fingerprint

### Repository

Icon name = inbox

### Access tokens

Icon name = password

### official images

Icon name = verified

### Hardened Docker Desktop

Icon name = lock

### Sign in

Icon name = passkey

### SSO and SCIM

Icon name = key

### 2FA

Icon name = phonelink_lock

### Add/update payment method

Icon name = credit_score

### Update billing info

Icon name = contract_edit

### Billing history

Icon name = payments

### Upgrade

Icon name = upgrade

### Add/manage more seats/users

Icon name = group_add

### Domains

Icon name = domain_verification

### Company owner

Icon name = supervised_user_circle

### General settings

Icon name = settings

---

# Images

> components and formatting examples used in Docker's docs

# Images

   Table of contents

---

## Example

- A small image:
  ![a small image](https://docs.docker.com/assets/images/footer_moby_icon.png)  ![a small image](https://docs.docker.com/assets/images/footer_moby_icon.png)
- Large images occupy the full width of the reading column by default:
  ![a pretty wide image](https://docs.docker.com/assets/images/banner_image_24512.png)  ![a pretty wide image](https://docs.docker.com/assets/images/banner_image_24512.png)
- Image size can be set using query parameters: `?h=<height>&w=<width>`
  ![a pretty wide image](https://docs.docker.com/assets/images/banner_image_24512.png?w=100&h=50)  ![a pretty wide image](https://docs.docker.com/assets/images/banner_image_24512.png?w=100&h=50)
- Image with a border, also set with a query parameter: `?border=true`
  ![a small image](https://docs.docker.com/assets/images/footer_moby_icon.png?border=true)  ![a small image](https://docs.docker.com/assets/images/footer_moby_icon.png?border=true)

## HTML and Markdown

```markdown
- A small image: ![a small image](/assets/images/footer_moby_icon.png)

- Large images occupy the full width of the reading column by default:

  ![a pretty wide image](/assets/images/banner_image_24512.png)

- Image size can be set using query parameters: `?h=<height>&w=<width>`

  ![a pretty wide image](/assets/images/banner_image_24512.png?w=100&h=50)

- Image with a border, also set with a query parameter: `?border=true`

  ![a small image](/assets/images/footer_moby_icon.png?border=true)
```

---

# Links

> components and formatting examples used in Docker's docs

# Links

   Table of contents

---

## Examples

[External links](https://docker.com) and [internal links](https://docs.docker.com/contribute/components/links/) both
open in the same tab.

Use relative links, using source filenames.

#### Links to auto-generated content

When you link to heading IDs in auto-generated pages, such as CLI
reference content, you won't get any help from your editor in resolving the
anchor names. That's because the pages are generated at build-time and your
editor or LSP doesn't know about them in advance.

## Syntax

```md
[External links](https://docker.com)
[Internal links](links.md)
```

---

# Lists

> components and formatting examples used in Docker's docs

# Lists

   Table of contents

---

## Examples

Use dashes (`-`) or asterisks (`*`) for bullet points.

- Bullet list item 1
- Bullet list item 2
- Bullet list item 3

1. Numbered list item 1. Two spaces between the period and the first letter
  helps with alignment.
2. Numbered list item 2. Let's put a note in it.
  > Note
3. Numbered list item 3 with a code block in it. You need the blank line before
  the code block happens.
  ```bash
  $ docker run hello-world
  ```
4. Numbered list item 4 with a bullet list inside it and a numbered list
  inside that.
  - Sub-item 1
  - Sub-item 2
    1. Sub-sub-item 1
    2. Sub-sub-item-2 with a table inside it because we like to party!
      Indentation is super important.
      | Header 1 | Header 2 |
      | --- | --- |
      | Thing 1 | Thing 2 |
      | Thing 3 | Thing 4 |

## Markdown

```md
- Bullet list item 1
- Bullet list item 2
- Bullet list item 3

1.  Numbered list item 1. Two spaces between the period and the first letter
    helps with alignment.

2.  Numbered list item 2. Let's put a note in it.

    > [!NOTE]: We did it!

3.  Numbered list item 3 with a code block in it. You need the blank line before
    the code block happens.

    ```bash
    $ docker run hello-world
    ```

4.  Numbered list item 4 with a bullet list inside it and a numbered list
    inside that.

    - Sub-item 1
    - Sub-item 2

      1.  Sub-sub-item 1
      2.  Sub-sub-item-2 with a table inside it.
          Indentation is super important.

          | Header 1 | Header 2 |
          | -------- | -------- |
          | Thing 1  | Thing 2  |
          | Thing 3  | Thing 4  |
```

---

# Tables

> components and formatting examples used in Docker's docs

# Tables

   Table of contents

---

## Example

### Basic table

| Permission level | Access |
| --- | --- |
| Boldoritalicwithin a table cell. Next cell is empty on purpose. |  |
|  | Previous cell is empty. A--flagin mono text. |
| Read | Pull |
| Read/Write | Pull, push |
| Admin | All of the above, plus update description, create, and delete |

### Feature-support table

| Platform | x86_64 / amd64 |
| --- | --- |
| Ubuntu | ✅ |
| Debian | ✅ |
| Fedora |  |
| Arch (btw) | ✅ |

## Markdown

### Basic table

```md
| Permission level                                                         | Access                                                        |
| :----------------------------------------------------------------------- | :------------------------------------------------------------ |
| **Bold** or _italic_ within a table cell. Next cell is empty on purpose. |                                                               |
|                                                                          | Previous cell is empty. A `--flag` in mono text.              |
| Read                                                                     | Pull                                                          |
| Read/Write                                                               | Pull, push                                                    |
| Admin                                                                    | All of the above, plus update description, create, and delete |
```

The alignment of the cells in the source doesn't really matter. The ending pipe
character is optional (unless the last cell is supposed to be empty).

### Feature-support table

```md
| Platform   | x86_64 / amd64 |
| :--------- | :------------: |
| Ubuntu     |       ✅       |
| Debian     |       ✅       |
| Fedora     |                |
| Arch (btw) |       ✅       |
```

---

# Tabs

> components and formatting examples used in Docker's docs

# Tabs

   Table of contents

---

The tabs component consists of two shortcodes:

- `{{< tabs >}}`
- `{{< tab name="name of the tab" >}}`

The `{{< tabs >}}` shortcode is a parent, component, wrapping a number of `tabs`.
Each `{{< tab >}}` is given a name using the `name` attribute.

You can optionally specify a `group` attribute for the `tabs` wrapper to indicate
that a tab section should belong to a group of tabs. See [Groups](#groups).

## Example

```js
console.log("hello world")
```

```go
fmt.Println("hello world")
```

## Markup

```markdown
{{< tabs >}}
{{< tab name="JavaScript" >}}

```js
console.log("hello world")
```

{{< /tab >}}
{{< tab name="Go" >}}

```go
fmt.Println("hello world")
```

{{< /tab >}}
{{< /tabs >}}
```

## Groups

You can optionally specify a tab group on the `tabs` shortcode.
Doing so will synchronize the tab selection for all of the tabs that belong to the same group.

### Tab group example

The following example shows two tab sections belonging to the same group.

```js
console.log("hello world")
```

```go
fmt.Println("hello world")
```

```js
const res = await fetch("/users/1")
```

```go
resp, err := http.Get("/users/1")
```

---

# Videos

> Learn about guidelines and best practices for videos in docs, and how to add a video component.

# Videos

   Table of contents

---

## Video guidelines

Videos are used rarely in Docker's documentation. When used, video should complement written text and not be the sole format of documentation. Videos can take longer to produce and be more difficult to maintain than written text or even screenshots, so consider the following before adding video:

- Can you demonstrate a clear customer need for using video?
- Does the video offer new content, rather than directly reading or re-purposing official documentation?
- If the video contains user interfaces that may change regularly, do you have a maintenance plan to keep the video fresh?
- Does the [voice and tone](https://docs.docker.com/contribute/style/voice-tone/) of the video align with the rest of the documentation?
- Have you considered other options, such as screenshots or clarifying existing documentation?
- Is the quality of the video similar to the rest of Docker's documentation?
- Can the video be linked or embedded from the site?

If all of the above criteria are met, you can reference the following best practices before creating a video to add to Docker documentation.

### Best practices

- Determine the audience for your video. Will the video be a broad overview for beginners, or will it be a deep dive into a technical process designed for an advanced user?
- Videos should be less than 5 minutes long. Keep in mind how long the video needs to be to properly explain the topic, and if the video needs to be longer than 5 minutes, consider text, diagrams, or screenshots instead. These are easier for a user to scan for relevant information.
- Videos should adhere to the same standards for accessibility as the rest of the documentation.
- Ensure the quality of your video by writing a script (if there's narration), making sure multiple browsers and URLs aren't visible, blurring or cropping out any sensitive information, and using smooth transitions between different browsers or screens.

Videos are not hosted in the Docker documentation repository. To add a video, you can [link to](https://docs.docker.com/contribute/components/links/) hosted content, or embed using an [iframe](#iframe).

## iframe

To embed a video on a docs page, use an `<iframe>` element:

```html
<iframe
  class="border-0 w-full aspect-video mb-8"
  allow="fullscreen"
  title=""
  src=""
  ></iframe>
```

## asciinema

`asciinema` is a command line tool for recording terminal sessions. The
recordings can be embedded on the documentation site. These are similar to
`console` code blocks, but since they're playable and scrubbable videos, they
add another level of usefulness over static codeblocks in some cases. Text in
an `asciinema` "video" can also be copied, which makes them more useful.

Consider using an `asciinema` recording if:

- The input/output of the terminal commands are too long for a static example
  (you could also consider truncating the output)
- The steps you want to show are easily demonstrated in a few commands
- Where the it's useful to see both inputs and outputs of commands

To create an `asciinema` recording and add it to docs:

1. [Install](https://docs.asciinema.org/getting-started/) the `asciinema` CLI
2. Run `asciinema auth` to configure your client and create an account
3. Start a new recording with `asciinema rec`
4. Run the commands for your demo and stop the recording with `<C-d>` or `exit`
5. Upload the recording to <asciinema.org>
6. Embed the player with a `<script>` tag using the **Share** button on <asciinema.org>

---

# Source file conventions

> How new .md files should be formatted

# Source file conventions

   Table of contents

---

## File name

When you create a new .md file for new content, make sure:

- File names are as short as possible
- Try to keep the file name to one word or two words
- Use a dash to separate words. For example:
  - `add-seats.md` and `remove-seats.md`.
  - `multiplatform-images` preferred to `multi-platform-images`.

## Front matter

The front matter of a given page is in a section at the top of the Markdown
file that starts and ends with three hyphens. It includes YAML content. The
following keys are supported. The title, description, and keywords are required.

| Key | Required | Description |
| --- | --- | --- |
| title | yes | The page title. This is added to the HTML output as a<h1>level header. |
| description | yes | A sentence that describes the page contents. This is added to the HTML metadata. It’s not rendered on the page. |
| keywords | yes | A comma-separated list of keywords. These are added to the HTML metadata. |
| aliases | no | A YAML list of pages which should redirect to the current page. At build time, each page listed here is created as an HTML stub containing a 302 redirect to this page. |
| notoc | no | Eithertrueorfalse. Iftrue, no in-page TOC is generated for the HTML output of this page. Defaults tofalse. Appropriate for some landing pages that have no in-page headings. |
| toc_min | no | Ignored ifnotocis set totrue. The minimum heading level included in the in-page TOC. Defaults to2, to show<h2>headings as the minimum. |
| toc_max | no | Ignored ifnotocis set tofalse. The maximum heading level included in the in-page TOC. Defaults to3, to show<h3>headings. Set to the same astoc_minto only showtoc_minlevel of headings. |
| sitemap | no | Exclude the page from indexing by search engines. When set tofalse, the page is excluded fromsitemap.xml, and a<meta name="robots" content="noindex"/>header is added to the page. |
| sidebar.reverse | no | This parameter for section pages changes the sort order of the pages in that section. Pages that would normally appear at the top, by weight or by title, will instead appear near the bottom, and vice versa. |
| sidebar.goto | no | Set this to change the URL that the sidebar should point to for this entry. Seepageless sidebar entries. |
| sidebar.badge | no | Set this to add a badge to the sidebar entry for this page. This param option consists of two fields:badge.textandbadge.color. |

Here's an example of a valid (but contrived) page metadata. The order of
the metadata elements in the front matter isn't important.

```text
---
description: Instructions for installing Docker Engine on Ubuntu
keywords: requirements, apt, installation, ubuntu, install, uninstall, upgrade, update
title: Install Docker Engine on Ubuntu
aliases:
- /ee/docker-ee/ubuntu/
- /engine/installation/linux/docker-ce/ubuntu/
- /engine/installation/linux/docker-ee/ubuntu/
- /engine/installation/linux/ubuntu/
- /engine/installation/linux/ubuntulinux/
- /engine/installation/ubuntulinux/
- /install/linux/docker-ce/ubuntu/
- /install/linux/docker-ee/ubuntu/
- /install/linux/ubuntu/
- /installation/ubuntulinux/
toc_max: 4
---
```

## Body

The body of the page (with the exception of keywords) starts after the front matter.

### Text length

Splitting long lines (preferably up to 80 characters) can make it easier to provide feedback on small chunks of text.

## Pageless sidebar entries

If you want to add an entry to the sidebar, but you want the link to point somewhere else, you can use the `sidebar.goto` parameter.
This is useful in combination with `build.render` set to `always`, which creates a pageless entry in the sidebar that links to another page.

```text
---
title: Dummy sidebar link
build:
  render: never
sidebar:
  goto: /some/other/page/
weight: 30
---
```
