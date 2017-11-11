from collections import namedtuple

DmgReduction = namedtuple("DmgReduction", ["slashing", "piercing", "bludgeoning"])


class Item(object):
    """
    Has: name

    This class is treated as an abstract class and shouldn't be instantiated"
    """

    def __init__(self, name):
        super(Item, self).__init__()

        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


class OffensiveGear(Item):
    """
    Has: damage, dmg_type, handedness

    This class is treated as an abstract class and shouldn't be instantiated"
    """

    def __init__(self, damage, dmg_type, handedness, **kwargs):
        super(OffensiveGear, self).__init__(**kwargs)
        self._damage = damage  # two numbers tuple
        self._dmg_type = dmg_type  # corresponding to dmg_reduction in Armor
        self._handedness = handedness

    def __str__(self):
        return "{} ({})".format(self._name, self._dmg_type)

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def dmg_type(self):
        return self._dmg_type

    @dmg_type.setter
    def dmg_type(self, value):
        self._dmg_type = value

    @property
    def handedness(self):
        return self._handedness

    @handedness.setter
    def handedness(self, value):
        self._handedness = value


class Weapon(OffensiveGear):
    """Has: to_parry"""

    def __init__(self, name, damage,
                 dmg_type="bludgeoning",
                 handedness=1.0,
                 to_parry=0):

        super(Weapon, self).__init__(name=name, damage=damage, dmg_type=dmg_type, handedness=handedness)
        self._to_parry = to_parry

    def __str__(self):
        return "{} ({}, {}, {}, {})".format(self.name, self.damage, self.dmg_type, self.handedness, self.to_parry)

    @property
    def to_parry(self):
        return self._to_parry

    @to_parry.setter
    def to_parry(self, value):
        self._to_parry = to_parry


class DefensiveGear(Item):
    """
    Has: encumbrance

    This class is treated as an abstract class and shouldn't be instantiated"
    """

    def __init__(self, encumbrance, **kwargs):  # UNPACKING!
        super(DefensiveGear, self).__init__(**kwargs)
        self._encumbrance = encumbrance

    @property
    def encumbrance(self):
        return self._encumbrance

    @encumbrance.setter
    def encumbrance(self, value):
        self._encumbrance = encumbrance


class Armor(DefensiveGear):
    """Has: dmg_reduction"""

    def __init__(self, name,
                 encumbrance=0,
                 dmg_reduction=DmgReduction(1, 0, 0)):

        super(Armor, self).__init__(name=name, encumbrance=encumbrance)
        self._dmg_reduction = dmg_reduction  # corresponding to dmg_type in Weapon

    def __str__(self):
        return "{} ({}, {})".format(self.name, self.encumbrance, self.dmg_reduction)

    @property
    def dmg_reduction(self):
        return self._dmg_reduction

    @dmg_reduction.setter
    def dmg_reduction(self, value):
        self._dmg_reduction = value


class Shield(DefensiveGear, OffensiveGear):
    """Has: to_block"""

    def __init__(self, name, damage,
                 dmg_type="bludgeoning",
                 handedness=0.5,
                 encumbrance=1,
                 to_block=15):

        super(Shield, self).__init__(name=name, damage=damage, dmg_type=dmg_type, handedness=handedness, encumbrance=encumbrance)
        self._to_block = to_block

    def __str__(self):
        return "{} ({}, {}, {}, {})".format(self.name, self.damage, self.dmg_type, self.handedness, self.to_block)

    @property
    def to_block(self):
        return self._to_block

    @to_block.setter
    def to_block(self, value):
        self._to_block = value


WEAPONS = {
    "Bare Hand": Weapon("Bare Hand", (1, 3)),
    "Longsword": Weapon("Longsword", (5, 12), "slashing", 1.0, 15)
}

SHIELDS = {
    "Tower Shield": Shield("Tower Shield", (1, 4), to_block=25)
}

ARMORS = {
    "Adventurer's Garb": Armor("Adventurer's Garb"),
    "Chainmail": Armor("Chainmail", encumbrance=3, dmg_reduction=DmgReduction(4, 3, 2))
}


class Inventory(object):
    """Has: weapon, offhand_weapon, shield, armor and items"""

    def __init__(self,  # no setting offhand and shield in constructor - only setters!
                 weapon=WEAPONS["Bare Hand"],
                 armor=ARMORS["Adventurer's Garb"],
                 items=None):

        super(Inventory, self).__init__()

        self._weapon = weapon
        self._offhand_weapon = None
        self._shield = None
        self._armor = armor
        if items is None:
            self._items = []
        else:
            self._items = items

    def __str__(self):
        text = []
        if self._weapon is not None:
            text.append(str(self._weapon))
        if self._offhand_weapon is not None:
            text.append(str(self._offhand_weapon))
        if self._shield is not None:
            text.append(str(self._shield))
        if self._armor is not None:
            text.append(str(self._armor))
        if len(self.items) > 0:
            for item in self.items:
                text.append(str(item))

        return "\n".join(text)

    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        self._weapon = value

    @property
    def offhand_weapon(self):
        return self._offhand_weapon

    @offhand_weapon.setter
    def offhand_weapon(self, value):
        try:
            if self._shield is not None:
                raise ValueError("Can't wield an off-hand weapon while wielding a shield")
            if self._weapon is not None:
                if self._weapon.handedness > 1.0:
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
            if self._weapon is not None:
                if self._weapon.handedness > 1.5:
                    raise ValueError("Can't wield a shield while wielding a two-handed weapon")

            self._shield = value

        except ValueError:
            self._shield = None
            raise

    @property
    def armor(self):
        return self._armor

    @armor.setter
    def armor(self, value):
        self._armor = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value
