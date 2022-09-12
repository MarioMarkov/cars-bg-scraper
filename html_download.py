from unicodedata import name
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import time

driver = webdriver.Chrome(ChromeDriverManager().install())
#brand_ids = [86]
brand_ids = [86,54,10,8,63,64,69,80,26,17,60]

for brand_id in brand_ids:
    url = "https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId={id:.2f}&conditions%5B%5D=4&conditions%5B%5D=1"
    print(url.format(id = brand_id))
    driver.get(url.format(id = brand_id))
           
    ScrollNumber = 30
    for i in range(1,ScrollNumber):
        driver.execute_script("window.scrollTo(1,1000)")
        time.sleep(3)

    file = open('DS.html', 'a', encoding="utf-8")
    file.write(driver.page_source)
   


   
file.close()
driver.close()