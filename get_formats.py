import os
import csv
import undetected_chromedriver as uc
from time import sleep
from urllib.parse import quote

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def get_formats(names):
    driver = uc.Chrome(version_main=107)

    driver.get('https://accounts.google.com')
    username_input = driver.find_element(By.ID, 'identifierId')
    username_input.send_keys(os.getenv('GOOGLE_USERNAME'))

    next_button = driver.find_element(
        By.XPATH, '//*[@id="identifierNext"]/div/button/span')
    next_button.click()

    while True:
        try:
            password_input = driver.find_element(
                By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
            password_input.send_keys(os.getenv('GOOGLE_PASSWORD'))
            break
        except:
            pass

    next_button = driver.find_element(
        By.XPATH, '//*[@id="passwordNext"]/div/button/span')
    next_button.click()

    f = open('out/formats.csv', 'w')
    writer = csv.writer(f)

    formats = {}
    not_found = []
    for name in names:
        res, i = None, 0
        driver.get(
            f'https://www.google.com/search?q={quote(name)} email format RocketReach')

        j = 0
        while 'sorry' in driver.current_url:
            if j > 10:
                print('Complete Google captcha')
                sleep(10)
            else:
                sleep(1)
                print(f'Google captcha try #{j}', end='\r')
                actions = ActionChains(driver)
                actions.send_keys(Keys.TAB)
                actions.send_keys(Keys.SPACE)
                actions.perform()
                j += 1

        while not res and i < 5:
            try:
                if driver.find_elements(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[2]/div/span'):
                    res = driver.find_element(By.XPATH,
                                              '//*[@id="rso"]/div[1]/div/div/div[2]/div/span')
                elif driver.find_elements(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[2]/div/span'):
                    res = driver.find_element(By.XPATH,
                                              '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[2]/div/span')
                elif driver.find_elements(By.XPATH, '//*[@id="rso"]/div[1]/div/block-component/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/span/span'):
                    res = driver.find_element(By.XPATH,
                                              '//*[@id="rso"]/div[1]/div/block-component/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/span/span')

                if not res:
                    raise Exception('Need to add xpath case')

            except:
                sleep(1)
                i += 1

        if not res:
            print("Timeout error: " + name)
            not_found.append(name)
            continue

        text = None
        try:
            if 'formats:' in res.text:
                text = res.text[res.text.index(
                    '.') + 2:res.text.index('(') - 1]
                try:
                    first = text[:text.index(' ')]
                    rest = text[text.index(' ') + 1:]
                    between = rest[rest.index(
                        "'") + 1:rest.index('l') - 2].strip()
                    last = rest[rest.index('l'):rest.index('@')]
                    end = text[text.index('@'):]
                except:
                    first = text[:text.index('@')]
                    between = last = ''
                    end = text[text.index('@'):]

            else:
                text = res.text[:res.text.index(')') + 1]
                first = text[text.index('[') + 1:text.index(']')]
                rest = text[text.index(']') + 1:]
                try:
                    between = rest[:rest.index('[')].strip()
                    last = rest[rest.index('[') + 1:rest.index(']')]
                except:
                    between = last = ''
                end = rest[rest.index('@'):rest.index(')')]
        except:
            if text is not None:
                print("Formatting error: " + text)
            else:
                print("Formatting error: " + name)
            not_found.append(name)
            continue

        formats[name] = (first, between, last, end)
        writer.writerow([name, first, between, last, end])

    with open('out/not_found.txt', 'w') as f:
        for name in not_found:
            f.write(name + '\n')

    f.close()
    driver.close()
    return formats
