#! /usr/bin/env python
# coding=utf-8

# from random import randint


# Main Classes

class Item(object):
    """ major item class """

    def __init__(self, name, price, image):
        self.name = name  # string: item name
        self.price = price  # integer: price in BTC
        self.image = image  # string containing path to image


class Gun(Item):
    """ gun subclass """

    def __init__(self, name, price, image, damage, grange, ap):
        super(Gun, self).__init__(name, price, image)
        self.damage = damage  # Integer
        self.grange = grange  # Integer
        self.ap = ap  # Integer, AP needed to fire the gun
        self.type = "gun"


class Sword(Item):
    """ sword subclass """

    def __init__(self, name, price, image, ap, critical, stun, damage,
                 silverdamage):
        super(Sword, self).__init__(name, price, image)
        self.damage = damage  # integer: damage dealt
        self.ap = ap  # integer: ap needed to attack
        self.critical = critical  # float: chance to do critical damage
        self.stun = stun  # float: change to stun enemy
        self.silverdamage = silverdamage  # boolean: does extra damage to SUPs
        self.type = "sword"


"""
# Swords

# name
# price
# path to image (empty string until artwork is done)
# AP
# Critical ( Damage*2 )
# Stun
# Damage
# Silverdamage ( Damage*2 )

class Nosword(Sword):
    def __init__(self):
        super(Nosword, self).__init__("Fist", 0, "", 50, 0.0, 0.3, 0, False)


class Baton(Sword):
    def __init__(self):
        super(Baton, self).__init__("Baton", 20, "", 75, 0.0, 0.3, 20, False)


class Knife(Sword):
    def __init__(self):
        super(Knife, self).__init__("Knife", 20, "", 60, 0.2, 0.0, 30, False)


class Shortsword(Sword):
    def __init__(self):
        super(Shortsword, self).__init__("Short sword", 40, "", 90, 0.3, 0.0,
                                         50, False)


class Longsword(Sword):
    def __init__(self):
        super(Longsword, self).__init__("Long sword", 70, "", 120, 0.4, 0.1,
                                        70, False)


class NunChaku(Sword):
    def __init__(self):
        super(NunChaku, self).__init__("Nun-Chakus", 70, "", 80, 0.1, 0.7, 50,
                                       False)


class Mace(Sword):
    def __init__(self):
        super(Mace, self).__init__("Mace", 70, "", 100, 0.1, 0.5, 70, False)


class Claymore(Sword):
    def __init__(self):
        super(Claymore, self).__init__("Claymore", 120, "", 150, 0.3, 0.2,
                                       120, False)


class Katana(Sword):
    def __init__(self):
        super(Katana, self).__init__("Katana", 100, "", 110, 0.6, 0.1, 75,
                                     False)


class Silversword(Sword):
    def __init__(self):
        super(Silversword, self).__init__("Silver sword", 90, "", 120, 0.3,
                                          0.2, 50, True)


class Silverdagger(Sword):
    def __init__(self):
        super(Silverdagger, self).__init__("Silver dagger", 40, "", 60, 0.2,
                                           0.0, 30, True)


class Whip(Sword):
    def __init__(self):
        super(Whip, self).__init__("Silver whip", 60, "", 150, 0.7, 0.8, 30,
                                   True)


class Claws(Sword):
    def __init__(self):
        super(Claws, self).__init__("Claws", 50, "", 50, 0.3, 0.6, 30, False)


class Silverclaws(Sword):
    def __init__(self):
        super(Silverclaws, self).__init__("Silver Claws", 150, "", 50, 0.4,
                                          0.7, 30, True)


# Guns

# Name
# Cost
# Path to image (empty until artworks are done)
# Damage
# g(un)Range
# AP needed to fire gun
# max. 2 Upgrades


class Nogun(Gun):
    def __init__(self):
        super(Nogun, self).__init__("No gun", 0, "", 0, 0, 0)


class Glock(Gun):
    def __init__(self):
        super(Glock, self).__init__("Glock", 30, "", 10, 8, 100)


class Uzi(Gun):
    def __init__(self):
        super(Uzi, self).__init__("uzi", 50, "", 10, 6, 50)


class Ak74(Gun):
    def __init__(self):
        super(Ak74, self).__init__("Kalaschnikow", 80, "", 30, 10, 100)


class P90(Gun):
    def __init__(self):
        super(P90, self).__init__("p90 SMG", 60, "", 15, 8, 75)


class Sawnoffshotgun(Gun):
    def __init__(self):
        super(Sawnoffshotgun, self).__init__("Sawn-off shotgun", 30, "", 50,
                                             4, 150)


class Shotgun(Gun):
    def __init__(self):
        super(Shotgun, self).__init__("Shotgun", 80, "", 70, 6, 150)


class Awp(Gun):
    def __init__(self):
        super(Awp, self).__init__("Sniper rifle", 140, "", 90, 15, 175)


class M4(Gun):
    def __init__(self):
        super(M4, self).__init__("M4 carbine", 110, "", 25, 12, 75)


class Lmg(Gun):
    def __init__(self):
        super(Lmg, self).__init__("Light machine gun", 130, "", 10, 4, 25)


class AllItems:
    # buyableC(lasses) (!= buyableO(bjects)) This dictionary is needed in buy().
    def __init__(self):
        self.buyableswordsC = {
            "Baton": Baton, "Knife": Knife, "Short sword": Shortsword, "Long sword":
                Longsword, "Nun-Chakus": NunChaku, "Mace": Mace, "Claymore": Claymore,
            "Katana": Katana, "Silver dagger": Silverdagger, "Silver sword":
                Silversword, "Silver claws": Silverclaws, "Silver whip": Whip
        }
        self.buyablegunsC = {
            "Glock": Glock, "uzi": Uzi, "Kalaschnikow": Ak74, "p90 SMG": P90,
            "Sawn-off shotgun": Sawnoffshotgun, "Shotgun": Shotgun, "Sniper rifle":
                Awp, "M4 carbine": M4, "Light machine gun": Lmg
        }



"""

"""
nosword = Sword("Fist", 0, "", 50, 0.0, 0.3, 0, False)
baton = Sword("Baton", 20, "", 75, 0.0, 0.3, 20, False)
knife = Sword("Knife", 20, "", 60, 0.2, 0.0, 30, False)
shortsword = Sword("Short sword", 40, "", 90, 0.3, 0.0, 50, False)
longsword = Sword("Long sword", 70, "", 120, 0.4, 0.1, 70, False)
nunchaku = Sword("Nun-Chakus", 70, "", 80, 0.1, 0.7, 50, False)
mace = Sword("Mace", 70, "", 100, 0.1, 0.5, 70, False)
claymore = Sword("Claymore", 120, "", 150, 0.3, 0.2, 120, False)
katana = Sword("Katana", 100, "", 110, 0.6, 0.1, 75, False)
silversword = Sword("Silver sword", 90, "", 120, 0.3, 0.2, 50, True)
silverdagger = Sword("Silver dagger", 40, "", 60, 0.2, 0.0, 30, True)
whip = Sword("Silver whip", 60, "", 150, 0.7, 0.8, 30, True)
krallen = Sword("Claws", 50, "", 50, 0.3, 0.6, 30, False)
silverkrallen = Sword("Silver Claws", 150, "", 50, 0.4, 0.7, 30, True)

nogun = Gun("No gun", 0, "", 0, 0, 0)
glock = Gun("Glock", 30, "", 10, 8, 100)
uzi = Gun("Uzi", 50, "", 10, 6, 50)
ak74 = Gun("Kalaschnikow", 80, "", 30, 10, 100)
p90 = Gun("p90 SMG", 60, "", 15, 8, 75)
sawnoffshotgun = Gun("Sawn-off shotgun", 30, "", 50, 4, 150)
shotgun = Gun("Shotgun", 80, "", 70, 6, 150)
awp = Gun("Sniper rifle", 140, "", 90, 15, 175)
m4 = Gun("M4 Carbine", 110, "", 25, 12, 75)
lmg = Gun("Light machine gun", 130, "", 10, 4, 25)



# UPGRADES

Verlaengerter Lauf
R += 2
C: 60

Halbmantelgeschosse
D += 5
C: 60

Verbesserte Mechanik
F += 1
C: 60

Keramikwaffe # erhoeht Bewegunsgeschwindigkeit
movement += 1
C: 60

Silberkugeln
if target.race != "human":
    D += 10
C: 80


"""

"""
# List format:
"""
# Swords
nosword = ["Fist", 0, "", 50, 0.0, 0.3, 0, False]
baton = ["Baton", 20, "swords/baton.gif", 75, 0.0, 0.3, 20, False]
knife = ["Knife", 20, "swords/knife.gif", 60, 0.2, 0.0, 30, False]
shortsword = ["Short sword", 40, "swords/shortsword.gif", 90, 0.3, 0.0, 50, False]
longsword = ["Long sword", 70, "swords/longsword.gif", 120, 0.4, 0.1, 70, False]
nunchaku = ["Nun-Chakus", 70, "swords/nunchaku.gif", 80, 0.1, 0.7, 50, False]
mace = ["Mace", 70, "swords/mace.gif", 100, 0.1, 0.5, 70, False]
claymore = ["Claymore", 120, "swords/claymore.gif", 150, 0.3, 0.2, 120, False]
katana = ["Katana", 100, "swords/katana.gif", 110, 0.6, 0.1, 75, False]
silversword = ["Silver sword", 90, "swords/silversword.gif", 120, 0.3, 0.2, 50, True]
silverdagger = ["Silver dagger", 40, "swords/silverdagger.gif", 60, 0.2, 0.0, 30, True]
whip = ["Silver whip", 60, "swords/whip.gif", 150, 0.7, 0.8, 30, True]
krallen = ["Claws", 50, "swords/claws.gif", 50, 0.3, 0.6, 30, False]
silverkrallen = ["Silberkrallen", 30, "swords/silverclaws.gif", 50, 0.4, 0.7, 150, True]


# Guns
nogun = ["No gun", 0, "", 0, 0, 0]
glock = ["Glock", 30, "guns/glock.gif", 10, 8, 100]
uzi = ["Uzi", 50, "guns/uzi.gif", 10, 6, 50]
ak74 = ["Kalaschnikow", 80, "guns/kalaschnikow.gif", 30, 10, 100]
p90 = ["p90 SMG", 60, "guns/p90.gif", 15, 8, 75]
sawnoffshotgun = ["Sawn-off shotgun", 30, "guns/sawnoff.gif", 50, 4, 150]
shotgun = ["Shotgun", 80, "guns/shotgun.gif", 70, 6, 150]
awp = ["Sniper rifle", 140, "guns/sniper.gif", 90, 15, 175]
m4 = ["M4 Carbine", 110, "guns/m4carbine.gif", 25, 12, 75]
lmg = ["Light machine gun", 130, "guns/lmg.gif", 10, 4, 25]

allswords = [baton, knife, shortsword, longsword, nunchaku, mace, claymore, katana, silverdagger, silversword,
             silverkrallen, whip]
guns = [glock, uzi, ak74, p90, sawnoffshotgun, shotgun, awp, m4, lmg]
