#!/usr/bin/python3

import os
import datetime


def nbtscan(db):
    """
    Launch nbtscan on 192.168.0.0/16 ... Edit Mask Here
    """
    os.system("nbtscan 192.168.0.0/16 | grep : > scan.txt")
    os.system("nbtscan 10.0.0.0/16 | grep : >> scan.txt")
    os.system("nbtscan 172.16.0.0/16 | grep : >> scan.txt")

    buffer = open("scan.txt",'rU', encoding='utf-8').readlines()


    for line in buffer :
        data = line.split()
        if len(data) == 5 :
            db.computers.update({"hostname": data[1]}, {
                "$set":
                {"hostname" : data[1],
                 "ip" : data[0],
                 "mac" : data[4],
                 "user" : data[3],
                 "date" : datetime.datetime.now()
                 },
            },True)

        elif len(data) == 4 :
             db.computers.update({"hostname": data[1]}, {
                 "$set":
                {"hostname" : data[1],
                 "ip" : data[0],
                 "mac" : data[3],
                "date" : datetime.datetime.now()
                 },
            },True)