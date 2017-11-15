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
        self._result = self.calculate_result()  # int or boolean depending on child class implementation

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    def calculate_result(self):
        """Calculates the result of an action. To be overridden in child classes"""
        return None


class Attack(RoundAction):
    """Has: attacker, defender, attacker_roll, defender_roll. Result is an int"""

    def __init__(self, attacker, defender):
        super(Attack, self).__init__()
        self._attacker = attacker
        self._defender = defender
        self._attacker_roll = randrange(1, 21)
        self._defender_roll = randrange(1, 21)

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
    def attacker_roll(self):
        return self._attacker_roll

    @attacker_roll.setter
    def attacker_roll(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    @property
    def defender_roll(self):
        return self._defender_roll

    @defender_roll.setter
    def defender_roll(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    def calculate_result(self):  # returns int
        return self._attacker.ofense + self._attacker_roll - (self._defender.defense + self._defender_roll)


class OffhandAttack(Attack):
    """Has: offhand_modifier"""

    def __init__(self, attacker, defender, offhand_modifier=OFFHAND_MODIFIER):
        super(OffhandAttack, self).__init__(attacker, defender)
        self._offhand_modifier = offhand_modifier

    @property
    def offhand_modifier(self):
        return self._offhand_modifier

    @offhand_modifier.setter
    def offhand_modifier(self, value):
        self._offhand_modifier = value

    def calculate_result(self):  # retuens int
        return math.floor(self.attacker.offense * OFFHAND_MODIFIER) + self.attacker_roll - (self.defender.defense + self.defender_roll)


class Block(RoundAction):
    """Has: hit (successfull attack object), roll"""

    def __init__(self, hit):
        super(Block, self).__init__()
        self._hit = hit
        self._roll = randrange(1, 21)

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

    @property
    def roll(self):
        return self._roll

    @roll.setter
    def roll(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    def calculate_result(self):  # returns boolean
        return self._hit.defender.inventory.shield.to_block + self._roll - self._hit.result


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
        self._parrying_bonus = self.calculate_parrying_bonus()
        self._offhand_modifier = offhand_modifier

    @property
    def offhand_modifier(self):
        return self._offhand_modifier

    @offhand_modifier.setter
    def offhand_modifier(self, value):
        self._offhand_modifier = value

    @property
    def parrying_bonus(self):
        return self._parrying_bonus

    @parrying_bonus.setter
    def parrying_bonus(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    def calculate_parrying_bonus(self):  # returns int
        parrying_bonus = 0
        # 1)
        if self.hit.defender.inventory.weapon is not None and self.hit.defender.inventory.offhand_weapon is None:
            parrying_bonus += self.hit.defender.inventory.weapon.to_parry
        # 2)
        elif self.hit.defender.inventory.weapon is not None and self.hit.defender.inventory.offhand_weapon is not None:
            parrying_bonus += self.hit.defender.inventory.weapon.to_parry + math.floor(self.hit.defender.inventory.offhand_weapon.to_parry * OFFHAND_MODIFIER)
        # 3)
        elif self.hit.defender.inventory.weapon is None and self.hit.defender.inventory.offhand_weapon is not None:
            parrying_bonus += math.floor(self.hit.defender.inventory.offhand_weapon.to_parry * OFFHAND_MODIFIER)

        return parrying_bonus

    def calculate_result(self):  # returns boolean
        if self._parrying_bonus <= 0:
            return False

        result = self._parrying_bonus + self.roll - self.hit.result
        if result < 0:
            return False
        else:
            return True


class DamageDealt(RoundAction):
    """Has: hit, weapon, weapon_roll, augmenting, reduction"""

    def __init__(self, hit, weapon):
        super(DamageDealt, self).__init__()
        self._hit = hit
        self._weapon = weapon
        self._weapon_roll = randrange(self._weapon.damage[0], self._weapon.damage[1] + 1)
        self._augmenting, self._reduction = self.calculate_dmg_factors()  # float, int

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        self._weapon = value

    @property
    def weapon_roll(self):
        return self._weapon_roll

    @weapon_roll.setter
    def weapon_roll(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    @property
    def augmenting(self):
        return self._augmenting

    @augmenting.setter
    def augmenting(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    @property
    def reduction(self):
        return self._reduction

    @reduction.setter
    def reduction(self, value):
        raise NotImplementedError("This setter method ought not to be called")

    def calculate_dmg_factors(self):  # returns (float, int)
        augmenting = 0.0
        reduction = 0
        if self._weapon.dmg_type == "bludgeoning":
            augmenting += (1 + self._hit.result / 20) * 0.75
            reduction += self._hit.defender.inventory.armor.dmg_reduction.bludgeoning
        elif self._weapon.dmg_type == "slashing":
            augmenting += 1 + self._hit.result / 20
            reduction += self._hit.defender.inventory.armor.dmg_reduction.slashing
        elif self._weapon.dmg_type == "piercing":
            augmenting += (1 + self._hit.result / 20) * 1.25
            reduction += self._hit.defender.inventory.armor.dmg_reduction.piercing

        return augmenting, reduction

    def calculate_result(self):  # returns int
        result = math.floor(self._weapon_roll * self._augmenting) - self._reduction
        if result <= 0:
            return 0
        else:
            return result
