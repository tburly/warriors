"""
Functions bundled in this module make various announcements about the current game state to the standard output
"""

import math


def introduce_battle(attacker, defender):
    print()
    print("********* BATTLE *********")
    print("Two brave warriors came to fight today:")
    print(str(attacker))
    print(str(defender))


def report_initiative(initiative):
    print(initiative.attacker.name, "rolls", "*" + str(initiative.attacker_roll) + "*", "for initiative")
    print(initiative.defender.name, "rolls", "*" + str(initiative.defender_roll) + "*", "for initiative")

    if initiative.result == "attacker":
        sign = ">"
        ending = initiative.attacker.name + " wins initiative\nLet the battle begin!"
    elif initiative.result == "draw":
        sign = "="
        ending = " Draw! Let's roll again"
    elif initiative.result == "defender":
        sign = "<"
        ending = initiative.defender.name + " wins initiative\nLet the battle begin!"

    print(str(initiative.attacker.offense) + " + " + str(initiative.attacker_roll), sign, str(initiative.defender.offense) + " + " + str(initiative.defender_roll) + ",", ending)


def introduce_round(attacker, defender, rounds_count):
    print()
    print("******** ROUND #" + str(rounds_count), "********")
    print("Attacker is:", str(attacker))
    print("Defender is:", str(defender))


def report_attack(attack):
    if attack.offhand_modifier is None:
        intro = "*** ATTACK ***"
        weapon_name = attack.attacker.inventory.weapon.name.lower()
        offense_text = str(attack.attacker.offense)
        attack_text = "attack"
    else:
        intro = "*** OFF-HAND ATTACK ***"
        weapon_name = attack.attacker.inventory.offhand_weapon.name.lower()
        offense_text = str(math.floor(attack.attacker.offense * attack.offhand_modifier))
        attack_text = "off-hand attack"

    print(intro)
    print(attack.attacker.name, "swings his", weapon_name, "at", attack.defender.name)
    print("He rolls", "*" + str(attack.attacker_roll) + "*", "for", attack_text)
    print(attack.defender.name, "tries to fend off the attack")
    print("He rolls", "*" + str(attack.defender_roll) + "*", "for defense")
    result_text = offense_text + " + " + str(attack.attacker_roll) + " - " + str(attack.defender.defense) + " - " + str(attack.defender_roll) + " ="
    print("The result of", attack.attacker.name + "'s", attack_text, "is:", result_text, attack.result)
    if attack.result < 0:
        print("It's a miss!")
    else:
        print("It's a hit!")

    # block/parry, damage dealt
    if attack.block is not None:
        report_block(attack.block)
    if attack.parry is not None:
        report_parry(attack.parry)
    if attack.dmg_dealt is not None:
        report_damage(attack.dmg_dealt)


def report_block(block):
    print("*** BLOCK ***")
    print(block.defender.name, "tries to block with his", block.defender.inventory.shield.name.lower())
    print("His blocking bonus is:", block.defender.inventory.shield.to_block)
    print(block.defender.name, "rolls", "*" + str(block.roll) + "*", "for block")
    result_text = str(block.defender.inventory.shield.to_block) + " + " + str(block.roll) + " - " + str(block.hit_result)
    if block.result:
        print(result_text, "> 0, block succeeded!")
    else:
        print(result_text, "< 0, block failed!")


def report_parry(parry):
    print("*** PARRY ***")
    if parry.defender.inventory.weapon is not None and parry.defender.inventory.offhand_weapon is None:
        print(parry.defender.name, "tries to parry with his", parry.defender.inventory.weapon.name.lower())
    elif parry.defender.inventory.weapon is not None and parry.defender.inventory.offhand_weapon is not None:
        print(parry.defender.name, "tries to parry with both his weapons")
    elif parry.defender.inventory.weapon is None and parry.defender.inventory.offhand_weapon is not None:
        print(parry.defender.name, "tries to parry with his off-hand", parry.defender.inventory.offhand_weapon.name.lower())

    if parry.parrying_bonus <= 0:
        print("His parrying bonus is:", parry.parrying_bonus)
        print(parry.defender.name, "has no weapon to parry with. Parry failed!")
    else:
        print("His parrying bonus is:", parry.parrying_bonus)
        print(parry.defender.name, "rolls", "*" + str(parry.roll) + "*", "for parry")
        result_text = str(parry.parrying_bonus) + " + " + str(parry.roll) + " - " + str(parry.hit_result)

        if parry.result:
            print(result_text, "> 0, parry succeeded!")
        else:
            print(result_text, "< 0, parry failed!")


def report_damage(dmg_dealt):
    print("*** DAMAGE ***")
    print(dmg_dealt.attacker.name, "rolls", "*" + str(dmg_dealt.roll) + "*", "for base weapon damage")
    print("Augmenting Factor of", dmg_dealt.attacker.name + "'s attack is:", dmg_dealt.augmenting)
    print("Damage Reduction of", dmg_dealt.defender.name + "'s", dmg_dealt.defender.inventory.armor.name.lower(), "is:", dmg_dealt.reduction)
    result_text = str(math.floor(dmg_dealt.roll * dmg_dealt.augmenting)) + " - " + str(dmg_dealt.reduction)
    if dmg_dealt.result <= 0:
        print(result_text, "<= 0, no damage dealt")
    else:
        print(result_text, "> 0,", dmg_dealt.attacker.name, "deals", "*" + str(dmg_dealt.result) + "*", "of damage")


def close_battle(attacker, defender, rounds_count):
    if attacker.health <= 0:
        winner = defender
        loser = attacker
    else:
        winner = attacker
        loser = defender

    print("***************************")
    print(winner.name + "'s health is: ", winner.health)
    print(loser.name + "'s health is: ", loser.health)
    print(winner.name, "wins after", rounds_count, "rounds of relentless battle.")
    print()
    print("************************************************************************************")
    print("*************************************** END ****************************************")
    print("************************************************************************************")
    print()


def report(warrior):
    print()
    print("Hail, my good fellow. I am {}. My health is {}. My offense/defense rating is {}/{}. I'm affected by following effects: {}. I'm equipped with: \n{}".format(warrior.name, warrior.health, warrior.offense, warrior.defense, [effect.name for effect in warrior.effects], str(warrior.inventory)))
