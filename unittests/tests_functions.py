import unittest

from unittests.functions import Fibonacci, formatted_name


class TestFibonacci(unittest.TestCase):

    def setUp(self) -> None:
        self.function = Fibonacci()

    def test_fibonacci_returns_1(self):
        self.assertEqual(self.function(1), 1)

    def test_fibonacci_returns_float(self):
        self.assertRaises(ValueError, self.function, 0.5)

    def test_default_number_fibonacci(self):
        self.assertEqual(self.function(17), 1597)

    def test_big_number_fibonacci(self):
        self.assertEqual(self.function(110), 43566776258854844738105)

    def test_huge_number_fibonacci(self):
        self.assertEqual(self.function(410),
                         21649481537897403506609107715822337285038973915379503528404929519011871658725122483505)

    def test_fibonacci_returns_str(self):
        self.assertRaises(ValueError, self.function, "0")

    def test_fibonacci_returns_negative(self):
        self.assertRaises(ValueError, self.function, -1)


class TestFormattedName(unittest.TestCase):

    def test_name_surname_lower_case(self):
        self.assertEqual(formatted_name('artur', 'vini', middle_name='a'), 'Artur A Vini')

    def test_name_surname_upper_case(self):
        self.assertEqual(formatted_name('ARTUR', 'VINI', middle_name='A'), 'Artur A Vini')

    def test_full_name_default_case(self):
        self.assertEqual(formatted_name('Artur', 'Vini', middle_name='A'), 'Artur A Vini')

    def test_without_middle_name_default_case(self):
        self.assertEqual(formatted_name('Artur', 'Vini'), 'Artur Vini')

    def test_name_surname_int_without_middle_name(self):
        with self.assertRaises(TypeError):
            formatted_name(0, 9)

    def test_default_case_with_middle_name_int_(self):
        with self.assertRaises(TypeError):
            formatted_name("Artur", "Vini", 0)
