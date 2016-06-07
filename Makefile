all: bin/django widget mkdirs

help:
	@echo 'make ubuntu     install the necessary system packages (requires sudo)'
	@echo 'make            set up the development environment'
	@echo 'make run        start the web server'
	@echo 'make tags       build ctags file'

ubuntu:
	sudo apt-get update
	sudo apt-get -y build-dep python-imaging python-mysqldb python-pylibmc
	sudo apt-get -y install build-essential python-dev python-virtualenv \
		git mercurial gettext exuberant-ctags libxml2-dev libxslt1-dev \
		libffi-dev libssl-dev antiword coffeescript

run: bin/django ; bin/django devserver 0.0.0.0:8000

test: bin/django ; scripts/runtests.py

tags: bin/django ; bin/ctags -v --tag-relative


buildout.cfg: ; ./scripts/genconfig.py config/env/development.cfg

bin/pip:
	rm -rf lib
	virtualenv --no-site-packages --python=python2.7 .
	bin/pip install -U pip setuptools wheel

bin/buildout: bin/pip
	bin/pip install zc.buildout==2.4.6
	touch -c $@

mkdirs: var/log var/www/static var/www/media

var/log var/www/static var/www/media: ; mkdir -p $@

bin/django bin/sassc: bin/buildout buildout.cfg $(wildcard config/*.cfg) $(wildcard config/env/*.cfg) setup.py
	bin/buildout
	touch -c bin/django
	touch -c bin/sassc

migrate: bin/django ; bin/django migrate

clean:
	rm -rf bin develop-eggs .installed.cfg .mr.developer.cfg buildout.cfg parts

reset_mysql:
	mysql -e 'drop database if exists manoseimas; create database manoseimas character set utf8 collate utf8_bin;'

import_backup: bin/django
	mysql -u manoseimas < backup/manoseimas.sql
	bin/django migrate --fake-initial

.PHONY: all help run mkdirs widget tags migrate clean reset_mysql import_backup

here := manoseimas/widget/frontend
include $(here)/Makefile
widget: $(widget_stamp)
# one extra dependency
$(widget_stamp): bin/sassc
