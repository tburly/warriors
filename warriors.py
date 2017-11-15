#!/usr/bin/env python3

from items import Inventory, WEAPONS, SHIELDS, ARMORS
from effects import Effect, EFFECTS
from round_actions import Initiative, Attack, OFFHAND_MODIFIER
from copy import deepcopy

"""
Warriors fight
"""


class Warrior(object):
    """
    Equips, drops, gains, discards. Has: name, health, offense, defense, inventory, effects
    """

    def __init__(self, name,
                 health=30,
                 offense=10,
                 defense=10,
                 inventory=None,  # Inventory accepts only weapon, armor and items in constructor
                 effects=None):

        super(Warrior, self).__init__()

        self.name = name
        self.health = health
        self.offense = offense
        self.defense = defense
        if inventory is None:
            self.inventory = Inventory()
        else:
            self.inventory = inventory
        if effects is None:
            self.effects = []
        else:
            self.effects = effects

    def __str__(self):
        inv_list = [self.inventory.weapon,
                    self.inventory.offhand_weapon,
                    self.inventory.shield,
                    self.inventory.armor] + self.inventory.items
        return "{} (*{}*/{}/{}), inventory: {}, effects: {}".format(self.name, self.health, self.offense, self.defense, [item.name for item in inv_list if item is not None], [effect.name for effect in self.effects])

    def equip_weapon(self, weapon):
        print(self.name, "equips a weapon:", str(weapon))
        self.inventory.weapon = weapon

    def drop_weapon(self):
        print(self.name, "drops a weapon")
        self.inventory.weapon = None

    def equip_offhand_weapon(self, offhand_weapon):
        print(self.name, "equips an off-hand weapon:", str(offhand_weapon))
        self.inventory.offhand_weapon = offhand_weapon

    def drop_offhand_weapon(self):
        print(self.name, "drops an off-hand weapon")
        self.inventory.offhand_weapon = None

    def equip_shield(self, shield):
        print(self.name, "equips a shield:", str(shield))
        self.inventory.shield = shield

    def drop_shield(self):
        print(self.name, "drops a shield")
        self.inventory.shield = None

    def equip_armor(self, armor):
        print(self.name, "equips an armor:", str(armor))
        self.inventory.armor = armor

    def drop_armor(self):
        print(self.name, "drops an armor")
        self.inventory.armor = None

    def equip_item(self, item):
        print(self.name, "equips an inventory item:", str(item))
        self.inventory.items.append(item)

    def drop_item(self, item):
        print(self.name, "drops an inventory item:", str(item))
        self.inventory.items.remove(item)

    def gain_effect(self, effect):
        print(self.name, "gains an effect:", effect.name)
        self.effects.append(effect)

    def discard_effect(self, effect):
        print(self.name, "discards an effect:", effect.name)
        self.effects.remove(effect)


class Battle(object):
    """Commences. Has: attacker, defender, base_attacker, base_defender"""

    def __init__(self, attacker, defender):
        super(Battle, self).__init__()

        self.attacker = attacker
        self.defender = defender
        self.rounds = []
        # for future use
        self.base_attacker = deepcopy(attacker)
        self.base_defender = deepcopy(defender)

    def resolve_initiative(self):
        # TODO: announcement

        while True:
            initiative = Initiative(self.attacker, self.defender)

            if initiative.result == "attacker":
                # TODO: announcement
                break
            elif initiative.result == "draw":
                # TODO: announcement
                continue
            elif initiative.result == "defender":
                # TODO: announcement
                self.swap_sides()
                break

    def commence(self):
        self.resolve_initiative()

        while True:
            battle_round = BattleRound(self.attacker, self.defender)
            self.rounds.append(battle_round)
            # TODO: announcement

            if self.attacker.health <= 0:
                # TODO: announcement
                break
            elif self.defender.health <= 0:
                # TODO: announcement
                break

            battle_round.resolve_effects()
            self.swap_sides()

    def swap_sides(self):
        temp = self.attacker
        self.attacker = self.defender
        self.defender = temp


class BattleRound(object):
    """Has: attacker, defender, attack, offhand_attack"""

    def __init__(self, attacker, defender):
        super(BattleRound, self).__init__()
        self.attacker = attacker
        self.defender = defender
        self.attack = Attack(self.attacker, self.defender)
        if self.attacker.inventory.offhand_weapon is not None:
            self.offhand_attack = Attack(self.attacker, self.defender, OFFHAND_MODIFIER)
        else:
            self.offhand_attack = None

    def resolve_effects(self):
        # MISS effect - remove all if there was at least one hit, apply if otherwise
        if self.offhand_attack is None:
            if self.attack.result < 0:
                self.attacker.gain_effect(Effect(EFFECTS["miss"]))
            else:
                # clear all MISS effects on the attacker
                for miss in [effect for effect in self.attacker.effects if effect.name == EFFECTS["miss"]]:
                    self.attacker.discard_effect(miss)
        else:
            if self.attack.result < 0 and self.offhand_attack.result < 0:
                self.attacker.gain_effect(Effect(EFFECTS["miss"]))
            else:
                # clear all MISS effects on the attacker
                for miss in [effect for effect in self.attacker.effects if effect.name == EFFECTS["miss"]]:
                    self.attacker.discard_effect(miss)


def report(warrior):
    print()
    print("Hail, my good fellow. I am {}. My health is {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}. I'm equipped with: \n{}".format(warrior.name, warrior.health, warrior.offense, warrior.defense, [effect.name for effect in warrior.effects], str(warrior.inventory)))


def main():
    """Runs the game"""
    dagobert = Warrior("Dagobert")
    dagobert.equip_weapon(WEAPONS["Longsword"])
    dagobert.equip_shield(SHIELDS["Tower Shield"])
    dagobert.equip_armor(ARMORS["Chainmail"])

    rogbar = Warrior("Rogbar")
    rogbar.equip_weapon(WEAPONS["Longsword"])
    rogbar.equip_offhand_weapon(WEAPONS["Short Sword"])
    rogbar.equip_armor(ARMORS["Chainmail"])

    report(dagobert)
    report(rogbar)

    battle = Battle(dagobert, rogbar)
    battle.commence()


if __name__ == "__main__":
    main()
