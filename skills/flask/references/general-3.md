# Changes¶

# Changes¶

# Changes

## Version 3.1.2

Released 2025-08-19

- `stream_with_context` does not fail inside async views. [#5774](https://github.com/pallets/flask/issues/5774)
- When using `follow_redirects` in the test client, the final state
  of `session` is correct. [#5786](https://github.com/pallets/flask/issues/5786)
- Relax type hint for passing bytes IO to `send_file`. [#5776](https://github.com/pallets/flask/issues/5776)

## Version 3.1.1

Released 2025-05-13

- Fix signing key selection order when key rotation is enabled via
  `SECRET_KEY_FALLBACKS`. [GHSA-4grg-w6v8-c28g](https://github.com/pallets/flask/security/advisories/GHSA-4grg-w6v8-c28g)
- Fix type hint for `cli_runner.invoke`. [#5645](https://github.com/pallets/flask/issues/5645)
- `flask --help` loads the app and plugins first to make sure all commands
  are shown. [#5673](https://github.com/pallets/flask/issues/5673)
- Mark sans-io base class as being able to handle views that return
  `AsyncIterable`. This is not accurate for Flask, but makes typing easier
  for Quart. [#5659](https://github.com/pallets/flask/pull/5659)

## Version 3.1.0

Released 2024-11-13

- Drop support for Python 3.8. [#5623](https://github.com/pallets/flask/pull/5623)
- Update minimum dependency versions to latest feature releases.
  Werkzeug >= 3.1, ItsDangerous >= 2.2, Blinker >= 1.9. [#5624,5633](https://github.com/pallets/flask/pull/5624,5633)
- Provide a configuration option to control automatic option
  responses. [#5496](https://github.com/pallets/flask/pull/5496)
- `Flask.open_resource`/`open_instance_resource` and
  `Blueprint.open_resource` take an `encoding` parameter to use when
  opening in text mode. It defaults to `utf-8`. [#5504](https://github.com/pallets/flask/issues/5504)
- `Request.max_content_length` can be customized per-request instead of only
  through the `MAX_CONTENT_LENGTH` config. Added
  `MAX_FORM_MEMORY_SIZE` and `MAX_FORM_PARTS` config. Added documentation
  about resource limits to the security page. [#5625](https://github.com/pallets/flask/issues/5625)
- Add support for the `Partitioned` cookie attribute (CHIPS), with the
  `SESSION_COOKIE_PARTITIONED` config. [#5472](https://github.com/pallets/flask/issues/5472)
- `-e path` takes precedence over default `.env` and `.flaskenv` files.
  `load_dotenv` loads default files in addition to a path unless
  `load_defaults=False` is passed. [#5628](https://github.com/pallets/flask/issues/5628)
- Support key rotation with the `SECRET_KEY_FALLBACKS` config, a list of old
  secret keys that can still be used for unsigning. Extensions will need to
  add support. [#5621](https://github.com/pallets/flask/issues/5621)
- Fix how setting `host_matching=True` or `subdomain_matching=False`
  interacts with `SERVER_NAME`. Setting `SERVER_NAME` no longer restricts
  requests to only that domain. [#5553](https://github.com/pallets/flask/issues/5553)
- `Request.trusted_hosts` is checked during routing, and can be set through
  the `TRUSTED_HOSTS` config. [#5636](https://github.com/pallets/flask/issues/5636)

## Version 3.0.3

Released 2024-04-07

- The default `hashlib.sha1` may not be available in FIPS builds. Don’t
  access it at import time so the developer has time to change the default.
  [#5448](https://github.com/pallets/flask/issues/5448)
- Don’t initialize the `cli` attribute in the sansio scaffold, but rather in
  the `Flask` concrete class. [#5270](https://github.com/pallets/flask/pull/5270)

## Version 3.0.2

Released 2024-02-03

- Correct type for `jinja_loader` property. [#5388](https://github.com/pallets/flask/issues/5388)
- Fix error with `--extra-files` and `--exclude-patterns` CLI options.
  [#5391](https://github.com/pallets/flask/issues/5391)

## Version 3.0.1

Released 2024-01-18

- Correct type for `path` argument to `send_file`. [#5336](https://github.com/pallets/flask/issues/5336)
- Fix a typo in an error message for the `flask run --key` option. [#5344](https://github.com/pallets/flask/pull/5344)
- Session data is untagged without relying on the built-in `json.loads` `object_hook`. This allows other JSON providers that don’t implement that.
  [#5381](https://github.com/pallets/flask/issues/5381)
- Address more type findings when using mypy strict mode. [#5383](https://github.com/pallets/flask/pull/5383)

## Version 3.0.0

Released 2023-09-30

- Remove previously deprecated code. [#5223](https://github.com/pallets/flask/pull/5223)
- Deprecate the `__version__` attribute. Use feature detection, or
  `importlib.metadata.version("flask")`, instead. [#5230](https://github.com/pallets/flask/issues/5230)
- Restructure the code such that the Flask (app) and Blueprint
  classes have Sans-IO bases. [#5127](https://github.com/pallets/flask/pull/5127)
- Allow self as an argument to url_for. [#5264](https://github.com/pallets/flask/pull/5264)
- Require Werkzeug >= 3.0.0.

## Version 2.3.3

Released 2023-08-21

- Python 3.12 compatibility.
- Require Werkzeug >= 2.3.7.
- Use `flit_core` instead of `setuptools` as build backend.
- Refactor how an app’s root and instance paths are determined. [#5160](https://github.com/pallets/flask/issues/5160)

## Version 2.3.2

Released 2023-05-01

- Set `Vary: Cookie` header when the session is accessed, modified, or refreshed.
- Update Werkzeug requirement to >=2.3.3 to apply recent bug fixes.
  [GHSA-m2qf-hxjv-5gpq](https://github.com/pallets/flask/security/advisories/GHSA-m2qf-hxjv-5gpq)

## Version 2.3.1

Released 2023-04-25

- Restore deprecated `from flask import Markup`. [#5084](https://github.com/pallets/flask/issues/5084)

## Version 2.3.0

Released 2023-04-25

- Drop support for Python 3.7. [#5072](https://github.com/pallets/flask/pull/5072)
- Update minimum requirements to the latest versions: Werkzeug>=2.3.0, Jinja2>3.1.2,
  itsdangerous>=2.1.2, click>=8.1.3.
- Remove previously deprecated code. [#4995](https://github.com/pallets/flask/pull/4995)
  - The `push` and `pop` methods of the deprecated `_app_ctx_stack` and
    `_request_ctx_stack` objects are removed. `top` still exists to give
    extensions more time to update, but it will be removed.
  - The `FLASK_ENV` environment variable, `ENV` config key, and `app.env`
    property are removed.
  - The `session_cookie_name`, `send_file_max_age_default`, `use_x_sendfile`,
    `propagate_exceptions`, and `templates_auto_reload` properties on `app`
    are removed.
  - The `JSON_AS_ASCII`, `JSON_SORT_KEYS`, `JSONIFY_MIMETYPE`, and
    `JSONIFY_PRETTYPRINT_REGULAR` config keys are removed.
  - The `app.before_first_request` and `bp.before_app_first_request` decorators
    are removed.
  - `json_encoder` and `json_decoder` attributes on app and blueprint, and the
    corresponding `json.JSONEncoder` and `JSONDecoder` classes, are removed.
  - The `json.htmlsafe_dumps` and `htmlsafe_dump` functions are removed.
  - Calling setup methods on blueprints after registration is an error instead of a
    warning. [#4997](https://github.com/pallets/flask/pull/4997)
- Importing `escape` and `Markup` from `flask` is deprecated. Import them
  directly from `markupsafe` instead. [#4996](https://github.com/pallets/flask/pull/4996)
- The `app.got_first_request` property is deprecated. [#4997](https://github.com/pallets/flask/pull/4997)
- The `locked_cached_property` decorator is deprecated. Use a lock inside the
  decorated function if locking is needed. [#4993](https://github.com/pallets/flask/issues/4993)
- Signals are always available. `blinker>=1.6.2` is a required dependency. The
  `signals_available` attribute is deprecated. [#5056](https://github.com/pallets/flask/issues/5056)
- Signals support `async` subscriber functions. [#5049](https://github.com/pallets/flask/pull/5049)
- Remove uses of locks that could cause requests to block each other very briefly.
  [#4993](https://github.com/pallets/flask/issues/4993)
- Use modern packaging metadata with `pyproject.toml` instead of `setup.cfg`.
  [#4947](https://github.com/pallets/flask/pull/4947)
- Ensure subdomains are applied with nested blueprints. [#4834](https://github.com/pallets/flask/issues/4834)
- `config.from_file` can use `text=False` to indicate that the parser wants a
  binary file instead. [#4989](https://github.com/pallets/flask/issues/4989)
- If a blueprint is created with an empty name it raises a `ValueError`.
  [#5010](https://github.com/pallets/flask/issues/5010)
- `SESSION_COOKIE_DOMAIN` does not fall back to `SERVER_NAME`. The default is not
  to set the domain, which modern browsers interpret as an exact match rather than
  a subdomain match. Warnings about `localhost` and IP addresses are also removed.
  [#5051](https://github.com/pallets/flask/issues/5051)
- The `routes` command shows each rule’s `subdomain` or `host` when domain
  matching is in use. [#5004](https://github.com/pallets/flask/issues/5004)
- Use postponed evaluation of annotations. [#5071](https://github.com/pallets/flask/pull/5071)

## Version 2.2.5

Released 2023-05-02

- Update for compatibility with Werkzeug 2.3.3.
- Set `Vary: Cookie` header when the session is accessed, modified, or refreshed.

## Version 2.2.4

Released 2023-04-25

- Update for compatibility with Werkzeug 2.3.

## Version 2.2.3

Released 2023-02-15

- Autoescape is enabled by default for `.svg` template files. [#4831](https://github.com/pallets/flask/issues/4831)
- Fix the type of `template_folder` to accept `pathlib.Path`. [#4892](https://github.com/pallets/flask/issues/4892)
- Add `--debug` option to the `flask run` command. [#4777](https://github.com/pallets/flask/issues/4777)

## Version 2.2.2

Released 2022-08-08

- Update Werkzeug dependency to >= 2.2.2. This includes fixes related
  to the new faster router, header parsing, and the development
  server. [#4754](https://github.com/pallets/flask/pull/4754)
- Fix the default value for `app.env` to be `"production"`. This
  attribute remains deprecated. [#4740](https://github.com/pallets/flask/issues/4740)

## Version 2.2.1

Released 2022-08-03

- Setting or accessing `json_encoder` or `json_decoder` raises a
  deprecation warning. [#4732](https://github.com/pallets/flask/issues/4732)

## Version 2.2.0

Released 2022-08-01

- Remove previously deprecated code. [#4667](https://github.com/pallets/flask/pull/4667)
  - Old names for some `send_file` parameters have been removed.
    `download_name` replaces `attachment_filename`, `max_age`
    replaces `cache_timeout`, and `etag` replaces `add_etags`.
    Additionally, `path` replaces `filename` in
    `send_from_directory`.
  - The `RequestContext.g` property returning `AppContext.g` is
    removed.
- Update Werkzeug dependency to >= 2.2.
- The app and request contexts are managed using Python context vars
  directly rather than Werkzeug’s `LocalStack`. This should result
  in better performance and memory use. [#4682](https://github.com/pallets/flask/pull/4682)
  - Extension maintainers, be aware that `_app_ctx_stack.top`
    and `_request_ctx_stack.top` are deprecated. Store data on
    `g` instead using a unique prefix, like
    `g._extension_name_attr`.
- The `FLASK_ENV` environment variable and `app.env` attribute are
  deprecated, removing the distinction between development and debug
  mode. Debug mode should be controlled directly using the `--debug`
  option or `app.run(debug=True)`. [#4714](https://github.com/pallets/flask/issues/4714)
- Some attributes that proxied config keys on `app` are deprecated:
  `session_cookie_name`, `send_file_max_age_default`,
  `use_x_sendfile`, `propagate_exceptions`, and
  `templates_auto_reload`. Use the relevant config keys instead.
  [#4716](https://github.com/pallets/flask/issues/4716)
- Add new customization points to the `Flask` app object for many
  previously global behaviors.
  - `flask.url_for` will call `app.url_for`. [#4568](https://github.com/pallets/flask/issues/4568)
  - `flask.abort` will call `app.aborter`.
    `Flask.aborter_class` and `Flask.make_aborter` can be used
    to customize this aborter. [#4567](https://github.com/pallets/flask/issues/4567)
  - `flask.redirect` will call `app.redirect`. [#4569](https://github.com/pallets/flask/issues/4569)
  - `flask.json` is an instance of `JSONProvider`. A different
    provider can be set to use a different JSON library.
    `flask.jsonify` will call `app.json.response`, other
    functions in `flask.json` will call corresponding functions in
    `app.json`. [#4692](https://github.com/pallets/flask/pull/4692)
- JSON configuration is moved to attributes on the default
  `app.json` provider. `JSON_AS_ASCII`, `JSON_SORT_KEYS`,
  `JSONIFY_MIMETYPE`, and `JSONIFY_PRETTYPRINT_REGULAR` are
  deprecated. [#4692](https://github.com/pallets/flask/pull/4692)
- Setting custom `json_encoder` and `json_decoder` classes on the
  app or a blueprint, and the corresponding `json.JSONEncoder` and
  `JSONDecoder` classes, are deprecated. JSON behavior can now be
  overridden using the `app.json` provider interface. [#4692](https://github.com/pallets/flask/pull/4692)
- `json.htmlsafe_dumps` and `json.htmlsafe_dump` are deprecated,
  the function is built-in to Jinja now. [#4692](https://github.com/pallets/flask/pull/4692)
- Refactor `register_error_handler` to consolidate error checking.
  Rewrite some error messages to be more consistent. [#4559](https://github.com/pallets/flask/issues/4559)
- Use Blueprint decorators and functions intended for setup after
  registering the blueprint will show a warning. In the next version,
  this will become an error just like the application setup methods.
  [#4571](https://github.com/pallets/flask/issues/4571)
- `before_first_request` is deprecated. Run setup code when creating
  the application instead. [#4605](https://github.com/pallets/flask/issues/4605)
- Added the `View.init_every_request` class attribute. If a view
  subclass sets this to `False`, the view will not create a new
  instance on every request. [#2520](https://github.com/pallets/flask/issues/2520).
- A `flask.cli.FlaskGroup` Click group can be nested as a
  sub-command in a custom CLI. [#3263](https://github.com/pallets/flask/issues/3263)
- Add `--app` and `--debug` options to the `flask` CLI, instead
  of requiring that they are set through environment variables.
  [#2836](https://github.com/pallets/flask/issues/2836)
- Add `--env-file` option to the `flask` CLI. This allows
  specifying a dotenv file to load in addition to `.env` and
  `.flaskenv`. [#3108](https://github.com/pallets/flask/issues/3108)
- It is no longer required to decorate custom CLI commands on
  `app.cli` or `blueprint.cli` with `@with_appcontext`, an app
  context will already be active at that point. [#2410](https://github.com/pallets/flask/issues/2410)
- `SessionInterface.get_expiration_time` uses a timezone-aware
  value. [#4645](https://github.com/pallets/flask/pull/4645)
- View functions can return generators directly instead of wrapping
  them in a `Response`. [#4629](https://github.com/pallets/flask/pull/4629)
- Add `stream_template` and `stream_template_string` functions to
  render a template as a stream of pieces. [#4629](https://github.com/pallets/flask/pull/4629)
- A new implementation of context preservation during debugging and
  testing. [#4666](https://github.com/pallets/flask/pull/4666)
  - `request`, `g`, and other context-locals point to the
    correct data when running code in the interactive debugger
    console. [#2836](https://github.com/pallets/flask/issues/2836)
  - Teardown functions are always run at the end of the request,
    even if the context is preserved. They are also run after the
    preserved context is popped.
  - `stream_with_context` preserves context separately from a
    `with client` block. It will be cleaned up when
    `response.get_data()` or `response.close()` is called.
- Allow returning a list from a view function, to convert it to a
  JSON response like a dict is. [#4672](https://github.com/pallets/flask/issues/4672)
- When type checking, allow `TypedDict` to be returned from view
  functions. [#4695](https://github.com/pallets/flask/pull/4695)
- Remove the `--eager-loading/--lazy-loading` options from the
  `flask run` command. The app is always eager loaded the first
  time, then lazily loaded in the reloader. The reloader always prints
  errors immediately but continues serving. Remove the internal
  `DispatchingApp` middleware used by the previous implementation.
  [#4715](https://github.com/pallets/flask/issues/4715)

## Version 2.1.3

Released 2022-07-13

- Inline some optional imports that are only used for certain CLI
  commands. [#4606](https://github.com/pallets/flask/pull/4606)
- Relax type annotation for `after_request` functions. [#4600](https://github.com/pallets/flask/issues/4600)
- `instance_path` for namespace packages uses the path closest to
  the imported submodule. [#4610](https://github.com/pallets/flask/issues/4610)
- Clearer error message when `render_template` and
  `render_template_string` are used outside an application context.
  [#4693](https://github.com/pallets/flask/pull/4693)

## Version 2.1.2

Released 2022-04-28

- Fix type annotation for `json.loads`, it accepts str or bytes.
  [#4519](https://github.com/pallets/flask/issues/4519)
- The `--cert` and `--key` options on `flask run` can be given
  in either order. [#4459](https://github.com/pallets/flask/issues/4459)

## Version 2.1.1

Released on 2022-03-30

- Set the minimum required version of importlib_metadata to 3.6.0,
  which is required on Python < 3.10. [#4502](https://github.com/pallets/flask/issues/4502)

## Version 2.1.0

Released 2022-03-28

- Drop support for Python 3.6. [#4335](https://github.com/pallets/flask/pull/4335)
- Update Click dependency to >= 8.0. [#4008](https://github.com/pallets/flask/pull/4008)
- Remove previously deprecated code. [#4337](https://github.com/pallets/flask/pull/4337)
  - The CLI does not pass `script_info` to app factory functions.
  - `config.from_json` is replaced by
    `config.from_file(name, load=json.load)`.
  - `json` functions no longer take an `encoding` parameter.
  - `safe_join` is removed, use `werkzeug.utils.safe_join`
    instead.
  - `total_seconds` is removed, use `timedelta.total_seconds`
    instead.
  - The same blueprint cannot be registered with the same name. Use
    `name=` when registering to specify a unique name.
  - The test client’s `as_tuple` parameter is removed. Use
    `response.request.environ` instead. [#4417](https://github.com/pallets/flask/pull/4417)
- Some parameters in `send_file` and `send_from_directory` were
  renamed in 2.0. The deprecation period for the old names is extended
  to 2.2. Be sure to test with deprecation warnings visible.
  - `attachment_filename` is renamed to `download_name`.
  - `cache_timeout` is renamed to `max_age`.
  - `add_etags` is renamed to `etag`.
  - `filename` is renamed to `path`.
- The `RequestContext.g` property is deprecated. Use `g` directly
  or `AppContext.g` instead. [#3898](https://github.com/pallets/flask/issues/3898)
- `copy_current_request_context` can decorate async functions.
  [#4303](https://github.com/pallets/flask/pull/4303)
- The CLI uses `importlib.metadata` instead of `pkg_resources` to
  load command entry points. [#4419](https://github.com/pallets/flask/issues/4419)
- Overriding `FlaskClient.open` will not cause an error on redirect.
  [#3396](https://github.com/pallets/flask/issues/3396)
- Add an `--exclude-patterns` option to the `flask run` CLI
  command to specify patterns that will be ignored by the reloader.
  [#4188](https://github.com/pallets/flask/issues/4188)
- When using lazy loading (the default with the debugger), the Click
  context from the `flask run` command remains available in the
  loader thread. [#4460](https://github.com/pallets/flask/issues/4460)
- Deleting the session cookie uses the `httponly` flag.
  [#4485](https://github.com/pallets/flask/issues/4485)
- Relax typing for `errorhandler` to allow the user to use more
  precise types and decorate the same function multiple times.
  [#4095, 4295, 4297](https://github.com/pallets/flask/issues/4095, 4295, 4297)
- Fix typing for `__exit__` methods for better compatibility with
  `ExitStack`. [#4474](https://github.com/pallets/flask/issues/4474)
- From Werkzeug, for redirect responses the `Location` header URL
  will remain relative, and exclude the scheme and domain, by default.
  [#4496](https://github.com/pallets/flask/pull/4496)
- Add `Config.from_prefixed_env()` to load config values from
  environment variables that start with `FLASK_` or another prefix.
  This parses values as JSON by default, and allows setting keys in
  nested dicts. [#4479](https://github.com/pallets/flask/pull/4479)

## Version 2.0.3

Released 2022-02-14

- The test client’s `as_tuple` parameter is deprecated and will be
  removed in Werkzeug 2.1. It is now also deprecated in Flask, to be
  removed in Flask 2.1, while remaining compatible with both in
  2.0.x. Use `response.request.environ` instead. [#4341](https://github.com/pallets/flask/pull/4341)
- Fix type annotation for `errorhandler` decorator. [#4295](https://github.com/pallets/flask/issues/4295)
- Revert a change to the CLI that caused it to hide `ImportError`
  tracebacks when importing the application. [#4307](https://github.com/pallets/flask/issues/4307)
- `app.json_encoder` and `json_decoder` are only passed to
  `dumps` and `loads` if they have custom behavior. This improves
  performance, mainly on PyPy. [#4349](https://github.com/pallets/flask/issues/4349)
- Clearer error message when `after_this_request` is used outside a
  request context. [#4333](https://github.com/pallets/flask/issues/4333)

## Version 2.0.2

Released 2021-10-04

- Fix type annotation for `teardown_*` methods. [#4093](https://github.com/pallets/flask/issues/4093)
- Fix type annotation for `before_request` and `before_app_request`
  decorators. [#4104](https://github.com/pallets/flask/issues/4104)
- Fixed the issue where typing requires template global
  decorators to accept functions with no arguments. [#4098](https://github.com/pallets/flask/issues/4098)
- Support View and MethodView instances with async handlers. [#4112](https://github.com/pallets/flask/issues/4112)
- Enhance typing of `app.errorhandler` decorator. [#4095](https://github.com/pallets/flask/issues/4095)
- Fix registering a blueprint twice with differing names. [#4124](https://github.com/pallets/flask/issues/4124)
- Fix the type of `static_folder` to accept `pathlib.Path`.
  [#4150](https://github.com/pallets/flask/issues/4150)
- `jsonify` handles `decimal.Decimal` by encoding to `str`.
  [#4157](https://github.com/pallets/flask/issues/4157)
- Correctly handle raising deferred errors in CLI lazy loading.
  [#4096](https://github.com/pallets/flask/issues/4096)
- The CLI loader handles `**kwargs` in a `create_app` function.
  [#4170](https://github.com/pallets/flask/issues/4170)
- Fix the order of `before_request` and other callbacks that trigger
  before the view returns. They are called from the app down to the
  closest nested blueprint. [#4229](https://github.com/pallets/flask/issues/4229)

## Version 2.0.1

Released 2021-05-21

- Re-add the `filename` parameter in `send_from_directory`. The
  `filename` parameter has been renamed to `path`, the old name
  is deprecated. [#4019](https://github.com/pallets/flask/pull/4019)
- Mark top-level names as exported so type checking understands
  imports in user projects. [#4024](https://github.com/pallets/flask/issues/4024)
- Fix type annotation for `g` and inform mypy that it is a namespace
  object that has arbitrary attributes. [#4020](https://github.com/pallets/flask/issues/4020)
- Fix some types that weren’t available in Python 3.6.0. [#4040](https://github.com/pallets/flask/issues/4040)
- Improve typing for `send_file`, `send_from_directory`, and
  `get_send_file_max_age`. [#4044](https://github.com/pallets/flask/issues/4044), [#4026](https://github.com/pallets/flask/pull/4026)
- Show an error when a blueprint name contains a dot. The `.` has
  special meaning, it is used to separate (nested) blueprint names and
  the endpoint name. [#4041](https://github.com/pallets/flask/issues/4041)
- Combine URL prefixes when nesting blueprints that were created with
  a `url_prefix` value. [#4037](https://github.com/pallets/flask/issues/4037)
- Revert a change to the order that URL matching was done. The
  URL is again matched after the session is loaded, so the session is
  available in custom URL converters. [#4053](https://github.com/pallets/flask/issues/4053)
- Re-add deprecated `Config.from_json`, which was accidentally
  removed early. [#4078](https://github.com/pallets/flask/issues/4078)
- Improve typing for some functions using `Callable` in their type
  signatures, focusing on decorator factories. [#4060](https://github.com/pallets/flask/issues/4060)
- Nested blueprints are registered with their dotted name. This allows
  different blueprints with the same name to be nested at different
  locations. [#4069](https://github.com/pallets/flask/issues/4069)
- `register_blueprint` takes a `name` option to change the
  (pre-dotted) name the blueprint is registered with. This allows the
  same blueprint to be registered multiple times with unique names for
  `url_for`. Registering the same blueprint with the same name
  multiple times is deprecated. [#1091](https://github.com/pallets/flask/issues/1091)
- Improve typing for `stream_with_context`. [#4052](https://github.com/pallets/flask/issues/4052)

## Version 2.0.0

Released 2021-05-11

- Drop support for Python 2 and 3.5.
- Bump minimum versions of other Pallets projects: Werkzeug >= 2,
  Jinja2 >= 3, MarkupSafe >= 2, ItsDangerous >= 2, Click >= 8. Be sure
  to check the change logs for each project. For better compatibility
  with other applications (e.g. Celery) that still require Click 7,
  there is no hard dependency on Click 8 yet, but using Click 7 will
  trigger a DeprecationWarning and Flask 2.1 will depend on Click 8.
- JSON support no longer uses simplejson. To use another JSON module,
  override `app.json_encoder` and `json_decoder`. [#3555](https://github.com/pallets/flask/issues/3555)
- The `encoding` option to JSON functions is deprecated. [#3562](https://github.com/pallets/flask/pull/3562)
- Passing `script_info` to app factory functions is deprecated. This
  was not portable outside the `flask` command. Use
  `click.get_current_context().obj` if it’s needed. [#3552](https://github.com/pallets/flask/issues/3552)
- The CLI shows better error messages when the app failed to load
  when looking up commands. [#2741](https://github.com/pallets/flask/issues/2741)
- Add `SessionInterface.get_cookie_name` to allow setting the
  session cookie name dynamically. [#3369](https://github.com/pallets/flask/pull/3369)
- Add `Config.from_file` to load config using arbitrary file
  loaders, such as `toml.load` or `json.load`.
  `Config.from_json` is deprecated in favor of this. [#3398](https://github.com/pallets/flask/pull/3398)
- The `flask run` command will only defer errors on reload. Errors
  present during the initial call will cause the server to exit with
  the traceback immediately. [#3431](https://github.com/pallets/flask/issues/3431)
- `send_file` raises a `ValueError` when passed an `io` object
  in text mode. Previously, it would respond with 200 OK and an empty
  file. [#3358](https://github.com/pallets/flask/issues/3358)
- When using ad-hoc certificates, check for the cryptography library
  instead of PyOpenSSL. [#3492](https://github.com/pallets/flask/pull/3492)
- When specifying a factory function with `FLASK_APP`, keyword
  argument can be passed. [#3553](https://github.com/pallets/flask/issues/3553)
- When loading a `.env` or `.flaskenv` file, the current working
  directory is no longer changed to the location of the file.
  [#3560](https://github.com/pallets/flask/pull/3560)
- When returning a `(response, headers)` tuple from a view, the
  headers replace rather than extend existing headers on the response.
  For example, this allows setting the `Content-Type` for
  `jsonify()`. Use `response.headers.extend()` if extending is
  desired. [#3628](https://github.com/pallets/flask/issues/3628)
- The `Scaffold` class provides a common API for the `Flask` and
  `Blueprint` classes. `Blueprint` information is stored in
  attributes just like `Flask`, rather than opaque lambda functions.
  This is intended to improve consistency and maintainability.
  [#3215](https://github.com/pallets/flask/issues/3215)
- Include `samesite` and `secure` options when removing the
  session cookie. [#3726](https://github.com/pallets/flask/pull/3726)
- Support passing a `pathlib.Path` to `static_folder`. [#3579](https://github.com/pallets/flask/pull/3579)
- `send_file` and `send_from_directory` are wrappers around the
  implementations in `werkzeug.utils`. [#3828](https://github.com/pallets/flask/pull/3828)
- Some `send_file` parameters have been renamed, the old names are
  deprecated. `attachment_filename` is renamed to `download_name`.
  `cache_timeout` is renamed to `max_age`. `add_etags` is
  renamed to `etag`. [#3828, 3883](https://github.com/pallets/flask/pull/3828, 3883)
- `send_file` passes `download_name` even if
  `as_attachment=False` by using `Content-Disposition: inline`.
  [#3828](https://github.com/pallets/flask/pull/3828)
- `send_file` sets `conditional=True` and `max_age=None` by
  default. `Cache-Control` is set to `no-cache` if `max_age` is
  not set, otherwise `public`. This tells browsers to validate
  conditional requests instead of using a timed cache. [#3828](https://github.com/pallets/flask/pull/3828)
- `helpers.safe_join` is deprecated. Use
  `werkzeug.utils.safe_join` instead. [#3828](https://github.com/pallets/flask/pull/3828)
- The request context does route matching before opening the session.
  This could allow a session interface to change behavior based on
  `request.endpoint`. [#3776](https://github.com/pallets/flask/issues/3776)
- Use Jinja’s implementation of the `|tojson` filter. [#3881](https://github.com/pallets/flask/issues/3881)
- Add route decorators for common HTTP methods. For example,
  `@app.post("/login")` is a shortcut for
  `@app.route("/login", methods=["POST"])`. [#3907](https://github.com/pallets/flask/pull/3907)
- Support async views, error handlers, before and after request, and
  teardown functions. [#3412](https://github.com/pallets/flask/pull/3412)
- Support nesting blueprints. [#593, 1548](https://github.com/pallets/flask/issues/593, 1548), [#3923](https://github.com/pallets/flask/pull/3923)
- Set the default encoding to “UTF-8” when loading `.env` and
  `.flaskenv` files to allow to use non-ASCII characters. [#3931](https://github.com/pallets/flask/issues/3931)
- `flask shell` sets up tab and history completion like the default
  `python` shell if `readline` is installed. [#3941](https://github.com/pallets/flask/issues/3941)
- `helpers.total_seconds()` is deprecated. Use
  `timedelta.total_seconds()` instead. [#3962](https://github.com/pallets/flask/pull/3962)
- Add type hinting. [#3973](https://github.com/pallets/flask/pull/3973).

## Version 1.1.4

Released 2021-05-13

- Update `static_folder` to use `_compat.fspath` instead of
  `os.fspath` to continue supporting Python < 3.6 [#4050](https://github.com/pallets/flask/issues/4050)

## Version 1.1.3

Released 2021-05-13

- Set maximum versions of Werkzeug, Jinja, Click, and ItsDangerous.
  [#4043](https://github.com/pallets/flask/issues/4043)
- Re-add support for passing a `pathlib.Path` for `static_folder`.
  [#3579](https://github.com/pallets/flask/pull/3579)

## Version 1.1.2

Released 2020-04-03

- Work around an issue when running the `flask` command with an
  external debugger on Windows. [#3297](https://github.com/pallets/flask/issues/3297)
- The static route will not catch all URLs if the `Flask` `static_folder` argument ends with a slash. [#3452](https://github.com/pallets/flask/issues/3452)

## Version 1.1.1

Released 2019-07-08

- The `flask.json_available` flag was added back for compatibility
  with some extensions. It will raise a deprecation warning when used,
  and will be removed in version 2.0.0. [#3288](https://github.com/pallets/flask/issues/3288)

## Version 1.1.0

Released 2019-07-04

- Bump minimum Werkzeug version to >= 0.15.
- Drop support for Python 3.4.
- Error handlers for `InternalServerError` or `500` will always be
  passed an instance of `InternalServerError`. If they are invoked
  due to an unhandled exception, that original exception is now
  available as `e.original_exception` rather than being passed
  directly to the handler. The same is true if the handler is for the
  base `HTTPException`. This makes error handler behavior more
  consistent. [#3266](https://github.com/pallets/flask/pull/3266)
  - `Flask.finalize_request` is called for all unhandled
    exceptions even if there is no `500` error handler.
- `Flask.logger` takes the same name as `Flask.name` (the value
  passed as `Flask(import_name)`. This reverts 1.0’s behavior of
  always logging to `"flask.app"`, in order to support multiple apps
  in the same process. A warning will be shown if old configuration is
  detected that needs to be moved. [#2866](https://github.com/pallets/flask/issues/2866)
- `RequestContext.copy` includes the current session object in the
  request context copy. This prevents `session` pointing to an
  out-of-date object. [#2935](https://github.com/pallets/flask/issues/2935)
- Using built-in RequestContext, unprintable Unicode characters in
  Host header will result in a HTTP 400 response and not HTTP 500 as
  previously. [#2994](https://github.com/pallets/flask/pull/2994)
- `send_file` supports `PathLike` objects as described in
  [PEP 519](https://peps.python.org/pep-0519/), to support `pathlib` in Python 3. [#3059](https://github.com/pallets/flask/pull/3059)
- `send_file` supports `BytesIO` partial content.
  [#2957](https://github.com/pallets/flask/issues/2957)
- `open_resource` accepts the “rt” file mode. This still does the
  same thing as “r”. [#3163](https://github.com/pallets/flask/issues/3163)
- The `MethodView.methods` attribute set in a base class is used by
  subclasses. [#3138](https://github.com/pallets/flask/issues/3138)
- `Flask.jinja_options` is a `dict` instead of an
  `ImmutableDict` to allow easier configuration. Changes must still
  be made before creating the environment. [#3190](https://github.com/pallets/flask/pull/3190)
- Flask’s `JSONMixin` for the request and response wrappers was
  moved into Werkzeug. Use Werkzeug’s version with Flask-specific
  support. This bumps the Werkzeug dependency to >= 0.15.
  [#3125](https://github.com/pallets/flask/issues/3125)
- The `flask` command entry point is simplified to take advantage
  of Werkzeug 0.15’s better reloader support. This bumps the Werkzeug
  dependency to >= 0.15. [#3022](https://github.com/pallets/flask/issues/3022)
- Support `static_url_path` that ends with a forward slash.
  [#3134](https://github.com/pallets/flask/issues/3134)
- Support empty `static_folder` without requiring setting an empty
  `static_url_path` as well. [#3124](https://github.com/pallets/flask/pull/3124)
- `jsonify` supports `dataclass` objects. [#3195](https://github.com/pallets/flask/pull/3195)
- Allow customizing the `Flask.url_map_class` used for routing.
  [#3069](https://github.com/pallets/flask/pull/3069)
- The development server port can be set to 0, which tells the OS to
  pick an available port. [#2926](https://github.com/pallets/flask/issues/2926)
- The return value from `cli.load_dotenv` is more consistent with
  the documentation. It will return `False` if python-dotenv is not
  installed, or if the given path isn’t a file. [#2937](https://github.com/pallets/flask/issues/2937)
- Signaling support has a stub for the `connect_via` method when
  the Blinker library is not installed. [#3208](https://github.com/pallets/flask/pull/3208)
- Add an `--extra-files` option to the `flask run` CLI command to
  specify extra files that will trigger the reloader on change.
  [#2897](https://github.com/pallets/flask/issues/2897)
- Allow returning a dictionary from a view function. Similar to how
  returning a string will produce a `text/html` response, returning
  a dict will call `jsonify` to produce a `application/json`
  response. [#3111](https://github.com/pallets/flask/pull/3111)
- Blueprints have a `cli` Click group like `app.cli`. CLI commands
  registered with a blueprint will be available as a group under the
  `flask` command. [#1357](https://github.com/pallets/flask/issues/1357).
- When using the test client as a context manager (`with client:`),
  all preserved request contexts are popped when the block exits,
  ensuring nested contexts are cleaned up correctly. [#3157](https://github.com/pallets/flask/pull/3157)
- Show a better error message when the view return type is not
  supported. [#3214](https://github.com/pallets/flask/issues/3214)
- `flask.testing.make_test_environ_builder()` has been deprecated in
  favour of a new class `flask.testing.EnvironBuilder`. [#3232](https://github.com/pallets/flask/pull/3232)
- The `flask run` command no longer fails if Python is not built
  with SSL support. Using the `--cert` option will show an
  appropriate error message. [#3211](https://github.com/pallets/flask/issues/3211)
- URL matching now occurs after the request context is pushed, rather
  than when it’s created. This allows custom URL converters to access
  the app and request contexts, such as to query a database for an id.
  [#3088](https://github.com/pallets/flask/issues/3088)

## Version 1.0.4

Released 2019-07-04

- The key information for `BadRequestKeyError` is no longer cleared
  outside debug mode, so error handlers can still access it. This
  requires upgrading to Werkzeug 0.15.5. [#3249](https://github.com/pallets/flask/issues/3249)
- `send_file` url quotes the “:” and “/” characters for more
  compatible UTF-8 filename support in some browsers. [#3074](https://github.com/pallets/flask/issues/3074)
- Fixes for [PEP 451](https://peps.python.org/pep-0451/) import loaders and pytest 5.x. [#3275](https://github.com/pallets/flask/issues/3275)
- Show message about dotenv on stderr instead of stdout. [#3285](https://github.com/pallets/flask/issues/3285)

## Version 1.0.3

Released 2019-05-17

- `send_file` encodes filenames as ASCII instead of Latin-1
  (ISO-8859-1). This fixes compatibility with Gunicorn, which is
  stricter about header encodings than [PEP 3333](https://peps.python.org/pep-3333/). [#2766](https://github.com/pallets/flask/issues/2766)
- Allow custom CLIs using `FlaskGroup` to set the debug flag without
  it always being overwritten based on environment variables.
  [#2765](https://github.com/pallets/flask/pull/2765)
- `flask --version` outputs Werkzeug’s version and simplifies the
  Python version. [#2825](https://github.com/pallets/flask/pull/2825)
- `send_file` handles an `attachment_filename` that is a native
  Python 2 string (bytes) with UTF-8 coded bytes. [#2933](https://github.com/pallets/flask/issues/2933)
- A catch-all error handler registered for `HTTPException` will not
  handle `RoutingException`, which is used internally during
  routing. This fixes the unexpected behavior that had been introduced
  in 1.0. [#2986](https://github.com/pallets/flask/pull/2986)
- Passing the `json` argument to `app.test_client` does not
  push/pop an extra app context. [#2900](https://github.com/pallets/flask/issues/2900)

## Version 1.0.2

Released 2018-05-02

- Fix more backwards compatibility issues with merging slashes between
  a blueprint prefix and route. [#2748](https://github.com/pallets/flask/pull/2748)
- Fix error with `flask routes` command when there are no routes.
  [#2751](https://github.com/pallets/flask/issues/2751)

## Version 1.0.1

Released 2018-04-29

- Fix registering partials (with no `__name__`) as view functions.
  [#2730](https://github.com/pallets/flask/pull/2730)
- Don’t treat lists returned from view functions the same as tuples.
  Only tuples are interpreted as response data. [#2736](https://github.com/pallets/flask/issues/2736)
- Extra slashes between a blueprint’s `url_prefix` and a route URL
  are merged. This fixes some backwards compatibility issues with the
  change in 1.0. [#2731](https://github.com/pallets/flask/issues/2731), [#2742](https://github.com/pallets/flask/issues/2742)
- Only trap `BadRequestKeyError` errors in debug mode, not all
  `BadRequest` errors. This allows `abort(400)` to continue
  working as expected. [#2735](https://github.com/pallets/flask/issues/2735)
- The `FLASK_SKIP_DOTENV` environment variable can be set to `1`
  to skip automatically loading dotenv files. [#2722](https://github.com/pallets/flask/issues/2722)

## Version 1.0

Released 2018-04-26

- Python 2.6 and 3.3 are no longer supported.
- Bump minimum dependency versions to the latest stable versions:
  Werkzeug >= 0.14, Jinja >= 2.10, itsdangerous >= 0.24, Click >= 5.1.
  [#2586](https://github.com/pallets/flask/issues/2586)
- Skip `app.run` when a Flask application is run from the command
  line. This avoids some behavior that was confusing to debug.
- Change the default for `JSONIFY_PRETTYPRINT_REGULAR` to
  `False`. `~json.jsonify` returns a compact format by default,
  and an indented format in debug mode. [#2193](https://github.com/pallets/flask/pull/2193)
- `Flask.__init__` accepts the `host_matching` argument and sets
  it on `Flask.url_map`. [#1559](https://github.com/pallets/flask/issues/1559)
- `Flask.__init__` accepts the `static_host` argument and passes
  it as the `host` argument when defining the static route.
  [#1559](https://github.com/pallets/flask/issues/1559)
- `send_file` supports Unicode in `attachment_filename`.
  [#2223](https://github.com/pallets/flask/pull/2223)
- Pass `_scheme` argument from `url_for` to
  `Flask.handle_url_build_error`. [#2017](https://github.com/pallets/flask/pull/2017)
- `Flask.add_url_rule` accepts the `provide_automatic_options`
  argument to disable adding the `OPTIONS` method. [#1489](https://github.com/pallets/flask/pull/1489)
- `MethodView` subclasses inherit method handlers from base classes.
  [#1936](https://github.com/pallets/flask/pull/1936)
- Errors caused while opening the session at the beginning of the
  request are handled by the app’s error handlers. [#2254](https://github.com/pallets/flask/pull/2254)
- Blueprints gained `Blueprint.json_encoder` and
  `Blueprint.json_decoder` attributes to override the app’s
  encoder and decoder. [#1898](https://github.com/pallets/flask/pull/1898)
- `Flask.make_response` raises `TypeError` instead of
  `ValueError` for bad response types. The error messages have been
  improved to describe why the type is invalid. [#2256](https://github.com/pallets/flask/pull/2256)
- Add `routes` CLI command to output routes registered on the
  application. [#2259](https://github.com/pallets/flask/pull/2259)
- Show warning when session cookie domain is a bare hostname or an IP
  address, as these may not behave properly in some browsers, such as
  Chrome. [#2282](https://github.com/pallets/flask/pull/2282)
- Allow IP address as exact session cookie domain. [#2282](https://github.com/pallets/flask/pull/2282)
- `SESSION_COOKIE_DOMAIN` is set if it is detected through
  `SERVER_NAME`. [#2282](https://github.com/pallets/flask/pull/2282)
- Auto-detect zero-argument app factory called `create_app` or
  `make_app` from `FLASK_APP`. [#2297](https://github.com/pallets/flask/pull/2297)
- Factory functions are not required to take a `script_info`
  parameter to work with the `flask` command. If they take a single
  parameter or a parameter named `script_info`, the `ScriptInfo`
  object will be passed. [#2319](https://github.com/pallets/flask/pull/2319)
- `FLASK_APP` can be set to an app factory, with arguments if
  needed, for example `FLASK_APP=myproject.app:create_app('dev')`.
  [#2326](https://github.com/pallets/flask/pull/2326)
- `FLASK_APP` can point to local packages that are not installed in
  editable mode, although `pip install -e` is still preferred.
  [#2414](https://github.com/pallets/flask/pull/2414)
- The `View` class attribute
  `View.provide_automatic_options` is set in `View.as_view`, to be
  detected by `Flask.add_url_rule`. [#2316](https://github.com/pallets/flask/pull/2316)
- Error handling will try handlers registered for `blueprint, code`,
  `app, code`, `blueprint, exception`, `app, exception`.
  [#2314](https://github.com/pallets/flask/pull/2314)
- `Cookie` is added to the response’s `Vary` header if the session
  is accessed at all during the request (and not deleted). [#2288](https://github.com/pallets/flask/pull/2288)
- `Flask.test_request_context` accepts `subdomain` and
  `url_scheme` arguments for use when building the base URL.
  [#1621](https://github.com/pallets/flask/pull/1621)
- Set `APPLICATION_ROOT` to `'/'` by default. This was already the
  implicit default when it was set to `None`.
- `TRAP_BAD_REQUEST_ERRORS` is enabled by default in debug mode.
  `BadRequestKeyError` has a message with the bad key in debug mode
  instead of the generic bad request message. [#2348](https://github.com/pallets/flask/pull/2348)
- Allow registering new tags with `TaggedJSONSerializer` to support
  storing other types in the session cookie. [#2352](https://github.com/pallets/flask/pull/2352)
- Only open the session if the request has not been pushed onto the
  context stack yet. This allows `stream_with_context` generators to
  access the same session that the containing view uses. [#2354](https://github.com/pallets/flask/pull/2354)
- Add `json` keyword argument for the test client request methods.
  This will dump the given object as JSON and set the appropriate
  content type. [#2358](https://github.com/pallets/flask/pull/2358)
- Extract JSON handling to a mixin applied to both the `Request` and
  `Response` classes. This adds the `Response.is_json` and
  `Response.get_json` methods to the response to make testing JSON
  response much easier. [#2358](https://github.com/pallets/flask/pull/2358)
- Removed error handler caching because it caused unexpected results
  for some exception inheritance hierarchies. Register handlers
  explicitly for each exception if you want to avoid traversing the
  MRO. [#2362](https://github.com/pallets/flask/pull/2362)
- Fix incorrect JSON encoding of aware, non-UTC datetimes. [#2374](https://github.com/pallets/flask/pull/2374)
- Template auto reloading will honor debug mode even if
  `Flask.jinja_env` was already accessed. [#2373](https://github.com/pallets/flask/pull/2373)
- The following old deprecated code was removed. [#2385](https://github.com/pallets/flask/issues/2385)
  - `flask.ext` - import extensions directly by their name instead
    of through the `flask.ext` namespace. For example,
    `import flask.ext.sqlalchemy` becomes
    `import flask_sqlalchemy`.
  - `Flask.init_jinja_globals` - extend
    `Flask.create_jinja_environment` instead.
  - `Flask.error_handlers` - tracked by
    `Flask.error_handler_spec`, use `Flask.errorhandler`
    to register handlers.
  - `Flask.request_globals_class` - use
    `Flask.app_ctx_globals_class` instead.
  - `Flask.static_path` - use `Flask.static_url_path` instead.
  - `Request.module` - use `Request.blueprint` instead.
- The `Request.json` property is no longer deprecated. [#1421](https://github.com/pallets/flask/issues/1421)
- Support passing a `EnvironBuilder` or `dict` to
  `test_client.open`. [#2412](https://github.com/pallets/flask/pull/2412)
- The `flask` command and `Flask.run` will load environment
  variables from `.env` and `.flaskenv` files if python-dotenv is
  installed. [#2416](https://github.com/pallets/flask/pull/2416)
- When passing a full URL to the test client, the scheme in the URL is
  used instead of `PREFERRED_URL_SCHEME`. [#2430](https://github.com/pallets/flask/pull/2430)
- `Flask.logger` has been simplified. `LOGGER_NAME` and
  `LOGGER_HANDLER_POLICY` config was removed. The logger is always
  named `flask.app`. The level is only set on first access, it
  doesn’t check `Flask.debug` each time. Only one format is used,
  not different ones depending on `Flask.debug`. No handlers are
  removed, and a handler is only added if no handlers are already
  configured. [#2436](https://github.com/pallets/flask/pull/2436)
- Blueprint view function names may not contain dots. [#2450](https://github.com/pallets/flask/pull/2450)
- Fix a `ValueError` caused by invalid `Range` requests in some
  cases. [#2526](https://github.com/pallets/flask/issues/2526)
- The development server uses threads by default. [#2529](https://github.com/pallets/flask/pull/2529)
- Loading config files with `silent=True` will ignore `ENOTDIR`
  errors. [#2581](https://github.com/pallets/flask/pull/2581)
- Pass `--cert` and `--key` options to `flask run` to run the
  development server over HTTPS. [#2606](https://github.com/pallets/flask/pull/2606)
- Added `SESSION_COOKIE_SAMESITE` to control the `SameSite`
  attribute on the session cookie. [#2607](https://github.com/pallets/flask/pull/2607)
- Added `Flask.test_cli_runner` to create a Click runner that can
  invoke Flask CLI commands for testing. [#2636](https://github.com/pallets/flask/pull/2636)
- Subdomain matching is disabled by default and setting
  `SERVER_NAME` does not implicitly enable it. It can be enabled by
  passing `subdomain_matching=True` to the `Flask` constructor.
  [#2635](https://github.com/pallets/flask/pull/2635)
- A single trailing slash is stripped from the blueprint
  `url_prefix` when it is registered with the app. [#2629](https://github.com/pallets/flask/pull/2629)
- `Request.get_json` doesn’t cache the result if parsing fails when
  `silent` is true. [#2651](https://github.com/pallets/flask/issues/2651)
- `Request.get_json` no longer accepts arbitrary encodings. Incoming
  JSON should be encoded using UTF-8 per [RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259.html), but Flask will
  autodetect UTF-8, -16, or -32. [#2691](https://github.com/pallets/flask/pull/2691)
- Added `MAX_COOKIE_SIZE` and `Response.max_cookie_size` to
  control when Werkzeug warns about large cookies that browsers may
  ignore. [#2693](https://github.com/pallets/flask/pull/2693)
- Updated documentation theme to make docs look better in small
  windows. [#2709](https://github.com/pallets/flask/pull/2709)
- Rewrote the tutorial docs and example project to take a more
  structured approach to help new users avoid common pitfalls.
  [#2676](https://github.com/pallets/flask/pull/2676)

## Version 0.12.5

Released 2020-02-10

- Pin Werkzeug to < 1.0.0. [#3497](https://github.com/pallets/flask/issues/3497)

## Version 0.12.4

Released 2018-04-29

- Repackage 0.12.3 to fix package layout issue. [#2728](https://github.com/pallets/flask/issues/2728)

## Version 0.12.3

Released 2018-04-26

- `Request.get_json` no longer accepts arbitrary encodings.
  Incoming JSON should be encoded using UTF-8 per [RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259.html), but
  Flask will autodetect UTF-8, -16, or -32. [#2692](https://github.com/pallets/flask/issues/2692)
- Fix a Python warning about imports when using `python -m flask`.
  [#2666](https://github.com/pallets/flask/issues/2666)
- Fix a `ValueError` caused by invalid `Range` requests in some
  cases.

## Version 0.12.2

Released 2017-05-16

- Fix a bug in `safe_join` on Windows.

## Version 0.12.1

Released 2017-03-31

- Prevent `flask run` from showing a `NoAppException` when an
  `ImportError` occurs within the imported application module.
- Fix encoding behavior of `app.config.from_pyfile` for Python 3.
  [#2118](https://github.com/pallets/flask/issues/2118)
- Use the `SERVER_NAME` config if it is present as default values
  for `app.run`. [#2109](https://github.com/pallets/flask/issues/2109), [#2152](https://github.com/pallets/flask/pull/2152)
- Call `ctx.auto_pop` with the exception object instead of `None`,
  in the event that a `BaseException` such as `KeyboardInterrupt`
  is raised in a request handler.

## Version 0.12

Released 2016-12-21, codename Punsch

- The cli command now responds to `--version`.
- Mimetype guessing and ETag generation for file-like objects in
  `send_file` has been removed. [#104](https://github.com/pallets/flask/issues/104), :pr`1849`
- Mimetype guessing in `send_file` now fails loudly and doesn’t fall
  back to `application/octet-stream`. [#1988](https://github.com/pallets/flask/pull/1988)
- Make `flask.safe_join` able to join multiple paths like
  `os.path.join` [#1730](https://github.com/pallets/flask/pull/1730)
- Revert a behavior change that made the dev server crash instead of
  returning an Internal Server Error. [#2006](https://github.com/pallets/flask/pull/2006)
- Correctly invoke response handlers for both regular request
  dispatching as well as error handlers.
- Disable logger propagation by default for the app logger.
- Add support for range requests in `send_file`.
- `app.test_client` includes preset default environment, which can
  now be directly set, instead of per `client.get`.
- Fix crash when running under PyPy3. [#1814](https://github.com/pallets/flask/pull/1814)

## Version 0.11.1

Released 2016-06-07

- Fixed a bug that prevented `FLASK_APP=foobar/__init__.py` from
  working. [#1872](https://github.com/pallets/flask/pull/1872)

## Version 0.11

Released 2016-05-29, codename Absinthe

- Added support to serializing top-level arrays to `jsonify`. This
  introduces a security risk in ancient browsers.
- Added before_render_template signal.
- Added `**kwargs` to `Flask.test_client` to support passing
  additional keyword arguments to the constructor of
  `Flask.test_client_class`.
- Added `SESSION_REFRESH_EACH_REQUEST` config key that controls the
  set-cookie behavior. If set to `True` a permanent session will be
  refreshed each request and get their lifetime extended, if set to
  `False` it will only be modified if the session actually modifies.
  Non permanent sessions are not affected by this and will always
  expire if the browser window closes.
- Made Flask support custom JSON mimetypes for incoming data.
- Added support for returning tuples in the form `(response,
  headers)` from a view function.
- Added `Config.from_json`.
- Added `Flask.config_class`.
- Added `Config.get_namespace`.
- Templates are no longer automatically reloaded outside of debug
  mode. This can be configured with the new `TEMPLATES_AUTO_RELOAD`
  config key.
- Added a workaround for a limitation in Python 3.3’s namespace
  loader.
- Added support for explicit root paths when using Python 3.3’s
  namespace packages.
- Added `flask` and the `flask.cli` module to start the
  local debug server through the click CLI system. This is recommended
  over the old `flask.run()` method as it works faster and more
  reliable due to a different design and also replaces
  `Flask-Script`.
- Error handlers that match specific classes are now checked first,
  thereby allowing catching exceptions that are subclasses of HTTP
  exceptions (in `werkzeug.exceptions`). This makes it possible for
  an extension author to create exceptions that will by default result
  in the HTTP error of their choosing, but may be caught with a custom
  error handler if desired.
- Added `Config.from_mapping`.
- Flask will now log by default even if debug is disabled. The log
  format is now hardcoded but the default log handling can be disabled
  through the `LOGGER_HANDLER_POLICY` configuration key.
- Removed deprecated module functionality.
- Added the `EXPLAIN_TEMPLATE_LOADING` config flag which when
  enabled will instruct Flask to explain how it locates templates.
  This should help users debug when the wrong templates are loaded.
- Enforce blueprint handling in the order they were registered for
  template loading.
- Ported test suite to py.test.
- Deprecated `request.json` in favour of `request.get_json()`.
- Add “pretty” and “compressed” separators definitions in jsonify()
  method. Reduces JSON response size when
  `JSONIFY_PRETTYPRINT_REGULAR=False` by removing unnecessary white
  space included by default after separators.
- JSON responses are now terminated with a newline character, because
  it is a convention that UNIX text files end with a newline and some
  clients don’t deal well when this newline is missing. [#1262](https://github.com/pallets/flask/pull/1262)
- The automatically provided `OPTIONS` method is now correctly
  disabled if the user registered an overriding rule with the
  lowercase-version `options`. [#1288](https://github.com/pallets/flask/issues/1288)
- `flask.json.jsonify` now supports the `datetime.date` type.
  [#1326](https://github.com/pallets/flask/pull/1326)
- Don’t leak exception info of already caught exceptions to context
  teardown handlers. [#1393](https://github.com/pallets/flask/pull/1393)
- Allow custom Jinja environment subclasses. [#1422](https://github.com/pallets/flask/pull/1422)
- Updated extension dev guidelines.
- `flask.g` now has `pop()` and `setdefault` methods.
- Turn on autoescape for `flask.templating.render_template_string`
  by default. [#1515](https://github.com/pallets/flask/pull/1515)
- `flask.ext` is now deprecated. [#1484](https://github.com/pallets/flask/pull/1484)
- `send_from_directory` now raises BadRequest if the filename is
  invalid on the server OS. [#1763](https://github.com/pallets/flask/pull/1763)
- Added the `JSONIFY_MIMETYPE` configuration variable. [#1728](https://github.com/pallets/flask/pull/1728)
- Exceptions during teardown handling will no longer leave bad
  application contexts lingering around.
- Fixed broken `test_appcontext_signals()` test case.
- Raise an `AttributeError` in `helpers.find_package` with a
  useful message explaining why it is raised when a [PEP 302](https://peps.python.org/pep-0302/) import
  hook is used without an `is_package()` method.
- Fixed an issue causing exceptions raised before entering a request
  or app context to be passed to teardown handlers.
- Fixed an issue with query parameters getting removed from requests
  in the test client when absolute URLs were requested.
- Made `@before_first_request` into a decorator as intended.
- Fixed an etags bug when sending a file streams with a name.
- Fixed `send_from_directory` not expanding to the application root
  path correctly.
- Changed logic of before first request handlers to flip the flag
  after invoking. This will allow some uses that are potentially
  dangerous but should probably be permitted.
- Fixed Python 3 bug when a handler from
  `app.url_build_error_handlers` reraises the `BuildError`.

## Version 0.10.1

Released 2013-06-14

- Fixed an issue where `|tojson` was not quoting single quotes which
  made the filter not work properly in HTML attributes. Now it’s
  possible to use that filter in single quoted attributes. This should
  make using that filter with angular.js easier.
- Added support for byte strings back to the session system. This
  broke compatibility with the common case of people putting binary
  data for token verification into the session.
- Fixed an issue where registering the same method twice for the same
  endpoint would trigger an exception incorrectly.

## Version 0.10

Released 2013-06-13, codename Limoncello

- Changed default cookie serialization format from pickle to JSON to
  limit the impact an attacker can do if the secret key leaks.
- Added `template_test` methods in addition to the already existing
  `template_filter` method family.
- Added `template_global` methods in addition to the already
  existing `template_filter` method family.
- Set the content-length header for x-sendfile.
- `tojson` filter now does not escape script blocks in HTML5
  parsers.
- `tojson` used in templates is now safe by default. This was
  allowed due to the different escaping behavior.
- Flask will now raise an error if you attempt to register a new
  function on an already used endpoint.
- Added wrapper module around simplejson and added default
  serialization of datetime objects. This allows much easier
  customization of how JSON is handled by Flask or any Flask
  extension.
- Removed deprecated internal `flask.session` module alias. Use
  `flask.sessions` instead to get the session module. This is not to
  be confused with `flask.session` the session proxy.
- Templates can now be rendered without request context. The behavior
  is slightly different as the `request`, `session` and `g`
  objects will not be available and blueprint’s context processors are
  not called.
- The config object is now available to the template as a real global
  and not through a context processor which makes it available even in
  imported templates by default.
- Added an option to generate non-ascii encoded JSON which should
  result in less bytes being transmitted over the network. It’s
  disabled by default to not cause confusion with existing libraries
  that might expect `flask.json.dumps` to return bytes by default.
- `flask.g` is now stored on the app context instead of the request
  context.
- `flask.g` now gained a `get()` method for not erroring out on
  non existing items.
- `flask.g` now can be used with the `in` operator to see what’s
  defined and it now is iterable and will yield all attributes stored.
- `flask.Flask.request_globals_class` got renamed to
  `flask.Flask.app_ctx_globals_class` which is a better name to what
  it does since 0.10.
- `request`, `session` and `g` are now also added as proxies to
  the template context which makes them available in imported
  templates. One has to be very careful with those though because
  usage outside of macros might cause caching.
- Flask will no longer invoke the wrong error handlers if a proxy
  exception is passed through.
- Added a workaround for chrome’s cookies in localhost not working as
  intended with domain names.
- Changed logic for picking defaults for cookie values from sessions
  to work better with Google Chrome.
- Added `message_flashed` signal that simplifies flashing testing.
- Added support for copying of request contexts for better working
  with greenlets.
- Removed custom JSON HTTP exception subclasses. If you were relying
  on them you can reintroduce them again yourself trivially. Using
  them however is strongly discouraged as the interface was flawed.
- Python requirements changed: requiring Python 2.6 or 2.7 now to
  prepare for Python 3.3 port.
- Changed how the teardown system is informed about exceptions. This
  is now more reliable in case something handles an exception halfway
  through the error handling process.
- Request context preservation in debug mode now keeps the exception
  information around which means that teardown handlers are able to
  distinguish error from success cases.
- Added the `JSONIFY_PRETTYPRINT_REGULAR` configuration variable.
- Flask now orders JSON keys by default to not trash HTTP caches due
  to different hash seeds between different workers.
- Added `appcontext_pushed` and `appcontext_popped` signals.
- The builtin run method now takes the `SERVER_NAME` into account
  when picking the default port to run on.
- Added `flask.request.get_json()` as a replacement for the old
  `flask.request.json` property.

## Version 0.9

Released 2012-07-01, codename Campari

- The `Request.on_json_loading_failed` now returns a JSON formatted
  response by default.
- The `url_for` function now can generate anchors to the generated
  links.
- The `url_for` function now can also explicitly generate URL rules
  specific to a given HTTP method.
- Logger now only returns the debug log setting if it was not set
  explicitly.
- Unregister a circular dependency between the WSGI environment and
  the request object when shutting down the request. This means that
  environ `werkzeug.request` will be `None` after the response was
  returned to the WSGI server but has the advantage that the garbage
  collector is not needed on CPython to tear down the request unless
  the user created circular dependencies themselves.
- Session is now stored after callbacks so that if the session payload
  is stored in the session you can still modify it in an after request
  callback.
- The `Flask` class will avoid importing the provided import name if
  it can (the required first parameter), to benefit tools which build
  Flask instances programmatically. The Flask class will fall back to
  using import on systems with custom module hooks, e.g. Google App
  Engine, or when the import name is inside a zip archive (usually an
  egg) prior to Python 2.7.
- Blueprints now have a decorator to add custom template filters
  application wide, `Blueprint.app_template_filter`.
- The Flask and Blueprint classes now have a non-decorator method for
  adding custom template filters application wide,
  `Flask.add_template_filter` and
  `Blueprint.add_app_template_filter`.
- The `get_flashed_messages` function now allows rendering flashed
  message categories in separate blocks, through a `category_filter`
  argument.
- The `Flask.run` method now accepts `None` for `host` and
  `port` arguments, using default values when `None`. This allows
  for calling run using configuration values, e.g.
  `app.run(app.config.get('MYHOST'), app.config.get('MYPORT'))`,
  with proper behavior whether or not a config file is provided.
- The `render_template` method now accepts a either an iterable of
  template names or a single template name. Previously, it only
  accepted a single template name. On an iterable, the first template
  found is rendered.
- Added `Flask.app_context` which works very similar to the request
  context but only provides access to the current application. This
  also adds support for URL generation without an active request
  context.
- View functions can now return a tuple with the first instance being
  an instance of `Response`. This allows for returning
  `jsonify(error="error msg"), 400` from a view function.
- `Flask` and `Blueprint` now provide a `get_send_file_max_age`
  hook for subclasses to override behavior of serving static files
  from Flask when using `Flask.send_static_file` (used for the
  default static file handler) and `helpers.send_file`. This hook is
  provided a filename, which for example allows changing cache
  controls by file extension. The default max-age for `send_file`
  and static files can be configured through a new
  `SEND_FILE_MAX_AGE_DEFAULT` configuration variable, which is used
  in the default `get_send_file_max_age` implementation.
- Fixed an assumption in sessions implementation which could break
  message flashing on sessions implementations which use external
  storage.
- Changed the behavior of tuple return values from functions. They are
  no longer arguments to the response object, they now have a defined
  meaning.
- Added `Flask.request_globals_class` to allow a specific class to
  be used on creation of the `g` instance of each request.
- Added `required_methods` attribute to view functions to force-add
  methods on registration.
- Added `flask.after_this_request`.
- Added `flask.stream_with_context` and the ability to push contexts
  multiple times without producing unexpected behavior.

## Version 0.8.1

Released 2012-07-01

- Fixed an issue with the undocumented `flask.session` module to not
  work properly on Python 2.5. It should not be used but did cause
  some problems for package managers.

## Version 0.8

Released 2011-09-29, codename Rakija

- Refactored session support into a session interface so that the
  implementation of the sessions can be changed without having to
  override the Flask class.
- Empty session cookies are now deleted properly automatically.
- View functions can now opt out of getting the automatic OPTIONS
  implementation.
- HTTP exceptions and Bad Request errors can now be trapped so that
  they show up normally in the traceback.
- Flask in debug mode is now detecting some common problems and tries
  to warn you about them.
- Flask in debug mode will now complain with an assertion error if a
  view was attached after the first request was handled. This gives
  earlier feedback when users forget to import view code ahead of
  time.
- Added the ability to register callbacks that are only triggered once
  at the beginning of the first request with
  `Flask.before_first_request`.
- Malformed JSON data will now trigger a bad request HTTP exception
  instead of a value error which usually would result in a 500
  internal server error if not handled. This is a backwards
  incompatible change.
- Applications now not only have a root path where the resources and
  modules are located but also an instance path which is the
  designated place to drop files that are modified at runtime (uploads
  etc.). Also this is conceptually only instance depending and outside
  version control so it’s the perfect place to put configuration files
  etc.
- Added the `APPLICATION_ROOT` configuration variable.
- Implemented `TestClient.session_transaction` to easily modify
  sessions from the test environment.
- Refactored test client internally. The `APPLICATION_ROOT`
  configuration variable as well as `SERVER_NAME` are now properly
  used by the test client as defaults.
- Added `View.decorators` to support simpler decorating of pluggable
  (class-based) views.
- Fixed an issue where the test client if used with the “with”
  statement did not trigger the execution of the teardown handlers.
- Added finer control over the session cookie parameters.
- HEAD requests to a method view now automatically dispatch to the
  `get` method if no handler was implemented.
- Implemented the virtual `flask.ext` package to import extensions
  from.
- The context preservation on exceptions is now an integral component
  of Flask itself and no longer of the test client. This cleaned up
  some internal logic and lowers the odds of runaway request contexts
  in unittests.
- Fixed the Jinja environment’s `list_templates` method not
  returning the correct names when blueprints or modules were
  involved.

## Version 0.7.2

Released 2011-07-06

- Fixed an issue with URL processors not properly working on
  blueprints.

## Version 0.7.1

Released 2011-06-29

- Added missing future import that broke 2.5 compatibility.
- Fixed an infinite redirect issue with blueprints.

## Version 0.7

Released 2011-06-28, codename Grappa

- Added `Flask.make_default_options_response` which can be used by
  subclasses to alter the default behavior for `OPTIONS` responses.
- Unbound locals now raise a proper `RuntimeError` instead of an
  `AttributeError`.
- Mimetype guessing and etag support based on file objects is now
  deprecated for `send_file` because it was unreliable. Pass
  filenames instead or attach your own etags and provide a proper
  mimetype by hand.
- Static file handling for modules now requires the name of the static
  folder to be supplied explicitly. The previous autodetection was not
  reliable and caused issues on Google’s App Engine. Until 1.0 the old
  behavior will continue to work but issue dependency warnings.
- Fixed a problem for Flask to run on jython.
- Added a `PROPAGATE_EXCEPTIONS` configuration variable that can be
  used to flip the setting of exception propagation which previously
  was linked to `DEBUG` alone and is now linked to either `DEBUG`
  or `TESTING`.
- Flask no longer internally depends on rules being added through the
  `add_url_rule` function and can now also accept regular werkzeug
  rules added to the url map.
- Added an `endpoint` method to the flask application object which
  allows one to register a callback to an arbitrary endpoint with a
  decorator.
- Use Last-Modified for static file sending instead of Date which was
  incorrectly introduced in 0.6.
- Added `create_jinja_loader` to override the loader creation
  process.
- Implemented a silent flag for `config.from_pyfile`.
- Added `teardown_request` decorator, for functions that should run
  at the end of a request regardless of whether an exception occurred.
  Also the behavior for `after_request` was changed. It’s now no
  longer executed when an exception is raised.
- Implemented `has_request_context`.
- Deprecated `init_jinja_globals`. Override the
  `Flask.create_jinja_environment` method instead to achieve the
  same functionality.
- Added `safe_join`.
- The automatic JSON request data unpacking now looks at the charset
  mimetype parameter.
- Don’t modify the session on `get_flashed_messages` if there are no
  messages in the session.
- `before_request` handlers are now able to abort requests with
  errors.
- It is not possible to define user exception handlers. That way you
  can provide custom error messages from a central hub for certain
  errors that might occur during request processing (for instance
  database connection errors, timeouts from remote resources etc.).
- Blueprints can provide blueprint specific error handlers.
- Implemented generic class-based views.

## Version 0.6.1

Released 2010-12-31

- Fixed an issue where the default `OPTIONS` response was not
  exposing all valid methods in the `Allow` header.
- Jinja template loading syntax now allows “./” in front of a
  template load path. Previously this caused issues with module
  setups.
- Fixed an issue where the subdomain setting for modules was ignored
  for the static folder.
- Fixed a security problem that allowed clients to download arbitrary
  files if the host server was a windows based operating system and
  the client uses backslashes to escape the directory the files where
  exposed from.

## Version 0.6

Released 2010-07-27, codename Whisky

- After request functions are now called in reverse order of
  registration.
- OPTIONS is now automatically implemented by Flask unless the
  application explicitly adds ‘OPTIONS’ as method to the URL rule. In
  this case no automatic OPTIONS handling kicks in.
- Static rules are now even in place if there is no static folder for
  the module. This was implemented to aid GAE which will remove the
  static folder if it’s part of a mapping in the .yml file.
- `Flask.config` is now available in the templates as `config`.
- Context processors will no longer override values passed directly to
  the render function.
- Added the ability to limit the incoming request data with the new
  `MAX_CONTENT_LENGTH` configuration value.
- The endpoint for the `Module.add_url_rule` method is now optional
  to be consistent with the function of the same name on the
  application object.
- Added a `make_response` function that simplifies creating response
  object instances in views.
- Added signalling support based on blinker. This feature is currently
  optional and supposed to be used by extensions and applications. If
  you want to use it, make sure to have `blinker` installed.
- Refactored the way URL adapters are created. This process is now
  fully customizable with the `Flask.create_url_adapter` method.
- Modules can now register for a subdomain instead of just an URL
  prefix. This makes it possible to bind a whole module to a
  configurable subdomain.

## Version 0.5.2

Released 2010-07-15

- Fixed another issue with loading templates from directories when
  modules were used.

## Version 0.5.1

Released 2010-07-06

- Fixes an issue with template loading from directories when modules
  where used.

## Version 0.5

Released 2010-07-06, codename Calvados

- Fixed a bug with subdomains that was caused by the inability to
  specify the server name. The server name can now be set with the
  `SERVER_NAME` config key. This key is now also used to set the
  session cookie cross-subdomain wide.
- Autoescaping is no longer active for all templates. Instead it is
  only active for `.html`, `.htm`, `.xml` and `.xhtml`. Inside
  templates this behavior can be changed with the `autoescape` tag.
- Refactored Flask internally. It now consists of more than a single
  file.
- `send_file` now emits etags and has the ability to do conditional
  responses builtin.
- (temporarily) dropped support for zipped applications. This was a
  rarely used feature and led to some confusing behavior.
- Added support for per-package template and static-file directories.
- Removed support for `create_jinja_loader` which is no longer used
  in 0.5 due to the improved module support.
- Added a helper function to expose files from any directory.

## Version 0.4

Released 2010-06-18, codename Rakia

- Added the ability to register application wide error handlers from
  modules.
- `Flask.after_request` handlers are now also invoked if the request
  dies with an exception and an error handling page kicks in.
- Test client has not the ability to preserve the request context for
  a little longer. This can also be used to trigger custom requests
  that do not pop the request stack for testing.
- Because the Python standard library caches loggers, the name of the
  logger is configurable now to better support unittests.
- Added `TESTING` switch that can activate unittesting helpers.
- The logger switches to `DEBUG` mode now if debug is enabled.

## Version 0.3.1

Released 2010-05-28

- Fixed a error reporting bug with `Config.from_envvar`.
- Removed some unused code.
- Release does no longer include development leftover files (.git
  folder for themes, built documentation in zip and pdf file and some
  .pyc files)

## Version 0.3

Released 2010-05-28, codename Schnaps

- Added support for categories for flashed messages.
- The application now configures a `logging.Handler` and will log
  request handling exceptions to that logger when not in debug mode.
  This makes it possible to receive mails on server errors for
  example.
- Added support for context binding that does not require the use of
  the with statement for playing in the console.
- The request context is now available within the with statement
  making it possible to further push the request context or pop it.
- Added support for configurations.

## Version 0.2

Released 2010-05-12, codename J?germeister

- Various bugfixes
- Integrated JSON support
- Added `get_template_attribute` helper function.
- `Flask.add_url_rule` can now also register a view function.
- Refactored internal request dispatching.
- Server listens on 127.0.0.1 by default now to fix issues with
  chrome.
- Added external URL support.
- Added support for `send_file`.
- Module support and internal request handling refactoring to better
  support pluggable applications.
- Sessions can be set to be permanent now on a per-session basis.
- Better error reporting on missing secret keys.
- Added support for Google Appengine.

## Version 0.1

Released 2010-04-16

- First public preview release.
