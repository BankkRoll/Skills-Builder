# Repository Management Tasks¶ and more

# Repository Management Tasks¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Repository Management Tasks¶

These are the tasks that can be performed to manage the FastAPI repository by [team members](https://fastapi.tiangolo.com/fastapi-people/#team).

Tip

This section is useful only to a handful of people, team members with permissions to manage the repository. You can probably skip it. 😉

...so, you are a [team member of FastAPI](https://fastapi.tiangolo.com/fastapi-people/#team)? Wow, you are so cool! 😎

You can help with everything on [Help FastAPI - Get Help](https://fastapi.tiangolo.com/help-fastapi/) the same ways as external contributors. But additionally, there are some tasks that only you (as part of the team) can perform.

Here are the general instructions for the tasks you can perform.

Thanks a lot for your help. 🙇

## Be Nice¶

First of all, be nice. 😊

You probably are super nice if you were added to the team, but it's worth mentioning it. 🤓

### When Things are Difficult¶

When things are great, everything is easier, so that doesn't need much instructions. But when things are difficult, here are some guidelines.

Try to find the good side. In general, if people are not being unfriendly, try to thank their effort and interest, even if you disagree with the main subject (discussion, PR), just thank them for being interested in the project, or for having dedicated some time to try to do something.

It's difficult to convey emotion in text, use emojis to help. 😅

In discussions and PRs, in many cases, people bring their frustration and show it without filter, in many cases exaggerating, complaining, being entitled, etc. That's really not nice, and when it happens, it lowers our priority to solve their problems. But still, try to breath, and be gentle with your answers.

Try to avoid using bitter sarcasm or potentially passive-aggressive comments. If something is wrong, it's better to be direct (try to be gentle) than sarcastic.

Try to be as specific and objective as possible, avoid generalizations.

For conversations that are more difficult, for example to reject a PR, you can ask me (@tiangolo) to handle it directly.

## Edit PR Titles¶

- Edit the PR title to start with an emoji from [gitmoji](https://gitmoji.dev/).
  - Use the emoji character, not the GitHub code. So, use `🐛` instead of `:bug:`. This is so that it shows up correctly outside of GitHub, for example in the release notes.
  - For translations use the `🌐` emoji ("globe with meridians").
- Start the title with a verb. For example `Add`, `Refactor`, `Fix`, etc. This way the title will say the action that the PR does. Like `Add support for teleporting`, instead of `Teleporting wasn't working, so this PR fixes it`.
- Edit the text of the PR title to start in "imperative", like giving an order. So, instead of `Adding support for teleporting` use `Add support for teleporting`.
- Try to make the title descriptive about what it achieves. If it's a feature, try to describe it, for example `Add support for teleporting` instead of `Create TeleportAdapter class`.
- Do not finish the title with a period (`.`).
- When the PR is for a translation, start with the `🌐` and then `Add {language} translation for` and then the translated file path. For example:

```
🌐 Add Spanish translation for `docs/es/docs/teleporting.md`
```

Once the PR is merged, a GitHub Action ([latest-changes](https://github.com/tiangolo/latest-changes)) will use the PR title to update the latest changes automatically.

So, having a nice PR title will not only look nice in GitHub, but also in the release notes. 📝

## Add Labels to PRs¶

The same GitHub Action [latest-changes](https://github.com/tiangolo/latest-changes) uses one label in the PR to decide the section in the release notes to put this PR in.

Make sure you use a supported label from the [latest-changes list of labels](https://github.com/tiangolo/latest-changes#using-labels):

- `breaking`: Breaking Changes
  - Existing code will break if they update the version without changing their code. This rarely happens, so this label is not frequently used.
- `security`: Security Fixes
  - This is for security fixes, like vulnerabilities. It would almost never be used.
- `feature`: Features
  - New features, adding support for things that didn't exist before.
- `bug`: Fixes
  - Something that was supported didn't work, and this fixes it. There are many PRs that claim to be bug fixes because the user is doing something in an unexpected way that is not supported, but they considered it what should be supported by default. Many of these are actually features or refactors. But in some cases there's an actual bug.
- `refactor`: Refactors
  - This is normally for changes to the internal code that don't change the behavior. Normally it improves maintainability, or enables future features, etc.
- `upgrade`: Upgrades
  - This is for upgrades to direct dependencies from the project, or extra optional dependencies, normally in `pyproject.toml`. So, things that would affect final users, they would end up receiving the upgrade in their code base once they update. But this is not for upgrades to internal dependencies used for development, testing, docs, etc. Those internal dependencies or GitHub Action versions should be marked as `internal`, not `upgrade`.
- `docs`: Docs
  - Changes in docs. This includes updating the docs, fixing typos. But it doesn't include changes to translations.
  - You can normally quickly detect it by going to the "Files changed" tab in the PR and checking if the updated file(s) starts with `docs/en/docs`. The original version of the docs is always in English, so in `docs/en/docs`.
- `lang-all`: Translations
  - Use this for translations. You can normally quickly detect it by going to the "Files changed" tab in the PR and checking if the updated file(s) starts with `docs/{some lang}/docs` but not `docs/en/docs`. For example, `docs/es/docs`.
- `internal`: Internal
  - Use this for changes that only affect how the repo is managed. For example upgrades to internal dependencies, changes in GitHub Actions or scripts, etc.

Tip

Some tools like Dependabot, will add some labels, like `dependencies`, but have in mind that this label is not used by the `latest-changes` GitHub Action, so it won't be used in the release notes. Please make sure one of the labels above is added.

## Add Labels to Translation PRs¶

When there's a PR for a translation, apart from adding the `lang-all` label, also add a label for the language.

There will be a label for each language using the language code, like `lang-{lang code}`, for example, `lang-es` for Spanish, `lang-fr` for French, etc.

- Add the specific language label.
- Add the label `awaiting-review`.

The label `awaiting-review` is special, only used for translations. A GitHub Action will detect it, then it will read the language label, and it will update the GitHub Discussions managing the translations for that language to notify people that there's a new translation to review.

Once a native speaker comes, reviews the PR, and approves it, the GitHub Action will come and remove the `awaiting-review` label, and add the `approved-1` label.

This way, we can notice when there are new translations ready, because they have the `approved-1` label.

## Merge Translation PRs¶

Translations are generated automatically with LLMs and scripts.

There's one GitHub Action that can be manually run to add or update translations for a language: [translate.yml](https://github.com/fastapi/fastapi/actions/workflows/translate.yml).

For these language translation PRs, confirm that:

- The PR was automated (authored by @tiangolo), not made by another user.
- It has the labels `lang-all` and `lang-{lang code}`.
- If the PR is approved by at least one native speaker, you can merge it.

## Review PRs¶

- If a PR doesn't explain what it does or why, if it seems like it could be useful, ask for more information. Otherwise, feel free to close it.
- If a PR seems to be spam, meaningless, only to change statistics (to appear as "contributor") or similar, you can simply mark it as `invalid`, and it will be automatically closed.
- If a PR seems to be AI generated, and seems like reviewing it would take more time from you than the time it took to write the prompt, mark it as `maybe-ai`, and it will be automatically closed.
- A PR should have a specific use case that it is solving.
- If the PR is for a feature, it should have docs.
  - Unless it's a feature we want to discourage, like support for a corner case that we don't want users to use.
- The docs should include a source example file, not write Python directly in Markdown.
- If the source example(s) file can have different syntax for different Python versions, there should be different versions of the file, and they should be shown in tabs in the docs.
- There should be tests testing the source example.
- Before the PR is applied, the new tests should fail.
- After applying the PR, the new tests should pass.
- Coverage should stay at 100%.
- If you see the PR makes sense, or we discussed it and considered it should be accepted, you can add commits on top of the PR to tweak it, to add docs, tests, format, refactor, remove extra files, etc.
- Feel free to comment in the PR to ask for more information, to suggest changes, etc.
- Once you think the PR is ready, move it in the internal GitHub project for me to review it.

## FastAPI People PRs¶

Every month, a GitHub Action updates the FastAPI People data. Those PRs look like this one: [👥 Update FastAPI People](https://github.com/fastapi/fastapi/pull/11669).

If the tests are passing, you can merge it right away.

## Dependabot PRs¶

Dependabot will create PRs to update dependencies for several things, and those PRs all look similar, but some are way more delicate than others.

- If the PR is for a direct dependency, so, Dependabot is modifying `pyproject.toml` in the main dependencies, **don't merge it**. 😱 Let me check it first. There's a good chance that some additional tweaks or updates are needed.
- If the PR updates one of the internal dependencies, for example the group `dev` in `pyproject.toml`, or GitHub Action versions, if the tests are passing, the release notes (shown in a summary in the PR) don't show any obvious potential breaking change, you can merge it. 😎

## Mark GitHub Discussions Answers¶

When a question in GitHub Discussions has been answered, mark the answer by clicking "Mark as answer".

You can filter discussions by [Questionsthat areUnanswered](https://github.com/tiangolo/fastapi/discussions/categories/questions?discussions_q=category:Questions+is:open+is:unanswered).

---

# Repository Management¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Repository Management¶

Here's a short description of how the FastAPI repository is managed and maintained.

## Owner¶

I, [@tiangolo](https://github.com/tiangolo), am the creator and owner of the FastAPI repository. 🤓

I normally give the final review to each PR before merging them. I make the final decisions on the project, I'm the [BDFL](https://en.wikipedia.org/wiki/Benevolent_dictator_for_life). 😅

## Team¶

There's a team of people that help manage and maintain the project. 😎

They have different levels of permissions and [specific instructions](https://fastapi.tiangolo.com/management-tasks/).

Some of the tasks they can perform include:

- Adding labels to PRs.
- Editing PR titles.
- Adding commits on top of PRs to tweak them.
- Mark answers in GitHub Discussions questions, etc.
- Merge some specific types of PRs.

You can see the current team members in [FastAPI People - Team](https://fastapi.tiangolo.com/fastapi-people/#team).

Joining the team is by invitation only, and I could update or remove permissions, instructions, or membership.

## FastAPI Experts¶

The people that help others the most in GitHub Discussions can become [FastAPI Experts](https://fastapi.tiangolo.com/fastapi-people/#fastapi-experts).

This is normally the best way to contribute to the project.

## External Contributions¶

External contributions are very welcome and appreciated, including answering questions, submitting PRs, etc. 🙇‍♂️

There are many ways to [help maintain FastAPI](https://fastapi.tiangolo.com/help-fastapi/#help-maintain-fastapi).

---

# Full Stack FastAPI Template¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Full Stack FastAPI Template¶

Templates, while typically come with a specific setup, are designed to be flexible and customizable. This allows you to modify and adapt them to your project's requirements, making them an excellent starting point. 🏁

You can use this template to get started, as it includes a lot of the initial set up, security, database and some API endpoints already done for you.

GitHub Repository: [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template)

## Full Stack FastAPI Template - Technology Stack and Features¶

- ⚡ [FastAPI](https://fastapi.tiangolo.com) for the Python backend API.
- 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
- 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
- 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
- 🎨 [Tailwind CSS](https://tailwindcss.com) and [shadcn/ui](https://ui.shadcn.com) for the frontend components.
- 🤖 An automatically generated frontend client.
- 🧪 [Playwright](https://playwright.dev) for End-to-End testing.
- 🦇 Dark mode support.
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email based password recovery.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

---

# Python Types Intro¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Python Types Intro¶

Python has support for optional "type hints" (also called "type annotations").

These **"type hints"** or annotations are a special syntax that allow declaring the type of a variable.

By declaring types for your variables, editors and tools can give you better support.

This is just a **quick tutorial / refresher** about Python type hints. It covers only the minimum necessary to use them with **FastAPI**... which is actually very little.

**FastAPI** is all based on these type hints, they give it many advantages and benefits.

But even if you never use **FastAPI**, you would benefit from learning a bit about them.

Note

If you are a Python expert, and you already know everything about type hints, skip to the next chapter.

## Motivation¶

Let's start with a simple example:

 [Python 3.9+](#__tabbed_1_1)

```
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))
```

Calling this program outputs:

```
John Doe
```

The function does the following:

- Takes a `first_name` and `last_name`.
- Converts the first letter of each one to upper case with `title()`.
- Concatenates them with a space in the middle.

 [Python 3.9+](#__tabbed_2_1)

```
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))
```

### Edit it¶

It's a very simple program.

But now imagine that you were writing it from scratch.

At some point you would have started the definition of the function, you had the parameters ready...

But then you have to call "that method that converts the first letter to upper case".

Was it `upper`? Was it `uppercase`? `first_uppercase`? `capitalize`?

Then, you try with the old programmer's friend, editor autocompletion.

You type the first parameter of the function, `first_name`, then a dot (`.`) and then hit `Ctrl+Space` to trigger the completion.

But, sadly, you get nothing useful:

![image](https://fastapi.tiangolo.com/img/python-types/image01.png)

### Add types¶

Let's modify a single line from the previous version.

We will change exactly this fragment, the parameters of the function, from:

```
first_name, last_name
```

to:

```
first_name: str, last_name: str
```

That's it.

Those are the "type hints":

 [Python 3.9+](#__tabbed_3_1)

```
def get_full_name(first_name: str, last_name: str):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))
```

That is not the same as declaring default values like would be with:

```
first_name="john", last_name="doe"
```

It's a different thing.

We are using colons (`:`), not equals (`=`).

And adding type hints normally doesn't change what happens from what would happen without them.

But now, imagine you are again in the middle of creating that function, but with type hints.

At the same point, you try to trigger the autocomplete with `Ctrl+Space` and you see:

![image](https://fastapi.tiangolo.com/img/python-types/image02.png)

With that, you can scroll, seeing the options, until you find the one that "rings a bell":

![image](https://fastapi.tiangolo.com/img/python-types/image03.png)

## More motivation¶

Check this function, it already has type hints:

 [Python 3.9+](#__tabbed_4_1)

```
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + age
    return name_with_age
```

Because the editor knows the types of the variables, you don't only get completion, you also get error checks:

![image](https://fastapi.tiangolo.com/img/python-types/image04.png)

Now you know that you have to fix it, convert `age` to a string with `str(age)`:

 [Python 3.9+](#__tabbed_5_1)

```
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + str(age)
    return name_with_age
```

## Declaring types¶

You just saw the main place to declare type hints. As function parameters.

This is also the main place you would use them with **FastAPI**.

### Simple types¶

You can declare all the standard Python types, not only `str`.

You can use, for example:

- `int`
- `float`
- `bool`
- `bytes`

 [Python 3.9+](#__tabbed_6_1)

```
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_e
```

### Generic types with type parameters¶

There are some data structures that can contain other values, like `dict`, `list`, `set` and `tuple`. And the internal values can have their own type too.

These types that have internal types are called "**generic**" types. And it's possible to declare them, even with their internal types.

To declare those types and the internal types, you can use the standard Python module `typing`. It exists specifically to support these type hints.

#### Newer versions of Python¶

The syntax using `typing` is **compatible** with all versions, from Python 3.6 to the latest ones, including Python 3.9, Python 3.10, etc.

As Python advances, **newer versions** come with improved support for these type annotations and in many cases you won't even need to import and use the `typing` module to declare the type annotations.

If you can choose a more recent version of Python for your project, you will be able to take advantage of that extra simplicity.

In all the docs there are examples compatible with each version of Python (when there's a difference).

For example "**Python 3.6+**" means it's compatible with Python 3.6 or above (including 3.7, 3.8, 3.9, 3.10, etc). And "**Python 3.9+**" means it's compatible with Python 3.9 or above (including 3.10, etc).

If you can use the **latest versions of Python**, use the examples for the latest version, those will have the **best and simplest syntax**, for example, "**Python 3.10+**".

#### List¶

For example, let's define a variable to be a `list` of `str`.

Declare the variable, with the same colon (`:`) syntax.

As the type, put `list`.

As the list is a type that contains some internal types, you put them in square brackets:

 [Python 3.9+](#__tabbed_7_1)

```
def process_items(items: list[str]):
    for item in items:
        print(item)
```

Info

Those internal types in the square brackets are called "type parameters".

In this case, `str` is the type parameter passed to `list`.

That means: "the variable `items` is a `list`, and each of the items in this list is a `str`".

By doing that, your editor can provide support even while processing items from the list:

![image](https://fastapi.tiangolo.com/img/python-types/image05.png)

Without types, that's almost impossible to achieve.

Notice that the variable `item` is one of the elements in the list `items`.

And still, the editor knows it is a `str`, and provides support for that.

#### Tuple and Set¶

You would do the same to declare `tuple`s and `set`s:

 [Python 3.9+](#__tabbed_8_1)

```
def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s
```

This means:

- The variable `items_t` is a `tuple` with 3 items, an `int`, another `int`, and a `str`.
- The variable `items_s` is a `set`, and each of its items is of type `bytes`.

#### Dict¶

To define a `dict`, you pass 2 type parameters, separated by commas.

The first type parameter is for the keys of the `dict`.

The second type parameter is for the values of the `dict`:

 [Python 3.9+](#__tabbed_9_1)

```
def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
```

This means:

- The variable `prices` is a `dict`:
  - The keys of this `dict` are of type `str` (let's say, the name of each item).
  - The values of this `dict` are of type `float` (let's say, the price of each item).

#### Union¶

You can declare that a variable can be any of **several types**, for example, an `int` or a `str`.

In Python 3.6 and above (including Python 3.10) you can use the `Union` type from `typing` and put inside the square brackets the possible types to accept.

In Python 3.10 there's also a **new syntax** where you can put the possible types separated by a vertical bar (`|`).

 [Python 3.10+](#__tabbed_10_1)[Python 3.9+](#__tabbed_10_2)

```
def process_item(item: int | str):
    print(item)
```

```
from typing import Union

def process_item(item: Union[int, str]):
    print(item)
```

In both cases this means that `item` could be an `int` or a `str`.

#### PossiblyNone¶

You can declare that a value could have a type, like `str`, but that it could also be `None`.

In Python 3.6 and above (including Python 3.10) you can declare it by importing and using `Optional` from the `typing` module.

```
from typing import Optional

def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
```

Using `Optional[str]` instead of just `str` will let the editor help you detect errors where you could be assuming that a value is always a `str`, when it could actually be `None` too.

`Optional[Something]` is actually a shortcut for `Union[Something, None]`, they are equivalent.

This also means that in Python 3.10, you can use `Something | None`:

 [Python 3.10+](#__tabbed_11_1)[Python 3.9+](#__tabbed_11_2)[Python 3.9+ alternative](#__tabbed_11_3)

```
def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
```

```
from typing import Optional

def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
```

```
from typing import Union

def say_hi(name: Union[str, None] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
```

#### UsingUnionorOptional¶

If you are using a Python version below 3.10, here's a tip from my very **subjective** point of view:

- 🚨 Avoid using `Optional[SomeType]`
- Instead ✨ **useUnion[SomeType, None]** ✨.

Both are equivalent and underneath they are the same, but I would recommend `Union` instead of `Optional` because the word "**optional**" would seem to imply that the value is optional, and it actually means "it can be `None`", even if it's not optional and is still required.

I think `Union[SomeType, None]` is more explicit about what it means.

It's just about the words and names. But those words can affect how you and your teammates think about the code.

As an example, let's take this function:

 [Python 3.9+](#__tabbed_12_1)

```
from typing import Optional

def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

     🤓 Other versions and variants [Python 3.10+](#__tabbed_13_1)

```
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

The parameter `name` is defined as `Optional[str]`, but it is **not optional**, you cannot call the function without the parameter:

```
say_hi()  # Oh, no, this throws an error! 😱
```

The `name` parameter is **still required** (not *optional*) because it doesn't have a default value. Still, `name` accepts `None` as the value:

```
say_hi(name=None)  # This works, None is valid 🎉
```

The good news is, once you are on Python 3.10 you won't have to worry about that, as you will be able to simply use `|` to define unions of types:

 [Python 3.10+](#__tabbed_14_1)

```
def say_hi(name: str | None):
    print(f"Hey {name}!")
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_15_1)

```
from typing import Optional

def say_hi(name: Optional[str]):
    print(f"Hey {name}!")
```

And then you won't have to worry about names like `Optional` and `Union`. 😎

#### Generic types¶

These types that take type parameters in square brackets are called **Generic types** or **Generics**, for example:

 [Python 3.10+](#__tabbed_16_1)[Python 3.9+](#__tabbed_16_2)

You can use the same builtin types as generics (with square brackets and types inside):

- `list`
- `tuple`
- `set`
- `dict`

And the same as with previous Python versions, from the `typing` module:

- `Union`
- `Optional`
- ...and others.

In Python 3.10, as an alternative to using the generics `Union` and `Optional`, you can use the vertical bar (`|`) to declare unions of types, that's a lot better and simpler.

You can use the same builtin types as generics (with square brackets and types inside):

- `list`
- `tuple`
- `set`
- `dict`

And generics from the `typing` module:

- `Union`
- `Optional`
- ...and others.

### Classes as types¶

You can also declare a class as the type of a variable.

Let's say you have a class `Person`, with a name:

 [Python 3.9+](#__tabbed_17_1)

```
class Person:
    def __init__(self, name: str):
        self.name = name

def get_person_name(one_person: Person):
    return one_person.name
```

Then you can declare a variable to be of type `Person`:

 [Python 3.9+](#__tabbed_18_1)

```
class Person:
    def __init__(self, name: str):
        self.name = name

def get_person_name(one_person: Person):
    return one_person.name
```

And then, again, you get all the editor support:

![image](https://fastapi.tiangolo.com/img/python-types/image06.png)

Notice that this means "`one_person` is an **instance** of the class `Person`".

It doesn't mean "`one_person` is the **class** called `Person`".

## Pydantic models¶

[Pydantic](https://docs.pydantic.dev/) is a Python library to perform data validation.

You declare the "shape" of the data as classes with attributes.

And each attribute has a type.

Then you create an instance of that class with some values and it will validate the values, convert them to the appropriate type (if that's the case) and give you an object with all the data.

And you get all the editor support with that resulting object.

An example from the official Pydantic docs:

 [Python 3.10+](#__tabbed_19_1)

```
from datetime import datetime

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
```

     🤓 Other versions and variants [Python 3.9+](#__tabbed_20_1)

```
from datetime import datetime
from typing import Union

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: Union[datetime, None] = None
    friends: list[int] = []

external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
```

Info

To learn more about [Pydantic, check its docs](https://docs.pydantic.dev/).

**FastAPI** is all based on Pydantic.

You will see a lot more of all this in practice in the [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/).

Tip

Pydantic has a special behavior when you use `Optional` or `Union[Something, None]` without a default value, you can read more about it in the Pydantic docs about [Required Optional fields](https://docs.pydantic.dev/2.3/usage/models/#required-fields).

## Type Hints with Metadata Annotations¶

Python also has a feature that allows putting **additionalmetadata** in these type hints using `Annotated`.

Since Python 3.9, `Annotated` is a part of the standard library, so you can import it from `typing`.

 [Python 3.9+](#__tabbed_21_1)

```
from typing import Annotated

def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"
```

Python itself doesn't do anything with this `Annotated`. And for editors and other tools, the type is still `str`.

But you can use this space in `Annotated` to provide **FastAPI** with additional metadata about how you want your application to behave.

The important thing to remember is that **the firsttype parameter** you pass to `Annotated` is the **actual type**. The rest, is just metadata for other tools.

For now, you just need to know that `Annotated` exists, and that it's standard Python. 😎

Later you will see how **powerful** it can be.

Tip

The fact that this is **standard Python** means that you will still get the **best possible developer experience** in your editor, with the tools you use to analyze and refactor your code, etc. ✨

And also that your code will be very compatible with many other Python tools and libraries. 🚀

## Type hints inFastAPI¶

**FastAPI** takes advantage of these type hints to do several things.

With **FastAPI** you declare parameters with type hints and you get:

- **Editor support**.
- **Type checks**.

...and **FastAPI** uses the same declarations to:

- **Define requirements**: from request path parameters, query parameters, headers, bodies, dependencies, etc.
- **Convert data**: from the request to the required type.
- **Validate data**: coming from each request:
  - Generating **automatic errors** returned to the client when the data is invalid.
- **Document** the API using OpenAPI:
  - which is then used by the automatic interactive documentation user interfaces.

This might all sound abstract. Don't worry. You'll see all this in action in the [Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/).

The important thing is that by using standard Python types, in a single place (instead of adding more classes, decorators, etc), **FastAPI** will do a lot of the work for you.

Info

If you already went through all the tutorial and came back to see more about types, a good resource is [the "cheat sheet" frommypy](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html).

---

# Reference¶

> FastAPI framework, high performance, easy to learn, fast to code, ready for production

# Reference¶

Here's the reference or code API, the classes, functions, parameters, attributes, and
all the FastAPI parts you can use in your applications.

If you want to **learn FastAPI** you are much better off reading the
[FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/).
