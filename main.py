from get_formats import get_formats
from get_emails import get_emails

# get_formats()

names, emails = get_emails(company_names_from_file=False, company_names=['Snowflake'])

print(names)
print(emails)