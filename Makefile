# scq makefile

PROJECTPATH="`pwd`/src"
TESTINGPATH="`pwd`/test"
TESTS = $(wildcard test/*.py)

serve:
	@export PROJECTPATH=${PROJECTPATH} && gulp prod-js && cd ./src && python3 -m tornado.autoreload server.py

serve-nogulp:
	@export PROJECTPATH=${PROJECTPATH} && cd ./src && python3 server.py

console:
	@export PROJECTPATH=${PROJECTPATH} && gulp dev-js && cd ./src && python3

test:
	@cd src && python3 -m tornado.testing discover test --verbose

initialize_test_db:
	@cd src && python3 -c "from server import initialize_db; initialize_db('test')"

bootstrap_data:
	@read -p 'Enter User ID to boostrap (include surrounding quotes):' x; \
	cd src && python3 -c 'from server import bootstrap_data; bootstrap_data('$$x')'

wipe_user_data:
	@read -p 'Enter User ID to wipe (include surrounding quotes):' x; \
	cd src && python3 -c 'from server import wipe_data; wipe_data('$$x')'

build:
	pip3 install -r requirements.txt
	npm install

clean:
	@find . -name *.pyc -exec rm {} \;

.PHONY: test serve clean serve-dev
