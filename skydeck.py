import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from urllib.parse import quote

INDUSTRY = 'BioTech/MedTech'

options = uc.ChromeOptions()
options.add_argument('--headless')
driver = uc.Chrome(options=options)

driver.get(f'https://skydeck.berkeley.edu/portfolio/?custom-main-industry-select={quote(INDUSTRY)}')

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'company-block-item'))
)

elements = driver.find_elements(By.CLASS_NAME, 'company-block-item')

with open('in/names.txt', 'w') as f:
    for element in elements:
        if '...' not in element.text:
            f.write(element.text[:element.text.index('\n')] + '\n')

