# Stupid Scan

It's like autoscan network but more dirty :').

## Intro

Stupid scan it's a very simple app which scan the network with linux command nbtscan & nmap.

## Install

On debian / ubuntu :

		sudo apt-get install nbtscan
		sudo apt-get install nmap

For db I use mongodb :

		sudo apt-get install mongodb-server
	
Python modules :

	pip install -r requirements.txt

## Run

python3 app.py

go on http://0.0.0.0:5000


## Crontab ntbscan

	chmod a+x cron.py
	
	*/15 * * * * /usr/bin/python3.4 /path/to/app/cron.py >/dev/null 2>&1


You are Welcome to Pull it !


. screenshot :

![alt tag](http://thxer.com/data/images/ssc1.jpg)


![alt tag](http://thxer.com/data/images/ssc2.jpg)
