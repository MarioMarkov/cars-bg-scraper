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
    "kупе":"coupe",
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

    all_details = details[1].text.lower().split(",")
    all_details = [i.strip() for i in all_details]
    print(all_details)


    #Add the data to the car with the car.id from cars-data.csv
    cars.at[index,'transmission'] = 1 if  'автоматични скорости' in all_details else 0
    cars.at[index,'2door'] = 1 if  '2/3 врати' in all_details else 0 

    # Find color of car
    color = None
    for bg_color in color_name_en.keys():
        found = [i for i in all_details if bg_color in i]
        if found: 
            color = bg_color
            break
        
    # Map bulgarian names to english names if there is a match else None
    if color:
        cars.at[index,'color'] = color_name_en[color]
    else:
        cars.at[index,'color'] = None 


    # Find type of car
    type = None
    for bg_type in type_of_car_en.keys():
        found = bg_type in all_details
        if found: 
            type = bg_type
            break

    # Map bulgarian names to english names if there is a match else None
    if type:
        cars.at[index,'type'] = type_of_car_en[type]
    else:
        cars.at[index,'type'] = None 

    # Find displacement of engine
    dis_value = [i for i in all_details if "см3" in i]
    cars.at[index,'displacement'] = dis_value[0].replace("см3", "").strip().strip(',') if dis_value else None  

    # Find horsepower of engine
    hp_value = [i for i in all_details if "к.с." in i]
    cars.at[index,'hp'] = hp_value[0].replace("к.с.", "").strip().strip(',') if hp_value else None  

    # Find euro rating
    euro_value = [i for i in all_details if "euro" in i]
    cars.at[index,'euro'] = euro_value[0].replace("euro", "").strip().strip(',') if euro_value else None  

    print(cars.loc[cars['id'] == car.id])

cars = cars[['id','brand','model','year','fuel','kms','transmission','2door','color','type','displacement','hp','euro','price']] 
cars.to_csv('cars-data3.csv', index=False)
driver.close()  

