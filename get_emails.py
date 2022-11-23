from get_formats import get_formats
from splinter import Browser
from dotenv import load_dotenv
from time import sleep
from collections import defaultdict
import os

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()

ROLES = ['Senior Software Engineer', 'Project Manager', 'Product Manager']

def get_emails(company_names_from_file=True, company_names=[], w=True, format_w=True):
    formats = get_formats(from_file=company_names_from_file,
                          w=format_w, names=company_names)

    if company_names_from_file:
        company_names_file = open('in/names.txt', 'r')
        company_names = [line.strip()
                         for line in company_names_file.readlines()]

    if w:
        if os.path.exists("out/names.txt"):
            os.remove("out/names.txt")
        names_out = open('out/names.txt', 'a')

        if os.path.exists("out/emails.txt"):
            os.remove("out/emails.txt")
        emails_out = open('out/emails.txt', 'a')

    emails, names = defaultdict(list), defaultdict(list)

    with Browser('chrome', headless=False, incognito=True) as browser:
        browser.visit('https://www.linkedin.com')

        username_input = browser.find_by_id('session_key')
        username_input.fill(os.getenv('LINKEDIN_USERNAME'))

        password_input = browser.find_by_id('session_password')
        password_input.fill(os.getenv('LINKEDIN_PASSWORD'))

        submit_button = browser.find_by_xpath(
            '//*[@id="main-content"]/section[1]/div/div/form/button')
        submit_button.click()

        while not browser.is_element_present_by_xpath('//*[@id="global-nav-typeahead"]/input'):
            sleep(1) # do captcha

        count = 0
        for company in company_names:
            for role in ROLES:
                search_input = browser.find_by_xpath(
                    '//*[@id="global-nav-typeahead"]/input')
                search_input.fill(f'{role} {company}')

                # pressing enter
                actions = ActionChains(browser.driver)
                actions.send_keys(Keys.ENTER)
                actions.perform()

                for i in range(1, 4):
                    name_xpath = f'/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li[{i}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]'

                    if not browser.is_element_present_by_xpath(name_xpath):
                        continue

                    name_element = browser.find_by_xpath(name_xpath)
                    text = name_element.text
                    name = tuple(text.strip().split())
                    if len(name) > 2:
                        name = (name[0], name[-1])
                    if '.' in name[-1] and formats[company][2] != 'last_initial': # if only last initial on LinkedIn
                        continue
                    
                    count += 1

                    names_out.write(text + '\n')
                    names[company].append(name)

                    name = [n.lower() for n in name]

                    first, between, last, end = formats[company]
                    email = ''

                    if first == 'first':
                        email += name[0]
                    elif first == 'first_initial':
                        email += name[0][:1]
                    email += between
                    if last == 'last':
                        email += name[1]
                    elif last == 'last_initial':
                        email += name[1][:1]
                    email += end

                    emails_out.write(email + '\n')
                    emails[company].append((role, email))

    return dict(names), dict(emails), count
