from random import randrange
import math

OFFHAND_MODIFIER = 0.75
BLUDGEONING_MODIFIER = 0.75
SLASHING_MODIFIER = 1.00
PIERCING_MODIFIER = 1.25


class RoundPhase(object):
    """
    Has: attacker, defender, result
    The root for all classes in this module
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self, attacker, defender):
        super(RoundPhase, self).__init__()
        self.attacker = attacker
        self.defender = defender
        self.result = None  # depends entirely on child class calculate_result() implementation

    def calculate_result(self):  # to be overriden in child (last generation!) classes
        pass


class TwoRollsPhase(RoundPhase):
    """
    Has: attacker_roll, defender_roll
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self, attacker, defender):
        super(TwoRollsPhase, self).__init__(attacker, defender)
        self.attacker_roll = randrange(1, 21)
        self.defender_roll = randrange(1, 21)


class Initiative(TwoRollsPhase):
    """Has: implementation for result"""

    def __init__(self, attacker, defender):
        super(Initiative, self).__init__(attacker, defender)
        self.result = self.calculate_result()

    def calculate_result(self):  # returns string
        if self.attacker.offense + self.attacker_roll > self.defender.offense + self.defender_roll:
            return "attacker"
        elif self.attacker.offense + self.attacker_roll == self.defender.offense + self.defender_roll:
            return "draw"
        elif self.attacker.offense + self.attacker_roll < self.defender.offense + self.defender_roll:
            return "defender"


class Attack(TwoRollsPhase):
    """
    Has: offhand_modifier, block, parry and dmg_dealt.
    """

    # if you want an off-hand attack, pass an offhand_modifier that is not None
    def __init__(self, attacker, defender, offhand_modifier=None):
        super(Attack, self).__init__(attacker, defender)
        self.offhand_modifier = offhand_modifier
        self.result = self.calculate_result()
        self.block = None
        self.parry = None
        self.dmg_dealt = None
        if self.result >= 0:
            self.resolve()

    def calculate_result(self):  # returns int
        if self.offhand_modifier is None:  # this is not an off-hand attack
            return self.attacker.offense + self.attacker_roll - (self.defender.defense + self.defender_roll)
        else:  # this is an off-hand attack
            return math.floor(self.attacker.offense * self.offhand_modifier) + self.attacker_roll - (self.defender.defense + self.defender_roll)

    def resolve(self):
        hit_deflected = False
        if self.defender.inventory.shield is not None:
            self.block = Block(self.attacker, self.defender, self.result)
            hit_deflected = self.block.result
        elif self.defender.inventory.weapon is not None or self.defender.offhand_weapon is not None:
            self.parry = Parry(self.attacker, self.defender, self.result)
            hit_deflected = self.parry.result
        if not hit_deflected:
            if self.offhand_modifier is None:  # this is not an off-hand attack
                weapon = self.attacker.inventory.weapon
            else:  # this is an off-hand attack
                weapon = self.attacker.inventory.offhand_weapon
            self.dmg_dealt = DamageDealt(self.attacker, self.defender, self.result, weapon)
            self.defender.health -= self.dmg_dealt.result


class OneRollAfterAttackPhase(RoundPhase):
    """
    Has: roll, hit_result
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self, attacker, defender, hit_result):
        super(OneRollAfterAttackPhase, self).__init__(attacker, defender)
        self.roll = randrange(1, 21)
        self.hit_result = hit_result


class Block(OneRollAfterAttackPhase):
    """Has: implementation for result"""

    def __init__(self, attacker, defender, hit_result):
        super(Block, self).__init__(attacker, defender, hit_result)
        self.result = self.calculate_result()

    def calculate_result(self):  # returns boolean
        result = self.defender.inventory.shield.to_block + self.roll - self.hit_result
        if result < 0:
            return False
        else:
            return True


class Parry(OneRollAfterAttackPhase):
    """
    Has: parrying bonus, offhand_modifier

    Parry is possible only if the wapon used has to_parry > 0.
    There can be three possible situations:
        1) defender can parry only with main weapon ==> parrying bonus = weapon's to_parry
        2) defender can parry both with main and off-hand weapon ==>  parrying bonus = weapon's to_parry + OFFHAND_MODIFIER * off-hand weapon's to_parry
        3) defender can parry only with off-hand weapon ==> parrying bonus = OFFHAND_MODIFIER off-hand weapon's to_parry
    """

    def __init__(self, attacker, defender, hit_result, offhand_modifier=OFFHAND_MODIFIER):
        super(Parry, self).__init__(attacker, defender, hit_result)
        self.offhand_modifier = offhand_modifier
        self.parrying_bonus = self.calculate_parrying_bonus()
        self.result = self.calculate_result()

    def calculate_parrying_bonus(self):  # returns int
        parrying_bonus = 0
        # 1)
        if self.defender.inventory.weapon is not None and self.defender.inventory.offhand_weapon is None:
            parrying_bonus += self.defender.inventory.weapon.to_parry
        # 2)
        elif self.defender.inventory.weapon is not None and self.defender.inventory.offhand_weapon is not None:
            parrying_bonus += self.defender.inventory.weapon.to_parry + math.floor(self.defender.inventory.offhand_weapon.to_parry * self.offhand_modifier)
        # 3)
        elif self.defender.inventory.weapon is None and self.defender.inventory.offhand_weapon is not None:
            parrying_bonus += math.floor(self.defender.inventory.offhand_weapon.to_parry * self.offhand_modifier)

        return parrying_bonus

    def calculate_result(self):  # returns boolean
        if self.parrying_bonus <= 0:
            return False

        result = self.parrying_bonus + self.roll - self.hit_result
        if result < 0:
            return False
        else:
            return True


class DamageDealt(OneRollAfterAttackPhase):
    """Has: weapon, augmenting, reduction"""

    def __init__(self, attacker, defender, hit_result, weapon):
        super(DamageDealt, self).__init__(attacker, defender, hit_result)
        self.weapon = weapon
        self.roll = randrange(self.weapon.damage[0], self.weapon.damage[1] + 1)
        self.augmenting, self.reduction = self.calculate_dmg_factors()  # float, int
        self.result = self.calculate_result()

    def calculate_dmg_factors(self):  # returns (float, int)
        augmenting = 0.0
        reduction = 0
        if self.weapon.dmg_type == "bludgeoning":
            augmenting += (1 + self.hit_result / 20) * BLUDGEONING_MODIFIER
            reduction += self.defender.inventory.armor.dmg_reduction.bludgeoning
        elif self.weapon.dmg_type == "slashing":
            augmenting += 1 + self.hit_result / 20 * SLASHING_MODIFIER
            reduction += self.defender.inventory.armor.dmg_reduction.slashing
        elif self.weapon.dmg_type == "piercing":
            augmenting += (1 + self.hit_result / 20) * PIERCING_MODIFIER
            reduction += self.defender.inventory.armor.dmg_reduction.piercing

        return augmenting, reduction

    def calculate_result(self):  # returns int
        result = math.floor(self.roll * self.augmenting) - self.reduction
        if result <= 0:
            return 0
        else:
            return result
