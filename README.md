# scq
Our main repo for the SCQ senior project.

## Installing Dependenices:
We are using virtual environments to manage our dependencies and make sure they are the same between dev environments. If you don't have a virtualenv setup for this project, this is how to do it.

To setup virtualenvs in general on your computer, do the following:
```
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/Envs
$ source /usr/local/bin/virtualenvwrapper.sh
```

To setup our specific environment:
```
$ mkvirtualenv scq
```

Whenever you are going to work on the project to ensure that we are all using the same dependencies:
```
$ workon scq
```

Add the following to ~/.bashrc (or zshrc if you use one):

```
export WORKON_HOME=$HOME/Envs
source /usr/local/bin/virtualenvwrapper.sh
```

Then run:
```
$ source ~/.bashrc
```

Then go to the project and run this command in your project directory to install the dependencies.
```
$ make build
```

## Install [rethinkdb]( https://rethinkdb.com/docs/install/):

On Mac:

```$ brew update && brew install rethinkdb```

[On Linux](https://www.rethinkdb.com/docs/install/ubuntu/):

Copy and past the entire codeblock:
```
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

## Running:

The webserver can be started by running the following commands:

```
python app.py
```
