def alphabet_position(text):
    text = ' '.join(
        str(ord(i)-96)
        for i in text.lower()
        if i.isalpha()
    )
    return text


print(alphabet_position("Text"))
