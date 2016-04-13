#!/bin/sh
#
# job to backup the database, and make a fresh dump of the db for serving

python3 main.py --backup && python3 main.py --dump
