from items import Item, Weapon, Armor, Shield, DmgReduction
import pprint

"""
CORE MECHANICS:
===============

BATTLE ROUND

Each round warriors fight. Their durability in battle depends on their HEALTH and how they perform depends on their battle prowess (OFFENSE & DEFENSE) and equipment (weapons & armor).

ATTACK - CHANCE TO HIT

The fight in each round starts with one warrior swinging his weapon at the other and the other trying to defend himself. The chance to hit is decided by two d20 rolls (one for the attacker and another for the defender) which represent randomness of their efforts and depends on the attacker's OFFENSE and on his opponent's DEFFENCE which represent their corresponding, inherent abilities. Attack that doesn't miss still can be blocked by the opponent's shield or parried by his weapon. To better simulate real world it's generally easier to land a hit than to evade a hit, but it's mitigated by considerably high chances TO_PARRY or TO_BLOCK it - as in a real medieval fight. Those chances depend on two factors: an inherent weapon's/shield's bonus and (in greater extent) on the quality of the attack (decided by the attack/defense rolls and battle prowess of the opponents)

Attack can have 3 different results: miss (bad for an attacker), parry/block (neutral), hit (bad for a defender). Each consecutive miss makes an unsuccessful attacker more vulnerable on his next defensive attempt (his DEFENSE gets a cumulative negative modifier - implemented as an EFFECT)

HIT ROLLS FORMULA
OFFENCE + d20 - DEFENCE + d20 = Quality of Attack (QoA), if >= 0 ===> a hit on target
Example:
Dagobert's OFFENCE is 15 and he rolls 12, so his result equals: 27
Robar's DEFENCE is 5 and he rolls 18, so his result equals: 23
Dagobert doesn't miss with QoA of 4. Now Robar has a chance to parry or block.

DEFENSE - CHANCE TO PARRY/BLOCK ROLL FORMULA
WEAPON/SHIELD BONUS + d20 - QoA >= 0 ===> a parry/block

TODO: CRITICAL HITS/MISSES. Critical hit should result in: 1) bypassing a chance to PARRY/BLOCK and 2) spike in DAMAGE dealt (and a chance for a special injury EFFECT). Critical misses should (maybe) provoke an attack of opportunity (a bonus attack against opponent's DEFENCE reduced to zero)

ATTACK - DAMAGE DEALT

The damage dealt after a successful hit (that didn't missed a target and wasn't blocked or parried) depends first on the weapon's DAMAGE of the attacker and on the armor's DMG_REDUCTION of the defender and second on the quality of the attack (i.e. a good hit augments the damage). Damage comes in three types: SLASHING, PIERCING & BLUDGEONING. The augmenting effect of quality of the attack is different for all types (BLUDGEONING being the least affected and PIERCING the most).

DEFENSE - DAMAGE REDUCTION

Armors provide DMG_REDUCTION - different for different types of DAMAGE. They protect best against SLASHING and worst against BLUDGEONING. Most come at a cost of ENCUMBRANCE that diminishes DEFENCE of the wearer (should be implemented as an scalable EFFECT).

TODO: Weapon DAMAGE type balance. Now BLUDGEONING is least affected by armor DMG_REDUCTION and QoA augmenting (so it balances out). PIERCING is most affected by augmenting and neutral against armor. SLASHING is worst against armor and neutral with augmenting. So slashing needs a buff and piercing a nerf. The easy way would be to introduce ENCUMBRANCE for weapons, but that logically should affect mostly BLUDGEONING type. Another one could be introducing some kind of effect like BLEEDING, exclusive only to the SLASHING type. Another would be making them the easiest one to perform a successful PARRY and the PIERCING ones the worst.

DAMAGE ROLL FORMULA
(WEAPON DAMAGE roll * QoA Augmanting Factor) - corresponding ARMOR DMG_REDUCTION
BLUDGEONING QAF = (1 + QoA/10) * 0.75
SLASHING QAF = (1 + QoA/10) * 1.00
PIERCING QAF = (1 + QoA/10) * 1.25

The damage dealt (if any) is subtracted from HEALTH of the warrior that was hit. If it drops below zero, he's dead and his opponent wins.
"""


class Warrior:
    """Fights, equips, drops. Has: name, health, was_hit, items, offense, defense, effects"""

    def __init__(self, name,
                 health=30,
                 was_hit=False,
                 items=None,
                 offense=10,
                 defense=5,
                 effects=None):

        self._name = name
        self._health = health
        self._was_hit = was_hit
        if items is None:
            self._items = [Weapon("Bare Hand", (1, 3), 1.0, 0), Weapon("Bare Hand", (1, 3), 1.0, 0)]
        else:
            self._items = items
        self._offense = offense
        self._defense = defense
        self._misses_count = misses_count
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
    def was_hit(self):
        return self._was_hit

    @was_hit.setter
    def was_hit(self, value):
        self._was_hit = was_hit

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = items

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
    def effects(self):
        return self._effects

    @effects.setter
    def effects(self, value):
        self._effects = effects

    def attack(self, opponent, weapon):
        pass

    def equip(self, item):
        self._items.append(item)

    def drop(self, item):
        self._items.remove(item)


def main():
    dagobert = Warrior("Dagobert")
    print()
    pprint.pprint(dir(dagobert))
    print("Hail, my good fellow. My name is {}. My health is {}. If someone says I was hit, then it's {}. I'm equipped with: {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}".format(dagobert.name, dagobert.health, dagobert.was_hit, ["{} ({}, {}, {})".format(item.name, item.handedness, item.dmg_type, item.to_parry) for item in dagobert.items], dagobert.offense, dagobert.defense, dagobert.effects))
    print(type(dagobert.name))
    print("handedness:", dagobert.items[0].handedness)
    print("dmg_type: ", dagobert.items[0].dmg_type)
    print("to_parry:", dagobert.items[0].to_parry)


main()
