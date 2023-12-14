from random import randint


class Item:
    def __init__(self, algorithm, quest_item=False):
        self.algorithm = algorithm
        if quest_item:
            self.name, self.description = self.generate_description()
        else:
            self.name, self.description = "Object", ""
        self.attack = randint(0, 2)
        self.defense = randint(0, 2)

    def generate_description(self):
        return self.algorithm.generate_item()

    def print_stats(self):
        if self.description == "":
            self.name, self.description = self.generate_description()
        print("{}\nAttack: {}\nDefense: {}\nDescription: {}".format(self.name, self.attack,
                                                                    self.defense,
                                                                    self.description))
