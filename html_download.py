from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

#TODO Dupplicates appear around 50 page index
# #996 destinct cars
#https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId=86&conditions%5B%5D=4&conditions%5B%5D=1&ajax=1&page=3&time=1666898830836
for brand in range(1,100):
    for page in range(1,100):
        url = 'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId={brand}&conditions%5B%5D=4&conditions%5B%5D=1&ajax=1&page={id}'                                                               
        print(url.format(id = page,brand = brand))
        driver.get(url.format(id = page,brand = brand))
        print()
        if(len(driver.page_source)<200):
            break
        time.sleep(0.1)
        file = open('DS.html', 'a', encoding="utf-8")
        file.write(driver.page_source)
   
file.close()
driver.close()