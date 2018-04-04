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
        self.val_eq['left'] = [1 for i in range(self.maxExp)]
        self.val_eq['right'] = [1 for i in range(self.maxExp)]
        try:
            self.initPart('left', tab[0:tab.index('=')])
            self.initPart('right', tab[tab.index('=') + 1:])
        except ValueError: # if we dont have '=' -> (right = 0)
            self.initPart('left', tab)
            self.initPart('right', ['0'])


    def initPart(self, part, tab):
        print(part, tab)
        for i, val in enumerate(tab):
            if i % 2 == 0:
                res = self.parseOne(val, tab[i - 1] if i > 0 else '+')
                print('%d * X^%d' % (res['val'], res['exp']))

    
    def parseOne(self, val, sign):
        ret = {
            'val' : 1,
            'exp' : 0
        }

        return ret

    def getMaxExp(self, tab):
        print(c.RED + c.BOLD + 'getMaxExp a faire' + c.EOC)
        self.maxExp = 3


    def printEq(self):
        for i, val, in enumerate(self.val_eq['left']):
            if i > 0:
                print(end=' + ')
            print('%d * X^%d' % (val, i), end='')
        print(end=' = ')
        for i, val, in enumerate(self.val_eq['right']):
            if i > 0:
                print(' + ', end='')
            print('%d * X^%d' % (val, i), end='')
        print()
