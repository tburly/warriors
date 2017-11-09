from collections import namedtuple

DmgReduction = namedtuple("DmgReduction", ["slashing", "piercing", "bludgeoning"])


class Item:
    """Has: name, handedness"""

    def __init__(self, name, handedness):
        self._name = name
        self._handedness = handedness

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def handedness(self):
        return self._handedness

    @handedness.setter
    def handedness(self, value):
        self._handedness = value


class Weapon(Item):
    """Has: damage, dmg_type, to_parry"""

    def __init__(self, name, damage, handedness=1.0, to_parry=15, dmg_type="bludgeoning"):
        super(Weapon, self).__init__(name, handedness)
        self._damage = damage  # two numbers tuple
        self._dmg_type = dmg_type  # corresponding to dmg_reduction in Armor
        self._to_parry = to_parry

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
    def to_parry(self):
        return self._to_parry

    @to_parry.setter
    def to_parry(self, value):
        self._to_parry = to_parry


class Armor(Item):
    """Has: dmg_reduction, encumbrance"""

    def __init__(self, name, handedness=0.0, dmg_reduction=DmgReduction(1, 1, 1), encumbrance=5):
        super(Armor, self).__init__(name, handedness, dmg_reduction, encumbrance)
        self._dmg_reduction = dmg_reduction  # corresponding to dmg_type in Weapon
        self._encumbrance = encumbrance

    @property
    def dmg_reduction(self):
        return self._dmg_reduction

    @dmg_reduction.setter
    def dmg_reduction(self, value):
        self._dmg_reduction = value

    @property
    def encumbrance(self):
        return self._encumbrance

    @encumbrance.setter
    def encumbrance(self, value):
        self._encumbrance = encumbrance


class Shield(Armor):
    """Has: to_block"""

    def __init__(self, name, handedness=1.0, dmg_reduction=DmgReduction(3, 3, 2), encumbrance=2, to_block=15):
        super(Shield, self).__init__(name, handedness, dmg_reduction, encumbrance)
        self._to_block = to_block

    @property
    def to_block(self):
        return self._to_block

    @to_block.setter
    def to_block(self, value):
        self._to_block = value
