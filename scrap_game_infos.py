import urllib.request
import csv
import os
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import json
import time

import pprint
pp = pprint.PrettyPrinter(width=80, compact=True)


filepath='gamelinks.csv'

file_exists = os.path.isfile(filepath)
if (file_exists is False):
    print("Wrong filepath.!")

metacritic_base = "http://www.metacritic.com"
hdr= {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux', 'win'))}


links = []
with open(filepath, 'r') as input:
    reader = csv.reader(input)
    for r in reader:
        links.append(r[0])


count = 1
for link in links:
    print("Scraping Game {} - {} Games Left".format(count, len(links)-count))
    #
    metacritic = metacritic_base+link
    page = urllib.request.Request(metacritic, headers=hdr)
    content = urllib.request.urlopen(page).read()
    soup = BeautifulSoup(content, 'html.parser')

    data = json.loads(soup.find('script', type='application/ld+json').text)

    user_rating = soup.find('div', class_="user").text
    rating_count = data['aggregateRating']['ratingCount']
    rating_value = data['aggregateRating']['ratingValue']
    date = data['datePublished']
    genre_list = data['genre']
    name = data['name']

    publishers_list = []
    publishers = data['publisher']
    for pb in publishers:
        publishers_list.append(pb['name'])


    dic = {}
    dic["Name"] = name
    dic["Release Date"] = date
    dic["Genre"] = genre_list
    dic["Meta Score"] = rating_value
    dic["Total Ratings"] = rating_count
    dic["Publisher"] = publishers_list
    dic["User Rating"] = user_rating

    pp.pprint(dic)

    #
    count += 1
    time.sleep(5)