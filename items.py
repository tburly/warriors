from collections import namedtuple

DmgReduction = namedtuple("DmgReduction", ["slashing", "piercing", "bludgeoning"])

# self._items = [Weapon(name="Bare Hand",
#                       damage=(1, 3),
#                       dmg_type="bludgeoning",
#                       handedness=1.0,
#                       to_parry=-1),


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
                 to_parry=-1):

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
                 encumbrance=5,
                 dmg_reduction=DmgReduction(1, 1, 1)):

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
                 handedness=1.0,
                 encumbrance=1,
                 to_block=-1):

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
