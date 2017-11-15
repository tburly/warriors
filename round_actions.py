from random import randrange
import math

OFFHAND_MODIFIER = 0.75


class RoundAction(object):
    """
    Has: result
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self):
        super(RoundAction, self).__init__()
        self.result = self.calculate_result()  # int or boolean depending on child class implementation

    def calculate_result(self):
        """Calculates the result of an action. To be overridden in child classes"""
        return None


class Attack(RoundAction):
    """Has: attacker, defender, attacker_roll, defender_roll. Result is an int"""

    def __init__(self, attacker, defender):
        super(Attack, self).__init__()
        self.attacker = attacker
        self.defender = defender
        self.attacker_roll = randrange(1, 21)
        self.defender_roll = randrange(1, 21)

    def calculate_result(self):  # returns int
        return self.attacker.ofense + self.attacker_roll - (self.defender.defense + self.defender_roll)


class OffhandAttack(Attack):
    """Has: offhand_modifier"""

    def __init__(self, attacker, defender, offhand_modifier=OFFHAND_MODIFIER):
        super(OffhandAttack, self).__init__(attacker, defender)
        self.offhand_modifier = offhand_modifier

    def calculate_result(self):  # returns int
        return math.floor(self.attacker.offense * self.offhand_modifier) + self.attacker_roll - (self.defender.defense + self.defender_roll)


class Block(RoundAction):
    """Has: hit (successfull attack object), roll"""

    def __init__(self, hit):
        super(Block, self).__init__()
        self.hit = hit
        self.roll = randrange(1, 21)

    def calculate_result(self):  # returns boolean
        return self.hit.defender.inventory.shield.to_block + self.roll - self.hit.result


class Parry(Block):
    """
    Has: parrying bonus, offhand_modifier

    Parry is possible only if the wapon used has to_parry > 0.
    There can be three possible situations:
        1) defender can parry only with main weapon ==> parrying bonus = weapon's to_parry
        2) defender can parry both with main and off-hand weapon ==>  parrying bonus = weapon's to_parry + OFFHAND_MODIFIER * off-hand weapon's to_parry
        3) defender can parry only with off-hand weapon ==> parrying bonus = OFFHAND_MODIFIER off-hand weapon's to_parry
    """

    def __init__(self, hit, offhand_modifier=OFFHAND_MODIFIER):
        super(Parry, self).__init__(attacker, defender, hit)
        self.offhand_modifier = offhand_modifier
        self.parrying_bonus = self.calculate_parrying_bonus()

    def calculate_parrying_bonus(self):  # returns int
        parrying_bonus = 0
        # 1)
        if self.hit.defender.inventory.weapon is not None and self.hit.defender.inventory.offhand_weapon is None:
            parrying_bonus += self.hit.defender.inventory.weapon.to_parry
        # 2)
        elif self.hit.defender.inventory.weapon is not None and self.hit.defender.inventory.offhand_weapon is not None:
            parrying_bonus += self.hit.defender.inventory.weapon.to_parry + math.floor(self.hit.defender.inventory.offhand_weapon.to_parry * self.offhand_modifier)
        # 3)
        elif self.hit.defender.inventory.weapon is None and self.hit.defender.inventory.offhand_weapon is not None:
            parrying_bonus += math.floor(self.hit.defender.inventory.offhand_weapon.to_parry * self.offhand_modifier)

        return parrying_bonus

    def calculate_result(self):  # returns boolean
        if self.parrying_bonus <= 0:
            return False

        result = self.parrying_bonus + self.roll - self.hit.result
        if result < 0:
            return False
        else:
            return True


class DamageDealt(RoundAction):
    """Has: hit, weapon, weapon_roll, augmenting, reduction"""

    def __init__(self, hit, weapon):
        super(DamageDealt, self).__init__()
        self.hit = hit
        self.weapon = weapon
        self.weapon_roll = randrange(self.weapon.damage[0], self.weapon.damage[1] + 1)
        self.augmenting, self._reduction = self.calculate_dmg_factors()  # float, int

    def calculate_dmg_factors(self):  # returns (float, int)
        augmenting = 0.0
        reduction = 0
        if self.weapon.dmg_type == "bludgeoning":
            augmenting += (1 + self.hit.result / 20) * 0.75
            reduction += self.hit.defender.inventory.armor.dmg_reduction.bludgeoning
        elif self.weapon.dmg_type == "slashing":
            augmenting += 1 + self.hit.result / 20
            reduction += self.hit.defender.inventory.armor.dmg_reduction.slashing
        elif self.weapon.dmg_type == "piercing":
            augmenting += (1 + self.hit.result / 20) * 1.25
            reduction += self.hit.defender.inventory.armor.dmg_reduction.piercing

        return augmenting, reduction

    def calculate_result(self):  # returns int
        result = math.floor(self.weapon_roll * self.augmenting) - self._reduction
        if result <= 0:
            return 0
        else:
            return result
