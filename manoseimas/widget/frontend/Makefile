# non-recursive make support
here ?= .

tmpdir := $(here)/tmp
scripts := $(here)/scripts/*.coffee
templates := $(here)/templates/*.handlebars
widget_stamp := $(here)/.done
bindir := node_modules/.bin

.PHONY: all
all: $(widget_stamp)

$(widget_stamp): $(tmpdir) $(scripts) $(templates)
	cd $(here) && npm install .
	cd $(here) && PATH=$(PATH):$(bindir) $(bindir)/cake build
	touch $@

$(tmpdir):
	mkdir -p $@
