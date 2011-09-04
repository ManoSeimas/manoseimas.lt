Development environment
=======================

To prepare development environment, only single command is needed::

    make

If you can't use ``make`` (for example if you running Windows), use this
commands::

    python waf configure build

Running development web server
------------------------------

::

    make run


Production environment
======================

1. Configure build environment (see ``./waf --help`` for more configuration
   options with descriptions). Here is example comand with all required
   configuration options::

    ./waf configure --production \
                    --server-name=www.worapay.com \
                    --server-admin=administrator@example.com

   If you need to update production server often with possible changing
   configuration options, you can create a sheel script called ``configure``
   with configuration line. This script can be used later if one of
   configuration options chanes, then you can change it in this script, without
   touching other options.

2. Build project::

    make

http://sass-lang.com/
sass --watch project/sass:var/generated_static/css