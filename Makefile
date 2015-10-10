# scq

# Configuration
# TODO: finish tidying up these make tasks

PYTHON="/usr/bin/python"
EASYINSTALL="/path/to/easy_install"
NOSETESTS="/path/to/nosetests"

# Targets

PROJECTPATH="`pwd`/src"

server:
	export PROJECTPATH=${PROJECTPATH} && cd src && ${PYTHON} server.py

console:
	export PROJECTPATH=${PROJECTPATH} && cd src && ${PYTHON}

test:
	${NOSETESTS} -i should -i spec --verbose --nocapture

database:
	mkdir -p data
	export PROJECTPATH=${PROJECTPATH} && cd src/ && ${PYTHON} util/database.py

build:
	${EASYINSTALL}

clean:
	find . -name *.pyc -exec rm {} \;

.PHONY: server test database clean
