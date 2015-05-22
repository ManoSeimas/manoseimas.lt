all: bin/django

help:
	@echo 'make ubuntu     install the necessary system packages (requires sudo)'
	@echo 'make            set up the development environment'
	@echo 'make run        start the web server'
	@echo 'make tags       build ctags file'

ubuntu:
	sudo apt-get update
	sudo apt-get -y build-dep python-imaging python-mysqldb
	sudo apt-get -y install build-essential python-dev python-virtualenv git gettext exuberant-ctags

run: bin/django ; bin/django runserver

tags: bin/django ; bin/ctags -v --tag-relative


buildout.cfg: ; ./scripts/genconfig.py config/env/development.cfg

bin/pip: ; virtualenv --no-site-packages --python=python2.7 .

bin/buildout: bin/pip ; $< install zc.buildout==2.3.1

mkdirs: var/log var/www/static var/www/media

var/log var/www/static var/www/media: ; mkdir -p $@

bin/django: bin/buildout buildout.cfg $(wildcard config/*.cfg) $(wildcard config/env/*.cfg) mkdirs ; $<


.PHONY: all help run mkdirs tags
