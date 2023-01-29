def pig_it(text: str):
    text = text.split()
    format_text = []

    for word in text:
        if word in "!?#$%^*&@":
            symbol = word
            format_text.append(symbol)
        else:
            word = word[1:] + word[0] + "ay"
            format_text.append(word)

    result = ' '.join(format_text)

    return result


print(pig_it('Pig latin is cool !'))
