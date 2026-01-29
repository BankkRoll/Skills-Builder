# Class and more

# Class

# Class-based Views

This page introduces using the [View](https://flask.palletsprojects.com/en/api/#flask.views.View) and [MethodView](https://flask.palletsprojects.com/en/api/#flask.views.MethodView)
classes to write class-based views.

A class-based view is a class that acts as a view function. Because it
is a class, different instances of the class can be created with
different arguments, to change the behavior of the view. This is also
known as generic, reusable, or pluggable views.

An example of where this is useful is defining a class that creates an
API based on the database model it is initialized with.

For more complex API behavior and customization, look into the various
API extensions for Flask.

## Basic Reusable View

Let’s walk through an example converting a view function to a view
class. We start with a view function that queries a list of users then
renders a template to show the list.

```
@app.route("/users/")
def user_list():
    users = User.query.all()
    return render_template("users.html", users=users)
```

This works for the user model, but let’s say you also had more models
that needed list pages. You’d need to write another view function for
each model, even though the only thing that would change is the model
and template name.

Instead, you can write a [View](https://flask.palletsprojects.com/en/api/#flask.views.View) subclass that will query a model
and render a template. As the first step, we’ll convert the view to a
class without any customization.

```
from flask.views import View

class UserList(View):
    def dispatch_request(self):
        users = User.query.all()
        return render_template("users.html", objects=users)

app.add_url_rule("/users/", view_func=UserList.as_view("user_list"))
```

The [View.dispatch_request()](https://flask.palletsprojects.com/en/api/#flask.views.View.dispatch_request) method is the equivalent of the view
function. Calling [View.as_view()](https://flask.palletsprojects.com/en/api/#flask.views.View.as_view) method will create a view
function that can be registered on the app with its
[add_url_rule()](https://flask.palletsprojects.com/en/api/#flask.Flask.add_url_rule) method. The first argument to
`as_view` is the name to use to refer to the view with
[url_for()](https://flask.palletsprojects.com/en/api/#flask.url_for).

Note

You can’t decorate the class with `@app.route()` the way you’d
do with a basic view function.

Next, we need to be able to register the same view class for different
models and templates, to make it more useful than the original function.
The class will take two arguments, the model and template, and store
them on `self`. Then `dispatch_request` can reference these instead
of hard-coded values.

```
class ListView(View):
    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = self.model.query.all()
        return render_template(self.template, items=items)
```

Remember, we create the view function with `View.as_view()` instead of
creating the class directly. Any extra arguments passed to `as_view`
are then passed when creating the class. Now we can register the same
view to handle multiple models.

```
app.add_url_rule(
    "/users/",
    view_func=ListView.as_view("user_list", User, "users.html"),
)
app.add_url_rule(
    "/stories/",
    view_func=ListView.as_view("story_list", Story, "stories.html"),
)
```

## URL Variables

Any variables captured by the URL are passed as keyword arguments to the
`dispatch_request` method, as they would be for a regular view
function.

```
class DetailView(View):
    def __init__(self, model):
        self.model = model
        self.template = f"{model.__name__.lower()}/detail.html"

    def dispatch_request(self, id)
        item = self.model.query.get_or_404(id)
        return render_template(self.template, item=item)

app.add_url_rule(
    "/users/<int:id>",
    view_func=DetailView.as_view("user_detail", User)
)
```

## View Lifetime andself

By default, a new instance of the view class is created every time a
request is handled. This means that it is safe to write other data to
`self` during the request, since the next request will not see it,
unlike other forms of global state.

However, if your view class needs to do a lot of complex initialization,
doing it for every request is unnecessary and can be inefficient. To
avoid this, set [View.init_every_request](https://flask.palletsprojects.com/en/api/#flask.views.View.init_every_request) to `False`, which will
only create one instance of the class and use it for every request. In
this case, writing to `self` is not safe. If you need to store data
during the request, use [g](https://flask.palletsprojects.com/en/api/#flask.g) instead.

In the `ListView` example, nothing writes to `self` during the
request, so it is more efficient to create a single instance.

```
class ListView(View):
    init_every_request = False

    def __init__(self, model, template):
        self.model = model
        self.template = template

    def dispatch_request(self):
        items = self.model.query.all()
        return render_template(self.template, items=items)
```

Different instances will still be created each for each `as_view`
call, but not for each request to those views.

## View Decorators

The view class itself is not the view function. View decorators need to
be applied to the view function returned by `as_view`, not the class
itself. Set [View.decorators](https://flask.palletsprojects.com/en/api/#flask.views.View.decorators) to a list of decorators to apply.

```
class UserList(View):
    decorators = [cache(minutes=2), login_required]

app.add_url_rule('/users/', view_func=UserList.as_view())
```

If you didn’t set `decorators`, you could apply them manually instead.
This is equivalent to:

```
view = UserList.as_view("users_list")
view = cache(minutes=2)(view)
view = login_required(view)
app.add_url_rule('/users/', view_func=view)
```

Keep in mind that order matters. If you’re used to `@decorator` style,
this is equivalent to:

```
@app.route("/users/")
@login_required
@cache(minutes=2)
def user_list():
    ...
```

## Method Hints

A common pattern is to register a view with `methods=["GET", "POST"]`,
then check `request.method == "POST"` to decide what to do. Setting
[View.methods](https://flask.palletsprojects.com/en/api/#flask.views.View.methods) is equivalent to passing the list of methods to
`add_url_rule` or `route`.

```
class MyView(View):
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "POST":
            ...
        ...

app.add_url_rule('/my-view', view_func=MyView.as_view('my-view'))
```

This is equivalent to the following, except further subclasses can
inherit or change the methods.

```
app.add_url_rule(
    "/my-view",
    view_func=MyView.as_view("my-view"),
    methods=["GET", "POST"],
)
```

## Method Dispatching and APIs

For APIs it can be helpful to use a different function for each HTTP
method. [MethodView](https://flask.palletsprojects.com/en/api/#flask.views.MethodView) extends the basic [View](https://flask.palletsprojects.com/en/api/#flask.views.View) to dispatch
to different methods of the class based on the request method. Each HTTP
method maps to a method of the class with the same (lowercase) name.

[MethodView](https://flask.palletsprojects.com/en/api/#flask.views.MethodView) automatically sets [View.methods](https://flask.palletsprojects.com/en/api/#flask.views.View.methods) based on the
methods defined by the class. It even knows how to handle subclasses
that override or define other methods.

We can make a generic `ItemAPI` class that provides get (detail),
patch (edit), and delete methods for a given model. A `GroupAPI` can
provide get (list) and post (create) methods.

```
from flask.views import MethodView

class ItemAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        self.validator = generate_validator(model)

    def _get_item(self, id):
        return self.model.query.get_or_404(id)

    def get(self, id):
        item = self._get_item(id)
        return jsonify(item.to_json())

    def patch(self, id):
        item = self._get_item(id)
        errors = self.validator.validate(item, request.json)

        if errors:
            return jsonify(errors), 400

        item.update_from_json(request.json)
        db.session.commit()
        return jsonify(item.to_json())

    def delete(self, id):
        item = self._get_item(id)
        db.session.delete(item)
        db.session.commit()
        return "", 204

class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        self.validator = generate_validator(model, create=True)

    def get(self):
        items = self.model.query.all()
        return jsonify([item.to_json() for item in items])

    def post(self):
        errors = self.validator.validate(request.json)

        if errors:
            return jsonify(errors), 400

        db.session.add(self.model.from_json(request.json))
        db.session.commit()
        return jsonify(item.to_json())

def register_api(app, model, name):
    item = ItemAPI.as_view(f"{name}-item", model)
    group = GroupAPI.as_view(f"{name}-group", model)
    app.add_url_rule(f"/{name}/<int:id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)

register_api(app, User, "users")
register_api(app, Story, "stories")
```

This produces the following views, a standard REST API!

| URL | Method | Description |
| --- | --- | --- |
| /users/ | GET | List all users |
| /users/ | POST | Create a new user |
| /users/<id> | GET | Show a single user |
| /users/<id> | PATCH | Update a user |
| /users/<id> | DELETE | Delete a user |
| /stories/ | GET | List all stories |
| /stories/ | POST | Create a new story |
| /stories/<id> | GET | Show a single story |
| /stories/<id> | PATCH | Update a story |
| /stories/<id> | DELETE | Delete a story |

---

# Security Considerations¶

# Security Considerations

Web applications face many types of potential security problems, and it can be
hard to get everything right, or even to know what “right” is in general. Flask
tries to solve a few of these things by default, but there are other parts you
may have to take care of yourself. Many of these solutions are tradeoffs, and
will depend on each application’s specific needs and threat model. Many hosting
platforms may take care of certain types of problems without the need for the
Flask application to handle them.

## Resource Use

A common category of attacks is “Denial of Service” (DoS or DDoS). This is a
very broad category, and different variants target different layers in a
deployed application. In general, something is done to increase how much
processing time or memory is used to handle each request, to the point where
there are not enough resources to handle legitimate requests.

Flask provides a few configuration options to handle resource use. They can
also be set on individual requests to customize only that request. The
documentation for each goes into more detail.

- [MAX_CONTENT_LENGTH](https://flask.palletsprojects.com/en/config/#MAX_CONTENT_LENGTH) or [Request.max_content_length](https://flask.palletsprojects.com/en/api/#flask.Request.max_content_length) controls
  how much data will be read from a request. It is not set by default,
  although it will still block truly unlimited streams unless the WSGI server
  indicates support.
- [MAX_FORM_MEMORY_SIZE](https://flask.palletsprojects.com/en/config/#MAX_FORM_MEMORY_SIZE) or [Request.max_form_memory_size](https://flask.palletsprojects.com/en/api/#flask.Request.max_form_memory_size)
  controls how large any non-file `multipart/form-data` field can be. It is
  set to 500kB by default.
- [MAX_FORM_PARTS](https://flask.palletsprojects.com/en/config/#MAX_FORM_PARTS) or [Request.max_form_parts](https://flask.palletsprojects.com/en/api/#flask.Request.max_form_parts) controls how many
  `multipart/form-data` fields can be parsed. It is set to 1000 by default.
  Combined with the default `max_form_memory_size`, this means that a form
  will occupy at most 500MB of memory.

Regardless of these settings, you should also review what settings are available
from your operating system, container deployment (Docker etc), WSGI server, HTTP
server, and hosting platform. They typically have ways to set process resource
limits, timeouts, and other checks regardless of how Flask is configured.

## Cross-Site Scripting (XSS)

Cross site scripting is the concept of injecting arbitrary HTML (and with
it JavaScript) into the context of a website.  To remedy this, developers
have to properly escape text so that it cannot include arbitrary HTML
tags.  For more information on that have a look at the Wikipedia article
on [Cross-Site Scripting](https://en.wikipedia.org/wiki/Cross-site_scripting).

Flask configures Jinja to automatically escape all values unless
explicitly told otherwise.  This should rule out all XSS problems caused
in templates, but there are still other places where you have to be
careful:

- generating HTML without the help of Jinja
- calling `Markup` on data submitted by users
- sending out HTML from uploaded files, never do that, use the
  `Content-Disposition: attachment` header to prevent that problem.
- sending out textfiles from uploaded files.  Some browsers are using
  content-type guessing based on the first few bytes so users could
  trick a browser to execute HTML.

Another thing that is very important are unquoted attributes.  While
Jinja can protect you from XSS issues by escaping HTML, there is one
thing it cannot protect you from: XSS by attribute injection.  To counter
this possible attack vector, be sure to always quote your attributes with
either double or single quotes when using Jinja expressions in them:

```
<input value="{{ value }}">
```

Why is this necessary?  Because if you would not be doing that, an
attacker could easily inject custom JavaScript handlers.  For example an
attacker could inject this piece of HTML+JavaScript:

```
onmouseover=alert(document.cookie)
```

When the user would then move with the mouse over the input, the cookie
would be presented to the user in an alert window.  But instead of showing
the cookie to the user, a good attacker might also execute any other
JavaScript code.  In combination with CSS injections the attacker might
even make the element fill out the entire page so that the user would
just have to have the mouse anywhere on the page to trigger the attack.

There is one class of XSS issues that Jinja’s escaping does not protect
against. The `a` tag’s `href` attribute can contain a `javascript:` URI,
which the browser will execute when clicked if not secured properly.

```
<a href="{{ value }}">click here</a>
<a href="javascript:alert('unsafe');">click here</a>
```

To prevent this, you’ll need to set the [Content Security Policy (CSP)](#security-csp) response header.

## Cross-Site Request Forgery (CSRF)

Another big problem is CSRF.  This is a very complex topic and I won’t
outline it here in detail just mention what it is and how to theoretically
prevent it.

If your authentication information is stored in cookies, you have implicit
state management.  The state of “being logged in” is controlled by a
cookie, and that cookie is sent with each request to a page.
Unfortunately that includes requests triggered by 3rd party sites.  If you
don’t keep that in mind, some people might be able to trick your
application’s users with social engineering to do stupid things without
them knowing.

Say you have a specific URL that, when you sent `POST` requests to will
delete a user’s profile (say `http://example.com/user/delete`).  If an
attacker now creates a page that sends a post request to that page with
some JavaScript they just have to trick some users to load that page and
their profiles will end up being deleted.

Imagine you were to run Facebook with millions of concurrent users and
someone would send out links to images of little kittens.  When users
would go to that page, their profiles would get deleted while they are
looking at images of fluffy cats.

How can you prevent that?  Basically for each request that modifies
content on the server you would have to either use a one-time token and
store that in the cookie **and** also transmit it with the form data.
After receiving the data on the server again, you would then have to
compare the two tokens and ensure they are equal.

Why does Flask not do that for you?  The ideal place for this to happen is
the form validation framework, which does not exist in Flask.

## JSON Security

In Flask 0.10 and lower, `jsonify()` did not serialize top-level
arrays to JSON. This was because of a security vulnerability in ECMAScript 4.

ECMAScript 5 closed this vulnerability, so only extremely old browsers are
still vulnerable. All of these browsers have [other more serious
vulnerabilities](https://github.com/pallets/flask/issues/248#issuecomment-59934857), so
this behavior was changed and `jsonify()` now supports serializing
arrays.

## Security Headers

Browsers recognize various response headers in order to control security. We
recommend reviewing each of the headers below for use in your application.
The [Flask-Talisman](https://github.com/wntrblm/flask-talisman) extension can be used to manage HTTPS and the security
headers for you.

### HTTP Strict Transport Security (HSTS)

Tells the browser to convert all HTTP requests to HTTPS, preventing
man-in-the-middle (MITM) attacks.

```
response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
```

- [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)

### Content Security Policy (CSP)

Tell the browser where it can load various types of resource from. This header
should be used whenever possible, but requires some work to define the correct
policy for your site. A very strict policy would be:

```
response.headers['Content-Security-Policy'] = "default-src 'self'"
```

- [https://csp.withgoogle.com/docs/index.html](https://csp.withgoogle.com/docs/index.html)
- [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy)

### X-Content-Type-Options

Forces the browser to honor the response content type instead of trying to
detect it, which can be abused to generate a cross-site scripting (XSS)
attack.

```
response.headers['X-Content-Type-Options'] = 'nosniff'
```

- [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)

### X-Frame-Options

Prevents external sites from embedding your site in an `iframe`. This
prevents a class of attacks where clicks in the outer frame can be translated
invisibly to clicks on your page’s elements. This is also known as
“clickjacking”.

```
response.headers['X-Frame-Options'] = 'SAMEORIGIN'
```

- [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)

### Set-Cookie options

These options can be added to a `Set-Cookie` header to improve their
security. Flask has configuration options to set these on the session cookie.
They can be set on other cookies too.

- `Secure` limits cookies to HTTPS traffic only.
- `HttpOnly` protects the contents of cookies from being read with
  JavaScript.
- `SameSite` restricts how cookies are sent with requests from
  external sites. Can be set to `'Lax'` (recommended) or `'Strict'`.
  `Lax` prevents sending cookies with CSRF-prone requests from
  external sites, such as submitting a form. `Strict` prevents sending
  cookies with all external requests, including following regular links.

```
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

response.set_cookie('username', 'flask', secure=True, httponly=True, samesite='Lax')
```

Specifying `Expires` or `Max-Age` options, will remove the cookie after
the given time, or the current time plus the age, respectively. If neither
option is set, the cookie will be removed when the browser is closed.

```
# cookie expires after 10 minutes
response.set_cookie('snakes', '3', max_age=600)
```

For the session cookie, if [session.permanent](https://flask.palletsprojects.com/en/api/#flask.session.permanent)
is set, then [PERMANENT_SESSION_LIFETIME](https://flask.palletsprojects.com/en/config/#PERMANENT_SESSION_LIFETIME) is used to set the expiration.
Flask’s default cookie implementation validates that the cryptographic
signature is not older than this value. Lowering this value may help mitigate
replay attacks, where intercepted cookies can be sent at a later time.

```
app.config.update(
    PERMANENT_SESSION_LIFETIME=600
)

@app.route('/login', methods=['POST'])
def login():
    ...
    session.clear()
    session['user_id'] = user.id
    session.permanent = True
    ...
```

Use `itsdangerous.TimedSerializer` to sign and validate other cookie
values (or any values that need secure signatures).

- [https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie)

## Host Header Validation

The `Host` header is used by the client to indicate what host name the request
was made to. This is used, for example, by `url_for(..., _external=True)` to
generate full URLs, for use in email or other messages outside the browser
window.

By default the app doesn’t know what host(s) it is allowed to be accessed
through, and assumes any host is valid. Although browsers do not allow setting
the `Host` header, requests made by attackers in other scenarios could set
the `Host` header to a value they want.

When deploying your application, set [TRUSTED_HOSTS](https://flask.palletsprojects.com/en/config/#TRUSTED_HOSTS) to restrict what
values the `Host` header may be.

The `Host` header may be modified by proxies in between the client and your
application. See [Tell Flask it is Behind a Proxy](https://flask.palletsprojects.com/en/deploying/proxy_fix/) to tell your app which proxy values
to trust.

## Copy/Paste to Terminal

Hidden characters such as the backspace character (`\b`, `^H`) can
cause text to render differently in HTML than how it is interpreted if
[pasted into a terminal](https://security.stackexchange.com/q/39118).

For example, `import y\bose\bm\bi\bt\be\b` renders as
`import yosemite` in HTML, but the backspaces are applied when pasted
into a terminal, and it becomes `import os`.

If you expect users to copy and paste untrusted code from your site,
such as from comments posted by users on a technical blog, consider
applying extra filtering, such as replacing all `\b` characters.

```
body = body.replace("\b", "")
```

Most modern terminals will warn about and remove hidden characters when
pasting, so this isn’t strictly necessary. It’s also possible to craft
dangerous commands in other ways that aren’t possible to filter.
Depending on your site’s use case, it may be good to show a warning
about copying code in general.
