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

pokemon_no = 0

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

#Training
EV_yield        = page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[1]/td/text()')
catch_rate      = page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[2]/td/text()')
catch_rate.extend(page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[2]/td/small/text()'))
base_friendship = page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[3]/td/text()')
base_friendship.extend(page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[3]/td/small/text()'))
base_exp        = page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[4]/td/text()')
growth_rate     = page_html.xpath('(//table[@class="vitals-table"])[2]/tbody/tr[5]/td/text()')

print(f'EV_yield: {EV_yield}')
print(f'catch_rate: {catch_rate}')
print(f'base_friendship: {base_friendship}')
print(f'base_exp: {base_exp}')
print(f'growth_rate: {growth_rate}')

#Breeding
egg_groups = page_html.xpath('(//table[@class="vitals-table"])[3]/tbody/tr[1]/td/a/text()')
gender     = page_html.xpath('(//table[@class="vitals-table"])[3]/tbody/tr[2]/td/span/text()')
egg_cycles = page_html.xpath('(//table[@class="vitals-table"])[3]/tbody/tr[3]/td/text()')
del egg_cycles[-1]
egg_cycles.extend(page_html.xpath('(//table[@class="vitals-table"])[3]/tbody/tr[3]/td/small/text()'))

print(f'egg_groups: {egg_groups}')
print(f'gender: {gender}')
print(f'egg_cycles: {egg_cycles}')

#Base stats
hp             = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[1]/td[1]/text()')
hp_min         = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[1]/td[3]/text()')
hp_max         = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[1]/td[4]/text()')
attack         = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[2]/td[1]/text()')
attack_min     = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[2]/td[3]/text()')
attack_max     = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[2]/td[4]/text()')
defense        = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[3]/td[1]/text()')
defense_min    = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[3]/td[3]/text()')
defense_max    = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[3]/td[4]/text()')
sp_attack      = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[4]/td[1]/text()')
sp_attack_min  = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[4]/td[3]/text()')
sp_attack_max  = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[4]/td[4]/text()')
sp_defense     = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[5]/td[1]/text()')
sp_defense_min = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[5]/td[3]/text()')
sp_defense_max = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[5]/td[4]/text()')
speed          = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[6]/td[1]/text()')
speed_min      = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[6]/td[3]/text()')
speed_max      = page_html.xpath('(//table[@class="vitals-table"])[4]/tbody/tr[6]/td[4]/text()')
base_total     = page_html.xpath('(//table[@class="vitals-table"])[4]/tfoot/tr/td/b/text()')

print(f'hp: {hp}')
print(f'hp_min: {hp_min}')
print(f'hp_max: {hp_max}')
print(f'attack: {attack}')
print(f'attack_min: {attack_min}')
print(f'attack_max: {attack_max}')
print(f'defense: {defense}')
print(f'defense_min: {defense_min}')
print(f'defense_max: {defense_max}')
print(f'sp_attack: {sp_attack}')
print(f'sp_attack_min: {sp_attack_min}')
print(f'sp_attack_max: {sp_attack_max}')
print(f'sp_defense: {sp_defense}')
print(f'sp_defense_min: {sp_defense_min}')
print(f'sp_defense_max: {sp_defense_max}')
print(f'speed: {speed}')
print(f'speed_min: {speed_min}')
print(f'speed_max: {speed_max}')
print(f'base_total: {base_total}')
#print(f': {}')
