from pokemon_helper import *
import csv

debug = False

pokemon_https = getPokemonHTTPList("https://pokemondb.net/pokedex/all")
pokemon_dir = "pokemon"
verifyPokemonDIR(pokemon_dir)

with open('pokemon.csv', mode='w', encoding='UTF-8') as file:
	csv_file = csv.writer(file)
	
	rowLabels = initLabels()
	csv_file.writerow(rowLabels)
	
	for pokemon in pokemon_https:
		page_html = GETPokemonRequest(pokemon, pokemon_dir)
		
		#scrape data, if order changes update initLabels()
		data = []
		data.extend(scrapePokedexData(page_html, debug))
		data.extend(scrapeTrainingData(page_html, debug))
		data.extend(scrapeBreedingData(page_html, debug))
		data.extend(scrapeBaseStatsData(page_html, debug))
		data.extend(scrapeTypeDefencesData(page_html, debug))
		
		csv_file.writerow(data)
		
		print('Scraped')
