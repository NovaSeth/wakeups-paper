import math
def poly(xs, x): return sum([c*math.pow(x,i) for i,c in enumerate(xs)])
def find_zero(xs):
    begin,end=-1.0,1.0
    while poly(xs,begin)*poly(xs,end)>0: begin*=2; end*=2
    for _ in range(30):
        center=(begin+end)/2.0
        if poly(xs,begin)*poly(xs,center)>0: begin=center
        else: end=center
    return begin