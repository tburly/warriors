#!/usr/bin/env python3

from items import Inventory, WEAPONS, SHIELDS, ARMORS
from effects import Effect, EFFECTS
from round_actions import Attack, Block, Parry, DamageDealt, OFFHAND_MODIFIER
import math
from random import randrange

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
    """Commences. Has: attacker, defender"""

    def __init__(self, attacker, defender):
        super(Battle, self).__init__()

        self.attacker = attacker
        self.defender = defender
        self.rounds_count = 1

    def resolve_initiative(self):
        print()
        print("******** BATTLE ********")
        print("Two brave warriors came to fight today:")
        print(str(self.attacker))
        print(str(self.defender))

        while True:
            attacker_roll = randrange(1, 21)
            defender_roll = randrange(1, 21)

            print(self.attacker.name, "rolls", "*" + str(attacker_roll) + "*", "for initiative")
            print(self.defender.name, "rolls", "*" + str(defender_roll) + "*", "for initiative")

            attacker_result = self.attacker.offense + attacker_roll
            defender_result = self.defender.offense + defender_roll

            if attacker_result > defender_result:
                print(str(self.attacker.offense) + " + " + str(attacker_roll), ">", str(self.defender.offense) + " + " + str(defender_roll) + ".", self.attacker.name, "wins initiative")
                print("Let the battle begin!")
                break

            elif attacker_result == defender_result:
                print(str(self.attacker.offense) + " + " + str(attacker_roll), "=", str(self.defender.offense) + " + " + str(defender_roll) + ". Draw! Let's roll again")
                continue

            elif attacker_result < defender_result:
                print(str(self.attacker.offense) + " + " + str(attacker_roll), "<", str(self.defender.offense) + " + " + str(defender_roll) + ".", self.defender.name, "wins initiative")
                print("Let the battle begin!")
                self.swap_sides()
                break

    def commence(self):
        self.resolve_initiative()

        while True:
            print()
            print("******** ROUND #" + str(self.rounds_count), "********")
            print("Attacker is:", str(self.attacker))
            print("Defender is:", str(self.defender))
            self.resolve_round()

            if self.attacker.health <= 0:
                print("************************")
                print(self.defender.name + "'s health is: ", self.defender.health)
                print(self.attacker.name + "'s health is: ", self.attacker.health)
                print(self.defender.name, "wins after", self.rounds_count, "rounds of relentless battle.")
                print()
                print("************************************************************************************")
                print("*************************************** END ****************************************")
                print("************************************************************************************")
                print()
                break

            elif self.defender.health <= 0:
                print("************************")
                print(self.attacker.name + "'s health is: ", self.attacker.health)
                print(self.defender.name + "'s health is: ", self.defender.health)
                print(self.attacker.name, "wins after", self.rounds_count, "rounds of relentless battle.")
                print()
                print("************************************************************************************")
                print("*************************************** END ****************************************")
                print("************************************************************************************")
                print()
                break

    def resolve_round(self):
        misses = 0
        hits = 0

        # attack
        quality_of_attack = self.calculate_attack()
        if quality_of_attack < 0:
            print("It's a miss!")
            misses += 1

        else:
            print("It's a hit!")
            hits += 1
            self.resolve_hit(quality_of_attack, self.attacker.inventory.weapon)

        # off-hand attack
        if self.attacker.inventory.offhand_weapon is not None:
            quality_of_offhand_attack = self.calculate_offhand_attack()
            if quality_of_offhand_attack < 0:
                print("It's a miss!")
                misses += 1

            else:
                print("It's a hit!")
                hits += 1
                self.resolve_hit(quality_of_offhand_attack, self.attacker.inventory.offhand_weapon)

        # MISS effect
        if misses > 0 and hits == 0:  # only one miss counts (if there were no hits)
            self.attacker.gain_effect(Effect(EFFECTS["miss"]))
        if hits > 0:
            # clear all MISS effects on the attacker
            for miss in [effect for effect in self.attacker.effects if effect.name == EFFECTS["miss"]]:
                self.attacker.discard_effect(miss)

        self.swap_sides()
        self.rounds_count += 1

    def calculate_attack(self):
        print("*** ATTACK ***")
        print(self.attacker.name, "swings his", self.attacker.inventory.weapon.name.lower(), "at", self.defender.name)
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        print(self.attacker.name, "rolls", "*" + str(attacker_roll) + "*", "for attack")
        print(self.defender.name, "rolls", "*" + str(defender_roll) + "*", "for defense")

        quality_of_attack = self.attacker.offense + attacker_roll - (self.defender.defense + defender_roll)

        qoa_text = str(self.attacker.offense) + " + " + str(attacker_roll) + " - " + str(self.defender.defense) + " - " + str(defender_roll) + " ="
        print(self.attacker.name + "'s QoA is:", qoa_text, quality_of_attack)

        return quality_of_attack

    def calculate_offhand_attack(self):
        print("*** OFF-HAND ATTACK ***")
        print(self.attacker.name, "swings his", self.attacker.inventory.offhand_weapon.name.lower(), "at", self.defender.name)
        attacker_roll = randrange(1, 21)
        defender_roll = randrange(1, 21)
        print(self.attacker.name, "rolls", "*" + str(attacker_roll) + "*", "for off-hand attack")
        print(self.defender.name, "rolls", "*" + str(defender_roll) + "*", "for defense")

        # Fighting with an off-hand weapon is 25% tougher, so OFFENCE = OFFENCE * OFFHAND_MODIFIER (floored)
        quality_of_attack = math.floor(self.attacker.offense * OFFHAND_MODIFIER) + attacker_roll - (self.defender.defense + defender_roll)

        qoa_text = str(math.floor(self.attacker.offense * OFFHAND_MODIFIER)) + " + " + str(attacker_roll) + " - " + str(self.defender.defense) + " - " + str(defender_roll) + " ="
        print(self.attacker.name + "'s off-hand QoA is:", qoa_text, quality_of_attack)

        return quality_of_attack

    def calculate_block(self, qoa):
        print("*** BLOCK ***")
        print(self.defender.name, "tries to block with his shield")
        print("His blocking bonus is:", self.defender.inventory.shield.to_block)
        block_roll = randrange(1, 21)
        print(self.defender.name, "rolls", "*" + str(block_roll) + "*", "for block")

        result = self.defender.inventory.shield.to_block + block_roll - qoa
        result_text = str(self.defender.inventory.shield.to_block) + " + " + str(block_roll) + " - " + str(qoa)

        if result < 0:
            print(result_text, "< 0, block failed!")
            return False
        else:
            print(result_text, "> 0, block succeeded!")
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
        if self.defender.inventory.weapon is not None and self.defender.inventory.offhand_weapon is None:
            print(self.defender.name, "tries to parry with his main weapon")
            parrying_bonus += self.defender.inventory.weapon.to_parry
        # 2)
        elif self.defender.inventory.weapon is not None and self.defender.inventory.offhand_weapon is not None:
            print(self.defender.name, "tries to parry with both his weapons")
            parrying_bonus += self.defender.inventory.weapon.to_parry + math.floor(self.defender.inventory.offhand_weapon.to_parry * OFFHAND_MODIFIER)
        # 3)
        elif self.defender.inventory.weapon is None and self.defender.inventory.offhand_weapon is not None:
            print(self.defender.name, "tries to parry with his off-hand weapon")
            parrying_bonus += math.floor(self.defender.inventory.offhand_weapon.to_parry * OFFHAND_MODIFIER)

        if parrying_bonus <= 0:
            print("His parrying bonus is:", parrying_bonus)
            print(self.defender.name, "has no weapon to parry with. Parry failed!")
            return False

        print("His parrying bonus is:", parrying_bonus)

        parry_roll = randrange(1, 21)
        print(self.defender.name, "rolls", "*" + str(parry_roll) + "*", "for parry")

        result = parrying_bonus + parry_roll - qoa
        result_text = str(parrying_bonus) + " + " + str(parry_roll) + " - " + str(qoa)

        if result < 0:
            print(result_text, "< 0, parry failed!")
            return False
        else:
            print(result_text, "> 0, parry succeeded!")
            return True

    def calculate_damage(self, qoa, weapon):
        print("*** DAMAGE ***")
        qoa_augmenting = 0.0  # float
        dmg_reduction = 0
        if weapon.dmg_type == "bludgeoning":
            qoa_augmenting += (1 + qoa / 20) * 0.75
            dmg_reduction += self.defender.inventory.armor.dmg_reduction.bludgeoning
        elif weapon.dmg_type == "slashing":
            qoa_augmenting += 1 + qoa / 20
            dmg_reduction += self.defender.inventory.armor.dmg_reduction.slashing
        elif weapon.dmg_type == "piercing":
            qoa_augmenting += (1 + qoa / 20) * 1.25
            dmg_reduction += self.defender.inventory.armor.dmg_reduction.piercing

        print(self.attacker.name + "'s QoA Augmenting Factor is:", qoa_augmenting)
        print(self.defender.name + "'s Damage Reduction is:", dmg_reduction)

        weapon_roll = randrange(weapon.damage[0], weapon.damage[1] + 1)
        print(self.attacker.name, "rolls", "*" + str(weapon_roll) + "*", "for base weapon damage")

        damage_dealt = math.floor(weapon_roll * qoa_augmenting) - dmg_reduction
        damage_dealt_text = str(math.floor(weapon_roll * qoa_augmenting)) + " - " + str(dmg_reduction)

        if damage_dealt <= 0:
            print(damage_dealt_text, "<= 0, no damage dealt")
            return 0
        else:
            print(damage_dealt_text, "> 0,", self.attacker.name, "deals", "*" + str(damage_dealt) + "*", "of damage")
            return damage_dealt

    def resolve_hit(self, qoa, weapon):
        hit_deflected = False
        if self.defender.inventory.shield is not None:
            hit_deflected = self.calculate_block(qoa)
        elif self.defender.inventory.weapon is not None or self_defender.offhand_weapon is not None:
            hit_deflected = self.calculate_parry(qoa)
        if not hit_deflected:
            self.defender.health -= self.calculate_damage(qoa, weapon)

    def swap_sides(self):
        temp = self.attacker
        self.attacker = self.defender
        self.defender = temp


class Round(object):
    """Has: attacker, defender, attack, offhand_attack"""

    def __init__(self, attacker, defender):
        super(Round, self).__init__()
        self.attacker = attacker
        self.defender = defender
        self.attack = Attack(self.attacker, self.defender)
        if self.attacker.inventory.offhand_weapon is not None:
            self.offhand_attack = Attack(self.attacker, self.defender, OFFHAND_MODIFIER)
        else:
            self.offhand_attack = None


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
