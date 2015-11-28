# agroscraper
Getting structured data out of transparenzdatenbank, which shows EU aids for Austrian agricultural businesses.



## data model


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