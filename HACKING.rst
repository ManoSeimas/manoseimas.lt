Here are instructions how you can build and run this project on your own
computer to get started with the development.

Configuring development environment
===================================


First, decide if you want to set it up directly on your machine, or if you want
to use Vagrant.


Direct setup (Ubuntu 14.04)
---------------------------

Before starting, install system dependencies (this will require ``sudo``)::

    make ubuntu

Build the project::

    make

Run migrations::

    bin/django migrate

And run the project::

    make run


Vagrant setup
-------------

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


Manually running crawlers and housekeeping
==========================================

These crawlers are currently present::

    bin/scrapy crawl mps  # Parliament member profiles
    bin/scrapy crawl stenograms  # Stenograms
    bin/scrapy crawl law_projects  # Law project stats
    bin/scrapy crawl sittings  # Sittings and voting stats, usually invoked via syncsittings
    bin/scrapy crawl lobbyists  # Lobbyists

These commands are used to precompute and load various things::

    bin/django recompute_stats  # Recompute stats on models
    bin/django couchdb_sync_id  # Run this if you see CouchDB conflicts
    bin/django syncsittings [--update] [--scrape]  # update sittings
    bin/django syncmps [--update] [--scrape]  # update mps
    bin/django syncpositions  # Sync MP and Fraction positions on various political issues

See the crontab rules in ``deployment/deploy.yml`` for the order and frequency
of their execution.


Running tests
=============

You can use this command for testing::

  bin/django test \
      -v 2 \
      --settings=manoseimas.settings.testing \
      --nocapture --nologcapture \
      --all-modules --with-doctest --doctest-tests \
      --with-coverage --cover-erase --cover-package manoseimas \
      --noinput --failfast --keepdb \
      manoseimas

Note ``--keepdb`` flag, with this flag, database from previous test run will be
reused. Usually this is a good thig, because tests will run much faster, but if
database schema is changes, you need to create migration file and then recreate
database::

    $ mysql -uroot -e 'DROP DATABASE test_manoseimas; CREATE DATABASE manoseimas CHARSET=utf8;'
