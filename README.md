# Plexmailer

This software automates the client sourcing software

## 1. Prerequisites

In order to run Plexmailer

## 2. Installation

In a terminal window, run:

`git clone https://github.com/shamith09/plexmailer.git`

`cd plexmailer`

`pip install -r requirements.txt`

## 3. Environment Setup

Create a `.env` file by running:

`touch .env`

In this file, add the following information:

```
LINKEDIN_USERNAME=<your_linkedin_username>
LINKEDIN_PASSWORD=<your_linkedin_password>
GOOGLE_USERNAME=<your_gmail_username>
GOOGLE_PASSWORD=<your_gmail_password>
SPREADSHEET_ID=<google_sheet_id>
```

In order to get the `SPREADSHEET_ID` field, go to whichever Google Sheet you want to populate (e.g. the master client sourcing spreadsheet) and look at the URL.

The URL will come in this format:

`https://docs.google.com/spreadsheets/d/<google_sheet_id>/...`

Copy the ID from the URL as shown above and paste into the `.env` file.


## 4. Additional configuration (optional)

On line 17 of `main.py`, input the date that you want your emails to be sent out in the format specified in the comment. 

On line 13 of `get_emails.py`, input the roles that you want to search for as an array of strings. (ex. `['Senior Software Engineer', 'Project Manager', 'Product Manager', 'CEO']`)

## 5. Execution

Before running the program, in `in/names.txt`, type all of the company names that you want emails for, separated by newlines.

Example:

```
Google
Meta
Apple
Netflix
```

In a terminal window, run:

`python3 main.py`

If any email formats are unable to be found, they will be added to `out/not_found.txt`.

If there are errors, `out/formats.csv` and `out/emails.csv` will contain the formats and emails found until the error in spreadsheet format.

## Epilogue

If you are experiencing any issues, message me (Shamith) and I probably won't be able to help.

If you have any suggestions or want to update the code, submit a pull request and describe what you want to change.