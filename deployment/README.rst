How to deploy
=============

Deployment scripts are written using Ansible_, in order to deploy you need to
install Ansible_::

    sudo apt install python-pip
    sudo pip install 'ansible>=1.6'

To deploy this app run following command::

    ansible-playbook deploy.yml

.. _Ansible: http://www.ansible.com/


About deployment scripts
========================

Main deployment script is ``deploy.yml``. In addition, you can specify
deployment profile by specifying vars file, like this::

    ansible-playbook deploy.yml -e vars=vagrant

With this, ``vars/vagrant.yml`` file will be used with some overrides.

By default, ``inventory.cfg`` file is used as Ansible inventory file. This is
specified in ``ansible.cfg`` which is read by Ansible by default.


Testing deployment scripts
==========================

Before doing real deployment you may want to try it in a sandbox, instructions
bellow helps you to do that.

Install vagrant, virtualbox and ansible::

    sudo apt install vagrant virtualbox python-pip
    sudo pip install 'ansible>=1.6'

For the vagrant, you will probably need to download it from vagrant.com_,
because at least 1.6 version is required.


.. _vagrant.com: http://www.vagrantup.com/downloads.html

Run following command::

    vagrant up

It downloads virtuabl mox images and runs deployment scripts. If you want to
rested deployment scripts repeatedly run::

    vagrant provision

If everything went well you should see working web page by visiting
http://localhost:8080/ .
