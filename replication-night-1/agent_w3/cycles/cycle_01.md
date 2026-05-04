=== REASONING ===
Cycle 1. Bugs: 32-bracket expansion only-end; 38-correct; 126-v>1->v>2; 129-max->min; 132->2->>=2; 137-return inverted.

=== ACTION ===
DONE: HumanEval/32, HumanEval/38, HumanEval/126, HumanEval/129, HumanEval/132, HumanEval/137

=== CODE_DRAFTS ===
TASK_ID: HumanEval/32
```python
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
```

TASK_ID: HumanEval/38
```python
def encode_cyclic(s):
    g=[s[3*i:min(3*i+3,len(s))] for i in range((len(s)+2)//3)]
    g=[(x[1:]+x[0]) if len(x)==3 else x for x in g]
    return ''.join(g)
def decode_cyclic(s):
    g=[s[3*i:min(3*i+3,len(s))] for i in range((len(s)+2)//3)]
    g=[(x[2:]+x[:2]) if len(x)==3 else x for x in g]
    return ''.join(g)
```

TASK_ID: HumanEval/126
```python
def is_sorted(lst):
    from collections import Counter
    if any(lst[i]>lst[i+1] for i in range(len(lst)-1)): return False
    return not any(v>2 for v in Counter(lst).values())
```

TASK_ID: HumanEval/129
```python
def minPath(grid, k):
    n=len(grid); val=n*n
    for i in range(n):
        for j in range(n):
            if grid[i][j]==1:
                t=[]
                if i: t.append(grid[i-1][j])
                if j: t.append(grid[i][j-1])
                if i!=n-1: t.append(grid[i+1][j])
                if j!=n-1: t.append(grid[i][j+1])
                val=min(t)
    return [1 if i%2==0 else val for i in range(k)]
```

TASK_ID: HumanEval/132
```python
def is_nested(s):
    o=[i for i,c in enumerate(s) if c=='[']
    c=[i for i,ch in enumerate(s) if ch==']']
    c.reverse(); cnt=0; i=0
    for idx in o:
        if i<len(c) and idx<c[i]: cnt+=1; i+=1
    return cnt>=2
```

TASK_ID: HumanEval/137
```python
def compare_one(a,b):
    ta=a.replace(',', '.') if isinstance(a,str) else a
    tb=b.replace(',', '.') if isinstance(b,str) else b
    if float(ta)==float(tb): return None
    return a if float(ta)>float(tb) else b
```

=== NEW_STATE ===
All 6 done; 38 had no bug.

=== CYCLE_NOTE ===
All 6 problems analyzed and fixed.