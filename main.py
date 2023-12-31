import typing
import requests
import pandas as pd
import matplotlib.pyplot as plt
from Pokemon import Pokemon
from Population import Population


def get_poke(user_poke_name: str) -> Pokemon:
    """Takes the user-entered pokemon name and creates a corresponding Pokemon object
    """
    poke_url = "https://pokeapi.co/api/v2/pokemon/" + user_poke_name  # Use input to define appropriate URL
    poke_request: requests.Response = requests.get(poke_url)  # Set up request
    poke_got: typing.Union[str, dict] = "0"  # Give request a placeholder value
    while poke_got == "0":
        try:  # Try to get json for that pokemon
            poke_request.raise_for_status()
            poke_got = poke_request.json()
            break
        except requests.exceptions.RequestException as req_ex:
            if poke_request.status_code == 404:  # If a 404 error occurs, that pokemon probably isn't real; ask for pokemon name again
                print("We can't find a Pokemon with that name.")
                user_poke = input("Enter the name of a Pokemon: ").lower()
                poke_url = "https://pokeapi.co/api/v2/pokemon/" + user_poke
                poke_request = requests.get(poke_url)
            else:
                quit()
    return Pokemon(poke_got)  # Use poke_got dictionary to create a corresponding Pokemon object


# Create a Population object from .csv file

pop = Population("Population_Data.csv")

# Ask user for a pokemon name, then use PokeAPI to create an appropriate Pokemon object

user_poke_name = input("Enter the name of a Pokemon: ").lower()  # Ask for a pokemon name
user_poke: Pokemon = get_poke(user_poke_name)  # Create a corresponding Pokemon object

# Test prints

print(user_poke)
print(user_poke.compare_stat("height", pop))
print(user_poke.compare_stat("weight", pop))

# Test graphs

pop.plot_dist_marked("height", user_poke.height, user_poke_name)
pop.plot_dist_marked("weight", user_poke.weight, user_poke_name)