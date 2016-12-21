#! /usr/bin/env python
# coding=utf-8
#
#
# contents:
# 1. Imports
# 2. Globals
# 3. Classes
# 4.



# # # # # # #
# 1.Imports #
# # # # # # #
import pickle
import pygtk
import game
import os
from enemies import *
from items import *
pygtk.require("2.0")
import gtk


# # # # # # #
# 2.Globals #
# # # # # # #




# # # # # # #
# 3.Classes #
# # # # # # #



class RoomEditor(object):
    """ Room Editor window class.

    Window contains a List of choosable fields on the right, the modifiable fields on the left,
    and can give certain fields other values, which go into Room.fielddata
    or it does when its ready >.<
    weird bug: Save&Quit doesnt close the window, but still returns a room object.
    """

    def __init__(self):
        self.chosen = "W"
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        self.box2 = gtk.HBox(False, 0)
        self.menubox = gtk.VBox(False, 0)

        # initialise list of lists: fields, later argument to Room()
        self.fields = []
        for i in range(30):
            self.fields.append([])
            for j in range(52):
                self.fields[i].append("O")
        # initialize dictionary: fielddata, later argument to Room()
        self.fielddata = {}
        self.show_fields()

        # List which contains the buttons to choose field types
        self.choose_buttons = []
        self.choose_buttons.append(self.add_button(i_wall(), self.choose_field,
                                                   box=self.menubox, arg="W"))
        self.choose_buttons.append(self.add_button(i_leer(), self.choose_field,
                                                   box=self.menubox, arg="O"))
        self.choose_buttons.append(self.add_button(i_barricada(), self.choose_field,
                                                   box=self.menubox, arg="B"))
        self.choose_buttons.append(self.add_button(i_treasure(), self.choose_field,
                                                   box=self.menubox, arg="T"))
        self.choose_buttons.append(self.add_button(i_player(), self.choose_field,
                                                   box=self.menubox, arg=0))
        self.choose_buttons.append(self.add_button(i_1one(), self.choose_field,
                                                   box=self.menubox, arg=1))
        self.choose_buttons.append(self.add_text_button("Give Option", self.choose_field,
                                                        box=self.menubox, arg="C"))
        self.choose_buttons.append(self.add_text_button("Save & Quit", self.savequit,
                                                        box=self.menubox))

        self.window.add(self.box2)
        self.box2.pack_end(self.menubox)  # Vertical Box, for choosing Buttons

        self.menubox.show()
        self.box2.show()
        self.window.unmaximize()
        self.window.show()

    def main(self):
        gtk.main()  # starting event processing loop

    def delete_event(self, widget, event, data=None):
        """
        :return False if you want to destroy window
        :return True if you want to keep window
        """
        print "[Gtk] delete event occured"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def add_button(self, image, function, box=0, arg=None):
        self.button = gtk.Button()
        # When the button is clicked it calls self.hello()
        self.button.connect("clicked", function, arg)
        self.button.add(image)
        # pack a box to the beginning.
        if box:
            box.pack_start(self.button, True, True, 0)
        # Close the window
        # uncomment this if you want to close all parent windows without other children
        # when you close a window.
        # self.button1.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.button.show()
        return self.button

    def add_text_button(self, label, function, box=0, arg=None):
        self.button = gtk.Button(label)
        self.button.connect("clicked", function, arg)
        if box:
            box.pack_start(self.button, True, True, 0)
        self.button.show()
        return self.button

    def choose_field(self, unusedbutnecessary, arg):
        """ choose, which field you want to add to Room.fields

        :param arg: string/integer of field type which is chosen to be added to fields.
        """
        self.chosen = arg

    def show_fields(self):
        """ shows the current fields.

        :param fields: list of lists
        :return:
        """
        y = len(self.fields)
        x = len(self.fields[0])
        self.table = gtk.Table(x, y)
        self.buttonlist = []
        for i in range(y):
            self.buttonlist.append([])
            for j in range(x):
                a = (i, j)
                a = self.add_button(self.which_image(self.fields[i][j]),
                                    self.change_field, arg=a)
                self.buttonlist[i].append(a)
                self.table.attach(a, j, j + 1, i, i + 1)
                a.show()
        self.box2.pack_start(self.table)
        self.table.show()

    def change_field(self, unusedbutnecessary, xy):
        if self.chosen == "C":
            self.give_option()
            return
        i = xy[0]
        j = xy[1]
        self.fields[i][j] = self.chosen
        self.buttonlist[i][j].destroy()
        a = self.add_button(self.which_image(self.fields[i][j]), self.change_field, arg=xy)
        self.buttonlist[i][j] = a
        self.table.attach(a, j, j + 1, i, i + 1)
        a.show()
        self.table.show()
        self.box2.show()
        self.window.show()

    def which_image(self, arg):
        if arg == "W":
            return i_wall()
        elif arg == "O":
            return i_leer()
        elif arg == "B":
            return i_barricada()
        elif arg == "T":
            return i_treasure()
        elif arg == 0:
            return i_player()
        elif arg == 1:
            return i_1one()

    def give_option(self, unusedbutnecessary, xy):
        """ Dialog to add entries to fielddata.

        This is executed if the give_option is chosen and a field is clicked.
        The field type is then assigned a value, e.g:
        {
            1 : "Police Officer", (enemy[0])
            2 : 15413874260947 (Room.description)
        }
        for now I can't implement Doors, as there is no way to edit Rooms.
        enemies: list of lists
        Do I need this function? maybe I should do this with CLI.
        :param unusedbutnecessary: unused
        :param xy: tuple(x,y), self.fields[x][y]
        :return:
        """
        # dialog
        # Lots of Buttons to choose from:
        # for room in rooms: room.id
        # for enemy in enemies: enemy[0]
        # fielddata.remove(entry)
        # fielddata[entry] = choice
        # dialog = gtk.Dialog(title="Enter a description", parent=self.window, flags=gtk.DIALOG_DESTROY_WITH_PARENT, buttons=None)
        with open("../resources/enemies", "r+") as file:
            enemies = pickle.load(file)

    def savequit(self, unusedbutnecessary, unusedbutnecessary2):
        dialog = gtk.Dialog(title="Enter a description", parent=self.window,
                            flags=gtk.DIALOG_DESTROY_WITH_PARENT, buttons=None)
        entry = gtk.Entry()
        dialog.action_area.pack_start(entry)
        entry.show()

        button = gtk.Button("Ok")
        button.connect("clicked", self.getext, entry)
        button.connect("clicked", dialog.destroy)
        dialog.action_area.pack_start(button)
        button.show()

        dialog.action_area.show()
        dialog.show()

    def getext(self, unusedbutnecessary, widget):
        description = widget.get_text()
        widget.destroy()
        self.room = game.Room(self.fields, self.fielddata, description)
        self.window.destroy()


class Choose_Field_Window(object):
    """ Window for choosing one field of the mission.

    weird bug: Save&Quit doesnt close the window, but still returns the coordinates.
    """
    def __init__(self, room):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.box1 = gtk.HBox()
        self.room = room
        self.show_fields()
        self.window.add(self.box1)
        self.box1.show()
        self.window.show()

    def main(self):
        gtk.main()  # starting event processing loop
        return self.arg

    def delete_event(self, widget, event, data=None):
        """
        :return False if you want to destroy window
        :return True if you want to keep window
        """
        print "[Gtk] delete event occured"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def show_fields(self):
        """ shows the current fields.

        :param fields: list of lists
        :return:
        """
        y = len(self.room.fields)
        x = len(self.room.fields[0])
        self.table = gtk.Table(x, y)
        self.buttonlist = []
        for i in range(y):
            self.buttonlist.append([])
            for j in range(x):
                a = (i, j)
                a = self.add_button(self.which_image(self.room.fields[i][j]), self.choose_field, arg=a)
                self.buttonlist[i].append(a)
                self.table.attach(a, j, j + 1, i, i + 1)
                a.show()
        self.box1.pack_start(self.table)
        self.table.show()

    def which_image(self, arg):
        if arg == "W":
            return i_wall()
        elif arg == "O":
            return i_leer()
        elif arg == "B":
            return i_barricada()
        elif arg == "T":
            return i_treasure()
        elif arg == 0:
            return i_player()
        elif arg == 1:
            return i_1one()

    def add_button(self, image, function, box=0, arg=None):
        self.button = gtk.Button()
        self.button.add(image)
        # When the button is clicked it calls self.hello()
        self.button.connect("clicked", function, arg)
        # pack a box to the beginning.
        if box:
            box.pack_start(self.button, True, True, 0)
        # Close the window
        # uncomment this if you want to close all parent windows without other children
        # when you close a window.
        # self.button1.connect_object("clicked", gtk.Widget.destroy, self.window)
        self.button.show()
        return self.button

    def choose_field(self, unusedbutnecessary, arg):
        self.arg = arg
        self.window.destroy()


class CreateEnemyWin(object):
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(20)
        global filename
        filename = "../images/1one.gif"  # default value

        self.box1 = gtk.VBox()
        self.table1()

        self.button = gtk.Button("Done")
        self.button.connect("clicked", self.get_values)
        self.button.connect("clicked", self.destroy)
        self.box1.pack_start(self.button)
        self.button.show()

        self.window.add(self.box1)
        self.box1.show()
        self.window.show()

    def main(self):
        gtk.main()  # starting event processing loop
        return self.output

    def delete_event(self, widget, event, data=None):
        """
        :return False if you want to destroy window
        :return True if you want to keep window
        """
        print "[Gtk] delete event occured"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def table1(self):
        self.table = gtk.Table(2, 13)
        self.tablelabel("Name:", 0)
        self.tablelabel("Race:", 1)
        self.tablelabel("Image:", 2)
        self.tablelabel("Constitution:", 3)
        self.tablelabel("Strength:", 4)
        self.tablelabel("Agility:", 5)
        self.tablelabel("Mobility:", 6)
        self.tablelabel("Intelligence:", 7)
        self.tablelabel("Gun:", 8)
        self.tablelabel("Sword:", 9)
        self.tablelabel("Min. Loot:", 10)
        self.tablelabel("Max. Loot:", 11)
        self.tablelabel("Experience", 12)
        self.inputs = []
        self.tableobject(gtk.Entry, 0)
        self.tableobject(gtk.Entry, 1)

        self.button = gtk.Button("Choose File")
        self.button.connect("clicked", self.choose_file)
        self.table.attach(self.button, 1, 2, 2, 3)
        self.button.show()

        self.tableobject(gtk.Entry, 3)
        self.tableobject(gtk.Entry, 4)
        self.tableobject(gtk.Entry, 5)
        self.tableobject(gtk.Entry, 6)
        self.tableobject(gtk.Entry, 7)
        self.tableobject(gtk.Entry, 8)
        self.tableobject(gtk.Entry, 9)
        self.tableobject(gtk.Entry, 10)
        self.tableobject(gtk.Entry, 11)
        self.tableobject(gtk.Entry, 12)

        self.box1.pack_start(self.table)
        self.table.show()

    def tablelabel(self, title, y):
        a = gtk.Label(title)
        self.table.attach(a, 0, 1, y, y + 1)
        a.show()

    def tableobject(self, Klass, y):
        a = Klass()
        self.inputs.append(a)
        self.table.attach(a, 1, 2, y, y + 1)
        a.show()

    def get_values(self, unusedbutnecessary):
        lst = []
        end = []
        for a in self.inputs:
            lst.append(a.get_text())
        for i in range(len(lst) + 1):
            if i == 2:
                end.append(self.filename)
            end.append(i)
        self.output = {lst[0]: lst}

    def choose_file(self, unusedbutnecessary):
        self.filesel = gtk.FileSelection("Select an image")
        self.filesel.ok_button.connect("clicked", lambda w: self.file_ok_sel)
        self.filesel.ok_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.cancel_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.set_filename("../images/characters/1one.gif")
        self.filesel.show()

    def file_ok_sel(self, w):
        global filename
        filename = self.filesel.get_filename()


class CreateGunWin(object):
    """ Window to create guns classes.

    To do: design gun logos and change the default values.

    def __init__(self, name, price, image, damage, grange, ap):
    super(Gun, self).__init__(name, price, image)
    self.damage = damage  # Integer
    self.grange = grange  # Integer
    self.ap = ap  # Integer, AP needed to fire the gun
    self.type = "gun"
    """

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(20)
        self.filename = "../images/guns/glock.gif"  # default value

        self.box1 = gtk.VBox()
        self.table1()

        self.button = gtk.Button("Done")
        self.button.connect("clicked", self.get_values)
        self.button.connect("clicked", self.destroy)
        self.box1.pack_start(self.button)
        self.button.show()

        self.window.add(self.box1)
        self.box1.show()
        self.window.show()

    def main(self):
        gtk.main()  # starting event processing loop
        return self.output

    def delete_event(self, widget, event, data=None):
        """
        :return False if you want to destroy window
        :return True if you want to keep window
        """
        print "[Gtk] delete event occured"
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def table1(self):
        self.table = gtk.Table(2, 13)
        self.tablelabel("Name:", 0)
        self.tablelabel("Price:", 1)
        self.tablelabel("Damage:", 2)
        self.tablelabel("Range:", 3)
        self.tablelabel("AP:", 4)
        self.tablelabel("Image:", 5)
        self.inputs = []
        for i in range(0, 5):
            self.tableobject(gtk.Entry, i)

        self.button = gtk.Button("Choose File")
        self.button.connect("clicked", self.choose_file)
        self.table.attach(self.button, 1, 2, 5, 6)
        self.button.show()

        self.box1.pack_start(self.table)
        self.table.show()

    def tablelabel(self, title, y):
        a = gtk.Label(title)
        self.table.attach(a, 0, 1, y, y + 1)
        a.show()

    def tableobject(self, Klass, y):
        a = Klass()
        self.inputs.append(a)
        self.table.attach(a, 1, 2, y, y + 1)
        a.show()

    def get_values(self, unusedbutnecessary):
        lst = []
        end = []
        for a in self.inputs:
            lst.append(a.get_text())
        for i in range(len(lst) + 1):
            if i == 2:
                end.append(self.filename)
            end.append(i)
        self.output = {lst[0]: lst}

    def choose_file(self, unusedbutnecessary):
        self.filesel = gtk.FileSelection("Select an image")
        self.filesel.ok_button.connect("clicked", lambda w: self.file_ok_sel)
        self.filesel.ok_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.cancel_button.connect("clicked", lambda w: self.filesel.destroy())
        self.filesel.set_filename("../images/guns/glock.gif")
        self.filesel.show()

    def file_ok_sel(self, w):
        global filename
        filename = self.filesel.get_filename()


# # # # # # # #
# 3.Functions #
# # # # # # # #

def i_wall():
    i_wall = gtk.Image()
    i_wall.set_from_file("../images/fields/wall.gif")
    i_wall.show()
    return i_wall


def i_leer():
    i_leer = gtk.Image()
    i_leer.set_from_file("../images/fields/0leer.gif")
    i_leer.show()
    return i_leer


def i_barricada():
    i_barricada = gtk.Image()
    i_barricada.set_from_file("../images/fields/barricada.gif")
    i_barricada.show()
    return i_barricada


def i_treasure():
    i_treasure = gtk.Image()
    i_treasure.set_from_file("../images/fields/treasure.gif")
    i_treasure.show()
    return i_treasure


def i_player():
    i_player = gtk.Image()
    i_player.set_from_file("../images/characters/player.gif")
    i_player.show()
    return i_player


def i_1one():
    i_1one = gtk.Image()
    i_1one.set_from_file("../images/characters/1one.gif")
    i_1one.show()
    return i_1one


def i_circle():
    i_circle = gtk.Image()
    i_circle.set_from_file("../images/kreis.gif")
    i_circle.show()
    return i_circle


def create_file(filename):
    """ tests if file exists - if not it creates an empty dict in it.

    :param filename: string - file path to create
    """
    try:
        with open(filename, "rb"):
            return
    except IOError:
        print("ERROR: ", filename, " doesn't exist, is created instead.")
        with open(filename, "wb") as file:
            dct = {}
            pickle.dump(dct, file)


def create_enemy():
    """ creating enemy classes and saving them in resources/enemies """
    print("Create an enemy.")
    window = CreateEnemyWin()
    newdict = window.main()
    print("Saving enemy in resources/enemies...")
    create_file("../resources/enemies")
    with open("../resources/enemies", "rb") as file:
        allenemies = pickle.load(file)
    for i in newdict:
        allenemies[i] = newdict[i]
    with open("../resources/enemies", "wb") as file:
        pickle.dump(allenemies, file)
    print("Enemy saved.")


def create_gun():
    """ creating gun classes and saving them in resources/guns """
    print("Create a gun.")
    window = CreateGunWin()
    newdict = window.main()
    print("Saving gun in resources/guns...")
    create_file("../resources/guns")
    with open("../resources/guns", "rb") as file:
        allenemies = pickle.load(file)
    for i in newdict:
        allenemies[i] = newdict[i]
    with open("../resources/guns", "wb") as file:
        pickle.dump(allenemies, file)
    print("Gun saved.")


def create_fielddata_entry(room):
    """ Create a fielddata entry for a room


    :param room: Room object
    :return: room: Room object
    """
    choice = 0
    while choice == 0:
        print("0 : Abort")
        for entry in room.fielddata:
            print(str(entry) + " : " + room.fielddata[entry])
        try:
            choice = int(raw_input("Which entry do you want to create? Pick a number which "
                                   "is not given yet. delete it if you want to update an "
                                   "existing: "))
        except ValueError:
            print("ERROR: Enter a number.")
        if choice == 0:
            return room
        elif choice in room.fielddata:
            print("ERROR: " + str(choice) + " is already in fielddata. Try again.")
            choice = 0
        else:
            room.fielddata[choice] = raw_input("Enter the content of " + str(choice) + ": ")
            return room


def erase_fielddata_entry(room):
    """
    :param room: Room object
    :return: room: Room object
    """
    choice = 0
    while choice == 0:
        print("0 : Abort")
        for entry in room.fielddata:
            print(str(entry) + " : " + room.fielddata[entry])
        try:
            choice = int(raw_input("Which entry do you want to delete? "))
        except ValueError:
            print("ERROR: Enter a number.")
        if choice == 0:
            return room
        elif choice in room.fielddata:
            del room.fielddata[choice]
            return room
        else:
            print("ERROR: " + str(choice) + " is not in fielddata. Try again.")
            choice = 0


def choose_target_enemy(room):
    for i in room.fielddata:
        print i, room.fielddata[i]
    choice = 0
    while choice == 0:
        try:
            choice = int(raw_input("Which enemy is to be killed? "))
        except ValueError:
            print("ERROR: Enter a number.")
            choice = 0
    room.fielddata["target"] = choice


def create_room():
    window = RoomEditor()
    window.main()
    choice = 0
    while choice == 0:
        print("(1) Create a fielddata entry")
        print("(2) Erase a fielddata entry")
        print("(3) Choose a target enemy")
        print("(4) Finish room creation")
        try:
            choice = int(raw_input("What do you want to do? "))
        except ValueError:
            print("ERROR: Enter a number.")
        if choice == 1:
            create_fielddata_entry(window.room)
        elif choice == 2:
            erase_fielddata_entry(window.room)
        elif choice == 3:
            choose_target_enemy(window.room)
        elif choice == 4:
            print("Back to mission creation.")
            return window.room
        else:
            print("ERROR: Enter a number between 1 and 5.")
        choice = 0


def choose_room(rooms, string):
    choice = "y"
    while choice == "y":
        for i in rooms:
            print str(id(i)), i.description
        try:
            choice = raw_input(string)
        except ValueError:
            print("ERROR: Enter the ID of the room.")
        for i in rooms:
            try:
                if id(i) == int(choice):
                    return i
            except ValueError:
                if i.description == choice:
                    return i
        print("ERROR: ID is not in room list.")
        choice = "y"


def create_mission():
    """ mission creation func

    rewardmoney         # integer
    rewarditems         # list of Item-objects
    rewardxp            # integer
    description         # string
    room                # Room-object where to start
    target_item         # string (name of item) - default: None
    target_enemy        # integer (how many enemies have target attribute) - default: 0
    target_coordinates  # list (x,y,roomID) - default: None
    """
    name = 0
    while name == 0:
        name = raw_input("What shall be the name of the mission? ")
        if name in os.listdir("../missions"):
            print("ERROR: Mission name already taken.")
            name = 0
    rooms = []
    choice = "y"
    while choice == "y":
        print("Create a room.")
        rooms.append(create_room())
        try:
            choice = raw_input("Do you want to create another room? (y/N) ")
        except ValueError:
            print("ERROR: Wrong input. Continuing mission creation.")
            choice = "N"
    room = choose_room(rooms, "Which room shall be the starting point? ")
    print("Define success conditions:")
    target_item = raw_input("Name of target item necessary to win the mission (leave "
                            "empty if not): ")
    if target_item == "":
        target_item = None
    choice = raw_input("Do you want to define target coordinates? (y/N) ")
    while choice == "y":
        targetroom = choose_room(rooms, "Which room shall the target position be in? ")
        field_choice_win = Choose_Field_Window(targetroom)
        xy = field_choice_win.main()
        target_coordinates = [xy[0], xy[1], targetroom]
        choice = raw_input("Do you want to create another target position? (y/N) ")
    else:
        target_coordinates = None
    target_enemy = 0
    for r in rooms:
        if "target" in r.fielddata:
            for i in r.fields:
                for j in i:
                    if r.fielddata["target"] == j:
                        target_enemy += 1
    print(str(target_enemy) + " target enemies in mission.")
    print("Enter additional data: ")
    money = -1
    while money == -1:
        try:
            money = int(raw_input("How much BTC shall be the reward? "))
        except ValueError:
            print("ERROR: Enter a number.")
            money = -1
    xp = -1
    while xp == -1:
        try:
            xp = int(raw_input("How much XP shall be rewarded? "))
        except ValueError:
            print("ERROR: Enter a number.")
            xp = -1
    items = []  # Add reward items as soon as there is a modular item system.
    print("Enter a mission description:")
    description = raw_input()
    mission = game.Mission(money, items, xp, description, room, rooms, target_item,
                           target_enemy, target_coordinates)
    print("Mission created. Saving mission as missions/" + name + "...")
    with open("../missions/" + name, mode="wb") as file:
        pickle.dump(mission, file)
    print("Mission saved.")


def main():
    choice = 0
    while choice == 0:
        print("(1) Create a mission\n(2) Create a room (useless)\n(3) Create a gun")
        print("(4) Create a sword\n(5) Create an enemy\n(6) Exit the editor")
        try:
            choice = int(raw_input("What do you want to do? "))
        except ValueError:
            print("ERROR: Enter a number.")
        if choice == 1:
            create_mission()
        elif choice == 2:
            create_room()
        elif choice == 3:
            create_gun()
        elif choice == 4:
            pass
            # create_sword()
        elif choice == 5:
            create_enemy()
        elif choice == 6:
            print("Good Bye.")
            exit()
        else:
            print("ERROR: Enter a number between 1 and 5.")
        choice = 0


if __name__ == "__main__":
    main()
