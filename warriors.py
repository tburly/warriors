#!/usr/bin/env python3

from items import Weapon, Armor, Shield, Inventory, DmgReduction, WEAPONS, SHIELDS, ARMORS
from effects import EFFECTS
import pprint
import math
from random import randrange

"""
Warriors fight
"""

OFFHAND_MODIFIER = 0.75


class Warrior(object):
    """
    Equips, drops, gains, discards. Has: name, health, offense, defense, inventory, effects
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
        while True:
            self.resolve_round()
            if self._attacker.health < 0 or self._defender.health < 0:
                break

    def resolve_round(self):
        misses = 0
        hits = 0

        # attack
        quality_of_attack = self.calculate_hit()
        if quality_of_attack < 0:
            misses += 1
        else:
            hits += 1
            resolve_hit(quality_of_attack, self._attacker.weapon)

        # off-hand attack
        if self._attacker.offhand_weapon is not None:
            quality_of_offhand_attack = self.calculate_offhand_hit()
            if quality_of_offhand_attack < 0:
                misses += 1
            else:
                hits += 1
                resolve_hit(quality_of_offhand_attack, self._attacker.offhand_weapon)

        # MISS effect
        if len(misses) > 0 and len(hits) == 0:  # only one miss counts (if there were no hits)
            self._attacker.gain_effect(Effect(EFFECTS["miss"]))
        if len(hits) > 0:
            # clear all MISS effects on the attacker
            for miss in [effect for effect in self._attacker.effects if effect.name == EFFECTS["miss"]]:
                self._attacker.discard_effect(miss)

        self.swap_sides()
        self.rounds_count += 1

    def calculate_hit(self):
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        quality_of_attack = self._attacker.offense + attacker_roll - (self.defender.defense + defender_roll)
        return quality_of_attack

    def calculate_offhand_hit(self):
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        # Fighting with an off-hand weapon is 25% tougher, so OFFENCE = OFFENCE * OFFHAND_MODIFIER (floored)
        quality_of_attack = math.floor(self._attacker.offense * OFFHAND_MODIFIER) + attacker_roll - (self.defender.defense + defender_roll)
        return quality_of_attack

    def calculate_block(self, qof):
        block_roll = randrange(1, 21)
        result = self._defender.shield.to_block + block_roll - qof
        if result < 0:
            return False
        else:
            return True

    def calculate_parry(self, qof):
        """
        Parry is possible only if the wapon used has to_parry > 0.
        There can be three possible situations:
            1) defender can parry only with main weapon ==> prrying bonus = weapon's to_parry
            2) defender can parry both with main and off-hand weapon ==>  parrying bonus = weapon's to_parry + OFFHAND_MODIFIER * off-hand weapon's to_parry
            3) defender can parry only with off-hand weapon ==> parrying bonus = OFFHAND_MODIFIER off-hand weapon's to_parry
        """
        parrying_bonus = 0
        # 1)
        if self._defender.weapon is not None and self._defender.offhand_weapon is None:
            parrying_bonus += self._defender.weapon.to_parry
        # 2)
        elif self._defender.weapon is not None and self._defender.offhand_weapon is not None:
            parrying_bonus += self._defender.weapon.to_parry + math.floor(self._defender.offhand_weapon.to_parry * OFFHAND_MODIFIER)
        elif self._defender.weapon is None and self._defender.offhand_weapon is not None:
            parrying_bonus += math.floor(self._defender.offhand_weapon.to_parry * OFFHAND_MODIFIER)

        parry_roll = randrange(1, 21)
        result = parrying_bonus + parry_roll - qof
        if result < 0:
            return False
        else:
            return True

    def calculate_damage(self, qof, weapon):
        qof_augmenting = 0.0  # float
        dmg_reduction = 0
        if weapon.dmg_type == "bludgeoning":
            qof_augmenting += (1 + qof / 10) * 0.75
            dmg_reduction += self.defender.armor.dmg_reduction.bludgeoning
        elif weapon.dmg_type == "slashing":
            qof_augmenting += 1 + qof / 10
            dmg_reduction += self.defender.armor.dmg_reduction.slashing
        elif weapon.dmg_type == "piercing":
            qof_augmenting += (1 + qof / 10) * 1.25
            dmg_reduction += self.defender.armor.dmg_reduction.piercing

        weapon_roll = randrange(weapon.damage[0], weapon.damage[1] + 1)
        damage_dealt = math.floor(weapon_roll * qof_augmenting) - dmg_reduction

        if damage_dealt <= 0:
            return 0
        else:
            return damage_dealt

    def resolve_hit(self, qof, weapon):
        hit_deflected = False
        if self._defender.shield is not None:
            hit_deflected = self.calculate_block(qof)
        elif self._defender.weapon is not None or self_defender.offhand_weapon is not None:
            hit_deflected = self.calculate_parry(qof)
        if not hit_deflected:
            self._defender.health - calculate_damage(qof, weapon)

    def swap_sides(self):
        temp = self._attacker
        self._attacker = self._defender
        self._defender = temp


def report(warrior):
    print()
    print("Hail, my good fellow. I am {}. My health is {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}. I'm equipped with: \n{}".format(warrior.name, warrior.health, warrior.offense, warrior.defense, [effect.name for effect in warrior.effects], str(warrior.inventory)))


def main():
    dagobert = Warrior("Dagobert")
    dagobert.equip_weapon(WEAPONS["Longsword"])
    dagobert.drop_offhand_weapon()
    dagobert.equip_shield(SHIELDS["Tower Shield"])
    dagobert.equip_armor(ARMORS["Chainmail"])
    report(dagobert)


main()
