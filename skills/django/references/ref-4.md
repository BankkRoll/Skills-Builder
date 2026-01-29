---

# django.contrib.auth¶

# django.contrib.auth¶

This document provides API reference material for the components of Django’s
authentication system. For more details on the usage of these components or
how to customize authentication and authorization see the [authentication
topic guide](https://docs.djangoproject.com/en/topics/auth/).

## Usermodel¶

   *class*models.User[¶](#django.contrib.auth.models.User)

### Fields¶

   *class*models.User

[User](#django.contrib.auth.models.User) objects have the following
fields:

   username[¶](#django.contrib.auth.models.User.username)

Required. 150 characters or fewer. Usernames may contain alphanumeric,
`_`, `@`, `+`, `.` and `-` characters.

The `max_length` should be sufficient for many use cases. If you need
a longer length, please use a [custom user model](https://docs.djangoproject.com/en/topics/auth/customizing/#specifying-custom-user-model). If you use MySQL with the `utf8mb4`
encoding (recommended for proper Unicode support), specify at most
`max_length=191` because MySQL can only create unique indexes with
191 characters in that case by default.

    first_name[¶](#django.contrib.auth.models.User.first_name)

Optional ([blank=True](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.blank)). 150
characters or fewer.

    last_name[¶](#django.contrib.auth.models.User.last_name)

Optional ([blank=True](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.blank)). 150
characters or fewer.

    email[¶](#django.contrib.auth.models.User.email)

Optional ([blank=True](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.blank)). Email
address.

    password[¶](#django.contrib.auth.models.User.password)

Required. A hash of, and metadata about, the password. (Django doesn’t
store the raw password.) Raw passwords can be arbitrarily long and can
contain any character. See the [password documentation](https://docs.djangoproject.com/en/topics/auth/passwords/).

    groups[¶](#django.contrib.auth.models.User.groups)

Many-to-many relationship to [Group](#django.contrib.auth.models.Group)

    user_permissions[¶](#django.contrib.auth.models.User.user_permissions)

Many-to-many relationship to [Permission](#django.contrib.auth.models.Permission)

    is_staff[¶](#django.contrib.auth.models.User.is_staff)

Boolean. Allows this user to access the admin site.

    is_active[¶](#django.contrib.auth.models.User.is_active)

Boolean. Marks this user account as active. We recommend that you set
this flag to `False` instead of deleting accounts. That way, if your
applications have any foreign keys to users, the foreign keys won’t
break.

This doesn’t necessarily control whether or not the user can log in.
Authentication backends aren’t required to check for the `is_active`
flag but the default backend
([ModelBackend](#django.contrib.auth.backends.ModelBackend)) and the
[RemoteUserBackend](#django.contrib.auth.backends.RemoteUserBackend) do. You can
use [AllowAllUsersModelBackend](#django.contrib.auth.backends.AllowAllUsersModelBackend)
or [AllowAllUsersRemoteUserBackend](#django.contrib.auth.backends.AllowAllUsersRemoteUserBackend)
if you want to allow inactive users to login. In this case, you’ll also
want to customize the
[AuthenticationForm](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm) used by the
[LoginView](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.views.LoginView) as it rejects inactive
users. Be aware that the permission-checking methods such as
[has_perm()](#django.contrib.auth.models.User.has_perm) and the
authentication in the Django admin all return `False` for inactive
users.

    is_superuser[¶](#django.contrib.auth.models.User.is_superuser)

Boolean. Treats this user as having all permissions without assigning
any permission to it in particular.

    last_login[¶](#django.contrib.auth.models.User.last_login)

A datetime of the user’s last login.

    date_joined[¶](#django.contrib.auth.models.User.date_joined)

The date/time when the account was created.

### Attributes¶

   *class*models.User   is_authenticated[¶](#django.contrib.auth.models.User.is_authenticated)

Read-only attribute which is always `True` (as opposed to
`AnonymousUser.is_authenticated` which is always `False`). This is
a way to tell if the user has been authenticated. This does not imply
any permissions and doesn’t check if the user is active or has a valid
session. Even though normally you will check this attribute on
`request.user` to find out whether it has been populated by the
[AuthenticationMiddleware](https://docs.djangoproject.com/en/5.0/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware)
(representing the currently logged-in user), you should know this
attribute is `True` for any [User](#django.contrib.auth.models.User) instance.

    is_anonymous[¶](#django.contrib.auth.models.User.is_anonymous)

Read-only attribute which is always `False`. This is a way of
differentiating [User](#django.contrib.auth.models.User) and [AnonymousUser](#django.contrib.auth.models.AnonymousUser)
objects. Generally, you should prefer using
[is_authenticated](#django.contrib.auth.models.User.is_authenticated) to this
attribute.

### Methods¶

   *class*models.User   get_username()[¶](#django.contrib.auth.models.User.get_username)

Returns the username for the user. Since the `User` model can be
swapped out, you should use this method instead of referencing the
username attribute directly.

    get_full_name()[¶](#django.contrib.auth.models.User.get_full_name)

Returns the [first_name](#django.contrib.auth.models.User.first_name) plus
the [last_name](#django.contrib.auth.models.User.last_name), with a space in
between.

    get_short_name()[¶](#django.contrib.auth.models.User.get_short_name)

Returns the [first_name](#django.contrib.auth.models.User.first_name).

    set_password(*raw_password*)[¶](#django.contrib.auth.models.User.set_password)

Sets the user’s password to the given raw string, taking care of the
password hashing. Doesn’t save the
[User](#django.contrib.auth.models.User) object.

When the `raw_password` is `None`, the password will be set to an
unusable password, as if
[set_unusable_password()](#django.contrib.auth.models.User.set_unusable_password)
were used.

    check_password(*raw_password*)[¶](#django.contrib.auth.models.User.check_password)    acheck_password(*raw_password*)[¶](#django.contrib.auth.models.User.acheck_password)

*Asynchronous version*: `acheck_password()`

Returns `True` if the given raw string is the correct password for
the user. (This takes care of the password hashing in making the
comparison.)

  Changed in Django 5.0:

`acheck_password()` method was added.

     set_unusable_password()[¶](#django.contrib.auth.models.User.set_unusable_password)

Marks the user as having no password set.  This isn’t the same as
having a blank string for a password.
[check_password()](#django.contrib.auth.models.User.check_password) for this user
will never return `True`. Doesn’t save the
[User](#django.contrib.auth.models.User) object.

You may need this if authentication for your application takes place
against an existing external source such as an LDAP directory.

Password reset restriction

Users having an unusable password will not able to request a
password reset email via
[PasswordResetView](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.views.PasswordResetView).

     has_usable_password()[¶](#django.contrib.auth.models.User.has_usable_password)

Returns `False` if
[set_unusable_password()](#django.contrib.auth.models.User.set_unusable_password) has
been called for this user.

    get_user_permissions(*obj=None*)[¶](#django.contrib.auth.models.User.get_user_permissions)

Returns a set of permission strings that the user has directly.

If `obj` is passed in, only returns the user permissions for this
specific object.

    get_group_permissions(*obj=None*)[¶](#django.contrib.auth.models.User.get_group_permissions)

Returns a set of permission strings that the user has, through their
groups.

If `obj` is passed in, only returns the group permissions for
this specific object.

    get_all_permissions(*obj=None*)[¶](#django.contrib.auth.models.User.get_all_permissions)

Returns a set of permission strings that the user has, both through
group and user permissions.

If `obj` is passed in, only returns the permissions for this
specific object.

    has_perm(*perm*, *obj=None*)[¶](#django.contrib.auth.models.User.has_perm)

Returns `True` if the user has the specified permission, where perm
is in the format `"<app label>.<permission codename>"`. (see
documentation on [permissions](https://docs.djangoproject.com/en/topics/auth/default/#topic-authorization)). If the user is
inactive, this method will always return `False`. For an active
superuser, this method will always return `True`.

If `obj` is passed in, this method won’t check for a permission for
the model, but for this specific object.

    has_perms(*perm_list*, *obj=None*)[¶](#django.contrib.auth.models.User.has_perms)

Returns `True` if the user has each of the specified permissions,
where each perm is in the format
`"<app label>.<permission codename>"`. If the user is inactive,
this method will always return `False`. For an active superuser, this
method will always return `True`.

If `obj` is passed in, this method won’t check for permissions for
the model, but for the specific object.

    has_module_perms(*package_name*)[¶](#django.contrib.auth.models.User.has_module_perms)

Returns `True` if the user has any permissions in the given package
(the Django app label). If the user is inactive, this method will
always return `False`. For an active superuser, this method will
always return `True`.

    email_user(*subject*, *message*, *from_email=None*, ***kwargs*)[¶](#django.contrib.auth.models.User.email_user)

Sends an email to the user. If `from_email` is `None`, Django uses
the [DEFAULT_FROM_EMAIL](https://docs.djangoproject.com/en/5.0/settings/#std-setting-DEFAULT_FROM_EMAIL). Any `**kwargs` are passed to the
underlying [send_mail()](https://docs.djangoproject.com/en/topics/email/#django.core.mail.send_mail) call.

### Manager methods¶

   *class*models.UserManager[¶](#django.contrib.auth.models.UserManager)

The [User](#django.contrib.auth.models.User) model has a custom manager
that has the following helper methods (in addition to the methods provided
by [BaseUserManager](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager)):

   create_user(*username*, *email=None*, *password=None*, ***extra_fields*)[¶](#django.contrib.auth.models.UserManager.create_user)

Creates, saves and returns a [User](#django.contrib.auth.models.User).

The [username](#django.contrib.auth.models.User.username) and
[password](#django.contrib.auth.models.User.password) are set as given. The
domain portion of [email](#django.contrib.auth.models.User.email) is
automatically converted to lowercase, and the returned
[User](#django.contrib.auth.models.User) object will have
[is_active](#django.contrib.auth.models.User.is_active) set to `True`.

If no password is provided,
[set_unusable_password()](#django.contrib.auth.models.User.set_unusable_password) will
be called.

The `extra_fields` keyword arguments are passed through to the
[User](#django.contrib.auth.models.User)’s `__init__` method to
allow setting arbitrary fields on a [custom user model](https://docs.djangoproject.com/en/topics/auth/customizing/#auth-custom-user).

See [Creating users](https://docs.djangoproject.com/en/topics/auth/default/#topics-auth-creating-users) for example usage.

    create_superuser(*username*, *email=None*, *password=None*, ***extra_fields*)[¶](#django.contrib.auth.models.UserManager.create_superuser)

Same as [create_user()](#django.contrib.auth.models.UserManager.create_user), but sets [is_staff](#django.contrib.auth.models.User.is_staff) and
[is_superuser](#django.contrib.auth.models.User.is_superuser) to `True`.

    with_perm(*perm*, *is_active=True*, *include_superusers=True*, *backend=None*, *obj=None*)[¶](#django.contrib.auth.models.UserManager.with_perm)

Returns users that have the given permission `perm` either in the
`"<app label>.<permission codename>"` format or as a
[Permission](#django.contrib.auth.models.Permission) instance. Returns an
empty queryset if no users who have the `perm` found.

If `is_active` is `True` (default), returns only active users, or
if `False`, returns only inactive users. Use `None` to return all
users irrespective of active state.

If `include_superusers` is `True` (default), the result will
include superusers.

If `backend` is passed in and it’s defined in
[AUTHENTICATION_BACKENDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTHENTICATION_BACKENDS), then this method will use it.
Otherwise, it will use the `backend` in
[AUTHENTICATION_BACKENDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTHENTICATION_BACKENDS), if there is only one, or raise an
exception.

## AnonymousUserobject¶

   *class*models.AnonymousUser[¶](#django.contrib.auth.models.AnonymousUser)

[django.contrib.auth.models.AnonymousUser](#django.contrib.auth.models.AnonymousUser) is a class that
implements the [django.contrib.auth.models.User](#django.contrib.auth.models.User) interface, with
these differences:

- [id](https://docs.djangoproject.com/en/topics/db/models/#automatic-primary-key-fields) is always `None`.
- [username](#django.contrib.auth.models.User.username) is always the empty
  string.
- [get_username()](#django.contrib.auth.models.User.get_username) always returns
  the empty string.
- [is_anonymous](#django.contrib.auth.models.User.is_anonymous) is `True`
  instead of `False`.
- [is_authenticated](#django.contrib.auth.models.User.is_authenticated) is
  `False` instead of `True`.
- [is_staff](#django.contrib.auth.models.User.is_staff) and
  [is_superuser](#django.contrib.auth.models.User.is_superuser) are always
  `False`.
- [is_active](#django.contrib.auth.models.User.is_active) is always `False`.
- [groups](#django.contrib.auth.models.User.groups) and
  [user_permissions](#django.contrib.auth.models.User.user_permissions) are always
  empty.
- [set_password()](#django.contrib.auth.models.User.set_password),
  [check_password()](#django.contrib.auth.models.User.check_password),
  [save()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.save) and
  [delete()](https://docs.djangoproject.com/en/5.0/models/instances/#django.db.models.Model.delete) raise [NotImplementedError](https://docs.python.org/3/library/exceptions.html#NotImplementedError).

In practice, you probably won’t need to use
[AnonymousUser](#django.contrib.auth.models.AnonymousUser) objects on your own, but
they’re used by web requests, as explained in the next section.

## Permissionmodel¶

   *class*models.Permission[¶](#django.contrib.auth.models.Permission)

### Fields¶

[Permission](#django.contrib.auth.models.Permission) objects have the following
fields:

   *class*models.Permission   name[¶](#django.contrib.auth.models.Permission.name)

Required. 255 characters or fewer. Example: `'Can vote'`.

    content_type[¶](#django.contrib.auth.models.Permission.content_type)

Required. A reference to the `django_content_type` database table,
which contains a record for each installed model.

    codename[¶](#django.contrib.auth.models.Permission.codename)

Required. 100 characters or fewer. Example: `'can_vote'`.

### Methods¶

[Permission](#django.contrib.auth.models.Permission) objects have the standard
data-access methods like any other [Django model](https://docs.djangoproject.com/en/5.0/models/instances/).

## Groupmodel¶

   *class*models.Group[¶](#django.contrib.auth.models.Group)

### Fields¶

[Group](#django.contrib.auth.models.Group) objects have the following fields:

   *class*models.Group   name[¶](#django.contrib.auth.models.Group.name)

Required. 150 characters or fewer. Any characters are permitted.
Example: `'Awesome Users'`.

    permissions[¶](#django.contrib.auth.models.Group.permissions)

Many-to-many field to [Permission](#django.contrib.auth.models.Permission):

```
group.permissions.set([permission_list])
group.permissions.add(permission, permission, ...)
group.permissions.remove(permission, permission, ...)
group.permissions.clear()
```

## Validators¶

   *class*validators.ASCIIUsernameValidator[¶](#django.contrib.auth.validators.ASCIIUsernameValidator)

A field validator allowing only ASCII letters and numbers, in addition to
`@`, `.`, `+`, `-`, and `_`.

    *class*validators.UnicodeUsernameValidator[¶](#django.contrib.auth.validators.UnicodeUsernameValidator)

A field validator allowing Unicode characters, in addition to `@`, `.`,
`+`, `-`, and `_`. The default validator for `User.username`.

## Login and logout signals¶

The auth framework uses the following [signals](https://docs.djangoproject.com/en/topics/signals/) that
can be used for notification when a user logs in or out.

   user_logged_in[¶](#django.contrib.auth.signals.user_logged_in)

Sent when a user logs in successfully.

Arguments sent with this signal:

  `sender`

The class of the user that just logged in.

  `request`

The current [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) instance.

  `user`

The user instance that just logged in.

      user_logged_out[¶](#django.contrib.auth.signals.user_logged_out)

Sent when the logout method is called.

  `sender`

As above: the class of the user that just logged out or `None`
if the user was not authenticated.

  `request`

The current [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) instance.

  `user`

The user instance that just logged out or `None` if the
user was not authenticated.

      user_login_failed[¶](#django.contrib.auth.signals.user_login_failed)

Sent when the user failed to login successfully

  `sender`

The name of the module used for authentication.

  `credentials`

A dictionary of keyword arguments containing the user credentials that were
passed to [authenticate()](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.authenticate) or your own custom
authentication backend. Credentials matching a set of ‘sensitive’ patterns,
(including password) will not be sent in the clear as part of the signal.

  `request`

The [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) object, if one was provided to
[authenticate()](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.authenticate).

## Authentication backends¶

This section details the authentication backends that come with Django. For
information on how to use them and how to write your own authentication
backends, see the [Other authentication sources section](https://docs.djangoproject.com/en/topics/auth/customizing/#authentication-backends) of the [User authentication guide](https://docs.djangoproject.com/en/topics/auth/).

### Available authentication backends¶

The following backends are available in [django.contrib.auth.backends](#module-django.contrib.auth.backends):

   *class*BaseBackend[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#BaseBackend)[¶](#django.contrib.auth.backends.BaseBackend)

A base class that provides default implementations for all required
methods. By default, it will reject any user and provide no permissions.

   get_user_permissions(*user_obj*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#BaseBackend.get_user_permissions)[¶](#django.contrib.auth.backends.BaseBackend.get_user_permissions)

Returns an empty set.

    get_group_permissions(*user_obj*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#BaseBackend.get_group_permissions)[¶](#django.contrib.auth.backends.BaseBackend.get_group_permissions)

Returns an empty set.

    get_all_permissions(*user_obj*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#BaseBackend.get_all_permissions)[¶](#django.contrib.auth.backends.BaseBackend.get_all_permissions)

Uses [get_user_permissions()](#django.contrib.auth.backends.BaseBackend.get_user_permissions) and [get_group_permissions()](#django.contrib.auth.backends.BaseBackend.get_group_permissions) to
get the set of permission strings the `user_obj` has.

    has_perm(*user_obj*, *perm*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#BaseBackend.has_perm)[¶](#django.contrib.auth.backends.BaseBackend.has_perm)

Uses [get_all_permissions()](#django.contrib.auth.backends.BaseBackend.get_all_permissions) to check if `user_obj` has the
permission string `perm`.

     *class*ModelBackend[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend)[¶](#django.contrib.auth.backends.ModelBackend)

This is the default authentication backend used by Django.  It
authenticates using credentials consisting of a user identifier and
password.  For Django’s default user model, the user identifier is the
username, for custom user models it is the field specified by
USERNAME_FIELD (see [Customizing Users and authentication](https://docs.djangoproject.com/en/topics/auth/customizing/)).

It also handles the default permissions model as defined for
[User](#django.contrib.auth.models.User) and
[PermissionsMixin](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin).

[has_perm()](#django.contrib.auth.backends.ModelBackend.has_perm), [get_all_permissions()](#django.contrib.auth.backends.ModelBackend.get_all_permissions), [get_user_permissions()](#django.contrib.auth.backends.ModelBackend.get_user_permissions),
and [get_group_permissions()](#django.contrib.auth.backends.ModelBackend.get_group_permissions) allow an object to be passed as a
parameter for object-specific permissions, but this backend does not
implement them other than returning an empty set of permissions if
`obj is not None`.

[with_perm()](#django.contrib.auth.backends.ModelBackend.with_perm) also allows an object to be passed as a parameter, but
unlike others methods it returns an empty queryset if `obj is not None`.

   authenticate(*request*, *username=None*, *password=None*, ***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.authenticate)[¶](#django.contrib.auth.backends.ModelBackend.authenticate)

Tries to authenticate `username` with `password` by calling
[User.check_password](#django.contrib.auth.models.User.check_password). If no `username`
is provided, it tries to fetch a username from `kwargs` using the
key [CustomUser.USERNAME_FIELD](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD). Returns an
authenticated user or `None`.

`request` is an [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) and may be `None`
if it wasn’t provided to [authenticate()](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.authenticate)
(which passes it on to the backend).

    get_user_permissions(*user_obj*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.get_user_permissions)[¶](#django.contrib.auth.backends.ModelBackend.get_user_permissions)

Returns the set of permission strings the `user_obj` has from their
own user permissions. Returns an empty set if
[is_anonymous](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.is_anonymous) or
[is_active](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active) is `False`.

    get_group_permissions(*user_obj*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.get_group_permissions)[¶](#django.contrib.auth.backends.ModelBackend.get_group_permissions)

Returns the set of permission strings the `user_obj` has from the
permissions of the groups they belong. Returns an empty set if
[is_anonymous](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.is_anonymous) or
[is_active](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active)  is `False`.

    get_all_permissions(*user_obj*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.get_all_permissions)[¶](#django.contrib.auth.backends.ModelBackend.get_all_permissions)

Returns the set of permission strings the `user_obj` has, including both
user permissions and group permissions. Returns an empty set if
[is_anonymous](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.is_anonymous) or
[is_active](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active) is `False`.

    has_perm(*user_obj*, *perm*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.has_perm)[¶](#django.contrib.auth.backends.ModelBackend.has_perm)

Uses [get_all_permissions()](#django.contrib.auth.backends.ModelBackend.get_all_permissions) to check if `user_obj` has the
permission string `perm`. Returns `False` if the user is not
[is_active](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active).

    has_module_perms(*user_obj*, *app_label*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.has_module_perms)[¶](#django.contrib.auth.backends.ModelBackend.has_module_perms)

Returns whether the `user_obj` has any permissions on the app
`app_label`.

    user_can_authenticate()[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.user_can_authenticate)[¶](#django.contrib.auth.backends.ModelBackend.user_can_authenticate)

Returns whether the user is allowed to authenticate. To match the
behavior of [AuthenticationForm](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm)
which [prohibitsinactiveusersfromloggingin](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm.confirm_login_allowed),
this method returns `False` for users with [is_active=False](#django.contrib.auth.models.User.is_active). Custom user models that
don’t have an [is_active](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active)
field are allowed.

    with_perm(*perm*, *is_active=True*, *include_superusers=True*, *obj=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#ModelBackend.with_perm)[¶](#django.contrib.auth.backends.ModelBackend.with_perm)

Returns all active users who have the permission `perm` either in
the form of `"<app label>.<permission codename>"` or a
[Permission](#django.contrib.auth.models.Permission) instance. Returns an
empty queryset if no users who have the `perm` found.

If `is_active` is `True` (default), returns only active users, or
if `False`, returns only inactive users. Use `None` to return all
users irrespective of active state.

If `include_superusers` is `True` (default), the result will
include superusers.

     *class*AllowAllUsersModelBackend[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#AllowAllUsersModelBackend)[¶](#django.contrib.auth.backends.AllowAllUsersModelBackend)

Same as [ModelBackend](#django.contrib.auth.backends.ModelBackend) except that it doesn’t reject inactive users
because [user_can_authenticate()](#django.contrib.auth.backends.ModelBackend.user_can_authenticate) always returns `True`.

When using this backend, you’ll likely want to customize the
[AuthenticationForm](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm) used by the
[LoginView](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.views.LoginView) by overriding the
[confirm_login_allowed()](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.forms.AuthenticationForm.confirm_login_allowed)
method as it rejects inactive users.

    *class*RemoteUserBackend[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#RemoteUserBackend)[¶](#django.contrib.auth.backends.RemoteUserBackend)

Use this backend to take advantage of external-to-Django-handled
authentication.  It authenticates using usernames passed in
[request.META['REMOTE_USER']](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest.META).  See
the [Authenticating against REMOTE_USER](https://docs.djangoproject.com/en/howto/auth-remote-user/)
documentation.

If you need more control, you can create your own authentication backend
that inherits from this class and override these attributes or methods:

   create_unknown_user[¶](#django.contrib.auth.backends.RemoteUserBackend.create_unknown_user)

`True` or `False`. Determines whether or not a user object is
created if not already in the database  Defaults to `True`.

    authenticate(*request*, *remote_user*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#RemoteUserBackend.authenticate)[¶](#django.contrib.auth.backends.RemoteUserBackend.authenticate)

The username passed as `remote_user` is considered trusted. This
method returns the user object with the given username, creating a new
user object if [create_unknown_user](#django.contrib.auth.backends.RemoteUserBackend.create_unknown_user) is
`True`.

Returns `None` if [create_unknown_user](#django.contrib.auth.backends.RemoteUserBackend.create_unknown_user) is
`False` and a `User` object with the given username is not found in
the database.

`request` is an [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) and may be `None`
if it wasn’t provided to [authenticate()](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.authenticate)
(which passes it on to the backend).

    clean_username(*username*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#RemoteUserBackend.clean_username)[¶](#django.contrib.auth.backends.RemoteUserBackend.clean_username)

Performs any cleaning on the `username` (e.g. stripping LDAP DN
information) prior to using it to get or create a user object. Returns
the cleaned username.

    configure_user(*request*, *user*, *created=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#RemoteUserBackend.configure_user)[¶](#django.contrib.auth.backends.RemoteUserBackend.configure_user)

Configures the user on each authentication attempt. This method is
called immediately after fetching or creating the user being
authenticated, and can be used to perform custom setup actions, such as
setting the user’s groups based on attributes in an LDAP directory.
Returns the user object.

The setup can be performed either once when the user is created
(`created` is `True`) or on existing users (`created` is
`False`) as a way of synchronizing attributes between the remote and
the local systems.

`request` is an [HttpRequest](https://docs.djangoproject.com/en/5.0/request-response/#django.http.HttpRequest) and may be `None`
if it wasn’t provided to [authenticate()](https://docs.djangoproject.com/en/topics/auth/default/#django.contrib.auth.authenticate)
(which passes it on to the backend).

    user_can_authenticate()[¶](#django.contrib.auth.backends.RemoteUserBackend.user_can_authenticate)

Returns whether the user is allowed to authenticate. This method
returns `False` for users with [is_active=False](#django.contrib.auth.models.User.is_active). Custom user models that
don’t have an [is_active](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active)
field are allowed.

     *class*AllowAllUsersRemoteUserBackend[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/backends/#AllowAllUsersRemoteUserBackend)[¶](#django.contrib.auth.backends.AllowAllUsersRemoteUserBackend)

Same as [RemoteUserBackend](#django.contrib.auth.backends.RemoteUserBackend) except that it doesn’t reject inactive
users because [user_can_authenticate](#django.contrib.auth.backends.RemoteUserBackend.user_can_authenticate) always
returns `True`.

## Utility functions¶

   get_user(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/#get_user)[¶](#django.contrib.auth.get_user)    aget_user(*request*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/auth/#aget_user)[¶](#django.contrib.auth.aget_user)

*Asynchronous version*: `aget_user()`

Returns the user model instance associated with the given `request`’s
session.

It checks if the authentication backend stored in the session is present in
[AUTHENTICATION_BACKENDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTHENTICATION_BACKENDS). If so, it uses the backend’s
`get_user()` method to retrieve the user model instance and then verifies
the session by calling the user model’s
[get_session_auth_hash()](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash)
method. If the verification fails and [SECRET_KEY_FALLBACKS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECRET_KEY_FALLBACKS) are
provided, it verifies the session against each fallback key using
[get_session_auth_fallback_hash()](https://docs.djangoproject.com/en/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_session_auth_fallback_hash).

Returns an instance of [AnonymousUser](#django.contrib.auth.models.AnonymousUser)
if the authentication backend stored in the session is no longer in
[AUTHENTICATION_BACKENDS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-AUTHENTICATION_BACKENDS), if a user isn’t returned by the
backend’s `get_user()` method, or if the session auth hash doesn’t
validate.

  Changed in Django 4.1.8:

Fallback verification with [SECRET_KEY_FALLBACKS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-SECRET_KEY_FALLBACKS) was added.

   Changed in Django 5.0:

`aget_user()` function was added.

---

# The contenttypes framework¶

# The contenttypes framework¶

Django includes a [contenttypes](#module-django.contrib.contenttypes) application that can
track all of the models installed in your Django-powered project, providing a
high-level, generic interface for working with your models.

## Overview¶

At the heart of the contenttypes application is the
[ContentType](#django.contrib.contenttypes.models.ContentType) model, which lives at
`django.contrib.contenttypes.models.ContentType`. Instances of
[ContentType](#django.contrib.contenttypes.models.ContentType) represent and store
information about the models installed in your project, and new instances of
[ContentType](#django.contrib.contenttypes.models.ContentType) are automatically
created whenever new models are installed.

Instances of [ContentType](#django.contrib.contenttypes.models.ContentType) have
methods for returning the model classes they represent and for querying objects
from those models. [ContentType](#django.contrib.contenttypes.models.ContentType)
also has a [custom manager](https://docs.djangoproject.com/en/topics/db/managers/#custom-managers) that adds methods for
working with [ContentType](#django.contrib.contenttypes.models.ContentType) and for
obtaining instances of [ContentType](#django.contrib.contenttypes.models.ContentType)
for a particular model.

Relations between your models and
[ContentType](#django.contrib.contenttypes.models.ContentType) can also be used to
enable “generic” relationships between an instance of one of your
models and instances of any model you have installed.

## Installing the contenttypes framework¶

The contenttypes framework is included in the default
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) list created by `django-admin startproject`,
but if you’ve removed it or if you manually set up your
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) list, you can enable it by adding
`'django.contrib.contenttypes'` to your [INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting.

It’s generally a good idea to have the contenttypes framework
installed; several of Django’s other bundled applications require it:

- The admin application uses it to log the history of each object
  added or changed through the admin interface.
- Django’s [authenticationframework](https://docs.djangoproject.com/en/topics/auth/#module-django.contrib.auth) uses it
  to tie user permissions to specific models.

## TheContentTypemodel¶

   *class*ContentType[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentType)[¶](#django.contrib.contenttypes.models.ContentType)

Each instance of [ContentType](#django.contrib.contenttypes.models.ContentType)
has two fields which, taken together, uniquely describe an installed
model:

   app_label[¶](#django.contrib.contenttypes.models.ContentType.app_label)

The name of the application the model is part of. This is taken from
the [app_label](#django.contrib.contenttypes.models.ContentType.app_label) attribute of the model, and includes only the
*last* part of the application’s Python import path;
`django.contrib.contenttypes`, for example, becomes an
[app_label](#django.contrib.contenttypes.models.ContentType.app_label) of `contenttypes`.

    model[¶](#django.contrib.contenttypes.models.ContentType.model)

The name of the model class.

Additionally, the following property is available:

   name[¶](#django.contrib.contenttypes.models.ContentType.name)

The human-readable name of the content type. This is taken from the
[verbose_name](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.verbose_name)
attribute of the model.

Let’s look at an example to see how this works. If you already have
the [contenttypes](#module-django.contrib.contenttypes) application installed, and then add
[thesitesapplication](https://docs.djangoproject.com/en/5.0/ref/sites/#module-django.contrib.sites) to your
[INSTALLED_APPS](https://docs.djangoproject.com/en/5.0/settings/#std-setting-INSTALLED_APPS) setting and run `manage.py migrate` to install it,
the model [django.contrib.sites.models.Site](https://docs.djangoproject.com/en/5.0/ref/sites/#django.contrib.sites.models.Site) will be installed into
your database. Along with it a new instance of
[ContentType](#django.contrib.contenttypes.models.ContentType) will be
created with the following values:

- [app_label](#django.contrib.contenttypes.models.ContentType.app_label)
  will be set to `'sites'` (the last part of the Python
  path `django.contrib.sites`).
- [model](#django.contrib.contenttypes.models.ContentType.model)
  will be set to `'site'`.

## Methods onContentTypeinstances¶

Each [ContentType](#django.contrib.contenttypes.models.ContentType) instance has
methods that allow you to get from a
[ContentType](#django.contrib.contenttypes.models.ContentType) instance to the
model it represents, or to retrieve objects from that model:

   ContentType.get_object_for_this_type(***kwargs*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentType.get_object_for_this_type)[¶](#django.contrib.contenttypes.models.ContentType.get_object_for_this_type)

Takes a set of valid [lookup arguments](https://docs.djangoproject.com/en/topics/db/queries/#field-lookups-intro) for the
model the [ContentType](#django.contrib.contenttypes.models.ContentType)
represents, and does
[aget()lookup](https://docs.djangoproject.com/en/5.0/models/querysets/#django.db.models.query.QuerySet.get)
on that model, returning the corresponding object.

    ContentType.model_class()[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentType.model_class)[¶](#django.contrib.contenttypes.models.ContentType.model_class)

Returns the model class represented by this
[ContentType](#django.contrib.contenttypes.models.ContentType) instance.

For example, we could look up the
[ContentType](#django.contrib.contenttypes.models.ContentType) for the
[User](https://docs.djangoproject.com/en/5.0/ref/auth/#django.contrib.auth.models.User) model:

```
>>> from django.contrib.contenttypes.models import ContentType
>>> user_type = ContentType.objects.get(app_label="auth", model="user")
>>> user_type
<ContentType: user>
```

And then use it to query for a particular
[User](https://docs.djangoproject.com/en/5.0/ref/auth/#django.contrib.auth.models.User), or to get access
to the `User` model class:

```
>>> user_type.model_class()
<class 'django.contrib.auth.models.User'>
>>> user_type.get_object_for_this_type(username="Guido")
<User: Guido>
```

Together,
[get_object_for_this_type()](#django.contrib.contenttypes.models.ContentType.get_object_for_this_type)
and [model_class()](#django.contrib.contenttypes.models.ContentType.model_class) enable
two extremely important use cases:

1. Using these methods, you can write high-level generic code that
  performs queries on any installed model – instead of importing and
  using a single specific model class, you can pass an `app_label` and
  `model` into a
  [ContentType](#django.contrib.contenttypes.models.ContentType) lookup at
  runtime, and then work with the model class or retrieve objects from it.
2. You can relate another model to
  [ContentType](#django.contrib.contenttypes.models.ContentType) as a way of
  tying instances of it to particular model classes, and use these methods
  to get access to those model classes.

Several of Django’s bundled applications make use of the latter technique.
For example,
[thepermissionssystem](https://docs.djangoproject.com/en/5.0/ref/auth/#django.contrib.auth.models.Permission) in
Django’s authentication framework uses a
[Permission](https://docs.djangoproject.com/en/5.0/ref/auth/#django.contrib.auth.models.Permission) model with a foreign
key to [ContentType](#django.contrib.contenttypes.models.ContentType); this lets
[Permission](https://docs.djangoproject.com/en/5.0/ref/auth/#django.contrib.auth.models.Permission) represent concepts like
“can add blog entry” or “can delete news story”.

### TheContentTypeManager¶

   *class*ContentTypeManager[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentTypeManager)[¶](#django.contrib.contenttypes.models.ContentTypeManager)

[ContentType](#django.contrib.contenttypes.models.ContentType) also has a custom
manager, [ContentTypeManager](#django.contrib.contenttypes.models.ContentTypeManager),
which adds the following methods:

   clear_cache()[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentTypeManager.clear_cache)[¶](#django.contrib.contenttypes.models.ContentTypeManager.clear_cache)

Clears an internal cache used by
[ContentType](#django.contrib.contenttypes.models.ContentType) to keep track
of models for which it has created
[ContentType](#django.contrib.contenttypes.models.ContentType) instances. You
probably won’t ever need to call this method yourself; Django will call
it automatically when it’s needed.

    get_for_id(*id*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentTypeManager.get_for_id)[¶](#django.contrib.contenttypes.models.ContentTypeManager.get_for_id)

Lookup a [ContentType](#django.contrib.contenttypes.models.ContentType) by ID.
Since this method uses the same shared cache as
[get_for_model()](#django.contrib.contenttypes.models.ContentTypeManager.get_for_model),
it’s preferred to use this method over the usual
`ContentType.objects.get(pk=id)`

    get_for_model(*model*, *for_concrete_model=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentTypeManager.get_for_model)[¶](#django.contrib.contenttypes.models.ContentTypeManager.get_for_model)

Takes either a model class or an instance of a model, and returns the
[ContentType](#django.contrib.contenttypes.models.ContentType) instance
representing that model. `for_concrete_model=False` allows fetching
the [ContentType](#django.contrib.contenttypes.models.ContentType) of a proxy
model.

    get_for_models(**models*, *for_concrete_models=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentTypeManager.get_for_models)[¶](#django.contrib.contenttypes.models.ContentTypeManager.get_for_models)

Takes a variadic number of model classes, and returns a dictionary
mapping the model classes to the
[ContentType](#django.contrib.contenttypes.models.ContentType) instances
representing them. `for_concrete_models=False` allows fetching the
[ContentType](#django.contrib.contenttypes.models.ContentType) of proxy
models.

    get_by_natural_key(*app_label*, *model*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/models/#ContentTypeManager.get_by_natural_key)[¶](#django.contrib.contenttypes.models.ContentTypeManager.get_by_natural_key)

Returns the [ContentType](#django.contrib.contenttypes.models.ContentType)
instance uniquely identified by the given application label and model
name. The primary purpose of this method is to allow
[ContentType](#django.contrib.contenttypes.models.ContentType) objects to be
referenced via a [natural key](https://docs.djangoproject.com/en/topics/serialization/#topics-serialization-natural-keys)
during deserialization.

The [get_for_model()](#django.contrib.contenttypes.models.ContentTypeManager.get_for_model) method is especially
useful when you know you need to work with a
[ContentType](#django.contrib.contenttypes.models.ContentType) but don’t
want to go to the trouble of obtaining the model’s metadata to perform a manual
lookup:

```
>>> from django.contrib.auth.models import User
>>> ContentType.objects.get_for_model(User)
<ContentType: user>
```

## Generic relations¶

Adding a foreign key from one of your own models to
[ContentType](#django.contrib.contenttypes.models.ContentType) allows your model to
effectively tie itself to another model class, as in the example of the
[Permission](https://docs.djangoproject.com/en/5.0/ref/auth/#django.contrib.auth.models.Permission) model above. But it’s possible
to go one step further and use
[ContentType](#django.contrib.contenttypes.models.ContentType) to enable truly
generic (sometimes called “polymorphic”) relationships between models.

For example, it could be used for a tagging system like so:

```
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.tag

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
```

A normal [ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey) can only “point
to” one other model, which means that if the `TaggedItem` model used a
[ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey) it would have to
choose one and only one model to store tags for. The contenttypes
application provides a special field type (`GenericForeignKey`) which
works around this and allows the relationship to be with any
model:

   *class*GenericForeignKey[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/fields/#GenericForeignKey)[¶](#django.contrib.contenttypes.fields.GenericForeignKey)

There are three parts to setting up a
[GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey):

1. Give your model a [ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey)
  to [ContentType](#django.contrib.contenttypes.models.ContentType). The usual
  name for this field is “content_type”.
2. Give your model a field that can store primary key values from the
  models you’ll be relating to. For most models, this means a
  [PositiveIntegerField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.PositiveIntegerField). The usual name
  for this field is “object_id”.
3. Give your model a
  [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey), and
  pass it the names of the two fields described above. If these fields
  are named “content_type” and “object_id”, you can omit this – those
  are the default field names
  [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey) will
  look for.

Unlike for the [ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey), a database index is
*not* automatically created on the
[GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey), so it’s
recommended that you use
[Meta.indexes](https://docs.djangoproject.com/en/5.0/models/options/#django.db.models.Options.indexes) to add your own
multiple column index. This behavior [may change](https://code.djangoproject.com/ticket/23435) in the
future.

   for_concrete_model[¶](#django.contrib.contenttypes.fields.GenericForeignKey.for_concrete_model)

If `False`, the field will be able to reference proxy models. Default
is `True`. This mirrors the `for_concrete_model` argument to
[get_for_model()](#django.contrib.contenttypes.models.ContentTypeManager.get_for_model).

Primary key type compatibility

The “object_id” field doesn’t have to be the same type as the
primary key fields on the related models, but their primary key values
must be coercible to the same type as the “object_id” field by its
[get_db_prep_value()](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.get_db_prep_value) method.

For example, if you want to allow generic relations to models with either
[IntegerField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.IntegerField) or
[CharField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.CharField) primary key fields, you
can use [CharField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.CharField) for the
“object_id” field on your model since integers can be coerced to
strings by [get_db_prep_value()](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.Field.get_db_prep_value).

For maximum flexibility you can use a
[TextField](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.TextField) which doesn’t have a
maximum length defined, however this may incur significant performance
penalties depending on your database backend.

There is no one-size-fits-all solution for which field type is best. You
should evaluate the models you expect to be pointing to and determine
which solution will be most effective for your use case.

Serializing references to `ContentType` objects

If you’re serializing data (for example, when generating
[fixtures](https://docs.djangoproject.com/en/topics/testing/tools/#django.test.TransactionTestCase.fixtures)) from a model that implements
generic relations, you should probably be using a natural key to uniquely
identify related [ContentType](#django.contrib.contenttypes.models.ContentType)
objects. See [natural keys](https://docs.djangoproject.com/en/topics/serialization/#topics-serialization-natural-keys) and
[dumpdata--natural-foreign](https://docs.djangoproject.com/en/5.0/django-admin/#cmdoption-dumpdata-natural-foreign) for more information.

This will enable an API similar to the one used for a normal
[ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey);
each `TaggedItem` will have a `content_object` field that returns the
object it’s related to, and you can also assign to that field or use it when
creating a `TaggedItem`:

```
>>> from django.contrib.auth.models import User
>>> guido = User.objects.get(username="Guido")
>>> t = TaggedItem(content_object=guido, tag="bdfl")
>>> t.save()
>>> t.content_object
<User: Guido>
```

If the related object is deleted, the `content_type` and `object_id` fields
remain set to their original values and the `GenericForeignKey` returns
`None`:

```
>>> guido.delete()
>>> t.content_object  # returns None
```

Due to the way [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey)
is implemented, you cannot use such fields directly with filters (`filter()`
and `exclude()`, for example) via the database API. Because a
[GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey) isn’t a
normal field object, these examples will *not* work:

```
# This will fail
>>> TaggedItem.objects.filter(content_object=guido)
# This will also fail
>>> TaggedItem.objects.get(content_object=guido)
```

Likewise, [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey)s
does not appear in [ModelForm](https://docs.djangoproject.com/en/topics/forms/modelforms/#django.forms.ModelForm)s.

### Reverse generic relations¶

   *class*GenericRelation[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/fields/#GenericRelation)[¶](#django.contrib.contenttypes.fields.GenericRelation)   related_query_name[¶](#django.contrib.contenttypes.fields.GenericRelation.related_query_name)

The relation on the related object back to this object doesn’t exist by
default. Setting `related_query_name` creates a relation from the
related object back to this one. This allows querying and filtering
from the related object.

If you know which models you’ll be using most often, you can also add
a “reverse” generic relationship to enable an additional API. For example:

```
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

class Bookmark(models.Model):
    url = models.URLField()
    tags = GenericRelation(TaggedItem)
```

`Bookmark` instances will each have a `tags` attribute, which can
be used to retrieve their associated `TaggedItems`:

```
>>> b = Bookmark(url="https://www.djangoproject.com/")
>>> b.save()
>>> t1 = TaggedItem(content_object=b, tag="django")
>>> t1.save()
>>> t2 = TaggedItem(content_object=b, tag="python")
>>> t2.save()
>>> b.tags.all()
<QuerySet [<TaggedItem: django>, <TaggedItem: python>]>
```

You can also use `add()`, `create()`, or `set()` to create
relationships:

```
>>> t3 = TaggedItem(tag="Web development")
>>> b.tags.add(t3, bulk=False)
>>> b.tags.create(tag="Web framework")
<TaggedItem: Web framework>
>>> b.tags.all()
<QuerySet [<TaggedItem: django>, <TaggedItem: python>, <TaggedItem: Web development>, <TaggedItem: Web framework>]>
>>> b.tags.set([t1, t3])
>>> b.tags.all()
<QuerySet [<TaggedItem: django>, <TaggedItem: Web development>]>
```

The `remove()` call will bulk delete the specified model objects:

```
>>> b.tags.remove(t3)
>>> b.tags.all()
<QuerySet [<TaggedItem: django>]>
>>> TaggedItem.objects.all()
<QuerySet [<TaggedItem: django>]>
```

The `clear()` method can be used to bulk delete all related objects for an
instance:

```
>>> b.tags.clear()
>>> b.tags.all()
<QuerySet []>
>>> TaggedItem.objects.all()
<QuerySet []>
```

Defining [GenericRelation](#django.contrib.contenttypes.fields.GenericRelation) with
`related_query_name` set allows querying from the related object:

```
tags = GenericRelation(TaggedItem, related_query_name="bookmark")
```

This enables filtering, ordering, and other query operations on `Bookmark`
from `TaggedItem`:

```
>>> # Get all tags belonging to bookmarks containing `django` in the url
>>> TaggedItem.objects.filter(bookmark__url__contains="django")
<QuerySet [<TaggedItem: django>, <TaggedItem: python>]>
```

If you don’t add the `related_query_name`, you can do the same types of
lookups manually:

```
>>> bookmarks = Bookmark.objects.filter(url__contains="django")
>>> bookmark_type = ContentType.objects.get_for_model(Bookmark)
>>> TaggedItem.objects.filter(content_type__pk=bookmark_type.id, object_id__in=bookmarks)
<QuerySet [<TaggedItem: django>, <TaggedItem: python>]>
```

Just as [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey)
accepts the names of the content-type and object-ID fields as
arguments, so too does
[GenericRelation](#django.contrib.contenttypes.fields.GenericRelation);
if the model which has the generic foreign key is using non-default names
for those fields, you must pass the names of the fields when setting up a
[GenericRelation](#django.contrib.contenttypes.fields.GenericRelation) to it. For example, if the `TaggedItem` model
referred to above used fields named `content_type_fk` and
`object_primary_key` to create its generic foreign key, then a
[GenericRelation](#django.contrib.contenttypes.fields.GenericRelation) back to it would need to be defined like so:

```
tags = GenericRelation(
    TaggedItem,
    content_type_field="content_type_fk",
    object_id_field="object_primary_key",
)
```

Note also, that if you delete an object that has a
[GenericRelation](#django.contrib.contenttypes.fields.GenericRelation), any objects
which have a [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey)
pointing at it will be deleted as well. In the example above, this means that
if a `Bookmark` object were deleted, any `TaggedItem` objects pointing at
it would be deleted at the same time.

Unlike [ForeignKey](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey),
[GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey) does not accept
an [on_delete](https://docs.djangoproject.com/en/5.0/models/fields/#django.db.models.ForeignKey.on_delete) argument to customize this
behavior; if desired, you can avoid the cascade-deletion by not using
[GenericRelation](#django.contrib.contenttypes.fields.GenericRelation), and alternate
behavior can be provided via the [pre_delete](https://docs.djangoproject.com/en/5.0/signals/#django.db.models.signals.pre_delete)
signal.

### Generic relations and aggregation¶

[Django’s database aggregation API](https://docs.djangoproject.com/en/topics/db/aggregation/) works with a
[GenericRelation](#django.contrib.contenttypes.fields.GenericRelation). For example, you
can find out how many tags all the bookmarks have:

```
>>> Bookmark.objects.aggregate(Count("tags"))
{'tags__count': 3}
```

### Generic relation in forms¶

The [django.contrib.contenttypes.forms](#module-django.contrib.contenttypes.forms) module provides:

- [BaseGenericInlineFormSet](#django.contrib.contenttypes.forms.BaseGenericInlineFormSet)
- A formset factory, [generic_inlineformset_factory()](#django.contrib.contenttypes.forms.generic_inlineformset_factory), for use with
  [GenericForeignKey](#django.contrib.contenttypes.fields.GenericForeignKey).

   *class*BaseGenericInlineFormSet[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/forms/#BaseGenericInlineFormSet)[¶](#django.contrib.contenttypes.forms.BaseGenericInlineFormSet)    generic_inlineformset_factory(*model*, *form=ModelForm*, *formset=BaseGenericInlineFormSet*, *ct_field='content_type'*, *fk_field='object_id'*, *fields=None*, *exclude=None*, *extra=3*, *can_order=False*, *can_delete=True*, *max_num=None*, *formfield_callback=None*, *validate_max=False*, *for_concrete_model=True*, *min_num=None*, *validate_min=False*, *absolute_max=None*, *can_delete_extra=True*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/forms/#generic_inlineformset_factory)[¶](#django.contrib.contenttypes.forms.generic_inlineformset_factory)

Returns a `GenericInlineFormSet` using
[modelformset_factory()](https://docs.djangoproject.com/en/5.0/forms/models/#django.forms.models.modelformset_factory).

You must provide `ct_field` and `fk_field` if they are different from
the defaults, `content_type` and `object_id` respectively. Other
parameters are similar to those documented in
[modelformset_factory()](https://docs.djangoproject.com/en/5.0/forms/models/#django.forms.models.modelformset_factory) and
[inlineformset_factory()](https://docs.djangoproject.com/en/5.0/forms/models/#django.forms.models.inlineformset_factory).

The `for_concrete_model` argument corresponds to the
[for_concrete_model](#django.contrib.contenttypes.fields.GenericForeignKey.for_concrete_model)
argument on `GenericForeignKey`.

### Generic relations in admin¶

The [django.contrib.contenttypes.admin](#module-django.contrib.contenttypes.admin) module provides
[GenericTabularInline](#django.contrib.contenttypes.admin.GenericTabularInline) and
[GenericStackedInline](#django.contrib.contenttypes.admin.GenericStackedInline) (subclasses of
[GenericInlineModelAdmin](#django.contrib.contenttypes.admin.GenericInlineModelAdmin))

These classes and functions enable the use of generic relations in forms
and the admin. See the [model formset](https://docs.djangoproject.com/en/topics/forms/modelforms/) and
[admin](https://docs.djangoproject.com/en/5.0/ref/admin/#using-generic-relations-as-an-inline) documentation for more
information.

   *class*GenericInlineModelAdmin[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/admin/#GenericInlineModelAdmin)[¶](#django.contrib.contenttypes.admin.GenericInlineModelAdmin)

The [GenericInlineModelAdmin](#django.contrib.contenttypes.admin.GenericInlineModelAdmin)
class inherits all properties from an
[InlineModelAdmin](https://docs.djangoproject.com/en/5.0/ref/admin/#django.contrib.admin.InlineModelAdmin) class. However,
it adds a couple of its own for working with the generic relation:

   ct_field[¶](#django.contrib.contenttypes.admin.GenericInlineModelAdmin.ct_field)

The name of the
[ContentType](#django.contrib.contenttypes.models.ContentType) foreign key
field on the model. Defaults to `content_type`.

    ct_fk_field[¶](#django.contrib.contenttypes.admin.GenericInlineModelAdmin.ct_fk_field)

The name of the integer field that represents the ID of the related
object. Defaults to `object_id`.

     *class*GenericTabularInline[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/admin/#GenericTabularInline)[¶](#django.contrib.contenttypes.admin.GenericTabularInline)    *class*GenericStackedInline[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/admin/#GenericStackedInline)[¶](#django.contrib.contenttypes.admin.GenericStackedInline)

Subclasses of [GenericInlineModelAdmin](#django.contrib.contenttypes.admin.GenericInlineModelAdmin) with stacked and tabular
layouts, respectively.

### GenericPrefetch()¶

  New in Django 5.0.    *class*GenericPrefetch(*lookup*, *querysets*, *to_attr=None*)[[source]](https://docs.djangoproject.com/en/_modules/django/contrib/contenttypes/prefetch/#GenericPrefetch)[¶](#django.contrib.contenttypes.prefetch.GenericPrefetch)

This lookup is similar to `Prefetch()` and it should only be used on
`GenericForeignKey`. The `querysets` argument accepts a list of querysets,
each for a different `ContentType`. This is useful for `GenericForeignKey`
with non-homogeneous set of results.

```
>>> from django.contrib.contenttypes.prefetch import GenericPrefetch
>>> bookmark = Bookmark.objects.create(url="https://www.djangoproject.com/")
>>> animal = Animal.objects.create(name="lion", weight=100)
>>> TaggedItem.objects.create(tag="great", content_object=bookmark)
>>> TaggedItem.objects.create(tag="awesome", content_object=animal)
>>> prefetch = GenericPrefetch(
...     "content_object", [Bookmark.objects.all(), Animal.objects.only("name")]
... )
>>> TaggedItem.objects.prefetch_related(prefetch).all()
<QuerySet [<TaggedItem: Great>, <TaggedItem: Awesome>]>
```
