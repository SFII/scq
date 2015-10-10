# scq

# Configuration
# TODO: finish tidying up these make tasks

PYTHON="/usr/bin/python"

# Targets

PROJECTPATH="`pwd`/src"

serve:
	export PROJECTPATH=${PROJECTPATH} && cd src && ${PYTHON} server.py

console:
	export PROJECTPATH=${PROJECTPATH} && cd src && ${PYTHON}

test:
	echo "not yet implemented"

database:
	echo "not yet implemented"

build:
	sudo apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev
	sudo pip install -r requirements.txt

clean:
	find . -name *.pyc -exec rm {} \;

.PHONY: serve clean
