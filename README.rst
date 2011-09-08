Building development environment
================================

To prepare development environment, only single command is needed::

    make

If you can't use ``make`` (for example if you running Windows), use this
commands::

    python waf configure build

Running development web server
------------------------------

::

    make run

or::

    bin/django runserver


Building production environment
===============================

1. Configure build environment (see ``./waf --help`` for more configuration
   options with descriptions). Here is example comand with all required
   configuration options::

    ./waf configure --production \
                    --server-name=www.example.com \
                    --server-admin=administrator@example.com

   If you need to update production server often with possible changing
   configuration options, you can create a sheel script called ``configure``
   with configuration line. This script can be used later if one of
   configuration options changes, then you can change it in this script,
   without touching other options.

2. Build project::

    make

Project layout
==============

bin/
    All executables.

bin/django
    Django tool originally named ``manage.py``.

bootstrap.py
    Buildout bootstrap files, this file is used to prepare buildout
    environment. You don't need to use this file, this file is used
    automatically from ``wscript``.

buildout.cfg
    Auto generated buildout configuration file. You should not modify this
    file, instead change original template file ``conf/buildout.cfg``.

config/
    All project configuration template files. Templates are written using
    Cheetah_ template language. Templates for configuration files are used to
    make possible various configuration modifications depending on build
    options.

config/settings.py
    Template for Django settings file. Output of this template will be stored
    to ``manoseimas/settings.py``.

config/buildout.cfg
    Buildout configuration file, output will be stored in environment root
    folder as ``buildout.cfg``.

config/apache.conf
    Apache virtual host configuration files. Output of this template will be
    stored to ``var/etc/apache.conf``. You can include this file to apache
    virtual host configuration files using ``include`` directive::

        include /path/to/project/root/var/etc/apache.conf

initial_data.json
    Initial project database data. Used only for development to provide each
    developer with databases filled with test data.

    This file should be used only for project wide fixtures, all application
    related fixtures must be stored in ``fixtures/initial_data.json`` file of
    each application.

Makefile
    This is simply wrapper for Waf_. It helps to build project environment more
    easily. Instead plain Waf_::

        ./waf configure
        ./waf build

    Using Makefile you only need one command::

        make

    Although this command will not be enough if you want to pass some extra
    configuration parameters.

manoseimas/
    Django project code.

manoseimas/settings.py
    Auto generated Django settings file. You should not modify this file,
    instead change original template file ``conf/settings.py``.

manoseimas/static
    Django project wide static files, put here all your images, CSS and
    JavaScript files.

manoseimas/templates/
    Django project wide templates.

manoseimas/sass/
    SASS style files, compiled CSS output will be stored to ``var/sass``.

manoseimas/urls.py
    Django project wide urls.

parts/
    This is buildout folder, where files from external libraries are stored.

var/
    Folder where all automatically generated content are stored.

var/development.db
    Sqlite database, used for development.

var/etc/
    Generated configuration files.

var/log/
    Logs.

var/sass/
    Generated SASS files.

var/www/media/
    Folder for serving static content, here should be stored all user uploaded
    data.
    
var/www/static/
    Folder for serving static files, here automatically will be collected
    static files from Django project and all applications that have static
    content.

waf
    Waf_ executable.

wscript
    Waf_ script files. This file is used to describe how project environment
    should be built.


.. _Waf: http://code.google.com/p/waf/
.. _Cheetah: http://www.cheetahtemplate.org/
