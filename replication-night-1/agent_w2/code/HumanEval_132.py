def is_nested(string):
    opens, closes = [], []
    for i, c in enumerate(string):
        if c == '[': opens.append(i)
        else: closes.append(i)
    closes.reverse()
    cnt, i = 0, 0
    for idx in opens:
        if i < len(closes) and idx < closes[i]:
            cnt += 1
            i += 1
    return cnt >= 2