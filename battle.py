# Automate battles in Risk.

import argparse

# ----------BEGIN ARGUMENTS----------

parser = argparse.ArgumentParser(description="Automate battles in Risk.")

# first argument is size of attacking force
parser.add_argument("numAttacking", type=int, 
                    help="The total number of troops in the attacking territory.")

# second argument is size of defending force
parser.add_argument("numDefending", type=int,
                    help="The total number of troops in the attacking territory.")

args = parser.parse_args()

# -----------END ARGUMENTS-----------
