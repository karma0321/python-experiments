# We receive two parameters guess and number
def play_guess_the_number(guess, secret):
    message = ''
    # Convert guess to an integer to be able to compare it with secret
    guess = int(guess)
    # set a boolean flag to inform if the game is over. It will change to true if our player guesses the number
    success = False
    last_guess_message = "Last guess: {}".format(guess)
    if guess == secret:
        message = "Yeah!! You guessed it!\nThe right number is {0}".format(secret)
        success = True

        # In this case the function returns two values (separated with comma).
        return success, message
    elif guess < secret:
        message = "Wrong guess... try something bigger.\n{}".format(last_guess_message)

        # the function returns two values (separated with comma).
        return success, message
    else:
        message = "Wrong guess... try something smaller.\n{}".format(last_guess_message)

        # the function returns two values (separated with comma).
        return success, message

if __name__ == '__main__':
    play_guess_the_number()
