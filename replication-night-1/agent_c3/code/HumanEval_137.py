def compare_one(a,b):
    ta,tb=a,b
    if isinstance(ta,str): ta=ta.replace(',','.')
    if isinstance(tb,str): tb=tb.replace(',','.')
    if float(ta)==float(tb): return None
    return a if float(ta)>float(tb) else b