import os
import json
import requests
import random
import pandas as pd


class PokemonAPI:
    def __init__(
        self,
        team_name: str,
        number_characters: int,
        path: str,
        type_file: str
    ) -> None:
        self.__team_name = team_name
        self.__number_characters = number_characters
        self.__path = path
        self.__type_file = type_file

    def get_pokemon(self, codPokemon: int) -> dict:
        """Consulta pokeapi e retorna atributos do pokemon"""
        try:
            url = f"https://pokeapi.co/api/v2/pokemon/{codPokemon}"
            response = requests.get(url)
            content = response.content
            content_dict = json.loads(content)

            types_list = []
            for name in content_dict["types"]:
                types_list.append(str.title(name["type"]["name"]))

            pokemon = {
                "codigo_pokedex": codPokemon,
                "nome_pokemon": str.title(content_dict["name"]),
                "naturezas": types_list,
                "imagem": content_dict["sprites"]["front_default"],
            }

            return pokemon
        except:
            raise Exception("Pokemon não encontrado!!!")

    def __generate_pokemon_random(self) -> dict:
        """Gera pokemon de forma aleatória"""
        x = random.randint(1, 905)
        charPokemon = self.get_pokemon(x)
        return charPokemon

    def __generate_team_pokemon_random(self) -> list:
        """Retorna um time pokemon de forma aleatória"""
        team = []
        for i in range(self.__number_characters):
            pokemon = self.__generate_pokemon_random()
            team.append(pokemon)
        return team

    def extract_team_pokemon(self) -> None:
        """Responsável por extrair o time no diretório"""
        team = self.__generate_team_pokemon_random()
        self.__generate_path()

        if self.__type_file == "json":
            self.__write_json(team)

        elif self.__type_file == "csv":
            self.__write_csv(team)

    def __write_json(self, team) -> None:
        """Gera output formato json"""
        with open(f"{self.__path}/{self.__team_name}.json", "w") as f:
            f.write(json.dumps(team, indent = 4))

    def __write_csv(self, team)  -> None:
        """Gera output formato csv"""
        team = pd.json_normalize(team)
        team.to_csv(
            f"{self.__path}/{self.__team_name}.csv",
            sep = ";",
            index = True
        )

    def __generate_path(self) -> None:
        """Cria path de destino caso não existir"""
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)

if __name__ == '__main__':

    pkm_azul_json = PokemonAPI('time_azul', 6, "extract_json", 'json')
    pkm_vermelho_json = PokemonAPI('time_vermelho', 6, "extract_json", 'json')
    pkm_azul_csv = PokemonAPI('time_azul', 6, "extract_csv", 'csv')
    pkm_vermelho_csv = PokemonAPI('time_vermelho', 6, "extract_csv", 'csv')

    pkm_azul_json.extract_team_pokemon()
    pkm_vermelho_json.extract_team_pokemon()
    pkm_azul_csv.extract_team_pokemon()
    pkm_vermelho_csv.extract_team_pokemon()