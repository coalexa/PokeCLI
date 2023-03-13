import json
import requests
import inquirer
import pyfiglet
import textwrap
import time
from termcolor import colored

# change text selection color for better readability
color_theme = inquirer.themes.load_theme_from_dict({"List": {"selection_color": "bright_red", "selection_cursor": ">"}})

def main():
    """Main driver function"""
    name = pyfiglet.figlet_format("PokeCLI", font="standard")
    goodbye_msg = pyfiglet.figlet_format("GoodBye", font="standard")
    print(name)
    print(">> Welcome to the pokémon CLI tool")
    print(">> With this tool, you can find information about any pokémon")
    print(">> To start, use the up and down arrow keys and select an option")
    print("** Have a question? Select the FAQ option to get help **")
    print("\n")
    while True:
        choice = options()['choice']
        if choice == "FAQ":
            faq()
        if choice == "Search by pokémon name (e.g., pikachu)":
            search_by_name()
        if choice == "Generate a random pokémon":
            generate_random_pokemon()
        if choice == "Exit":
            break
    print(goodbye_msg)

def options():
    """Options for user selection function"""
    option = [
        inquirer.List('choice',
                      message="- Select an option",
                      choices=["FAQ",
                               "Search by pokémon name (e.g., pikachu)",
                               "Generate a random pokémon",
                               "Exit"],
                    ),
    ]
    answer = inquirer.prompt(option, theme=color_theme)
    return answer

def faq():
    """FAQ function"""
    faq_header = pyfiglet.figlet_format("FAQ", font="standard")
    print(faq_header)
    f = open('faq.json')
    data = json.load(f)
    data_len = len(data)
    
    for i in range(1, data_len + 1):
        # ensure special characters get output correctly using encode/decode
        print(data[f"{i}"][0].encode('latin1').decode('utf8'))
        value = data[f"{i}"][1].encode('latin1').decode('utf8')

        # limit amount of words per line then print to terminal
        wrapper = textwrap.TextWrapper(width=85)
        word_list = wrapper.wrap(text=value)
        for element in word_list:
            print(element)
        print("\n")
    
    option = [inquirer.List('choice', choices=["Return Home"])]
    inquirer.prompt(option, theme=color_theme)

def search_by_name():
    """Search function"""
    poke_name = [inquirer.Text('name', message="Enter a pokémon name")]
    answer = inquirer.prompt(poke_name)
    poke_name = answer['name'].replace('.', ' ').replace(' ', '-').lower()

    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + poke_name)
    get_results(response)

def generate_random_pokemon():
    """Generate random pokemon function"""
    prng_file = open('prng-service.txt', 'w')
    prng_file.write('run')
    prng_file.close()
    time.sleep(2)
    prng_file = open('prng-service.txt', 'r')
    rand_num = prng_file.readline()

    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + rand_num)
    get_results(response)

def get_type(result):
    """Get and display pokemon type"""
    types = result['types']
    if len(types) > 1:
        type_str = types[0]['type']['name'] + "/" + types[1]['type']['name']
        print(" ○ " + "Type: " + type_str)
    else:
        print(" ○ " + "Type: " + f"{types[0]['type']['name']}")

def get_species(result_2):
    """Get and display pokemon species"""
    species = result_2['genera']
    for i in range(len(species)):
        if species[i]['language']['name'] == "en":
            print(" ○ " + "Species: " + f"{species[i]['genus']}")

def get_height_weight(result):
    """Get poke height and weight"""
    height = result['height'] / 10
    weight = result['weight'] / 10
    print(" ○ " + f"Height: {height}m" + "  /  " + f"Weight: {weight}kg")

def get_abilities(result):
    """Get and display pokemon abilities"""
    abilities = result['abilities']
    if len(abilities) == 3:
        ability_1 = abilities[0]['ability']['name']
        ability_2 = abilities[1]['ability']['name']
        ability_3 = abilities[2]['ability']['name'] + "(hidden)"
        ab_str = ability_1 + " | " + ability_2 + " | " + ability_3
    elif len(abilities) == 2:
        ability_1 = abilities[0]['ability']['name']
        ability_2 = abilities[1]['ability']['name'] + "(hidden)"
        ab_str = ability_1 + " | " + ability_2
    else:
        ab_str = abilities[0]['ability']['name']
    print(" ○ " + "Abilities: " + ab_str)

def get_evolve_from(result_2):
    """Get and display pokemon pre-evolution"""
    evolve = result_2['evolves_from_species']
    if evolve == None:
        print("\n")
    else:
        print(" ○ " + "Evolves from: " + evolve['name'] + "\n")

def get_base_stats(result):
    """Get and display pokemon base stats"""
    stat_dict = {'HP': 0, 'Attack': 0, 'Defense': 0, 'Special-Attack': 0, 'Special-Defense': 0,
                 'Speed': 0}
    for index, key in enumerate(stat_dict):
        stat_dict[key] = result['stats'][index]['base_stat']
    
    for key in stat_dict:
        print(" ○ " + f"{key}: " + f"{stat_dict[key]}")
    print('\n')
    pokemon_options(result)

def get_moves(result):
    """Get and display pokemon moves"""
    moves = result['moves']
    total = len(result['moves'])
    count = 0
    while count < total:
        for i in range(15):
            if count != total:
                if i % 2 == 0:
                    print(colored(" ○ " + moves[count]['move']['name'], 'red'))
                    count += 1
                else:
                    print(" ○ " + moves[count]['move']['name'])
                    count += 1
            else:
                break
        print('\n' + " ○ " + colored('Total moves viewed: ' + f"{count}" + "/" + f"{total}", 'red'))
        if count == total:
            break
        next_page = inquirer.confirm("View more moves?", default = True)
        if next_page is True:
            continue
        else:
            break
    pokemon_options(result)

def get_results(response):
    """Show results function"""
    try:
        result = response.json()
        poke_name = result['name']
    except:
        print(" ○ " + "Error: pokémon not found, please enter a new name \n")

    if response.status_code == 200:
        poke_header = pyfiglet.figlet_format(f"{poke_name.lower()}", font="standard")
        print(poke_header)
        print(" ○ " + "National Number: " + f"{result['id']}")

        response_2 = requests.get(f"{result['species']['url']}")
        result_2 = response_2.json()

        # get and print pokemon information
        get_type(result)
        get_species(result_2)
        get_height_weight(result)
        get_abilities(result)
        get_evolve_from(result_2)
        pokemon_options(result)

def pokemon_options(result):
    """Second set of options after getting information about a pokemon"""
    option = [
    inquirer.List('choice',
                    message="- Select an option",
                    choices=["View base stats",
                            "View moves",
                            "Return home"],
                ),
    ]
    answer = inquirer.prompt(option, theme=color_theme)
    if answer['choice'] == "View base stats":
        get_base_stats(result)
    if answer['choice'] == "View moves":
        get_moves(result)
    if answer['choice'] == "Return home":
        return


if __name__ == "__main__":
    main()
