###
# Text input handler
###
from room import *


class InputHandler:
    def __init__(self, dungeon):
        self.valid_commands = {"north": self.north, "south": self.south,
                               "east": self.east, "west": self.west,
                               "up": self.up, "down": self.down,
                               "attack": self.attack, "inspect": self.inspect,
                               "pickup": self.pickup, "drop": self.drop,
                               "inv": self.inv, "stats": self.stats,
                               "equip": self.equip, "unequip": self.unequip,
                               "help": self.help}
        self.help_info = {"north": "Use the exit to the North.",
                          "south": "Use the exit to the South.",
                          "east": "Use the exit to the East.",
                          "west": "Use the exit to the West.",
                          "up": "Use the exit that leads upward.",
                          "down": "Use the exit that leads downward.",
                          "attack": "Attack an npc to deal damage and complete quests.",
                          "inspect": "Inspect an NPC or item to view its stats and description.",
                          "pickup": "Pickup an item in a room and add it to your inventory.",
                          "drop": "Drop an item from your inventory.",
                          "inv": "Check which items are in your inventory.",
                          "stats": "Check your player stats.",
                          "equip": "Equip an item for stat boosts. You may only have two items equipped at a time.",
                          "unequip": "Unequip an item.",
                          "help": "Display this help information."}
        self.dungeon = dungeon

    def get_action(self):
        user_input = input("What would you like to do? ").split()
        desired_function = self.valid_commands.get(user_input.pop(0).lower())
        return desired_function, user_input

    def help(self, user_input=None):
        commands = None
        if not user_input:
            print("Explore rooms while searching for strange objects and mysterious strangers.\n" +
                  "Use the inspect command to view their secrets.\n" +
                  "Those whose names start with * are quest items/NPCs. Pickup or attack them.\n" +
                  "\nThe following commands are available:")
            commands = self.help_info
        else:
            cmd_name = user_input.pop(0)
            if cmd_name in self.help_info:
                commands = {cmd_name: self.help_info.get(cmd_name)}
        if commands is not None:
            for cmd, info in commands.items():
                print("{}: {}".format(cmd, info))
        else:
            print("Command not found.")

    def north(self, user_input):
        # move north
        self.dungeon.move(Direction.NORTH)

    def south(self, user_input):
        # move south
        self.dungeon.move(Direction.SOUTH)

    def east(self, user_input):
        # move north
        self.dungeon.move(Direction.EAST)

    def west(self, user_input):
        # move south
        self.dungeon.move(Direction.WEST)

    def up(self, user_input):
        # move north
        self.dungeon.move(Direction.UP)

    def down(self, user_input):
        # move south
        self.dungeon.move(Direction.DOWN)

    def attack(self, user_input):
        if user_input:
            target = self.dungeon.current_room.get_target(user_input.pop(0))
            if target is not None:
                self.dungeon.player.attack(target)
                if not target.dead:
                    target.attack(self.dungeon.player)
                else:
                    print("" + target.name + " dies.")
                    self.dungeon.current_room.del_npc(target)
                    self.dungeon.quest.check_target(target)
        else:
            print("Please enter a target to attack.")

    def pickup(self, user_input):
        if user_input:
            item = self.dungeon.current_room.get_item(user_input.pop(0))
            if item is not None:
                self.dungeon.current_room.remove_item(item)
                self.dungeon.player.pickup(item)
                print("You pick up the %s." % item.name)
                self.dungeon.quest.check_target(item)
        else:
            print("Please enter an item to pickup.")

    def drop(self, user_input):
        if user_input:
            item = self.dungeon.player.drop(user_input.pop(0))
            if item is not None:
                self.dungeon.current_room.add_item(item)
                print("You dropped the %s." % item.name)
        else:
            print("Please enter an item to drop.")

    def inv(self, user_input):
        self.dungeon.player.print_inventory()

    def inspect(self, user_input):
        item_name = user_input.pop(0)
        items = [i for i in [self.dungeon.current_room.get_target(item_name), self.dungeon.player.get_item(item_name),
                             self.dungeon.current_room.get_item(item_name)] if i]
        item = items[0] if len(items) == 1 else None
        if len(items) > 1:
            for i in range(len(items)):
                print("{}: {}".format(i + 1, items[i].name))
            index = int(input("Please enter the index for which you wish to inspect:")) - 1
            if index in range(len(items)):
                item = items[index]
            else:
                print("Invalid index.")

        if item is not None:
            item.print_stats()

    def stats(self, user_input):
        self.dungeon.player.print_stats()

    def unequip(self, user_input):
        if user_input:
            try:
                slot = int(user_input.pop(0))
                item = self.dungeon.player.unequip(slot)
                print("You unequip the %s." % item.name)
            except ValueError:
                print("Invalid input.")
        else:
            self.dungeon.player.print_equipped()
            slot = int(input("Please select a slot number to unequip (1 or 2): "))
            item = self.dungeon.player.unequip(slot)
            print("You unequip the %s." % item.name)

    def equip(self, user_input):
        if user_input:
            item = self.dungeon.player.equip(user_input.pop(0))
            if item is not None:
                print("You equip the %s." % item.name)
        else:
            print("Please enter an item to equip.")
