# EU Agricultural Funding Scraper

This scrapers gets data out of [Transparenzdatenbank](http://transparenzdatenbank.at/), which displays EU aids for Austrian agricultural businesses. The scraper exports the data into CSV so it can be analyzed and visualized.

This repository provides the code and documentation, and keeps track of [bugs as well as feature requests](https://github.com/OKFNat/agroScraper/issues).

* Original Data Source: [Transparenzdatenbank](http://transparenzdatenbank.at/)
- [Extracted Data](https://github.com/OKFNat/data/tree/master/agrarfoerderungen)
* Team: [Gute Taten für gute Daten](http://okfn.at/gutedaten/) project of [Open Knowledge Austria](http://okfn.at/).
* Status: Production
* Documentation: English
* Licenses:
  * Content: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
  * Software: [MIT License](http://opensource.org/licenses/MIT)

**Used Software**

The sourcecode is written in Python 3. It was created with use of [requests](http://docs.python-requests.org/en/master/).

## SCRAPER

### Description

The scraper first retrieves the overall data about funding aid and saves it to a local file. In a second pass the scraper retrieves the detailed data for the funding IDs mentioned in the overall data. The second pass may take few hours to complete and to avoid data loss due to network errors, the scraper regularly caches the detailed data - this also reduces server strain. The retrieved data is then reformatted and saved to a CSV-file.

### Run scraper

You need Python 3 for running this, it handles encoding better.

Run this in your shell with your custon foldername:
```bash
python3 agroscraper.py --output OUTPUTFOLDERNAME --year 2014
```

The scraper produces two JSON-files and one CSV-file, where `YYYY` will be replaced by the year the funding data is about:
* `agrofunding_YYYY.json`, containing IDs, names of recipients, postcode and municipality, year and total amount.
* `agrofunding_details_YYYY.json`, containing all of the above plus a detailed description per funding with type, description and partial amounts.
* `agrofunding_YYYY.csv` with the following headers: "unique_id", "funding_id", "recipient", "year", "postcode", "municipality", "total_amount", "detail_id", "type", "partial_amount"

## DATA INPUT

The original data table displays recipients ("Zahlungsempfänger"), postcode ("PLZ"), municipality ("Gemeinde"), year ("Jahr") and total amount ("Betrag").

| Zahlungsempfänger | PLZ | Gemeinde | Jahr | Betrag |
|---|---|---|---|
| NAME | XXXX | ORTSNAME | 2014 | 7812,00 |

When clicking on an entry it opens up and displays detailed information, such as type ("Art der Förderung"), a short description ("Kurzbeschreibung") and itemized detailed amounts ("Teilbeträge").


### Soundness

**Scope of dataset**

The current database provides data only for 2014 (as at May 2015).

> Demnach müssen ab 2015 auch wieder natürliche Personen unter den Empfängern veröffentlicht werden. Zu veröffentlichen sind: Name, Gemeinde samt Postleitzahl, Betrag der Zahlungen aus dem EGFL, Betrag der Zahlungen aus dem ELER einschließlich der nationalen Anteile sowie Bezeichnung und Beschreibung der geförderten Maßnahmen unter Angabe des jeweiligen EU-Fonds des vorangegangenen EU- Haushaltsjahrs. Das EU-Haushaltsjahr beginnt am 16.10. eines Jahres und endet am 15.10. des Folgejahres. Die veröffentlichten Daten bleiben vom Zeitpunkt ihrer ersten Veröffentlichung zwei Jahre lang zugänglich. Ausgenommen von der namentlichen Veröffentlichungspflicht sind lediglich jene Personen, deren jährliche Zahlungen 1.250,-- Euro nicht übersteigen. In diesem Fall werden die Empfänger in kodierter Form veröffentlicht.

**Data errors found**

None so far, please [raise an issue](https://github.com/OKFNat/agroScraper/issues) if you detect one.

## DATA OUTPUT

### Data model of agrofunding.json

```
{"id":
  {
   "betrag": float,
   "gemeinde": "str",
   "id": "str",
   "jahr": "str",
   "name": "str",
   "plz": int
  }
}
```

### Data model of agrofunding_details.json

```
{"id":
	{
		"id": int,
		"recipient": "str",
		"postcode": int,
		"municipality": "str",
		"year": int,
		"total_amount": float
		"details":
    [
			{
				"id": int,
				"type": "str",
				"description": "str",
				"partial_amount": float
			}
		]
	}
}
```

### Data model of agrofunding.csv

Tabular data (delimiter `,`, quotechar `"`) with the following columns:

> unique_id, funding_id, recipient, year, postcode, municipality, total_amount, detail_id, type, partial_amount

| unique_id | funding_id | recipient | year | postcode | municipality | total_amount | detail_id | type | partial_amount |
|-----|-----|----|----|----|----|----|------|-------|-------|
|4XYZZZ|47XYZ|AGRARMARKT AUSTRIA|2014|XXXX|LOCATION NAME|24183721.77|8|Verwaltung EU-Fonds - Technische Hilfe|24183721.77|

Fundings are recorded individually, so if one recipient received more than one funding a new entry (row) is created for each. Please note that decimal numbers are indicated by a point `.` when reading in with Excel/LibreOffice.

## CONTRIBUTING

In the spirit of free software, everyone is encouraged to help improve this project.

Here are some ways you can contribute:

* by reporting bugs
* by suggesting new features
* by translating to a new language
* by writing or editing documentation
* by analyzing the data
* by visualizing the data
* by writing code (no pull request is too small: fix typos in the user interface, add code comments, clean up inconsistent whitespace)
* by refactoring code
* by closing issues
* by reviewing pull requests
* by enriching the data with other data sources

When you are ready, submit a [pull request](https://github.com/OKFNat/agroScraper/pulls).

### Submitting an Issue

We use the [GitHub issue tracker](https://github.com/OKFNat/agroScraper/issues) to track bugs and features. Before submitting a bug report or feature request, check to make sure it hasn't already been submitted. When submitting a bug report, please try to provide a screenshot that demonstrates the problem.

## COPYRIGHT

All content is openly licensed under the [Creative Commons Attribution 4.0 license](http://creativecommons.org/licenses/by/4.0/), unless otherwisely stated.

All sourcecode is free software: you can redistribute it and/or modify it under the terms of the MIT License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Visit http://opensource.org/licenses/MIT to learn more about the MIT License.

## SOURCES

**Gute Taten für gute Daten**
- [Website](http://okfn.at/gutedaten/)
- [Extracted Data](https://github.com/OKFNat/data/tree/master/agrarfoerderungen): the scraped and cleaned data.

**Documentation**
- [Original Data](http://transparenzdatenbank.at/)

**Other Datasources**

## REPOSITORY
- [README.md](README.md):
- [code/agroscraper.py](code/agroscraper.py):
- [CHANGELOG.md](CHANGELOG.md):
- [LICENSE](LICENSE):

## CHANGELOG
See the [whole history](CHANGELOG.md). Next the current version.


### Version 0.0.3 - 2016-05-02

* moved global variables to respective functions
* improved format, readability, doc strings
* fixed export errors
