Requirements
============

To be able to build and run this project you will need:

* working CouchDB server instance with created database, specified in
  conf/settings.py file

* python

* mercurial DVCS's

* C/C++ compiler, python and development headers for compiling python extension

System requirements can be installed all at once using this command::

    sudo apt-get install mercurial
    hg clone http://bitbucket.org/manoseimas/manoseimas
    cd manoseimas
    sudo ./waf setup

Configuring development environment
===================================

Install CouchDB database. You can install it using your package manager, but
most package managers provides old 1.0.x version of CouchDB which has some
problems with database replication. To avoid these problems, it is recommended
to install 1.2 version. If your package manager has old version, you can
install newes version using:

    https://github.com/iriscouch/build-couchdb

In short, CouchDB can be installed using these commands::

    sudo apt-get install make gcc zlib1g-dev libssl-dev rake
    git clone git://github.com/iriscouch/build-couchdb
    cd build-couchdb
    git submodule init
    git submodule update
    rake

After building CouchDB, run it using this command::

    ./build/bin/couchdb

To prepare and run development environment, only single command is needed::

    make run

If everything works so far, you can fill your database with real data using
this command::

    bin/couch replicate

.. note::

    Database replication can take some tame, be patient.

Configuring production environment
==================================

You need to follow these installation steps:

#. Make sure, that locale packages are installed for all languages, that you
   planing to use::

       sudo apt-get install language-pack-en language-pack-lt

#. Install and configure MySQL server, create new database and user::

       sudo apt-get install mysql-server
       mysql -uroot -p
       > CREATE DATABASE manoseimas CHARACTER SET utf8;
       > CREATE USER 'manoseimas'@'localhost' IDENTIFIED BY '<password>';
       > GRANT ALL ON manoseimas.* TO 'manoseimas'@'localhost';

#. Install Apache with mod_wsgi::

       sudo apt-get install apache2 libapache2-mod-wsgi
   
   Make sure, that Apache locale settings are correct. ``LANG`` environment
   variable in ``/etc/apache2/envvars`` file must be set to ``en_US.UTF-8``,
   but not to ``C``.

   Information about how to configure Apache, will be provided in next steps.

#. Install and configure outgoing mail server::

       sudo apt-get install postfix

   Test your outgoing mail configuration::

       sudo apt-get install mailutils
       echo test | mail -s 'Test mail' yourmail@example.com

#. Install all required build dependencies using this command::

       sudo ./waf setup --production

   This command will install needed packages using ``apt-get`` command. To see
   what command will be executed use ``--dry-run`` flag::

       ./waf setup --production --dry-run

#. Configure project with configuration options that are described in
   ``./waf --help`` command output.

   Here is example how project can be configured::

       ./waf configure \
           --production \
           --server-name=<server-name> \
           --server-admin=<server-admin-email> \
           --mysql-dbname=<mysql-dbname> \
           --mysql-username=<mysql-user> \
           --mysql-password=<mysql-password>



   All your configuration options will be stored in ``configure`` file, if you
   made a mistake, you can edit this file and configure project again using
   this command::

       ./configure

   If you manually run ``./waf configure`` command, existing ``./configure``
   file will not be overwritten.

#. Finally build project using this command::

       make

#. Setup ElasticSearch index, to start indexing CouchDB nodes database::

       bin/django estool install --path=parts/elasticsearch

#. Make sure, that ``var`` folder is writable for Apache user::

       sudo chown -R www-data:www-data var

#. Configure Apache using these commands::

       echo "include $PWD/var/etc/apache.conf" | sudo tee \
           /etc/apache2/sites-available/manoseimas.lt.conf
       sudo a2ensite manoseimas.lt.conf

#. Restart Apache::

       sudo service apache2 restart

#. Create administrator user account::

       bin/django createsuperuser

#. Configure CouchDB public access.

   To do this, first create and admin user::

       curl -X PUT 'http://localhost:5984/_config/admins/<username>' -d '"<password>"'

   Then configure apache virtualhost::

       echo "include $PWD/var/etc/apache.couchdb.conf" | sudo tee \
           /etc/apache2/sites-available/couchdb.manoseimas.lt.conf
       sudo a2enmod proxy_http
       sudo a2ensite couchdb.manoseimas.lt.conf

   Fallow these instructions:

       http://blog.lizconlan.com/sandbox/securing-couchdb.html


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
