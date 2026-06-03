## About
This is a python implementation of an llm text API, built to run models from huggingface using Python's transformers pipeline. As it is configured the API uses the 135M-Instruct version of the SmolLM v2 model.
The purpose of this text based LLM API is to allow the user to upload a CSV data file, analyze it through the Python Pandas library, then to allow the user to ask the AI about the data in cleartext.

## How To Run
Install the API by running the following commands in its root directory:
```
uv sync
```

Then start the program by running the following: (The first run may take a while, as you will be downloading the configured LLM model)
```
uv run uvicorn app.main:app --reload
```

To test the api with swagger go to the following adress:
```
localhost:8000/docs
```
Or check the following to be provided a list of endpoints:
```
localhost:8000
```

To run the tests run the following:
```
uv run pytest app/tests/ -v
```

The API also expects an .env file in the root directory of the project, with the following variable:
```
APP_NAME=String
```
with String representing whatever you want.
Although this file is not a requirement.

## Assumptions
This API is intended to be run locally, and makes the assumption that you will want you chat history with the AI read for any future prompts.

The API is also configured to provide prompt data in the structure desired by SmolLM, meaning some minor adjustments may be needed, even between different models.

This API does also make some data type assumptions, which could be problematic in a real world scenario, such as that valid CSV files provided also has valid data fields, although it makes checks to prevent providing the model with non-csv files, a corrupted CSV file could protentially still cause issues.

The API is intended to be easily extendible, with additional routes added to api.py