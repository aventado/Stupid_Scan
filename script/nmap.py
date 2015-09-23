#!/usr/bin/python3

import os


def nmapscan(db,ip):
    """
    Launch os.system nmap -A scan
    """
    if db and ip :
        os.system("nmap -A %s > nmap.txt" % ip )

        buffer = open("nmap.txt",'rU', encoding='utf-8').readlines()
        buf = ""
        for line in buffer :
            buf += line + "<br/>"
        db.computers.update({"ip": ip}, {
                             "$set":
                                 {
                                    "nmap" : buf
                                 } } )
