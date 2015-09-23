#!/usr/bin/python3

import config
from mongo import db as db
import pymongo
from threading import Thread

from script.nmap import nmapscan
from script.ntbscan import nbtscan

# Script for crontab Enjoy' Edit it !
nbtscan(db)

