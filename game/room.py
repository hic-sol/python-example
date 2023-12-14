###
# Code for handling, generating, and interacting with rooms
###

from random import choice, randint
from enum import Enum
from character import NPC
from item import Item
from algorithm import Algorithm


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    UP = 5
    DOWN = 6

def opposite(direction):
    return {Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP}.get(direction)


class Room:
    def __init__(self, location, algorithm, quest=None, desc="", from_direction=None, from_room=None):
        self.location = location
        self.algorithm = algorithm
        self.quest = quest
        self.description = desc
        self.exits = dict()
        if from_direction is not None:
            self.exits[opposite(from_direction)] = from_room
        self.items = list()
        self.generate_items()
        self.npcs = list()
        self.generate_npcs()
        self.generated_exits = False

    def generate_adjacent(self):
        if not self.generated_exits:
            for direction in Direction:
                if direction not in self.exits:
                    if choice([True, False]):  # 50% chance we add an exit in each direction
                        self.exits[direction] = Room(self.location, self.algorithm, self.quest, from_direction=direction,
                                                     from_room=self)
            self.generated_exits = True

    def generate_items(self):
        while choice([True, True, False, False, False]):
            if self.quest.quest_type == self.quest.QuestType.COLLECT and \
                    randint(0, 100) <= self.quest.difficulty:
                self.items.append(self.quest.target)
                break
            else:
                self.items.append(Item(self.algorithm))

    def generate_npcs(self):
        while choice([True, False]):
            if self.quest.quest_type == self.quest.QuestType.KILL and \
                    randint(0, 100) <= self.quest.difficulty:
                self.npcs.append(self.quest.target.respawn(self))
                break
            else:
                self.npcs.append(NPC(self.algorithm, room=self))

    def generate_description(self):
        return self.algorithm.generate_room(self.location.name)

    def describe(self):
        if self.description == "":
            self.description = self.generate_description()
        print("\n" + self.description + "\nExits: " +
              self.get_exits() + "\nItems: " + self.get_items() + "\nNPCs: " + self.get_npcs())

    def get_exits(self):
        exits = ""
        for direction in self.exits:
            if exits > "":
                exits += ", "
            exits += direction.name.lower()
        return exits

    def get_items(self):
        items = ""
        for item in self.items:
            if items > "":
                items += ", "
            items += item.name
        return items

    def add_item(self, item):
        if item is not None:
            self.items.append(item)

    def get_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item

    def remove_item(self, item):
        self.items.remove(item)

    def get_npcs(self):
        npcs = ""
        for npc in self.npcs:
            if npcs > "":
                npcs += ", "
            npcs += npc.name
        return npcs

    def get_target(self, target):
        for npc in self.npcs:
            if npc.name.lower() == target.lower():
                return npc

    def del_npc(self, npc):
        if npc in self.npcs:
            self.npcs.remove(npc)


