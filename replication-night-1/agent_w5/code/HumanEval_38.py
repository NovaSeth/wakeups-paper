def encode_cyclic(s):
    groups=[s[3*i:min(3*i+3,len(s))] for i in range((len(s)+2)//3)]
    groups=[(g[1:]+g[0]) if len(g)==3 else g for g in groups]
    return ''.join(groups)
def decode_cyclic(s):
    groups=[s[3*i:min(3*i+3,len(s))] for i in range((len(s)+2)//3)]
    groups=[(g[-1]+g[:-1]) if len(g)==3 else g for g in groups]
    return ''.join(groups)