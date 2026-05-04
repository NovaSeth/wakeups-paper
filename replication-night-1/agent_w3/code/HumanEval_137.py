def compare_one(a,b):
    ta=a.replace(',', '.') if isinstance(a,str) else a
    tb=b.replace(',', '.') if isinstance(b,str) else b
    if float(ta)==float(tb): return None
    return a if float(ta)>float(tb) else b