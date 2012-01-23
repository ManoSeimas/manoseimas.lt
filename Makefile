#!/usr/bin/make

PROJECT=project
TESTS = 
COVERAGE_INCLUDES = --include=project/*


.PHONY: all
all: c4che env
	env/bin/python waf

.PHONY: run
run: all
	bin/django runserver_plus

c4che:
	./waf configure --project-name=$(PROJECT)

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
