# scq

# Configuration
# TODO: finish tidying up these make tasks

PROJECTPATH="`pwd`/src"

serve:
	export PROJECTPATH=${PROJECTPATH} && cd src && python server.py

console:
	export PROJECTPATH=${PROJECTPATH} && cd src && python

test:
	echo "not yet implemented"

database:
	echo "not yet implemented"

build:
	pip install -r requirements.txt
	npm install

clean:
	find . -name *.pyc -exec rm {} \;

.PHONY: serve clean
