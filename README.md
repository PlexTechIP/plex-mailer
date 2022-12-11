# Plexmailer

This software automates the client sourcing process for PlexTech by webscraping email formats from Google and emails from LinkedIn.

The program may find some invalid emails, so be sure to hover over all the emails in the spreadsheet and filter out the ones with the default profile picture.

You also may need to complete some captchas as `get_formats.py` runs, so keep an eye on the Chrome tab.

**Read through this whole README or else you might not get the right results.**

There are a few things that you need to configure before running the program, so do not skim through the instructions.

## 1. Prerequisites

In order to run Plexmailer, you need to have Python 3 installed.

## 2. Installation

In a terminal window, run:

`git clone https://github.com/shamith09/plexmailer.git`

`cd plexmailer`

`pip install -r requirements.txt`

## 3. Environment Setup 
Create two directories, `in` and `out`, by running:

`mkdir in`

`mkdir out`

Create a `.env` file by running:

`touch .env`

In this file, add the following information:

```
LINKEDIN_USERNAME=<your_linkedin_username>
LINKEDIN_PASSWORD=<your_linkedin_password>
GOOGLE_USERNAME=<your_gmail_username>
GOOGLE_PASSWORD=<your_gmail_password>
SPREADSHEET_ID=<google_sheet_id>
SHEET_NAME=<google_sheet_name>
```

I recommend using your personal GMail account so that you don't have to log in through CalNet. This login is just so that we can bypass CAPTCHA, NOT for the Google Sheets API.

In order to get the `SPREADSHEET_ID` field, go to whichever Google Sheet you want to populate (e.g. the master client sourcing spreadsheet) and look at the URL.

The URL will come in this format:

`https://docs.google.com/spreadsheets/d/<google_sheet_id>/...`

Copy the ID from the URL as shown above and paste into the `.env` file.

For the `SHEET_NAME` field, input the name of the specific *sheet* that you're on, not the name of the entire document.

For example, if you're using the master spreadsheet, `SHEET_NAME` will be the PM's name, NOT `[MASTER] PlexTech Client Sourcing`.

### IMPORTANT:

I recommend making a copy of the master client sourcing spreadsheet and using your copy with this program because if others are writing to the master spreadsheet, it may cause unexpected behavior.

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

The first time you run this, it should open a browser window asking you to sign into Google. Use whichever account your Google sheet is owned by.

If any email formats are unable to be found, they will be added to `out/not_found.txt`.

If there are errors, `out/formats.csv` and `out/emails.csv` will contain the formats and emails found until the error in spreadsheet format.

## Epilogue

If you are experiencing any issues, message me (Shamith) and I probably won't be able to help.

If you have any suggestions or want to update the code, submit a pull request and describe what you want to change.