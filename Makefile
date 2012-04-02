#!/usr/bin/make

PROJECT=manoseimas
TESTS = sboard
COVERAGE_INCLUDES = --include=project/*


.PHONY: all
all: c4che env
	env/bin/python waf

.PHONY: run
run: all
	bin/django estool --path=parts/elasticsearch start
	bin/django runserver

.PHONY: stop
stop:
	bin/django estool --path=parts/elasticsearch stop

c4che/_cache.py:
	if [ -x configure ] ; then \
	    ./configure ; \
	else \
	    ./waf configure --project-name=$(PROJECT)
	fi

env:
	./waf virtualenv


# Helpers

.PHONY: clean
clean:
	./waf distclean

.PHONY: clean
messages:
	./waf makemessages

.PHONY: tags
tags: all
	bin/ctags -v

.PHONY: todo
todo:
	@egrep -nirI 'FIXME|TODO|XXX' $(PROJECT) config wscript

test: all
	bin/django test $(TESTS)

coverage: all
	bin/coverage run $(COVERAGE_INCLUDES) bin/django test $(TESTS)
	bin/coverage html -d var/htmlcov/ $(COVERAGE_INCLUDES)
	bin/coverage report $(COVERAGE_INCLUDES)
	@echo "Also try xdg-open var/htmlcov/index.html"

graph: all
	bin/django graph_models \
	    --group-models \
	    --all-applications \
	    -o var/graph.png
	xdg-open var/graph.png
