from unicodedata import name
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import re

driver = webdriver.Chrome(ChromeDriverManager().install())
cars = pd.read_csv('cars-data.csv')

color_name_en = {
    "син": "blue",
    "бял":"white",
    "черен":"black",
    "сив": "gray",
    "жълт":"yellow",
    "бежов":"beige",
    "бордо":"bordo",
    "бронзов":"bronze",
    "виолетов":"violet",
    "зелен":"green",
    "златен":"gold",
    "кафяв":"brown",
    "оранжев":"orange",
    "сребърен":"silver",
    "червен":"red",
    "лилав":"purple",
    "охра":"ohra",
    "перла":"perl",
    "розов":"pink",
    "хамелеон":"chameleon"
}

type_of_car_en = {
    "седан": "sedan",
    "хечбек":"hatchback",
    "комби":"combi",
    "купе": "coupe",
    "кабрио":"cabrio",
    "джип":"jeep",
    "пикап":"pickup",
    "ван" :"van"
}

for index, car in cars.iterrows():
    url = 'https://www.cars.bg/offer/{id}'
    driver.get(url.format(id = car.id))
    #file = open('individual.html', 'a', encoding="utf-8")
    
    #Make beutiful soup from this 
    #strainer = SoupStrainer('div', attrs={'class': 'text-copy'})
    html_soup = BeautifulSoup(driver.page_source,'html.parser')

    #Extract a div with text copy and wanted data
    details = html_soup.find_all('div',attrs={'class':'text-copy'})
    if len(details) == 0:
        continue

    #Add the data to the car with the car.id from cars-data.csv
    cars.at[index,'transmission'] = 1 if  'автоматични скорости' in details[1].text.lower() else 0
    cars.at[index,'2door'] = 1 if  '2/3 врати' in details[1].text else 0 

    # Find color of car
    matches_color = [word if word in details[1].text.lower().strip()  else None for word in color_name_en.keys()]
    
    # Map bulgarian names to english names if there is a match else None
    if any(matches_color):
        color = None
        for item in matches_color:
            if item is not None: 
                color = item
                break

        cars.at[index,'color'] = color_name_en[color]
    else:
        cars.at[index,'color'] = None 

    # Find type of car
    matches_type = [  word if word in details[1].text.lower().strip()  else None  for word in type_of_car_en.keys()]

    # Map bulgarian names to english names if there is a match else None
    if any(matches_type):
        type = None
        for item in matches_type:
            if item is not None: 
                type = item
                break
        cars.at[index,'type'] = type_of_car_en[type]
    else:
        cars.at[index,'type'] = None 

    # Find displacement of engine
    dis = details[1].text.lower().find("см3")
    dis_value = details[1].text.lower()[dis-4:dis]
    cars.at[index,'displacement'] = dis_value if dis != -1  else None  

    # Find horsepower of engine
    hp = details[1].text.lower().find("к.с.")
    hp_value = details[1].text.lower()[hp-3:hp]
    cars.at[index,'hp'] = hp_value.strip().strip(',') if hp != -1  else None  

    # Find euro rating
    euro = details[1].text.lower().find("euro")
    euro_value = details[1].text.lower()[euro+4:euro+6]
    cars.at[index,'euro'] = euro_value.strip() if euro != -1  else None  


    print(cars.loc[cars['id'] == car.id])

cars = cars[['id','brand','model','year','fuel','kms','transmission','2door','color','type','displacement','hp','euro','price']] 
cars.to_csv('cars-data3.csv', index=False)
driver.close()  

