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


def get_cache():
    try: # load cached search
        with open("firstround.json", "r") as infile:
            raw = json.load(infile)
    except: # if nothing cached
        raw =get_raw()
        # make a quick save
        with open("firstround.json", "w") as outfile:
            json.dump(raw, outfile)

    try: # load cached details
        with open("agrofunding.json", "r") as infile:
            results = json.load(infile)
    except: # if nothing cached
        results = []

    return raw, results

def get_missing_ids(raw, results):
    """
    Compares cached results with overall expected IDs,
    returns missing ones.
    """
    all_ids = set(raw.keys())
    cached_ids = set([r.get("id") for r in results])
    print("There are {0} IDs in the dataset, we already have {1}. {2} are missing.".format(len(all_ids), len(cached_ids), len(all_ids) - len(cached_ids)))
    return all_ids - cached_ids

def get_raw():
    """
    If not yet cached, will get the raw data.
    """
    response = requests.request("POST", url, data=payload, headers = header)
    raw = response.json()
    return {r.get("id"):r for r in raw}

def crawl(raw, results, missing_ids):
    """
    Adds missing results by iterating over missing IDs.
    """
    # for progress bar
    progress = 0.0
    maxi = len(missing_ids)

    for id_ in missing_ids:

        try:
            r = raw.get(id_)
            results.append(enhance_raw(r, id_))

            # more progress
            progress += 1
            percent = progress/maxi
            drawProgressBar(percent)
        except: # some server/network error
            # store cache
            with open("agrofunding.json", "w") as outfile:
                json.dump(results, outfile)
    return results

def enhance_raw(r, missing_id):
    """
    Reformats the raw data.
    Adds the detailed information to a raw search result.
    """
    result = {}
    result["id"] = int(r.get("id"))
    result["recipient"] = r.get("name")

    # missing values for plz
    if r.get("plz") is None:
        result["postcode"] = "NA"
    else:
        result["postcode"] = int(r.get("plz"))
        
    result["municipality"] = r.get("gemeinde")
    result["year"] = int(r.get("jahr"))
    result["total_amount"] = float(r.get("betrag"))
    result["details"] = get_details(r.get("id"))

    return result

def get_details(id_):
    """
    Gets the detailed information for a funding ID.
    """
    details = []

    searchurl = 'http://transparenzdatenbank.at/suche/details/%s/2014' %id_
    rawdetails = requests.request("GET", searchurl, headers = searchheader).json()
    for rd in rawdetails:
        detail = {}
        detail["id"] = int(rd.get("id"))
        detail["type"] = rd.get("bezeichnung")
        detail["description"] = rd.get("beschreibung")
        detail["partial_amount"] = float(rd.get("betrag"))
        details.append(detail)
    return details

def save2csv(results, filename):
    with open(filename+".csv", "w") as csvfile:
        agrowriter = csv.writer(csvfile, delimiter = ",", quotechar='"')
        agrowriter.writerow(["id", "recipient", "year", "postcode", "municipality", "total_amount", "detail_id", "type", "partial_amount"])
        for result in results:
            metadata = [result.get("id"), result.get("recipient"), result.get("year"), result.get("postcode"), result.get("municipality"), result.get("total_amount")]
            for detail in result.get("details"):
                data = [detail.get("id"), detail.get("type"), detail.get("partial_amount")]
                agrowriter.writerow(metadata+data)

def main():
    raw, results = get_cache()
    missing_ids = get_missing_ids(raw, results)
    results = crawl(raw, results, missing_ids)

    # store final
    with open("agrofunding.json", "w") as outfile:
        json.dump(results, outfile)

    save2csv(results, "agrofunding")


if __name__ == '__main__':
    main()