import datetime
import random
import string
import pandas as pd
import httpx
import csv
import requests

from faker import Faker

from http import HTTPStatus

from flask import Flask, request, Response

from webargs import fields, validate

from webargs.flaskparser import use_kwargs


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!!!!</p>"


@app.route("/mykhailo")
def hello_mykhailo():
    return "<p>Hello, Mykhailo!!!!</p>"


@app.route("/now")
def get_time():
    return f"current time: {datetime.datetime.now()}"


@app.route("/password")
@use_kwargs(
    {
        'length': fields.Int(
            missing=10,
            validate=[validate.Range(min=8, max=100)]
                             )
    },
    location='query'
)
def generate_password(length):

    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation

    conditions = letters + digits + special_chars
    password = ''

    return password.join(random.choices(
        conditions, k=length)
                         )


@app.route("/parameters")
def get_average_parameters():

    df = pd.read_csv(r'/Users/letsgooo/Desktop/hw.csv')

    mean1 = df[' Height(Inches)'].mean()
    mean2 = df[' Weight(Pounds)'].mean()

    return f'Average height: {mean1}' + '\t' + f'Average weight: {mean2}'


@app.route("/students")
def generate_students():

    students_count = request.args.get('count', default=100)

    if not students_count.isdigit():
        return 'ERROR: should be a number'

    students_count = int(students_count)

    if not 1 <= students_count <= 1000:
        return 'ERROR: should be in range[1, 1000]'

    faker_instance = Faker("UK")
    student_header = ['first_name', 'last_name', 'email', 'password', 'birthday']

    with open('students.csv', 'w') as file:

        writer = csv.writer(file)
        writer.writerow(student_header)
        for _ in range(students_count):
            student_data = [
                {
                    faker_instance.first_name(): 'first_name',
                    faker_instance.last_name(): 'last_name',
                    faker_instance.email(): 'email',
                    faker_instance.password(): 'password',
                    faker_instance.date(): 'birthday'
                }
            ]
            writer.writerows(student_data)

    students = pd.read_csv('students.csv')

    students.to_html("Table.htm")
    html_file = students.to_html()

    return html_file


@app.route('/bitcoin-rate')
@use_kwargs(
    {
        'currency': fields.Str(
            missing='USD'
                             ),
        'count': fields.Int(
            missing=1,
            validate=[validate.Range(min=1, max=100)]
        )
    },
    location='query'
)
def get_bitcoin_value(currency, count):
    url = 'https://bitpay.com/api/rates'
    result = httpx.get(url)

    if result.status_code not in (HTTPStatus.OK,):
        return Response('ERROR: Something went wrong', status=result.status_code)

    result = result.json()

    first_dict = {}
    second_dict = {}
    third_dict = {}

    symbol_url = 'https://bitpay.com/currencies'
    symbol_result = httpx.get(symbol_url)

    if symbol_result.status_code not in (HTTPStatus.OK,):
        return Response('ERROR: Something went wrong', status=symbol_result.status_code)

    symbol_result = symbol_result.json()
    symbol = {}
    done = {}

    for entry in result:

        new = {'currency': currency}
        first_dict.update(new)
        first_dict['code'] = first_dict.get('', currency)

        second_dict[entry['code']] = second_dict.get('', entry['code'])

        if first_dict['code'] == second_dict[entry['code']]:

            third_dict['code'] = first_dict['code']
            third_dict['rate'] = third_dict.get('', entry['rate'])
            third_dict['rate'] = third_dict['rate'] * count
            #symbol.update(third_dict)

            #for entry in symbol_result.get('data', {}):

                #symbol[entry['code']] = symbol.get('', entry['symbol'])

                #if third_dict['code'] == symbol['code']:

                    #symbol[entry['code']] = symbol.get('', entry['symbol'])

                    #done['code'] = third_dict['code']
                    #done['decimals'] = third_dict['rate']
                    #done['code'] = symbol.get('', entry['symbol'])
                    #symbol['code'] = symbol.get('', entry['symbol'])

                    #if done['code'] == symbol['code']:

                        #symbol['code'] = currency

                        #print(symbol, done)

    return third_dict


@app.route('/astronauts')
def get_astronauts():
    url = 'http://api.open-notify.org/astros.json'

    result = httpx.get(url)

    if result.status_code not in (HTTPStatus.OK, ):
        return Response('ERROR: Something went wrong', status=result.status_code)

    result = result.json()

    statistics = {}

    for entry in result.get('people', {}):
        statistics[entry['craft']] = statistics.get(entry['craft'], 0) + 1

    return statistics

app.run(port=5001, debug=True)
