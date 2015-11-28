#!/bin/env python2
# -*- coding: utf-8 -*-

"""
Extracting information from transparenzdatenbank.at

Output from the #gutedaten Hackathon in Graz, Sat. 28. Nov. 2015



[
    {
        "id": int,
        "recipient": "str",
        "zip code": int,
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
import time

import json


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

payload = "{\"name\":\"\", \"betrag_von\":\"\", \"betrag_bis\":\"\", \"gemeinde\":\"\", \"massnahme\":null,\"jahr\":2014, \"sort\":\"name\"}"


raw = []
response = requests.request("POST", url, data=payload, headers = header)
raw.extend(response.json())

# make a quick save
with open("firstround.json", "w") as outfile:
    json.dump(response.json(), outfile)


ids = [r.get("id") for r in raw]


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


details = []

for id_ in ids[:10]:
    searchurl = 'http://transparenzdatenbank.at/suche/details/%s/2014' %id_
    detail = requests.get(searchurl, searchheader)
    details.extend(detail.json())



results = {}