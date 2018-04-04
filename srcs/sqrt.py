def sqrt(n, precision=5):
     i = 0.0
     for p in range(-10, precision):
         add = 10**-p
         while i*i <= n:
             i += add
         i -= add
         if i*i == float(n):
             return i
     return i
