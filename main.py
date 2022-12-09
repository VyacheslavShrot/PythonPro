import datetime
import random
import string
import pandas as pd
import httpx
import csv



from helpers import format_records

from database_handler import execute_qeury

from faker import Faker

from http import HTTPStatus

from flask import Flask, Response

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
@use_kwargs(
    {
        'count': fields.Int(
            missing=100,
            validate=[validate.Range(min=1, max=1000)]
        )
    },
    location='query'
)
def generate_students(count):

    faker_instance = Faker("UK")
    student_header = ['first_name', 'last_name', 'email', 'password', 'birthday']

    with open('students.csv', 'w') as file:

        writer = csv.writer(file)
        writer.writerow(student_header)
        for _ in range(count):
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

    return students.to_html()


@app.route('/bitcoin-rate')
@use_kwargs(
    {
        'currency': fields.Str(
            load_default='USD'
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

    new = {'currency': currency}
    first_dict.update(new)

    for entry in result:

        first_dict['code'] = first_dict.get('', currency)
        second_dict[entry['code']] = second_dict.get('', entry['code'])

        if first_dict['code'] == second_dict[entry['code']]:

            third_dict['code'] = first_dict['code']
            third_dict['rate'] = third_dict.get('', entry['rate'])
            third_dict['rate'] = third_dict['rate'] * count


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


@app.route("/customers")
@use_kwargs(
    {
        "first_name": fields.Str(
            required=False,
            load_default=None,
            validate=[validate.Regexp("^[0-9]*")]
        ),
        "last_name": fields.Str(
            required=False,
            load_default=None,
            validate=[validate.Regexp("^[0-9]*")]
        )
    },
    location="query"
)
def get_all_customers(first_name, last_name):
    query = "SELECT * FROM customers"

    fields = {}

    if first_name:
        fields["FirstName"] = first_name

    if last_name:
        fields["LastName"] = last_name

    if fields:
        query += " WHERE " + " AND ".join(
            f"{key}=?" for key in fields.keys()
        )

    records = execute_qeury(query=query, args=tuple(fields.values()))

    return format_records(records)


@app.route('/price')
@use_kwargs(
    {
        'country': fields.Str(
            required=False,
            load_default=None
        )
    },
    location='query'
)
def order_price(country):

    query = 'SELECT SUM(UnitPrice * Quantity) AS Sales,' \
            ' invoices.BillingCountry FROM invoice_items' \
            ' JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId ' \
            'GROUP BY BillingCountry '

    fields = {}

    if country:
        fields['BillingCountry'] = country

    if fields:
        query += 'HAVING ' + 'invoices.BillingCountry == '.join(
            f"{key}=?" for key in fields.keys()
        )

    records = execute_qeury(query=query, args=tuple(fields.values()))


    return format_records(records)


@app.route('/track')
@use_kwargs(
    {
        'TrackId': fields.Int(
            required=False,
            load_default=None
        )
    },
    location='query'
)
def get_all_info_about_track(TrackId):

    query = 'SELECT tracks.Name, Composer, albums.Title, media_types.Name, genres.Name FROM tracks ' \
            'JOIN media_types ON tracks.MediaTypeId == media_types.MediaTypeId ' \
            'JOIN albums ON tracks.AlbumId == albums.AlbumId ' \
            'JOIN genres ON tracks.GenreId == genres.GenreId ' \
            'GROUP BY TrackId '

    fields = {}

    if TrackId:
        fields['TrackId'] = TrackId

    if fields:
        query += 'HAVING ' + 'TrackId == '.join(
            f"{key}=?" for key in fields.keys()
        )


    records = execute_qeury(query=query, args=tuple(fields.values()))
    print(records)
    print(fields)

    return format_records(records)

app.run(port=5002, debug=True)
