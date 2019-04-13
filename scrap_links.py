import urllib.request
import csv
import os
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

filepath='gamelinks.csv'

file_exists = os.path.isfile(filepath)
if (file_exists):
    os.remove(filepath)

metacritic_base = "http://www.metacritic.com/browse/games/release-date/available/pc/metascore?view=detailed&page="
hdr= {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux', 'win'))}

page_start = 0
page_end = 10

for i in range(page_start,page_end):
    print("Scraping Page {} - {} Pages Left".format(i, page_end - (page_start+1)))
    #
    links= []
    metacritic = metacritic_base+str(i)
    page = urllib.request.Request(metacritic, headers=hdr)
    content = urllib.request.urlopen(page).read()
    soup = BeautifulSoup(content, 'html.parser')

    right_class=soup.find_all('div', class_='browse_list_wrapper')
    for item in right_class:
        try:
            hrefs = item.find_all('a', class_="title", href=True)
            for it in hrefs:
                link = it['href']
                links.append(link)
        except: pass


    with open(filepath, 'a') as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in links:
            writer.writerow([val])
#
print("Im done.")