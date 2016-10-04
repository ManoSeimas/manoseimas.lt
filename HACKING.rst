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

Install npm packages::

    npm install

Create mysql user::

    mysql -u root
      CREATE DATABASE IF NOT EXISTS manoseimas CHARSET=utf8;
      CREATE USER 'manoseimas'@'localhost';
      GRANT ALL PRIVILEGES ON *.* TO 'manoseimas'@'localhost';
      FLUSH PRIVILEGES;

Create mysql config file::

    vim ~/.my.cnf
      [client]
      database = manoseimas
      user = manoseimas
      password =
      default-character-set = utf8

Run migrations::

    bin/django migrate

And run the project::

    make run


OSX Setup
---------

You will need to run MySQL 5.7 in OSX. Cleanest way to do that is to use Docker
for OSX and ``docker-compose``::

    docker-compose up -d  # -d will run in daemon mode.

You will likely need some headers for mysql and a client, so you'll have to install
these (mysql server won't get run unless enabled)::

    brew install mysql

Create mysql user::

    mysql -u root
      CREATE DATABASE IF NOT EXISTS manoseimas CHARSET=utf8;
      CREATE DATABASE IF NOT EXISTS test_manoseimas CHARSET=utf8;
      CREATE USER 'manoseimas'@'%';
      GRANT ALL PRIVILEGES ON *.* TO 'manoseimas'@'%';
      FLUSH PRIVILEGES;

Build the project::

    make

Install npm packages::

    npm install

Create mysql config file::

    vim ~/.my.cnf
      [client]
      host = 127.0.0.1
      database = manoseimas
      user = manoseimas
      password =
      default-character-set = utf8

Run migrations::

    bin/django migrate

And run the project::

    make run

Run tests::

    make test

If you see a problem migrating permissions in tests (``OperationalError``
any tests are run), recreate the test DB with ``utf-8`` encoding.
(TODO: This should be automated)::

    mysql -e 'DROP DATABASE IF EXISTS test_manoseimas; CREATE DATABASE test_manoseimas CHARSET=utf8;'


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
    bin/scrapy crawl sittings  # Sittings and voting stats
    bin/scrapy crawl lobbyists  # Lobbyists

You can use ``bin/scrapy crawl --loglevel=INFO <spider>`` to get more details
to de screen while scrapy crawls.

These commands are used to precompute and load various things::

    bin/django recompute_stats

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
reused. Usually this is a good thing, because tests will run much faster, but
if database schema changes, you will need to create a migration file and then
recreate database::

    mysql -e 'DROP DATABASE IF EXISTS test_manoseimas; CREATE DATABASE test_manoseimas CHARSET=utf8;'
