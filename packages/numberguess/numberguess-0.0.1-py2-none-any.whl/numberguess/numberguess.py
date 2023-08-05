def numberguess():

    import numpy as np

    print("This is a number guessing game. my number is between 1 and 10")

    play=0
    while play==0:
        rightguess=np.random.choice(range(1,11))
        stop=0

    

        while stop==0:
            guess= int(input("Please input your guess. >"))
    
            if guess == rightguess:
                print ("you've guessed it!")
                stop=1
            else:
                print("nope, keep guessing!")
        
        print ("would you like to play again?")
        ans=input("enter y or n. >")
        if ans==("n"):
            print("thanks for playing")
            play=1
        else:
            pass
        
    

numberguess()

