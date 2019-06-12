from flask import Flask, render_template, request, make_response, redirect
import datetime
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

@app.route("/guess-the-number", methods=["GET", "POST"])
def guess_the_number():
    if request.method == "GET":
        if request.cookies.get("player_name"):
            player_name = request.cookies.get("player_name")
        else:
            return render_template('guess-the-number-intro.html')

        return render_template('guess-the-number-intro.html', player_name=player_name)

    elif request.method == "POST":
        if request.form.get("player-name"):
            player_name = request.form.get("player-name")

            response = make_response(render_template("guess-the-number.html", player_name=player_name))
            response.set_cookie("player_name", player_name)
            return response
        else:
            return render_template('guess-the-number-intro.html')


@app.route("/guess-the-number/play", methods=["GET", "POST"])
def guess_the_number_play(title="Guess the number!!"):
    if request.method == "GET":
        # check if user has already set his name
        if request.cookies.get("player_name"):
            player_name = request.cookies.get("player_name")
        else:
            # Be sure to have a player name, else redirect to the Enter name view
            return redirect("/guess-the-number")
        response = make_response(render_template('guess-the-number.html', player_name=player_name, title=title))
        response.set_cookie("secret", expires=0)
        return response

    elif request.method == "POST":
        if request.cookies.get("player_name"):
            player_name = request.cookies.get("player_name")
        else:
            return redirect("/guess-the-number")

        if request.cookies.get("secret"):
            secret = int(request.cookies.get("secret"))
        else:
            secret = random.randint(1, 50)

        guess = request.form.get("guess")
        success, message = play_guess_the_number(guess, secret)

        response = make_response(render_template("guess-the-number.html",  guess=guess, secret=secret, message=message, player_name=player_name, title=title))

        if success:
            response = make_response(
                render_template("guess-the-number-success.html", guess=guess, secret=secret, message=message, player_name=player_name, title=title))
            response.set_cookie("secret", expires=0)
        else:
            response.set_cookie("secret", str(secret))
        response.set_cookie("player_name", player_name)
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