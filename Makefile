TESTS = 
COVERAGE_INCLUDES = --include=project/*

.PHONY: all waf clean run tags todo test coverage syncdb graph

all: c4che/build.config.py waf

c4che/build.config.py:
	./waf configure

waf:
	./waf

clean:
	./waf distclean

run:
	bin/django runserver

tags:
	bin/ctags -v

todo:
	@egrep -n 'FIXME|TODO' $$(find . -type f -regextype egrep -regex '\./project/.*\.(cfg|conf|css|html|in|js|json|md|py|pl|po|pot|rst|sh|txt|wsgi|xml)') Makefile *.cfg

test:
	bin/django test $(TESTS)

coverage:
	bin/coverage run $(COVERAGE_INCLUDES) bin/django test $(TESTS)
	bin/coverage html -d var/htmlcov/ $(COVERAGE_INCLUDES)
	bin/coverage report $(COVERAGE_INCLUDES)
	@echo "Also try xdg-open var/htmlcov/index.html"

syncdb:
	./waf syncdb

graph:
	bin/django graph_models \
	    --group-models \
	    --all-applications \
	    -o var/graph.png
	xdg-open var/graph.png
