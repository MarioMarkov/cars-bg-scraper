from unicodedata import name
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

#exec(open('html_download.py').read())
driver = webdriver.Chrome(ChromeDriverManager())


headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit\
/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
headers_offer =({})

base_url = "https://www.cars.bg/"
car_offer_url = "https://www.cars.bg/offer/"
#response = get(base_url,headers=headers)
response_from_file = open('DS.html','r', encoding="utf-8")
html_soup = BeautifulSoup(response_from_file,'html.parser')


basic_info =[]
content_list = html_soup.find_all('div',attrs={'class': 'mdc-card offer-item'})



def get_ids(content_list):
    ids = [] 
    for item in content_list:
        ids.append(item.attrs['data-reference'])
    return ids
        


for item in content_list:
    basic_info.append(item.find_all('div', attrs={'class': 'mdc-card__primary-action'}))


def get_names(basic_info):
    names = [] 
    for item in basic_info:
        for i in item:
            names.append(i.find_all("h5",attrs = {"class": "observable"})[0].text.strip())
    return names

def get_prices(basic_info):
    prices = [] 
    for item in basic_info:
        for i in item:
            prices.append(i.find_all("h6",attrs = {"class": "price"})[0].text.strip())
    return prices


def get_details(basic_info):
    details = [] 
    for item in basic_info:
        for i in item:
            details.append(i.find_all("div",attrs = {"class": "mdc-typography--body1"})[0].text.strip())
    return details


data = {"id" :[],"brand": [],"model":[] , "year": [],"fuel": [], "kms":[], "price": []}

df = pd.DataFrame(data)



for item in zip(get_names(basic_info),get_prices(basic_info),get_details(basic_info),get_ids(content_list)):
    
    id = item[3]
    brand = item[0].split()[0]
    model = item[0].split()[1]
    if(item[1] == "цена по договаряне"):
        continue
    price = int(item[1].split()[0].replace(",",""))
    year = item[2].split()[0].replace(",","")
    fuel = "d" if item[2].split()[1].replace(",","") == "Дизел" else "p"
    kms = "" if len(item[2].split())<3 else int(item[2].split()[2].replace(",",""))
    row = pd.DataFrame({"id":[id],"brand": [brand],"model":[model] , "year": [year],"fuel": [fuel], "kms":[kms], "price": [price]})
    print(row)
    df = pd.concat([df, row])
    
df = df.drop_duplicates()
df.to_csv('cars-data.csv', index=False)
