#!/bin/env python3
# -*- coding: utf-8 -*-

"""
Extracting information from transparenzdatenbank.at

Output from the #gutedaten Hackathon in Graz, Sat. 28. Nov. 2015



[
    {
        "id": int,
        "recipient": "str",
        "postcode": int,
        "municipality": "str",
        "year": int,
        "total_amount": float
        "details": [
            {
                "id": int,
                "type": "str",
                "description": "str",
                "partial_amount": float
            }
        ]   
    }
]
"""


__author__ = "Christopher Kittel"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainer__ = "Christopher Kittel"
__email__ = "web@christopherkittel.eu"
__status__ = "Prototype" # 'Development', 'Production' or 'Prototype'


import requests

import json
import csv

import sys


def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()



url = 'http://transparenzdatenbank.at/suche'

header = {"Accept": "application/json, text/plain, */*",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
           "Content-Length": "100",
           "Content-Type": "application/json;charset=utf-8",
           "DNT": "1",
           "Host": "transparenzdatenbank.at",
           "PAGINATION_CURRENT": "1",
           "PAGINATION_PER_PAGE": "140000",
           "Referer": "http://transparenzdatenbank.at/",
           "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"
           }

# json string
payload = "{\"name\":\"\", \"betrag_von\":\"\", \"betrag_bis\":\"\", \"gemeinde\":\"\", \"massnahme\":null,\"jahr\":2014, \"sort\":\"name\"}"



try: # load cached search
	with open("firstround.json", "r") as infile:
		raw = json.load(infile)
except:
	response = requests.request("POST", url, data=payload, headers = header)
	raw = response.json()
	# make a quick save
	with open("firstround.json", "w") as outfile:
	    json.dump(raw, outfile)

# create new header for detailed search

searchheader = {'Host': 'transparenzdatenbank.at',
                 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
                 'Accept': 'application/json, text/plain, */*',
                 'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
                 'Accept-Encoding': 'gzip, deflate',
                 'DNT': '1',
                 'Referer': 'http://transparenzdatenbank.at/',
                 'Cookie': 'AMA=!nuCdkyly1f7Zu8TJc9WWi6/Juy2r0rwBzfMkAVDZdlK7ppJA07eM8ERA7mL9kNBeY+AJZtNYoza5Ivk=; TS018cbf1b=015c95df5d1c780212c177d6031479ab2c968358d311dc333c0baee3ece7918812734b06fc4e15c151ca4dfe6a81a3b37c01e323c9'
                 }

# to hold detailed results
results = []

# for progress bar
progress = 0.0
maxi = len(raw)



for r in raw:
    result = {}
    result["id"] = int(r.get("id"))
    result["recipient"] = r.get("name")

    # 
    if r.get("plz") is None:
        result["postcode"] = "NA"
    else:
        result["postcode"] = int(r.get("plz"))
        
    result["municipality"] = r.get("gemeinde")
    result["year"] = int(r.get("jahr"))
    result["total_amount"] = float(r.get("betrag"))
    result["details"] = []


    searchurl = 'http://transparenzdatenbank.at/suche/details/%s/2014' %r.get("id")
    rawdetails = requests.request("GET", searchurl, headers = searchheader).json()
    for rd in rawdetails:
        detail = {}

        detail["id"] = int(rd.get("id"))
        detail["type"] = rd.get("bezeichnung")
        detail["description"] = rd.get("beschreibung")
        detail["partial_amount"] = float(rd.get("betrag"))

        result["details"].append(detail)

    results.append(result)

    # more progress
    progress += 1
    percent = progress/maxi
    drawProgressBar(percent)


with open("agrofunding.json", "w") as outfile:
    json.dump(results, outfile)


with open("agrofunding.csv", "w") as csvfile:
	agrowriter = csv.writer(csvfile, delimiter = ",", quotechar='"')
	agrowriter.writerow(["id", "recipient", "year", "postcode", "municipality", "total_amount", "detail_id", "type", "partial_amount"])
	for result in results[:3]:
	    metadata = [result.get("id"), result.get("recipient"), result.get("year"), result.get("postcode"), result.get("municipality"), result.get("total_amount")]
	    for detail in result.get("details"):
	        data = [detail.get("id"), detail.get("type"), detail.get("partial_amount")]
	        agrowriter.writerow(metadata+data)