from lmutils import debug_info
class Utils():

    def __init__(self, conAfromH, conAfromW, conAtoH, conAtoW):

        self.conAtoH = conAtoH - 1
        self.conAtoW = conAtoW - 1

        self.conAfromW = conAfromW
        self.conAfromH = conAfromH

        self.bdy_chk = {
            '(x,{0})'.format(conAfromH):([1], [-1, 1]),
            '({0},x)'.format(conAfromW):([-1, 1], [1]),
            '(x,{0})'.format(self.conAtoH):([-1], [-1, 1]),
            '({0},x)'.format(self.conAtoW):([-1, 1], [-1])
        }

        self.horn_chk = {
            '({0},{1})'.format(self.conAfromW, self.conAfromH):(1,1),
            '({0},{1})'.format(self.conAfromW, self.conAtoH):(-1,1),
            '({0},{1})'.format(self.conAtoW, self.conAfromH):(1,-1),
            '({0},{1})'.format(self.conAtoW, self.conAtoH):(-1,-1),
        }

    def isbdy(self, p):
        try:
            #print(debug_info(), p, self.horn_chk)
            #print(debug_info(), p, self.bdy_chk)
            #print(debug_info(), self.conAtoH, self.conAtoW)
            return self.bdy_chk["({0},{1})".format(
                p[1] if p[1] in [self.conAfromW, self.conAtoW] else "x", 
                p[0] if p[0] in [self.conAfromH, self.conAtoH] else "x",
                )]
        except KeyError as e:
            #print(debug_info(), "raise error")
            return -1

    def isinarea(self, p, react):
        print(debug_info(), react)
        if p[0] in [react[0], react[2]] or p1 in [react[1], react[3]]:
            return True
        return False

    def ishorn(self, p):
        try:
            return self.horn_chk["({0},{1})".format(p[1], p[0])]
        except KeyError as e:
            return -1