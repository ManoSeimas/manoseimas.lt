all: .done

.done: tmp
	npm instal .
	PATH=$(PATH):node_modules/.bin node_modules/.bin/cake build
	touch .done

tmp:
	mkdir -p $@
