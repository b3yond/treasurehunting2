#! /usr/bin/env python
# coding=utf-8
#
# Contents:
#
# 1. Imports
# 2. Classes
# 3. Functions

# # # # # # #
# 1.Imports #
# # # # # # #

from random import randint
import items
import augmentations
import enemies
from editor import *
import pygtk
import pickle
import os
import gtk
import sdl2
import sdl2.ext
import sys
import ctypes
from sdl2.sdlttf import (TTF_OpenFont,
                         TTF_RenderText_Shaded,
                         TTF_GetError,
                         TTF_Init,
                         TTF_Quit
                         )

pygtk.require("2.0")


# # # # # # #
# 2.Classes #
# # # # # # #

# Characters
class Individuum(object):
    """
    This is the main character class, originally not only for player
    characters, but I failed and made Enemies their own super class.
    subclasses:
    Vampire, Angel, Human, Werewolf, Golem.
    """

    def __init__(self, name, race, con, str, mob, agi, int):
        self.name = name
        self.race = race
        self.con = con  # Constitution
        self.str = str  # Strength
        self.agi = agi  # Agility
        self.mob = mob  # Mobility
        self.int = int  # Intelligence
        self.max_hp = self.con * 8 + self.str * 5 + 10
        self.id = enemies.getenemyid()
        self.hp = self.max_hp
        self.ic = 0  # Initiative Counter
        self.inventory = []  # List of Objects
        self.augmentations = []  # List of Strings
        self.bitcoins = 150  # Integer
        self.level = 1  # There is no max. level, I think
        self.experience = 0  # set back to 0 when level increments in levelup()
        self.gun = items.Gun("No gun", 0, "", 0, 0, 0)  # drawn gun
        self.sword = items.Sword("Fist", 0, "", 50, 0.0, 0.3, 0, False)  # drawn sword

    def update_max_hp(self):
        """
        to update the max health points
        triggered in levelup()
        :rtype: object
        """
        if "kevlar_implant" in self.augmentations:
            self.max_hp = self.con * 8 + self.str * 5 + 30
        else:
            self.max_hp = self.con * 8 + self.str * 5 + 10

    def walk_ap(self):
        """
        returns, how many AP 1 step is costing
        :return: integer
        """
        walk_ap = 100 / self.mob
        return walk_ap

    def print_char(self):
        """
        prints out the character screen. for this time it is in CLI
        mode, maybe once with GUI.
        :return: -
        """
        print("Information - Attributes - Values")
        print self.name, (14 - len(self.name)) * " ",
        print "| Intelligence: ", str(self.int),
        print "| HP: ", str(self.hp), "/", self.max_hp
        print self.race, (14 - len(self.race)) * " ",
        print "| Constitution: ", str(self.con),
        print "| Initiative: ", str((self.mob * 3 + self.int * 5) / 10)
        print "Level: ", self.level, (6 - len(str(self.level))) * " ",
        print "| Strength:     ", str(self.str),
        print "| Range Hitting: ", str(self.agi * 7 + self.int * 3)
        print "BTC: ", self.bitcoins, (8 - len(str(self.bitcoins))) * " ",
        print "| Agility:      ", str(self.agi),
        print "| Melee Hitting: ", str(self.agi * 3 + self.str * 5)
        print "XP: ", self.experience, (9 - len(str(self.experience))) * " ",
        print "| Mobility:     ", str(self.mob),
        print "| Melee Defense: ", str(self.mob * 5 + self.con * 3)

    def save_profile(self):
        with open("../saves/" + self.name, "wb") as file:
            pickle.dump(self, file)


class Vampire(Individuum):
    """ race subclass """

    def __init__(self, name):
        super(Vampire, self).__init__(name, "Vampire", 6, 8, 5, 5, 5)


class Angel(Individuum):
    """ race subclass """

    def __init__(self, name):
        super(Angel, self).__init__(name, "Angel", 4, 3, 7, 7, 5)


class Human(Individuum):
    """ human race subclass

    not sure if this one is ever used...
    """

    def __init__(self, name):
        super(Human, self).__init__(name, "Human", 4, 5, 5, 4, 4)


class Werewolf(Individuum):
    """ race subclass """

    def __init__(self, name):
        super(Werewolf, self).__init__(name, "Werewolf", 4, 5, 5, 4, 4)
        # able to morph, can also be learned w/ augmentations - func for this?
        self.morph = True
        # should Claws be done differently? maybe doing more damage if morphed?
        # no, because there are also silver Claws asd
        self.inventory = [Sword("Claws", 50, "../images/swords/claws.gif", 50, 0.3, 0.6,
                                30, False)]


class Golem(Individuum):
    """ race subclass """

    def __init__(self, name):
        super(Golem, self).__init__(name, "Golem", 7, 8, 4, 4, 3)


class Mission(object):
    """ mission class
    success_func        # function to check if mission is accomplished
    rewardmoney         # integer
    rewarditems         # list of Item-objects
    rewardxp            # integer
    description         # string
    room                # Room-object where to start
    current_room        # Room where the player is
    rooms               # list of Room objects
    target_item         # string (name of item) - default: None
    target_enemy        # integer (how many enemies have target attribute) - default: 0
    target_coordinates  # list (x,y,roomID) - default: None
    """

    def __init__(self, money, items, xp, description, room, rooms, target_item,
                 target_enemy, target_coordinates):
        self.rewardmoney = money
        self.rewarditems = items
        self.rewardxp = xp
        self.description = description
        self.room = room
        self.current_room = room
        self.rooms = rooms
        self.target_item = target_item
        self.target_enemy = target_enemy
        self.target_coordinates = target_coordinates

    def success_func(self, player):
        """ Tests if the mission was a success

        There are several possible conditions, if a mission has succeeded.
        They are True by default. This function calls other function which
        return values of the current status. If all are True, Success.
        :return: boolean
        """
        current = [
            self.item_owned(player),
            self.enemy_killed(),
            self.at_position(player, self.current_room)
        ]
        for a in current:
            if a == False:
                return False
        print current
        player.bitcoins += self.rewardmoney
        player.experience += self.rewardxp
        for i in self.rewarditems:
            player.inventory.add(i)
        return True

    def item_owned(self, player):
        if self.target_item == None:
            return True
        if self.target_item in player.inventory:
            return True
        return False

    def enemy_killed(self):
        if self.target_enemy == 0:
            return True
        return False

    def at_position(self, player, room):
        if self.target_coordinates == None:
            return True
        if self.target_coordinates[2] == room.id:
            if self.target_coordinates[0] == player.x:
                if self.target_coordinates[1] == player.y:
                    return True
        return False


class Room(object):
    """ room class
    fields      # list of lists
    field data  # dictionary for field data
    description # string - necessary?
    """

    def __init__(self, fields, fielddata, description):
        self.fields = fields
        self.fielddata = fielddata
        self.description = description
        self.id = id(self)


class Panel(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx, posy):
        # super(Panel, self).__init__(world)
        self.sprite = sprite
        self.sprite.position = posx, posy


class TextSprite(sdl2.ext.TextureSprite):
    """
    font_cache: Dictionary { (font, fontsize) : TTF_OpenFont(font, fontsize) }
    """
    font_cache = {}

    def __init__(self, renderer, font=None, text="", fontsize=24,
                 textcolor=sdl2.pixels.SDL_Color(255, 255, 255),
                 background=sdl2.pixels.SDL_Color(30, 30, 30), depth=20):
        self.renderer = renderer.renderer
        if (font, fontsize) not in self.font_cache:
            self.font_cache[(font, fontsize)] = TTF_OpenFont(font, fontsize)
        self.font = self.font_cache.get((font, fontsize))
        self._text = text
        self.fontsize = fontsize
        self.fontcolor = textcolor
        self.background = background
        self.depth = depth
        texture = self._createTexture()

        super(TextSprite, self).__init__(texture)

    def _createTexture(self):
        textSurface = TTF_RenderText_Shaded(self.font, self._text, self.fontcolor, self.background)
        if textSurface is None:
            raise TTF_GetError()
        texture = sdl2.render.SDL_CreateTextureFromSurface(self.renderer, textSurface)
        if texture is None:
            raise sdl2.ext.SDLError()
        sdl2.surface.SDL_FreeSurface(textSurface)
        return texture

    def _updateTexture(self):
        textureToDelete = self.texture

        texture = self._createTexture()
        super(TextSprite, self).__init__(texture)

        sdl2.render.SDL_DestroyTexture(textureToDelete)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value
        self._updateTexture()


class SDLInstanceManager(object):
    """ Contains all the pySDL2-instances.

    Is given from function to function, so I don't have to give each instance on its own.
    replaces sdllist
    """

    def __init__(self):
        """ creates the instances, starts the window. """
        sdl2.ext.init()
        TTF_Init()
        self.window = sdl2.ext.Window("Treasure Hunting 2", size=(800, 600))
        self.window.show()
        self.renderer = sdl2.ext.Renderer(self.window)
        self.factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=self.renderer)
        self.uifactory = sdl2.ext.UIFactory(self.factory)
        self.world = sdl2.ext.World()
        self.spriterenderer = sdl2.ext.TextureSpriteRenderSystem(self.renderer)
        self.uiprocessor = sdl2.ext.UIProcessor()
        self.console = Consolescreen(self.world, self.renderer)

        self.world.add_system(self.spriterenderer)
        self.world.add_system(self.uiprocessor)


class Consolescreen(object):
    """ Instance to control the Console output.

    call Consolescreen.push(line) to add a new line to the Console.
    """

    def __init__(self, world, renderer):
        self.lines = [" ", " ", " ", " ", " "]
        self.world = world
        self.renderer = renderer
        self.sprites = []
        self.sprites = self.create_sprites()
        self.show_console = True

    def process(self):
        self.sprites = []
        if self.show_console:
            self.create_sprites()

    def create_sprites(self):
        y = 505
        for i in self.lines:
            self.sprites.append(create_text(self.world, self.renderer, "  " + i, 215, y, fontsize=13,
                                            background=sdl2.pixels.SDL_Color(0, 0, 0)))
            y += 15

    def push(self, text):
        del self.lines[0]
        self.lines.append(text)
        try:
            self.delete()
        except TypeError:
            pass
        self.process()

    def tooltip_gun(self, item):
        self.infotext = []
        self.infotext.append(create_text(self.world, self.renderer, item[0], 215, 505,
                                         fontsize=13, background=sdl2.pixels.
                                         SDL_Color(150, 200, 30)))
        self.infotext.append(create_text(self.world, self.renderer, "BTC: " + str(item[1]),
                                         215, 520, fontsize=13, background=sdl2.pixels.SDL_Color
            (150, 200, 30)))
        self.infotext.append(create_text(self.world, self.renderer, "Damage: " +
                                         str(item[3]), 215, 535, fontsize=13,
                                         background=sdl2.pixels.SDL_Color(150, 200, 30)))
        self.infotext.append(create_text(self.world, self.renderer, "AP: " +
                                         str(item[5]), 215, 550, fontsize=13,
                                         background=sdl2.pixels.SDL_Color(150, 200, 30)))
        for i in self.infotext:
            self.sprites.append(i)

    def tooltip_sword(self, item):
        self.infotext = []
        self.infotext.append(create_text(self.world, self.renderer, item[0], 215, 505,
                                         fontsize=13, background=sdl2.pixels.
                                         SDL_Color(150, 200, 30)))
        self.infotext.append(create_text(self.world, self.renderer, "BTC: " + str(item[1]),
                                         215, 505 + 15, fontsize=13, background=sdl2.pixels.SDL_Color
            (150, 200, 30)))
        self.infotext.append(create_text(self.world, self.renderer, "Damage: " +
                                         str(item[6]), 215, 505 + 30, fontsize=13,
                                         background=sdl2.pixels.SDL_Color(150, 200, 30)))
        self.infotext.append(create_text(self.world, self.renderer, "AP: " +
                                         str(item[3]), 215, 505 + 45, fontsize=13,
                                         background=sdl2.pixels.SDL_Color(150, 200, 30)))
        for i in self.infotext:
            self.sprites.append(i)

    def delete(self):
        for i in self.sprites:
            self.world.delete(i)


class Charwindow(object):
    def __init__(self, player, m):
        self.player = player
        self.world = m.world
        self.renderer = m.renderer
        self.factory = m.factory
        self.uifactory = m.uifactory

        self.characterpanel = create_panel(self.world, self.factory, "panels2/charwinbackground.gif",
                                           10, 460, -19)
        self.inventorypanel = create_panel(self.world, self.factory, "panels2/inventorybackground.gif",
                                           550, 460, -19)
        self.augmentationpanel = create_panel(self.world, self.factory, "panels2/augframe.gif", 510,
                                              460, -19)

        self.charwidgets = self.build_charwin()
        self.invwidgets = self.build_inventory_panels()
        self.augwidgets = self.build_aug_panels()
        self.process()

    def build_charwin(self):
        widgets = []
        pl = self.player
        if "learning software" in pl.augmentations:
            lvlup = pl.experience > pl.level * 10 - 15
        else:
            lvlup = pl.experience > pl.level * 10
        line1 = "%s - Level %s" % (pl.name, pl.level)
        line2 = "HP %d/%d - BTC %d" % (pl.hp, pl.max_hp, pl.bitcoins)
        line3 = "INT %d       Ini %d" % (pl.int, (pl.mob * 3 + pl.int * 5) / 10)
        line4 = "CON %d     Aim %d" % (pl.con, pl.agi * 7 + pl.int * 3)
        line5 = " STR %d      Hit %d" % (pl.str, pl.agi * 3 + pl.str * 5)
        line6 = "  AGI %d     Def %d" % (pl.agi, pl.mob * 5 + pl.con * 3)
        line7 = "MOB %d     XP %d/%d" % (pl.mob, pl.experience, lvlup)
        widgets.append(create_text(self.world, self.renderer, line1, 15, 465, fontsize=13))
        widgets.append(create_text(self.world, self.renderer, line2, 15, 483, fontsize=13))
        widgets.append(create_text(self.world, self.renderer, line3, 15, 501, fontsize=13))
        widgets.append(create_text(self.world, self.renderer, line4, 15, 519, fontsize=13))
        widgets.append(create_text(self.world, self.renderer, line5, 15, 537, fontsize=13))
        widgets.append(create_text(self.world, self.renderer, line6, 15, 555, fontsize=13))
        widgets.append(create_text(self.world, self.renderer, line7, 15, 573, fontsize=13))
        widgets.append(create_panel(self.world, self.factory, "races/" + pl.race + ".gif",
                                    155, 470))
        return widgets

    def build_inventory_panels(self):
        widgets = []
        self.buttons = []
        pl = self.player
        x = 555
        y = 465
        for item in pl.inventory:
            widgets.append(create_panel(self.world, self.factory, item.image, x, y))
            button = create_button(self.world, self.uifactory, size=(25, 25), pos=(x, y))
            self.buttons.append(button)
            x += 30
            if x > 740:
                y += 30
        return widgets

    def build_aug_panels(self):
        widgets = []
        pl = self.player
        x = 510
        y = 460
        for aug in pl.augmentations:
            widgets.append(create_panel(self.world, self.factory,
                                        augmentations.all_augmentations[aug], x, y))
            y += 30
        return widgets

    def process(self):
        self.delete()
        self.charwidgets = self.build_charwin()
        self.invwidgets = self.build_inventory_panels()
        self.augwidgets = self.build_aug_panels()
        self.characterpanel = create_panel(self.world, self.factory,
                                           "panels2/charwinbackground.gif", 10, 460, -19)
        self.inventorypanel = create_panel(self.world, self.factory,
                                           "panels2/inventorybackground.gif", 550, 460, -19)
        self.augmentationpanel = create_panel(self.world, self.factory,
                                              "panels2/augframe.gif", 510, 460, -19)

    def delete(self):
        for i in self.charwidgets:
            self.world.delete(i)
        for i in self.invwidgets:
            self.world.delete(i)
        for i in self.augwidgets:
            self.world.delete(i)
        self.world.delete(self.characterpanel)
        self.world.delete(self.inventorypanel)
        self.world.delete(self.augmentationpanel)


class ItemButton(object):
    """ Class for the item button in the merchant window """

    def __init__(self, m, item, x, y):
        """
        :param m: SDLInstanceManager object
        :param item: list of item properties, i[0] = name, i[2] = image
        :param x: integer
        :param y: integer
        """
        self.world = m.world
        self.factory = m.factory
        self.uifactory = m.uifactory
        self.item = item
        self.button = create_button(self.world, self.uifactory, size=(30, 30), pos=(x, y))
        self.panel = create_panel(self.world, self.factory, item[2], x, y)

    def delete(self):
        self.world.delete(self.button)
        self.world.delete(self.panel)


# # # # # # # #
# 3.Functions #
# # # # # # # #

"""
 pySDL2-functions
"""
def get_mouse_position():
    """ Get mouse coordinates

    http://stackoverflow.com/questions/27322219/how-to-get-mouse-position-using-pysdl2
    :return: x, y integers of mouse position
    """
    x, y = ctypes.c_int(0), ctypes.c_int(0)  # Create two ctypes values
    # Not needed: Pass x and y as references (pointers) to SDL_GetMouseState()
    buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
    # Print x and y as "native" ctypes values
    # print(x, y)
    # Print x and y as Python values
    return x.value, y.value


def create_panel(world, factory, imagepath, x, y, depth=0):
    """ create an Entity.

    :param world: World object
    :param factory: SpriteFactory object
    :param imagepath: string, path to sprite image
    :param x: integer, horizontal position
    :param y: integer, vertical position
    :return: Panel object
    """
    sprite = factory.from_image("../images/" + imagepath)
    sprite.depth = depth
    return Panel(world, sprite, x, y)


def create_text(world, renderer, text, x, y, fontsize=24, depth=20,
                background=sdl2.pixels.SDL_Color(30, 30, 30)):
    """ Creates a text display Entity.

    font is default.
    fontsize is default 24.
    :param world: World object
    :param renderer: Renderer object
    :param text: string
    :param x: integer, position
    :param y: integer, position
    :return: Panel object
    """
    font = "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf"
    sprite = TextSprite(renderer, font, text, fontsize=fontsize, background=background,
                        depth=depth)
    return Panel(world, sprite, x, y)


def create_button(world, uifactory, size=(15, 15), pos=(0, 0), depth=-25):
    """ Creates a clickable button object.

    :param world: World object
    :param uifactory: SpriteFactory object
    :param size: tuple of integers, (x,y)
    :param pos: tuple of integers, coordinates, (x,y)
    :param depth: integer, layering
    :return: Entity object
    """
    newgame_button = uifactory.create_button(size=size)
    newgame_button.depth = depth
    newgame_entity = Panel(world, newgame_button, pos[0], pos[1])
    return newgame_entity


def delete_entitylist(world, entities):
    """ delete Entity objects.

    :param entities: List of Entity objects
    :return world: World object
    """
    for i in entities:
        world.delete(i)
    return world


"""
 functions to create ingame data
"""


def build_enemy(enemydata):
    """ build an enemy object from given data

    :param enemydata: list of arguments to Enemy()
    :return: output: enemy object
    """
    ed = enemydata
    output = enemies.Enemy(ed[0], ed[1], ed[2], ed[3], ed[4], ed[5], ed[6], ed[7],
                           ed[8], ed[9], [ed[10][0], ed[10][1]], ed[11])
    return output


def build_battlefield(player, mission):
    """ build up the mission list and foelist

    This will probably be replaced with a GUI function. for now it returns:
    :param player: Individuum object
    :param mission: Mission object
    :return mission, player
    """
    fields = mission.current_room.fields
    fielddata = mission.current_room.fielddata
    mission.current_room.foelist = [player]
    with open("../resources/enemies", "rb") as file:
        enemydict = pickle.load(file)

    for i in fields:
        for j in i:
            if j in fielddata:
                # dont try to call on Doors
                for enemy in enemydict:
                    if fielddata[j] == enemydict[enemy][0]:
                        print(enemydict[enemy][0])
                        mission.current_room.foelist.append(build_enemy(enemydict[enemy]))
                for room in mission.rooms:
                    if j == room.id:
                        pass  # display door?
    for i in mission.current_room.foelist:
        print i.name
    for x in range(len(fields)):
        for y in range(len(fields[x])):
            if fields[x][y] == 0:
                player.x = x
                player.y = y
    return mission, player


def build_gun(gd):
    """ Build a gun object

    :param gd: gundata, list with arguments to Gun()
    :return: output: Gun object
    """
    output = items.Gun(gd[0], gd[1], gd[2], gd[3], gd[4], gd[5])
    return output


def build_sword(sd):
    """ Build a sword object

    :param sd: sworddata, lists with arguments to Sword()
    :return: output: Sword object
    """
    output = items.Sword(sd[0], sd[1], sd[2], sd[3], sd[4], sd[5], sd[6], sd[7])
    return output


"""
 menu-functions
"""
def main_menu_sdl():
    """ create window and show main menu.

    calls new_game_sdl(), load_game_sdl()
    """
    m = SDLInstanceManager()

    # add background panels
    mainmenu = True
    while mainmenu:
        highpanel = create_panel(m.world, m.factory, "panels2/highpanel.gif", 0, 0, -20)
        leftpanel = create_panel(m.world, m.factory, "panels2/leftpanel.gif", 0, 450, -20)
        midpanel = create_panel(m.world, m.factory, "panels2/rightmidpanel.gif", 200, 450, -20)
        rightpanel = create_panel(m.world, m.factory, "panels2/rightmidpanel.gif", 500, 450, -20)
        consolepanel = create_panel(m.world, m.factory, "panels2/consolebackground.gif", 210, 500, -19)

        # panellist = [highpanel, leftpanel, midpanel, rightpanel]

        # mainmenu_text = create_text(world, renderer, " MAIN MENU ", 20, 290)
        newgame_text = create_text(m.world, m.renderer, " new game ", 20, 330)
        loadgame_text = create_text(m.world, m.renderer, " choose game ", 20, 370)
        quit_text = create_text(m.world, m.renderer, " quit ", 20, 410)

        newgame_entity = create_button(m.world, m.uifactory, (100, 29), (20, 330))
        loadgame_entity = create_button(m.world, m.uifactory, (128, 29), (20, 370))
        quit_entity = create_button(m.world, m.uifactory, (41, 29), (20, 410))

        textlist = [newgame_text, loadgame_text, quit_text]
        entitylist = [newgame_entity, loadgame_entity, quit_entity]

        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                m.uiprocessor.dispatch(m.world, event)
                if event.type == sdl2.SDL_QUIT:
                    m.console.push("Good Bye.")
                    sdl2.ext.quit()
                    exit(0)
                if newgame_entity.sprite.state == 3:
                    delete_entitylist(m.world, entitylist)
                    delete_entitylist(m.world, textlist)
                    m.console.push("Starting new game.")
                    new_game_sdl(m)
                    running = False
                    break
                elif loadgame_entity.sprite.state == 3:
                    delete_entitylist(m.world, entitylist)
                    delete_entitylist(m.world, textlist)
                    m.console.push("Choosing Game.")
                    load_game_sdl(m)
                    running = False
                    break
                elif quit_entity.sprite.state == 3:
                    m.console.push("Good Bye.")
                    running = False
                    mainmenu = False
                    break
            m.world.process()


def new_game_sdl(m):
    """
    :param m: SDLInstanceManager object
    :return:
    """
    name_input_sprite = m.uifactory.create_text_entry(size=(220, 29))
    name_input_sprite.depth = 15
    name_input_entity = Panel(m.world, name_input_sprite, 20, 250)

    name_input_text = create_text(m.world, m.renderer, " Click here and enter text ", 20, 250)

    vampire_text = create_text(m.world, m.renderer, " vampire ", 20, 290)
    golem_text = create_text(m.world, m.renderer, " golem ", 20, 330)
    angel_text = create_text(m.world, m.renderer, " angel ", 20, 370)
    werewolf_text = create_text(m.world, m.renderer, " werewolf ", 20, 410)
    back_panel = create_panel(m.world, m.factory, "panels2/backbutton.gif", 210, 460, 20)

    vampire_entity = create_button(m.world, m.uifactory, (81, 29), (20, 290))
    golem_entity = create_button(m.world, m.uifactory, (63, 29), (20, 330))
    angel_entity = create_button(m.world, m.uifactory, (57, 29), (20, 370))
    werewolf_entity = create_button(m.world, m.uifactory, (88, 29), (20, 410))
    back_button = create_button(m.world, m.uifactory, (25, 25), (210, 460))
    widgetlist = [name_input_sprite, name_input_text, name_input_entity, vampire_entity,
                  vampire_text, golem_entity, golem_text, angel_entity, angel_text,
                  werewolf_entity, werewolf_text, back_panel, back_button]

    running = True
    while running:
        events = sdl2.ext.get_events()
        # name_input_text = create_text(m.world, m.renderer, name_input_sprite.text, 20, 250, depth=10)
        for event in events:
            m.uiprocessor.dispatch(m.world, event)
            if event.type == sdl2.SDL_QUIT:
                m.console.push("Good Bye.")
                running = False
                break
            if vampire_entity.sprite.state == 3:
                m.console.push("You chose to be a Vampire.")
                race = "Vampire"
                if name_input_sprite.text != "":
                    name = name_input_sprite.text
                    player = Vampire(name)
                    running = False
                    break
            elif golem_entity.sprite.state == 3:
                m.console.push("You chose to be a Golem.")
                race = "Golem"
                if name_input_sprite.text != "":
                    name = name_input_sprite.text
                    player = Golem(name)
                    running = False
                    break
            elif angel_entity.sprite.state == 3:
                m.console.push("You chose to be an Angel.")
                race = "Angel"
                if name_input_sprite.text != "":
                    name = name_input_sprite.text
                    player = Angel(name)
                    running = False
                    break
            elif werewolf_entity.sprite.state == 3:
                m.console.push("You chose to be a Werewolf.")
                race = "Werewolf"
                if name_input_sprite.text != "":
                    name = name_input_sprite.text
                    player = Werewolf(name)
                    running = False
                    break
            if back_button.sprite.state == 3:
                m.console.push("Back to Main Menu.")
                running = False
                break
        m.world.process()
    delete_entitylist(m.world, widgetlist)
    try:
        player.save_profile()
        m.console.push("Saving character...")
    except UnboundLocalError:
        pass


def load_game_sdl(m):
    """ Chooses a game and continues to profile.

    :param m: SDLInstanceManager object
    """
    saved_games = os.listdir("../saves")
    panels = []
    buttons = []
    x = 20
    y = 410
    widgetlist = []
    for i in range(len(saved_games)):
        panels.append(create_text(m.world, m.renderer, saved_games[i], x, y))
        buttons.append(create_button(m.world, m.uifactory, (100, 29), (x, y)))
        buttons[i].title = saved_games[i]
        y -= 40
        if y < 100:
            x += 140
            y = 410

    widgetlist.append(create_panel(m.world, m.factory, "panels2/backbutton.gif", 210, 460, 20))
    widgetlist.append(create_button(m.world, m.uifactory, (25, 25), (210, 460)))
    for i in buttons:
        widgetlist.append(i)
    for i in panels:
        widgetlist.append(i)

    running = True
    while running:
        events = sdl2.ext.get_events()
        # name_input_text = create_text(m.world, m.renderer, name_input_sprite.text, 20, 250, depth=10)
        for event in events:
            m.uiprocessor.dispatch(m.world, event)
            if event.type == sdl2.SDL_QUIT:
                m.console.push("Good Bye.")
                running = False
                break
            if widgetlist[1].sprite.state == 3:
                m.console.push("Back to Main Menu.")
                delete_entitylist(m.world, widgetlist)
                running = False
                break
            for i in range(len(buttons)):
                if buttons[i].sprite.state == 3:
                    name = saved_games[i]
                    with open("../saves/" + name, "rb", ) as file:
                        player = pickle.load(file)
                    delete_entitylist(m.world, widgetlist)
                    m = profile_sdl(m, player)
                    running = False
                    break
        m.world.process()


def build_profile_sdl(m, player):
    """
    :param player: Individuum object
    :param m: SDLInstanceManager object
    :param new_char_window: boolean, if there shall be created a new charwindow.
    :return:
    """
    widgetlist = []
    widgetlist.append(create_panel(m.world, m.factory, "panels2/backbutton.gif", 210, 460, 20))
    widgetlist.append(create_button(m.world, m.uifactory, (25, 25), (210, 460)))

    m.charwin = Charwindow(player, m)

    merchant_text = create_text(m.world, m.renderer, " merchant ", 20, 370)
    startmission_text = create_text(m.world, m.renderer, " start mission ", 20, 410)

    merchant_entity = create_button(m.world, m.uifactory, (92, 29), (20, 370))
    startmission_entity = create_button(m.world, m.uifactory, (120, 29), (20, 410))
    widgetlist.append(merchant_entity)
    widgetlist.append(merchant_text)
    widgetlist.append(startmission_entity)
    widgetlist.append(startmission_text)

    m.console.push("Welcome, " + player.name + "!")
    return widgetlist, m


def profile_sdl(m, player):
    """ Displays player data and profile options.

    Game Options: Merchant, Start Mission
    TODO creating infotexts if hovering over buttons.
    :param m: SDLInstanceManager object
    :param player: Individuum object
    """
    widgetlist, m = build_profile_sdl(m, player)

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            m.uiprocessor.dispatch(m.world, event)
            if event.type == sdl2.SDL_QUIT:
                m.console.push("Good Bye.")
                sdl2.ext.quit()
                exit(0)
            # Backbutton
            if widgetlist[1].sprite.state == 3:
                m.console.push("Back to Main Menu.")
                delete_entitylist(m.world, widgetlist)
                running = False
                break
            if widgetlist[2].sprite.state == 3:
                m.console.push("Shopping.")
                delete_entitylist(m.world, widgetlist)
                player, m = merchant_sdl(player, m)
                player.save_profile()
                widgetlist, m = build_profile_sdl(m, player)
                m.charwin.process()
                break
            if widgetlist[4].sprite.state == 3:
                m.console.push("Let's get a job.")
                delete_entitylist(m.world, widgetlist)
                mission = choose_mission(m)
                try:
                    player = run_mission(m, player, mission)
                except AttributeError:
                    m.console.push("Back to Profile.")
                    widgetlist, m = build_profile_sdl(m, player)
                    m.charwin.process()
                    break
                with open("../saves/" + player.name, mode='w') as file:
                    pickle.dump(player, file)
                m.console.push("Game Saved.")
                running = False
                break
        m.charwin.process()
        m.world.process()
    m.charwin.delete()
    del m.charwin
    return m


def choose_mission(m):
    """ Choose a level

    :param m: SDLInstanceManager object
    :param player: Individuum object
    :return: Mission object
    """
    all_missions = os.listdir("../missions")
    panels = []
    buttons = []
    x = 20
    y = 410
    widgetlist = []
    widgetlist.append(create_panel(m.world, m.factory, "panels2/backbutton.gif", 210, 460, 20))
    widgetlist.append(create_button(m.world, m.uifactory, (25, 25), (210, 460)))

    for i in range(len(all_missions)):
        panels.append(create_text(m.world, m.renderer, all_missions[i], x, y))
        buttons.append(create_button(m.world, m.uifactory, (100, 29), (x, y)))
        buttons[i].title = all_missions[i]
        y -= 40
        if y < 100:
            x += 140
            y = 410

    for i in buttons:
        widgetlist.append(i)
    for i in panels:
        widgetlist.append(i)

    running = True
    while running:
        events = sdl2.ext.get_events()
        # name_input_text = create_text(m.world, m.renderer, name_input_sprite.text, 20, 250, depth=10)
        for event in events:
            m.uiprocessor.dispatch(m.world, event)
            if event.type == sdl2.SDL_QUIT:
                m.console.push("Good Bye.")
                running = False
                break
            # Backbutton
            if widgetlist[1].sprite.state == 3:
                m.console.push("Back to Main Menu.")
                delete_entitylist(m.world, widgetlist)
                running = False
                break
            for i in range(len(buttons)):
                if buttons[i].sprite.state == 3:
                    name = all_missions[i]
                    with open("../missions/" + name, "rb", ) as file:
                        mission = pickle.load(file)
                    m.console.push("You are now starting the mission \'" + name + "\'.")
                    delete_entitylist(m.world, widgetlist)
                    return mission
        m.world.process()


"""
 merchant-functions
"""
def merchant_sdl(player, m):
    """ Buy items, spells and augmentations.

    TODO
    create Spells to buy
    create Buttons for every item to sell, analogous to the existing item panels.
    create Buttons for every aug to sell, analogous to the existing aug panels.
    creating infotexts if hovering over buttons.
    :param player: Individuum object
    :param m: SDLInstanceManager object
    :return: player: Individuum object
    """
    widgetlist = []
    # Backbutton
    widgetlist.append(create_panel(m.world, m.factory, "panels2/backbutton.gif", 210, 460, 20))
    widgetlist.append(create_button(m.world, m.uifactory, (25, 25), (210, 460)))

    # Headlines
    widgetlist.append(create_text(m.world, m.renderer, " Guns ", 10, 20))
    widgetlist.append(create_text(m.world, m.renderer, " Swords ", 170, 20))
    widgetlist.append(create_text(m.world, m.renderer, " Spells ", 410, 20))
    widgetlist.append(create_text(m.world, m.renderer, " Augmentations ", 650, 20))

    # Getting Resources
    with open("../resources/guns", "r+") as file:
        allguns = pickle.load(file)
    with open("../resources/swords", "r+") as file:
        allswords = pickle.load(file)

    # Creating Gun Buttons
    gunlist = []
    x = 10
    y = 70
    for i in allguns:
        gunlist.append(ItemButton(m, i, x, y))
        x += 30
        if x > 150:
            x = 10
            y += 30

    # Creating Sword Buttons
    swordlist = []
    x = 170
    y = 70
    for i in allswords:
        if i[2] != "":
            swordlist.append(ItemButton(m, i, x, y))
        x += 30
        if x > 400:
            x = 170
            y += 30

    # Creating Augmentations Buttons
    auglist = []
    x = 650
    y = 70
    for i in augmentations.all_augmentations:
        lst = [i, 0, augmentations.all_augmentations[i]]
        auglist.append(ItemButton(m, lst, x, y))
        x += 35
        if x > 760:
            x = 650
            y += 35

    # set previous state, so you can detect state changes
    for i in swordlist:
        i.old_state = 0
    for i in gunlist:
        i.old_state = 0

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            m.uiprocessor.dispatch(m.world, event)
            if event.type == sdl2.SDL_QUIT:
                m.console.push("Good Bye.")
                sdl2.ext.quit()
                exit(0)
            # Backbutton
            if widgetlist[1].sprite.state == 3:
                m.console.push("Back to Profile.")
                delete_entitylist(m.world, widgetlist)
                running = False
                break
            for i in gunlist:
                if i.button.sprite.state == 3:
                    buy_gun_sdl(player, i.item, m)
                # check if Tooltip shall be shown
                if i.button.sprite.state == 1:
                    if i.old_state == 0:
                        m.console.delete()
                        m.console.tooltip_gun(i.item)
                        info_text_shown = i
                        m.console.showconsole = False
                        i.old_state = 1
                try:
                    # check if Tooltip shall disappear
                    if info_text_shown.button.sprite.state == 0:
                        if i.old_state == 1:
                            m.console.showconsole = True
                            m.console.delete()
                            m.console.process()
                            i.old_state = 0
                except UnboundLocalError:
                    pass
            for i in swordlist:
                if i.button.sprite.state == 3:
                    buy_sword_sdl(player, i.item, m)
                # check if Tooltip shall be shown
                if i.button.sprite.state == 1:
                    if i.old_state == 0:
                        m.console.delete()
                        m.console.tooltip_sword(i.item)
                        info_text_shown = i
                        m.console.showconsole = False
                        i.old_state = 1
                try:
                    # check if Tooltip shall disappear
                    if info_text_shown.button.sprite.state == 0:
                        if i.old_state == 1:
                            m.console.showconsole = True
                            m.console.delete()
                            m.console.process()
                            i.old_state = 0
                except UnboundLocalError:
                    pass
            for i in auglist:
                if i.button.sprite.state == 3:
                    augmentations.augment(player, i.item[0], m)
        m.charwin.process()
        m.world.process()
    m.charwin.delete()
    del m.charwin
    for i in gunlist:
        i.delete()
    for i in swordlist:
        i.delete()
    for i in auglist:
        i.delete()
    return player, m


def buy_sword_sdl(player, sword, m):
    """
    :param player: Individuum object
    :param sword: list of gun properties: name, price, image, damage, grange, ap
    :param m:
    :return: player: Individuum object
    """
    # Does the player have enough money?
    if "cosmetic surgery" in player.augmentations:
        cost = sword[1] - 10
    else:
        cost = sword[1]
    if player.bitcoins < cost:
        m.console.push("You don't have " + str(cost) + " Bitcoins for " + sword[0] + ".")
    else:
        player.bitcoins -= cost
        player.inventory.append(build_sword(sword))
        m.console.push("You have purchased " + sword[0] + ".")
    return player


def buy_gun_sdl(player, gun, m):
    """
    :param player: Individuum object
    :param gun: list of gun properties: name, price, image, damage, grange, ap
    :param m: SDLInstanceManager object
    :return: player: Individuum object
    """
    # Does the player have enough money?
    if "cosmetic surgery" in player.augmentations:
        cost = gun[1] - 10
    else:
        cost = gun[1]
    if player.bitcoins < cost:
        m.console.push("You don't have " + str(cost) + " Bitcoins for " + gun[0] + ".")
    else:
        player.bitcoins -= cost
        player.inventory.append(build_gun(gun))
        m.console.push("You have purchased " + gun[0] + ".")
    return player


"""
 level functions
"""


def run_mission(m, player, mission):
    """ mission function, goes from one room to the next
    :param m: SDLInstanceManager object
    :param player: Individuum object
    :param mission: Mission object
    :return: player
    """
    print mission.description  # debug
    while not mission.success_func(player):
        player, mission = run_room(m, player, mission)
    print player.bitcoins  # debug
    return player


def run_room(m, player, mission):
    """
    :param m: SDLInstanceManager object
    :param player: Individuum object
    :param mission: Mission object
    :return: player, mission
    """
    mission, player = build_battlefield(player, mission)
    running = True
    while running:
        widgetlist = display_fields(m, player, mission)
        # print "running"  # debug
        # print mission.current_room.fielddata  # debug
        events = sdl2.ext.get_events()
        for event in events:
            m.uiprocessor.dispatch(m.world, event)
            if event.type == sdl2.SDL_QUIT:
                m.console.push("Good Bye.")
                sdl2.ext.quit()
                exit(0)
        m.charwin.process()
        m.world.process()
    delete_entitylist(m.world, widgetlist)
    return player, mission


def display_fields(m, player, mission):
    """ displays the panels and buttons the player sees.
    :param m: SDLInstanceManager object
    :param player: Individuum object
    :param mission: Mission object
    :return: widgetlist: list of lists: [Panels, Buttons]
    """
    fields = mission.current_room.fields
    fielddata = mission.current_room.fielddata
    x = 2
    y = 2
    panels = []
    buttons = []

    for i in fielddata:
        print i, fielddata[i]
    panels.append(create_panel(m.world, m.factory,
                               "../images/panels2/emptyfields.gif", x, y, depth=-15))
    for i in range(len(fields)):
        for j in range(len(fields[i])):
            # print fields[i][j],  # debug
            # Player
            if fields[i][j] == 0:
                panels.append(create_panel(m.world, m.factory,
                                           "../images/characters/player.gif", x, y))
            # Walls
            if fields[i][j] == "W":
                panels.append(create_panel(m.world, m.factory,
                                           "../images/fields/wall.gif", x, y))
            # Barricades
            if fields[i][j] == "B":
                panels.append(create_panel(m.world, m.factory,
                                           "../images/fields/barricada.gif", x, y))
            # Treasure
            if fields[i][j] == "T":
                panels.append(create_panel(m.world, m.factory,
                                           "../images/fields/treasure.gif", x, y))
            # Enemy or Door?
            if fields[i][j] in fielddata:
                # Compare fielddata entry with door IDs
                for room in mission.rooms:
                    if fielddata[fields[i][j]] == str(room.id):
                            panels.append(create_panel(m.world, m.factory,
                                                       "../images/fields/door.gif", x, y))
                            print "door",  # debug
                # look for enemyname in fielddata
                name = fielddata[fields[i][j]]
                print name,
                for enemy in mission.current_room.foelist:
                    print enemy.name,
                    if enemy.name == name:
                        panels.append(create_panel(m.world, m.factory,
                                                   enemy.image, x, y))
                        enemy.button = create_button(m.world, m.uifactory)
                        buttons.append(enemy.button)
                        # print enemy.name,  # debug
            x += 15
        y += 15
        # print  # debug
    return [panels, buttons]




if __name__ == "__main__":
    sys.exit(main_menu_sdl())
