import sys
import srcs.color as c
from srcs.equation import Equation


#try:
if len(sys.argv) == 1:
    eq = input('equation: ')
elif len(sys.argv) == 2:
    eq = sys.argv[1]
else:
    print('Usage: python computor.py [equation]')
    exit(1)

if len(eq) == 0:
    print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD + ' empty argument')
    exit(1)
eq = Equation(str(eq))
eq.printEq()
#except:
#    print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD)
