from splinter import Browser
from time import sleep
import os

def get_formats(from_file=True, w=True, names=[]):
    if from_file:
        names_file = open('in/names.txt', 'r')
        names = [line.strip() for line in names_file.readlines()]

    if w:
        if os.path.exists("out/formats.txt"):
            os.remove("out/formats.txt")
        else:
            print("The file does not exist")
        out = open('out/formats.txt', 'a')

    with Browser('chrome', headless=True, incognito=True) as browser:
        formats = {}
        for name in names:
            res = None
            while not res:
                try:
                    browser.visit(f'https://www.google.com/search?q={name} email format')

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
            
            text = res.value[:res.value.index(',')]

            first = text[text.index('['):text.index(']') + 1]
            rest = text[text.index(']') + 1:]
            between = rest[:rest.index('[')].strip()
            last = rest[rest.index('['):rest.index(']') + 1]
            end = rest[rest.index('@'):rest.index(')')]

            format = first + between + last + end
            formats[name] = format
            if w:
                out.write(format + '\n')

    return res
