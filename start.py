import os

# Make html_files folder if there is not any
# else clean it
if not os.path.isdir('./html_files'):
    os.mkdir('./html_files')
else :
    dir = './html_files'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

if os.path.isfile('all_html.html'):
    os.remove('all_html.html')

exec(open('html_download.py').read())
exec(open('webscraper.py',encoding='utf-8-sig').read())
exec(open('download_individual.py',encoding="utf-8").read())