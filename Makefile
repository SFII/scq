# scq makefile

PROJECTPATH="`pwd`/src"
TESTINGPATH="`pwd`/test"
TESTS = $(wildcard test/*.py)

serve:
	@export PROJECTPATH=${PROJECTPATH} && gulp prod-js && python3 server.py

serve-nogulp:
	@export PROJECTPATH=${PROJECTPATH} && python3 server.py

console:
	@export PROJECTPATH=${PROJECTPATH} && gulp dev-js && python3

test:
	@export PROJECTPATH=${PROJECTPATH} && python3 server.py --test

bootstrap_data:
	@export PROJECTPATH=${PROJECTPATH} && python3 server.py --bootstrap_data

wipe_user_data:
	@export PROJECTPATH=${PROJECTPATH} && python3 server.py --wipe_user_data

build:
	pip3 install -r requirements.txt
	npm install

clean:
	@find . -name *.pyc -exec rm {} \;

.PHONY: test serve clean serve-dev
