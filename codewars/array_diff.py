def array_diff(a: list, b: list) -> list:
    for number in b:
        while number in a:
            a.remove(number)
    return a


print(array_diff([1, 2, 2], [2]))
