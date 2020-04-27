import os
import random
import string
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)

# configuring the connection to postgresql database
app.config['DATABASE_URL'] = 'postgres://hzimzwnodcjnlg:b7d3f5287994c904922a28b91a35f48b9ca966791bc454398bc6412fb214d620@ec2-52-6-143-153.compute-1.amazonaws.com:5432/d3kb2tqikr63h8'
db = SQLAlchemy(app)
# generating secret key - will be used later
# SECRET_KEY = os.urandom(32)
# app.config['SECRET_KEY'] = SECRET_KEY

# creating the table schema in database 'password_gen
class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(30), unique=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, password, date):
        self.password = password
        self.date = date


@app.route("/", methods=['POST', 'GET'])
def letters_post():
    """Generation of the passwords and display of the password to the user
    after input has been accepted and passed through the function"""

    password = []
    appendList = []

    # allowing html input
    if request.method == 'POST':
        letters = request.form.get('letters', type=int)
        numbers = request.form.get('numbers', type=int)
        characters = request.form.get('characters', type=int)

    # prompting the random generation functions
        possible_letters = string.ascii_letters
        possible_numbers = string.digits
        possible_chars = string.punctuation

    # returning the values of the generation
        password.append(random.choices(possible_letters, k=(letters)))
        password.append(random.choices(possible_numbers, k=(numbers)))
        password.append(random.choices(possible_chars, k=(characters)))

    # sorting through values in password list to convert to a string for
        # legibility
        for i in password:
            appendList.append((''.join(i)))

        password = (''.join(appendList))

    # adding generated passwords to the local database
        passwords = Passwords(password=password, date=datetime.datetime.now()
                              .strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(passwords)
        db.session.commit()

    db_query_all = Passwords.query.all()

    return render_template('base.html', password=password,
                            db_query_all=db_query_all)


@app.route("/delete_pass/<string:id>", methods=['POST'])
def delete_pass(id):
    """Deletion of passwords that are available in the database"""
    passwords = Passwords.query.filter_by(id=id).one()
    db.session.delete(passwords)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
