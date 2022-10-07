from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
cars = pd.read_csv('cars-data.csv')

print(cars.iloc[-1,])
for car in cars:
    url = 'https://www.cars.bg/offer/{id}'
    print(url.format(id = car.loc['id']))
    driver.get(url.format(id = car.id))
    time.sleep(1)
    print(driver.page_source)
    print('asd')
   

driver.close()