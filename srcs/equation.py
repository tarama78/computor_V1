import srcs.color as c

class Equation(object):
    def __init__(self, eq):
        self.eq = eq
        self.val_eq = {
            'left' : None, # [X^0, X^1, X^2, ..., X^n]
            'right' : None
        }
        self.maxExp = 0
        self.initVal()

##### parser
    def initVal(self):
        tmp = self.eq.replace(' ', '').replace('\t', '').replace('\n', '')
        tab = []

        i = 0
        while i < len(tmp):
            j = 1
            while i + j < len(tmp) and not tmp[i + j] in ('+', '-', '='):
                j += 1
            tab.append(tmp[i:i + j])
            if i + j < len(tmp):
                tab.append(tmp[i + j])
            i += j + 1

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

        if val.find('X') == -1 and val.find('x') == -1: # X^0
            ret['exp'] = 0
            try:
                ret['val'] = float(val)
            except ValueError: ########################### gere les 2*3 ???
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
        while i < len(val):
            if val[i] in ('x', 'X'):
                i += 2
                while i < len(val) and val[i].isdigit():
                    i += 1
            if i < len(val) and (val[i].isdigit() or val[i] in ('.', '-')):
                j = i + (1 if val[i] == '-' else 0)
                while j < len(val) and (val[j].isdigit() or val[j] == '.'):
                    j += 1
                try:
                    res = float(val[i:j])
                except:
                    print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                            ' %s is not a float' % (val))
                    exit(1)
                break
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
        if pos + 2 >= len(val) or val[pos + 1] != '^':
            print(c.RED + c.BOLD + 'ERROR:' + c.EOC + c.BOLD +
                    ' %s is not avalid exposant' % (val))
            exit(1)

        pos += 2
        i = pos
        while i < len(val) and val[i].isdigit():
            i += 1
        return int(val[pos:i])
###
    def getMaxExp(self, tab):
        self.maxExp = 0
        for i in tab:
            self.maxExp = max(self.maxExp, self.getExp(i))
##### end parser

##### print
    def printEq(self):
        print(end=c.BOLD + c.GREEN)
        for i, val, in enumerate(self.val_eq['left']):
            if i > 0:
                print(end=' + ')
            print('{} * X^{}'.format(val, i), end='')
        print(end=' = ')
        for i, val, in enumerate(self.val_eq['right']):
            if i > 0:
                print(' + ', end='')
            print('{} * X^{}'.format(val, i), end='')
        print(c.EOC)
##### end print
