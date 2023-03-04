def rot13(text: str) -> str:
    encode = ""

    if text:
        for char in text:
            if 65 <= ord(char) <= 90 or 97 <= ord(char) <= 122:
                if 65 <= ord(char) <= 90:
                    if ord(char) + 13 > 90:
                        char = chr(ord(char) + 13 - 90 + 65 - 1)

                    else:
                        char = chr(ord(char) + 13)

                else:
                    if ord(char) + 13 > 122:
                        char = chr(ord(char) + 13 - 122 + 97 - 1)

                    else:
                        char = chr(ord(char) + 13)

            else:
                pass

            encode += char

    return encode


print(rot13("test"))
print(rot13("Test"))
print(rot13('aA bB zZ 1234 *!?%'))
