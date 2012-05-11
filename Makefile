#!/usr/bin/make

PROJECT = manoseimas
COVERAGE_MODULES = $(PROJECT),sboard


.PHONY: all
all: c4che/_cache.py env
	env/bin/python waf

.PHONY: run
run: all
	bin/django runserver

.PHONY: pull
pull:
	hg pull -u
	bin/develop up

c4che/_cache.py:
	if [ -x configure ] ; then \
	    ./configure ; \
	else \
	    ./waf configure --project-name=$(PROJECT) ; \
	fi

env:
	./waf virtualenv


# Helpers

.PHONY: clean
clean:
	./waf distclean

.PHONY: messages
messages:
	./waf makemessages

.PHONY: tags
tags: all
	bin/ctags -v

.PHONY: todo
todo:
	@egrep -nirI 'FIXME|TODO|XXX' $(PROJECT) config wscript

test: all
	bin/django test

test-failed: all
	bin/django test --failed --stop

coverage: all
	bin/django test \
		--with-coverage \
		--cover-erase \
		--cover-inclusive \
		--cover-html \
		--cover-html-dir=../var/htmlcov \
		--cover-package=$(COVERAGE_MODULES)
	@echo "Also try xdg-open var/htmlcov/index.html"

graph: all
	bin/django graph_models \
	    --group-models \
	    --all-applications \
	    -o var/graph.png
	xdg-open var/graph.png
