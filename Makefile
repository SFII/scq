# scq makefile

PROJECTPATH="`pwd`"
TESTS = $(wildcard test/*.py)

serve:
	@export PROJECTPATH=${PROJECTPATH} && gulp prod-js && python3 main.py

serve-nogulp:
	@export PROJECTPATH=${PROJECTPATH} && python3 main.py

dev:
	@export PROJECTPATH=${PROJECTPATH} && gulp prod-js && gulp watch & python3 main.py

console:
	@export PROJECTPATH=${PROJECTPATH} && gulp dev-js && python3

test:
	@export PROJECTPATH=${PROJECTPATH} && python3 main.py --test

bootstrap_data:
	@export PROJECTPATH=${PROJECTPATH} && python3 main.py --bootstrap_data

wipe_user_data:
	@export PROJECTPATH=${PROJECTPATH} && python3 main.py --wipe_user_data

build:
	pip3 install -r requirements.txt
	npm install

clean:
	@find . -name *.pyc -exec rm {} \;

.PHONY: test serve clean serve-dev
