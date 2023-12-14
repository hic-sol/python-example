from random import choice, randint


class Character:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.name, self.description = "Someone", ""
        self.inventory = list()
        self.equipped = list()
        self.attack_score = randint(1, 2)
        self.defense_score = randint(1, 2)
        self.hp = sum(x * randint(1, 3) for x in range(self.attack_score + 1))
        self.dead = False

    def generate_description(self):
        return self.algorithm.generate_character()

    def print_stats(self):
        if self.description == "":
            self.name, self.description = self.generate_description()
        print("{}\nHP: {}\nAttack: {} (+{})\nDefense: {} (+{})\nDescription: {}"
              .format(self.name, self.hp,
                      self.attack_score,
                      self.total_attack() - self.attack_score,
                      self.defense_score,
                      self.total_defense() - self.defense_score,
                      self.description))

    def total_attack(self):
        tot = self.attack_score
        for e in self.equipped:
            tot += e.attack
        return tot

    def total_defense(self):
        tot = self.defense_score
        for e in self.equipped:
            tot += e.defense
        return tot

    def attack(self, target):
        damage = 0
        attack = self.total_attack()
        if attack + randint(1, 20) > target.total_defense() + randint(1, 20):
            damage = self.total_attack() + randint(1, 3)
            target.deal_damage(damage)
        return damage

    def deal_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.die()

    def equip(self, item_name):
        if len(self.equipped) >= 2:
            print("You can only have two items equipped at once.")
        else:
            item = self.get_item(item_name)
            if item is not None:
                self.equipped.append(item)
                self.inventory.remove(item)
                return item

    def unequip(self, slot):
        if slot - 1 in range(2):
            if slot - 1 in range(len(self.equipped)):
                item = self.equipped.pop(slot - 1)
                self.pickup(item)
                return item
            else:
                print("Nothing is equipped in slot %d." % slot)
        else:
            print("%d is not a valid equipment slot." % slot)

    def pickup(self, item):
        self.inventory.append(item)

    def get_item(self, item_name):
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item

    def remove_item(self, item):
        self.inventory.remove(item)

    def die(self):
        self.dead = True

    def print_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print("  {} (+{}, +{})".format(item.name, item.attack, item.defense))
        print()
        self.print_equipped()

    def print_equipped(self):
        print("Equipped:")
        for i in range(len(self.equipped)):
            print("{}:  {} (+{}, +{})".format(i + 1, self.equipped[i].name, self.equipped[i].attack,
                                              self.equipped[i].defense))

    def drop(self, drop_item):
        for item in self.inventory:
            if item.name.lower() == drop_item.lower():
                self.inventory.remove(item)
                return item


class Player(Character):
    def __init__(self, algorithm):
        super().__init__(algorithm)
        self.name, self.description = self.generate_description()
        self.attack_score += 1

    def die(self):
        print("You die. Game over.")
        exit()

    def attack(self, target):
        damage = super().attack(target)
        print("You attack " + target.name + " and deal " + str(damage) + " damage.")


class NPC(Character):
    def __init__(self, algorithm, room=None, quest_npc=False, hostile=None):
        super().__init__(algorithm)
        if quest_npc:
            self.name, self.description = self.algorithm.generate_character()
        self.o_hp = self.hp
        self.room = room
        self.hostile = hostile if hostile is not None else choice([True, True, True, False])

    def attack(self, target):
        damage = super().attack(target)
        print(self.name + " attacks you and deals " + str(damage) + " damage.")

    def respawn(self, room):
        self.hp = self.o_hp
        self.dead = False
        self.room = room
        return self
