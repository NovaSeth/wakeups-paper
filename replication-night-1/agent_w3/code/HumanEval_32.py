import math
def poly(xs, x): return sum(c*math.pow(x,i) for i,c in enumerate(xs))
def find_zero(xs):
    a,b=-1.0,1.0
    while poly(xs,a)*poly(xs,b)>0: a*=2; b*=2
    for _ in range(30):
        m=(a+b)/2
        if poly(xs,a)*poly(xs,m)>0: a=m
        else: b=m
    return a