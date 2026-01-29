# Environment Variables¶ and more

# Environment Variables¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Environment Variables¶

Tip

If you already know what "environment variables" are and how to use them, feel free to skip this.

An environment variable (also known as "**env var**") is a variable that lives **outside** of the Python code, in the **operating system**, and could be read by your Python code (or by other programs as well).

Environment variables could be useful for handling application **settings**, as part of the **installation** of Python, etc.

## Create and Use Env Vars¶

You can **create** and use environment variables in the **shell (terminal)**, without needing Python:

 [Linux, macOS, Windows Bash](#__tabbed_1_1)[Windows PowerShell](#__tabbed_1_2)

```
export MY_NAME="Wade Wilson"
echo "Hello $MY_NAME"
```

```
$Env:MY_NAME = "Wade Wilson"
echo "Hello $Env:MY_NAME"
```

## Read env vars in Python¶

You could also create environment variables **outside** of Python, in the terminal (or with any other method), and then **read them in Python**.

For example you could have a file `main.py` with:

```
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

Tip

The second argument to [os.getenv()](https://docs.python.org/3.8/library/os.html#os.getenv) is the default value to return.

If not provided, it's `None` by default, here we provide `"World"` as the default value to use.

Then you could call that Python program:

 [Linux, macOS, Windows Bash](#__tabbed_2_1)[Windows PowerShell](#__tabbed_2_2)

```
python main.py
export MY_NAME="Wade Wilson"
python main.py
```

```
python main.py
$Env:MY_NAME = "Wade Wilson"
python main.py
```

As environment variables can be set outside of the code, but can be read by the code, and don't have to be stored (committed to `git`) with the rest of the files, it's common to use them for configurations or **settings**.

You can also create an environment variable only for a **specific program invocation**, that is only available to that program, and only for its duration.

To do that, create it right before the program itself, on the same line:

```
MY_NAME="Wade Wilson" python main.py
python main.py
```

Tip

You can read more about it at [The Twelve-Factor App: Config](https://12factor.net/config).

## Types and Validation¶

These environment variables can only handle **text strings**, as they are external to Python and have to be compatible with other programs and the rest of the system (and even with different operating systems, as Linux, Windows, macOS).

That means that **any value** read in Python from an environment variable **will be astr**, and any conversion to a different type or any validation has to be done in code.

You will learn more about using environment variables for handling **application settings** in the [Advanced User Guide - Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/).

## PATHEnvironment Variable¶

There is a **special** environment variable called **PATH** that is used by the operating systems (Linux, macOS, Windows) to find programs to run.

The value of the variable `PATH` is a long string that is made of directories separated by a colon `:` on Linux and macOS, and by a semicolon `;` on Windows.

For example, the `PATH` environment variable could look like this:

 [Linux, macOS](#__tabbed_3_1)[Windows](#__tabbed_3_2)

```
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

This means that the system should look for programs in the directories:

- `/usr/local/bin`
- `/usr/bin`
- `/bin`
- `/usr/sbin`
- `/sbin`

```
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

This means that the system should look for programs in the directories:

- `C:\Program Files\Python312\Scripts`
- `C:\Program Files\Python312`
- `C:\Windows\System32`

When you type a **command** in the terminal, the operating system **looks for** the program in **each of those directories** listed in the `PATH` environment variable.

For example, when you type `python` in the terminal, the operating system looks for a program called `python` in the **first directory** in that list.

If it finds it, then it will **use it**. Otherwise it keeps looking in the **other directories**.

### Installing Python and Updating thePATH¶

When you install Python, you might be asked if you want to update the `PATH` environment variable.

 [Linux, macOS](#__tabbed_4_1)[Windows](#__tabbed_4_2)

Let's say you install Python and it ends up in a directory `/opt/custompython/bin`.

If you say yes to update the `PATH` environment variable, then the installer will add `/opt/custompython/bin` to the `PATH` environment variable.

It could look like this:

```
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

This way, when you type `python` in the terminal, the system will find the Python program in `/opt/custompython/bin` (the last directory) and use that one.

Let's say you install Python and it ends up in a directory `C:\opt\custompython\bin`.

If you say yes to update the `PATH` environment variable, then the installer will add `C:\opt\custompython\bin` to the `PATH` environment variable.

```
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

This way, when you type `python` in the terminal, the system will find the Python program in `C:\opt\custompython\bin` (the last directory) and use that one.

So, if you type:

```
python
```

  [Linux, macOS](#__tabbed_5_1)[Windows](#__tabbed_5_2)

The system will **find** the `python` program in `/opt/custompython/bin` and run it.

It would be roughly equivalent to typing:

```
/opt/custompython/bin/python
```

The system will **find** the `python` program in `C:\opt\custompython\bin\python` and run it.

It would be roughly equivalent to typing:

```
C:\opt\custompython\bin\python
```

This information will be useful when learning about [Virtual Environments](https://fastapi.tiangolo.com/virtual-environments/).

## Conclusion¶

With this you should have a basic understanding of what **environment variables** are and how to use them in Python.

You can also read more about them in the [Wikipedia for Environment Variable](https://en.wikipedia.org/wiki/Environment_variable).

In many cases it's not very obvious how environment variables would be useful and applicable right away. But they keep showing up in many different scenarios when you are developing, so it's good to know about them.

For example, you will need this information in the next section, about [Virtual Environments](https://fastapi.tiangolo.com/virtual-environments/).

---

# External Links¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# External Links¶

**FastAPI** has a great community constantly growing.

There are many posts, articles, tools, and projects, related to **FastAPI**.

You could easily use a search engine or video platform to find many resources related to FastAPI.

Info

Before, this page used to list links to external articles.

But now that FastAPI is the backend framework with the most GitHub stars across languages, and the most starred and used framework in Python, it no longer makes sense to attempt to list all articles written about it.

## GitHub Repositories¶

Most starred [GitHub repositories with the topicfastapi](https://github.com/topics/fastapi):

[★ 40334 - full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template) by [@fastapi](https://github.com/fastapi).

[★ 33628 - Hello-Python](https://github.com/mouredev/Hello-Python) by [@mouredev](https://github.com/mouredev).

[★ 21817 - serve](https://github.com/jina-ai/serve) by [@jina-ai](https://github.com/jina-ai).

[★ 20409 - HivisionIDPhotos](https://github.com/Zeyi-Lin/HivisionIDPhotos) by [@Zeyi-Lin](https://github.com/Zeyi-Lin).

[★ 17415 - sqlmodel](https://github.com/fastapi/sqlmodel) by [@fastapi](https://github.com/fastapi).

[★ 15776 - fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) by [@zhanymkanov](https://github.com/zhanymkanov).

[★ 15588 - Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) by [@Evil0ctal](https://github.com/Evil0ctal).

[★ 12447 - machine-learning-zoomcamp](https://github.com/DataTalksClub/machine-learning-zoomcamp) by [@DataTalksClub](https://github.com/DataTalksClub).

[★ 12128 - SurfSense](https://github.com/MODSetter/SurfSense) by [@MODSetter](https://github.com/MODSetter).

[★ 11326 - fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) by [@tadata-org](https://github.com/tadata-org).

[★ 10901 - awesome-fastapi](https://github.com/mjhea0/awesome-fastapi) by [@mjhea0](https://github.com/mjhea0).

[★ 9584 - XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader) by [@JoeanAmier](https://github.com/JoeanAmier).

[★ 8951 - polar](https://github.com/polarsource/polar) by [@polarsource](https://github.com/polarsource).

[★ 8934 - FastUI](https://github.com/pydantic/FastUI) by [@pydantic](https://github.com/pydantic).

[★ 7934 - FileCodeBox](https://github.com/vastsa/FileCodeBox) by [@vastsa](https://github.com/vastsa).

[★ 7248 - nonebot2](https://github.com/nonebot/nonebot2) by [@nonebot](https://github.com/nonebot).

[★ 6392 - hatchet](https://github.com/hatchet-dev/hatchet) by [@hatchet-dev](https://github.com/hatchet-dev).

[★ 5899 - fastapi-users](https://github.com/fastapi-users/fastapi-users) by [@fastapi-users](https://github.com/fastapi-users).

[★ 5754 - serge](https://github.com/serge-chat/serge) by [@serge-chat](https://github.com/serge-chat).

[★ 4577 - strawberry](https://github.com/strawberry-graphql/strawberry) by [@strawberry-graphql](https://github.com/strawberry-graphql).

[★ 4303 - poem](https://github.com/poem-web/poem) by [@poem-web](https://github.com/poem-web).

[★ 4287 - chatgpt-web-share](https://github.com/chatpire/chatgpt-web-share) by [@chatpire](https://github.com/chatpire).

[★ 4221 - dynaconf](https://github.com/dynaconf/dynaconf) by [@dynaconf](https://github.com/dynaconf).

[★ 4181 - Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI) by [@remsky](https://github.com/remsky).

[★ 4090 - atrilabs-engine](https://github.com/Atri-Labs/atrilabs-engine) by [@Atri-Labs](https://github.com/Atri-Labs).

[★ 4037 - devpush](https://github.com/hunvreus/devpush) by [@hunvreus](https://github.com/hunvreus).

[★ 3896 - logfire](https://github.com/pydantic/logfire) by [@pydantic](https://github.com/pydantic).

[★ 3756 - LitServe](https://github.com/Lightning-AI/LitServe) by [@Lightning-AI](https://github.com/Lightning-AI).

[★ 3702 - huma](https://github.com/danielgtaylor/huma) by [@danielgtaylor](https://github.com/danielgtaylor).

[★ 3680 - Yuxi-Know](https://github.com/xerrors/Yuxi-Know) by [@xerrors](https://github.com/xerrors).

[★ 3675 - datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator) by [@koxudaxi](https://github.com/koxudaxi).

[★ 3659 - fastapi-admin](https://github.com/fastapi-admin/fastapi-admin) by [@fastapi-admin](https://github.com/fastapi-admin).

[★ 3497 - farfalle](https://github.com/rashadphz/farfalle) by [@rashadphz](https://github.com/rashadphz).

[★ 3421 - tracecat](https://github.com/TracecatHQ/tracecat) by [@TracecatHQ](https://github.com/TracecatHQ).

[★ 3136 - opyrator](https://github.com/ml-tooling/opyrator) by [@ml-tooling](https://github.com/ml-tooling).

[★ 3111 - docarray](https://github.com/docarray/docarray) by [@docarray](https://github.com/docarray).

[★ 3051 - fastapi-realworld-example-app](https://github.com/nsidnev/fastapi-realworld-example-app) by [@nsidnev](https://github.com/nsidnev).

[★ 3034 - mcp-context-forge](https://github.com/IBM/mcp-context-forge) by [@IBM](https://github.com/IBM).

[★ 2904 - uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker) by [@tiangolo](https://github.com/tiangolo).

[★ 2680 - FastAPI-template](https://github.com/s3rius/FastAPI-template) by [@s3rius](https://github.com/s3rius).

[★ 2662 - best-of-web-python](https://github.com/ml-tooling/best-of-web-python) by [@ml-tooling](https://github.com/ml-tooling).

[★ 2614 - YC-Killer](https://github.com/sahibzada-allahyar/YC-Killer) by [@sahibzada-allahyar](https://github.com/sahibzada-allahyar).

[★ 2587 - sqladmin](https://github.com/aminalaee/sqladmin) by [@aminalaee](https://github.com/aminalaee).

[★ 2566 - fastapi-react](https://github.com/Buuntu/fastapi-react) by [@Buuntu](https://github.com/Buuntu).

[★ 2456 - RasaGPT](https://github.com/paulpierre/RasaGPT) by [@paulpierre](https://github.com/paulpierre).

[★ 2394 - supabase-py](https://github.com/supabase/supabase-py) by [@supabase](https://github.com/supabase).

[★ 2338 - nextpy](https://github.com/dot-agent/nextpy) by [@dot-agent](https://github.com/dot-agent).

[★ 2289 - fastapi-utils](https://github.com/fastapiutils/fastapi-utils) by [@fastapiutils](https://github.com/fastapiutils).

[★ 2234 - langserve](https://github.com/langchain-ai/langserve) by [@langchain-ai](https://github.com/langchain-ai).

[★ 2232 - 30-Days-of-Python](https://github.com/codingforentrepreneurs/30-Days-of-Python) by [@codingforentrepreneurs](https://github.com/codingforentrepreneurs).

[★ 2141 - solara](https://github.com/widgetti/solara) by [@widgetti](https://github.com/widgetti).

[★ 2046 - mangum](https://github.com/Kludex/mangum) by [@Kludex](https://github.com/Kludex).

[★ 1963 - fastapi_best_architecture](https://github.com/fastapi-practices/fastapi_best_architecture) by [@fastapi-practices](https://github.com/fastapi-practices).

[★ 1943 - NoteDiscovery](https://github.com/gamosoft/NoteDiscovery) by [@gamosoft](https://github.com/gamosoft).

[★ 1936 - agentkit](https://github.com/BCG-X-Official/agentkit) by [@BCG-X-Official](https://github.com/BCG-X-Official).

[★ 1909 - vue-fastapi-admin](https://github.com/mizhexiaoxiao/vue-fastapi-admin) by [@mizhexiaoxiao](https://github.com/mizhexiaoxiao).

[★ 1887 - manage-fastapi](https://github.com/ycd/manage-fastapi) by [@ycd](https://github.com/ycd).

[★ 1879 - openapi-python-client](https://github.com/openapi-generators/openapi-python-client) by [@openapi-generators](https://github.com/openapi-generators).

[★ 1845 - slowapi](https://github.com/laurentS/slowapi) by [@laurentS](https://github.com/laurentS).

[★ 1843 - piccolo](https://github.com/piccolo-orm/piccolo) by [@piccolo-orm](https://github.com/piccolo-orm).

[★ 1813 - python-week-2022](https://github.com/rochacbruno/python-week-2022) by [@rochacbruno](https://github.com/rochacbruno).

[★ 1805 - fastapi-cache](https://github.com/long2ice/fastapi-cache) by [@long2ice](https://github.com/long2ice).

[★ 1785 - ormar](https://github.com/collerek/ormar) by [@collerek](https://github.com/collerek).

[★ 1780 - fastapi-langgraph-agent-production-ready-template](https://github.com/wassim249/fastapi-langgraph-agent-production-ready-template) by [@wassim249](https://github.com/wassim249).

[★ 1734 - FastAPI-boilerplate](https://github.com/benavlabs/FastAPI-boilerplate) by [@benavlabs](https://github.com/benavlabs).

[★ 1724 - termpair](https://github.com/cs01/termpair) by [@cs01](https://github.com/cs01).

[★ 1671 - fastapi-crudrouter](https://github.com/awtkns/fastapi-crudrouter) by [@awtkns](https://github.com/awtkns).

[★ 1633 - langchain-serve](https://github.com/jina-ai/langchain-serve) by [@jina-ai](https://github.com/jina-ai).

[★ 1588 - fastapi-pagination](https://github.com/uriyyo/fastapi-pagination) by [@uriyyo](https://github.com/uriyyo).

[★ 1583 - awesome-fastapi-projects](https://github.com/Kludex/awesome-fastapi-projects) by [@Kludex](https://github.com/Kludex).

[★ 1571 - coronavirus-tracker-api](https://github.com/ExpDev07/coronavirus-tracker-api) by [@ExpDev07](https://github.com/ExpDev07).

[★ 1549 - bracket](https://github.com/evroon/bracket) by [@evroon](https://github.com/evroon).

[★ 1491 - fastapi-amis-admin](https://github.com/amisadmin/fastapi-amis-admin) by [@amisadmin](https://github.com/amisadmin).

[★ 1452 - fastapi-boilerplate](https://github.com/teamhide/fastapi-boilerplate) by [@teamhide](https://github.com/teamhide).

[★ 1452 - fastcrud](https://github.com/benavlabs/fastcrud) by [@benavlabs](https://github.com/benavlabs).

[★ 1430 - awesome-python-resources](https://github.com/DjangoEx/awesome-python-resources) by [@DjangoEx](https://github.com/DjangoEx).

[★ 1399 - prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator) by [@trallnag](https://github.com/trallnag).

[★ 1371 - fastapi-code-generator](https://github.com/koxudaxi/fastapi-code-generator) by [@koxudaxi](https://github.com/koxudaxi).

[★ 1346 - fastapi-tutorial](https://github.com/liaogx/fastapi-tutorial) by [@liaogx](https://github.com/liaogx).

[★ 1345 - budgetml](https://github.com/ebhy/budgetml) by [@ebhy](https://github.com/ebhy).

[★ 1331 - fastapi-scaff](https://github.com/atpuxiner/fastapi-scaff) by [@atpuxiner](https://github.com/atpuxiner).

[★ 1266 - bolt-python](https://github.com/slackapi/bolt-python) by [@slackapi](https://github.com/slackapi).

[★ 1266 - bedrock-chat](https://github.com/aws-samples/bedrock-chat) by [@aws-samples](https://github.com/aws-samples).

[★ 1260 - fastapi-alembic-sqlmodel-async](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async) by [@jonra1993](https://github.com/jonra1993).

[★ 1222 - fastapi_production_template](https://github.com/zhanymkanov/fastapi_production_template) by [@zhanymkanov](https://github.com/zhanymkanov).

[★ 1179 - langchain-extract](https://github.com/langchain-ai/langchain-extract) by [@langchain-ai](https://github.com/langchain-ai).

[★ 1152 - restish](https://github.com/rest-sh/restish) by [@rest-sh](https://github.com/rest-sh).

[★ 1143 - odmantic](https://github.com/art049/odmantic) by [@art049](https://github.com/art049).

[★ 1128 - authx](https://github.com/yezz123/authx) by [@yezz123](https://github.com/yezz123).

[★ 1104 - SAG](https://github.com/Zleap-AI/SAG) by [@Zleap-AI](https://github.com/Zleap-AI).

[★ 1072 - aktools](https://github.com/akfamily/aktools) by [@akfamily](https://github.com/akfamily).

[★ 1063 - RuoYi-Vue3-FastAPI](https://github.com/insistence/RuoYi-Vue3-FastAPI) by [@insistence](https://github.com/insistence).

[★ 1059 - flock](https://github.com/Onelevenvy/flock) by [@Onelevenvy](https://github.com/Onelevenvy).

[★ 1046 - fastapi-observability](https://github.com/blueswen/fastapi-observability) by [@blueswen](https://github.com/blueswen).

[★ 1019 - enterprise-deep-research](https://github.com/SalesforceAIResearch/enterprise-deep-research) by [@SalesforceAIResearch](https://github.com/SalesforceAIResearch).

[★ 1016 - titiler](https://github.com/developmentseed/titiler) by [@developmentseed](https://github.com/developmentseed).

[★ 1004 - every-pdf](https://github.com/DDULDDUCK/every-pdf) by [@DDULDDUCK](https://github.com/DDULDDUCK).

[★ 1003 - autollm](https://github.com/viddexa/autollm) by [@viddexa](https://github.com/viddexa).

[★ 996 - lanarky](https://github.com/ajndkr/lanarky) by [@ajndkr](https://github.com/ajndkr).

---

# FastAPI CLI¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# FastAPI CLI¶

**FastAPI CLI** is a command line program that you can use to serve your FastAPI app, manage your FastAPI project, and more.

When you install FastAPI (e.g. with `pip install "fastapi[standard]"`), it includes a package called `fastapi-cli`, this package provides the `fastapi` command in the terminal.

To run your FastAPI app for development, you can use the `fastapi dev` command:

```
<font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>
```

The command line program called `fastapi` is **FastAPI CLI**.

FastAPI CLI takes the path to your Python program (e.g. `main.py`) and automatically detects the `FastAPI` instance (commonly named `app`), determines the correct import process, and then serves it.

For production you would use `fastapi run` instead. 🚀

Internally, **FastAPI CLI** uses [Uvicorn](https://www.uvicorn.dev), a high-performance, production-ready, ASGI server. 😎

## fastapi dev¶

Running `fastapi dev` initiates development mode.

By default, **auto-reload** is enabled, automatically reloading the server when you make changes to your code. This is resource-intensive and could be less stable than when it's disabled. You should only use it for development. It also listens on the IP address `127.0.0.1`, which is the IP for your machine to communicate with itself alone (`localhost`).

## fastapi run¶

Executing `fastapi run` starts FastAPI in production mode by default.

By default, **auto-reload** is disabled. It also listens on the IP address `0.0.0.0`, which means all the available IP addresses, this way it will be publicly accessible to anyone that can communicate with the machine. This is how you would normally run it in production, for example, in a container.

In most cases you would (and should) have a "termination proxy" handling HTTPS for you on top, this will depend on how you deploy your application, your provider might do this for you, or you might need to set it up yourself.

Tip

You can learn more about it in the [deployment documentation](https://fastapi.tiangolo.com/deployment/).

---

# FastAPI People¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# FastAPI People¶

FastAPI has an amazing community that welcomes people from all backgrounds.

## Creator¶

Hey! 👋

This is me:

  [@tiangolo](https://github.com/tiangolo) Answers: 1900Pull Requests: 857

I'm the creator of **FastAPI**. You can read more about that in [Help FastAPI - Get Help - Connect with the author](https://fastapi.tiangolo.com/help-fastapi/#connect-with-the-author).

...But here I want to show you the community.

---

**FastAPI** receives a lot of support from the community. And I want to highlight their contributions.

These are the people that:

- [Help others with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github).
- [Create Pull Requests](https://fastapi.tiangolo.com/help-fastapi/#create-a-pull-request).
- Review Pull Requests, [especially important for translations](https://fastapi.tiangolo.com/contributing/#translations).
- Help [manage the repository](https://fastapi.tiangolo.com/management-tasks/) (team members).

All these tasks help maintain the repository.

A round of applause to them. 👏 🙇

## Team¶

This is the current list of team members. 😎

They have different levels of involvement and permissions, they can perform [repository management tasks](https://fastapi.tiangolo.com/management-tasks/) and together we  [manage the FastAPI repository](https://fastapi.tiangolo.com/management/).

  [@tiangolo](https://github.com/tiangolo) [@Kludex](https://github.com/Kludex) [@alejsdev](https://github.com/alejsdev) [@svlandeg](https://github.com/svlandeg) [@YuriiMotov](https://github.com/YuriiMotov) [@patrick91](https://github.com/patrick91) [@luzzodev](https://github.com/luzzodev)

Although the team members have the permissions to perform privileged tasks, all the [help from others maintaining FastAPI](https://fastapi.tiangolo.com/help-fastapi/#help-maintain-fastapi) is very much appreciated! 🙇‍♂️

## FastAPI Experts¶

These are the users that have been [helping others the most with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github). 🙇

They have proven to be **FastAPI Experts** by helping many others. ✨

Tip

You could become an official FastAPI Expert too!

Just [help others with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github). 🤓

You can see the **FastAPI Experts** for:

- [Last Month](https://fastapi.tiangolo.com/fastapi-people/#fastapi-experts-last-month) 🤓
- [3 Months](https://fastapi.tiangolo.com/fastapi-people/#fastapi-experts-3-months) 😎
- [6 Months](https://fastapi.tiangolo.com/fastapi-people/#fastapi-experts-6-months) 🧐
- [1 Year](https://fastapi.tiangolo.com/fastapi-people/#fastapi-experts-1-year) 🧑‍🔬
- [All Time](https://fastapi.tiangolo.com/fastapi-people/#fastapi-experts-all-time) 🧙

### FastAPI Experts - Last Month¶

These are the users that have been [helping others the most with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github) during the last month. 🤓

  [@YuriiMotov](https://github.com/YuriiMotov) Questions replied: 17 [@valentinDruzhinin](https://github.com/valentinDruzhinin) Questions replied: 5 [@yinziyan1206](https://github.com/yinziyan1206) Questions replied: 4 [@luzzodev](https://github.com/luzzodev) Questions replied: 2

### FastAPI Experts - 3 Months¶

These are the users that have been [helping others the most with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github) during the last 3 months. 😎

  [@YuriiMotov](https://github.com/YuriiMotov) Questions replied: 397 [@valentinDruzhinin](https://github.com/valentinDruzhinin) Questions replied: 24 [@luzzodev](https://github.com/luzzodev) Questions replied: 17 [@raceychan](https://github.com/raceychan) Questions replied: 6 [@yinziyan1206](https://github.com/yinziyan1206) Questions replied: 5 [@DoctorJohn](https://github.com/DoctorJohn) Questions replied: 5 [@sachinh35](https://github.com/sachinh35) Questions replied: 4 [@eqsdxr](https://github.com/eqsdxr) Questions replied: 4 [@Jelle-tenB](https://github.com/Jelle-tenB) Questions replied: 3

### FastAPI Experts - 6 Months¶

These are the users that have been [helping others the most with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github) during the last 6 months. 🧐

  [@YuriiMotov](https://github.com/YuriiMotov) Questions replied: 763 [@luzzodev](https://github.com/luzzodev) Questions replied: 45 [@valentinDruzhinin](https://github.com/valentinDruzhinin) Questions replied: 24 [@alv2017](https://github.com/alv2017) Questions replied: 16 [@sachinh35](https://github.com/sachinh35) Questions replied: 9 [@yauhen-sobaleu](https://github.com/yauhen-sobaleu) Questions replied: 9 [@JavierSanchezCastro](https://github.com/JavierSanchezCastro) Questions replied: 6 [@raceychan](https://github.com/raceychan) Questions replied: 6 [@yinziyan1206](https://github.com/yinziyan1206) Questions replied: 5

### FastAPI Experts - 1 Year¶

These are the users that have been [helping others the most with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github) during the last year. 🧑‍🔬

  [@YuriiMotov](https://github.com/YuriiMotov) Questions replied: 824 [@luzzodev](https://github.com/luzzodev) Questions replied: 89 [@Kludex](https://github.com/Kludex) Questions replied: 50 [@sinisaos](https://github.com/sinisaos) Questions replied: 33 [@alv2017](https://github.com/alv2017) Questions replied: 26 [@valentinDruzhinin](https://github.com/valentinDruzhinin) Questions replied: 24 [@JavierSanchezCastro](https://github.com/JavierSanchezCastro) Questions replied: 24 [@jgould22](https://github.com/jgould22) Questions replied: 17 [@Kfir-G](https://github.com/Kfir-G) Questions replied: 13 [@sehraramiz](https://github.com/sehraramiz) Questions replied: 11 [@sachinh35](https://github.com/sachinh35) Questions replied: 9 [@yauhen-sobaleu](https://github.com/yauhen-sobaleu) Questions replied: 9 [@estebanx64](https://github.com/estebanx64) Questions replied: 7 [@ceb10n](https://github.com/ceb10n) Questions replied: 7 [@yvallois](https://github.com/yvallois) Questions replied: 7 [@raceychan](https://github.com/raceychan) Questions replied: 6 [@yinziyan1206](https://github.com/yinziyan1206) Questions replied: 5 [@DoctorJohn](https://github.com/DoctorJohn) Questions replied: 5 [@n8sty](https://github.com/n8sty) Questions replied: 5

### FastAPI Experts - All Time¶

Here are the all time **FastAPI Experts**. 🤓🤯

These are the users that have [helped others the most with questions in GitHub](https://fastapi.tiangolo.com/help-fastapi/#help-others-with-questions-in-github) through *all time*. 🧙

  [@YuriiMotov](https://github.com/YuriiMotov) Questions replied: 971 [@Kludex](https://github.com/Kludex) Questions replied: 654 [@jgould22](https://github.com/jgould22) Questions replied: 263 [@dmontagu](https://github.com/dmontagu) Questions replied: 240 [@Mause](https://github.com/Mause) Questions replied: 219 [@ycd](https://github.com/ycd) Questions replied: 216 [@JarroVGIT](https://github.com/JarroVGIT) Questions replied: 190 [@euri10](https://github.com/euri10) Questions replied: 153 [@iudeen](https://github.com/iudeen) Questions replied: 128 [@phy25](https://github.com/phy25) Questions replied: 126 [@JavierSanchezCastro](https://github.com/JavierSanchezCastro) Questions replied: 94 [@luzzodev](https://github.com/luzzodev) Questions replied: 89 [@raphaelauv](https://github.com/raphaelauv) Questions replied: 83 [@ArcLightSlavik](https://github.com/ArcLightSlavik) Questions replied: 71 [@ghandic](https://github.com/ghandic) Questions replied: 71 [@n8sty](https://github.com/n8sty) Questions replied: 67 [@falkben](https://github.com/falkben) Questions replied: 59 [@yinziyan1206](https://github.com/yinziyan1206) Questions replied: 54 [@sm-Fifteen](https://github.com/sm-Fifteen) Questions replied: 49 [@acidjunk](https://github.com/acidjunk) Questions replied: 49 [@adriangb](https://github.com/adriangb) Questions replied: 46 [@Dustyposa](https://github.com/Dustyposa) Questions replied: 45 [@insomnes](https://github.com/insomnes) Questions replied: 45 [@frankie567](https://github.com/frankie567) Questions replied: 43 [@odiseo0](https://github.com/odiseo0) Questions replied: 43 [@sinisaos](https://github.com/sinisaos) Questions replied: 41 [@includeamin](https://github.com/includeamin) Questions replied: 40 [@STeveShary](https://github.com/STeveShary) Questions replied: 37 [@chbndrhnns](https://github.com/chbndrhnns) Questions replied: 37 [@krishnardt](https://github.com/krishnardt) Questions replied: 35 [@panla](https://github.com/panla) Questions replied: 32 [@prostomarkeloff](https://github.com/prostomarkeloff) Questions replied: 28 [@hasansezertasan](https://github.com/hasansezertasan) Questions replied: 27 [@alv2017](https://github.com/alv2017) Questions replied: 26 [@dbanty](https://github.com/dbanty) Questions replied: 26 [@wshayes](https://github.com/wshayes) Questions replied: 25 [@valentinDruzhinin](https://github.com/valentinDruzhinin) Questions replied: 24 [@SirTelemak](https://github.com/SirTelemak) Questions replied: 23 [@connebs](https://github.com/connebs) Questions replied: 22 [@nymous](https://github.com/nymous) Questions replied: 22 [@chrisK824](https://github.com/chrisK824) Questions replied: 22 [@rafsaf](https://github.com/rafsaf) Questions replied: 21 [@nsidnev](https://github.com/nsidnev) Questions replied: 20 [@chris-allnutt](https://github.com/chris-allnutt) Questions replied: 20 [@ebottos94](https://github.com/ebottos94) Questions replied: 20 [@estebanx64](https://github.com/estebanx64) Questions replied: 19 [@sehraramiz](https://github.com/sehraramiz) Questions replied: 18 [@retnikt](https://github.com/retnikt) Questions replied: 18

## Top Contributors¶

Here are the **Top Contributors**. 👷

These users have [created the most Pull Requests](https://fastapi.tiangolo.com/help-fastapi/#create-a-pull-request) that have been *merged*.

They have contributed source code, documentation, etc. 📦

  [@alejsdev](https://github.com/alejsdev) Pull Requests: 53 [@YuriiMotov](https://github.com/YuriiMotov) Pull Requests: 36 [@Kludex](https://github.com/Kludex) Pull Requests: 25 [@dmontagu](https://github.com/dmontagu) Pull Requests: 17 [@svlandeg](https://github.com/svlandeg) Pull Requests: 16 [@nilslindemann](https://github.com/nilslindemann) Pull Requests: 15 [@euri10](https://github.com/euri10) Pull Requests: 13 [@kantandane](https://github.com/kantandane) Pull Requests: 13 [@zhaohan-dong](https://github.com/zhaohan-dong) Pull Requests: 11 [@mariacamilagl](https://github.com/mariacamilagl) Pull Requests: 9 [@handabaldeep](https://github.com/handabaldeep) Pull Requests: 9 [@vishnuvskvkl](https://github.com/vishnuvskvkl) Pull Requests: 8 [@alissadb](https://github.com/alissadb) Pull Requests: 6 [@alv2017](https://github.com/alv2017) Pull Requests: 6 [@wshayes](https://github.com/wshayes) Pull Requests: 5 [@samuelcolvin](https://github.com/samuelcolvin) Pull Requests: 5 [@waynerv](https://github.com/waynerv) Pull Requests: 5 [@musicinmybrain](https://github.com/musicinmybrain) Pull Requests: 5 [@krishnamadhavan](https://github.com/krishnamadhavan) Pull Requests: 5 [@jekirl](https://github.com/jekirl) Pull Requests: 4 [@hitrust](https://github.com/hitrust) Pull Requests: 4 [@ShahriyarR](https://github.com/ShahriyarR) Pull Requests: 4 [@adriangb](https://github.com/adriangb) Pull Requests: 4 [@iudeen](https://github.com/iudeen) Pull Requests: 4 [@philipokiokio](https://github.com/philipokiokio) Pull Requests: 4 [@AlexWendland](https://github.com/AlexWendland) Pull Requests: 4 [@divums](https://github.com/divums) Pull Requests: 3 [@prostomarkeloff](https://github.com/prostomarkeloff) Pull Requests: 3 [@frankie567](https://github.com/frankie567) Pull Requests: 3 [@nsidnev](https://github.com/nsidnev) Pull Requests: 3 [@pawamoy](https://github.com/pawamoy) Pull Requests: 3 [@patrickmckenna](https://github.com/patrickmckenna) Pull Requests: 3 [@hukkin](https://github.com/hukkin) Pull Requests: 3 [@marcosmmb](https://github.com/marcosmmb) Pull Requests: 3 [@Serrones](https://github.com/Serrones) Pull Requests: 3 [@uriyyo](https://github.com/uriyyo) Pull Requests: 3 [@andrew222651](https://github.com/andrew222651) Pull Requests: 3 [@rkbeatss](https://github.com/rkbeatss) Pull Requests: 3 [@asheux](https://github.com/asheux) Pull Requests: 3 [@blkst8](https://github.com/blkst8) Pull Requests: 3 [@ghandic](https://github.com/ghandic) Pull Requests: 3 [@TeoZosa](https://github.com/TeoZosa) Pull Requests: 3 [@graingert](https://github.com/graingert) Pull Requests: 3 [@jaystone776](https://github.com/jaystone776) Pull Requests: 3 [@zanieb](https://github.com/zanieb) Pull Requests: 3 [@MicaelJarniac](https://github.com/MicaelJarniac) Pull Requests: 3

There are hundreds of other contributors, you can see them all in the [FastAPI GitHub Contributors page](https://github.com/fastapi/fastapi/graphs/contributors). 👷

## Top Translation Reviewers¶

These users are the **Top Translation Reviewers**. 🕵️

Translation reviewers have the [power to approve translations](https://fastapi.tiangolo.com/contributing/#translations) of the documentation. Without them, there wouldn't be documentation in several other languages.

  [@s111d](https://github.com/s111d) Reviews: 147 [@Xewus](https://github.com/Xewus) Reviews: 140 [@sodaMelon](https://github.com/sodaMelon) Reviews: 127 [@ceb10n](https://github.com/ceb10n) Reviews: 117 [@tokusumi](https://github.com/tokusumi) Reviews: 104 [@hard-coders](https://github.com/hard-coders) Reviews: 96 [@hasansezertasan](https://github.com/hasansezertasan) Reviews: 95 [@alv2017](https://github.com/alv2017) Reviews: 88 [@nazarepiedady](https://github.com/nazarepiedady) Reviews: 87 [@AlertRED](https://github.com/AlertRED) Reviews: 81 [@Alexandrhub](https://github.com/Alexandrhub) Reviews: 68 [@waynerv](https://github.com/waynerv) Reviews: 63 [@cassiobotaro](https://github.com/cassiobotaro) Reviews: 62 [@mattwang44](https://github.com/mattwang44) Reviews: 61 [@nilslindemann](https://github.com/nilslindemann) Reviews: 59 [@Laineyzhang55](https://github.com/Laineyzhang55) Reviews: 48 [@Kludex](https://github.com/Kludex) Reviews: 47 [@YuriiMotov](https://github.com/YuriiMotov) Reviews: 46 [@komtaki](https://github.com/komtaki) Reviews: 45 [@rostik1410](https://github.com/rostik1410) Reviews: 42 [@svlandeg](https://github.com/svlandeg) Reviews: 42 [@alperiox](https://github.com/alperiox) Reviews: 42 [@Rishat-F](https://github.com/Rishat-F) Reviews: 42 [@Winand](https://github.com/Winand) Reviews: 40 [@solomein-sv](https://github.com/solomein-sv) Reviews: 38 [@JavierSanchezCastro](https://github.com/JavierSanchezCastro) Reviews: 38 [@alejsdev](https://github.com/alejsdev) Reviews: 37 [@mezgoodle](https://github.com/mezgoodle) Reviews: 37 [@stlucasgarcia](https://github.com/stlucasgarcia) Reviews: 36 [@SwftAlpc](https://github.com/SwftAlpc) Reviews: 36 [@timothy-jeong](https://github.com/timothy-jeong) Reviews: 36 [@rjNemo](https://github.com/rjNemo) Reviews: 34 [@codingjenny](https://github.com/codingjenny) Reviews: 34 [@akarev0](https://github.com/akarev0) Reviews: 33 [@Vincy1230](https://github.com/Vincy1230) Reviews: 33 [@romashevchenko](https://github.com/romashevchenko) Reviews: 32 [@LorhanSohaky](https://github.com/LorhanSohaky) Reviews: 30 [@black-redoc](https://github.com/black-redoc) Reviews: 29 [@pedabraham](https://github.com/pedabraham) Reviews: 28 [@Smlep](https://github.com/Smlep) Reviews: 28 [@dedkot01](https://github.com/dedkot01) Reviews: 28 [@hsuanchi](https://github.com/hsuanchi) Reviews: 28 [@dpinezich](https://github.com/dpinezich) Reviews: 28 [@maoyibo](https://github.com/maoyibo) Reviews: 27 [@0417taehyun](https://github.com/0417taehyun) Reviews: 27 [@BilalAlpaslan](https://github.com/BilalAlpaslan) Reviews: 26 [@junah201](https://github.com/junah201) Reviews: 26 [@zy7y](https://github.com/zy7y) Reviews: 25 [@mycaule](https://github.com/mycaule) Reviews: 25

## Sponsors¶

These are the **Sponsors**. 😎

They are supporting my work with **FastAPI** (and others), mainly through [GitHub Sponsors](https://github.com/sponsors/tiangolo).

### Gold Sponsors¶

### Silver Sponsors¶

### Bronze Sponsors¶

### Individual Sponsors¶

      [@Ponte-Energy-Partners](https://github.com/Ponte-Energy-Partners) [@BoostryJP](https://github.com/BoostryJP) [@acsone](https://github.com/acsone)   [@Trivie](https://github.com/Trivie)   [@takashi-yoneya](https://github.com/takashi-yoneya)   [@mainframeindustries](https://github.com/mainframeindustries)   [@alixlahuec](https://github.com/alixlahuec)   [@primer-io](https://github.com/primer-io)   [@upciti](https://github.com/upciti) [@ChargeStorm](https://github.com/ChargeStorm) [@ibrahimpelumi6142](https://github.com/ibrahimpelumi6142) [@nilslindemann](https://github.com/nilslindemann)   [@samuelcolvin](https://github.com/samuelcolvin) [@otosky](https://github.com/otosky) [@ramonalmeidam](https://github.com/ramonalmeidam) [@roboflow](https://github.com/roboflow) [@dudikbender](https://github.com/dudikbender) [@ehaca](https://github.com/ehaca) [@raphaellaude](https://github.com/raphaellaude) [@timlrx](https://github.com/timlrx) [@Leay15](https://github.com/Leay15) [@jugeeem](https://github.com/jugeeem) [@Karine-Bauch](https://github.com/Karine-Bauch) [@kaoru0310](https://github.com/kaoru0310) [@chickenandstats](https://github.com/chickenandstats) [@patricioperezv](https://github.com/patricioperezv) [@anthonycepeda](https://github.com/anthonycepeda) [@AalbatrossGuy](https://github.com/AalbatrossGuy) [@patsatsia](https://github.com/patsatsia) [@oliverxchen](https://github.com/oliverxchen) [@jaredtrog](https://github.com/jaredtrog) [@Ryandaydev](https://github.com/Ryandaydev) [@gorhack](https://github.com/gorhack) [@mj0331](https://github.com/mj0331) [@anomaly](https://github.com/anomaly) [@aacayaco](https://github.com/aacayaco) [@kennywakeland](https://github.com/kennywakeland) [@zsinx6](https://github.com/zsinx6) [@dblackrun](https://github.com/dblackrun) [@knallgelb](https://github.com/knallgelb) [@dodo5522](https://github.com/dodo5522) [@mintuhouse](https://github.com/mintuhouse) [@falkben](https://github.com/falkben) [@koxudaxi](https://github.com/koxudaxi) [@wshayes](https://github.com/wshayes) [@pamelafox](https://github.com/pamelafox) [@robintw](https://github.com/robintw) [@jstanden](https://github.com/jstanden) [@RaamEEIL](https://github.com/RaamEEIL) [@ashi-agrawal](https://github.com/ashi-agrawal) [@mjohnsey](https://github.com/mjohnsey) [@khadrawy](https://github.com/khadrawy) [@dannywade](https://github.com/dannywade) [@jsoques](https://github.com/jsoques) [@wdwinslow](https://github.com/wdwinslow) [@hiancdtrsnm](https://github.com/hiancdtrsnm) [@Rehket](https://github.com/Rehket) [@FernandoCelmer](https://github.com/FernandoCelmer) [@eseglem](https://github.com/eseglem) [@ternaus](https://github.com/ternaus)   [@Artur-Galstyan](https://github.com/Artur-Galstyan) [@manoelpqueiroz](https://github.com/manoelpqueiroz)   [@pawamoy](https://github.com/pawamoy) [@siavashyj](https://github.com/siavashyj) [@mobyw](https://github.com/mobyw) [@ArtyomVancyan](https://github.com/ArtyomVancyan) [@caviri](https://github.com/caviri) [@hgalytoby](https://github.com/hgalytoby) [@johnl28](https://github.com/johnl28) [@danielunderwood](https://github.com/danielunderwood) [@hoenie-ams](https://github.com/hoenie-ams) [@joerambo](https://github.com/joerambo) [@engineerjoe440](https://github.com/engineerjoe440) [@bnkc](https://github.com/bnkc) [@petercool](https://github.com/petercool) [@PelicanQ](https://github.com/PelicanQ) [@PunRabbit](https://github.com/PunRabbit) [@my3](https://github.com/my3) [@WillHogan](https://github.com/WillHogan) [@miguelgr](https://github.com/miguelgr) [@tochikuji](https://github.com/tochikuji) [@ceb10n](https://github.com/ceb10n) [@slafs](https://github.com/slafs) [@bryanculbertson](https://github.com/bryanculbertson) [@ddanier](https://github.com/ddanier) [@nisutec](https://github.com/nisutec) [@joshuatz](https://github.com/joshuatz) [@TheR1D](https://github.com/TheR1D) [@Zuzah](https://github.com/Zuzah) [@mntolia](https://github.com/mntolia) [@hard-coders](https://github.com/hard-coders) [@DMantis](https://github.com/DMantis) [@xncbf](https://github.com/xncbf) [@moonape1226](https://github.com/moonape1226) [@harsh183](https://github.com/harsh183) [@katnoria](https://github.com/katnoria) [@KentShikama](https://github.com/KentShikama) [@Baghdady92](https://github.com/Baghdady92) [@sdevkota](https://github.com/sdevkota) [@rangulvers](https://github.com/rangulvers)   [@KOZ39](https://github.com/KOZ39) [@rwxd](https://github.com/rwxd) [@morzan1001](https://github.com/morzan1001) [@Olegt0rr](https://github.com/Olegt0rr) [@larsyngvelundin](https://github.com/larsyngvelundin) [@andrecorumba](https://github.com/andrecorumba) [@CoderDeltaLAN](https://github.com/CoderDeltaLAN) [@hippoley](https://github.com/hippoley) [@nayasinghania](https://github.com/nayasinghania) [@onestn](https://github.com/onestn) [@Toothwitch](https://github.com/Toothwitch) [@andreagrandi](https://github.com/andreagrandi) [@msserpa](https://github.com/msserpa)

## About the data - technical details¶

The main intention of this page is to highlight the effort of the community to help others.

Especially including efforts that are normally less visible, and in many cases more arduous, like helping others with questions and reviewing Pull Requests with translations.

The data is calculated each month, you can read the [source code here](https://github.com/fastapi/fastapi/blob/master/scripts/).

Here I'm also highlighting contributions from sponsors.

I also reserve the right to update the algorithm, sections, thresholds, etc (just in case 🤷).

---

# Features¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Features¶

## FastAPI features¶

**FastAPI** gives you the following:

### Based on open standards¶

- [OpenAPI](https://github.com/OAI/OpenAPI-Specification) for API creation, including declarations of path operations, parameters, request bodies, security, etc.
- Automatic data model documentation with [JSON Schema](https://json-schema.org/) (as OpenAPI itself is based on JSON Schema).
- Designed around these standards, after a meticulous study. Instead of an afterthought layer on top.
- This also allows using automatic **client code generation** in many languages.

### Automatic docs¶

Interactive API documentation and exploration web user interfaces. As the framework is based on OpenAPI, there are multiple options, 2 included by default.

- [Swagger UI](https://github.com/swagger-api/swagger-ui), with interactive exploration, call and test your API directly from the browser.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- Alternative API documentation with [ReDoc](https://github.com/Rebilly/ReDoc).

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Just Modern Python¶

It's all based on standard **Python type** declarations (thanks to Pydantic). No new syntax to learn. Just standard modern Python.

If you need a 2 minute refresher of how to use Python types (even if you don't use FastAPI), check the short tutorial: [Python Types](https://fastapi.tiangolo.com/python-types/).

You write standard Python with types:

```
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id

# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

That can then be used like:

```
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

Info

`**second_user_data` means:

Pass the keys and values of the `second_user_data` dict directly as key-value arguments, equivalent to: `User(id=4, name="Mary", joined="2018-11-30")`

### Editor support¶

All the framework was designed to be easy and intuitive to use, all the decisions were tested on multiple editors even before starting development, to ensure the best development experience.

In the Python developer surveys, it's clear [that one of the most used features is "autocompletion"](https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features).

The whole **FastAPI** framework is based to satisfy that. Autocompletion works everywhere.

You will rarely need to come back to the docs.

Here's how your editor might help you:

- in [Visual Studio Code](https://code.visualstudio.com/):

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

- in [PyCharm](https://www.jetbrains.com/pycharm/):

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

You will get completion in code you might even consider impossible before. As for example, the `price` key inside a JSON body (that could have been nested) that comes from a request.

No more typing the wrong key names, coming back and forth between docs, or scrolling up and down to find if you finally used `username` or `user_name`.

### Short¶

It has sensible **defaults** for everything, with optional configurations everywhere. All the parameters can be fine-tuned to do what you need and to define the API you need.

But by default, it all **"just works"**.

### Validation¶

- Validation for most (or all?) Python **data types**, including:
  - JSON objects (`dict`).
  - JSON array (`list`) defining item types.
  - String (`str`) fields, defining min and max lengths.
  - Numbers (`int`, `float`) with min and max values, etc.
- Validation for more exotic types, like:
  - URL.
  - Email.
  - UUID.
  - ...and others.

All the validation is handled by the well-established and robust **Pydantic**.

### Security and authentication¶

Security and authentication integrated. Without any compromise with databases or data models.

All the security schemes defined in OpenAPI, including:

- HTTP Basic.
- **OAuth2** (also with **JWT tokens**). Check the tutorial on [OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/).
- API keys in:
  - Headers.
  - Query parameters.
  - Cookies, etc.

Plus all the security features from Starlette (including **session cookies**).

All built as reusable tools and components that are easy to integrate with your systems, data stores, relational and NoSQL databases, etc.

### Dependency Injection¶

FastAPI includes an extremely easy to use, but extremely powerful **Dependency Injection** system.

- Even dependencies can have dependencies, creating a hierarchy or **"graph" of dependencies**.
- All **automatically handled** by the framework.
- All the dependencies can require data from requests and **augment the path operation** constraints and automatic documentation.
- **Automatic validation** even for *path operation* parameters defined in dependencies.
- Support for complex user authentication systems, **database connections**, etc.
- **No compromise** with databases, frontends, etc. But easy integration with all of them.

### Unlimited "plug-ins"¶

Or in other way, no need for them, import and use the code you need.

Any integration is designed to be so simple to use (with dependencies) that you can create a "plug-in" for your application in 2 lines of code using the same structure and syntax used for your *path operations*.

### Tested¶

- 100% test coverage.
- 100% type annotated code base.
- Used in production applications.

## Starlette features¶

**FastAPI** is fully compatible with (and based on) [Starlette](https://www.starlette.dev/). So, any additional Starlette code you have, will also work.

`FastAPI` is actually a sub-class of `Starlette`. So, if you already know or use Starlette, most of the functionality will work the same way.

With **FastAPI** you get all of **Starlette**'s features (as FastAPI is just Starlette on steroids):

- Seriously impressive performance. It is [one of the fastest Python frameworks available, on par withNodeJSandGo](https://github.com/encode/starlette#performance).
- **WebSocket** support.
- In-process background tasks.
- Startup and shutdown events.
- Test client built on HTTPX.
- **CORS**, GZip, Static Files, Streaming responses.
- **Session and Cookie** support.
- 100% test coverage.
- 100% type annotated codebase.

## Pydantic features¶

**FastAPI** is fully compatible with (and based on) [Pydantic](https://docs.pydantic.dev/). So, any additional Pydantic code you have, will also work.

Including external libraries also based on Pydantic, as ORMs, ODMs for databases.

This also means that in many cases you can pass the same object you get from a request **directly to the database**, as everything is validated automatically.

The same applies the other way around, in many cases you can just pass the object you get from the database **directly to the client**.

With **FastAPI** you get all of **Pydantic**'s features (as FastAPI is based on Pydantic for all the data handling):

- **No brainfuck**:
  - No new schema definition micro-language to learn.
  - If you know Python types you know how to use Pydantic.
- Plays nicely with your **IDE/linter/brain**:
  - Because pydantic data structures are just instances of classes you define; auto-completion, linting, mypy and your intuition should all work properly with your validated data.
- Validate **complex structures**:
  - Use of hierarchical Pydantic models, Python `typing`’s `List` and `Dict`, etc.
  - And validators allow complex data schemas to be clearly and easily defined, checked and documented as JSON Schema.
  - You can have deeply **nested JSON** objects and have them all validated and annotated.
- **Extensible**:
  - Pydantic allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator.
- 100% test coverage.
