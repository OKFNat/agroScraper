# agroScraper
Getting structured data out of transparenzdatenbank, which shows EU aids for Austrian agricultural businesses.

## usage

You need Python 3 for running this, it handles encoding better.

```python
python3 agroscraper.py
```

Produces two JSON-files:
* firstround.json of fundings, containing IDs, names of recipients, postcode and municipality, year and total amount.
* agrofunding.json of fundings, containing all of the above plus a detailed description per funding with type, description and partial amounts.

**Read data**

```
import json

with open("agrofunding.json", "r") as infile:
    results = json.load(infile)
```


## data model

```
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
```
