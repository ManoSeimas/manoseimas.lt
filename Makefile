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
		libffi-dev libssl-dev antiword

run: bin/django ; bin/django runserver 0.0.0.0:8000

test: bin/django ; scripts/runtests.py

tags: bin/django ; bin/ctags -v --tag-relative


buildout.cfg: ; ./scripts/genconfig.py config/env/development.cfg

bin/pip: ; virtualenv --no-site-packages --python=python2.7 .

bin/buildout: bin/pip
	bin/pip install zc.buildout==2.3.1
	touch -c $@

mkdirs: var/log var/www/static var/www/media

var/log var/www/static var/www/media: ; mkdir -p $@

widget: manoseimas/widget/frontend/.done

manoseimas/widget/frontend/.done: bin/sassc manoseimas/widget/frontend/scripts/*.coffee manoseimas/widget/frontend/templates/*.handlebars
	$(MAKE) -C manoseimas/widget/frontend

bin/django bin/sassc: bin/buildout buildout.cfg $(wildcard config/*.cfg) $(wildcard config/env/*.cfg) setup.py
	bin/buildout
	touch -c bin/django
	touch -c bin/sassc

migrate: bin/django ; bin/django migrate

reset_mysql:
	mysql -e 'drop database if exists manoseimas; create database manoseimas character set utf8 collate utf8_bin;'

import_backup: bin/django
	mysql -u manoseimas < backup/manoseimas.sql
	bin/django migrate --fake-initial
	bin/django couchdb_sync_id

.PHONY: all help run mkdirs widget tags migrate import_backup
