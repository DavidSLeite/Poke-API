import json
import requests
import random
import pandas as pd

def getPokemon(codPokemon: int):
    """ Consulta pokeapi e retorna atributos do pokemon """
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{codPokemon}"
        response = requests.get(url)
        content = response.content
        content_dict = json.loads(content)

        types_list = []
        for name in content_dict["types"]:
            types_list.append(str.title(name["type"]["name"]))
    
        pokemon = {
            "codigo_pokedex" : codPokemon,
            "nome_pokemon" : str.title(content_dict["name"]),
            "naturezas" : types_list,
            "imagem": content_dict["sprites"]["front_default"]
        }

        return pokemon
    except:
        raise Exception("Pokemon não encontrado!!!")

def genPokemon():
    """ Gera pokemon de forma aleatória """
    x = random.randint(1,905)
    charPokemon = getPokemon(x)
    return charPokemon

def genTeam():
    """ Retorna um time de seis pokemons de forma aleatória """
    team = []

    for i in range(6):
        pokemon = genPokemon()
        team.append(pokemon)

    return team

print("Criando time!!!")

time1 = genTeam()
time2 = genTeam()

# Gerando arquivo CSV
dftime1 = pd.json_normalize(time1)
dftime1.to_csv(r".\extracao_json\time1.csv", sep=";", index=True)

dftime2 = pd.json_normalize(time2)
dftime2.to_csv(r".\extracao_json\time2.csv", sep=";", index=True)

# Gerando arquivo Json
with open(r".\extracao_json\time1.json", "w") as f:
    f.write(json.dumps(time1, indent = 4))

with open(r".\extracao_json\time2.json", "w") as f:
    f.write(json.dumps(time2, indent = 4))

print("Time criado!!!")