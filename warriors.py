from items import Weapon, Armor, Shield, Inventory, DmgReduction, WEAPONS, SHIELDS, ARMORS
from effects import EFFECTS
import pprint
from random import randrange

"""
Warriors fight
"""


class Warrior(object):
    """
    Equips, drops, gains, discards. Has: name, health, offense, defense, inventory, was_hit, effects
    """

    def __init__(self, name,
                 health=30,
                 offense=10,
                 defense=5,
                 inventory=None,  # Inventory accepts only weapon, armor and items in constructor
                 effects=None):

        super(Warrior, self).__init__()

        self._name = name
        self._health = health
        self._offense = offense
        self._defense = defense
        self._was_hit = False
        if inventory is None:
            self._inventory = Inventory()
        else:
            self._inventory = inventory
        if effects is None:
            self._effects = []
        else:
            self._effects = effects

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def offense(self):
        return self._offense

    @offense.setter
    def offense(self, value):
        self._offense = offense

    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        self._defense = defense

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = inventory

    @property
    def was_hit(self):
        return self._was_hit

    @was_hit.setter
    def was_hit(self, value):
        self._was_hit = was_hit

    @property
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, value):
        self._effects = effects

    def equip_weapon(self, weapon):
        self._inventory.weapon = weapon

    def drop_weapon(self):
        self._inventory.weapon = None

    def equip_offhand_weapon(self, offhand_weapon):
        self._inventory.offhand_weapon = offhand_weapon

    def drop_offhand_weapon(self):
        self._inventory.offhand_weapon = None

    def equip_shield(self, shield):
        self._inventory.shield = shield

    def drop_shield(self):
        self._inventory.shield = None

    def equip_armor(self, armor):
        self._inventory.armor = armor

    def drop_armor(self):
        self._inventory.armor = None

    def equip_item(self, item):
        self._inventory.items.append(item)

    def drop_item(self, item):
        self._inventory.items.remove(item)

    def gain_effect(self, effect):
        self._effects.append(effect)

    def discard_effect(self, effect):
        self._effects.remove(effect)


class Battle(object):
    """Commences. Has: attacker, defender"""

    def __init__(self, attacker, defender):
        super(Battle, self).__init__()

        self._attacker = attacker
        self._defender = defender
        self._rounds_count = 0

    @property
    def attacker(self):
        return self._attacker

    @attacker.setter
    def attacker(self, value):
        self._attacker = value

    @property
    def defender(self):
        return self._defender

    @defender.setter
    def defender(self, value):
        self._defender = value

    @property
    def rounds_count(self):
        return self._rounds_count

    @rounds_count.setter
    def rounds_count(self, value):
        self._rounds_count = value

    def commence(self):
        while self._attacker.health and self._defender.health:
            self.resolve_round()

    def resolve_round(self):
        quality_of_attack = self.calculate_hit()
        if not EFFECTS["miss"] in [effect.name for effect in self._attacker.effects]:
            if any([hasattr(item, "to_block") for item in self._defender.items]):
                self.calculate_block(quality_of_attack)
            elif any([hasattr(item, "to_parry") for item in self._defender.items]):
                self.calculate_parry(quality_of_attack)
            if self._defender.was_hit:
                calculate_damage(quality_of_attack)
        self.swap_sides()

    def calculate_hit(self):
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        quality_of_attack = self._attacker.offense + attacker_roll - (self.defender.defense + defender_roll)
        if quality_of_attack < 0:
            self._attacker.gain_effect(Effect(EFFECTS("miss")))
        return quality_of_attack

    def calculate_parry(self, qof):
        pass

    def calculate_block(self, qof):
        pass

    def calculate_damage(self, qof):
        pass

    def swap_sides(self):
        temp = self._attacker
        self._attacker = self._defender
        self._defender = temp


def report(warrior):
    print()
    print("Hail, my good fellow. My name is {}. My health is {}. If someone says I was hit, then it's {}. I'm equipped with: {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}".format(warrior.name, warrior.health, warrior.was_hit, [item.name for item in warrior.items], warrior.offense, warrior.defense, warrior.effects))
    print("Here's a detailed list of my equipment:")
    for item in warrior.items:
        print(str(item))


def main():
    dagobert = Warrior("Dagobert")
    dagobert.equip_item(WEAPONS["Longsword"])
    dagobert.equip_item(SHIELDS["Tower Shield"])
    dagobert.equip_item(ARMORS["Chainmail"])
    report(dagobert)


main()
