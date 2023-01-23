def new_format(number: str) -> str:
    number = int(number)
    format_number = format(number, ',')
    format_number = format_number.replace(',', '.')
    return str(format_number)


assert (new_format("1000000") == "1.000.000")
assert (new_format("100") == "100")
assert (new_format("1000") == "1.000")
assert (new_format("100000") == "100.000")
assert (new_format("10000") == "10.000")
assert (new_format("0") == "0")
