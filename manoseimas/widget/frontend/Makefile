all: .done

.done: tmp scripts/*.coffee templates/*.handlebars
	npm instal .
	PATH=$(PATH):node_modules/.bin node_modules/.bin/cake build
	touch .done

tmp:
	mkdir -p $@
