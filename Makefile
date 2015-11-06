# scq

# Configuration
# TODO: finish tidying up these make tasks

PROJECTPATH="`pwd`/src"

serve:
	export PROJECTPATH=${PROJECTPATH} && cd src && python3 server.py

console:
	export PROJECTPATH=${PROJECTPATH} && cd src && python3

test:
	echo "not yet implemented"

database:
	echo "not yet implemented"

build:
	pip3 install -r requirements.txt
	npm install

clean:
	find . -name *.pyc -exec rm {} \;

.PHONY: serve clean
