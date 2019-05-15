from lxml import html, etree #etree needed for debug/printing htmlelement
import requests
import time
import pickle

import sys #using exit() for debugging

import os #needed for file stuff

from pathlib import Path

debug = False

print("Checking pokemon.http...", end='')

pokemon_http_file = Path('pokemon.http')

if pokemon_http_file.is_file():
	pokemon_https = pickle.load(open(pokemon_http_file, 'rb'))
	print('Loaded')
else:
	#Pokemondb.net Pokedex Website
	url = "https://pokemondb.net/pokedex/all"
	
	#Create response object from URL
	page = requests.get(url)
	
	#ASSERT page is an html file

	#Create html object from raw page contents
	page_html = html.fromstring(page.content)

	#Create a list of paths to each pokemon
	pokemon_names = page_html.xpath('//a[@class="ent-name"]/@href')

	#Remove Duplicates
#	pokemon_https = list(dict.fromkeys(pokemon_https))

	#Remove Duplicates including original and remove "/pokedex/" from name
	pokemon_https = [name[9:] for name in pokemon_names if pokemon_names.count(name) == 1]

	#Write pokemon_https to pokemon_http_file
	pickle.dump(pokemon_https, open(pokemon_http_file, 'wb'))
	print('Downloaded and Saved')

#print(pokemon_https)
#sys.exit()

print("Checking pokemon folder...", end='')

pokemon_dir = "pokemon"
if not os.path.isdir(pokemon_dir):
	os.mkdir(pokemon_dir)
	print('Created')
else:
	print('Exists')


#sys.exit()

pokemon_no = 0
pokemon = pokemon_https[pokemon_no]
pokemon_file = Path(pokemon_dir + '/' + pokemon)

print(f'{pokemon}...', end='')

if pokemon_file.is_file():
	page = pickle.load(open(pokemon_file, 'rb'))
	print("Loaded...", end='')
else:
	#be nice and dont spam the site
	time.sleep(1)
	page = requests.get("https://pokemondb.net/pokedex/" + pokemon)
	pickle.dump(page, open(pokemon_file, 'wb'))
	print("Downloaded...", end='')

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

if debug:
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

if debug:
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

if debug:
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

if debug:
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

#Type defenses
nor      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[1]/@title')
nor.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[1]/text()'))
if len(nor) == 1: nor.extend('0')
fir      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[2]/@title')
fir.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[2]/text()'))
if len(fir) == 1: fir.extend('0')
wat      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[3]/@title')
wat.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[3]/text()'))
if len(wat) == 1: wat.extend('0')
ele      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[4]/@title')
ele.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[4]/text()'))
if len(ele) == 1: ele.extend('0')
gra      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[5]/@title')
gra.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[5]/text()'))
if len(gra) == 1: gra.extend('0')
ice      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[6]/@title')
ice.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[6]/text()'))
if len(ice) == 1: ice.extend('0')
fig      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[7]/@title')
fig.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[7]/text()'))
if len(fig) == 1: fig.extend('0')
poi      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[8]/@title')
poi.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[8]/text()'))
if len(poi) == 1: poi.extend('0')
gro      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[9]/@title')
gro.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[1]/tr[2]/td[9]/text()'))
if len(gro) == 1: gro.extend('0')

if debug:
	print(f'nor: {nor}')
	print(f'fir: {fir}')
	print(f'wat: {wat}')
	print(f'ele: {ele}')
	print(f'gra: {gra}')
	print(f'ice: {ice}')
	print(f'fig: {fig}')
	print(f'poi: {poi}')
	print(f'gro: {gro}')

fly      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[1]/@title')
fly.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[1]/text()'))
if len(fly) == 1: fly.extend('0')
psy      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[2]/@title')
psy.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[2]/text()'))
if len(psy) == 1: psy.extend('0')
bug      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[3]/@title')
bug.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[3]/text()'))
if len(bug) == 1: bug.extend('0')
roc      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[4]/@title')
roc.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[4]/text()'))
if len(roc) == 1: roc.extend('0')
gho      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[5]/@title')
gho.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[5]/text()'))
if len(gho) == 1: gho.extend('0')
dra      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[6]/@title')
dra.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[6]/text()'))
if len(dra) == 1: dra.extend('0')
dar      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[7]/@title')
dar.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[7]/text()'))
if len(dar) == 1: dar.extend('0')
ste      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[8]/@title')
ste.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[8]/text()'))
if len(ste) == 1: ste.extend('0')
fai      = page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[9]/@title')
fai.extend(page_html.xpath('(//table[@class="type-table type-table-pokedex"])[2]/tr[2]/td[9]/text()'))
if len(fai) == 1: fai.extend('0')

if debug:
	print(f'fly: {fly}')
	print(f'psy: {psy}')
	print(f'bug: {bug}')
	print(f'roc: {roc}')
	print(f'gho: {gho}')
	print(f'dra: {dra}')
	print(f'dar: {dar}')
	print(f'ste: {ste}')
	print(f'fai: {fai}')

#Pokedex entries


#print(f': {}')

print('Scraped')