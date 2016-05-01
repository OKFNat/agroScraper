# EU Agricultural funding aids
This scrapers gets data out of [Transparenzdatenbank](http://transparenzdatenbank.at/), which displays EU aids for Austrian agricultural businesses. The scraper exports the data into CSV so it can be analyzed and visualized.

This repository provides the code and documentation, and keeps track of [bugs as well as feature requests(https://github.com/OKFNat/agroScraper/issues).

* Team: [Gute Tagen für gute Daten](http://okfn.at/gutedaten/) of [Open Knowledge Austria](http://okfn.at/)
* Status: Production
* Documentation: English
* Licenses:
  * Content: [Creative Commons Attribution 4.0](http://creativecommons.org/licenses/by/4.0/)
  * Software: MIT License

Used Software

The sourcecode is written in Python 3. It was created with use of [requests](http://docs.python-requests.org/en/master/).

## Scraper

### Description

The scraper first retrieves the overall data about funding

### Run scraper

You need Python 3 for running this, it handles encoding better.

```python
python3 agroscraper.py --output OUTPUTFOLDERNAME --year 2014
```

The scraper produces two JSON-files and one CSV-file:
* `agrofunding.json` of fundings, containing IDs, names of recipients, postcode and municipality, year and total amount.
* `agrofunding_details.json` of fundings, containing all of the above plus a detailed description per funding with type, description and partial amounts.
* `agrofunding.csv` with the following headers: "unique_id", "funding_id", "recipient", "year", "postcode", "municipality", "total_amount", "detail_id", "type", "partial_amount"

## Data Input

### Soundness

**Scope of dataset**

The current database provides data only for 2014.

> Demnach müssen ab 2015 auch wieder natürliche Personen unter den Empfängern veröffentlicht werden. Zu veröffentlichen sind: Name, Gemeinde samt Postleitzahl, Betrag der Zahlungen aus dem EGFL, Betrag der Zahlungen aus dem ELER einschließlich der nationalen Anteile sowie Bezeichnung und Beschreibung der geförderten Maßnahmen unter Angabe des jeweiligen EU-Fonds des vorangegangenen EU- Haushaltsjahrs. Das EU-Haushaltsjahr beginnt am 16.10. eines Jahres und endet am 15.10. des Folgejahres. Die veröffentlichten Daten bleiben vom Zeitpunkt ihrer ersten Veröffentlichung zwei Jahre lang zugänglich. Ausgenommen von der namentlichen Veröffentlichungspflicht sind lediglich jene Personen, deren jährliche Zahlungen 1.250,-- Euro nicht übersteigen. In diesem Fall werden die Empfänger in kodierter Form veröffentlicht.

**Data errors found**

### Data Output

### Data model of agrofunding.json

```
{id:
  {"betrag": float,
 "gemeinde": "str",
 "id": "str",
 "jahr": "str",
 "name": "str",
 "plz": int}
}
```

### Data model of agrofunding_details.json

```
{id:
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
}
```

### Data model of

## Contributing

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

## Copyright

All content is openly licensed under the [Creative Commons Attribution 4.0 license](http://creativecommons.org/licenses/by/4.0/), unless otherwisely stated.

All sourcecode is free software: you can redistribute it and/or modify it under the terms of the MIT License.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

Visit http://opensource.org/licenses/MIT to learn more about the MIT License.
