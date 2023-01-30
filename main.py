import json
import requests
import inquirer
import pyfiglet
import textwrap

# change text selection color for better readability
color_theme = inquirer.themes.load_theme_from_dict({"List": {"selection_color": "bright_red", "selection_cursor": ">"}})

def main():
    """Add docstring later"""
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
        if choice == "Generate a random pokémon name":
            print("Not yet implemented")
        if choice == "Exit":
            break
    print(goodbye_msg)

def options():
    """Add docstring later"""
    option = [
        inquirer.List('choice',
                      message="- Select an option",
                      choices=["FAQ",
                               "Search by pokémon name (e.g., pikachu)",
                               "Generate a random pokémon name",
                               "Exit"],
                    ),
    ]
    answer = inquirer.prompt(option, theme=color_theme)
    return answer

def faq():
    """add docstring later"""
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
    """add docstring later"""
    poke_name = [inquirer.Text('name', message="Enter a pokémon name")]
    answer = inquirer.prompt(poke_name)

    response = requests.get("https://pokeapi.co/api/v2/pokemon/" + f"{answer['name'].lower()}")
    try:
        result = response.json()
    except:
        print("Error: pokémon not found, please enter a new name \n")

    if response.status_code == 200:
        poke_header = pyfiglet.figlet_format(f"{answer['name'].lower()}", font="standard")
        print(poke_header)
        print("National Number: " + f"{result['id']}")

        # types
        types = result['types']
        if len(types) > 1:
            type_str = types[0]['type']['name'] + "/" + types[1]['type']['name']
            print("Type: " + type_str)
        else:
            print("Type: " + f"{types[0]['type']['name']}")

        # species
        response_2 = requests.get(f"{result['species']['url']}")
        result_2 = response_2.json()
        print("Species: " + f"{result_2['genera'][7]['genus']}")

        # height/weight
        height = result['height'] / 10
        weight = result['weight'] / 10
        print(f"Height: {height}m" + "  /  " + f"Weight: {weight}kg")

        # abilities
        abilities = result['abilities']
        if len(abilities) == 3:
            ab_str = abilities[0]['ability']['name'] + " | " + abilities[1]['ability']['name'] + " | " + abilities[2]['ability']['name'] + "(hidden)"
        elif len(abilities) == 2:
            ab_str = abilities[0]['ability']['name'] + " | " + abilities[1]['ability']['name'] + "(hidden)"
        else:
            ab_str = abilities[0]['ability']['name']
        print("Abilities: " + ab_str)

        # evolution chain
        response_3 = requests.get(f"{result_2['evolution_chain']['url']}")
        result_3 = response_3.json()
        evolve = result_3['chain']['evolves_to']
        if len(evolve) == 0:
            evol_chain = result_3['chain']['species']['name']
        elif len(evolve) == 1:
            first = result_3['chain']['species']['name']
            second = evolve[0]['species']['name']
            evol_chain = first + " --> " + second
            if len(evolve[0]['evolves_to']) == 1:
                third = evolve[0]['evolves_to'][0]['species']['name']
                evol_chain = first + " --> " + second + " --> " + third
        print("Evolution Chain: " + evol_chain + "\n")

        option = [
        inquirer.List('choice',
                      message="- Select an option",
                      choices=["View base stats",
                               "View moves (e.g., level-up, egg, tutor, machine, all)",
                               "Return home"],
                    ),
        ]
        answer = inquirer.prompt(option, theme=color_theme)
        if answer['choice'] == "View base stats":
            print("Not yet implemented\n")
        if answer['choice'] == "View moves (e.g., level-up, egg, tutor, machine, all)":
            print("Not yet implemented\n")
        if answer['choice'] == "Return home":
            return


if __name__ == "__main__":
    main()
