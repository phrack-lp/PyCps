import sys

Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float

def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def rator(m):
    print(m)
    cps_trans(m)
def apply_cps(rator,rand,k):
    print("in apply cps rator:" + str(rator) + "  rand: "+ str(rand))
    ab = ['k']
    ae = []
    if(rator[0] != 'lambda'):
        ae.append(rator)
        for r in rand:
            ae.append(r)
        return ae

    print(cps_trans(rator,lambda m:m))

    return cps_trans(rator,lambda m:cps_trans(rand,lambda n: m.append(n)))



def con_param(param):
    pl = []
    for p in param:
        pl.append(p)
    pl.append('k')
    return pl

def con_body(body,k):
    bs = ['k']
    be = []
    if(body[0] != 'lambda'):
        for b in body:
            be.append(b);
        bs.append(be)
    else:
        (_,ip,ib) = body

        t = lambda_cps(ip,ib,lambda l:l)

    return bs

def lambda_cps(p,b,k):

    return k(['lambda',p,cps_trans(b,lambda m:m)])


def cps_trans(ast,k):
    #print("trans ast: " + str(ast))
    if not isinstance(ast,List):
        return k(ast)
    elif ast[0] == 'lambda':
        (_, param, body) = ast
        return lambda_cps(param,body,k)
    else:
        rator = ast[0]
        rand = []
        for i in range(1,len(ast)):
            rand.append(ast[i])

        if(len(rand) == 1):
            rand = rand[0]

        t = apply_cps(rator,rand,k)
        print("apply_cps res:" + str(t))

        return t


def cps(e):
    return cps_trans(e,lambda m:m)

def unparse_ast(s):
    for i in s:
        if isinstance(i,str):
            sys.stdout.write(i);

        elif isinstance(i,list):
            sys.stdout.write('(')
            unparse_ast(i)
            sys.stdout.write(')')
 
        else:
            sys.stdout.write(str(i))

        if(s.index(i) == len(s) - 1):
            continue
        sys.stdout.write(' ')

def cps_out(cps_r):
    if(isinstance(cps_r,Symbol) | isinstance(cps_r,Number)):
        print(cps_r)
    else:
        sys.stdout.write('(')
        unparse_ast(cps_r)
        print(')')

def docps(e):
    cps_out(cps(parse(e)))
