from items import Item, Weapon, Armor, Shield, DmgReduction
import pprint

"""

"""


class Warrior(object):
    """
    Fights, equips, gains, drops, discards. Has: name, health, was_hit, items, offense, defense, effects
    """

    def __init__(self, name,
                 health=30,
                 was_hit=False,
                 items=None,
                 offense=10,
                 defense=5,
                 effects=None):

        super(Warrior, self).__init__()

        self._name = name
        self._health = health
        self._was_hit = was_hit
        if items is None:
            self._items = []
        else:
            self._items = items
        self._offense = offense
        self._defense = defense
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
    def was_hit(self):
        return self._was_hit

    @was_hit.setter
    def was_hit(self, value):
        self._was_hit = was_hit

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = items

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
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, value):
        self._effects = effects

    def attack(self, opponent, weapon):
        pass

    def equip_item(self, item):
        self._items.append(item)

    def drop_item(self, item):
        self._items.remove(item)

    def gain_effect(self, effect):
        self._effects.append(effect)

    def discard_effect(self, effect):
        self._effects.remove(effect)


class Battle(object):
    """docstring for Battle"""

    def __init__(self, attacker, defender):
        super(Battle, self).__init__()

        self._attacker = attacker
        self._defender = defender

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


def main():
    dagobert = Warrior("Dagobert")
    dagobert.equip_item(Weapon("Longsword", (5, 12), "slashing", 1.0, 15))
    dagobert.equip_item(Shield("Tower Shield", (1, 4), to_block=25))
    dagobert.equip_item(Armor("Chainmail", dmg_reduction=DmgReduction(4, 3, 2)))
    print()
    pprint.pprint(dir(dagobert))
    print("Hail, my good fellow. My name is {}. My health is {}. If someone says I was hit, then it's {}. I'm equipped with: {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}".format(dagobert.name, dagobert.health, dagobert.was_hit, [item.name for item in dagobert.items], dagobert.offense, dagobert.defense, dagobert.effects))

    for item in dagobert.items:
        print(str(item))


main()
