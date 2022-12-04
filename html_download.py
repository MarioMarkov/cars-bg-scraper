from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

brands = [1,4,8,9,
10,15,16,17,19,
20,21,23,25,26,
30,31,33,34,36,37,38,
40,42,43,45,
53,54,56,57,
60,63,64,68,69,
72,73,74,75,76,77,
80,85,86,
92] 
#https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId=86&conditions%5B%5D=4&conditions%5B%5D=1&ajax=1&page=3&time=1666898830836
for brand in brands:
    for page in range(1,70):
        url = 'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId={brand}&conditions%5B%5D=4&conditions%5B%5D=1&ajax=1&page={id}'                                                               
        print(url.format(id = page,brand = brand))
        driver.get(url.format(id = page,brand = brand))
        filepath = "./html_files/brand_{brand}.html"
        if(len(driver.page_source)<200):
            break
        time.sleep(0.1)
        file = open(filepath.format(brand = brand), 'a', encoding="utf-8")
        file.write(driver.page_source)
    file.close()
   

driver.close()