import os
import csv
import undetected_chromedriver as uc
from time import sleep
from plyer import notification

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from get_formats import get_formats

# EDIT IF NEEDED
ROLES = ['Senior Software Engineer',
         'Project Manager', 'Product Manager', 'CEO']


def get_emails():
    names_file = open('in/names.txt', 'r')
    company_names = []
    start = False
    lines = names_file.readlines()

    if 'START\n' not in lines:
        company_names = [line.strip() for line in lines]
    else:
        for line in lines:
            line = line.strip()
            if line == 'STOP':
                break
            if start and line:
                company_names.append(line)
            if line == 'START':
                start = True
        
    formats = get_formats(company_names)

    emails = []

    driver = uc.Chrome(version_main=107)
    driver.get('https://www.linkedin.com')

    username_input = driver.find_element(By.ID, 'session_key')
    username_input.send_keys(os.getenv('LINKEDIN_USERNAME'))

    password_input = driver.find_element(By.ID, 'session_password')
    password_input.send_keys(os.getenv('LINKEDIN_PASSWORD'))

    submit_button = driver.find_element(By.XPATH,
                                        '//*[@id="main-content"]/section[1]/div/div/form/button')
    submit_button.click()

    while not driver.find_elements(By.XPATH, '//*[@id="global-nav-typeahead"]/input'):
        # notification.notify(
        #     title = 'Plexmailer',
        #     message = 'Complete LinkedIn Captcha',
        #     timeout = 10
        # )
        sleep(5)  # do captcha

    search_input = driver.find_element(By.XPATH,
                                       '//*[@id="global-nav-typeahead"]/input')
    search_input.send_keys(f'test\n')

    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="People"]'))
    )

    people_button = driver.find_element(By.XPATH, '//button[text()="People"]')
    people_button.click()

    sleep(2)

    f = open('out/emails.csv', 'w')
    writer = csv.writer(f)

    count = 0
    for company in formats:
        for role in ROLES:
            search_input.clear()
            search_input.send_keys(f'{role} {company}\n')

            for i in range(1, 4):
                name_xpath = f'/html/body/div[4]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/ul/li[{i}]/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]'

                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//button[text()="People"]'))
                    )
                except:
                    print('Timeout')
                    break

                if not driver.find_elements(By.XPATH, name_xpath):
                    print('No results found')
                    continue

                name_element = driver.find_element(By.XPATH, name_xpath)
                text = name_element.text
                name_original = tuple(text.strip().split())
                if len(name_original) > 2:
                    name_original = (name_original[0], name_original[-1])
                # if only last initial on LinkedIn
                if '.' in name_original[-1] and formats[company][2] != 'last_initial':
                    print('No last name')
                    continue

                count += 1

                name = [n.lower() for n in name_original]

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

                row = [company, role, name_original[0],
                       name_original[1], email]
                emails.append(row)
                writer.writerow(row)

    f.close()
    driver.close()
    return emails, count
