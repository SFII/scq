# scq

# Configuration
# TODO: finish tidying up these make tasks

PROJECTPATH="`pwd`/src"
TESTINGPATH="`pwd`/test"
TESTS = $(wildcard test/*.py)

serve:
	export PROJECTPATH=${PROJECTPATH} && cd ./src && python3 server.py

console:
	export PROJECTPATH=${PROJECTPATH} && cd ./src && python3

test:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3 test: $(TEST); \
		python3 $(TEST); \
		)

database:
	echo "not yet implemented"

build:
	pip3 install -r requirements.txt
	npm install
	gulp dev-js

clean:
	find . -name *.pyc -exec rm {} \;

.PHONY: test serve clean
