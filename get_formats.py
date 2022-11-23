from splinter import Browser
from time import sleep
from urllib.parse import quote
import os


def get_formats(from_file=True, w=True, names=[]):
    if from_file:
        names_file = open('in/names.txt', 'r')
        names = [line.strip() for line in names_file.readlines()]

    if w:
        if os.path.exists("out/formats.txt"):
            os.remove("out/formats.txt")
        out = open('out/formats.txt', 'a')

    with Browser('chrome', headless=True, incognito=True) as browser:
        formats = {}
        for name in names:
            res, i = None, 0
            while not res and i < 5:
                browser.visit(
                    f'https://www.google.com/search?q={quote(name)} email format RocketReach')

                try:
                    if browser.is_element_present_by_xpath('//*[@id="rso"]/div[1]/div/div/div[2]/div/span'):
                        res = browser.find_by_xpath(
                            '//*[@id="rso"]/div[1]/div/div/div[2]/div/span')
                    elif browser.is_element_present_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[2]/div/span'):
                        res = browser.find_by_xpath(
                            '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div[2]/div/span')
                    elif browser.is_element_present_by_xpath('//*[@id="rso"]/div[1]/div/block-component/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/span/span'):
                        res = browser.find_by_xpath(
                            '//*[@id="rso"]/div[1]/div/block-component/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/span/span')

                    if not res:
                        raise Exception('Need to add xpath case')

                except:
                    sleep(1)
                    i += 1

            if not res:
                raise Exception('Timed out')

            text = res.value[:res.value.index(',')]

            try:
                first = text[text.index('[') + 1:text.index(']')]
            except:
                print(text)
                return

            rest = text[text.index(']') + 1:]
            between = rest[:rest.index('[')].strip()
            last = rest[rest.index('[') + 1:rest.index(']')]
            end = rest[rest.index('@'):rest.index(')')]

            formats[name] = (first, between, last, end)
            if w:
                out.write(f'[{first}]{between}[{last}]{end}\n')

    return formats
