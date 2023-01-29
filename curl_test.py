import os 
import time

#TODO Dupplicates appear around 50 page index
# #996 destinct cars
#https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId=86&conditions%5B%5D=4&conditions%5B%5D=1&ajax=1&page=3&time=1666898830836

brands = [1,86]
for brand in brands:
    for page in range(1,50):
        command = 'cmd /c "curl --output file_test.html --silent https://www.cars.bg/carslist.php?subm=1&add_search=1&typeoffer=1&brandId={brand}&conditions%5B%5D=4&conditions%5B%5D=1&ajax=1&page={page}"'                                                               
        print(page,brand )

        os.system(command.format(page = page,brand = brand))
        filepath = "./html_files/brand_{brand}.html"
        # open both files
        with open('file_test.html','r',encoding='UTF-8') as firstfile, open(filepath.format(brand = brand),'a',encoding='UTF-8') as secondfile:
            # read content from first file
            file_stat = os.stat('file_test.html')
            if(file_stat.st_size<500):
                break
            for line in firstfile:
             # append content to second file
             secondfile.write(line)
        firstfile.close()

secondfile.close()        




