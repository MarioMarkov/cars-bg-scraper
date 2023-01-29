import bs4
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup
from bs4 import SoupStrainer as strainer
import csv
import pandas as pd


data = pd.DataFrame({"id" :[],"brand": [],"model":[] , "year": [],
"fuel": [], "kms":[], "price": [],"transmission":[]})

# creates a SoupStrainer object that is used to
# generate minimal HTML in each parsed document
only_item_cells = strainer("div", attrs={"class": "mdc-card offer-item"})


page_cells = []

page_html = open('/content/html_bs4_test.html','r', encoding="utf-8")
page_soup = soup(page_html, 'html.parser', parse_only=only_item_cells)
page_soup_list = list(page_soup)
page_cells.append(page_soup_list)

with open('graphics_cards.csv', mode='w', newline='') as graphics_cards_file:
    file_writer = csv.writer(graphics_cards_file)
    file_writer.writerow(['id', 'brand', 'model', 'year',"fuel", "kms", "price","transmission"])
    for item in page_cells:
      for html in item:
        id = html.attrs['data-reference']
        print(id)
        brand = html.find_all("h5",
                                attrs = {"class": "observable"})[0].text.strip()
        price = html.find_all("h6",attrs = {"class": "price"})[0].text.strip()
                  
        file_writer.writerow([id, brand, price])