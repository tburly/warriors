from collections import namedtuple

DmgReduction = namedtuple("DmgReduction", ["slashing", "piercing", "bludgeoning"])


class Item(object):
    """
    Has: name
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self, name):
        super(Item, self).__init__()

        self.name = name


class OffensiveGear(Item):
    """
    Has: damage, dmg_type, handedness
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self, damage, dmg_type, handedness, **kwargs):
        super(OffensiveGear, self).__init__(**kwargs)
        self.damage = damage  # two numbers tuple
        self.dmg_type = dmg_type  # corresponding to dmg_reduction in Armor
        self.handedness = handedness

    def __str__(self):
        return "{} ({})".format(self.name, self.dmg_type)


class Weapon(OffensiveGear):
    """Has: to_parry"""

    def __init__(self, name, damage,
                 dmg_type="bludgeoning",
                 handedness=1.0,
                 to_parry=0):

        super(Weapon, self).__init__(name=name, damage=damage, dmg_type=dmg_type, handedness=handedness)
        self.to_parry = to_parry

    def __str__(self):
        return "{} ({}, {}, {}, {})".format(self.name, self.damage, self.dmg_type, self.handedness, self.to_parry)


class DefensiveGear(Item):
    """
    Has: encumbrance
    This class is treated as an abstract class and shouldn't be instantiated
    """

    def __init__(self, encumbrance, **kwargs):  # UNPACKING!
        super(DefensiveGear, self).__init__(**kwargs)
        self.encumbrance = encumbrance


class Armor(DefensiveGear):
    """Has: dmg_reduction"""

    def __init__(self, name,
                 encumbrance=0,
                 dmg_reduction=DmgReduction(1, 0, 0)):

        super(Armor, self).__init__(name=name, encumbrance=encumbrance)
        self.dmg_reduction = dmg_reduction  # corresponding to dmg_type in Weapon

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.encumbrance, self.dmg_reduction)


class Shield(DefensiveGear, OffensiveGear):
    """Has: to_block"""

    def __init__(self, name, damage,
                 dmg_type="bludgeoning",
                 handedness=0.5,
                 encumbrance=1,
                 to_block=4):

        super(Shield, self).__init__(name=name, damage=damage, dmg_type=dmg_type, handedness=handedness, encumbrance=encumbrance)
        self.to_block = to_block

    def __str__(self):
        return "{} ({}, {}, {}, {})".format(self.name, self.damage, self.dmg_type, self.handedness, self.to_block)


WEAPONS = {
    "Bare Hand": Weapon("Bare Hand", (1, 2)),
    "Longsword": Weapon("Longsword", (4, 10), "slashing", 1.0, 2),
    "Short Sword": Weapon("Short Sword", (3, 8), "slashing", 1.0, 3)
}

SHIELDS = {
    "Tower Shield": Shield("Tower Shield", (1, 4), to_block=7)
}

ARMORS = {
    "Adventurer's Garb": Armor("Adventurer's Garb"),
    "Chainmail": Armor("Chainmail", encumbrance=3, dmg_reduction=DmgReduction(8, 6, 4))
}


class Inventory(object):
    """Has: weapon, offhand_weapon, shield, armor and items"""

    def __init__(self,  # no setting offhand and shield in constructor - only setters!
                 weapon=WEAPONS["Bare Hand"],
                 armor=ARMORS["Adventurer's Garb"],
                 items=None):

        super(Inventory, self).__init__()

        self.weapon = weapon
        self._offhand_weapon = None  # property
        self._shield = None  # property
        self.armor = armor
        if items is None:
            self.items = []
        else:
            self.items = items

    def __str__(self):
        text = []
        if self.weapon is not None:
            text.append(str(self.weapon))
        if self._offhand_weapon is not None:
            text.append(str(self._offhand_weapon))
        if self._shield is not None:
            text.append(str(self._shield))
        if self.armor is not None:
            text.append(str(self.armor))
        if len(self.items) > 0:
            for item in self.items:
                text.append(str(item))

        return "\n".join(text)

    @property
    def offhand_weapon(self):
        return self._offhand_weapon

    @offhand_weapon.setter
    def offhand_weapon(self, value):
        try:
            if self._shield is not None:
                raise ValueError("Can't wield an off-hand weapon while wielding a shield")
            if self.weapon is not None:
                if self.weapon.handedness > 1.0:
                    raise ValueError("Can't wield an off-hand weapon while already wielding a greater than one-handed weapon")
            if value is not None and value.handedness > 1.0:
                raise ValueError("Can't wield a greater than one-handed weapon in off-hand")

            self._offhand_weapon = value

        except ValueError:
            self._offhand_weapon = None
            raise

    @property
    def shield(self):
        return self._shield

    @shield.setter
    def shield(self, value):
        try:
            if self._offhand_weapon is not None:
                raise ValueError("Can't wield a shield while wielding an off-hand weapon")
            if self.weapon is not None:
                if self.weapon.handedness > 1.5:
                    raise ValueError("Can't wield a shield while wielding a two-handed weapon")

            self._shield = value

        except ValueError:
            self._shield = None
            raise
