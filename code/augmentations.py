#! /usr/bin/env python
# Augmentations
# All of them cost 100 BTC?
# only 3 of them at the same time
# I think there is a dictionary needed to connect the strings to images, and maybe prices.
# most augmentation effects are checked in other functions.

from random import randint


def augment(char, aug, m):
    """ add an augmentation to character.

    When a Character gets an augmentation, its name is put in the
    char.augmentations-list. if it has a static effect on char values,
    they are also changed in this function. every other effects are
    checked in other functions.
    :param char: object
    :param aug: string
    :param m: SDLInstanceManager object
    :return: char: object
    """
    if aug in char.augmentations:
        m.console.push("ERROR: Character already has " + aug + ".")
    elif len(char.augmentations) > 4:
        m.console.push("ERROR: Character has already 3 augmentations")
    else:
        if "cosmetic surgery" in char.augmentations:
            cost = 90
        else:
            cost = 100
        if char.bitcoins < cost:
            m.console.push("ERROR: Not enough bitcoins!")
            return char
        else:
            char.bitcoins -= cost
        if randint(0, 99) > 10:
            if aug == "genetic surgery":
                char.morph = True
            elif aug == "eye processor":
                char.agi += 2
            elif aug == "artificial leg":
                char.mob += 2
            char.augmentations.append(aug)
            m.console.push("The surgery went well.")
        else:
            char.con -= 1
            m.console.push("The surgery failed. You lose 1 Consitution.")
        m.charwin.process()
    return char


def deaugment(char, aug, m):
    """ erase an augmentation from character.

    first destroys values, if they had been changed by augmentation, then
    deletes name from char.augmentations
    :param char: object
    :param aug: string
    :param m: SDLInstanceManager object
    :return: char: object
    """
    if aug not in char.augmentations:
        m.console.push("ERROR: Character doesn't have " + aug + ".")
    else:
        if aug == "genetic surgery":
            char.morph = False
        elif aug == "eye processor":
            char.agi -= 2
        elif aug == "artificial leg":
            char.mob -= 2
        char.augmentations.remove(aug)  # does this work? aug is not in
        # augmentations asd
        if randint(0, 99) > 10:
            m.console.push(aug + " has been removed successfully.")
            m.charwin.process()
        else:
            char.con -= 1
            m.console.push("The surgery failed. You lose 1 Consitution.")
    return char


all_augmentations = {
    "artificial leg": "../images/augmentations/artificial_leg.gif",
    "reflex chip": "../images/augmentations/reflex_chip.gif",
    "kevlar implant": "../images/augmentations/kevlar_implant.gif",
    "eye processor": "../images/augmentations/eye_processor.gif",
    "cosmetic surgery": "../images/augmentations/cosmetic_surgery.gif",
    "fear blocker": "../images/augmentations/fear_blocker.gif",
    "wallhack": "../images/augmentations/wallhack.gif",
    "genetic surgery": "../images/augmentations/genetic_surgery.gif",
    "learning software": "../images/augmentations/learning_software.gif",
    "blessed by luck": "../images/augmentations/blessed_by_luck.gif"
}
# What other augmentations are there, and what do they do?
'''
def artificial_leg(char):
    # mobility + 2
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("artificial leg")
        char.mob += 2


def reflex_chip(char):
    # 10 % Chance each turn, that IC is reduced by 10, checked at turn function
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("reflex chip")


def kevlar_implant(char):
    # +20 max_HP, check at update_maxHP()
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("kevlar implant")


def eye_processor(char):
    # agility + 2
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("eye processor")
        char.agi += 2


def cosmetic_surgery(char):
    # all costs -10 BTC, checked at buy function
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("cosmetic surgery")


def fear_blocker(char):
    # Use guns in melee, checked at act function
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("fear blocker")


def wallhack(char):
    # No hitting malus because of barricades
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("wallhack")


def genetic_surgery(char):
    # Player can morph into a werewolf: double stats, dont use weapons while morphed
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    elif char.morph:
        print("ERROR: player can already turn into a werewolf")
    else:
        char.augmentations.append("genetic surgery")
        char.morph = True


def learning_software(char):
    # needed XP per level: -15, checked at levelup function
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("learning software")


def blessed_by_luck(char):
    # chance tests += 0.05, checked at chance function?
    if char.augmentations.length > 4:
        print("ERROR: already 3 augmentations")
    else:
        char.augmentations.append("blessed by luck")
'''
