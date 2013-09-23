Here are instructions how you can build and run this project on your own
computer to get started with development.

Requirements
============

To be able to build and run this project you will need:

* working CouchDB server instance with created database, specified in
  conf/settings.py file

* python 2.7

* mercurial DVCS's

* C/C++ compiler, python development headers for compiling python extension.

* NodeJS 0.10+

System requirements can be installed all at once using this command:

    sudo apt-get install mercurial
    hg clone http://bitbucket.org/manoseimas/manoseimas
    cd manoseimas
    sudo ./waf setup

Note: to customize project settings, you may pass additional parameters to waf. 
See './waf --help' for details.


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
