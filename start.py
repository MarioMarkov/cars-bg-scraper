import os
 
dir = './html_files'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))

os.remove('all_html.html')

exec(open('html_download.py').read())
exec(open('webscraper.py',encoding='utf-8-sig').read())
exec(open('download_individual.py',encoding="utf-8").read())