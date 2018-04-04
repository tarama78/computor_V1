import sys
import srcs.color as c
from srcs.equation import Equation


#try:
if len(sys.argv) == 1:
    eq = input('Equation: ')
elif len(sys.argv) == 2:
    eq = sys.argv[1]
else:
    print('Usage: python computor.py [equation]')
    exit(1)

if len(eq) == 0:
    print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD + ' empty argument')
    exit(1)

eq = Equation(str(eq))
eq.initVal()
print(end='Your equation: ' + c.BOLD)
eq.printEq()
print(end=c.EOC)

eq.reduce()
print(end='Reduced form:  ' + c.BOLD)
eq.printEq()
print(end=c.EOC)

print('Polynomial degree: {}{}{}'.format(c.BOLD, eq.maxExp, c.EOC))
if eq.maxExp > 2:
    print('The polynomial degree is stricly greater than 2, I can\'t solve.')
    exit(1)
else:
    eq.resolve()

if len(eq.result) == 1:
    print('Solution: {}{:.5g}{}'.format(c.BOLD, eq.result[0], c.EOC))
elif len(eq.result) == 2:
    print('Solution 1: {}{:.5g}{}'.format(c.BOLD, eq.result[0], c.EOC))
    print('Solution 2: {}{:.5g}{}'.format(c.BOLD, eq.result[1], c.EOC))
elif eq.possible == 1:
    print('All real numbers are solutions')
else:
    print('There is no solution')
    
#except:
#    print(c.RED + c.BOLD + 'ERROR' + c.EOC + c.BOLD)
