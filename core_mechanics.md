# CORE MECHANICS
---
### BATTLE ROUND
Each round warriors fight. Their durability in battle depends on their HEALTH and how they perform depends on their battle prowess (OFFENSE & DEFENSE) and equipment (weapons & armor).

### ATTACK - CHANCE TO HIT
The fight in each round starts with one warrior swinging his weapon at the other and the other trying to defend himself. The chance to hit is decided by two d20 rolls (one for the attacker and another for the defender) which represent randomness of their efforts and depends on the attacker's OFFENSE and on his opponent's DEFFENCE which represent their corresponding, inherent abilities. Attack that doesn't miss still can be blocked by the opponent's shield or parried by his weapon. To better simulate real world it's generally easier to land a hit than to evade a hit, but it's mitigated by considerably high chances TO_PARRY or TO_BLOCK it - as in a real medieval fight. Those chances depend on two factors: an inherent weapon's/shield's bonus and (in greater extent) on the **quality of the attack** (decided by the attack/defense rolls and battle prowess of the opponents).

Attack can have 3 different results: **miss** (bad for an attacker), **parry/block** (neutral), **hit** (bad for a defender). Each consecutive miss makes an unsuccessful attacker more vulnerable on his next defensive attempt (his DEFENSE gets a cumulative negative modifier - implemented as an EFFECT).

---
##### INITIATIVE FORMULA
If warrior #1's OFFENCE + d20 - (warrior #2's OFFENCE + d20) > 0 ===> warrior #1 wins
If warrior #1's OFFENCE + d20 - (warrior #2's OFFENCE + d20) = 0 ===> draw, roll again
If warrior #1's OFFENCE + d20 - (warrior #2's OFFENCE + d20) > 0 ===> warrior #2 wins
Example:
Dagobert's OFFENCE is 12 and he rolls 12, so his result equals: 24
Rogbar's OFFENCE is 11 and he rolls 9, so his result equals: 20
Dagobert wins initiative and attacks.
---
---
##### HIT ROLLS FORMULA
OFFENCE + d20 - (DEFENCE + d20) = Quality of Attack (QoA), if >= 0 ===> a hit on target (can be blocked/parried)
Example:
Dagobert's OFFENCE is 12 and he rolls 17, so his result equals: 29
Rogbar's DEFENCE is 8 and he rolls 5, so his result equals: 13
Dagobert succeeds with QoA of 16. Now Rogbar has a chance to parry or block.
---
---
##### DEFENSE - CHANCE TO PARRY/BLOCK ROLL FORMULA
WEAPON/SHIELD BONUS + d20 - QoA >= 0 ==> a parry/block
Example:
Rogbar's shield bonus is 5 and he rolls 10, so his result equals: 15.
Dagobert performed an attack with QoA of 16, so 15 - 16 = -1. Rogbar's fails to block an incoming hit.

In case of using both a weapon and a shield, only the better of the two bonuses is used.

---

TODO: CRITICAL HITS/MISSES. Critical hit should result in: 1) bypassing a chance to PARRY/BLOCK and 2) spike in DAMAGE dealt (and a chance for a special injury EFFECT). Critical misses should (maybe) provoke an attack of opportunity (a bonus attack against opponent's DEFENCE reduced to zero).

---

### ATTACK - DAMAGE DEALT
The damage dealt after a successful hit (that didn't missed a target and wasn't blocked or parried) depends first on the weapon's DAMAGE of the attacker and on the armor's DMG_REDUCTION of the defender and second on the quality of the attack (i.e. a good hit augments the damage). Damage comes in three types: SLASHING, PIERCING & BLUDGEONING. The augmenting effect of quality of the attack is different for all types (BLUDGEONING being the least affected and PIERCING the most).

### DEFENSE - DAMAGE REDUCTION
Armors provide DMG_REDUCTION - different for different types of DAMAGE. They protect best against SLASHING and worst against BLUDGEONING. Most come at a cost of ENCUMBRANCE that diminishes DEFENCE of the wearer (should be implemented as an scalable EFFECT).

TODO: Weapon DAMAGE type balance. Now BLUDGEONING is least affected by armor DMG_REDUCTION and QoA augmenting (so it balances out). PIERCING is most affected by augmenting and neutral against armor. SLASHING is worst against armor and neutral with augmenting. So slashing needs a buff and piercing a nerf. The easy way would be to introduce ENCUMBRANCE for weapons, but that logically should affect mostly BLUDGEONING type. Another one could be introducing some kind of effect like BLEEDING, exclusive only to the SLASHING type. Another would be making them the easiest one to perform a successful PARRY and the PIERCING ones the worst.

---
##### DAMAGE ROLL FORMULA
(WEAPON DAMAGE roll * QoA Augmenting Factor) floored - corresponding ARMOR DMG_REDUCTION
BLUDGEONING QAF = (1 + QoA/20) * 0.75
SLASHING QAF = (1 + QoA/20) * 1.00
PIERCING QAF = (1 + QoA/20) * 1.25
Example:
Dagobert's longsword deals 4-10 of base damage. He rolls 8. Longsword is a slashing weapon and his QoA is 16, so his QoA Augmenting Facor equals: 1 + 0.8 = 1.8. That means: 8 * 1.8 = 14.4. Rounded down to integer it's 14. Rogbar's chainmail has slashing damage redection of 8. That means he is dealt 6 points of damage.
---

The damage dealt (if any) is subtracted from HEALTH of the warrior that was hit. If it drops below zero, he's dead and his opponent wins.

***
### ADDITIONAL IDEAS

##### PARRY/BLOCK
A successful PARRY/BLOCK could have a marginal chance of:
1) destroying either of engaged WEAPONS/SHIELDS according to it's DURABILITY,
2) disarming the opponent (making him drop his WEAPON/SHIELD) - implemented as an EFFECT with special mechanics (maybe giving him chance each round to regain it at the cost of sacrificing his attack).

Warrior should be able to fight with SHIELD, but DAMAGE dealt that way should be only marginally better than bare hands.

##### EFFECTS
ENCUMBERED - an ARMOR (and maybe some WEAPONS) dependent DEFENCE debuff
BLEEDING - a minor DoT inflicted exclusively by SLASHING WEAPONS
EXHAUSTED - a DEFENCE debuff after prolonged fight, will help with ending them on time, makes more sense with additional warrior stats like STRENGTH and CONSTITUTION
INJURED(HEAD) - both OFFENCE and DEFENCE debuff, same as DISORIENTED
INJURED(HAND) - both OFFENCE and DEFENCE debuff, has to discard one WEAPON and fight with off-hand
INJURED(OFF-HAND) - both OFFENCE and DEFENCE debuff, has to discard one WEAPON/SHIELD
INJURED(TORSO) - both OFFENCE and DEFENCE debuff, minor augmentation of HEALTH loss, same as WEAKENED
INJURED(LEGS) - both OFFENCE and DEFENCE debuff, same as SLOWED, not as bad as DISORIENTED
WOUNDED - a severe OFFENCE and DEFENCE debuff, augmented HEALTH loss
DISARMED - has to fight with bare hands or sacrifice attacks for trying to regain his WEAPON
MISS - -1 to DEFENCE on each consecutive miss (can be applied many times)
(maybe) Instant fight's end DEATH effects after some crits with very slim chances of happening and some variations like DEATH(IMPALED), DEATH(DECAPITATED), DEATH(DISEMBOWELED), DEATH(CRUSHED) for flavor

##### RACES & CLASSES
Future Warrior subclasses should be implemented through EFFECTS, e.g.:
AURA - a DEFENCE buff for *Paladin*
FRENZY - an OFFENCE buff/DEFENCE debuff for *Barbarian*
Higher chance to DISARM for *Duelist*. And so on

EFFECTS also should facilitate a possible introduction of races at some point.

Introduction of STRENGTH, DEXTERITY & CONSTITUTION (and maybe some MAGIC) would spice things a lot, but maybe let's not overcomplicate everything too much from the start.

STRENGTH should affect DAMAGE dealt most (BLUDGEONING > SLASHING > PIERCING).
DEXTERITY should affect OFFENSE & DEFENSE most.
CONSTITUTION should affect HEALTH most.
