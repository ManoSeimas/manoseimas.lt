Here are instructions how you can build and run this project on your own
computer to get started with the development.

Configuring development environment
===================================

Ubuntu 14.04
------------

Before starting, install system dependencies (this will require ``sudo``)::

    make ubuntu

Run CouchDB using Docker::

    docker run -d -p 5984:5984 --name couchdb klaemo/couchdb:1.6.1

If you don't have Docker, you can install CouchDB using the manual way (see
`Manual CouchDB install`_) also you can install CouchDB using your package
manager. It's up to you how you get CouchDB running.

By default ``config/env/development.cfg`` configuration is used and it expect
you to have ``django-sboard`` and ``couchdbkit`` in ``parts`` directory. So you
have to clone those repositories manually::

    mkdir parts
    hg clone ssh://hg@bitbucket.org/sirex/django-sboard parts/django-sboard
    git clone -b django-1.8 git@github.com:sirex/couchdbkit.git parts/couchdbkit

Build the project::

    make

Run migrations::

    bin/django migrate

Sync CouchDB views for scrapy::

    bin/initscrapy

And run the project::

    make run

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

Manual CouchDB install
----------------------

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


CouchDB
=======

To access CouchDB web ui run this command::

    ssh -L 9000:localhost:5984 manoseimas.lt

And visit http://localhost:9000/_utils/


Manually running crawlers and housekeeping
==========================================

These crawlers are currently present::

    bin/scrapy crawl mps  # Parliament member profiles
    bin/scrapy crawl stenograms  # Stenograms
    bin/scrapy crawl law_projects  # Law project stats
    bin/scrapy crawl sittings  # Sittings and voting stats, usually invoked via syncsittings


These commands are used to precompute and load various things::

    bin/django recompute_stats  # Recompute stats on models
    bin/django couchdb_sync_id  # RUn this if you see CouchDB conflicts
    bin/django syncsittings [--update] [--scrape]  # update sittings
    bin/django syncmps [--update] [--scrape]  # update mps
    bin/django syncpositions  # Sync MP and Fraction positions on various political issues

