from lxml import html
import requests
import time

#Pokemondb.net Pokedex Website
url = "https://pokemondb.net/pokedex/all"

#Create response object from URL
page = requests.get(url)

#ASSERT page is an html file

#Create html object from raw page contents
page_html = html.fromstring(page.content)

#Create a list of paths to each pokemon
pokemon_names = page_html.xpath('//a[@class="ent-name"]/@href')

#Prepend all entries with https://pokemondb.net
pokemon_https = ["https://pokemondb.net{0}".format(name) for name in pokemon_names]

#Remove Duplicates
pokemon_https = list(dict.fromkeys(pokemon_https))

#be nice and dont spam the site
time.sleep(1)

pokemon_no = 100

page = requests.get(pokemon_https[pokemon_no])

page_html = html.fromstring(page.content)

#Pokedex data
name        = page_html.xpath('//main/h1/text()')
national_no = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[1]/td/strong/text()')
types       = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[2]/td/a/text()')
species     = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[3]/td/text()')
height      = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[4]/td/text()')
height[0]   = height[0].replace(u'\xa0', ' ')
weight      = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[5]/td/text()')
weight[0]   = weight[0].replace(u'\xa0', ' ')
abilities   = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[6]/td/span/a/text()')
abilities_h = page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[6]/td/small/a/text()')
local_no    = dict(zip(page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[7]/td/small/text()'), page_html.xpath('(//table[@class="vitals-table"])[1]/tbody/tr[7]/td/text()')))

print(f'name: {name}')
print(f'national no: {national_no}')
print(f'type: {types}')
print(f'species: {species}')
print(f'height: {height}')
print(f'weight: {weight}')
print(f'abilities: {abilities}')
print(f'abilities_h: {abilities_h}')
print(f'local no: {local_no}')
