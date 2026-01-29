# Writing your first contribution for Django¶ and more

# Writing your first contribution for Django¶

# Writing your first contribution for Django¶

## Introduction¶

Interested in giving back to the community a little? Maybe you’ve found a bug
in Django that you’d like to see fixed, or maybe there’s a small feature you
want added.

Contributing back to Django itself is the best way to see your own concerns
addressed. This may seem daunting at first, but it’s a well-traveled path with
documentation, tooling, and a community to support you. We’ll walk you through
the entire process, so you can learn by example.

### Who’s this tutorial for?¶

See also

If you are looking for a reference on the details of making code
contributions, see the [Writing code](https://docs.djangoproject.com/en/internals/contributing/writing-code/)
documentation.

For this tutorial, we expect that you have at least a basic understanding of
how Django works. This means you should be comfortable going through the
existing tutorials on [writing your first Django app](https://docs.djangoproject.com/en/5.0/tutorial01/).
In addition, you should have a good understanding of Python itself. But if you
don’t, [Dive Into Python](https://diveintopython3.net/) is a fantastic (and free) online book for beginning
Python programmers.

Those of you who are unfamiliar with version control systems and Trac will find
that this tutorial and its links include just enough information to get started.
However, you’ll probably want to read some more about these different tools if
you plan on contributing to Django regularly.

For the most part though, this tutorial tries to explain as much as possible,
so that it can be of use to the widest audience.

Where to get help:

If you’re having trouble going through this tutorial, please post a message
on the [Django Forum](https://forum.djangoproject.com/), [django-developers](https://docs.djangoproject.com/en/internals/mailing-lists/#django-developers-mailing-list), or drop by
[#django-dev on irc.libera.chat](https://web.libera.chat/#django-dev) to chat with other Django users who
might be able to help.

### What does this tutorial cover?¶

We’ll be walking you through contributing to Django for the first time.
By the end of this tutorial, you should have a basic understanding of both the
tools and the processes involved. Specifically, we’ll be covering the following:

- Installing Git.
- Downloading a copy of Django’s development version.
- Running Django’s test suite.
- Writing a test for your changes.
- Writing the code for your changes.
- Testing your changes.
- Submitting a pull request.
- Where to look for more information.

Once you’re done with the tutorial, you can look through the rest of
[Django’s documentation on contributing](https://docs.djangoproject.com/en/internals/contributing/).
It contains lots of great information and is a must read for anyone who’d like
to become a regular contributor to Django. If you’ve got questions, it’s
probably got the answers.

Python 3 required!

The current version of Django doesn’t support Python 2.7. Get Python 3 at
[Python’s download page](https://www.python.org/downloads/) or with your
operating system’s package manager.

For Windows users

See [Install Python](https://docs.djangoproject.com/en/howto/windows/#install-python-windows) on Windows docs for additional guidance.

## Code of Conduct¶

As a contributor, you can help us keep the Django community open and inclusive.
Please read and follow our [Code of Conduct](https://www.djangoproject.com/conduct/).

## Installing Git¶

For this tutorial, you’ll need Git installed to download the current
development version of Django and to generate a branch for the changes you
make.

To check whether or not you have Git installed, enter `git` into the command
line. If you get messages saying that this command could not be found, you’ll
have to download and install it, see [Git’s download page](https://git-scm.com/download).

If you’re not that familiar with Git, you can always find out more about its
commands (once it’s installed) by typing `git help` into the command line.

## Getting a copy of Django’s development version¶

The first step to contributing to Django is to get a copy of the source code.
First, [fork Django on GitHub](https://github.com/django/django/fork). Then,
from the command line, use the `cd` command to navigate to the directory
where you’ll want your local copy of Django to live.

Download the Django source code repository using the following command:

   /  

```
$ git clone https://github.com/YourGitHubName/django.git
```

```
...\> git clone https://github.com/YourGitHubName/django.git
```

Low bandwidth connection?

You can add the `--depth 1` argument to `git clone` to skip downloading
all of Django’s commit history, which reduces data transfer from  ~250 MB
to ~70 MB.

Now that you have a local copy of Django, you can install it just like you would
install any package using `pip`. The most convenient way to do so is by using
a *virtual environment*, which is a feature built into Python that allows you
to keep a separate directory of installed packages for each of your projects so
that they don’t interfere with each other.

It’s a good idea to keep all your virtual environments in one place, for
example in `.virtualenvs/` in your home directory.

Create a new virtual environment by running:

   /  

```
$ python3 -m venv ~/.virtualenvs/djangodev
```

```
...\> py -m venv %HOMEPATH%\.virtualenvs\djangodev
```

The path is where the new environment will be saved on your computer.

The final step in setting up your virtual environment is to activate it:

```
$ source ~/.virtualenvs/djangodev/bin/activate
```

If the `source` command is not available, you can try using a dot instead:

```
$ . ~/.virtualenvs/djangodev/bin/activate
```

You have to activate the virtual environment whenever you open a new
terminal window.

For Windows users

To activate your virtual environment on Windows, run:

```
...\> %HOMEPATH%\.virtualenvs\djangodev\Scripts\activate.bat
```

The name of the currently activated virtual environment is displayed on the
command line to help you keep track of which one you are using. Anything you
install through `pip` while this name is displayed will be installed in that
virtual environment, isolated from other environments and system-wide packages.

Go ahead and install the previously cloned copy of Django:

   /  

```
$ python -m pip install -e /path/to/your/local/clone/django/
```

```
...\> py -m pip install -e \path\to\your\local\clone\django\
```

The installed version of Django is now pointing at your local copy by installing
in editable mode. You will immediately see any changes you make to it, which is
of great help when writing your first contribution.

### Creating projects with a local copy of Django¶

It may be helpful to test your local changes with a Django project. First you
have to create a new virtual environment, [install the previously cloned
local copy of Django in editable mode](#intro-contributing-install-local-copy),
and create a new Django project outside of your local copy of Django. You will
immediately see any changes you make to Django in your new project, which is
of great help when writing your first contribution, especially if testing
any changes to the UI.

You can follow the [tutorial](https://docs.djangoproject.com/en/5.0/tutorial01/) for help in creating a
Django project.

## Running Django’s test suite for the first time¶

When contributing to Django it’s very important that your code changes don’t
introduce bugs into other areas of Django. One way to check that Django still
works after you make your changes is by running Django’s test suite. If all
the tests still pass, then you can be reasonably sure that your changes
work and haven’t broken other parts of Django. If you’ve never run Django’s test
suite before, it’s a good idea to run it once beforehand to get familiar with
its output.

Before running the test suite, enter the Django `tests/` directory using the
`cd tests` command, and install test dependencies by running:

   /  

```
$ python -m pip install -r requirements/py3.txt
```

```
...\> py -m pip install -r requirements\py3.txt
```

If you encounter an error during the installation, your system might be missing
a dependency for one or more of the Python packages. Consult the failing
package’s documentation or search the web with the error message that you
encounter.

Now we are ready to run the test suite. If you’re using GNU/Linux, macOS, or
some other flavor of Unix, run:

   /  

```
$ ./runtests.py
```

```
...\> runtests.py
```

Now sit back and relax. Django’s entire test suite has thousands of tests, and
it takes at least a few minutes to run, depending on the speed of your
computer.

While Django’s test suite is running, you’ll see a stream of characters
representing the status of each test as it completes. `E` indicates that an
error was raised during a test, and `F` indicates that a test’s assertions
failed. Both of these are considered to be test failures. Meanwhile, `x` and
`s` indicated expected failures and skipped tests, respectively. Dots indicate
passing tests.

Skipped tests are typically due to missing external libraries required to run
the test; see [Running all the tests](https://docs.djangoproject.com/en/internals/contributing/writing-code/unit-tests/#running-unit-tests-dependencies) for a list of dependencies
and be sure to install any for tests related to the changes you are making (we
won’t need any for this tutorial). Some tests are specific to a particular
database backend and will be skipped if not testing with that backend. SQLite
is the database backend for the default settings. To run the tests using a
different backend, see [Using another settings module](https://docs.djangoproject.com/en/internals/contributing/writing-code/unit-tests/#running-unit-tests-settings).

Once the tests complete, you should be greeted with a message informing you
whether the test suite passed or failed. Since you haven’t yet made any changes
to Django’s code, the entire test suite **should** pass. If you get failures or
errors make sure you’ve followed all of the previous steps properly. See
[Running the unit tests](https://docs.djangoproject.com/en/internals/contributing/writing-code/unit-tests/#running-unit-tests) for more information.

Note that the latest Django “main” branch may not always be stable. When
developing against “main”, you can check [Django’s continuous integration
builds](https://djangoci.com) to determine if the failures are specific to your machine or if they
are also present in Django’s official builds. If you click to view a particular
build, you can view the “Configuration Matrix” which shows failures broken down
by Python version and database backend.

Note

For this tutorial and the ticket we’re working on, testing against SQLite
is sufficient, however, it’s possible (and sometimes necessary) to
[run the tests using a different database](https://docs.djangoproject.com/en/internals/contributing/writing-code/unit-tests/#running-unit-tests-settings). When making UI changes, you will need to
[run the Selenium tests](https://docs.djangoproject.com/en/internals/contributing/writing-code/unit-tests/#running-selenium-tests).

## Working on a feature¶

For this tutorial, we’ll work on a “fake ticket” as a case study. Here are the
imaginary details:

Ticket #99999 – Allow making toast

Django should provide a function `django.shortcuts.make_toast()` that
returns `'toast'`.

We’ll now implement this feature and associated tests.

## Creating a branch¶

Before making any changes, create a new branch for the ticket:

   /  

```
$ git checkout -b ticket_99999
```

```
...\> git checkout -b ticket_99999
```

You can choose any name that you want for the branch, “ticket_99999” is an
example. All changes made in this branch will be specific to the ticket and
won’t affect the main copy of the code that we cloned earlier.

## Writing some tests for your ticket¶

In most cases, for a contribution to be accepted into Django it has to include
tests. For bug fix contributions, this means writing a regression test to
ensure that  the bug is never reintroduced into Django later on. A regression
test should be written in such a way that it will fail while the bug still
exists and pass once the bug has been fixed. For contributions containing new
features, you’ll need to include tests which ensure that the new features are
working correctly. They too should fail when the new feature is not present,
and then pass once it has been implemented.

A good way to do this is to write your new tests first, before making any
changes to the code. This style of development is called
[test-driven development](https://en.wikipedia.org/wiki/Test-driven_development) and can be applied to both entire projects and
single changes. After writing your tests, you then run them to make sure that
they do indeed fail (since you haven’t fixed that bug or added that feature
yet). If your new tests don’t fail, you’ll need to fix them so that they do.
After all, a regression test that passes regardless of whether a bug is present
is not very helpful at preventing that bug from reoccurring down the road.

Now for our hands-on example.

### Writing a test for ticket #99999¶

In order to resolve this ticket, we’ll add a `make_toast()` function to the
`django.shortcuts` module. First we are going to write a test that tries to
use the function and check that its output looks correct.

Navigate to Django’s `tests/shortcuts/` folder and create a new file
`test_make_toast.py`. Add the following code:

```
from django.shortcuts import make_toast
from django.test import SimpleTestCase

class MakeToastTests(SimpleTestCase):
    def test_make_toast(self):
        self.assertEqual(make_toast(), "toast")
```

This test checks that the `make_toast()` returns `'toast'`.

But this testing thing looks kinda hard…

If you’ve never had to deal with tests before, they can look a little hard
to write at first glance. Fortunately, testing is a *very* big subject in
computer programming, so there’s lots of information out there:

- A good first look at writing tests for Django can be found in the
  documentation on [Writing and running tests](https://docs.djangoproject.com/en/topics/testing/overview/).
- Dive Into Python (a free online book for beginning Python developers)
  includes a great [introduction to Unit Testing](https://diveintopython3.net/unit-testing.html).
- After reading those, if you want something a little meatier to sink
  your teeth into, there’s always the Python [unittest](https://docs.python.org/3/library/unittest.html#module-unittest) documentation.

### Running your new test¶

Since we haven’t made any modifications to `django.shortcuts` yet, our test
should fail. Let’s run all the tests in the `shortcuts` folder to make sure
that’s really what happens. `cd` to the Django `tests/` directory and run:

   /  

```
$ ./runtests.py shortcuts
```

```
...\> runtests.py shortcuts
```

If the tests ran correctly, you should see one failure corresponding to the test
method we added, with this error:

```
ImportError: cannot import name 'make_toast' from 'django.shortcuts'
```

If all of the tests passed, then you’ll want to make sure that you added the
new test shown above to the appropriate folder and file name.

## Writing the code for your ticket¶

Next we’ll be adding the `make_toast()` function.

Navigate to the `django/` folder and open the `shortcuts.py` file. At the
bottom, add:

```
def make_toast():
    return "toast"
```

Now we need to make sure that the test we wrote earlier passes, so we can see
whether the code we added is working correctly. Again, navigate to the Django
`tests/` directory and run:

   /  

```
$ ./runtests.py shortcuts
```

```
...\> runtests.py shortcuts
```

Everything should pass. If it doesn’t, make sure you correctly added the
function to the correct file.

## Running Django’s test suite for the second time¶

Once you’ve verified that your changes and test are working correctly, it’s
a good idea to run the entire Django test suite to verify that your change
hasn’t introduced any bugs into other areas of Django. While successfully
passing the entire test suite doesn’t guarantee your code is bug free, it does
help identify many bugs and regressions that might otherwise go unnoticed.

To run the entire Django test suite, `cd` into the Django `tests/`
directory and run:

   /  

```
$ ./runtests.py
```

```
...\> runtests.py
```

## Writing Documentation¶

This is a new feature, so it should be documented. Open the file
`docs/topics/http/shortcuts.txt` and add the following at the end of the
file:

```
``make_toast()``
================

.. function:: make_toast()

.. versionadded:: 2.2

Returns ``'toast'``.
```

Since this new feature will be in an upcoming release it is also added to the
release notes for the next version of Django. Open the release notes for the
latest version in `docs/releases/`, which at time of writing is `2.2.txt`.
Add a note under the “Minor Features” header:

```
:mod:`django.shortcuts`
~~~~~~~~~~~~~~~~~~~~~~~

* The new :func:`django.shortcuts.make_toast` function returns ``'toast'``.
```

For more information on writing documentation, including an explanation of what
the `versionadded` bit is all about, see
[Writing documentation](https://docs.djangoproject.com/en/internals/contributing/writing-documentation/). That page also includes
an explanation of how to build a copy of the documentation locally, so you can
preview the HTML that will be generated.

## Previewing your changes¶

Now it’s time to review the changes made in the branch. To stage all the
changes ready for commit, run:

   /  

```
$ git add --all
```

```
...\> git add --all
```

Then display the differences between your current copy of Django (with your
changes) and the revision that you initially checked out earlier in the
tutorial with:

   /  

```
$ git diff --cached
```

```
...\> git diff --cached
```

Use the arrow keys to move up and down.

```
diff --git a/django/shortcuts.py b/django/shortcuts.py
index 7ab1df0e9d..8dde9e28d9 100644
--- a/django/shortcuts.py
+++ b/django/shortcuts.py
@@ -156,3 +156,7 @@ def resolve_url(to, *args, **kwargs):

     # Finally, fall back and assume it's a URL
     return to
+
+
+def make_toast():
+    return 'toast'
diff --git a/docs/releases/2.2.txt b/docs/releases/2.2.txt
index 7d85d30c4a..81518187b3 100644
--- a/docs/releases/2.2.txt
+++ b/docs/releases/2.2.txt
@@ -40,6 +40,11 @@ database constraints. Constraints are added to models using the
 Minor features
 --------------

+:mod:`django.shortcuts`
+~~~~~~~~~~~~~~~~~~~~~~~
+
+* The new :func:`django.shortcuts.make_toast` function returns ``'toast'``.
+
 :mod:`django.contrib.admin`
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~

diff --git a/docs/topics/http/shortcuts.txt b/docs/topics/http/shortcuts.txt
index 7b3a3a2c00..711bf6bb6d 100644
--- a/docs/topics/http/shortcuts.txt
+++ b/docs/topics/http/shortcuts.txt
@@ -271,3 +271,12 @@ This example is equivalent to::
         my_objects = list(MyModel.objects.filter(published=True))
         if not my_objects:
             raise Http404("No MyModel matches the given query.")
+
+``make_toast()``
+================
+
+.. function:: make_toast()
+
+.. versionadded:: 2.2
+
+Returns ``'toast'``.
diff --git a/tests/shortcuts/test_make_toast.py b/tests/shortcuts/test_make_toast.py
new file mode 100644
index 0000000000..6f4c627b6e
--- /dev/null
+++ b/tests/shortcuts/test_make_toast.py
@@ -0,0 +1,7 @@
+from django.shortcuts import make_toast
+from django.test import SimpleTestCase
+
+
+class MakeToastTests(SimpleTestCase):
+    def test_make_toast(self):
+        self.assertEqual(make_toast(), 'toast')
```

When you’re done previewing the changes, hit the `q` key to return to the
command line. If the diff looked okay, it’s time to commit the changes.

## Committing the changes¶

To commit the changes:

   /  

```
$ git commit
```

```
...\> git commit
```

This opens up a text editor to type the commit message. Follow the [commit
message guidelines](https://docs.djangoproject.com/en/internals/contributing/committing-code/#committing-guidelines) and write a message like:

```
Fixed #99999 -- Added a shortcut function to make toast.
```

## Pushing the commit and making a pull request¶

After committing the changes, send it to your fork on GitHub (substitute
“ticket_99999” with the name of your branch if it’s different):

   /  

```
$ git push origin ticket_99999
```

```
...\> git push origin ticket_99999
```

You can create a pull request by visiting the [Django GitHub page](https://github.com/django/django/). You’ll see your branch under “Your
recently pushed branches”. Click “Compare & pull request” next to it.

Please don’t do it for this tutorial, but on the next page that displays a
preview of the changes, you would click “Create pull request”.

## Next steps¶

Congratulations, you’ve learned how to make a pull request to Django! Details
of more advanced techniques you may need are in
[Working with Git and GitHub](https://docs.djangoproject.com/en/internals/contributing/writing-code/working-with-git/).

Now you can put those skills to good use by helping to improve Django’s
codebase.

### More information for new contributors¶

Before you get too into contributing to Django, there’s a little more
information on contributing that you should probably take a look at:

- You should make sure to read Django’s documentation on
  [claiming tickets and submitting pull requests](https://docs.djangoproject.com/en/internals/contributing/writing-code/submitting-patches/).
  It covers Trac etiquette, how to claim tickets for yourself, expected
  coding style (both for code and docs), and many other important details.
- First time contributors should also read Django’s [documentation
  for first time contributors](https://docs.djangoproject.com/en/internals/contributing/new-contributors/).
  It has lots of good advice for those of us who are new to helping out
  with Django.
- After those, if you’re still hungry for more information about
  contributing, you can always browse through the rest of
  [Django’s documentation on contributing](https://docs.djangoproject.com/en/internals/contributing/).
  It contains a ton of useful information and should be your first source
  for answering any questions you might have.

### Finding your first real ticket¶

Once you’ve looked through some of that information, you’ll be ready to go out
and find a ticket of your own to contribute to. Pay special attention to
tickets with the “easy pickings” criterion. These tickets are often much
simpler in nature and are great for first time contributors. Once you’re
familiar with contributing to Django, you can start working on more difficult
and complicated tickets.

If you just want to get started already (and nobody would blame you!), try
taking a look at the list of [easy tickets without a branch](https://code.djangoproject.com/query?status=new&status=reopened&has_patch=0&easy=1&col=id&col=summary&col=status&col=owner&col=type&col=milestone&order=priority) and the
[easy tickets that have branches which need improvement](https://code.djangoproject.com/query?status=new&status=reopened&needs_better_patch=1&easy=1&col=id&col=summary&col=status&col=owner&col=type&col=milestone&order=priority). If you’re familiar
with writing tests, you can also look at the list of
[easy tickets that need tests](https://code.djangoproject.com/query?status=new&status=reopened&needs_tests=1&easy=1&col=id&col=summary&col=status&col=owner&col=type&col=milestone&order=priority). Remember to follow the guidelines about
claiming tickets that were mentioned in the link to Django’s documentation on
[claiming tickets and submitting branches](https://docs.djangoproject.com/en/internals/contributing/writing-code/submitting-patches/).

### What’s next after creating a pull request?¶

After a ticket has a branch, it needs to be reviewed by a second set of eyes.
After submitting a pull request, update the ticket metadata by setting the
flags on the ticket to say “has patch”, “doesn’t need tests”, etc, so others
can find it for review. Contributing doesn’t necessarily always mean writing
code from scratch. Reviewing open pull requests is also a very helpful
contribution. See [Triaging tickets](https://docs.djangoproject.com/en/internals/contributing/triaging-tickets/) for details.

---

# Quick install guide¶

# Quick install guide¶

Before you can use Django, you’ll need to get it installed. We have a
[complete installation guide](https://docs.djangoproject.com/en/topics/install/) that covers all the
possibilities; this guide will guide you to a minimal installation that’ll work
while you walk through the introduction.

## Install Python¶

Being a Python web framework, Django requires Python. See
[What Python version can I use with Django?](https://docs.djangoproject.com/en/faq/install/#faq-python-version-support) for details. Python includes a lightweight
database called [SQLite](https://www.sqlite.org/) so you won’t need to set up a database just yet.

Get the latest version of Python at [https://www.python.org/downloads/](https://www.python.org/downloads/) or with
your operating system’s package manager.

You can verify that Python is installed by typing `python` from your shell;
you should see something like:

```
Python 3.x.y
[GCC 4.x] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Set up a database¶

This step is only necessary if you’d like to work with a “large” database engine
like PostgreSQL, MariaDB, MySQL, or Oracle. To install such a database, consult
the [database installation information](https://docs.djangoproject.com/en/topics/install/#database-installation).

## Install Django¶

You’ve got three options to install Django:

- [Install an official release](https://docs.djangoproject.com/en/topics/install/#installing-official-release). This
  is the best approach for most users.
- Install a version of Django [provided by your operating system
  distribution](https://docs.djangoproject.com/en/topics/install/#installing-distribution-package).
- [Install the latest development version](https://docs.djangoproject.com/en/topics/install/#installing-development-version). This option is for enthusiasts who want
  the latest-and-greatest features and aren’t afraid of running brand new code.
  You might encounter new bugs in the development version, but reporting them
  helps the development of Django. Also, releases of third-party packages are
  less likely to be compatible with the development version than with the
  latest stable release.

Always refer to the documentation that corresponds to the
version of Django you’re using!

If you do either of the first two steps, keep an eye out for parts of the
documentation marked **new in development version**. That phrase flags
features that are only available in development versions of Django, and
they likely won’t work with an official release.

## Verifying¶

To verify that Django can be seen by Python, type `python` from your shell.
Then at the Python prompt, try to import Django:

```
>>> import django
>>> print(django.get_version())
5.0
```

You may have another version of Django installed.

## That’s it!¶

That’s it – you can now [move onto the tutorial](https://docs.djangoproject.com/en/5.0/tutorial01/).

---

# Django at a glance¶

# Django at a glance¶

Because Django was developed in a fast-paced newsroom environment, it was
designed to make common web development tasks fast and easy. Here’s an informal
overview of how to write a database-driven web app with Django.

The goal of this document is to give you enough technical specifics to
understand how Django works, but this isn’t intended to be a tutorial or
reference – but we’ve got both! When you’re ready to start a project, you can
[start with the tutorial](https://docs.djangoproject.com/en/5.0/tutorial01/) or [dive right into more
detailed documentation](https://docs.djangoproject.com/en/topics/).

## Design your model¶

Although you can use Django without a database, it comes with an
[object-relational mapper](https://en.wikipedia.org/wiki/Object-relational_mapping) in which you describe your database layout in Python
code.

The [data-model syntax](https://docs.djangoproject.com/en/topics/db/models/) offers many rich ways of
representing your models – so far, it’s been solving many years’ worth of
database-schema problems. Here’s a quick example:

  `mysite/news/models.py`[¶](#id1)

```
from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline
```

## Install it¶

Next, run the Django command-line utilities to create the database tables
automatically:

   /  

```
$ python manage.py makemigrations
$ python manage.py migrate
```

```
...\> py manage.py makemigrations
...\> py manage.py migrate
```

The [makemigrations](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-makemigrations) command looks at all your available models and
creates migrations for whichever tables don’t already exist. [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate)
runs the migrations and creates tables in your database, as well as optionally
providing [much richer schema control](https://docs.djangoproject.com/en/topics/migrations/).

## Enjoy the free API¶

With that, you’ve got a free, and rich, [Python API](https://docs.djangoproject.com/en/topics/db/queries/)
to access your data. The API is created on the fly, no code generation
necessary:

```
# Import the models we created from our "news" app
>>> from news.models import Article, Reporter

# No reporters are in the system yet.
>>> Reporter.objects.all()
<QuerySet []>

# Create a new Reporter.
>>> r = Reporter(full_name="John Smith")

# Save the object into the database. You have to call save() explicitly.
>>> r.save()

# Now it has an ID.
>>> r.id
1

# Now the new reporter is in the database.
>>> Reporter.objects.all()
<QuerySet [<Reporter: John Smith>]>

# Fields are represented as attributes on the Python object.
>>> r.full_name
'John Smith'

# Django provides a rich database lookup API.
>>> Reporter.objects.get(id=1)
<Reporter: John Smith>
>>> Reporter.objects.get(full_name__startswith="John")
<Reporter: John Smith>
>>> Reporter.objects.get(full_name__contains="mith")
<Reporter: John Smith>
>>> Reporter.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Reporter matching query does not exist.

# Create an article.
>>> from datetime import date
>>> a = Article(
...     pub_date=date.today(), headline="Django is cool", content="Yeah.", reporter=r
... )
>>> a.save()

# Now the article is in the database.
>>> Article.objects.all()
<QuerySet [<Article: Django is cool>]>

# Article objects get API access to related Reporter objects.
>>> r = a.reporter
>>> r.full_name
'John Smith'

# And vice versa: Reporter objects get API access to Article objects.
>>> r.article_set.all()
<QuerySet [<Article: Django is cool>]>

# The API follows relationships as far as you need, performing efficient
# JOINs for you behind the scenes.
# This finds all articles by a reporter whose name starts with "John".
>>> Article.objects.filter(reporter__full_name__startswith="John")
<QuerySet [<Article: Django is cool>]>

# Change an object by altering its attributes and calling save().
>>> r.full_name = "Billy Goat"
>>> r.save()

# Delete an object with delete().
>>> r.delete()
```

## A dynamic admin interface: it’s not just scaffolding – it’s the whole house¶

Once your models are defined, Django can automatically create a professional,
production ready [administrative interface](https://docs.djangoproject.com/en/ref/contrib/admin/) –
a website that lets authenticated users add, change and delete objects. The
only step required is to register your model in the admin site:

  `mysite/news/models.py`[¶](#id2)

```
from django.db import models

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
```

    `mysite/news/admin.py`[¶](#id3)

```
from django.contrib import admin

from . import models

admin.site.register(models.Article)
```

The philosophy here is that your site is edited by a staff, or a client, or
maybe just you – and you don’t want to have to deal with creating backend
interfaces only to manage content.

One typical workflow in creating Django apps is to create models and get the
admin sites up and running as fast as possible, so your staff (or clients) can
start populating data. Then, develop the way data is presented to the public.

## Design your URLs¶

A clean, elegant URL scheme is an important detail in a high-quality web
application. Django encourages beautiful URL design and doesn’t put any cruft
in URLs, like `.php` or `.asp`.

To design URLs for an app, you create a Python module called a [URLconf](https://docs.djangoproject.com/en/topics/http/urls/). A table of contents for your app, it contains a mapping
between URL patterns and Python callback functions. URLconfs also serve to
decouple URLs from Python code.

Here’s what a URLconf might look like for the `Reporter`/`Article`
example above:

  `mysite/news/urls.py`[¶](#id4)

```
from django.urls import path

from . import views

urlpatterns = [
    path("articles/<int:year>/", views.year_archive),
    path("articles/<int:year>/<int:month>/", views.month_archive),
    path("articles/<int:year>/<int:month>/<int:pk>/", views.article_detail),
]
```

The code above maps URL paths to Python callback functions (“views”). The path
strings use parameter tags to “capture” values from the URLs. When a user
requests a page, Django runs through each path, in order, and stops at the
first one that matches the requested URL. (If none of them matches, Django
calls a special-case 404 view.) This is blazingly fast, because the paths are
compiled into regular expressions at load time.

Once one of the URL patterns matches, Django calls the given view, which is a
Python function. Each view gets passed a request object – which contains
request metadata – and the values captured in the pattern.

For example, if a user requested the URL “/articles/2005/05/39323/”, Django
would call the function `news.views.article_detail(request,
year=2005, month=5, pk=39323)`.

## Write your views¶

Each view is responsible for doing one of two things: Returning an
[HttpResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.HttpResponse) object containing the content for the
requested page, or raising an exception such as [Http404](https://docs.djangoproject.com/en/topics/http/views/#django.http.Http404).
The rest is up to you.

Generally, a view retrieves data according to the parameters, loads a template
and renders the template with the retrieved data. Here’s an example view for
`year_archive` from above:

  `mysite/news/views.py`[¶](#id5)

```
from django.shortcuts import render

from .models import Article

def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    context = {"year": year, "article_list": a_list}
    return render(request, "news/year_archive.html", context)
```

This example uses Django’s [template system](https://docs.djangoproject.com/en/topics/templates/), which has
several powerful features but strives to stay simple enough for non-programmers
to use.

## Design your templates¶

The code above loads the `news/year_archive.html` template.

Django has a template search path, which allows you to minimize redundancy among
templates. In your Django settings, you specify a list of directories to check
for templates with [DIRS](https://docs.djangoproject.com/en/ref/settings/#std-setting-TEMPLATES-DIRS). If a template doesn’t exist
in the first directory, it checks the second, and so on.

Let’s say the `news/year_archive.html` template was found. Here’s what that
might look like:

  `mysite/news/templates/news/year_archive.html`[¶](#id6)

```
{% extends "base.html" %}

{% block title %}Articles for {{ year }}{% endblock %}

{% block content %}
<h1>Articles for {{ year }}</h1>

{% for article in article_list %}
    <p>{{ article.headline }}</p>
    <p>By {{ article.reporter.full_name }}</p>
    <p>Published {{ article.pub_date|date:"F j, Y" }}</p>
{% endfor %}
{% endblock %}
```

Variables are surrounded by double-curly braces. `{{ article.headline }}`
means “Output the value of the article’s headline attribute.” But dots aren’t
used only for attribute lookup. They also can do dictionary-key lookup, index
lookup and function calls.

Note `{{ article.pub_date|date:"F j, Y" }}` uses a Unix-style “pipe” (the “|”
character). This is called a template filter, and it’s a way to filter the value
of a variable. In this case, the date filter formats a Python datetime object in
the given format (as found in PHP’s date function).

You can chain together as many filters as you’d like. You can write [custom
template filters](https://docs.djangoproject.com/en/howto/custom-template-tags/#howto-writing-custom-template-filters). You can write
[custom template tags](https://docs.djangoproject.com/en/howto/custom-template-tags/), which run custom
Python code behind the scenes.

Finally, Django uses the concept of “template inheritance”. That’s what the
`{% extends "base.html" %}` does. It means “First load the template called
‘base’, which has defined a bunch of blocks, and fill the blocks with the
following blocks.” In short, that lets you dramatically cut down on redundancy
in templates: each template has to define only what’s unique to that template.

Here’s what the “base.html” template, including the use of [static files](https://docs.djangoproject.com/en/howto/static-files/), might look like:

  `mysite/templates/base.html`[¶](#id7)

```
{% load static %}
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <img src="{% static 'images/sitelogo.png' %}" alt="Logo">
    {% block content %}{% endblock %}
</body>
</html>
```

Simplistically, it defines the look-and-feel of the site (with the site’s logo),
and provides “holes” for child templates to fill. This means that a site redesign
can be done by changing a single file – the base template.

It also lets you create multiple versions of a site, with different base
templates, while reusing child templates. Django’s creators have used this
technique to create strikingly different mobile versions of sites by only
creating a new base template.

Note that you don’t have to use Django’s template system if you prefer another
system. While Django’s template system is particularly well-integrated with
Django’s model layer, nothing forces you to use it. For that matter, you don’t
have to use Django’s database API, either. You can use another database
abstraction layer, you can read XML files, you can read files off disk, or
anything you want. Each piece of Django – models, views, templates – is
decoupled from the next.

## This is just the surface¶

This has been only a quick overview of Django’s functionality. Some more useful
features:

- A [caching framework](https://docs.djangoproject.com/en/topics/cache/) that integrates with memcached
  or other backends.
- A [syndication framework](https://docs.djangoproject.com/en/ref/contrib/syndication/) that lets you
  create RSS and Atom feeds by writing a small Python class.
- More attractive automatically-generated admin features – this overview
  barely scratched the surface.

The next steps are for you to [download Django](https://www.djangoproject.com/download/), read [the tutorial](https://docs.djangoproject.com/en/5.0/tutorial01/) and join [the community](https://www.djangoproject.com/community/). Thanks for your interest!
