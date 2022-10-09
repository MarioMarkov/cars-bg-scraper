from unicodedata import name
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())
cars = pd.read_csv('cars-data.csv')


for index, car in cars.iterrows():
    url = 'https://www.cars.bg/offer/{id}'
    driver.get(url.format(id = car.id))
    #file = open('individual.html', 'a', encoding="utf-8")
    
    #Make beutiful soup from this 
    html_soup = BeautifulSoup(driver.page_source,'html.parser')

    #Extract a div with text copy and wanted data
    details = html_soup.find_all('div',attrs={'class':'text-copy'})
    if len(details) == 0:
        continue
    print(car.id)

    #Add the data to the car with the car.id from cars-data.csv
    cars.at[index,'transmission'] = 1 if  'Автоматични скорости' in details[1].text else 0 
   
    print(cars.loc[cars['id'] == car.id])

cars.to_csv('cars-data.csv', index=False)
driver.close()  