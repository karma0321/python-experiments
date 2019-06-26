# We receive two parameters guess and number
def play_guess_the_number(guess, attempts, secret):
    message = ''
    # Convert guess to an integer to be able to compare it with secret
    if guess:
        guess = int(guess)
    else:
        guess = 0
    # set a boolean flag to inform if the game is over. It will change to true if our player guesses the number
    success = False

    # Initialize the attempts variable
    if attempts:
        attempts = int(attempts)
    else:
        attempts = 0

    last_guess_message = "Last guess: {}".format(guess)
    if guess == secret:
        message = "Yeah!! You guessed it!\nThe right number is {0}".format(secret)
        success = True

    elif guess < secret:
        message = "Wrong guess... try something bigger.\n{}".format(last_guess_message)
        # increase attempts by one while the player doesn't guess the secret number
        attempts += 1

    else:
        message = "Wrong guess... try something smaller.\n{}".format(last_guess_message)
        attempts += 1

    # The function returns three values (separated with comma).
    return success, attempts, message


if __name__ == '__main__':
    play_guess_the_number()
