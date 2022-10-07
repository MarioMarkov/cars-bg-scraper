from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

#TODO Dupplicates appear around 50 page index
# #996 destinct cars
for page in range(1,50):
    url = 'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&conditions%5B0%5D=4&conditions%5B1%5D=1&ajax=1&page={id}'                                                               
    print(url.format(id = page))
    driver.get(url.format(id = page))
    time.sleep(1)
    file = open('DS.html', 'a', encoding="utf-8")
    file.write(driver.page_source)
   
file.close()
driver.close()