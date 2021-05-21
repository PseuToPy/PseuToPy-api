# Routes of the PseuToPy
The home URL for your local api will be `http://localhost:5000`.

## Route list

**GET** `/`

Display generic information about the API.

Example of returned data (JSON) :
```
{
    "pseutopyTargetGrammar": "3.9",
    "pseutopyVersion": "2.0.2",
    "pythonVersion": "3.8.6"
}
```

- `pseutopyTargetGrammar` The version of Python that is parsed by the PseuToPy package.
- `pseutopyVersion` The version of the PseuToPy package.
- `pythonVersion` The version of Python used by the PseuToPy API.

---

**POST** `/convert/:lang`

Convert a string of PseuToPy code into Pyhton code. 

The `lang` parameter is the source language code that is used to pick the correct grammar language for conversion. Accepted values are : `en` `fr`. Incorrect values will be reverted to `en`.

The body of the request must be as follows :
```
{
    "instructions": "declare my_var\nset my_var to 2\nprint(my_var)"
}
```
The PseuToPy code must join lines with `\n`.

Example of returned data (JSON) :
```
{
    "code": "my_var = None\nmy_var = 2\nprint(my_var)",
    "language": "en",
    "message": "Converted successfully!",
    "status": "SUCCESS"
}
```

- `code` The converted Python code.
- `language` The effective language chosen.
- `message` The return message which can contain the error cause.
- `status` The status of Python parsing : `SUCCESS` or `ERROR`

---

**GET** `/grammar/:lang`

Fetch the JSON grammar examples file.

The `lang` parameter is the source language code that is used to pick the correct grammar language for conversion. Accepted values are : `en` `fr`. Incorrect values will be reverted to `en`.

Example of returned data (JSON) :

```
[
    {
        "category": "Variables",
        "rules": [
            {
                "rule": "Declare a variable",
                "samples": [
                    "declare my_var"
                ]
            }
        ]
    }
]
```

## Resources
A Postman collection with 3 request examples is available on GitHub at [docs/resources/PseuToPy.postman_collection.json](https://github.com/PseuToPy/PseuToPy-api/new/rtd/docs/resources/PseuToPy.postman_collection.json "PseuToPy.postman_collection.json").
