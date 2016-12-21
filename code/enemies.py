# coding=utf-8
# name, race, cons, strs, agis, mobs, ints, gun, sword, image, bitcoinloot (arguments for randint())

import items
from random import randint

def getenemyid():
    """ give a character an unique ID.
    in build_battlefield(), a foelist is created, in which the character
    objects are created, whose constructor triggers this function, which
    gives them an unique ID.
    :return integer
    """
    global enemyidcounter
    enemyidcounter += 1
    return enemyidcounter


# This global var increments every time an enemy gets an ID.
enemyidcounter = 0


class Enemy(object):
    """ enemy superclass. this one could get some useful methods one day. """
    def __init__(self, name, race, image, con, str, agi, mob, int, gun, sword,
                 loot, experience):
        self.name = name  # string
        self.race = race  # string
        self.image = image  # string: path to image
        self.con = con  # integer
        self.str = str  # integer
        self.agi = agi  # integer
        self.mob = mob  # integer
        self.int = int  # integer
        allitems = items.AllItems()
        if gun == "random":
            self.gun = self.randitem(self.allitems.buyablegunsC)
        else:
            self.gun = allitems.buyablegunsC[gun]()  # string: items.gun
        if sword == "random":
            self.sword = self.randitem(self.allitems.buyableswordsC)
        else:
            self.sword = allitems.buyableswordsC[sword]  # string: items.sword
        self.loot = loot  # list of 2 arguments for randint()
        self.experience = experience
        # integer, how much experience player gets at killing asd
        self.id = getenemyid()
        self.max_hp = self.con * 8 + self.str * 5 + 10
        self.hp = self.max_hp
        self.ic = 1
    def showinfo(self):
        pass  # open an infobox with info about the enemy on right-click
    def walk_ap(self):
        """
        returns, how many AP 1 step is costing
        :return: integer
        """
        walk_ap = 100 / self.mob
        return walk_ap

    def randitem(self, dict):
        lst = []
        for i in dict:
            if i is not "random":
                lst.append(dict[i])
        number = randint(0, len(lst))
        return lst[number]


"""
class Citizen(Enemy):
    def __init__(self):
        super(Citizen, self).__init__("Citizen", "human", "", 3, 3, 3, 3, 4,
                                      "None", "None", [5, 15], 0)


class Boss(Enemy):
    def __init__(self):
        super(Boss, self).__init__("Boss", "human", "", 7, 6, 6, 7, 4,
                                   "random", "random", [40, 70], 9)


class Police(Enemy):
    def __init__(self):
        super(Police, self).__init__("Police officer", "human", "", 4, 5, 5,
                                     4, 4, "glock", "teli", [5, 10], 5)


class Security(Enemy):
    def __init__(self):
        super(Security, self).__init__("Private Security", "human", "", 5, 7,
                                       5, 4, 4, "random", "teli", [1, 10], 6)


class Mercenary(Enemy):
    def __init__(self):
        super(Mercenary, self).__init__("Mercenary", "human", "", 6, 8, 8, 6,
                                        4, "ak74", "knife", [5, 20], 7)


class Soldier(Enemy):
    def __init__(self):
        super(Soldier, self).__init__("Soldier", "human", "", 7, 8, 8, 7, 4,
                                      "random", "knife", [10, 20], 8)


class Taskforce(Enemy):
    def __init__(self):
        super(Taskforce, self).__init__("Task Force", "human", "", 9, 10, 10,
                                        9, 7, "random", "random", [10, 5], 10)


class Criminal(Enemy):
    def __init__(self):
        super(Criminal, self).__init__("Criminal", "human", "", 5, 6, 7, 7, 6,
                                       "random", "random", [1, 15], 6)


class Terrorist(Enemy):
    def __init__(self):
        super(Terrorist, self).__init__("Terrorist", "human", "", 5, 7, 9, 8,
                                        6, "random", "random", [1, 15], 7)


class Silver1(Enemy):
    def __init__(self):
        super(Silver1, self).__init__("Besorgt", "human", "", 4, 5, 5, 4, 2,
                                      "random", "silversword",
                                      [1, 10], 7)


class Silver2(Enemy):
    def __init__(self):
        super(Silver2, self).__init__("Fascist", "human", "", 8, 10, 8, 5, 2,
                                      "random", "whip", [10, 20], 11)


class Angel1(Enemy):
    def __init__(self):
        super(Angel1, self).__init__("Angel", "angel", "", 5, 3, 8, 7, 6,
                                     "random", "random", [10, 15], 8)


class Angel2(Enemy):
    def __init__(self):
        super(Angel2, self).__init__("High Angel", "angel", "", 6, 4, 10, 8,
                                     7, "random", "random", [15, 25], 12)


class Vampire1(Enemy):
    def __init__(self):
        super(Vampire1, self).__init__("Vampire", "vampire", "", 7, 9, 5, 5,
                                       6, "random", "random", [10, 15], 8)


class Vampire2(Enemy):
    def __init__(self):
        super(Vampire2, self).__init__("Dark Vampire", "vampire", "", 8, 11,
                                       6, 6, 7, "random", "random", [15, 25],
                                       12)


class Werewolf1(Enemy):
    def __init__(self):
        super(Werewolf1, self).__init__("Werewolf", "werewolf", "", 4, 5, 6,
                                        5, 5, "random", "krallen", [10, 15], 8)


class Werewolf2(Enemy):
    def __init__(self):
        super(Werewolf2, self).__init__("Furious Werewolf ", "werewolf", "",
                                        5, 8, 6, 6, 5, "random",
                                        "silverkrallen", [15, 25], 12)


# You can create an enemy object by calling: enemies.all_enemies[name]()
all_enemies = {
    "Citizen": Citizen, "Boss": Boss, "Police Officer": Police,
    "Private Security": Security, "Mercenary": Mercenary, "Soldier": Soldier,
    "Task Force": Taskforce, "Criminal": Criminal, "Terrorist": Terrorist,
    "Besorgt": Silver1, "Fascist": Silver2, "Angel": Angel1,
    "High Angel": Angel2, "Vampire": Vampire1, "Dark Vampire": Vampire2,
    "Werewolf": Werewolf1, "Furious Werewolf": Werewolf2
}


civilian = ["Citizen", "human", "", 0, 0, 0, 0, 0, "None", "None", [5, 15], 0]
boss = ["Boss", "human", 7, 6, 6, 7, 0, "random", "random", [40, 70], 9]

police = ["Police Officer", "human", "", 0, 0, 0, 0, 0, "glock", "teli", [5, 10], 5]
security = ["Private Security", "human", "", 1, 2, 0, 0, 0, "random", "teli", [1, 10], 6]
mercenary = ["Mercenary", "human", "", 2, 3, 2, 2, 1, "ak74", "knife", [5, 20], 7]
soldier = ["Soldier", "human", "", 3, 3, 3, 3, 2, "random", "knife", [10, 20], 8]
taskforce = ["Task force", "human", "", 5, 5, 5, 5, 3, "random", "random", [10, 50], 10]

criminal = ["Criminial", "human", "", 1, 1, 2, 3, 2, "random", "random", [1, 15], 6]
terrorist = ["Terrorist", "human", "", 1, 2, 4, 4, 2, "random", "random", [1, 15], 7]

silver1 = ["Besorgt", "human", "", 0, 0, 0, 0, 0, "random", "silversword", [1, 10], 7]
silver2 = ["Fascist", "human", "", 4, 5, 3, 1, 3, "random", "whip", [10, 20], 11]

angel1 = ["Angel", "angel", "", 1, 0, 1, 0, 1, "random", "random", [10, 15], 8]
angel2 = ["Angel", "angel", "", 2, 1, 3, 1, 2, "random", "random", [15, 25], 12]

vampire1 = ["Vampire", "vampire", "", 1, 1, 0, 0, 1, "random", "random", [10, 15], 8]
vampire2 = ["Vampire", "vampire", "", 2, 3, 1, 1, 2, "random", "random", [15, 25], 12]

werewolf1 = ["Werewolf", "werewolf", "", 0, 0, 1, 1, 1, "random", "krallen", [10, 15], 8]
werewolf2 = ["Werewolf", "werewolf", "", 1, 3, 1, 2, 1, "random", "silverkrallen", [15, 25], 12]

all_enemies = {
    "Citizen": civilian, "Boss": boss, "Police Officer": police,
    "Private Security": security, "Mercenary": mercenary, "Soldier": soldier,
    "Task Force": taskforce, "Criminal": criminal, "Terrorist": terrorist,
    "Besorgt": silver1, "Fascist": silver2, "Angel": angel1,
    "High Angel": angel2, "Vampire": vampire1, "Dark Vampire": vampire2,
    "Werewolf": werewolf1, "Furious Werewolf": werewolf2
} """
