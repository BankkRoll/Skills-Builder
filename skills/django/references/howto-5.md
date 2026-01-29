# How to create PDF files¶ and more

# How to create PDF files¶

# How to create PDF files¶

This document explains how to output PDF files dynamically using Django views.
This is made possible by the excellent, open-source [ReportLab](https://docs.reportlab.com/) Python PDF
library.

The advantage of generating PDF files dynamically is that you can create
customized PDFs for different purposes – say, for different users or different
pieces of content.

For example, Django was used at [kusports.com](http://www2.kusports.com/) to generate customized,
printer-friendly NCAA tournament brackets, as PDF files, for people
participating in a March Madness contest.

## Install ReportLab¶

The ReportLab library is [available on PyPI](https://pypi.org/project/reportlab/). A [user guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
(not coincidentally, a PDF file) is also available for download.
You can install ReportLab with `pip`:

   /  

```
$ python -m pip install reportlab
```

```
...\> py -m pip install reportlab
```

Test your installation by importing it in the Python interactive interpreter:

```
>>> import reportlab
```

If that command doesn’t raise any errors, the installation worked.

## Write your view¶

The key to generating PDFs dynamically with Django is that the ReportLab API
acts on file-like objects, and Django’s [FileResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.FileResponse)
objects accept file-like objects.

Here’s a “Hello World” example:

```
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
```

The code and comments should be self-explanatory, but a few things deserve a
mention:

- The response will automatically set the MIME type *application/pdf*
  based on the filename extension. This tells browsers that the document is a
  PDF file, rather than an HTML file or a generic
  *application/octet-stream* binary content.
- When `as_attachment=True` is passed to `FileResponse`, it sets the
  appropriate `Content-Disposition` header and that tells web browsers to
  pop-up a dialog box prompting/confirming how to handle the document even if a
  default is set on the machine. If the `as_attachment` parameter is omitted,
  browsers will handle the PDF using whatever program/plugin they’ve been
  configured to use for PDFs.
- You can provide an arbitrary `filename` parameter. It’ll be used by browsers
  in the “Save as…” dialog.
- You can hook into the ReportLab API: The same buffer passed as the first
  argument to `canvas.Canvas` can be fed to the
  [FileResponse](https://docs.djangoproject.com/en/ref/request-response/#django.http.FileResponse) class.
- Note that all subsequent PDF-generation methods are called on the PDF
  object (in this case, `p`) – not on `buffer`.
- Finally, it’s important to call `showPage()` and `save()` on the PDF
  file.

Note

ReportLab is not thread-safe. Some of our users have reported odd issues
with building PDF-generating Django views that are accessed by many people
at the same time.

## Other formats¶

Notice that there isn’t a lot in these examples that’s PDF-specific – just the
bits using `reportlab`. You can use a similar technique to generate any
arbitrary format that you can find a Python library for. Also see
[How to create CSV output](https://docs.djangoproject.com/en/5.0/outputting-csv/) for another example and some techniques you can use
when generated text-based formats.

See also

Django Packages provides a [comparison of packages](https://djangopackages.org/grids/g/pdf/) that help generate PDF files
from Django.

---

# How to deploy static files¶

# How to deploy static files¶

See also

For an introduction to the use of [django.contrib.staticfiles](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#module-django.contrib.staticfiles), see
[How to manage static files (e.g. images, JavaScript, CSS)](https://docs.djangoproject.com/en/5.0/howto/).

## Serving static files in production¶

The basic outline of putting static files into production consists of two
steps: run the [collectstatic](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django-admin-collectstatic) command when static files change, then
arrange for the collected static files directory ([STATIC_ROOT](https://docs.djangoproject.com/en/ref/settings/#std-setting-STATIC_ROOT)) to be
moved to the static file server and served. Depending the `staticfiles` [STORAGES](https://docs.djangoproject.com/en/ref/settings/#std-setting-STORAGES) alias, files may need to be moved to a new location
manually or the [post_process](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django.contrib.staticfiles.storage.StaticFilesStorage.post_process) method of
the `Storage` class might take care of that.

As with all deployment tasks, the devil’s in the details. Every production
setup will be a bit different, so you’ll need to adapt the basic outline to fit
your needs. Below are a few common patterns that might help.

### Serving the site and your static files from the same server¶

If you want to serve your static files from the same server that’s already
serving your site, the process may look something like:

- Push your code up to the deployment server.
- On the server, run [collectstatic](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django-admin-collectstatic) to copy all the static files
  into [STATIC_ROOT](https://docs.djangoproject.com/en/ref/settings/#std-setting-STATIC_ROOT).
- Configure your web server to serve the files in [STATIC_ROOT](https://docs.djangoproject.com/en/ref/settings/#std-setting-STATIC_ROOT)
  under the URL [STATIC_URL](https://docs.djangoproject.com/en/ref/settings/#std-setting-STATIC_URL). For example, here’s
  [how to do this with Apache and mod_wsgi](https://docs.djangoproject.com/en/5.0/deployment/wsgi/modwsgi/#serving-files).

You’ll probably want to automate this process, especially if you’ve got
multiple web servers.

### Serving static files from a dedicated server¶

Most larger Django sites use a separate web server – i.e., one that’s not also
running Django – for serving static files. This server often runs a different
type of web server – faster but less full-featured. Some common choices are:

- [Nginx](https://nginx.org/en/)
- A stripped-down version of [Apache](https://httpd.apache.org/)

Configuring these servers is out of scope of this document; check each
server’s respective documentation for instructions.

Since your static file server won’t be running Django, you’ll need to modify
the deployment strategy to look something like:

- When your static files change, run [collectstatic](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django-admin-collectstatic) locally.
- Push your local [STATIC_ROOT](https://docs.djangoproject.com/en/ref/settings/#std-setting-STATIC_ROOT) up to the static file server into the
  directory that’s being served. [rsync](https://rsync.samba.org/) is a
  common choice for this step since it only needs to transfer the bits of
  static files that have changed.

### Serving static files from a cloud service or CDN¶

Another common tactic is to serve static files from a cloud storage provider
like Amazon’s S3 and/or a CDN (content delivery network). This lets you
ignore the problems of serving static files and can often make for
faster-loading web pages (especially when using a CDN).

When using these services, the basic workflow would look a bit like the above,
except that instead of using `rsync` to transfer your static files to the
server you’d need to transfer the static files to the storage provider or CDN.

There’s any number of ways you might do this, but if the provider has an API,
you can use a [custom file storage backend](https://docs.djangoproject.com/en/5.0/custom-file-storage/)
to integrate the CDN with your Django project. If you’ve written or are using a
3rd party custom storage backend, you can tell [collectstatic](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django-admin-collectstatic) to use
it by setting `staticfiles` in [STORAGES](https://docs.djangoproject.com/en/ref/settings/#std-setting-STORAGES).

For example, if you’ve written an S3 storage backend in
`myproject.storage.S3Storage` you could use it with:

```
STORAGES = {
    # ...
    "staticfiles": {"BACKEND": "myproject.storage.S3Storage"}
}
```

Once that’s done, all you have to do is run [collectstatic](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#django-admin-collectstatic) and your
static files would be pushed through your storage package up to S3. If you
later needed to switch to a different storage provider, you may only have to
change `staticfiles` in the [STORAGES](https://docs.djangoproject.com/en/ref/settings/#std-setting-STORAGES) setting.

For details on how you’d write one of these backends, see
[How to write a custom storage class](https://docs.djangoproject.com/en/5.0/custom-file-storage/). There are 3rd party apps available that
provide storage backends for many common file storage APIs. A good starting
point is the [overview at djangopackages.org](https://djangopackages.org/grids/g/storage-backends/).

  Changed in Django 4.2:

The [STORAGES](https://docs.djangoproject.com/en/ref/settings/#std-setting-STORAGES) setting was added.

## Learn more¶

For complete details on all the settings, commands, template tags, and other
pieces included in [django.contrib.staticfiles](https://docs.djangoproject.com/en/ref/contrib/staticfiles/#module-django.contrib.staticfiles), see [the
staticfiles reference](https://docs.djangoproject.com/en/ref/contrib/staticfiles/).

---

# How to create database migrations¶

# How to create database migrations¶

This document explains how to structure and write database migrations for
different scenarios you might encounter. For introductory material on
migrations, see [the topic guide](https://docs.djangoproject.com/en/topics/migrations/).

## Data migrations and multiple databases¶

When using multiple databases, you may need to figure out whether or not to
run a migration against a particular database. For example, you may want to
**only** run a migration on a particular database.

In order to do that you can check the database connection’s alias inside a
`RunPython` operation by looking at the `schema_editor.connection.alias`
attribute:

```
from django.db import migrations

def forwards(apps, schema_editor):
    if schema_editor.connection.alias != "default":
        return
    # Your migration code goes here

class Migration(migrations.Migration):
    dependencies = [
        # Dependencies to other migrations
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
```

You can also provide hints that will be passed to the [allow_migrate()](https://docs.djangoproject.com/en/topics/db/multi-db/#allow_migrate)
method of database routers as `**hints`:

  `myapp/dbrouters.py`[¶](#id4)

```
class MyRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if "target_db" in hints:
            return db == hints["target_db"]
        return True
```

Then, to leverage this in your migrations, do the following:

```
from django.db import migrations

def forwards(apps, schema_editor):
    # Your migration code goes here
    ...

class Migration(migrations.Migration):
    dependencies = [
        # Dependencies to other migrations
    ]

    operations = [
        migrations.RunPython(forwards, hints={"target_db": "default"}),
    ]
```

If your `RunPython` or `RunSQL` operation only affects one model, it’s good
practice to pass `model_name` as a hint to make it as transparent as possible
to the router. This is especially important for reusable and third-party apps.

## Migrations that add unique fields¶

Applying a “plain” migration that adds a unique non-nullable field to a table
with existing rows will raise an error because the value used to populate
existing rows is generated only once, thus breaking the unique constraint.

Therefore, the following steps should be taken. In this example, we’ll add a
non-nullable [UUIDField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.UUIDField) with a default value. Modify
the respective field according to your needs.

- Add the field on your model with `default=uuid.uuid4` and `unique=True`
  arguments (choose an appropriate default for the type of the field you’re
  adding).
- Run the [makemigrations](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-makemigrations) command. This should generate a migration
  with an `AddField` operation.
- Generate two empty migration files for the same app by running
  `makemigrations myapp --empty` twice. We’ve renamed the migration files to
  give them meaningful names in the examples below.
- Copy the `AddField` operation from the auto-generated migration (the first
  of the three new files) to the last migration, change `AddField` to
  `AlterField`, and add imports of `uuid` and `models`. For example:
    `0006_remove_uuid_null.py`[¶](#id5)
  ```
  # Generated by Django A.B on YYYY-MM-DD HH:MM
  from django.db import migrations, models
  import uuid
  class Migration(migrations.Migration):
      dependencies = [
          ("myapp", "0005_populate_uuid_values"),
      ]
      operations = [
          migrations.AlterField(
              model_name="mymodel",
              name="uuid",
              field=models.UUIDField(default=uuid.uuid4, unique=True),
          ),
      ]
  ```
- Edit the first migration file. The generated migration class should look
  similar to this:
    `0004_add_uuid_field.py`[¶](#id6)
  ```
  class Migration(migrations.Migration):
      dependencies = [
          ("myapp", "0003_auto_20150129_1705"),
      ]
      operations = [
          migrations.AddField(
              model_name="mymodel",
              name="uuid",
              field=models.UUIDField(default=uuid.uuid4, unique=True),
          ),
      ]
  ```
  Change `unique=True` to `null=True` – this will create the intermediary
  null field and defer creating the unique constraint until we’ve populated
  unique values on all the rows.
- In the first empty migration file, add a
  [RunPython](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.RunPython) or
  [RunSQL](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.RunSQL) operation to generate a
  unique value (UUID in the example) for each existing row. Also add an import
  of `uuid`. For example:
    `0005_populate_uuid_values.py`[¶](#id7)
  ```
  # Generated by Django A.B on YYYY-MM-DD HH:MM
  from django.db import migrations
  import uuid
  def gen_uuid(apps, schema_editor):
      MyModel = apps.get_model("myapp", "MyModel")
      for row in MyModel.objects.all():
          row.uuid = uuid.uuid4()
          row.save(update_fields=["uuid"])
  class Migration(migrations.Migration):
      dependencies = [
          ("myapp", "0004_add_uuid_field"),
      ]
      operations = [
          # omit reverse_code=... if you don't want the migration to be reversible.
          migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
      ]
  ```
- Now you can apply the migrations as usual with the [migrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-migrate) command.
  Note there is a race condition if you allow objects to be created while this
  migration is running. Objects created after the `AddField` and before
  `RunPython` will have their original `uuid`’s overwritten.

### Non-atomic migrations¶

On databases that support DDL transactions (SQLite and PostgreSQL), migrations
will run inside a transaction by default. For use cases such as performing data
migrations on large tables, you may want to prevent a migration from running in
a transaction by setting the `atomic` attribute to `False`:

```
from django.db import migrations

class Migration(migrations.Migration):
    atomic = False
```

Within such a migration, all operations are run without a transaction. It’s
possible to execute parts of the migration inside a transaction using
[atomic()](https://docs.djangoproject.com/en/topics/db/transactions/#django.db.transaction.atomic) or by passing `atomic=True` to
`RunPython`.

Here’s an example of a non-atomic data migration that updates a large table in
smaller batches:

```
import uuid

from django.db import migrations, transaction

def gen_uuid(apps, schema_editor):
    MyModel = apps.get_model("myapp", "MyModel")
    while MyModel.objects.filter(uuid__isnull=True).exists():
        with transaction.atomic():
            for row in MyModel.objects.filter(uuid__isnull=True)[:1000]:
                row.uuid = uuid.uuid4()
                row.save()

class Migration(migrations.Migration):
    atomic = False

    operations = [
        migrations.RunPython(gen_uuid),
    ]
```

The `atomic` attribute doesn’t have an effect on databases that don’t support
DDL transactions (e.g. MySQL, Oracle). (MySQL’s [atomic DDL statement support](https://dev.mysql.com/doc/refman/en/atomic-ddl.html) refers to individual
statements rather than multiple statements wrapped in a transaction that can be
rolled back.)

## Controlling the order of migrations¶

Django determines the order in which migrations should be applied not by the
filename of each migration, but by building a graph using two properties on the
`Migration` class: `dependencies` and `run_before`.

If you’ve used the [makemigrations](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-makemigrations) command you’ve probably
already seen `dependencies` in action because auto-created
migrations have this defined as part of their creation process.

The `dependencies` property is declared like this:

```
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0123_the_previous_migration"),
    ]
```

Usually this will be enough, but from time to time you may need to
ensure that your migration runs *before* other migrations. This is
useful, for example, to make third-party apps’ migrations run *after*
your [AUTH_USER_MODEL](https://docs.djangoproject.com/en/ref/settings/#std-setting-AUTH_USER_MODEL) replacement.

To achieve this, place all migrations that should depend on yours in
the `run_before` attribute on your `Migration` class:

```
class Migration(migrations.Migration):
    ...

    run_before = [
        ("third_party_app", "0001_do_awesome"),
    ]
```

Prefer using `dependencies` over `run_before` when possible. You should
only use `run_before` if it is undesirable or impractical to specify
`dependencies` in the migration which you want to run after the one you are
writing.

## Migrating data between third-party apps¶

You can use a data migration to move data from one third-party application to
another.

If you plan to remove the old app later, you’ll need to set the `dependencies`
property based on whether or not the old app is installed. Otherwise, you’ll
have missing dependencies once you uninstall the old app. Similarly, you’ll
need to catch [LookupError](https://docs.python.org/3/library/exceptions.html#LookupError) in the `apps.get_model()` call that
retrieves models from the old app. This approach allows you to deploy your
project anywhere without first installing and then uninstalling the old app.

Here’s a sample migration:

  `myapp/migrations/0124_move_old_app_to_new_app.py`[¶](#id8)

```
from django.apps import apps as global_apps
from django.db import migrations

def forwards(apps, schema_editor):
    try:
        OldModel = apps.get_model("old_app", "OldModel")
    except LookupError:
        # The old app isn't installed.
        return

    NewModel = apps.get_model("new_app", "NewModel")
    NewModel.objects.bulk_create(
        NewModel(new_attribute=old_object.old_attribute)
        for old_object in OldModel.objects.all()
    )

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
    dependencies = [
        ("myapp", "0123_the_previous_migration"),
        ("new_app", "0001_initial"),
    ]

    if global_apps.is_installed("old_app"):
        dependencies.append(("old_app", "0001_initial"))
```

Also consider what you want to happen when the migration is unapplied. You
could either do nothing (as in the example above) or remove some or all of the
data from the new application. Adjust the second argument of the
[RunPython](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.RunPython) operation accordingly.

## Changing aManyToManyFieldto use athroughmodel¶

If you change a [ManyToManyField](https://docs.djangoproject.com/en/ref/models/fields/#django.db.models.ManyToManyField) to use a `through`
model, the default migration will delete the existing table and create a new
one, losing the existing relations. To avoid this, you can use
[SeparateDatabaseAndState](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.SeparateDatabaseAndState) to rename the existing table to the new
table name while telling the migration autodetector that the new model has
been created. You can check the existing table name through
[sqlmigrate](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-sqlmigrate) or [dbshell](https://docs.djangoproject.com/en/ref/django-admin/#django-admin-dbshell). You can check the new table name
with the through model’s `_meta.db_table` property. Your new `through`
model should use the same names for the `ForeignKey`s as Django did. Also if
it needs any extra fields, they should be added in operations after
[SeparateDatabaseAndState](https://docs.djangoproject.com/en/ref/migration-operations/#django.db.migrations.operations.SeparateDatabaseAndState).

For example, if we had a `Book` model with a `ManyToManyField` linking to
`Author`, we could add a through model `AuthorBook` with a new field
`is_primary`, like so:

```
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                # Old table name from checking with sqlmigrate, new table
                # name from AuthorBook._meta.db_table.
                migrations.RunSQL(
                    sql="ALTER TABLE core_book_authors RENAME TO core_authorbook",
                    reverse_sql="ALTER TABLE core_authorbook RENAME TO core_book_authors",
                ),
            ],
            state_operations=[
                migrations.CreateModel(
                    name="AuthorBook",
                    fields=[
                        (
                            "id",
                            models.AutoField(
                                auto_created=True,
                                primary_key=True,
                                serialize=False,
                                verbose_name="ID",
                            ),
                        ),
                        (
                            "author",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.DO_NOTHING,
                                to="core.Author",
                            ),
                        ),
                        (
                            "book",
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.DO_NOTHING,
                                to="core.Book",
                            ),
                        ),
                    ],
                ),
                migrations.AlterField(
                    model_name="book",
                    name="authors",
                    field=models.ManyToManyField(
                        to="core.Author",
                        through="core.AuthorBook",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="authorbook",
            name="is_primary",
            field=models.BooleanField(default=False),
        ),
    ]
```

## Changing an unmanaged model to managed¶

If you want to change an unmanaged model ([managed=False](https://docs.djangoproject.com/en/ref/models/options/#django.db.models.Options.managed)) to managed, you must remove
`managed=False` and generate a migration before making other schema-related
changes to the model, since schema changes that appear in the migration that
contains the operation to change `Meta.managed` may not be applied.
