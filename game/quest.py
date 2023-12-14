from enum import Enum
from random import randint, choice
from item import Item
from character import NPC


class Quest:

    class QuestType(Enum):
        KILL = "kill"
        COLLECT = "collect"

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.quest_type = choice([quest for quest in self.QuestType])
        self.difficulty = randint(25, 100)
        self.count = randint(1, 4)
        self.done_count = 0
        self.target = self.generate_target()

    def generate_target(self):
        if self.quest_type == self.QuestType.KILL:
            target = NPC(self.algorithm, quest_npc=True, hostile=True)
        else:
            target = Item(self.algorithm, quest_item=True)
        target.name = '*' + target.name
        return target

    def difficulty_level(self):
        if self.difficulty < 40:
            difficulty = "hard"
        elif self.difficulty < 60:
            difficulty = "moderate"
        else:
            difficulty = "easy"
        return difficulty

    def check_target(self, target):
        if target == self.target:
            self.complete_one()

    def complete_one(self):
        self.done_count += 1
        if self.done_count >= self.count:
            self.complete_quest()

    def complete_quest(self):
        print("You win!")
        exit()

    def print_quest(self):
        print("Your quest is to " + self.quest_type.value + " " + str(self.count) + " " + self.target.name + ".")
        print("This quest is considered %s." % self.difficulty_level())
