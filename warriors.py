from items import Item, Weapon, Armor, Shield, DmgReduction
import pprint

"""
CORE MECHANICS:
===============

============
BATTLE ROUND
============
Each round warriors fight. Their durability in battle depends on their HEALTH and how they perform depends on their battle prowess (OFFENSE & DEFENSE) and equipment (weapons & armor).

======================
ATTACK - CHANCE TO HIT
======================

The fight in each round starts with one warrior swinging his weapon at the other and the other trying to defend himself. The chance to hit is decided by two d20 rolls (one for the attacker and another for the defender) which represent randomness of their efforts and depends on the attacker's OFFENSE and on his opponent's DEFFENCE which represent their corresponding, inherent abilities. Attack that doesn't miss still can be blocked by the opponent's shield or parried by his weapon. To better simulate real world it's generally easier to land a hit than to evade a hit, but it's mitigated by considerably high chances TO_PARRY or TO_BLOCK it - as in a real medieval fight. Those chances depend on two factors: an inherent weapon's/shield's bonus and (in greater extent) on the quality of the attack (decided by the attack/defense rolls and battle prowess of the opponents)

Attack can have 3 different results: miss (bad for an attacker), parry/block (neutral), hit (bad for a defender). Each consecutive miss makes an unsuccessful attacker more vulnerable on his next defensive attempt (his DEFENSE gets a cumulative negative modifier - implemented as an EFFECT)

=============================================================================================================
HIT ROLLS FORMULA
OFFENCE + d20 - DEFENCE + d20 = Quality of Attack (QoA), if >= 0 ===> a hit on target (can be blocked/parried)
Example:
Dagobert's OFFENCE is 15 and he rolls 12, so his result equals: 27
Rogbar's DEFENCE is 5 and he rolls 18, so his result equals: 23
Dagobert doesn't miss with QoA of 4. Now Rogbar has a chance to parry or block.
=============================================================================================================

=============================================================================================================
DEFENSE - CHANCE TO PARRY/BLOCK ROLL FORMULA
WEAPON/SHIELD BONUS + d20 - QoA >= 0 ===> a parry/block
=============================================================================================================

TODO: CRITICAL HITS/MISSES. Critical hit should result in: 1) bypassing a chance to PARRY/BLOCK and 2) spike in DAMAGE dealt (and a chance for a special injury EFFECT). Critical misses should (maybe) provoke an attack of opportunity (a bonus attack against opponent's DEFENCE reduced to zero)

=====================
ATTACK - DAMAGE DEALT
=====================

The damage dealt after a successful hit (that didn't missed a target and wasn't blocked or parried) depends first on the weapon's DAMAGE of the attacker and on the armor's DMG_REDUCTION of the defender and second on the quality of the attack (i.e. a good hit augments the damage). Damage comes in three types: SLASHING, PIERCING & BLUDGEONING. The augmenting effect of quality of the attack is different for all types (BLUDGEONING being the least affected and PIERCING the most).

==========================
DEFENSE - DAMAGE REDUCTION
==========================

Armors provide DMG_REDUCTION - different for different types of DAMAGE. They protect best against SLASHING and worst against BLUDGEONING. Most come at a cost of ENCUMBRANCE that diminishes DEFENCE of the wearer (should be implemented as an scalable EFFECT).

TODO: Weapon DAMAGE type balance. Now BLUDGEONING is least affected by armor DMG_REDUCTION and QoA augmenting (so it balances out). PIERCING is most affected by augmenting and neutral against armor. SLASHING is worst against armor and neutral with augmenting. So slashing needs a buff and piercing a nerf. The easy way would be to introduce ENCUMBRANCE for weapons, but that logically should affect mostly BLUDGEONING type. Another one could be introducing some kind of effect like BLEEDING, exclusive only to the SLASHING type. Another would be making them the easiest one to perform a successful PARRY and the PIERCING ones the worst.

=============================================================================================================
DAMAGE ROLL FORMULA
(WEAPON DAMAGE roll * QoA Augmanting Factor) - corresponding ARMOR DMG_REDUCTION
BLUDGEONING QAF = (1 + QoA/10) * 0.75
SLASHING QAF = (1 + QoA/10) * 1.00
PIERCING QAF = (1 + QoA/10) * 1.25
=============================================================================================================

The damage dealt (if any) is subtracted from HEALTH of the warrior that was hit. If it drops below zero, he's dead and his opponent wins.

=============================================================================================================
ADDITIONAL IDEAS

PARRY/BLOCK
A successful PARRY/BLOCK could have a marginal chance of:
1) destroying either of engaged WEAPONS/SHIELDS according to it's DURABILITY
2) disarming the opponent (making him drop his WEAPON/SHIELD) - implemented as an EFFECT with special mechanics (maybe giving him chance each round to regain it at thecost of sacrificing his attack)

Warrior should be able to fight with SHIELD, but DAMAGE dealt that way should be only marginally better than bare hands.

EFFECTS
ENCUMBERED - an ARMOR (and maybe some WEAPONS) dependent DEFENCE debuff
BLEEDING - a minor DoT inflicted exclusively by SLASHING WEAPONS
EXHAUSTED - a DEFENCE debuff after prolonged fight, will help with ending them on time
INJURED(HEAD) - both OFFENCE and DEFENCE debuff, same as DISORIENTED
INJURED(HAND) - both OFFENCE and DEFENCE debuff, has to discard one WEAPON/SHIELD and fight with OFF-HAND EFFECT
INJURED(OFF-HAND) - both OFFENCE and DEFENCE debuff, has to discard one WEAPON/SHIELD
INJURED(TORSO) - both OFFENCE and DEFENCE debuff, minor augmentation of HEALTH loss, same as WEAKENED
INJURED(LEGS) - both OFFENCE and DEFENCE debuff, same as SLOWED, not as bad as DISORIENTED
WOUNDED - a severe OFFENCE and DEFENCE debuff, augmented HEALTH loss
DISARMED - has to fight with bare hands or sacrifice attacks for trying to regain his WEAPON
MISSING - -1 to DEFENCE on each consecutive miss

Future Warrior subclassed should be implemented through EFFECTS.
AURA - a DEFENCE buff for Paladin
FRENZY - an OFFENCE buff/DEFENCE debuff for Barbarian
Higher chance to DISARM for Duelist. And so on

EFFECTS also should facilitate a possible introduction of races at some point.

"""


class Warrior:
    """
    Fights, equips, gains, drops, discards. Has: name, health, was_hit, items, offense, defense, effects
    """

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
            self._items = [Weapon("Bare Hand", (1, 3), 1.0, -1), Weapon("Bare Hand", (1, 3), 1.0, -1)]
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

    def equip_item(self, item):
        self._items.append(item)

    def drop_item(self, item):
        self._items.remove(item)

    def gain_effect(self, effect):
        self._effects.append(effect)

    def discard_effect(self, effect):
        self._effects.remove(effect)


class Battle:
    """docstring for Battle"""

    def __init__(self, attacker, defender):
        self._attacker = attacker
        self._defender = defender

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
