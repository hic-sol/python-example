from algorithm import Algorithm
from quest import Quest
from location import Location
from room import Room
from input import InputHandler
from character import Player

def main():
    # initialize dungeon
    dungeon = Dungeon()

    # initialize input handler
    handler = InputHandler(dungeon)

    print("Welcome to the Dungeon of Infinite Doors!\n")
    handler.help()
    print()
    dungeon.quest.print_quest()

    while True:
        dungeon.current_room.describe()
        action, user_input = handler.get_action()
        if action is not None:
            print()
            action(user_input)

class Dungeon:
    def __init__(self):
        # initialize the dungeon
        self.algorithm = Algorithm()
        self.quest = Quest(self.algorithm)
        loc, desc = self.algorithm.generate_first_room_location()
        self.location = Location(loc)
        self.root_room = Room(self.location, self.algorithm, quest=self.quest, desc=desc)
        self.root_room.generate_adjacent()
        self.current_room = self.root_room
        self.player = Player(self.algorithm)

    def move(self, direction):
        next_room = self.current_room.exits.get(direction)
        if next_room is not None:
            next_room.generate_adjacent()
            self.current_room = next_room
            print("You go " + direction.name.lower())
        else:
            print("There is no exit in that direction.")


if __name__ == "__main__":
    main()
