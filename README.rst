=============================
Django PostgreSQL light Schemas support
=============================

.. image:: https://badge.fury.io/py/django_postgresql_light_schemas.svg
    :target: https://badge.fury.io/py/django_postgresql_light_schemas

.. image:: https://travis-ci.org/regilero/django_postgresql_light_schemas.svg?branch=master
    :target: https://travis-ci.org/regilero/django_postgresql_light_schemas

.. image:: https://codecov.io/gh/regilero/django_postgresql_light_schemas/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/regilero/django_postgresql_light_schemas

Some PostgreSQl introspection fixs to support postgreSQL users binded to specific schemas,
multiple schemas on same database for various django installations.
No full schema support in models declarations(light).
Based on model table name hack and PostgreSQl users using search_path variables.

If you need/want a deeper schema management search for other django PostgreSQL extensions, like:

- https://github.com/ryannjohnson/django-schemas
- https://github.com/bernardopires/django-tenant-schemas
- https://github.com/damoti/django-postgres-schema

So, what is a light schema hack support, if you cannot declare the scema in the model?

Let's say you use the *classical* trick of hacking the model table name to:

.. code-block:: python

    (...)
    class Meta:
        managed = False
        db_table = 'my_schema\".\"foo'

And you use a PostgreSQL user where the user's **`search_path` variable** is altered
to at least includes `my_schema`. Note that by using a `search_path` variable which
does not start by the public schema you will end up with Django tables set in the
first schema in this list. If you use only one schema you do not need to hack
the `db_table` reference as we made here, `my_schema.` would be implicit for PostgreSQL.
But if you use several schemas in the same django app you can use the trick for
all tables which are not managed by django migrations.

.. code-block:: sql

    -- Case1: you need to access tables in 3 schemas
    ALTER ROLE "my_django-pg-user" SET search_path='my_app,public,other';
    -- Or case 2 : tables are in your schema, priority, but you read things
    -- on the public schema also
    ALTER ROLE "my_django-pg-user" SET search_path='my_app,public';
    -- Or case 3 (we could continue on that): you access one schema only
    ALTER ROLE "my_django-pg-user" SET search_path='my_app';

You cannot use this model to create migrations, but this covers most of the use cases.
This present module will help covering the things which are not covered, i.e.:
- you will be able to make migrations with foreign keys targeting theses hacked models,
 for other models which are not using the trick.
- you will be able to install several Django applications on several schemas, all
sharing the same database, if they all use this module.

Tested on Django **1.10** & **1.11**.

Django problems with schemas
-----------------------------

When using schemas and search_path, without this module, you would encounter
2 problems:
- all instrospections queries made by Django are performed on the catalog, and
are not filtering schemas. All defeinitions, for all tables, all schemas, are
visible on the PostgreSQL catalog (on Djangho 1.11 one the query is filtering on
the public schema, the other are not filtered).
So if you have several django applications installed on different schemas on the same database
**you would see all tables from all installed Django applications** on most queries,
same thing for indexes, and sometimes you would not detect existing tables or
indexes (where the public schema filter is applied), big problems.
Playing with the postgreSQl user **grants** cannot help you, even if the user has
access to only one schema, all definitions would be visible in the catalog.
This module  will fix all the catalog queries to restrict visibility to a given
list of schemas (like 'public' and 'my_app', or just 'my_app').
- when building foreign keys reference from managed tables to unmanaged tables
using the schema trick on `db_table` the `"."`  injection would be reapplied on
the constraint name, preventing the constraint creation.

Quickstart
----------

Install Django PostgreSQL light Schemas support (or use it in the requirements file)::

    pip install django_postgresql_light_schemas

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_postgresql_light_schemas',
        ...
    )

Fix your database connexion settings to use this module instead of the default
postgresql connector (this module inherits most part of this connector).

.. code-block:: python
    DATABASES = {
        'default': {
            'ENGINE': 'django_postgresql_light_schemas.engine',
            'NAME': 'my_app',
            'OPTIONS': {
                    'options': '-c search_path=foo,bar'  # if search_path is not set
            },
            'USER': 'my_app_user',
            (...)
        },
    }


Finally, and this is **required** also, list the schema that your PostgreSQL user
is able to access. As we will remove all informations from schemas which are not
listed there.

.. code-block:: python

    # for django_postgresql_light_schemas, this is the list of schemas known to postgresql, for this application
    # if you do not work with schemas set:
    # SUPPORTED_SCHEMAS = ('public',)
    # if your application as one unique 'foo' schema, set:
    # SUPPORTED_SCHEMAS = ('foo',)
    # if you need several schemas 'public', 'foo', 'bar' and 'baz' set
    # SUPPORTED_SCHEMAS = ('public','foo','bar','baz',)
    # table and indexes set in other schemas WONT be detected by Django intropsection
    # tables and indexes MUST still be uniques in this list of schemas
    # i.e. do not try to have foo.table1 and bar.table1 if you both support foo and bar schemas
    # but that's bnot a problem if you only declare 'foo' in SUPPORTED_SCHEMAS.
    SUPPORTED_SCHEMAS = (
        'public',
        'foo',
        'bar'
    )

Features
--------

* Django 1.10 & 1.11
* fix PostgreSQL introspection to limit visible schemas for Django
* fix Foreign keys names referencing schema hacked db_table names
* ... (if you find other issues, please report!)

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
