import cmath


def is_square(number: int) -> bool:
    if number < 0:
        return False
    else:
        return number == cmath.sqrt(number) ** 2


print(is_square(-1))
print(is_square(0))
print(is_square(3))
print(is_square(4))
print(is_square(25))
print(is_square(26))
