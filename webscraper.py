from unicodedata import name
from bs4 import BeautifulSoup, SoupStrainer
from requests import get
import pandas as pd
from selenium import webdriver
import lxml
import cchardet
# import OS module
import os
#exec(open('html_download.py').read())



# Get the list of all files and directories
path = "./html_files"

files = os.listdir(path)



with open('all_html.html','a',encoding='UTF-8') as all_html:
    for file in files:
        with open(path + '/' + file, "r", encoding='utf-8-sig') as single_file:
            html_as_string = single_file.read()
            all_html.write(html_as_string)
        single_file.close()


all_html.close()

response_from_file = open('all_html.html','r', encoding="utf-8")

strainer = SoupStrainer('div', attrs={'class': 'mdc-card offer-item'})
# Get response from file and cook it into soup
html_soup = BeautifulSoup(response_from_file,'html.parser', parse_only = strainer)

print("Soup Preparation done")
# Array holding a div card with the cars info
basic_info =[]
content_list = html_soup.find_all('div',attrs={'class': 'mdc-card offer-item'})

# Append only divs with cars to basic_info
for item in content_list:
    basic_info.append(item.find_all('div', attrs={'class': 'mdc-card__primary-action'}))

# Get ids of car from div
def get_ids(content_list):
    ids = [] 
    for item in content_list:
        ids.append(item.attrs['data-reference'])
    return ids

# Get names of car from div
def get_names(basic_info):
    names = [] 
    for item in basic_info:
        for i in item:
            names.append(i.find_all("h5",attrs = {"class": "observable"})[0].text.strip())
    return names

# Get prices of car from div
def get_prices(basic_info):
    prices = [] 
    for item in basic_info:
        for i in item:
            prices.append(i.find_all("h6",attrs = {"class": "price"})[0].text.strip())
    return prices

# Get details of car from div
def get_details(basic_info):
    details = [] 
    for item in basic_info:
        for i in item:
            details.append(i.find_all("div",attrs = {"class": "mdc-typography--body1"})[0].text.strip())
    return details

# Define dataset structure
data = {"id" :[],"brand": [],"model":[] , "year": [],"fuel": [], "kms":[], "price": []}
df = pd.DataFrame(data)

euro_prices = 0
for item in zip(get_names(basic_info),get_prices(basic_info),get_details(basic_info),get_ids(content_list)):
    print(item)
    

    #(Opel,Astra), (20 000), (2005, diesel,200 000 km), (id)
    #('Hyundai Terracan 2.9, CDI', '7,300 лв.', '2002, Дизел, 168350 км.', '633d762fe4515d92cd0d8103')

    id = item[3]
    brand = item[0].split()[0]
    if brand == "Alfa" or brand == "Land" :
        brand = brand + item[0].split()[1]
        model = item[0].split()[2]
    else:
        brand = item[0].split()[0]
        model = item[0].split()[1]
        

    if(item[1] == "цена по договаряне"):
        continue

    # Check if price includes EUR then multiply it by 1.95
    if str.__contains__(item[1], 'EUR'):
        print("EUR")
        euro_prices = euro_prices + 1
        price = int(int(item[1].split()[0].replace(",","")) * 1.95)
    else :
        price = int(item[1].split()[0].replace(",",""))



    year = item[2].split()[0].replace(",","")
    
    
    # Determine which properties are in the [2] field 
    # if there are only two properties
    if len(item[2].split(', ')) == 2 :
        second_prop = item[2].split()[1]
        #If the second one is kms
        if str.__contains__(second_prop, 'км'):
            kms = int(item[2].split()[1].replace(",","").replace("км.",""))
            fuel = "missing"
        # if the second one is fuel 
        else:
            kms = None
            if item[2].split()[1].replace(",","") == 'Дизел': fuel = 'd'
            elif item[2].split()[1].replace(",","") == 'Газ/Бензин': fuel = 'g'
            elif item[2].split()[1].replace(",","") == 'Хибрид': fuel = 'h'
            elif item[2].split()[1].replace(",","") == 'Метан/Бензин': fuel = 'm'
            elif item[2].split()[1].replace(",","") == 'Електричество': fuel = 'e'
            else : fuel = 'p'
    # if there are 3 properties
    else:
        if item[2].split()[1].replace(",","") == 'Дизел': fuel = 'd'
        elif item[2].split()[1].replace(",","") == 'Газ/Бензин': fuel = 'g'
        elif item[2].split()[1].replace(",","") == 'Хибрид': fuel = 'h'
        elif item[2].split()[1].replace(",","") == 'Метан/Бензин': fuel = 'm'
        elif item[2].split()[1].replace(",","") == 'Електричество': fuel = 'e'
        else : fuel = 'p'
        kms = int(item[2].split()[2].replace(",","").replace(" км.",""))

    row = pd.DataFrame({"id":[id],"brand": [brand],"model":[model] , "year": [year],"fuel": [fuel], "kms":[kms], "price": [price]})
    
    df = pd.concat([df, row])
    
df = df.drop_duplicates()
df.to_csv('cars-data.csv', index=False)

print(euro_prices)