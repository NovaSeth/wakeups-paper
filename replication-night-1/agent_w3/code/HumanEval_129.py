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