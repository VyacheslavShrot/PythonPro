def make_readable(seconds: int):
    mm, ss = divmod(seconds, 60)
    hh, mm = divmod(mm, 60)
    hh = str(hh)
    ss = str(ss)
    mm = str(mm)
    if len(hh) == 1:
        hh = "0" + hh
    if len(mm) == 1:
        mm = "0" + mm
    if len(ss) == 1:
        ss = "0" + ss
    return f"{hh}:{mm}:{ss}"


print(make_readable(0))
print(make_readable(5))
print(make_readable(60))
print(make_readable(86399))
print(make_readable(359999))
