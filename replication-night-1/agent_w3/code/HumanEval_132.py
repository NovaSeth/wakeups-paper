def is_nested(s):
    o=[i for i,c in enumerate(s) if c=='[']
    c=[i for i,ch in enumerate(s) if ch==']']
    c.reverse(); cnt=0; i=0
    for idx in o:
        if i<len(c) and idx<c[i]: cnt+=1; i+=1
    return cnt>=2