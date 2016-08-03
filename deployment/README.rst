How to deploy
=============

Deployment scripts are written using Ansible_.  In order to deploy you need to
install Ansible_::

    sudo apt install python-pip
    pip install --user ansible

(Be sure to include ``~/.local/bin`` early in your ``PATH``!)

To deploy this app on staging run the following command::

    ansible-playbook -i staging deploy.yml -K

If you don't have root access on the staging server, you can still do an update
of the existing deployment with::

    ansible-playbook -i staging deploy.yml -K --tags update


.. _Ansible: http://www.ansible.com/


About deployment scripts
========================

Main deployment script is ``deploy.yml``. In addition, you can specify
where to deploy by specifying a different inventory file, e.g. ::

    ansible-playbook -i production deploy.yml -K

By default ``staging`` is used as the Ansible inventory file. This is
specified in ``ansible.cfg`` which is read by Ansible by default.

You can check what Ansible would change without actually making any
changes by running ::

    ansible-playbook -i staging deploy.yml -K -C

If you have your SSH key in root's authorized_keys, you can avoid having
to type your sudo password if you do ::

    ansible-playbook -i staging deploy.yml -u root


Testing deployment scripts
==========================

Before doing real deployment you may want to try it in a Vagrant sandbox.

Install vagrant, virtualbox and ansible::

    sudo apt install vagrant virtualbox python-pip
    pip install --user ansible

For the vagrant, you will may need to download it from vagrant.com_,
because at least 1.6 version is required.

.. _vagrant.com: http://www.vagrantup.com/downloads.html

Run the following command::

    vagrant up

It downloads virtualbox images and runs deployment scripts. If you want to
retest deployment scripts repeatedly run::

    vagrant provision

If everything went well you should see a working web page by visiting
http://localhost:8080/ .


Working on the server
=====================

You may want re-run scraping on-demand on the server. To do so please login onto
manoseimas.lt and run ::

    sudo -u manoseimas -H bin/scrapy crawl <spinder-name>


Upgrade Notes
=============

2016-06-04 New test upgrade notes
---------------------------------

- By adding new test, CouchDB and django-sboard was `removed completely
  <https://github.com/ManoSeimas/manoseimas.lt/commit/d6a6f36472cd55cd23f48cd7bf7e420655f538d8>`_.

- When running ``bin/django migrate`` if you get error like this::

    RuntimeError: Error creating new content types. Please make
                  sure contenttypes is migrated before trying to
                  migrate apps individually.

- You need to execute following command in order to fix that::

    mysql -e 'alter table django_content_type drop column name;'

  For some reasons, it looks that ``contenttypes.0002_remove_content_type_name``
  migrations was not executend when upgrading to Django 1.8.

  For more information see this bug report:
  https://code.djangoproject.com/ticket/25100
