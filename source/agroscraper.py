#!/bin/env python2
# -*- coding: utf-8 -*-

"""
Extracting information from transparenzdatenbank.at

Output from the #gutedaten Hackathon in Graz, Sat. 28. Nov. 2015
"""


# import headless browsing
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


# import data handling
from bs4 import BeautifulSoup


__author__ = "Christopher Kittel"
__copyright__ = "Copyright 2015"
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Christopher Kittel"
__email__ = "web@christopherkittel.eu"
__status__ = "Prototype" # 'Development', 'Production' or 'Prototype'


# create webdriver
ff = webdriver.Firefox()
ff.get("http://transparenzdatenbank.at")

# wait until loaded completely
try:
    searchbutton = WebDriverWait(ff, 10).until(EC.presence_of_element_located((By.ID, "startSearch")))
finally:
    ff.find_element_by_xpath("//button[@id='startSearch']").click()


# increase paginatoin
options = ff.find_element_by_xpath("//select[@id='paginationPerPage']")
for option in options.find_elements_by_tag_name("option"):
    # select option '100'
    if option.text == "100":
        option.click()



# MAKE A FUNCTION, HAS TO BE LOOPABLE FOR PAGINATION

# overall table
table = ff.find_element_by_xpath("//table[@id='result']")


elements = table.find_elements_by_xpath("//tbody[@class='ng-scope']")

for element in elements[:3]:
    element.find_element_by_xpath("a[@data-ng-click=['showDetail(record);$event.stopPropagation();']").click()
    records = element.find_elements_by_xpath("tr[@data-ng-click='showDetail(record)']")
    for record in records:
        metadata = record.find_elements_by_xpath("td[@class='ng-binding']")
        overall_sum = record.find_element_by_xpath("td[@class='sum ng-binding']")
        
        for md in metadata:
            print md.text
        print overall_sum.text

        details = record.find_elements_by_xpath("tr[@data-ng-show='record.show']")
        for detail in details:
            title = detail.find_elements_by_tag_name("h4")
            descriptions = detail.find_elements_by_xpath("div[@class='sum ng-binding']/p")
            sums = detail.find_elements_by_xpath("div[@class='sum ng-binding']/p")
            rows= zip(descriptions, sums)
            for row in rows:
                d, s = row
                print d.text, s.text



# MAKE A CLASS FOR INDIVIDUAL SEARCHRESULTS WHICH CAN BE EXPORTED AS CSV