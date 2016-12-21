"""
This is a file for functions, which were used in the pre-pySDL2 game version.
They are no longer in use, so ignore warnings.
currently game is imported totally, so everything in here resolves.
"""

from game import *


def levelup(player):
    """ raise player level

    tested, whenever experience ist earned
    :param player: object
    :return: object
    """
    if "learning software" in player.aug:
        lvlup = player.experience > player.level * 10 - 15
    else:
        lvlup = player.experience > player.level * 10
    if lvlup:
        player.level += 1
        print("You gained one level! You can now raise an attribute.")
        choice = 0
        while choice == 0:  # can this be optimized?
            print("(0) Show character")
            print("(1) Intelligence")
            print("(2) Constitution")
            print("(3) Strength")
            print("(4) Agility")
            print("(5) Mobility")
            try:
                choice = int(raw_input("What do you want to raise? "))
            except NameError:
                choice = 0
            if choice == 0:
                player.print_char()
            elif choice == 1:
                player.int += 1
            elif choice == 2:
                player.con += 1
            elif choice == 3:
                player.str += 1
            elif choice == 4:
                player.agi += 1
            elif choice == 5:
                player.mob += 1
            else:
                print("ERROR: Enter a number between 0 and 5.")
            choice = 0
    player.update_max_hp()
    return player


def near(char):
    """ tests if someone is on the 8 fields surrounding char.

    :param char: Char object
    :return: list of char objects
    """
    return []  # for now.


def dead(player, mission):
    """  test, if someone died.

    is executed in start_level(). if the player died, level is ended, going
    back to profile menu
    :param player: Individuum object
    :param mission: Mission object
    :return object, object, boolean
    """
    level_running = True
    for i in mission.current_room.foelist:
        if i.hp < 1:
            player.experience += i.experience
            player = levelup(player)
            try:
                if i.target == True:
                    pass  # mission.target_enemy -= 1
            except AttributeError:
                pass
    if player.hp < 1:
        print("You died.")
        level_running = False
    return player, mission, level_running


def shoot(char, victim):
    """ if the shot hits, the damage is dealt.

    all parameters and returns are character objects.
    char always means the acting character object, not only the player.
    """
    print char.name, " shoots at ", victim.name, " with a ", char.gun.name, "."
    if randint(1, 100) > 100 - (char.agi * 7 + char.int * 3):
        victim.hp -= char.gun.damage
        print("The shot hits and does " + str(char.gun.damage) + " damage.")
    else:
        print("The shot doesn't hit.")
    return char, victim


def choose_gun(char):
    """ equip a gun.

    weapon change. is necessary for current game mechanics.
    maybe we could do that... differently? GUI ftw
    char always means the acting character object, not only the player.
    :param char: object
    :return: object
    """
    print "Name - Damage - Range - AP"
    for i in char.inventory:
        if i.type == "gun":
            print i.name, " ", str(i.damage), " ", str(i.grange), " ", str(i.ap)
    choice = 0
    while choice == 0:
        choice = raw_input("You currently have " + char.gun.name +
                           " equipped. Which one do you choose? (a)bort\n")
        if choice == "a":
            print("Aborted.")
            return char
        for i in char.inventory:
            if choice == i.name and i.type == "gun":
                char.gun = i
                print("Don't hurt anyone with that.")
                return char
        print("ERROR: incorrect input.")
        choice = 0


def aim(char, mission):
    """ who do i shoot?

    from a list of characters in sight (and range?) of char, a victim is
    chosen. for now every character is in sight, changes with GUI.
    char always means the acting character object, not only the player.
    :param char: object
    :param mission: object.
    :return: object, object
    """
    print("0: Abort")
    for i in mission.current_room.foelist:
        print(str(i.id) + ": " + str(i.name))
    victim = 0
    while victim == 0:
        try:
            victim = int(raw_input(char.name + ", who do you want to shoot?"))
        except ValueError:
            print("ERROR: Enter a number.")
            victim = 0
        if victim == 0:
            return mission, None
        for i in mission.current_room.foelist:
            if i.id == victim:
                victim = i
                break
    return mission, victim


def act(char, icdifference, mission):
    """ choose action for turn, calculate AP.

    This function handles each turn. The action is chosen.
    then it adds the AP to the acting char.
    char always means the acting character object, not only the player.
    :param char: object
    :param icdifference: integer
    :param mission: object.
    :return: mission: object
    """
    if "reflex chip" in char.augmentations:
        char.ic -= 10
    if char == mission.current_room.foelist[0]:  # if char == player
        choice = 0
        while choice == 0:  # can this be optimized?
            print("(0) Show character")
            print("(1) Walk: " + str(char.walk_ap()) + " AP")
            print("(2) Choose gun: 0 AP")
            print("(3) Choose sword: 0 AP")
            print("(4) Shoot: " + str(char.gun.ap) + " AP")
            print("(5) Fight: " + str(char.sword.ap) + " AP")
            print("(6) Wait and give away " + str(icdifference) + " AP")
            if char.morph:
                print("(7) Morph: " + str(130 / ((char.mob * 3 + char.int * 5) / 10)))
            try:
                choice = int(raw_input("What do you want to do? "))
            except ValueError:
                print("ERROR: Enter a number.")
                choice = 0
            if choice == 0:
                char.print_char()
            elif choice == 1:
                # walk()
                print("You walk somewhere.")  # debug
                char.ic += char.walk_ap()
                return mission
            elif choice == 2:
                choose_gun(char)
                return mission
            elif choice == 3:
                # choose_sword()
                print("Swords are not implemented yet.")  # debug
                return mission
            elif choice == 4:
                if "fear blocker" not in char.augmentations:
                    if near(char) != []:
                        return mission
                if char.morphed:
                    print("You cannot attack while morphed.")
                    return mission
                # choose a target
                mission, victim = aim(char, mission)
                if victim is not None:
                    char, victim = shoot(char, victim)  # does the damage
                    char.ic += char.gun.ap / ((char.mob * 3 + char.int * 5) / 10)
                return mission
            elif choice == 5:
                # near()    # returns a list with characters near you
                # melee()   # does the damage
                print("You aren't near anyone.")  # debug
                # if you hit someone, do this:
                char.ic += char.sword.ap / ((char.mob * 3 + char.int * 5) / 10)
                return mission
            elif choice == 6:
                print("You wait.")
                char.ic += icdifference + 1
                return mission
            elif choice == 7:
                if char.morph:
                    if char.morphed:
                        char.morphed = False
                        char.ic += 130 / ((char.mob * 3 + char.int * 5) / 10)
                    elif not char.morphed:
                        char.morphed = True
                        char.ic += 130 / ((char.mob * 3 + char.int * 5) / 10)
                    return mission
                else:
                    print("ERROR: Enter a number between 1 and 6.")
            else:
                print("ERROR: Enter a number between 1 and 6.")
            choice = 0
    else:
        # aiturn()
        char.ic += 1  # debug
        return mission
        pass


def initiative(player, mission):
    """ who has the lowest initiative and can act?

    :param player: object
    :param mission: object
    :param foelist: list of objects
    :return player: object
    :return mission: object
    :return foelist: list of character objects
    """
    lowest_ic = player
    for i in mission.room.foelist:
        if i.ic <= lowest_ic.ic:
            icdifference = lowest_ic.ic - i.ic
            lowest_ic = i
    mission = act(lowest_ic, icdifference, mission)
    return player, mission


def start_level(player, mission):
    """ choose level and loop through it.

    choose a level. there will be level description and choosing soon.
    calls build_battlefield to start the level, and uses while-loop
    to keep it running.
    :param player: object
    :return player: object
    """
    print(mission.description)
    mission = build_battlefield(player, mission)
    # returns a list of lists of the fields, a dict with enemy types,
    # and a list with every enemy in the level and his IC.
    level_running = True
    while level_running:
        player, mission = initiative(player, mission)
        player, mission, level_running = dead(player, mission)
        mission.success_func(player, mission.room)
    return player


def choose_level():
    """ Choose mission function

    if function returns 0, it goes back to main menu.
    :return: player: object
    """
    all_missions = os.listdir("../missions")
    if all_missions:
        choice = -1
        while choice == -1:  # can this be optimized?
            print("(0) Abort")
            for i in range(len(all_missions)):
                print("(%s) " + all_missions[i]) % str(i + 1)
            try:
                choice = int(raw_input("Which mission do you want to start?"))
            except ValueError:
                print("ERROR: Enter a number.")
                choice = -1
            if choice == 0:
                print("Choosing aborted.")
                return 0
            elif choice - 1 < len(all_missions) and choice > 0:
                with open("../missions/" + all_missions[choice - 1], "rb", ) as file:
                    mission = pickle.load(file)
                    return mission
            else:
                print("ERROR: Invalid choice.")
                choice = -1
    else:
        print("ERROR: No available missions.")
        return 0


def buy_gun(player):
    """ choose item and pay for it.

    choose an item. add it to player.inventory, reduce player.bitcoins.
    items.allguns: list of guns
    :param player: object
    :return: player: object
    """
    with open("../resources/guns", "rb") as file:
        guns = pickle.load(file)
    for i in guns:
        print "Item: " + i[0],
        leftspace = 20 - len(i[0])
        print leftspace * "_",
        if "cosmetic surgery" in player.augmentations:
            cost = i[1] - 10
        else:
            cost = i[1]
        print "Price: " + str(cost) + " BTC"
    choice = 0
    while choice == 0:
        print("You have " + str(player.bitcoins) + " BTC.")
        try:
            choice = raw_input("Which gun do you want to buy? (a)bort ")
        except SyntaxError:
            choice = 0
            print("ERROR: Incorrect input.")
        if choice == "a":
            return player
        for i in guns:
            if choice == i[0]:
                if "cosmetic surgery" in player.augmentations:
                    cost = i[1] - 10
                else:
                    cost = i[1]
                if cost > player.bitcoins:
                    print("Gun is too expensive.")
                    return player
                else:
                    player.bitcoins -= cost
                player.inventory.append(build_gun(i))
                print("Don't hurt anyone with that.")
                return player
        print("ERROR: Incorrect input.")
        choice = 0


def sell(player):
    """ not yet implemented. maybe when the GUI is coming? """
    print("You have:")
    for i in player.inventory:
        print i.name
    print("I won't buy your shit.")


def get_augments(player):
    choice = 0
    while choice == 0:
        print("Your augmentations:")
        for i in player.augmentations:
            print i
        print(" 0: Abort")
        print(" 1: Get rid of augmentation")
        for i in range(len(augmentations.all_augmentations)):
            if i < 8:  # nice output
                print "",
            print (str(i + 2) + ": " + augmentations.all_augmentations[i])
        try:
            choice = int(raw_input("Which augmentation do you want to get? (costs 100 BTC) "))
        except ValueError:
            print("ERROR: Enter a number.")
        if choice == 0:
            return player
        if choice == 1:
            while choice == 1:
                print("0: Abort")
                for i in range(len(player.augmentations)):
                    print (str(i + 1) + ": " + player.augmentations[i])
                try:
                    choice = int(raw_input("Which augmentation do you want to get rid of? "))
                except ValueError:
                    print("ERROR: Enter a number.")
                if choice == 0:
                    return player
                elif choice > 0 and choice <= len(player.augmentations):
                    player = augmentations.deaugment(player, player.augmentations[choice - 1])
                    return player
                else:
                    print("ERROR: Incorrect input.")
                    choice = 1
        elif choice <= i and choice > 0:
            player = augmentations.augment(player, augmentations.all_augmentations[choice - 2])
            return player
        else:
            print("ERROR: Incorrect input.")


def merchant(player):
    """ choose merchant option.

    needs to be reworked when there is an engine
    :param player: object
    :return: player: object
    """
    choice = 0
    while choice == 0:
        print "(0) Show character"
        print "(1) Buy a gun"
        print "(2) Sell an item"
        print "(3) Get an augmentation"
        print "(4) Back to profile"
        try:
            choice = int(raw_input("What do you want to do? "))
        except ValueError:
            choice = 0
        if choice == 0:
            player.print_char()
        elif choice == 1:  # if clicked on buyable item,
            buy_gun(player)
        elif choice == 2:
            if len(player.inventory) == 0:
                print("You have nothing to sell.")
            else:
                sell(player)
        elif choice == 3:
            get_augments(player)
        elif choice == 4:
            return player
        choice = 0


def profile(player):
    """ This is the profile menu. from here you can buy stuff or start levels. """
    choice = 0
    while choice == 0:  # can this be optimized?
        print "(0) Show character"
        print "(1) Visit the merchant"
        print "(2) Take a job offer"
        print "(3) Main Menu"
        try:
            choice = int(raw_input("What do you want to do? "))
        except NameError:
            choice = 0
        if choice == 0:
            player.print_char()
        elif choice == 1:
            player = merchant(player)
            player.save_profile()
        elif choice == 2:
            mission = choose_mission()
            if mission != 0:
                player = start_level(player, mission)
                player.save_profile()
        elif choice == 3:
            return
        else:
            print("ERROR: Enter a number between 1 and 4.")
        choice = 0


def load_game():
    """ Loading game function

    if function returns 0, it goes back to main menu.
    :return: player: object
    """
    saved_games = os.listdir("../saves")
    if saved_games:
        choice = -1
        while choice == -1:  # can this be optimized?
            print("(0) Abort")
            for i in range(len(saved_games)):
                print("(%s) " + saved_games[i]) % str(i + 1)
            try:
                choice = int(raw_input("Which character do you want to load? "))
            except ValueError:
                print("ERROR: Enter a number.")
                choice = -1
            if choice == 0:
                print("Loading aborted.")
                return 0
            elif choice - 1 < len(saved_games) and choice > 0:
                with open("../saves/" + saved_games[choice - 1], "rb", ) as file:
                    player = pickle.load(file)
                    return player
            else:
                print("ERROR: Invalid choice.")
                choice = -1
    else:
        print("ERROR: No saved games.")
        return 0


def create_character():
    """ returns player object, prints the character """
    name = ""
    while name == "":
        name = raw_input("What's your name? ")
    choice = 0
    while choice == 0:  # can this be optimized?
        print("(1) Vampire\n(2) Angel\n(3) Werewolf\n(4) Golem")
        try:
            choice = int(raw_input("What are you? "))
        except ValueError:
            choice = 0
        if choice == 0:
            print("ERROR: Enter a number.")
        elif choice == 1:
            player = Vampire(name)
        elif choice == 2:
            player = Angel(name)
        elif choice == 3:
            player = Werewolf(name)
        elif choice == 4:
            player = Golem(name)
        else:
            print("ERROR: Enter a number between 1 and 4.")
            choice = 0
    print("Your new character:")
    player.print_char()
    player.save_profile()
    return player


def main_menu():
    """ Main Menu, from here the other functions are started. """
    choice = 0
    while choice == 0:  # can this be optimized?
        print("(1) New game\n(2) Load game\n(3) Options\n(4) Exit")
        try:
            choice = int(raw_input("What do you want to do? "))
        except ValueError:
            choice = 0
        if choice == 0:
            print("ERROR: Enter a number.")
        elif choice == 1:
            player = create_character()
            profile(player)
        elif choice == 2:
            player = load_game()
            if player == 0:
                pass
            else:
                profile(player)
        elif choice == 3:
            pass  # options
        elif choice == 4:
            print("Good Bye.")
            exit()
        else:
            print("ERROR: Enter a number between 1 and 4.")
        choice = 0


def main():
    main_menu()
