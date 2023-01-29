import datetime
import math
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

from colorama import Fore, Style

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!!!!</p>"


@app.route("/Mykhailo")
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

    if result.status_code not in (HTTPStatus.OK,):
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
def get_all_info_about_track(track_id):
    query = 'SELECT tracks.Name, Composer, albums.Title, media_types.Name, genres.Name FROM tracks ' \
            'JOIN media_types ON tracks.MediaTypeId == media_types.MediaTypeId ' \
            'JOIN albums ON tracks.AlbumId == albums.AlbumId ' \
            'JOIN genres ON tracks.GenreId == genres.GenreId ' \
            'GROUP BY TrackId '

    fields = {}

    if track_id:
        fields['TrackId'] = track_id

    if fields:
        query += 'HAVING ' + 'TrackId == '.join(
            f"{key}=?" for key in fields.keys()
        )

    records = execute_qeury(query=query, args=tuple(fields.values()))

    return format_records(records)


@app.route('/stats-music')
@use_kwargs(
    {
        'genre': fields.Str(
            required=True
        )
    },
    location='query'
)
def stats_by_city(genre):
    query = 'WITH result AS (SELECT BillingCity, genres.Name, COUNT(*) ' \
            'AS genre_city FROM tracks ' \
            'JOIN genres ON tracks.GenreId = genres.GenreId ' \
            'JOIN invoice_items ON tracks.TrackId = invoice_items.TrackId ' \
            'JOIN invoices ON invoice_items.InvoiceId = invoices.InvoiceId '

    fields = {}

    if genre:
        fields['genres.name'] = genre

    if fields:
        query += 'WHERE ' + 'genres.Name == '.join(
            f"{key}=?" for key in fields.keys()
        )
        query += ' GROUP BY BillingCity) ' + \
                 'SELECT * FROM result WHERE genre_city IN (SELECT max(genre_city) FROM result);'

    records = execute_qeury(query=query, args=tuple(fields.values()))

    if not records:
        return 'INCORRECT GENRE(( ' \
               'CHOOSE ANOTHER STYLE OF MUSIC ' \
               'OR CHECK YOUR INPUT GENRE'

    return format_records(records)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:

    def __init__(self, circle_x, circle_y, radius):
        self.circle_x = circle_x
        self.circle_y = circle_y
        self.radius = radius

    def __contains__(self, point):

        if (
                (point.x - self.circle_x) * (point.x - self.circle_x) +
                (point.y - self.circle_y) * (point.y - self.circle_y) <= self.radius * self.radius
        ):
            return True

        else:
            return False


class Frange:
    @staticmethod
    def frange(start, stop=None, step=None):
        start = float(start)

        if stop is None:
            stop = start + 0.0
            start = 0.0

        if step is None:
            step = 1.0

        count = 0
        while True:
            temp = float(start + count * step)

            if step > 0 and temp >= stop:
                break

            elif step < 0 and temp <= stop:
                break
            yield temp

            count += 1


class colorizer:

    def __init__(self, text_color, text):
        self.text_color = text_color
        self.text = text

    def __enter__(self):
        self.color_blue = Fore.BLUE
        self.color_green = Fore.GREEN
        self.color_red = Fore.RED
        self.color_black = Fore.BLACK
        self.color_yellow = Fore.YELLOW
        self.color_white = Fore.WHITE
        self.color_magenta = Fore.MAGENTA
        self.color_cyan = Fore.CYAN

        if self.text_color == 'red':
            return self.color_red + self.text_color + '\n' + self.text

        elif self.text_color == 'blue':
            return self.color_blue + self.text_color + '\n' + self.text

        elif self.text_color == 'green':
            return self.color_green + self.text_color + '\n' + self.text

        elif self.text_color == 'black':
            return self.color_black + self.text_color + '\n' + self.text

        elif self.text_color == 'yellow':
            return self.color_yellow + self.text_color + '\n' + self.text

        elif self.text_color == 'white':
            return self.color_white + self.text_color + '\n' + self.text

        elif self.text_color == 'magenta':
            return self.color_magenta + self.text_color + '\n' + self.text

        elif self.text_color == 'cyan':
            return self.color_cyan + self.text_color + '\n' + self.text

        else:
            return f'choose another color or check your input color'.upper()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(Style.RESET_ALL)
        return print('printed in default color')


with colorizer('magenta', 'Hello World!!') as c:
    print(c)


class Shape:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def square(self):
        return 0


class Circle(Shape):

    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius

    def square(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):

    def __init__(self, x, y, height, width):
        super().__init__(x, y)
        self.height = height
        self.width = width

    def square(self):
        return self.width * self.height


class Parallelogram(Rectangle):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width)
        self.angle = angle

    def print_angle(self):
        print(self.angle)

    def __str__(self):
        result = super().__str__()
        return result + f'\nParallelogram: {self.width}, {self.height}, {self.angle}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def square(self):
        return self.width * self.height


class Triangle(Parallelogram):

    def __init__(self, x, y, height, width, angle):
        super().__init__(x, y, height, width, angle)

    def square(self):
        return (0.5 * self.width) * self.height


class Scene:
    def __init__(self):
        self._figures = []

    def add_figure(self, figure):
        self._figures.append(figure)

    def total_square(self):
        return sum(f.square() for f in self._figures)

    def __str__(self):
        pass


r = Rectangle(0, 0, 10, 20)
r1 = Rectangle(10, 0, -10, 20)
r2 = Rectangle(0, 20, 100, 20)

c = Circle(10, 0, 10)
c1 = Circle(100, 100, 5)

p = Parallelogram(1, 2, 20, 30, 45)
p1 = Parallelogram(1, 2, 20, 30, 45)
str(p1)

scene = Scene()
scene.add_figure(r)
scene.add_figure(r1)
scene.add_figure(r2)
scene.add_figure(c)
scene.add_figure(c1)

scene.total_square()

# app.run(port=5001, debug=True)
