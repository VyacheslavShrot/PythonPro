def solution(text: str, ending: str) -> bool:
    result = text.endswith(ending)
    return result


# True
print(solution("samurai", "ai"))
print(solution("ninja", "ja"))
print(solution("sensei", "i"))
print(solution("abc", "abc"))
print(solution("abcabc", "bc"))
print(solution("fails", "ails"))

print("---")

# False
print(solution("sumo", "omo"))
print(solution("samurai", "ra"))
print(solution("abc", "abcd"))
print(solution("this", "fails"))
print(solution("spam", "eggs"))
