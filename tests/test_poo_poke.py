import pytest
from poo_poke import PokemonAPI
import json


instance = PokemonAPI('time_azul', 6, "extract_json", 'json')


def test_mock_get_pokemon(mocker):
    expected = {
        'codigo_pokedex': 10,
        'nome_pokemon': 'Batata'
    }
    mocker.patch('poo_poke.PokemonAPI.get_pokemon', return_value = expected)
    request = instance.get_pokemon(10)
    assert request == expected

  
@pytest.mark.parametrize('input, expected',
    [
        (
            10,
            {
                'codigo_pokedex': 10,
                'imagem': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/10.png',
                'naturezas': ['Bug'],
                'nome_pokemon': 'Caterpie'
            }
        ),
        (
            19999,
            Exception("Pokemon não encontrado!!!")
        )
    ]
)
def test_get_pokemon(input, expected):
    if isinstance(expected, dict):
        request = instance.get_pokemon(input)
        assert request == expected
    else:
        with pytest.raises(Exception) as exc_info:
            instance.get_pokemon(input)
        assert str(exc_info.value) == str(expected)


def test_generate_pokemon_random(mocker):
    mocker.patch('poo_poke.PokemonAPI.get_pokemon', return_value = {})
    pokemon_aleatorio = instance._PokemonAPI__generate_pokemon_random()
    assert isinstance(pokemon_aleatorio, dict)
    assert instance.get_pokemon.call_count == 1


def test_generate_team_pokemon_random(mocker):
    mocker.spy(instance, '_PokemonAPI__generate_pokemon_random')
    team_pokemon = instance._PokemonAPI__generate_team_pokemon_random()
    assert instance._PokemonAPI__generate_pokemon_random.call_count == instance._PokemonAPI__number_characters
    assert isinstance(team_pokemon, list)
    for pokemon in team_pokemon:
        assert isinstance(pokemon, dict)


@pytest.mark.parametrize('path_name, file_type, call_write_json, call_write_csv',
    [
        ('extract_json', 'json', 1, 0),
        ('extract_csv', 'csv', 0, 1)
    ]
)
def test_extract_team_pokemon(
    path_name,
    file_type,
    call_write_json,
    call_write_csv,
    mocker
    ):
    instance = PokemonAPI('time_azul', 6, path_name, file_type)
    mocker.patch.object(instance, '_PokemonAPI__generate_team_pokemon_random')
    mocker.patch.object(instance, '_PokemonAPI__generate_path') 
    mocker.patch.object(instance, '_PokemonAPI__write_json')
    mocker.patch.object(instance, '_PokemonAPI__write_csv')
    instance.extract_team_pokemon()
    assert instance._PokemonAPI__generate_team_pokemon_random.call_count == 1
    assert instance._PokemonAPI__generate_path.call_count == 1
    assert instance._PokemonAPI__write_json.call_count == call_write_json
    assert instance._PokemonAPI__write_csv.call_count == call_write_csv


def test_write_json(mocker):
    mocker.patch.object(instance, '_PokemonAPI__write_json', return_value = None)
    team = []
    req = instance._PokemonAPI__write_json(team)

    assert req is None


def test_write_csv(mocker):
    mocker.patch.object(instance, '_PokemonAPI__write_csv', return_value = None)
    team = []
    req = instance._PokemonAPI__write_csv(team)

    assert req is None


def test_generate_path(mocker):
    mocker.patch.object(instance, '_PokemonAPI__generate_path', return_value = None)
    team = []
    req = instance._PokemonAPI__generate_path(team)

    assert req is None