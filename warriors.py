from items import Item, Weapon, Armor, Shield, DmgReduction
import pprint


class Warrior:
    """Fights, equips, drops. Has: name, health, was_hit, items, offense, defense, effects"""

    def __init__(self, name,
                 health=30,
                 was_hit=False,
                 items=None,
                 offense=10,
                 defense=5,
                 effects=None):

        self._name = name
        self._health = health
        self._was_hit = was_hit
        if items is None:
            self._items = [Weapon("Bare Hands", (3, 6), 2.0)]
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

    def equip(self, item):
        self._items.append(item)

    def drop(self, item):
        self._items.remove(item)


def main():
    dagobert = Warrior("Dagobert")
    print()
    pprint.pprint(dir(dagobert))
    print("Hail, my good fellow. My name is {}. My health is {}. If someone says I was hit, then it's {}. I'm equipped with: {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}".format(dagobert.name, dagobert.health, dagobert.was_hit, [item.name for item in dagobert.items], dagobert.offense, dagobert.defense, dagobert.effects))
    print(type(dagobert.name))


main()
