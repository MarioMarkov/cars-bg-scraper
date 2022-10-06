from unicodedata import name
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
#brand_ids = [86,54,10,8,63,64,69,80,26,17,60,36,15,19]
#print()
for page in range(1,150):
    url = 'https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&conditions%5B0%5D=4&conditions%5B1%5D=1&ajax=1&page={id}'                                                               
    print(url.format(id = page))
    driver.get(url.format(id = page))
    time.sleep(1)
    file = open('DS.html', 'a', encoding="utf-8")
    file.write(driver.page_source)
# for brand_id in brand_ids:
#     url = "https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId={id:.2f}&conditions%5B%5D=4&conditions%5B%5D=1"
#     print(url.format(id = brand_id))
#     driver.get(url.format(id = brand_id))
           
#     ScrollNumber = 50
#     for i in range(1,ScrollNumber):
#         driver.execute_script("window.scrollTo(1,5000)")
#         time.sleep(1)

#     file = open('DS.html', 'a', encoding="utf-8")
#     file.write(driver.page_source)
   


   
file.close()
driver.close()