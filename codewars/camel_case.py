import re


def to_camel_case(text):
    text = re.sub('[-_?!@#$]', ' ', text)
    text = text.title().replace(' ', '')
    return text


print(to_camel_case("A-B-C?"))
print(to_camel_case("the_stealth_warrior"))
print(to_camel_case("The-Stealth-Warrior"))
