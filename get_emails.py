from get_formats import get_formats
from splinter import Browser
from os import getenv
from dotenv import load_dotenv
from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()


def get_emails(company_names_from_file=True, company_names=[]):
    # formats = get_formats(from_file=company_names_from_file, w=False, names=company_names)
    if company_names_from_file:
        company_names_file = open('in/names.txt', 'r')
        company_names = [line.strip()
                         for line in company_names_file.readlines()]

    with Browser('chrome', headless=False, incognito=True) as browser:
        browser.visit('https://www.linkedin.com')

        username_input = browser.find_by_id('session_key')
        username_input.fill(getenv('LINKEDIN_USERNAME'))

        password_input = browser.find_by_id('session_password')
        password_input.fill(getenv('LINKEDIN_PASSWORD'))

        submit_button = browser.find_by_xpath(
            '//*[@id="main-content"]/section[1]/div/div/form/button')
        submit_button.click()

        def get_name(company, role, index):
            search_input = browser.find_by_xpath(
                '//*[@id="global-nav-typeahead"]/input')
            search_input.fill(f'{role} {company}')

            # pressing enter
            actions = ActionChains(browser.driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()

            name_xpath = f'/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li[{index}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]'

            if not browser.is_element_present_by_xpath(name_xpath):
                return

            name_element = browser.find_by_xpath(name_xpath)
            name = name_element.text
            print(name)

        for company in company_names:
            for i in range(1, 4):
                get_name(company, 'Senior Software Engineer', i)
                # get_name(company, 'Project Manager')
                # get_name(company, 'Product Manager')

        sleep(3)


get_emails()
