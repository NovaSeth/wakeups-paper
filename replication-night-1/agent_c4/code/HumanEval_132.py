def is_nested(s):
    opens=[i for i,c in enumerate(s) if c=='[']
    closes=[i for i,c in enumerate(s) if c==']']
    closes.reverse(); cnt=0; i=0
    for idx in opens:
        if i<len(closes) and idx<closes[i]: cnt+=1; i+=1
    return cnt>=2