# CORE MECHANICS
---
### BATTLE ROUND
Each round warriors fight. Their durability in battle depends on their HEALTH and how they perform depends on their battle prowess (OFFENSE & DEFENSE) and equipment (weapons & armor).

### ATTACK - CHANCE TO HIT
The fight in each round starts with one warrior swinging his weapon at the other and the other trying to defend himself. The chance to hit is decided by two d20 rolls (one for the attacker and another for the defender) which represent randomness of their efforts and depends on the attacker's OFFENSE and on his opponent's DEFFENCE which represent their corresponding, inherent abilities. Attack that doesn't miss still can be blocked by the opponent's shield or parried by his weapon. To better simulate real world it's generally easier to land a hit than to evade a hit, but it's mitigated by considerably high chances TO_PARRY or TO_BLOCK it - as in a real medieval fight. Those chances depend on two factors: an inherent weapon's/shield's bonus and (in greater extent) on the **quality of the attack** (decided by the attack/defense rolls and battle prowess of the opponents)

Attack can have 3 different results: **miss** (bad for an attacker), **parry/block** (neutral), **hit** (bad for a defender). Each consecutive miss makes an unsuccessful attacker more vulnerable on his next defensive attempt (his DEFENSE gets a cumulative negative modifier - implemented as an EFFECT)

---
##### HIT ROLLS FORMULA
OFFENCE + d20 - DEFENCE + d20 = Quality of Attack (QoA), if >= 0 ===> a hit on target (can be blocked/parried)
Example:
Dagobert's OFFENCE is 15 and he rolls 12, so his result equals: 27
Rogbar's DEFENCE is 5 and he rolls 18, so his result equals: 23
Dagobert doesn't miss with QoA of 4. Now Rogbar has a chance to parry or block.
---
---
##### DEFENSE - CHANCE TO PARRY/BLOCK ROLL FORMULA
WEAPON/SHIELD BONUS + d20 - QoA >= 0 ==> a parry/block
In case of using both a weapon and a shield, only the better of the two bonuses is used.
---

TODO: CRITICAL HITS/MISSES. Critical hit should result in: 1) bypassing a chance to PARRY/BLOCK and 2) spike in DAMAGE dealt (and a chance for a special injury EFFECT). Critical misses should (maybe) provoke an attack of opportunity (a bonus attack against opponent's DEFENCE reduced to zero)

### ATTACK - DAMAGE DEALT
The damage dealt after a successful hit (that didn't missed a target and wasn't blocked or parried) depends first on the weapon's DAMAGE of the attacker and on the armor's DMG_REDUCTION of the defender and second on the quality of the attack (i.e. a good hit augments the damage). Damage comes in three types: SLASHING, PIERCING & BLUDGEONING. The augmenting effect of quality of the attack is different for all types (BLUDGEONING being the least affected and PIERCING the most).

### DEFENSE - DAMAGE REDUCTION
Armors provide DMG_REDUCTION - different for different types of DAMAGE. They protect best against SLASHING and worst against BLUDGEONING. Most come at a cost of ENCUMBRANCE that diminishes DEFENCE of the wearer (should be implemented as an scalable EFFECT).

TODO: Weapon DAMAGE type balance. Now BLUDGEONING is least affected by armor DMG_REDUCTION and QoA augmenting (so it balances out). PIERCING is most affected by augmenting and neutral against armor. SLASHING is worst against armor and neutral with augmenting. So slashing needs a buff and piercing a nerf. The easy way would be to introduce ENCUMBRANCE for weapons, but that logically should affect mostly BLUDGEONING type. Another one could be introducing some kind of effect like BLEEDING, exclusive only to the SLASHING type. Another would be making them the easiest one to perform a successful PARRY and the PIERCING ones the worst.

---
##### DAMAGE ROLL FORMULA
(WEAPON DAMAGE roll * QoA Augmanting Factor) - corresponding ARMOR DMG_REDUCTION
BLUDGEONING QAF = (1 + QoA/10) * 0.75
SLASHING QAF = (1 + QoA/10) * 1.00
PIERCING QAF = (1 + QoA/10) * 1.25
---

The damage dealt (if any) is subtracted from HEALTH of the warrior that was hit. If it drops below zero, he's dead and his opponent wins.

***
### ADDITIONAL IDEAS

##### PARRY/BLOCK
A successful PARRY/BLOCK could have a marginal chance of:
1) destroying either of engaged WEAPONS/SHIELDS according to it's DURABILITY
2) disarming the opponent (making him drop his WEAPON/SHIELD) - implemented as an EFFECT with special mechanics (maybe giving him chance each round to regain it at thecost of sacrificing his attack)

Warrior should be able to fight with SHIELD, but DAMAGE dealt that way should be only marginally better than bare hands.

##### EFFECTS
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
MISSE - -1 to DEFENCE on each consecutive miss (can be applied many times)

##### RACES & CLASSES
Future Warrior subclasses should be implemented through EFFECTS, e.g.:
AURA - a DEFENCE buff for *Paladin*
FRENZY - an OFFENCE buff/DEFENCE debuff for *Barbarian*
Higher chance to DISARM for *Duelist*. And so on

EFFECTS also should facilitate a possible introduction of races at some point.
