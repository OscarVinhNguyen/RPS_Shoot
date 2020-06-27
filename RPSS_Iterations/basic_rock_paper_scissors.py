"""
ROCK, PAPER, SCISSORS (simple)
Made by Oscar-Vinh Nguyen
07/20/2020
"""



import getpass

#title screen
print("\n * ROCK *")
print("    || PAPER ||")
print("       8< SCISSORS 8<\n")

#P1 input
P1 = getpass.getpass(prompt="Input move for Player 1 (1=rock, 2=paper, 3=scissors):\n")
P1 = int(P1)

#P2 input
P2 = getpass.getpass(prompt="Input move for Player 2 (1=rock, 2=paper, 3=scissors):\n")
P2 = int(P2)

#calculating results
results = P1 - (P2 + 10)

#print choices
print("P1: " + str(P1) + " vs P2: " + str(P2))

#displaying results
if results == -10:
	print("\n---Tie!---\n")
elif results == -12 or results == -9:
	print("\n---Player 1 Wins!---\n")
elif results == -8 or results == -11:
	print("\n---Player 2 Wins!---\n")
else:
	print("\n---error---\n")