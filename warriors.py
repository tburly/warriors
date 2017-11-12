#!/usr/bin/env python3

from items import Weapon, Armor, Shield, Inventory, DmgReduction, WEAPONS, SHIELDS, ARMORS
from effects import Effect, EFFECTS
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
                 defense=10,
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

    def __str__(self):
        inv_list = [self._inventory.weapon,
                    self._inventory.offhand_weapon,
                    self._inventory.shield,
                    self._inventory.armor] + self._inventory.items
        return "{} (*{}*/{}/{}), inventory: {}, effects: {}".format(self._name, self._health, self._offense, self._defense, [item.name for item in inv_list if item is not None], [effect.name for effect in self._effects])

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
        print(self._name, "equips a weapon:", str(weapon))
        self._inventory.weapon = weapon

    def drop_weapon(self):
        print(self._name, "drops a weapon")
        self._inventory.weapon = None

    def equip_offhand_weapon(self, offhand_weapon):
        print(self._name, "equips an off-hand weapon:", str(offhand_weapon))
        self._inventory.offhand_weapon = offhand_weapon

    def drop_offhand_weapon(self):
        print(self._name, "drops an off-hand weapon")
        self._inventory.offhand_weapon = None

    def equip_shield(self, shield):
        print(self._name, "equips a shield:", str(shield))
        self._inventory.shield = shield

    def drop_shield(self):
        print(self._name, "drops a shield")
        self._inventory.shield = None

    def equip_armor(self, armor):
        print(self._name, "equips an armor:", str(armor))
        self._inventory.armor = armor

    def drop_armor(self):
        print(self._name, "drops an armor")
        self._inventory.armor = None

    def equip_item(self, item):
        print(self._name, "equips an inventory item:", str(item))
        self._inventory.items.append(item)

    def drop_item(self, item):
        print(self._name, "drops an inventory item:", str(item))
        self._inventory.items.remove(item)

    def gain_effect(self, effect):
        print(self._name, "gains an effect:", effect.name)
        self._effects.append(effect)

    def discard_effect(self, effect):
        print(self._name, "discards an effect:", effect.name)
        self._effects.remove(effect)


class Battle(object):
    """Commences. Has: attacker, defender"""

    def __init__(self, attacker, defender):
        super(Battle, self).__init__()

        self._attacker = attacker
        self._defender = defender
        self._rounds_count = 1

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

    def resolve_initiative(self):
        print("Two brave warriors came to fight today:")
        print(str(self._attacker))
        print(str(self._defender))

        while True:
            attacker_roll = self._attacker.offense + randrange(1, 21)
            defender_roll = self._defender.offense + randrange(1, 21)

            print(self._attacker.name, "rolls", "*" + attacker_roll + "*", "for initiative")
            print(self._defender.name, "rolls", "*" + defender_roll + "*", "for initiative")

            attacker_result = self._attacker.offense + attacker_roll
            defender_result = self._defender.offense + defender_roll

            if attacker_result > defender_result:
                print(attacker_result, ">", defender_result + ".", self._attacker.name, "wins initiative")
                print("Let the battle begin!")
                break

            elif attacker_result == defender_result:
                print(attacker_result, "=", defender_result + ".", "Draw! Let's roll again")
                continue

            elif attacker_result < defender_result:
                print(attacker_result, "<", defender_result + ".", self._defender.name, "wins initiative")
                print("Let the battle begin!")
                self.swap_sides()
                break

    def commence(self):
        self.resolve_initiative()

        while True:
            print()
            print("******** ROUND #", self._rounds_count, "********")
            print("Attacker is:", str(self._attacker))
            print("Defender is:", str(self._defender))
            self.resolve_round()

            if self._attacker.health < 0:
                print("************************")
                print(self._defender.name, "wins after", self._rounds_count, "rounds of relentless battle.")
                print("************************")
                break

            elif self._defender.health < 0:
                print("************************")
                print(self._attacker.name, "wins after", self._rounds_count, "rounds of relentless battle.")
                print("************************")
                break

    def resolve_round(self):
        misses = 0
        hits = 0

        # attack
        quality_of_attack = self.calculate_hit()
        if quality_of_attack < 0:
            print("It's a miss!")
            misses += 1

        else:
            print("It's a hit!")
            hits += 1
            resolve_hit(quality_of_attack, self._attacker.weapon)

        # off-hand attack
        if self._attacker.offhand_weapon is not None:
            quality_of_offhand_attack = self.calculate_offhand_hit()
            if quality_of_offhand_attack < 0:
                print("It's a miss!")
                misses += 1

            else:
                print("It's a hit!")
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
        print("*** HIT ***")
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        print(self._attacker.name, "rolls", "*" + attacker_roll + "*", "for attack")
        print(self._defender.name, "rolls", "*" + defender_roll + "*", "for defense")

        quality_of_attack = self._attacker.offense + attacker_roll - (self.defender.defense + defender_roll)

        qoa_text = str(self._attacker.offense) + " + " + str(attacker_roll) + " - " + str(self.defender.defense) + " - " + str(defender_roll) + " ="
        print(self._attacker.name + "'s QoA is:", qoa_text, quality_of_attack)

        return quality_of_attack

    def calculate_offhand_hit(self):
        print("*** OFF-HAND HIT ***")
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        print(self._attacker.name, "rolls", "*" + attacker_roll + "*", "for off-hand attack")
        print(self._defender.name, "rolls", "*" + defender_roll + "*", "for defense")

        # Fighting with an off-hand weapon is 25% tougher, so OFFENCE = OFFENCE * OFFHAND_MODIFIER (floored)
        quality_of_attack = math.floor(self._attacker.offense * OFFHAND_MODIFIER) + attacker_roll - (self.defender.defense + defender_roll)

        qoa_text = str(math.floor(self._attacker.offense * OFFHAND_MODIFIER)) + " + " + str(attacker_roll) + " - " + str(self.defender.defense) + " - " + str(defender_roll) + " ="
        print(self._attacker.name + "'s off-hand QoA is:", qoa_text, quality_of_attack)

        return quality_of_attack

    def calculate_block(self, qoa):
        print("*** BLOCK ***")
        block_roll = randrange(1, 21)
        print(self._defender.name, "rolls", "*" + block_roll + "*", "for block")

        result = self._defender.shield.to_block + block_roll - qoa
        result_text = str(self._defender.shield.to_block) + " + " + str(block_roll) + " - " + str(qoa)

        if result < 0:
            print(result_text, "< 0, block failed!")
            return False
        else:
            print(result_text, "< 0, block succeeded!")
            return True

    def calculate_parry(self, qoa):
        """
        Parry is possible only if the wapon used has to_parry > 0.
        There can be three possible situations:
            1) defender can parry only with main weapon ==> prrying bonus = weapon's to_parry
            2) defender can parry both with main and off-hand weapon ==>  parrying bonus = weapon's to_parry + OFFHAND_MODIFIER * off-hand weapon's to_parry
            3) defender can parry only with off-hand weapon ==> parrying bonus = OFFHAND_MODIFIER off-hand weapon's to_parry
        """
        print("*** PARRY ***")
        parrying_bonus = 0
        # 1)
        if self._defender.weapon is not None and self._defender.offhand_weapon is None:
            print(self._defender.name, "tries to parry with his main weapon")
            parrying_bonus += self._defender.weapon.to_parry
        # 2)
        elif self._defender.weapon is not None and self._defender.offhand_weapon is not None:
            print(self._defender.name, "tries to parry with both his weapons")
            parrying_bonus += self._defender.weapon.to_parry + math.floor(self._defender.offhand_weapon.to_parry * OFFHAND_MODIFIER)
        # 3)
        elif self._defender.weapon is None and self._defender.offhand_weapon is not None:
            print(self._defender.name, "tries to parry with his off-hand weapon")
            parrying_bonus += math.floor(self._defender.offhand_weapon.to_parry * OFFHAND_MODIFIER)

        print("His parrying bonus is:", parrying_bonus)

        parry_roll = randrange(1, 21)
        print(self._defender.name, "rolls", "*" + parry_roll + "*", "for parry")

        result = parrying_bonus + parry_roll - qoa
        result_text = str(parrying_bonus) + " + " + str(parry_roll) + " - " + str(qoa)

        if result < 0:
            print(result_text, "< 0, parry failed!")
            return False
        else:
            print(result_text, "< 0, parry succeeded!")
            return True

    def calculate_damage(self, qoa, weapon):
        print("*** DAMAGE ***")
        qoa_augmenting = 0.0  # float
        dmg_reduction = 0
        if weapon.dmg_type == "bludgeoning":
            qoa_augmenting += (1 + qoa / 20) * 0.75
            dmg_reduction += self.defender.armor.dmg_reduction.bludgeoning
        elif weapon.dmg_type == "slashing":
            qoa_augmenting += 1 + qoa / 20
            dmg_reduction += self.defender.armor.dmg_reduction.slashing
        elif weapon.dmg_type == "piercing":
            qoa_augmenting += (1 + qoa / 20) * 1.25
            dmg_reduction += self.defender.armor.dmg_reduction.piercing

        print(self._attacker.name + "'s QoA Augmenting Factor is:", qoa_augmenting)
        print(self._defender.name + "'s Damage Reduction is:", dmg_reduction)

        weapon_roll = randrange(weapon.damage[0], weapon.damage[1] + 1)
        print(self._attacker.name, "rolls", "*" + weapon_roll + "*", "for base weapon damage")

        damage_dealt = math.floor(weapon_roll * qoa_augmenting) - dmg_reduction
        damage_dealt_text = str(math.floor(weapon_roll * qoa_augmenting)) + " - " + str(dmg_reduction)

        if damage_dealt <= 0:
            print(damage_dealt, "<= 0, no damage dealt")
            return 0
        else:
            print(damage_dealt, "> 0,", self._attacker.name, "deals", "*" + damage_dealt + "*", "of damage")
            return damage_dealt

    def resolve_hit(self, qoa, weapon):
        hit_deflected = False
        if self._defender.shield is not None:
            hit_deflected = self.calculate_block(qoa)
        elif self._defender.weapon is not None or self_defender.offhand_weapon is not None:
            hit_deflected = self.calculate_parry(qoa)
        if not hit_deflected:
            self._defender.health - calculate_damage(qoa, weapon)

    def swap_sides(self):
        temp = self._attacker
        self._attacker = self._defender
        self._defender = temp


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
    rogbar.equip_weapon(WEAPONS["Short Sword"])
    rogbar.equip_offhand_weapon(WEAPONS["Short Sword"])
    rogbar.equip_armor(ARMORS["Chainmail"])

    report(dagobert)
    report(rogbar)


if __name__ == "__main__":
    main()
