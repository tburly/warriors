"""
Functions bundled in this module make various announcements about the current game's state to standard output
"""


def introduce_battle(attacker, defender):
    print()
    print("******** BATTLE ********")
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

    print(str(initiative.attacker.offense) + " + " + str(initiative.attacker_roll), sign, str(initiative.defender.offense) + " + " + str(initiative.defender_roll) + ".", ending)


def introduce_round(attacker, defender, rounds_count):
    print()
    print("******** ROUND #" + str(rounds_count), "********")
    print("Attacker is:", str(attacker))
    print("Defender is:", str(defender))


def close_battle(attacker, defender, rounds_count):
    if attacker.health <= 0:
        winner = defender
        loser = attacker
    else:
        winner = attacker
        loser = defender

    print("************************")
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
