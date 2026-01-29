# The Django template language¶ and more

# The Django template language¶

# The Django template language¶

This document explains the language syntax of the Django template system. If
you’re looking for a more technical perspective on how it works and how to
extend it, see [The Django template language: for Python programmers](https://docs.djangoproject.com/en/5.0/ref/api/).

Django’s template language is designed to strike a balance between power and
ease. It’s designed to feel comfortable to those used to working with HTML. If
you have any exposure to other text-based template languages, such as [Smarty](https://www.smarty.net/)
or [Jinja2](https://palletsprojects.com/p/jinja/), you should feel right at home with Django’s templates.

Philosophy

If you have a background in programming, or if you’re used to languages
which mix programming code directly into HTML, you’ll want to bear in
mind that the Django template system is not simply Python embedded into
HTML. This is by design: the template system is meant to express
presentation, not program logic.

The Django template system provides tags which function similarly to some
programming constructs – an [if](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-if) tag for boolean tests, a [for](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-for)
tag for looping, etc. – but these are not simply executed as the
corresponding Python code, and the template system will not execute
arbitrary Python expressions. Only the tags, filters and syntax listed below
are supported by default (although you can add [your own extensions](https://docs.djangoproject.com/en/howto/custom-template-tags/) to the template language as needed).

## Templates¶

A template is a text file. It can generate any text-based format (HTML, XML,
CSV, etc.).

A template contains **variables**, which get replaced with values when the
template is evaluated, and **tags**, which control the logic of the template.

Below is a minimal template that illustrates a few basics. Each element will be
explained later in this document.

```
{% extends "base_generic.html" %}

{% block title %}{{ section.title }}{% endblock %}

{% block content %}
<h1>{{ section.title }}</h1>

{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
    {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}
```

Philosophy

Why use a text-based template instead of an XML-based one (like Zope’s
TAL)? We wanted Django’s template language to be usable for more than
just XML/HTML templates. You can use the template language for any
text-based format such as emails, JavaScript and CSV.

## Variables¶

Variables look like this: `{{ variable }}`. When the template engine
encounters a variable, it evaluates that variable and replaces it with the
result. Variable names consist of any combination of alphanumeric characters
and the underscore (`"_"`) but may not start with an underscore, and may not
be a number. The dot (`"."`) also appears in variable sections, although that
has a special meaning, as indicated below. Importantly, *you cannot have spaces
or punctuation characters in variable names.*

Use a dot (`.`) to access attributes of a variable.

Behind the scenes

Technically, when the template system encounters a dot, it tries the
following lookups, in this order:

- Dictionary lookup
- Attribute or method lookup
- Numeric index lookup

If the resulting value is callable, it is called with no arguments. The
result of the call becomes the template value.

This lookup order can cause some unexpected behavior with objects that
override dictionary lookup. For example, consider the following code snippet
that attempts to loop over a `collections.defaultdict`:

```
{% for k, v in defaultdict.items %}
    Do something with k and v here...
{% endfor %}
```

Because dictionary lookup happens first, that behavior kicks in and provides
a default value instead of using the intended `.items()` method. In this
case, consider converting to a dictionary first.

In the above example, `{{ section.title }}` will be replaced with the
`title` attribute of the `section` object.

If you use a variable that doesn’t exist, the template system will insert the
value of the `string_if_invalid` option, which is set to `''` (the empty
string) by default.

Note that “bar” in a template expression like `{{ foo.bar }}` will be
interpreted as a literal string and not using the value of the variable “bar”,
if one exists in the template context.

Variable attributes that begin with an underscore may not be accessed as
they’re generally considered private.

## Filters¶

You can modify variables for display by using **filters**.

Filters look like this: `{{ name|lower }}`. This displays the value of the
`{{ name }}` variable after being filtered through the [lower](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-lower)
filter, which converts text to lowercase. Use a pipe (`|`) to apply a filter.

Filters can be “chained.” The output of one filter is applied to the next.
`{{ text|escape|linebreaks }}` is a common idiom for escaping text contents,
then converting line breaks to `<p>` tags.

Some filters take arguments. A filter argument looks like this: `{{
bio|truncatewords:30 }}`. This will display the first 30 words of the `bio`
variable.

Filter arguments that contain spaces must be quoted; for example, to join a
list with commas and spaces you’d use `{{ list|join:", " }}`.

Django provides about sixty built-in template filters. You can read all about
them in the [built-in filter reference](https://docs.djangoproject.com/en/5.0/ref/builtins/#ref-templates-builtins-filters).
To give you a taste of what’s available, here are some of the more commonly
used template filters:

  [default](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-default)

If a variable is false or empty, use given default. Otherwise, use the
value of the variable. For example:

```
{{ value|default:"nothing" }}
```

If `value` isn’t provided or is empty, the above will display
“`nothing`”.

  [length](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-length)

Returns the length of the value. This works for both strings and lists.
For example:

```
{{ value|length }}
```

If `value` is `['a', 'b', 'c', 'd']`, the output will be `4`.

  [filesizeformat](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-filesizeformat)

Formats the value like a “human-readable” file size (i.e. `'13 KB'`,
`'4.1 MB'`, `'102 bytes'`, etc.). For example:

```
{{ value|filesizeformat }}
```

If `value` is 123456789, the output would be `117.7 MB`.

Again, these are just a few examples; see the [built-in filter reference](https://docs.djangoproject.com/en/5.0/ref/builtins/#ref-templates-builtins-filters) for the complete list.

You can also create your own custom template filters; see
[How to create custom template tags and filters](https://docs.djangoproject.com/en/howto/custom-template-tags/).

See also

Django’s admin interface can include a complete reference of all template
tags and filters available for a given site. See
[The Django admin documentation generator](https://docs.djangoproject.com/en/5.0/contrib/admin/admindocs/).

## Tags¶

Tags look like this: `{% tag %}`. Tags are more complex than variables: Some
create text in the output, some control flow by performing loops or logic, and
some load external information into the template to be used by later variables.

Some tags require beginning and ending tags (i.e. `{% tag %} ... tag contents
... {% endtag %}`).

Django ships with about two dozen built-in template tags. You can read all about
them in the [built-in tag reference](https://docs.djangoproject.com/en/5.0/ref/builtins/#ref-templates-builtins-tags). To give
you a taste of what’s available, here are some of the more commonly used
tags:

  [for](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-for)

Loop over each item in an array.  For example, to display a list of athletes
provided in `athlete_list`:

```
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>
```

   [if](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-if), `elif`, and `else`

Evaluates a variable, and if that variable is “true” the contents of the
block are displayed:

```
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% endif %}
```

In the above, if `athlete_list` is not empty, the number of athletes
will be displayed by the `{{ athlete_list|length }}` variable. Otherwise,
if `athlete_in_locker_room_list` is not empty, the message “Athletes
should be out…” will be displayed. If both lists are empty,
“No athletes.” will be displayed.

You can also use filters and various operators in the [if](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-if) tag:

```
{% if athlete_list|length > 1 %}
   Team: {% for athlete in athlete_list %} ... {% endfor %}
{% else %}
   Athlete: {{ athlete_list.0.name }}
{% endif %}
```

While the above example works, be aware that most template filters return
strings, so mathematical comparisons using filters will generally not work
as you expect. [length](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-length) is an exception.

  [block](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) and [extends](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-extends)

Set up [template inheritance](#id1) (see below), a powerful way
of cutting down on “boilerplate” in templates.

Again, the above is only a selection of the whole list; see the [built-in
tag reference](https://docs.djangoproject.com/en/5.0/ref/builtins/#ref-templates-builtins-tags) for the complete list.

You can also create your own custom template tags; see
[How to create custom template tags and filters](https://docs.djangoproject.com/en/howto/custom-template-tags/).

See also

Django’s admin interface can include a complete reference of all template
tags and filters available for a given site. See
[The Django admin documentation generator](https://docs.djangoproject.com/en/5.0/contrib/admin/admindocs/).

## Comments¶

To comment-out part of a line in a template, use the comment syntax: `{# #}`.

For example, this template would render as `'hello'`:

```
{# greeting #}hello
```

A comment can contain any template code, invalid or not. For example:

```
{# {% if foo %}bar{% else %} #}
```

This syntax can only be used for single-line comments (no newlines are permitted
between the `{#` and `#}` delimiters). If you need to comment out a
multiline portion of the template, see the [comment](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-comment) tag.

## Template inheritance¶

The most powerful – and thus the most complex – part of Django’s template
engine is template inheritance. Template inheritance allows you to build a base
“skeleton” template that contains all the common elements of your site and
defines **blocks** that child templates can override.

Let’s look at template inheritance by starting with an example:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

This template, which we’ll call `base.html`, defines an HTML skeleton
document that you might use for a two-column page. It’s the job of “child”
templates to fill the empty blocks with content.

In this example, the [block](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tag defines three blocks that child
templates can fill in. All the [block](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tag does is to tell the template
engine that a child template may override those portions of the template.

A child template might look like this:

```
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

The [extends](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-extends) tag is the key here. It tells the template engine that
this template “extends” another template. When the template system evaluates
this template, first it locates the parent – in this case, “base.html”.

At that point, the template engine will notice the three [block](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tags
in `base.html` and replace those blocks with the contents of the child
template. Depending on the value of `blog_entries`, the output might look
like:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>My amazing blog</title>
</head>

<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>

    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>

        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

Note that since the child template didn’t define the `sidebar` block, the
value from the parent template is used instead. Content within a `{% block %}`
tag in a parent template is always used as a fallback.

You can use as many levels of inheritance as needed. One common way of using
inheritance is the following three-level approach:

- Create a `base.html` template that holds the main look-and-feel of your
  site.
- Create a `base_SECTIONNAME.html` template for each “section” of your
  site. For example, `base_news.html`, `base_sports.html`. These
  templates all extend `base.html` and include section-specific
  styles/design.
- Create individual templates for each type of page, such as a news
  article or blog entry. These templates extend the appropriate section
  template.

This approach maximizes code reuse and helps to add items to shared content
areas, such as section-wide navigation.

Here are some tips for working with inheritance:

- If you use [{%extends%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-extends) in a template, it must be the first template
  tag in that template. Template inheritance won’t work, otherwise.
- More [{%block%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tags in your base templates are better. Remember,
  child templates don’t have to define all parent blocks, so you can fill
  in reasonable defaults in a number of blocks, then only define the ones
  you need later. It’s better to have more hooks than fewer hooks.
- If you find yourself duplicating content in a number of templates, it
  probably means you should move that content to a `{% block %}` in a
  parent template.
- If you need to get the content of the block from the parent template,
  the `{{ block.super }}` variable will do the trick. This is useful
  if you want to add to the contents of a parent block instead of
  completely overriding it. Data inserted using `{{ block.super }}` will
  not be automatically escaped (see the [next section](#automatic-html-escaping)), since it was
  already escaped, if necessary, in the parent template.
- By using the same template name as you are inheriting from,
  [{%extends%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-extends) can be used to inherit a template at the same
  time as overriding it. Combined with `{{ block.super }}`, this can be a
  powerful way to make small customizations. See
  [Extending an overridden template](https://docs.djangoproject.com/en/howto/overriding-templates/#extending-an-overridden-template) in the *Overriding templates* How-to
  for a full example.
- Variables created outside of a [{%block%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) using the template
  tag `as` syntax can’t be used inside the block. For example, this template
  doesn’t render anything:
  ```
  {% translate "Title" as title %}
  {% block content %}{{ title }}{% endblock %}
  ```
- For extra readability, you can optionally give a *name* to your
  `{% endblock %}` tag. For example:
  ```
  {% block content %}
  ...
  {% endblock content %}
  ```
  In larger templates, this technique helps you see which `{% block %}`
  tags are being closed.
- [{%block%}](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tags are evaluated first. That’s why the content
  of a block is always overridden, regardless of the truthiness of surrounding
  tags. For example, this template will *always* override the content of the
  `title` block:
  ```
  {% if change_title %}
      {% block title %}Hello!{% endblock title %}
  {% endif %}
  ```

Finally, note that you can’t define multiple [block](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tags with the same
name in the same template. This limitation exists because a block tag works in
“both” directions. That is, a block tag doesn’t just provide a hole to fill –
it also defines the content that fills the hole in the *parent*. If there were
two similarly-named [block](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-block) tags in a template, that template’s parent
wouldn’t know which one of the blocks’ content to use.

## Automatic HTML escaping¶

When generating HTML from templates, there’s always a risk that a variable will
include characters that affect the resulting HTML. For example, consider this
template fragment:

```
Hello, {{ name }}
```

At first, this seems like a harmless way to display a user’s name, but consider
what would happen if the user entered their name as this:

```
<script>alert('hello')</script>
```

With this name value, the template would be rendered as:

```
Hello, <script>alert('hello')</script>
```

…which means the browser would pop-up a JavaScript alert box!

Similarly, what if the name contained a `'<'` symbol, like this?

```
<b>username
```

That would result in a rendered template like this:

```
Hello, <b>username
```

…which, in turn, would result in the remainder of the web page being in bold!

Clearly, user-submitted data shouldn’t be trusted blindly and inserted directly
into your web pages, because a malicious user could use this kind of hole to
do potentially bad things. This type of security exploit is called a
[Cross Site Scripting](https://en.wikipedia.org/wiki/Cross-site_scripting) (XSS) attack.

To avoid this problem, you have two options:

- One, you can make sure to run each untrusted variable through the
  [escape](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-escape) filter (documented below), which converts potentially
  harmful HTML characters to unharmful ones. This was the default solution
  in Django for its first few years, but the problem is that it puts the
  onus on *you*, the developer / template author, to ensure you’re escaping
  everything. It’s easy to forget to escape data.
- Two, you can take advantage of Django’s automatic HTML escaping. The
  remainder of this section describes how auto-escaping works.

By default in Django, every template automatically escapes the output
of every variable tag. Specifically, these five characters are
escaped:

- `<` is converted to `&lt;`
- `>` is converted to `&gt;`
- `'` (single quote) is converted to `&#x27;`
- `"` (double quote) is converted to `&quot;`
- `&` is converted to `&amp;`

Again, we stress that this behavior is on by default. If you’re using Django’s
template system, you’re protected.

### How to turn it off¶

If you don’t want data to be auto-escaped, on a per-site, per-template level or
per-variable level, you can turn it off in several ways.

Why would you want to turn it off? Because sometimes, template variables
contain data that you *intend* to be rendered as raw HTML, in which case you
don’t want their contents to be escaped. For example, you might store a blob of
HTML in your database and want to embed that directly into your template. Or,
you might be using Django’s template system to produce text that is *not* HTML
– like an email message, for instance.

#### For individual variables¶

To disable auto-escaping for an individual variable, use the [safe](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-safe)
filter:

```
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}
```

Think of *safe* as shorthand for *safe from further escaping* or *can be
safely interpreted as HTML*. In this example, if `data` contains `'<b>'`,
the output will be:

```
This will be escaped: &lt;b&gt;
This will not be escaped: <b>
```

#### For template blocks¶

To control auto-escaping for a template, wrap the template (or a particular
section of the template) in the [autoescape](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-autoescape) tag, like so:

```
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```

The [autoescape](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-autoescape) tag takes either `on` or `off` as its argument. At
times, you might want to force auto-escaping when it would otherwise be
disabled. Here is an example template:

```
Auto-escaping is on by default. Hello {{ name }}

{% autoescape off %}
    This will not be auto-escaped: {{ data }}.

    Nor this: {{ other_data }}
    {% autoescape on %}
        Auto-escaping applies again: {{ name }}
    {% endautoescape %}
{% endautoescape %}
```

The auto-escaping tag passes its effect onto templates that extend the
current one as well as templates included via the [include](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-include) tag,
just like all block tags. For example:

  `base.html`[¶](#id4)

```
{% autoescape off %}
<h1>{% block title %}{% endblock %}</h1>
{% block content %}
{% endblock %}
{% endautoescape %}
```

    `child.html`[¶](#id5)

```
{% extends "base.html" %}
{% block title %}This &amp; that{% endblock %}
{% block content %}{{ greeting }}{% endblock %}
```

Because auto-escaping is turned off in the base template, it will also be
turned off in the child template, resulting in the following rendered
HTML when the `greeting` variable contains the string `<b>Hello!</b>`:

```
<h1>This &amp; that</h1>
<b>Hello!</b>
```

### Notes¶

Generally, template authors don’t need to worry about auto-escaping very much.
Developers on the Python side (people writing views and custom filters) need to
think about the cases in which data shouldn’t be escaped, and mark data
appropriately, so things Just Work in the template.

If you’re creating a template that might be used in situations where you’re
not sure whether auto-escaping is enabled, then add an [escape](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-escape) filter
to any variable that needs escaping. When auto-escaping is on, there’s no
danger of the [escape](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-escape) filter *double-escaping* data – the
[escape](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-escape) filter does not affect auto-escaped variables.

### String literals and automatic escaping¶

As we mentioned earlier, filter arguments can be strings:

```
{{ data|default:"This is a string literal." }}
```

All string literals are inserted **without** any automatic escaping into the
template – they act as if they were all passed through the [safe](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatefilter-safe)
filter. The reasoning behind this is that the template author is in control of
what goes into the string literal, so they can make sure the text is correctly
escaped when the template is written.

This means you would write :

```
{{ data|default:"3 &lt; 2" }}
```

…rather than:

```
{{ data|default:"3 < 2" }}  {# Bad! Don't do this. #}
```

This doesn’t affect what happens to data coming from the variable itself.
The variable’s contents are still automatically escaped, if necessary, because
they’re beyond the control of the template author.

## Accessing method calls¶

Most method calls attached to objects are also available from within templates.
This means that templates have access to much more than just class attributes
(like field names) and variables passed in from views. For example, the Django
ORM provides the [“entry_set”](https://docs.djangoproject.com/en/topics/db/queries/#topics-db-queries-related) syntax for
finding a collection of objects related on a foreign key. Therefore, given
a model called “comment” with a foreign key relationship to a model called
“task” you can loop through all comments attached to a given task like this:

```
{% for comment in task.comment_set.all %}
    {{ comment }}
{% endfor %}
```

Similarly, [QuerySets](https://docs.djangoproject.com/en/5.0/models/querysets/) provide a `count()` method
to count the number of objects they contain. Therefore, you can obtain a count
of all comments related to the current task with:

```
{{ task.comment_set.all.count }}
```

You can also access methods you’ve explicitly defined on your own models:

  `models.py`[¶](#id6)

```
class Task(models.Model):
    def foo(self):
        return "bar"
```

    `template.html`[¶](#id7)

```
{{ task.foo }}
```

Because Django intentionally limits the amount of logic processing available
in the template language, it is not possible to pass arguments to method calls
accessed from within templates. Data should be calculated in views, then passed
to templates for display.

## Custom tag and filter libraries¶

Certain applications provide custom tag and filter libraries. To access them in
a template, ensure the application is in [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) (we’d add
`'django.contrib.humanize'` for this example), and then use the [load](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-load)
tag in a template:

```
{% load humanize %}

{{ 45000|intcomma }}
```

In the above, the [load](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-load) tag loads the `humanize` tag library, which then
makes the `intcomma` filter available for use. If you’ve enabled
[django.contrib.admindocs](https://docs.djangoproject.com/en/5.0/contrib/admin/admindocs/#module-django.contrib.admindocs), you can consult the documentation area in your
admin to find the list of custom libraries in your installation.

The [load](https://docs.djangoproject.com/en/5.0/ref/builtins/#std-templatetag-load) tag can take multiple library names, separated by spaces.
Example:

```
{% load humanize i18n %}
```

See [How to create custom template tags and filters](https://docs.djangoproject.com/en/howto/custom-template-tags/) for information on writing your own custom
template libraries.

### Custom libraries and template inheritance¶

When you load a custom tag or filter library, the tags/filters are only made
available to the current template – not any parent or child templates along
the template-inheritance path.

For example, if a template `foo.html` has `{% load humanize %}`, a child
template (e.g., one that has `{% extends "foo.html" %}`) will *not* have
access to the humanize template tags and filters. The child template is
responsible for its own `{% load humanize %}`.

This is a feature for the sake of maintainability and sanity.

See also

  [The Templates Reference](https://docs.djangoproject.com/en/5.0/ref/)

Covers built-in tags, built-in filters, using an alternative template
language, and more.

---

# Unicode data¶

# Unicode data¶

Django supports Unicode data everywhere.

This document tells you what you need to know if you’re writing applications
that use data or templates that are encoded in something other than ASCII.

## Creating the database¶

Make sure your database is configured to be able to store arbitrary string
data. Normally, this means giving it an encoding of UTF-8 or UTF-16. If you use
a more restrictive encoding – for example, latin1 (iso8859-1) – you won’t be
able to store certain characters in the database, and information will be lost.

- MySQL users, refer to the [MySQL manual](https://dev.mysql.com/doc/refman/en/charset-database.html) for details on how to set or alter
  the database character set encoding.
- PostgreSQL users, refer to the [PostgreSQL manual](https://www.postgresql.org/docs/current/multibyte.html#MULTIBYTE-SETTING) for details on creating
  databases with the correct encoding.
- Oracle users, refer to the [Oracle manual](https://docs.oracle.com/en/database/oracle/oracle-database/21/nlspg/index.html) for details on how to set
  ([section 2](https://docs.oracle.com/en/database/oracle/oracle-database/21/nlspg/choosing-character-set.html)) or alter ([section 11](https://docs.oracle.com/en/database/oracle/oracle-database/21/nlspg/character-set-migration.html)) the database character set encoding.
- SQLite users, there is nothing you need to do. SQLite always uses UTF-8
  for internal encoding.

All of Django’s database backends automatically convert strings into
the appropriate encoding for talking to the database. They also automatically
convert strings retrieved from the database into strings. You don’t even need
to tell Django what encoding your database uses: that is handled transparently.

For more, see the section “The database API” below.

## General string handling¶

Whenever you use strings with Django – e.g., in database lookups, template
rendering or anywhere else – you have two choices for encoding those strings.
You can use normal strings or bytestrings (starting with a ‘b’).

Warning

A bytestring does not carry any information with it about its encoding.
For that reason, we have to make an assumption, and Django assumes that all
bytestrings are in UTF-8.

If you pass a string to Django that has been encoded in some other format,
things will go wrong in interesting ways. Usually, Django will raise a
`UnicodeDecodeError` at some point.

If your code only uses ASCII data, it’s safe to use your normal strings,
passing them around at will, because ASCII is a subset of UTF-8.

Don’t be fooled into thinking that if your [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting is set
to something other than `'utf-8'` you can use that other encoding in your
bytestrings! [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) only applies to the strings generated as
the result of template rendering (and email). Django will always assume UTF-8
encoding for internal bytestrings. The reason for this is that the
[DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting is not actually under your control (if you are the
application developer). It’s under the control of the person installing and
using your application – and if that person chooses a different setting, your
code must still continue to work. Ergo, it cannot rely on that setting.

In most cases when Django is dealing with strings, it will convert them to
strings before doing anything else. So, as a general rule, if you pass
in a bytestring, be prepared to receive a string back in the result.

### Translated strings¶

Aside from strings and bytestrings, there’s a third type of string-like
object you may encounter when using Django. The framework’s
internationalization features introduce the concept of a “lazy translation” –
a string that has been marked as translated but whose actual translation result
isn’t determined until the object is used in a string. This feature is useful
in cases where the translation locale is unknown until the string is used, even
though the string might have originally been created when the code was first
imported.

Normally, you won’t have to worry about lazy translations. Just be aware that
if you examine an object and it claims to be a
`django.utils.functional.__proxy__` object, it is a lazy translation.
Calling `str()` with the lazy translation as the argument will generate a
string in the current locale.

For more details about lazy translation objects, refer to the
[internationalization](https://docs.djangoproject.com/en/topics/i18n/) documentation.

### Useful utility functions¶

Because some string operations come up again and again, Django ships with a few
useful functions that should make working with string and bytestring objects
a bit easier.

#### Conversion functions¶

The `django.utils.encoding` module contains a few functions that are handy
for converting back and forth between strings and bytestrings.

- `smart_str(s, encoding='utf-8', strings_only=False, errors='strict')`
  converts its input to a string. The `encoding` parameter
  specifies the input encoding. (For example, Django uses this internally
  when processing form input data, which might not be UTF-8 encoded.) The
  `strings_only` parameter, if set to True, will result in Python
  numbers, booleans and `None` not being converted to a string (they keep
  their original types). The `errors` parameter takes any of the values
  that are accepted by Python’s `str()` function for its error
  handling.
- `force_str(s, encoding='utf-8', strings_only=False, errors='strict')` is
  identical to `smart_str()` in almost all cases. The difference is when the
  first argument is a [lazy translation](https://docs.djangoproject.com/en/topics/i18n/translation/#lazy-translations) instance.
  While `smart_str()` preserves lazy translations, `force_str()` forces
  those objects to a string (causing the translation to occur). Normally,
  you’ll want to use `smart_str()`. However, `force_str()` is useful in
  template tags and filters that absolutely *must* have a string to work with,
  not just something that can be converted to a string.
- `smart_bytes(s, encoding='utf-8', strings_only=False, errors='strict')`
  is essentially the opposite of `smart_str()`. It forces the first
  argument to a bytestring. The `strings_only` parameter has the same
  behavior as for `smart_str()` and `force_str()`. This is
  slightly different semantics from Python’s builtin `str()` function,
  but the difference is needed in a few places within Django’s internals.

Normally, you’ll only need to use `force_str()`. Call it as early as
possible on any input data that might be either a string or a bytestring, and
from then on, you can treat the result as always being a string.

#### URI and IRI handling¶

Web frameworks have to deal with URLs (which are a type of IRI). One
requirement of URLs is that they are encoded using only ASCII characters.
However, in an international environment, you might need to construct a
URL from an [IRI](https://datatracker.ietf.org/doc/html/rfc3987.html) – very loosely speaking, a [URI](https://datatracker.ietf.org/doc/html/rfc3986.html)
that can contain Unicode characters. Use these functions for quoting and
converting an IRI to a URI:

- The [django.utils.encoding.iri_to_uri()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.encoding.iri_to_uri) function, which implements the
  conversion from IRI to URI as required by [RFC 3987 Section 3.1](https://datatracker.ietf.org/doc/html/rfc3987.html#section-3.1).
- The [urllib.parse.quote()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote) and [urllib.parse.quote_plus()](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus)
  functions from Python’s standard library.

These two groups of functions have slightly different purposes, and it’s
important to keep them straight. Normally, you would use `quote()` on the
individual portions of the IRI or URI path so that any reserved characters
such as ‘&’ or ‘%’ are correctly encoded. Then, you apply `iri_to_uri()` to
the full IRI and it converts any non-ASCII characters to the correct encoded
values.

Note

Technically, it isn’t correct to say that `iri_to_uri()` implements the
full algorithm in the IRI specification. It doesn’t (yet) perform the
international domain name encoding portion of the algorithm.

The `iri_to_uri()` function will not change ASCII characters that are
otherwise permitted in a URL. So, for example, the character ‘%’ is not
further encoded when passed to `iri_to_uri()`. This means you can pass a
full URL to this function and it will not mess up the query string or anything
like that.

An example might clarify things here:

```
>>> from urllib.parse import quote
>>> from django.utils.encoding import iri_to_uri
>>> quote("Paris & Orléans")
'Paris%20%26%20Orl%C3%A9ans'
>>> iri_to_uri("/favorites/François/%s" % quote("Paris & Orléans"))
'/favorites/Fran%C3%A7ois/Paris%20%26%20Orl%C3%A9ans'
```

If you look carefully, you can see that the portion that was generated by
`quote()` in the second example was not double-quoted when passed to
`iri_to_uri()`. This is a very important and useful feature. It means that
you can construct your IRI without worrying about whether it contains
non-ASCII characters and then, right at the end, call `iri_to_uri()` on the
result.

Similarly, Django provides [django.utils.encoding.uri_to_iri()](https://docs.djangoproject.com/en/5.0/utils/#django.utils.encoding.uri_to_iri) which
implements the conversion from URI to IRI as per [RFC 3987 Section 3.2](https://datatracker.ietf.org/doc/html/rfc3987.html#section-3.2).

An example to demonstrate:

```
>>> from django.utils.encoding import uri_to_iri
>>> uri_to_iri("/%E2%99%A5%E2%99%A5/?utf8=%E2%9C%93")
'/♥♥/?utf8=✓'
>>> uri_to_iri("%A9hello%3Fworld")
'%A9hello%3Fworld'
```

In the first example, the UTF-8 characters are unquoted. In the second, the
percent-encodings remain unchanged because they lie outside the valid UTF-8
range or represent a reserved character.

Both `iri_to_uri()` and `uri_to_iri()` functions are idempotent, which means the
following is always true:

```
iri_to_uri(iri_to_uri(some_string)) == iri_to_uri(some_string)
uri_to_iri(uri_to_iri(some_string)) == uri_to_iri(some_string)
```

So you can safely call it multiple times on the same URI/IRI without risking
double-quoting problems.

## Models¶

Because all strings are returned from the database as `str` objects, model
fields that are character based (CharField, TextField, URLField, etc.) will
contain Unicode values when Django retrieves data from the database. This
is *always* the case, even if the data could fit into an ASCII bytestring.

You can pass in bytestrings when creating a model or populating a field, and
Django will convert it to strings when it needs to.

### Taking care inget_absolute_url()¶

URLs can only contain ASCII characters. If you’re constructing a URL from
pieces of data that might be non-ASCII, be careful to encode the results in a
way that is suitable for a URL. The [reverse()](https://docs.djangoproject.com/en/5.0/urlresolvers/#django.urls.reverse) function
handles this for you automatically.

If you’re constructing a URL manually (i.e., *not* using the `reverse()`
function), you’ll need to take care of the encoding yourself. In this case,
use the `iri_to_uri()` and `quote()` functions that were documented
[above](#id1). For example:

```
from urllib.parse import quote
from django.utils.encoding import iri_to_uri

def get_absolute_url(self):
    url = "/person/%s/?x=0&y=0" % quote(self.location)
    return iri_to_uri(url)
```

This function returns a correctly encoded URL even if `self.location` is
something like “Jack visited Paris & Orléans”. (In fact, the `iri_to_uri()`
call isn’t strictly necessary in the above example, because all the
non-ASCII characters would have been removed in quoting in the first line.)

## Templates¶

Use strings when creating templates manually:

```
from django.template import Template

t2 = Template("This is a string template.")
```

But the common case is to read templates from the filesystem. If your template
files are not stored with a UTF-8 encoding, adjust the [TEMPLATES](https://docs.djangoproject.com/en/5.0/settings/#std-setting-TEMPLATES)
setting. The built-in [django](https://docs.djangoproject.com/en/topics/templates/#module-django.template.backends.django) backend
provides the `'file_charset'` option to change the encoding used to read
files from disk.

The [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting controls the encoding of rendered templates.
This is set to UTF-8 by default.

### Template tags and filters¶

A couple of tips to remember when writing your own template tags and filters:

- Always return strings from a template tag’s `render()` method
  and from template filters.
- Use `force_str()` in preference to `smart_str()` in these
  places. Tag rendering and filter calls occur as the template is being
  rendered, so there is no advantage to postponing the conversion of lazy
  translation objects into strings. It’s easier to work solely with
  strings at that point.

## Files¶

If you intend to allow users to upload files, you must ensure that the
environment used to run Django is configured to work with non-ASCII file names.
If your environment isn’t configured correctly, you’ll encounter
`UnicodeEncodeError` exceptions when saving files with file names or content
that contains non-ASCII characters.

Filesystem support for UTF-8 file names varies and might depend on the
environment. Check your current configuration in an interactive Python shell by
running:

```
import sys

sys.getfilesystemencoding()
```

This should output “UTF-8”.

The `LANG` environment variable is responsible for setting the expected
encoding on Unix platforms. Consult the documentation for your operating system
and application server for the appropriate syntax and location to set this
variable. See the [How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/howto/deployment/wsgi/modwsgi/) for examples.

In your development environment, you might need to add a setting to your
`~.bashrc` analogous to:

```
export LANG="en_US.UTF-8"
```

## Form submission¶

HTML form submission is a tricky area. There’s no guarantee that the
submission will include encoding information, which means the framework might
have to guess at the encoding of submitted data.

Django adopts a “lazy” approach to decoding form data. The data in an
`HttpRequest` object is only decoded when you access it. In fact, most of
the data is not decoded at all. Only the `HttpRequest.GET` and
`HttpRequest.POST` data structures have any decoding applied to them. Those
two fields will return their members as Unicode data. All other attributes and
methods of `HttpRequest` return data exactly as it was submitted by the
client.

By default, the [DEFAULT_CHARSET](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_CHARSET) setting is used as the assumed encoding
for form data. If you need to change this for a particular form, you can set
the `encoding` attribute on an `HttpRequest` instance. For example:

```
def some_view(request):
    # We know that the data must be encoded as KOI8-R (for some reason).
    request.encoding = "koi8-r"
    ...
```

You can even change the encoding after having accessed `request.GET` or
`request.POST`, and all subsequent accesses will use the new encoding.

Most developers won’t need to worry about changing form encoding, but this is
a useful feature for applications that talk to legacy systems whose encoding
you cannot control.

Django does not decode the data of file uploads, because that data is normally
treated as collections of bytes, rather than strings. Any automatic decoding
there would alter the meaning of the stream of bytes.
