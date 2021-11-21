# Automate battles in Risk.

# 1. Display number attacking and defending, and prompt for number to attack.
#    a. Remember the number entered.
#    b. If remembered number is greater than troops that can attack, erase memory.
# 2. Roll a die for each attacking troop, and store results in an ordered list.
# 3. Roll a die for each defending troop, and store results in an ordered list.
# 4. Compare the greatest values of each list.
#    a. If the attacking value is greater than the defending value, the defender
#       loses a troop. 
#    b. If the defending value is greater than the attacking value, the attacker
#       loses a troop. 
#    c. If the values are equal, the attacker loses a troop.
# 5. Store the result of the comparison in the appropriate loss-tracking
#    variable (one for attacker and one for defender).
# 6. Remove the greatest values from each list.
# 7. Repeat Steps 4-6 until one of the lists is empty.
# 8. Make the appropriate troop subtractions, and display the results.
# 9. Repeat Steps 1-8 until there are no defending troops remaining or the
#    attack is canceled.

import argparse
import itertools
import functools
import random

# ----------BEGIN ARGUMENTS----------

parser = argparse.ArgumentParser(description="Automate battles in Risk.")

# first argument is size of attacking force
parser.add_argument("attacking", type=int, 
                    help="The total number of troops in the attacking territory.")

# second argument is size of defending force
parser.add_argument("defending", type=int,
                    help="The total number of troops in the attacking territory.")

args = parser.parse_args()

# -----------END ARGUMENTS-----------

# ----------BEGIN FIGHT FUNCTIONS----------

# simulate the roll of several dice; return list of random integers 1-6
def rollD6s(numRolls):
    if numRolls:
        return list(itertools.chain(*[[random.randint(1,6)], 
                                      rollD6s(numRolls - 1)]))
    else: 
        return [] 

# perform the dice rolls; return tuple of sorted lists: (attRolls, defRolls)
def getRolls(numAtt, numDef):
    return (sorted(rollD6s(numAtt)), sorted(rollD6s(numDef)))

# return the loss at the end of a fight
def getFightLoss(rollAtt, rollDef):
    return (0,-1) if rollDef < rollAtt else (-1,0)

# return list of tuples of losses of each side for each fight
def getFightLosses(rollsAtt, rollsDef):
    if rollsAtt and rollsDef:
        return list(itertools.chain(*[
            [getFightLoss(rollsAtt[-1], rollsDef[-1])],
            getFightLosses(rollsAtt[0:-1], rollsDef[0:-1])])) 
    else:
        return []
    
# perform a battle; return total losses as tuple: (attLosses, defLosses)
def getBattleLosses(numAtt, numDef):
    rolls = getRolls(numAtt, numDef)
    return tuple([sum(fight) for fight in zip(*getFightLosses(rolls[0], rolls[1]))])

# -----------END FIGHT FUNCTIONS-----------

# ----------BEGIN BATTLE FUNCTIONS----------

# if attacking troops entry is invalid, try again
def retryGetNumAtt(enteredNumAtt, numAtt, totAtt):
    print("ERR: attacking troop number \"{}\" invalid".format(enteredNumAtt))
    return getNumAtt(numAtt, totAtt)

# return the number of troops to be used in the current fight and validate the
# entry 
def getNumAtt(numAtt, totAtt):
   
    # ask the user to enter how many troops are to attack
    enteredNumAtt = input("Enter number of attacking troops. [{}]> ".
                          format(numAtt))

    # if entry blank, just use the remembered troop number
    if not enteredNumAtt:
        return numAtt

    # verify the entered value is a number
    enteredNumAtt = int(enteredNumAtt) if enteredNumAtt.isdigit() else \
    retryGetNumAtt(enteredNumAtt, numAtt, totAtt)
    
    # validate entry; if invalid, ask again
    if enteredNumAtt > 0 and \
       enteredNumAtt < 4 and \
       enteredNumAtt < totAtt:
        return enteredNumAtt
    else:
        return retryGetNumAtt(enteredNumAtt, numAtt, totAtt)

# -----------END BATTLE FUNCTIONS-----------

# number of troops on each side (att, def)
troops = (args.attacking, args.defending)

# initialize number of attacking troops
numAtt = 1

# display the initial number of attacking and defending troops
print("A: {}, D: {}".format(str(troops[0]), str(troops[1]))) 

# continue the attack until either attacker or defender runs out of troops
while troops[0] > 1 and troops[1] > 0:
    
    # get number attacking troops
    numAtt = getNumAtt(numAtt, troops[0])

    # get the losses of the battle
    battleLosses = getBattleLosses(numAtt, 2 if args.defending > 1 else 1)

    # subtract losses from total troop numbers
    troops = tuple([sum(ele) for ele in zip(troops, battleLosses)])
    
    # display the new number of attacking and defending troops
    print("A: {}, D: {}".format(troops[0], troops[1] if troops[1] > -1 else 0))
