.PHONY: build clean test

build: env
	$(CURDIR)/env/bin/pip install -r $(CURDIR)/requirements.txt

env:
	virtualenv -p `which python3` $(CURDIR)/env

clean:
	rm -rf $(CURDIR)/env

test: build
	$(CURDIR)/env/bin/python -m unittest discover