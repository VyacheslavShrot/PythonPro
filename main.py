import datetime
import random
import string
import secrets
import pandas as pd

from flask import Flask







app = Flask(__name__)


@app.route("/")
def hello_world():
    # view
    return "<p>Hello, World!!!!</p>"


@app.route("/mykhailo")
def hello_mykhailo():
    return "<p>Hello, Mykhailo!!!!</p>"


@app.route("/now")
def get_time():
    return f"current time: {datetime.datetime.now()}"

@app.route("/password")
def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    conditions = letters + digits + special_chars
    password_length = random.randint(10, 20)
    password = ''

    for i in range(password_length):
        password += ''.join(secrets.choice(conditions))

    return password


@app.route("/parameters")
def get_average_parameters():

    df = pd.read_csv(r'/Users/letsgooo/Desktop/hw.csv')
    print(df)
    print(df.columns.tolist())

    mean1 = df[' Height(Inches)'].mean()
    mean2 = df[' Weight(Pounds)'].mean()


    return f'Average height: {mean1}' + '\t' + f'Average weight: {mean2}'



app.run(port=5001, debug=True)



