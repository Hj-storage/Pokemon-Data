import csv 
import requests
import json

print('Started')

id = []
alt_names_id = []
abc = 1

with open('Pokemon-Data/Names.json', mode='r') as file:
  data = json.load(file)
  n = 0 
  for a in data:
    id.append(a)
    alt_names_id.append([data[a][0],data[a][1],data[a][2],data[a][3],data[a][4],data[a][5]])

gen_info = {
  'generation-i': 'Kanto',
  'generation-ii': 'Jhoto',
  'generation-iii': 'Hoenn',
  'generation-iv': 'Sinnoh',
  'generation-v': 'Unova',
  'generation-vi': 'Kalos',
  'generation-vii': 'Alola',
  'generation-viii': 'Galar'
}

data = {}

for a in id:
  url = f"https://pokeapi.co/api/v2/pokemon/{a}"
  request = requests.get(url)
  if request:
    request_data = json.loads(request.text)

    
    ability = ""
    abilities = request_data["abilities"]
    for i in range(0, len(abilities)):
        ability += abilities[i]["ability"]["name"].capitalize()

        if i != len(abilities) - 1:
            ability += "\n"

    type = ""
    types = request_data["types"]
    for i in range(0, len(types)):
        type += types[i]["type"]["name"].capitalize()

        if i != len(types) - 1:
            type += "\n"

    stat = request_data['stats']
    
    info_request = requests.get(request_data['species']['url'])
    info_data = json.loads(info_request.text)

    gen = info_data['generation']['name']
    gen = gen_info.get(gen)

    genera = info_data['genera'][7]['genus'] if info_data['genera'][7] else None
    try:
      info = info_data['flavor_text_entries'][91]['flavor_text']
    except:
      info = None

      
    evolution_response = requests.get(f'https://pokeapi.co/api/v2/evolution-chain/{a}')
    evolution = None
    evolution_data = None
    if evolution_response:
      evolution_data = json.loads(evolution_response.text)
      evolution = ""
      evolution_chain = []
      chain_data = evolution_data["chain"]
      while chain_data != "":
        evolution_chain.append(chain_data["species"]["name"])
        try:
            chain_data = chain_data["evolves_to"][0]
        except:
            break
      for i in range(0, len(evolution_chain)):
        evolution += evolution_chain[i].capitalize()

        if i > len(evolution_chain) - 2:
            break
        else:
            evolution += "\n"
    else:
      pass
    
    altnames = alt_names_id[abc]
    abc+=1
    
    print(a)
    data[a] = {
      'name': request_data['name'].capitalize(),
      'ability': ability,
      'type': type,
      'info': info,
      'genera': genera,
      'gen': gen,
      'evolution': evolution,
      'alt': altnames,
      'height': request_data['height'],
      'weight': request_data['weight'],
      'shiny':  request_data['sprites']['front_shiny'],
      'normal': request_data['sprites']['front_default'],
      'stats': [stat[0]['base_stat'],stat[1]['base_stat'],stat[2]['base_stat'],stat[3]['base_stat'],stat[4]['base_stat'],stat[5]['base_stat']]
    }
    #[hp,atk,def,spatk,spdef,spd]
    #print(json.dumps(data,indent=2))
  else:
    pass
    
with open('Pokemon-Data/Pokemon.json', mode='w') as file:
  json.dump(data, file, indent=2)

print('Finished!')