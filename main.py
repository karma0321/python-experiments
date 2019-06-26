from flask import Flask, render_template, request, make_response, redirect, url_for
import datetime
from libs.guess_the_number import play_guess_the_number
import random
import uuid
import hashlib
# import the database related tools, as well as the User class, from models
from models import User, db

app = Flask(__name__)
db.create_all()


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
@app.route("/guess-the-number")
def guess_the_number(title="Guess the number!!"):

    # Check if the page is visited through a get request
    if request.method == "GET":
        return render_template('guess-the-number-intro.html')


@app.route("/guess-the-number/register", methods=["POST"])
def guess_the_number_register():

    name = request.form.get("new-player-name")
    email = request.form.get("new-player-email")
    password = request.form.get("new-player-password")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # create a secret number
    secret_number = random.randint(1, 50)

    # see if user already exists
    user = db.query(User).filter_by(email=email).first()

    if not user:
        # create a User object
        user = User(name=name, email=email, secret_number=secret_number, password=hashed_password)

        # create a random session token for this user
        session_token = str(uuid.uuid4())

        # save the session token in a database
        user.session_token = session_token
        db.add(user)
        db.commit()

        # save user's session token into a cookie
        response = make_response(redirect(url_for('guess_the_number_play')))
        response.set_cookie("session-token", session_token, httponly=True, samesite='Strict')

        return response

    else:
        message = "Error creating user, email already exists. Try to login instead."
        return render_template('guess-the-number-intro.html', user=user, message=message)




@app.route("/guess-the-number/login", methods=["POST"])
def guess_the_number_login():

    email = request.form.get("login-email")
    password = request.form.get("login-password")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # see if user already exists
    user = db.query(User).filter_by(email=email).first()

    if user:
        # check if password is incorrect
        if hashed_password != user.password:
            message = "WRONG PASSWORD! Go back and try again."
            return render_template('guess-the-number-intro.html', message=message)

        elif hashed_password == user.password:
            # create a random session token for this user
            session_token = str(uuid.uuid4())

            # save the session token in a database
            user.session_token = session_token
            db.add(user)
            db.commit()

            # save user's session token into a cookie
            response = make_response(render_template('guess-the-number.html', user=user))
            response.set_cookie("session-token", session_token, httponly=True, samesite='Strict')

            return response

    else:
        message = "We couldn't find any user with your email... try registering a new user."
        return render_template('guess-the-number-intro.html', user=user, message=message)



@app.route("/guess-the-number/play", methods=["GET", "POST"])
def guess_the_number_play(title="Guess the number!!"):
    if request.method == "GET":

        # check if user has already set his name
        session_token = request.cookies.get("session-token")

        if not session_token:
            message = 'You have to be logged in to play!'
            return render_template('guess-the-number-intro.html', message=message)

        else:
            # get user from the database based on her/his email address
            user = db.query(User).filter_by(session_token=session_token).first()

            # As we begin our game, be sure to reset previous secret numbers
            user.secret_number = random.randint(1, 50)
            db.add(user)
            db.commit()
            message = 'Secret number has been regenerated! Guess it!'
        response = make_response(render_template('guess-the-number.html', user=user, title=title, message=message))
        response.set_cookie("attempts", expires=0)

        return response

    elif request.method == "POST":

        session_token = request.cookies.get("session-token")

        if not session_token:
            message = 'You have to be logged in to play!'
            return render_template('guess-the-number-intro.html', message=message)

        else:
            # get user from the database based on her/his email address
            user = db.query(User).filter_by(session_token=session_token).first()

            # If there is already secret value that is not 0
            # - get the value from the db
            # - convert it to an integer
            # - store it in a variable - secret
            if user.secret_number != 0:
                secret_number = user.secret_number

            # If there is secret value in the db:
            # - generate a random number (between 1 and 50 in this case)
            # - store it in a variable - secret
            else:
                secret_number = random.randint(1, 50)

            # Get the player's guess from the form
            guess = request.form.get("guess")

            # Initialize the variable attempts
            if request.cookies.get("attempts"):
                attempts = int(request.cookies.get("attempts"))
            else:
                attempts = 1

            # Call the external function play_the_guess_number that we imported before
            # with the two parameters guess and secret to activate the game logic
            # (Check the play_guess_the_number.py file now)
            success, attempts, message = play_guess_the_number(guess, attempts, secret_number)

            # Assign the two values we receive from the function (success and message) to two variables
            # and pass all these values to the render_template. Then, create the response.
            response = make_response(render_template("guess-the-number.html",  guess=guess, message=message, user=user, title=title, attempts=attempts))

            # If success value has changed to True
            # we render the template for the success case (guess-the-number-success.html)
            # and pass the needed values to the template
            if success:
                response = make_response(
                    render_template("guess-the-number-success.html", guess=guess, message=message, user=user, title=title, attempts=attempts))

                # Here we reset the secret to be ready for another game
                user.secret_number = 0
                best_score = get_best_score(attempts, user.best_score)
                user.best_score = best_score
                response.set_cookie("attempts", expires=0)
            # If success value is not True, set the secret cookie with the value of the current secret number
            else:
                user.secret_number = secret_number
                response.set_cookie("attempts", str(attempts))

            db.add(user)
            db.commit()
            return response

# Here we set a path where we can delete the player_name cookie and restart the game
@app.route("/guess-the-number/logout")
def guess_the_number_logout():
    response = make_response(render_template("guess-the-number-intro.html"))
    response.set_cookie("session-token", expires=0)
    response.set_cookie("attempts", expires=0)

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

def get_best_score(attempts, best_score):
    if best_score == 0 or attempts < best_score:
        return attempts
    return best_score

if __name__ == '__main__':
    app.run()