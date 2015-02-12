"# -*- coding: UTF-8 -*-" 
import lex
import sys
import yacc
from setlanlexer import setlanLexer, parseArgs, tokens, find_column

entrada = parseArgs(sys.argv)
with open(entrada, "r") as myfile:
    data=myfile.read()#.replace('\n', '')
t = setlanLexer(data)
count = 0

precedence = (
    ('left', 'TokenOr'),
    ('left', 'TokenAnd'),
    ('nonassoc', 'TokenMenorQue', 'TokenMayorQue','TokenMenorIgual','TokenMayorIgual'),
    ('nonassoc', 'TokenIgualQue', 'TokenNoIgual'),
    ('right', 'not', 'TokenSetContains'),
    ('left', 'TokenUnion', 'TokenDif'),
    ('left', 'TokenIntersec'),
    ('left', 'TokenSetSuma', 'TokenSetResta'),
    ('left', 'TokenSetMult', 'TokenSetEnterDiv', 'TokenSetResto'),
    ('right', 'TokenSetMin','TokenSetMax','TokenSetSize'),
    ('left', 'TokenSuma', 'TokenResta'),
    ('left', 'TokenMult', 'TokenEnterDiv','TokenResto'),
    ('right', 'negacion'),
)

start = 'program'

def p_program(p):
    '''program : TokenProgram instruccion'''
    p[0] = ("Program", p[2])
def print_program(p,numero):
    print "PROGRAM"
    print_instruccion(p[1],numero+4)

def p_instruccion(p):
    '''instruccion : bloque
                   | asignacion
                   | if
                   | ciclo
                   | imprimir 
                   | read'''
    p[0] = p[1]
def print_instruccion(p,numero):
    if(p[0]=="bloque"):
        print_bloque(p,numero)
    elif(p[0]=="leer"):
        print_leer(p,numero)
    elif(p[0]=="imprimir"):
        print_imprimir(p,numero)
    elif(p[0]=="asignar"):
        print_asignar(p,numero)
    elif(p[0]=="if"):
        print_if(p,numero)
    elif(p[0]=="ciclo"):
        print_ciclo(p,numero)

def p_instrucciones(p):
    '''instrucciones : instruccion TokenSemicolon
                     | instrucciones instruccion TokenSemicolon'''
    if(len(p)==3):
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]

def p_asignacion(p):
    '''asignacion : TokenID TokenAsing expression
                  | TokenID TokenAsing setexpression
                  | TokenID TokenAsing boolexpression'''
    p[0]=("asignar", p[1], p[3])
def print_asignar(p,numero):
    print (" "*numero)+"ASSIGN"
    print (" "*(numero+4))+"variable"
    print (" "*(numero+8))+p[1]
    print (" "*(numero+4))+"value"
    if(((p[2])[0])=="sete"):
        print_sete(p[2],numero+8)
    elif(((p[2])[0])=="boole"):
        print_boole(p[2],numero+8)
    else:
        print_inte(p[2],numero+8)

def p_variables(p):
    '''variables : TokenID
                 | variables TokenComma TokenID'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]

def p_declaracion(p):
    '''declaracion : TokenInt variables
                   | TokenSet variables
                   | TokenBool variables'''
    p[0] = (p[1],p[2])
def print_declaracion(p,numero):
    for x in p[1]:
        print (" "*numero)+p[0]+" "+x

def p_declaraciones(p):
    '''declaraciones : declaracion TokenSemicolon
                     | declaraciones declaracion TokenSemicolon'''
    if(len(p)==3):
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[2]]
def print_declaraciones(p,numero):
    print (" "*numero)+"USING"
    for x in p:
        print_declaracion(x,numero+4)
    print (" "*numero)+"IN"

def p_bloque(p):
    '''bloque : TokenOpenCurly TokenCloseCurly
              | TokenOpenCurly instrucciones TokenCloseCurly
              | TokenOpenCurly TokenUsing declaraciones TokenIn instrucciones TokenCloseCurly'''
    x = len(p)
    if(x==3):
        p[0] = ("bloque",0)
    elif(x==4):
        p[0] = ("bloque",1,p[2])
    else:
        p[0] = ("bloque",2,p[3],p[5])
def print_bloque(p,numero):
    print (" "*numero)+"BLOCK"
    if(p[1]==0):
        pass
    elif(p[1]==1):
        for x in p[2]:
            print_instruccion(x,numero+4)
    elif(p[1]==2):
        print_declaraciones(p[2],numero+4)
        for x in p[3]:
            print_instruccion(x,numero+4)
    print (" "*numero)+"BLOCK_END"

def p_read(p):
    '''read : TokenScan TokenID'''
    p[0]=("leer",p[2])
def print_leer(p,numero):
    print (" "*numero)+"SCAN"
    print (" "*(numero+4))+"variable"
    print (" "*(numero+8))+p[1]

def p_printargs_id(p):
    '''printargs : TokenID
                 | printargs TokenComma TokenID'''
    if(len(p)==2):
        p[0]=[("id",p[1])]
    else:
        p[0]=p[1]+[("id",p[3])]

def p_printargs_string(p):
    '''printargs : TokenString
                 | printargs TokenComma TokenString'''
    if(len(p)==2):
        p[0]=[("st",p[1])]
    else:
        p[0]=p[1]+[("st",p[3])]

def p_printargs(p):
    '''printargs : expression
                 | setexpression
                 | boolexpression
                 | printargs TokenComma expression
                 | printargs TokenComma setexpression
                 | printargs TokenComma boolexpression'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]

def p_imprimir(p):
    '''imprimir : TokenPrint printargs
                | TokenPrintln printargs'''
    p[0]=("imprimir",p[1],p[2])
def print_imprimir(p,numero):
    print (" "*numero)+"PRINT"
    print (" "*(numero+4))+"elements"
    for x in p[2]:
        if(x[0]=="st"):
            print (" "*(numero+8))+"string"
            print (" "*(numero+12))+x[1]
        elif(x[0]=="id"):
            print (" "*(numero+8))+"variable"
            print (" "*(numero+12))+x[1]
        else:
            if(x[0]=="inte"):
                print_inte(x,numero+8)
            if(x[0]=="boole"):
                print_boole(x,numero+8)
            if(x[0]=="sete"):
                print_sete(x,numero+8)
    if(p[1]=="println"):
        print (" "*(numero+8))+"string"
        print (" "*(numero+12))+"\"\\n\""

def p_if(p):
    '''if : TokenIf TokenOpenParent boolexpression TokenCloseParent instruccion TokenElse instruccion
          | TokenIf TokenOpenParent boolexpression TokenCloseParent instruccion'''
    if(len(p)==6):
        p[0]=("if",False,p[3],p[5])
    else:
        p[0]=("if",True,p[3],p[5],p[7])
def print_if(p,numero):
    print (" "*numero)+"IF"
    print (" "*(numero+4))+"condition"
    print_boole(p[2],numero+8)
    print (" "*(numero+4))+"THEN"
    print_instruccion(p[3],numero+8)
    if(p[1]):
        print (" "*(numero+4))+"ELSE"
        print_instruccion(p[4],numero+8)

def p_repeat(p):
    '''ciclo : TokenRepeat instruccion TokenWhile TokenOpenParent boolexpression TokenCloseParent TokenDo instruccion
             | TokenRepeat instruccion TokenWhile TokenOpenParent boolexpression TokenCloseParent'''
    if(len(p)==7):
        p[0] = ("ciclo",2,False,p[2],p[5])
    else:
        p[0]=("ciclo",2,True,p[2],p[5],p[8])

def p_while(p):
    '''ciclo : TokenWhile TokenOpenParent boolexpression TokenCloseParent TokenDo instruccion'''
    p[0] = ("ciclo",1,p[3],p[6])

def p_ciclo(p):
    '''ciclo : TokenFor TokenID TokenMin setexpression TokenDo instruccion
             | TokenFor TokenID TokenMax setexpression TokenDo instruccion'''
    p[0] = ("ciclo",0,p[2],p[3],p[4],p[6])
def print_ciclo(p,numero):
    if(p[1]==0):
        print (" "*numero)+"FOR"
        print (" "*(numero+4))+"variable"
        print (" "*(numero+8))+p[2]
        print (" "*(numero+4))+"direction"
        print (" "*(numero+8))+p[3]
        print (" "*(numero+4))+"IN"
        print_sete(p[4],numero+4)
        print (" "*(numero+4))+"DO"
        print_instruccion(p[5],numero+8)
    elif(p[1]==1):
        print (" "*numero)+"WHILE"
        print (" "*(numero+4))+"condition"
        print_boole(p[2],numero+8)
        print (" "*(numero+4))+"DO"
        print_instruccion(p[3],numero+8)
    elif(p[1]==2):
        print (" "*numero)+"REPEAT"
        print_instruccion(p[3],numero+4)
        print (" "*numero)+"WHILE"
        print (" "*(numero+4))+"condition"
        print_boole(p[4],numero+8)
        if(p[2]):
            print (" "*(numero))+"DO"
            print_instruccion(p[5],numero+4)


def p_expr_not(p):
    'boolexpression : TokenNot boolexpression %prec not'
    p[0] = ("boole","neg",p[1],p[2])

def p_expr_boolparented(p):
    'boolexpression : TokenOpenParent boolexpression TokenCloseParent'
    p[0]=p[2]

def p_boolbase(p):
    '''boolexpression : TokenTrue
                      | TokenFalse'''
    p[0]=("boole","bool",p[1])

def p_boolvar(p):
    'boolexpression : TokenID'
    p[0] = ("boole","id",p[1])

def p_boolexpression(p):
    '''boolexpression : boolexpression TokenAnd boolexpression
                      | boolexpression TokenOr boolexpression
                      | boolexpression TokenIgualQue boolexpression
                      | boolexpression TokenNoIgual boolexpression
                      | setexpression TokenIgualQue setexpression
                      | setexpression TokenNoIgual setexpression
                      | expression TokenSetContains setexpression
                      | expression TokenIgualQue expression
                      | expression TokenNoIgual expression
                      | expression TokenMenorQue expression
                      | expression TokenMayorQue expression
                      | expression TokenMenorIgual expression
                      | expression TokenMayorIgual expression'''
    p[0]=("boole",p[2],p[1],p[3])
def print_boole(p,numero):
    if(p[1]=="neg"):
        print (" "*numero)+"BOOLNEG "+p[2]
        print_boole(p[3],numero+4)
    elif(p[1]=="bool"):
        print (" "*numero)+"bool "
        print (" "*(numero+4))+p[2]
    elif(p[1]=="id"):
        print (" "*numero)+"variable"
        print (" "*(numero+4))+p[2]
    else:
        print (" "*numero)+"BOOLOPERATOR "+p[1]
        if(((p[2])[0])=="sete"):
            print_sete(p[2],numero+4)
        elif(((p[2])[0])=="boole"):
            print_boole(p[2],numero+4)
        else:
            print_inte(p[2],numero+4)
        if(((p[3])[0])=="sete"):
            print_sete(p[3],numero+4)
        elif(((p[3])[0])=="boole"):
            print_boole(p[3],numero+4)
        else:
            print_inte(p[3],numero+4)

def p_numeros(p):
    '''numeros : expression
               | numeros TokenComma expression'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]

def p_expr_setparented(p):
    'setexpression : TokenOpenParent setexpression TokenCloseParent'
    p[0]=p[2]

def p_setbase(p):
    '''setexpression : TokenOpenCurly TokenCloseCurly
                     | TokenOpenCurly numeros TokenCloseCurly'''
    if(len(p)==3):
        p[0]=("sete","void")
    else:
        p[0]=("sete","base",p[2])

def p_setvar(p):
    'setexpression : TokenID'
    p[0] = ("sete","id",p[1])

def p_setexpression(p):
    '''setexpression : setexpression TokenUnion setexpression
                     | setexpression TokenDif setexpression
                     | setexpression TokenIntersec setexpression
                     | expression TokenSetSuma setexpression
                     | expression TokenSetResta setexpression
                     | expression TokenSetMult setexpression
                     | expression TokenSetEnterDiv setexpression
                     | expression TokenSetResto setexpression'''
    p[0]=("sete",p[2],p[1],p[3])
def print_sete(p,numero):
    if(p[1]=="void"):
        print (" "*numero)+"empty set"
    elif(p[1]=="id"):
        print (" "*numero)+"variable"
        print (" "*(numero+4))+p[2]
    elif(p[1]=="base"):
        print (" "*numero)+"set"
        for x in p[2]:
            print_inte(x,numero+4)
    else:
        print (" "*numero)+"SETOPERATOR "+p[1]
        if(((p[2])[0])=="sete"):
            print_sete(p[2],numero+4)
        else:
            print_inte(p[2],numero+4)
        print_sete(p[3],numero+4)

def p_expr_negacion(p):
    'expression : TokenResta expression %prec negacion'
    p[0] = ("inte","neg",p[1],p[2])

def p_expr_parented(p):
    'expression : TokenOpenParent expression TokenCloseParent'
    p[0]=p[2]

def p_expbase(p):
    'expression : TokenID'
    p[0] = ("inte","id",p[1])

def p_expbase2(p):
    'expression : TokenNumber'
    p[0] = ("inte","num",p[1])

def p_setintunary(p):
    '''expression : TokenSetMin setexpression
                  | TokenSetMax setexpression
                  | TokenSetSize setexpression'''
    p[0]=("inte","setu",p[1],p[2])

def p_expression(p):
    '''expression : expression TokenSuma expression
                  | expression TokenResta expression
                  | expression TokenMult expression
                  | expression TokenEnterDiv expression
                  | expression TokenResto expression'''
    p[0] = ("inte",p[2],p[1],p[3])
def print_inte(p,numero):
    if(p[1]=="id"):
        print (" "*numero)+"variable"
        print (" "*(numero+4))+p[2]
    elif(p[1]=="num"):
        print (" "*numero)+"int"
        print (" "*(numero+4))+str(p[2])
    elif(p[1]=="neg"):
        print (" "*numero)+"NEGATE "+p[2]
        print_inte(p[3],numero+4)
    elif(p[1]=="setu"):
        print (" "*numero)+"SETOPERATOR "+p[2]
        print_sete(p[3],numero+4)
    else:
        print (" "*numero)+"OPERATOR "+p[1]
        print_inte(p[2],numero+4)
        print_inte(p[3],numero+4)

# Error rule for syntax errors
def p_error(p):
    global data
    global lineas
    global errores
    errores = True
    print u"ERROR: unexpected token '"+str(p.value)+"' at line "+str(p.lineno-lineas+1)+", column "+str(find_column(data,p))

# Build the parser
lineas = len(data.split("\n"))
errores = False
parser = yacc.yacc()
g = parser.parse(data)
if errores:
    quit()
print_program(g,0)
