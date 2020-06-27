"""
ROCK, PAPER, SCISSORS
Made by Oscar-Vinh Nguyen
07/18/2020

----------

MAIN LOGIC:

1st Player:Rock = 1, Paper = 2, Scissors = 3

2nd Player: Rock = 11, Paper = 12, Scissors = 13

Results = P1 - P2

P1 Wins:
	1-13=-12
	2-11=-9
	3-12=-9
P2 Wins:
	3-11=-8
	1-12=-11
	2-13=-11
Tie = -10
"""



from os import system, name 
from time import sleep 



# define clear function 
def clear(): 
	_ = system('clear') 



# now call function we defined above 
clear()

#title screen
print("\n * ROCK *")
sleep(1)
print("    || PAPER ||")
sleep(1)
print("       8< SCISSORS 8<")

trans_int = 1
sleep(trans_int)

"""
#select mode
mode = input("\n\n\nSELECT MODE\n\n'two players' or 'vs ai': " )
print("\nYou have selected " + mode + " mode")
sleep(trans_int)
"""
clear()

#P1 input
P1 = input("Input move for Player 1\n(1=rock, 2=paper, 3=scissors):\n")
P1 = int(P1)
clear()
sleep(trans_int)

#P2 input
P2 = input("Input move for Player 2\n(1=rock, 2=paper, 3=scissors):\n")
P2 = int(P2)
P2 +=10
clear()
sleep(trans_int)

#suspense function
def suspense():
	sus_int = 0.2
	print("Counting...")
	sleep(sus_int)
	print("...")
	sleep(sus_int)
	print("...")
	sleep(sus_int)
	print("Calculating...")
	sleep(sus_int)
	print("...")
	sleep(sus_int)
	print("...")
	sleep(sus_int)
	print("Calibrating...")
	sleep(sus_int)
	print("...")
	sleep(sus_int)
	print("...")
	sleep(sus_int)

suspense()
sleep(trans_int)
clear()

#calculating results
results = P1 - P2

#redraw title screen
print("\n * ROCK *")
print("    || PAPER ||")
print("       8< SCISSORS 8<")

sleep(trans_int)

#displaying results
if results == -10:
	print("\n---Tie!---\n")
elif results == -12 or results == -9:
	print("\n---Player 1 Wins!---\n")
elif results == -8 or results == -11:
	print("\n---Player 2 Wins!---\n")
else:
	print("\n---error---\n")
