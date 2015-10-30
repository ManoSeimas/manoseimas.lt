How to deploy
=============

Deployment scripts are written using Ansible_.  In order to deploy you need to
install Ansible_::

    sudo apt install python-pip
    pip install --user ansible

(Be sure to include ``~/.local/bin`` early in your ``PATH``!)

To deploy this app on staging run the following command::

    ansible-playbook -i staging deploy.yml -K

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
