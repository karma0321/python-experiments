import random

def play_guess_the_number(guess, secret):
    message = ''
    guess = int(guess)
    success = False
    while True:
        last_guess_message = "Last guess: {}".format(guess)
        if guess == secret:
            message = "Yeah!! You guessed it!\nThe right number is {0}".format(secret)
            success = True
            return success, message
        elif guess < secret:
            message = "Wrong guess... try something bigger.\n{}".format(last_guess_message)
            return success, message
        else:
            message = "Wrong guess... try something smaller.\n{}".format(last_guess_message)
            return success, message


if __name__ == '__main__':
    play_guess_the_number()