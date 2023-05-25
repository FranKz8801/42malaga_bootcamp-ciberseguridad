import random

# Constants
SECRET_NUMBER = random.randint(1, 99)  # Generate a random secret number
TRIES_LIMIT = 10  # Maximum number of attempts allowed

# Game initialization
print("This is an interactive guessing game!")
print("You have to enter a number between 1 and 99 to find out the secret number.")
print("Type 'exit' to end the game.")
print("Good luck!")

# Game loop
tries = 0
while True:
    guess = input("What's your guess between 1 and 99? >> ")
    if guess.lower() == 'exit':
        print("Goodbye!")
        break
    elif not guess.isdigit():
        print("That's not a number.")
        continue
    else:
        guess = int(guess)
        if guess < 1 or guess > 99:
            print("The number must be between 1 and 99.")
            continue
        tries += 1
        if guess == SECRET_NUMBER:
            if SECRET_NUMBER == 42:
                print("The answer to the ultimate question of life, the universe and everything is 42.")
            print("Congratulations, you've got it!")
            print("You won in {} attempt(s)!".format(tries))
            break
        elif guess < SECRET_NUMBER:
            print("Too low!")
        else:
            print("Too high!")
        if tries == TRIES_LIMIT:
            print("You've reached the maximum number of attempts.")
            print("The secret number was {}.".format(SECRET_NUMBER))
            break
