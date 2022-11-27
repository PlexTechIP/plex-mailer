import undetected_chromedriver as uc
from proxy import get_free_proxies
from random import randint
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver


def get_formats(names):
    proxies = get_free_proxies()

    for name in names:
        proxy = proxies[randint(0, len(proxies) - 1)]
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % proxy)
        driver = webdriver.Chrome(options=options)

        driver.get('https://www.leadgibbon.com')

        sleep(1)

        input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/div[1]/div/div/div/div[1]/div/input')
        input.send_keys(name)

    while True:
        sleep(100)


get_formats('f')
