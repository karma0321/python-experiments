from models import User, db


def create_user(name, email):
    user = User(name=name, email=email)

    # save the user object into a database
    db.add(user)
    db.commit()

if __name__ == '__main__':
    create_user()