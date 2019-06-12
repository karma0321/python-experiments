from flask import Flask, render_template, request, make_response, redirect
import datetime
# Import play_guess_the_number from external file in directory libs
# To add a different directory as source for external functions you need to add an
# empty file called __init__.py to tell Python to add that code to the libraries
from libs.guess_the_number import play_guess_the_number
import random

app = Flask(__name__)


@app.route("/")
def index():
    some_text = "This is a dummy test text"
    current_year = datetime.datetime.now().year
    cities = ["Boston", "Vienna", "Paris", "Berlin"]

    return render_template('index.html', some_text=some_text, current_year=current_year, cities=cities )


@app.route("/hello")
def hello():
    return render_template("hello.html")

# This is the route for the first stage of the game.
# Here we set the player name and store it in a cookie.
# If the cookie already exists, we welcome the user and show a button to start the game.
@app.route("/guess-the-number", methods=["GET", "POST"])
def guess_the_number(title="Guess the number!!"):

    # Check if the page is visited through a get request
    if request.method == "GET":

        # Check if there is a cookie with ID "player_name"
        if request.cookies.get("player_name"):
            player_name = request.cookies.get("player_name")

        # If there is no cookie with ID "player_name"
        # we call the template without the player_name value
        # the template (guess-the-number-intro.html) will show an input field
        # to let the user type a name.
        else:
            return render_template('guess-the-number-intro.html', title=title)

        # If we find the cookie we pass the player_name value to the template
        # to welcome the player
        return render_template('guess-the-number-intro.html', player_name=player_name, title=title)

    # If the page is visited through a post request, it means the user has entered a name and
    # sent the name form so we go on with the value we just received.
    elif request.method == "POST":

        # If we get a value from the player-name field:
        # - pass that value to the template (render_template())
        # - create a response to be able to set a cookie with the player_name value
        # - return the response
        if request.form.get("player-name"):
            player_name = request.form.get("player-name")

            response = make_response(render_template("guess-the-number.html", player_name=player_name, title=title))
            response.set_cookie("player_name", player_name)
            return response

        # Maybe redundant, but if we don't receive the player_name value from the form, reload the page
        else:
            return render_template('guess-the-number-intro.html', title=title)


@app.route("/guess-the-number/play", methods=["GET", "POST"])
def guess_the_number_play(title="Guess the number!!"):
    if request.method == "GET":

        # check if user has already set his name
        if request.cookies.get("player_name"):
            player_name = request.cookies.get("player_name")
        else:

            # Be sure to have a player name, else redirect to the Enter name page
            return redirect("/guess-the-number")

        response = make_response(render_template('guess-the-number.html', player_name=player_name, title=title))

        # As we begin our game, be sure to remove any existing cookie with previous secret numbers
        response.set_cookie("secret", expires=0)
        return response

    elif request.method == "POST":

        # Here is where we receive the first guess value

        if request.cookies.get("player_name"):
            player_name = request.cookies.get("player_name")
        else:

            # Be sure to have a player name, else redirect to the Enter name page
            return redirect("/guess-the-number")

        # If there is already a cookie with our secret number
        # - get the value from the cookie
        # - convert it to an integer
        # - store it in a variable - secret
        if request.cookies.get("secret"):
            secret = int(request.cookies.get("secret"))

        # If there is no cookie called secret:
        # - generate a random number (between 1 and 50 in this case)
        # - store it in a variable - secret
        else:
            secret = random.randint(1, 50)

        # Get the player's guess from the form
        guess = request.form.get("guess")

        # Call the external function play_the_guess_number that we imported before
        # with the two parameters guess and secret to activate the game logic
        # (Check the play_guess_the_number.py file now)
        success, message = play_guess_the_number(guess, secret)

        # Assign the two values we receive from the function (success and message) to two variables
        # and pass all these values to the render_template. Then, create the response.
        response = make_response(render_template("guess-the-number.html",  guess=guess, secret=secret, message=message, player_name=player_name, title=title))

        # If success value has changed to True
        # we render the template for the success case (guess-the-number-success.html)
        # and pass the needed values to the template
        if success:
            response = make_response(
                render_template("guess-the-number-success.html", guess=guess, secret=secret, message=message, player_name=player_name, title=title))

            # Here we reset the cookie to be ready for another game
            response.set_cookie("secret", expires=0)
        # If success value is not True, set the secret cookie with the value of the current secret number
        else:
            response.set_cookie("secret", str(secret))

        return response

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        user_name = request.cookies.get("user_name")

        return render_template("contact.html", user_name=user_name)
    elif request.method == "POST":
        contact_name = request.form.get("contact-name")
        contact_email = request.form.get("contact-email")
        contact_message = request.form.get("contact-message")

        print(contact_name)
        print(contact_email)
        print(contact_message)

        response = make_response(render_template("contact.html", user_name=contact_name, user_email=contact_email))
        response.set_cookie("user_name", contact_name)
        response.set_cookie("user_email", contact_email)

        return response



if __name__ == '__main__':
    app.run()