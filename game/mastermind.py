#Import the other two python files and all of their functions
from .input import *
from .giveHint import *
#The following three lines are for the user’s input
numCol = getNumberOfColours()
codeLength = getLengthOfCode()
duplicates = isDuplicacy()
#Depending on the user's input list S of all possible codes will be created
#createS() in in the giveHint.py
S = createS(codeLength, numCol)
print(f"S is created and the length is {len(S)}")
#The createCode function from the input.py will create the Mastercode
code = createCode(numCol,codeLength,duplicates)
#Ask for user's guess
print (f"Make a guess")
#getGuess() from input.py gets the guess as a list of numbers
guess = getGuess(codeLength)
print(f"Guess is {guess}")
#guesslist will keep a record of the user’s guesses. It will be a list of lists. 
guessList = [guess]
#attempts is the number of tries
attempts=1
# The check_guess() from the input.py will return number of blacks and number of whites
blacks, whites = check_guess(guess,code)
print(f"blacks are {blacks}")
print(f"whites are {whites}")
#Keep looping until the guess is the code (blacks == codeLength)
while(blacks<codeLength):
    # A hint option will be available. If chosen, it will return the next best guess
    hint = input("Do you want a hint? (Y/N)")
    if hint in ("Y","y", "Yes", "yes"):
        print(f"Get help from computer - last guess was {guess}")
        #removeS() from giveHint.py will remove all codes with different score
        S = removeS(S,code,guess)
        #Now S is reduced and contains the Mastercode
        print (f"S after guess {guess} is {S} and the length is {len(S)}")
        # If S has only one element, this will be the next guess, else the Minimax algorithm will be executed from giveHint.py
        if (len(S)==1):
            guess=S[0]
        else:
            guess = giveHint(S, guess, code, numCol, codeLength, duplicates)
    else:
        # The user choose to give his own guess
        print("Give your new guess")
        guess = getGuess(codeLength)
    # Insert next guess to the guessList
    guessList.append(guess)
    attempts = attempts + 1
    blacks, whites = check_guess(guess,code)
    print(f"Now guess is {guess} with blacks: {blacks} and whites: {whites}. The code is {code}")
# When exit the loop (guess==code) the program will output the score
print(f"You broke the code in {attempts} attempts")
print(f"Guesses were {guessList}")