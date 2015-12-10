# scq

# Configuration
# TODO: finish tidying up these make tasks

PROJECTPATH="`pwd`/src"
TESTINGPATH="`pwd`/test"
TESTS = $(wildcard test/*.py)

serve:
	export PROJECTPATH=${PROJECTPATH} && gulp prod-js && cd ./src && python3 server.py

serve-nogulp:
	export PROJECTPATH=${PROJECTPATH} && cd ./src && python3 server.py

serve-dev:
	gulp watch & cd ./src && python3 ./setup.py && python3 ./server.py

console:
	export PROJECTPATH=${PROJECTPATH} && gulp dev-js && cd ./src && python3

test:
	cd src && python3 -m unittest discover test

bootstrap_data:
	cd ./src && python3 -c 'from server import bootstrap_data; bootstrap_data()'

build:
	pip3 install -r requirements.txt
	npm install

clean:
	find . -name *.pyc -exec rm {} \;

.PHONY: test serve clean serve-dev
