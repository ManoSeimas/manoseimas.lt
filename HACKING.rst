Here are instructions how you can build and run this project on your own
computer to get started with development.

Requirements
============

To be able to build and run this project you will need:

* working CouchDB server instance with created database, specified in
  conf/settings.py file

* python 2.7

* git DVCS's

* C/C++ compiler, python development headers for compiling python extension.

* NodeJS 0.10+

System requirements can be installed all at once using this command:

    sudo apt-get install git
    git clone https://github.com/ManoSeimas/manoseimas.lt.git
    cd manoseimas.lt
    sudo ./waf setup

Note: to customize project settings, you may pass additional parameters to waf.
See './waf --help' for details.


Configuring development environment
===================================

Vagrant
-------

Vagrant is a quick way to setup development environment. Download Vagrant from
`https://www.vagrantup.com/downloads.html` and optionally download Oracle
Virtualbox if it is not shipped with Vagrant.

Then in the project directory do::

    vagrant up
    vagrant ssh
    make run

This should set up all the dependencies for the project. To test the project open the
browser and navigate to::

    http://127.0.0.1:8000


Manual
------

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
