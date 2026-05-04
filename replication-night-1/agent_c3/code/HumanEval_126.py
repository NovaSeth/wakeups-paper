def is_sorted(lst):
    from collections import Counter
    if any(lst[i]>lst[i+1] for i in range(len(lst)-1)): return False
    if any(v>2 for v in Counter(lst).values()): return False
    return True