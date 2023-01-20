import GameEngine

def render_introduction():
    return "You are a black square in a white void. You have always been a black square in a white void, and you have no reason to be anything more.\n But something in you yearns to have it: something greater.\n You look around and find that your void is not as white as you thought it was.\n Left is a mass of squares black as you are, with boxes suspended above each other. \n Right is a similar mass, but the box is tightly packed and enclosed.\n Up and down are nothing more than the void you have always known."
    '''
    Create the message to be displayed at the start of your game.
    Returns:
        str: The introductory text of your game to be displayed.
    '''

def create_world():
    return {
        "map": create_map(),
        "player": create_player(),
        "status": "playing"
        }
    '''
    Creates a new version of the world in its initial state.

    Returns:
        World: The initial state of the world
    '''
def create_map():
    return {
        "Home": {
            "neighbors": ["Right", "Left", "Up", "Down"],
            "about": "You look around and wonder where you should go.",
            "stuff": []
            },
        "Platformer": {
        "neighbors": ["Home"],
        "lockedNeighbors": ["The Meaning"],
        "about": "You look up and down. You see, as you saw before, boxes above you and to each side.\n Some of those boxes look rather like you could jump on them... \n I wonder what lies at the top.",
        "stuff": []
        },
        "The Meaning": {
        "neighbors": ["Right"],
        "about": "On the floor is an object that whispers to you, \" Pick me up.... I am meaning...\"",
        "stuff": ["Meaning"]
        },
        "Right": {
            "neighbors": ["Home"],
            "lockedNeighbors": ["Platformer"],
            "about": "There is a block in your way. You could walk around it, but that might be a little disrespectful.\n You ask it, \"What can I do for you so that you let me pass?\".\n It says, \"The only thing I long for... The reason I live in this white void... Find me a vinyl record with Mariah Carey's \"All I Want For Christmas Is You\" recorded on it.\n Then I will let you pass.",
            "stuff": ["Big Block"]
        },
        "Down": {
            "neighbors": ["Home"],
            "about": "There is nothing here. But there must be something. You keep moving down. And moving down. And moving down.\n It occurs to you to turn around, but then, you've already come this far.\n There is no stopping until you find something.\n And you will most likely never find something.",
            "stuff": []
        },
        "Left": {
            "neighbors": ["Home"],
            "lockedNeighbors": ["Vinyl Room"],
            "about": "The enclosed box you saw before comes to clarity. It is a jumble of passages---snaking paths, winding corridors, and plenty of dead ends---a \"maze\".",
            "stuff": []
        },
        "Up": {
            "neighbors": ["Home"],
            "lockedNeighbors": ["Enlightenment"],
            "about": "You see an old square sitting on a platform.\n How does a square look \"old\"? Don't ask stupid questions.\n It looks at you and asks, \"What is the meaning?\"",
            "stuff": ["Old Square"]
        },
        "Vinyl Room": {
            "neighbors": ["Left"],
            "about": "There is an object on the floor. Closer inspection reveals it is a vinyl record with Mariah Carey's \"All I Want For Christmas Is You\" recorded on it.",
            "stuff": ["Vinyl Record"]
        },
        "Enlightenment": {
            "neighbors": ["Up"],
            "about": "You have reached enlightenment. You have realized that to be perfect is to find the state of unchanging, and to change is to exist. Thus, you no longer exist.\n You WIN!",
            "stuff": []
        },
        
        }

def create_player():
    return {
        "Location": "Home",
        "Inventory": []
        }

def render(world):
    return (render_location(world) + render_player(world) + render_visible_stuff(world))
    '''
    Consumes a world and produces a string that will describe the current state
    of the world. Does not print.

    Args:
        world (World): The current world to describe.

    Returns:
        str: A textual description of the world.
    '''

def render_location(world):
    player_location = world["player"]["Location"]
    map_location = world["map"][player_location]
    about = map_location["about"]
    return ("you are in "+player_location+"\n\n"+about+"\n")

def render_visible_stuff(world):
    player_location = world["player"]["Location"]
    stuff = world["map"][player_location]["stuff"]
    formatted_list = ""
    for item in stuff:
        formatted_list = formatted_list + "-"+item+"\n"
    return "you can see the following: \n"+formatted_list

def render_player(world):
    inventory = world["player"]["Inventory"]
    formatted_inventory = ""
    for item in inventory:
        formatted_inventory = formatted_inventory + "-"+item+"\n"
    return "your inventory contains the following: \n\n"+formatted_inventory

def get_options(world):
    inventory = world["player"]["Inventory"]
    location = world["player"]["Location"]
    commands = ["quit"]
    for i in world["map"][location]["neighbors"]:
        commands.append(f"goto {i}")
    if location == "Platformer":
        commands.append("play platformer")
    if location == "Left":
        commands.append("enter maze")
    if location == "Right":
        if "Vinyl Record" in inventory:
            commands.append("give vinyl to block")
    if location == "The Meaning":
        if not "Meaning" in inventory:
            commands.append("pick up Meaning")
    if location == "Vinyl Room":
        if not "Vinyl Record" in inventory:
            commands.append("pick up Vinyl Record")
    if location == "Up":
        commands.append("answer the question to the best of your ability")
    return commands
    '''
    Consumes a world and produces a list of strings representing the options
    that are available to be chosen given this state.

    Args:
        world (World): The current world to get options for.

    Returns:
        list[str]: The list of commands that the user can choose from.
    '''

def update(world, command):
    if command == "goto Enlightenment":
        world["status"] = "win"
    if command == "goto Down":
        world["status"] = "lose"
        return "There is nothing here. But there must be something. You keep moving down. And moving down. And moving down.\n It occurs to you to turn around, but then, you've already come this far.\n There is no stopping until you find something.\n And you will most likely never find something."
    if command.startswith("goto"):
        world["player"].update({"Location": command[5:]})
        return f"You went to {command[5:]}"
    if command.startswith("pick up"):
        world["player"]["Inventory"].append(command[8:])
        return f"You picked up {command[8:]}"
    if command == "play platformer":
        if GameEngine.start("platformer"):
            world["map"]["Platformer"]["lockedNeighbors"].remove("The Meaning")
            world["map"]["Platformer"]["neighbors"].append("The Meaning")
            return "You completed the challenge and unlocked the next room."
    if command == "enter maze":
        if GameEngine.start("maze"):
            world["map"]["Left"]["lockedNeighbors"].remove("Vinyl Room")
            world["map"]["Left"]["neighbors"].append("Vinyl Room")
            return "You completed the challenge and unlocked the next room."
    if command == "quit":
        world["status"] = "quit"
        return "You decide that you are happy to rest in your white void forever."
    if command == "give vinyl to block":
        world["player"]["Inventory"].remove("Vinyl Record")
        world["map"]["Right"]["lockedNeighbors"].remove("Platformer")
        world["map"]["Right"]["neighbors"].append("Platformer")
        return "The block moves and lets you pass"
    if command == "answer the question to the best of your ability":
        if "Meaning" in world["player"]["Inventory"]:
            world["map"]["Up"]["lockedNeighbors"].remove("Enlightenment")
            world["map"]["Up"]["neighbors"].append("Enlightenment")
            return "You have the meaning. You may pass."
        else:
            world["status"] = "lose"
            return "The old square says, \"You do not have meaning. You have failed.\""
            
    '''
    Consumes a world and a command and updates the world according to the
    command, also producing a message about the update that occurred. This
    function should modify the world given, not produce a new one.

    Args:
        world (World): The current world to modify.

    Returns:
        str: A message describing the change that occurred in the world.
    '''

def render_ending(world):
    status = world["status"]
    if status == "win":
        return "Congratulations. You have found meaning. Your void is still as empty, but you are not."
    elif status == "lose":
        return "You are condemned to exist in eternity."
    elif status == "quit":
        return "You decide you are content with your void just as it is."
    '''
    Create the message to be displayed at the end of your game.

    Args:
        world (World): The final world state to use in describing the ending.

    Returns:
        str: The ending text of your game to be displayed.
    '''

def choose(options):
    lits = "You can:\n"
    for i in options:
        lits = lits+i+"\n"
    print(lits)
    userInput = ""
    while userInput not in options:
        userInput = input("What would you like to do?")
    return userInput
    '''
    Consumes a list of commands, prints them for the user, takes in user input
    for the command that the user wants (prompting repeatedly until a valid
    command is chosen), and then returns the command that was chosen.

    Note:
        Use your answer to Programming Problem #42.3

    Args:
        options (list[str]): The potential commands to select from.

    Returns:
        str: The command that was selected by the user.
    '''
###### Main Function #####
# Do not modify this area

def main():
    '''
    Run your game using the Text Adventure console engine.
    Consumes and produces nothing, but prints and indirectly takes user input.
    '''
    print(render_introduction())
    world = create_world()
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))


if __name__ == '__main__':
    main()

