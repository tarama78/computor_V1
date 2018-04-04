import srcs.color as c
from srcs.sqrt import sqrt

class Equation(object):
    def __init__(self, eq):
        self.eq = eq
        self.val_eq = {
            'left' : None, # [X^0, X^1, X^2, ..., X^n]
            'right' : None
        }
        self.maxExp = 0
        self.result = None
        self.possible = 1 # == 0 if there are no solution
        self.autorized_chars = '0123456789. +-*=xX^'

##### reduce
    def reduce(self):
        for i, val in enumerate(self.val_eq['right']):
            self.val_eq['left'][i] -= val
            self.val_eq['right'][i] = 0
##### end reduce

##### solve
    def resolve(self):
        if self.maxExp == 0:
            self.result = []
        elif self.maxExp == 1:
            self.resolveDeg1()
        elif self.maxExp == 2:
            self.resolveDeg2()
        else:
            self.possible = 0

    def resolveDeg1(self):
        self.result = [0.0]
        if self.val_eq['left'][0] != 0:
            self.result[0] -= self.val_eq['left'][0]
        if self.val_eq['left'][1] != 0:
            self.result[0] /= self.val_eq['left'][1]
        if self.result[0] == -0:
            self.result[0] = 0

    def resolveDeg2(self):
        a = self.val_eq['left'][2]
        b = self.val_eq['left'][1]
        c = self.val_eq['left'][0]
        delta = b**2 - 4 * a * c
        if delta < 0:
            self.result = []
            self.possible = 0
        elif delta == 0:
            self.result = [-b / (2 * a)]
            if self.result[0] == -0:
                self.result[0] = 0
        else:
            self.result = [
                (-b - sqrt(delta)) / (2 * a),
                (-b + sqrt(delta)) / (2 * a)
            ]
            if self.result[0] == -0:
                self.result[0] = 0
            if self.result[1] == -0:
                self.result[1] = 0
##### end solve

##### parser
    def initVal(self):
        self.tejErr()
#        tmp = self.eq.replace(' ', '').replace('\t', '').replace('\n', '')
        tmp = self.eq
        tab = []

        i = 0
        while i < len(tmp):
            j = 1
            while i + j < len(tmp) and not tmp[i + j] in ('+', '-', '='):
                j += 1
            tab.append(tmp[i:i + j].strip())
            if i + j < len(tmp):
                tab.append(tmp[i + j])
            i += j + 1

        if tab[-1] in ('=', '+', '-'):
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' invalid line')
            exit(1)

        # set values for equation
        self.getMaxExp(tab)
        self.val_eq['left'] = [0.0 for i in range(self.maxExp + 1)]
        self.val_eq['right'] = [0.0 for i in range(self.maxExp + 1)]
        try:
            self.initPart('left', tab[0:tab.index('=')])
            self.initPart('right', tab[tab.index('=') + 1:])
        except ValueError: # if we dont have '=' -> (right = 0)
            self.initPart('left', tab)
            self.initPart('right', ['0'])

###
    def tejErr(self):
        # check autorized char
        if 1 in [(1 if self.autorized_chars.find(c) == -1 else 0) \
                for c in self.eq]:
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' invalid char in line')
            exit(1)


###
    def initPart(self, part, tab):
        for i, val in enumerate(tab):
            if i % 2 == 0:
                res = self.parseOne(val, tab[i - 1] if i > 0 else '+')
                self.val_eq[part][res['exp']] += res['val']

###
    def parseOne(self, val, sign):
        ret = {
            'val' : 0.0,
            'exp' : 0
        }

        if len(val.split('*')) > 2 or len(val.split(' ')) > 3:
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' invalid line')
            exit(1)
        if val[0] in ('*') or val[-1] in ('*', '-'):
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' invalid line')
            exit(1)

        if (val.count('X') >= 1 and val.count('x') >= 1) or \
                val.count('X') >= 2 or val.count('x') >= 2:
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' cannot multiply x')
            exit(1)
        if val.find('X') == -1 and val.find('x') == -1: # X^0
            ret['exp'] = 0
            try:
                ret['val'] = float(val)
                if sign == '-':
                    ret['val'] = -ret['val']
            except ValueError:
                print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                        ' %s is not a float' % (val))
                exit(1)
        else:
            ret['exp'] = self.getExp(val)
            ret['val'] = self.getVal(val, sign)

        return ret

###
    def getVal(self, val, sign):
        res = 1.0
        
        i = 0
        finish = 0
        while i < len(val):
            if val[i] in ('x', 'X'):
                i += 2
                while i < len(val) and val[i].isdigit():
                    i += 1

            if i < len(val) and (val[i].isdigit() or val[i] in ('.', '-')):
                if finish == 1:
                    print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                            ' invalid line')
                    exit(1)
                j = i + (1 if val[i] == '-' else 0)
                while j < len(val) and (val[j].isdigit() or val[j] == '.'):
                    j += 1
                try:
                    res = float(val[i:j])
                except:
                    print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                            ' %s is not a float' % (val))
                    exit(1)
                i = j - 1
                finish = 1
            i += 1

        if sign == '-':
            res = -res
        return res

###
    def getExp(self, val):
        pos = val.find('X')
        if pos == -1:
            pos = val.find('x')
            if pos == -1:
                return 0
        if pos + 1 >= len(val) or val[pos + 1] == ' ':
            return 1
        if pos + 2 >= len(val) or val[pos + 1] != '^':
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' %s is not a valid exposant' % (val))
            exit(1)

        pos += 2
        i = pos
        while i < len(val) and val[i].isdigit():
            i += 1
        if i < len(val) and not val[i] in (' ', '*'):
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' %s is not a valid exposant' % (val))
            exit(1)
        return int(val[pos:i])

###
    def getMaxExp(self, tab):
        self.maxExp = 0
        for i in tab:
            self.maxExp = max(self.maxExp, self.getExp(i))
##### end parser

##### print
    def printEq(self):
        plus = 0
        zero = 1
        for i, val, in enumerate(self.val_eq['left']):
            if val == 0:
                continue
            if plus == 1:
                print(end=' + ')
            plus = 1
            zero = 0
            if i == 0:
                print('{:.3g}'.format(val), end='')
            elif i == 1:
                print('{:.3g} * X'.format(val), end='')
            else:
                print('{:.3g} * X^{}'.format(val, i), end='')
        if zero == 1:
            print(end='0')
        print(end=' = ')
        plus = 0
        zero = 1
        for i, val, in enumerate(self.val_eq['right']):
            if val == 0:
                continue
            if plus == 1:
                print(end=' + ')
            plus = 1
            zero = 0
            if i == 0:
                print('{:.3g}'.format(val), end='')
            elif i == 1:
                print('{:.3g} * X'.format(val), end='')
            else:
                print('{:.3g} * X^{}'.format(val, i), end='')
        if zero == 1:
            print(end='0')
        print()
##### end print
