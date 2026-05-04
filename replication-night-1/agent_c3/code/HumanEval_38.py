def encode_cyclic(s):
    g=[s[3*i:min(3*i+3,len(s))] for i in range((len(s)+2)//3)]
    g=[(x[1:]+x[0]) if len(x)==3 else x for x in g]
    return ''.join(g)
def decode_cyclic(s):
    g=[s[3*i:min(3*i+3,len(s))] for i in range((len(s)+2)//3)]
    g=[(x[2:]+x[:2]) if len(x)==3 else x for x in g]
    return ''.join(g)