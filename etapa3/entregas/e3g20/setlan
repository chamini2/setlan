#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import lex
import sys
import yacc
import setlantable
from setlanlexer import setlanLexer, tokens, find_column, imprime_tokens

flags = {"-t":False,"-a":False,"-s":False}

def parseArgs(args): #evalua argumentos de entrada
    global flags
    msg = "Error en la linea de comando:.\setlan.py <archivo_de_entrada> <flags>"
    l = len(args)
    if l < 2 or l > 5:
        print(msg)
        sys.exit(1)
    if (l>=3):
        if (args[2]!="-t"and args[2]!="-a"and args[2]!="-s"):
            print(msg)
            sys.exit(1)
    if (l>=4):
        if (args[3]!="-t"and args[3]!="-a"and args[3]!="-s"):
            print(msg)
            sys.exit(1)
    if (l>=5):
        if (args[4]!="-t"and args[4]!="-a"and args[4]!="-s"):
            print(msg)
            sys.exit(1)
    i = 2
    while(i<l):
        flags[args[i]]=True
        i+=1
    return args[1]

entrada = parseArgs(sys.argv)
with open(entrada, "r") as myfile:
    data=myfile.read()#.replace('\n', '')
t = setlanLexer(data)
count = 0

def find_column2(input,pos,line):#encuentra numero de columna del token
    last_cr = input.rfind('\n',0,pos)
    if last_cr < 0:
        last_cr = 0
    column = (pos - last_cr) + 1
    if line>1:
        column-=1
    return column

precedence = (
    ('right', 'TokenIf'),
    ('right', 'TokenElse'),
    ('left', 'TokenOr'),
    ('left', 'TokenAnd'),
    ('left', 'TokenIgualQue'),
    ('left', 'TokenNoIgual'),
    ('nonassoc', 'TokenMenorQue', 'TokenMayorQue','TokenMenorIgual','TokenMayorIgual'),
    ('right', 'TokenSetContains'),
    ('right', 'not'),
    ('left', 'TokenUnion'),
    ('left', 'TokenDif'),
    ('left', 'TokenIntersec'),
    ('nonassoc', 'TokenSetSuma','TokenSetResta','TokenSetMult','TokenSetResto','TokenSetEnterDiv'),
    ('left', 'TokenSuma'),
    ('left', 'TokenResta'),
    ('left', 'TokenMult'),
    ('left', 'TokenEnterDiv'),
    ('left','TokenResto'),
    ('right', 'TokenSetMin'),
    ('right','TokenSetMax'),
    ('right','TokenSetSize'),
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
    '''asignacion : TokenID TokenAsing expression'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    line = p.slice[2].lineno-lineas+1
    temp2 = (find_column2(data,p.slice[2].lexpos,line),line)
    p[0]=("asignar", p[1], p[3],temp,temp2)
def print_asignar(p,numero):
    print (" "*numero)+"ASSIGN"
    print (" "*(numero+4))+"variable"
    print (" "*(numero+8))+p[1]
    print (" "*(numero+4))+"value"
    print_expre(p[2],numero+8)

def p_ID(p):
    ''' ID : TokenID'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0] = (p[1],temp)

def p_variables(p):
    '''variables : ID
                 | variables TokenComma ID'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]
        p[0].append(p[3])

def p_declaracion(p):
    '''declaracion : TokenInt variables
                   | TokenSet variables
                   | TokenBool variables'''
    p[0] = (p[1],p[2])
def print_declaracion(p,numero):
    for x in p[1]:
        print (" "*numero)+p[0]+" "+x[0]

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
              | TokenOpenCurly TokenUsing TokenIn instrucciones TokenCloseCurly
              | TokenOpenCurly TokenUsing declaraciones TokenIn instrucciones TokenCloseCurly'''
    x = len(p)
    if(x==3):
        p[0] = ("bloque",0)
    elif(x==4):
        p[0] = ("bloque",1,p[2])
    elif(x==6):
        p[0] = ("bloque",1,p[4])
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
    '''read : TokenScan ID'''
    p[0]=("leer",p[2])
def print_leer(p,numero):
    print (" "*numero)+"SCAN"
    print (" "*(numero+4))+"variable"
    print (" "*(numero+8))+p[1][0]

def p_printargs_string(p):
    '''printargs : TokenString
                 | printargs TokenComma TokenString'''
    if(len(p)==2):
        p[0]=[("st",p[1])]
    else:
        p[0]=p[1]+[("st",p[3])]

def p_printargs(p):
    '''printargs : expression
                 | printargs TokenComma expression'''
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
        else:
            print_expre(x,numero+8)
    if(p[1]=="println"):
        print (" "*(numero+8))+"string"
        print (" "*(numero+12))+"\"\\n\""

def p_if(p):
    '''if : TokenIf TokenOpenParent expression TokenCloseParent instruccion TokenElse instruccion
          | TokenIf TokenOpenParent expression TokenCloseParent instruccion'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    if(len(p)==6):
        p[0]=("if",False,p[3],p[5],(),temp)
    else:
        p[0]=("if",True,p[3],p[5],p[7],temp)
def print_if(p,numero):
    print (" "*numero)+"IF"
    print (" "*(numero+4))+"condition"
    print_expre(p[2],numero+8)
    print (" "*(numero+4))+"THEN"
    print_instruccion(p[3],numero+8)
    if(p[1]):
        print (" "*(numero+4))+"ELSE"
        print_instruccion(p[4],numero+8)

def p_repeat(p):
    '''ciclo : TokenRepeat instruccion TokenWhile TokenOpenParent expression TokenCloseParent TokenDo instruccion
             | TokenRepeat instruccion TokenWhile TokenOpenParent expression TokenCloseParent'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    if(len(p)==7):
        p[0] = ("ciclo",2,False,p[2],p[5],(),temp)
    else:
        p[0]=("ciclo",2,True,p[2],p[5],p[8],temp)

def p_while(p):
    '''ciclo : TokenWhile TokenOpenParent expression TokenCloseParent TokenDo instruccion'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0] = ("ciclo",1,p[3],p[6],temp)

def p_ciclo(p):
    '''ciclo : TokenFor TokenID TokenMin expression TokenDo instruccion
             | TokenFor TokenID TokenMax expression TokenDo instruccion'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0] = ("ciclo",0,p[2],p[3],p[4],p[6],temp)
def print_ciclo(p,numero):
    if(p[1]==0):
        print (" "*numero)+"FOR"
        print (" "*(numero+4))+"variable"
        print (" "*(numero+8))+p[2]
        print (" "*(numero+4))+"direction"
        print (" "*(numero+8))+p[3]
        print (" "*(numero+4))+"IN"
        print_expre(p[4],numero+4)
        print (" "*(numero+4))+"DO"
        print_instruccion(p[5],numero+8)
    elif(p[1]==1):
        print (" "*numero)+"WHILE"
        print (" "*(numero+4))+"condition"
        print_expre(p[2],numero+8)
        print (" "*(numero+4))+"DO"
        print_instruccion(p[3],numero+8)
    elif(p[1]==2):
        print (" "*numero)+"REPEAT"
        print_instruccion(p[3],numero+4)
        print (" "*numero)+"WHILE"
        print (" "*(numero+4))+"condition"
        print_expre(p[4],numero+8)
        if(p[2]):
            print (" "*(numero))+"DO"
            print_instruccion(p[5],numero+4)


def p_expr_not(p):
    'expression3 : TokenNot expression %prec not'
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0] = ("boole","neg",p[1],p[2],temp)

def p_boolbase(p):
    '''boolexpression : TokenTrue
                      | TokenFalse'''
    p[0]=("boole","bool",p[1])

def p_boolexpression(p):
    '''expression : expression TokenOr expression
                      | expression TokenAnd expression
                      | expression TokenIgualQue expression
                      | expression TokenNoIgual expression
                      | expression TokenSetContains expression
                      | expression TokenMenorQue expression
                      | expression TokenMayorQue expression
                      | expression TokenMenorIgual expression
                      | expression TokenMayorIgual expression
                      | boolexpression'''
    global data
    global lineas
    if(len(p)==4):
        line = p.slice[2].lineno-lineas+1
        temp = (find_column2(data,p.slice[2].lexpos,line),line)
        p[0] = ("expre",p[2],p[1],p[3],temp)
    else:
        p[0]=p[1]


def p_numeros(p):
    '''numeros : expression
               | numeros TokenComma expression'''
    if(len(p)==2):
        p[0]=[p[1]]
    else:
        p[0]=p[1]+[p[3]]


def p_setbase(p):
    '''setexpression : TokenOpenCurly TokenCloseCurly
                     | TokenOpenCurly numeros TokenCloseCurly'''
    global data
    global lineas
    if(len(p)==3):
        p[0]=("sete","void")
    else:
        line = p.slice[1].lineno-lineas+1
        temp = (find_column2(data,p.slice[1].lexpos,line),line)
        p[0]=("sete","base",p[2],temp)

def p_setexpression(p):
    '''expression : expression TokenSetSuma expression
                     | expression TokenSetResta expression
                     | expression TokenSetMult expression
                     | expression TokenSetEnterDiv expression
                     | expression TokenSetResto expression
                     | expression TokenUnion expression
                     | expression TokenDif expression
                     | expression TokenIntersec expression
                     | setexpression'''
    global data
    global lineas
    if(len(p)==4):
        line = p.slice[2].lineno-lineas+1
        temp = (find_column2(data,p.slice[2].lexpos,line),line)
        p[0] = ("expre",p[2],p[1],p[3],temp)
    else:
        p[0]=p[1]


def p_expr_negacion(p):
    'expression3 : TokenResta expression %prec negacion'
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0] = ("inte","neg",p[1],p[2],temp)

def p_expr_parented(p):
    'expressionParen : TokenOpenParent expression TokenCloseParent'
    p[0]=p[2]

def p_expbase(p):
    'expressionID : TokenID'
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0] = ("expre","id",p[1],temp)

def p_expbase2(p):
    'expression3 : TokenNumber'
    p[0] = ("inte","num",p[1])

def p_setintunary(p):
    '''expression3 : TokenSetMin expression
                  | TokenSetMax expression
                  | TokenSetSize expression'''
    global data
    global lineas
    line = p.slice[1].lineno-lineas+1
    temp = (find_column2(data,p.slice[1].lexpos,line),line)
    p[0]=("inte","setu",p[1],p[2])

def p_expression(p):
    '''expression : expression TokenSuma expression
                  | expression TokenResta expression
                  | expression TokenMult expression
                  | expression TokenEnterDiv expression
                  | expression TokenResto expression
                  | expression3
                  | expressionParen
                  | expressionID'''
    global data
    global lineas
    if(len(p)==4):
        line = p.slice[2].lineno-lineas+1
        temp = (find_column2(data,p.slice[2].lexpos,line),line)
        p[0] = ("expre",p[2],p[1],p[3],temp)
    else:
        p[0]=p[1]

def print_expre(p,numero):
    if(p[1]=="id"):
        print (" "*numero)+"variable"
        print (" "*(numero+4))+p[2]
    elif(p[1]=="num"):
        print (" "*numero)+"int"
        print (" "*(numero+4))+str(p[2])
    elif(p[1]=="neg"):
        print (" "*numero)+"NEGATE "+p[2]
        print_expre(p[3],numero+4)
    elif(p[1]=="setu"):
        print (" "*numero)+"SETOPERATOR "+p[2]
        print_expre(p[3],numero+4)
    elif(p[1]=="base"):
        print (" "*numero)+"set"
        for x in p[2]:
            print_expre(x,numero+4)
    elif(p[1]=="void"):
        print (" "*numero)+"empty set"
    elif(p[1]=="neg"):
        print (" "*numero)+"BOOLNEG "+p[2]
        print_boole(p[3],numero+4)
    elif(p[1]=="bool"):
        print (" "*numero)+"bool "
        print (" "*(numero+4))+p[2]
    else:
        print (" "*numero)+"OPERATOR "+p[1]
        print_expre(p[2],numero+4)
        print_expre(p[3],numero+4)

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
errores = False

# aqui inicia lo de la tabla de simbolos

def progCheck(arbol, Tabla):
    instrucCheck(arbol[1],Tabla)

def instrucCheck(arbol,Tabla):
    if(arbol[0]=="bloque"):
        bloqueCheck(arbol,Tabla)
    elif(arbol[0]=="leer"):
        leerCheck(arbol,Tabla)
    elif(arbol[0]=="imprimir"):
        imprimirCheck(arbol,Tabla)
    elif(arbol[0]=="asignar"):
        asignarCheck(arbol,Tabla)
    elif(arbol[0]=="if"):
        ifCheck(arbol,Tabla)
    elif(arbol[0]=="ciclo"):
        cicloCheck(arbol,Tabla)

def cicloCheck(arbol,Tabla):
    global data
    global lineas
    global errores

    if(arbol[1]==0):
        hijo = setlantable.symbolTable(Tabla)
        Tabla.insertT(hijo)
        hijo.insert((arbol[2],"int",setlantable.defaults['int'],False))
        ret = expreCheck(arbol[4],Tabla)
        if not ('set'==ret):
            errores = True
            if('error'==ret):
                print u"Error en línea "+str(arbol[6][1])+u", columna "+str(arbol[6][0])+u": For  esperaba una expresion set válida."
            else:
                print u"Error en línea "+str(arbol[6][1])+u", columna "+str(arbol[6][0])+u": For  esperaba una expresion de tipo set, pero expresion de tipo "+ret+u" presente."
        instrucCheck(arbol[5],hijo)
    elif(arbol[1]==1):
        ret = expreCheck(arbol[2],Tabla)
        if not ('bool'==ret):
            errores = True
            if('error'==ret):
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": While  esperaba una expresion bool válida."
            else:
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": While  esperaba una expresion de tipo bool, pero expresion de tipo "+ret+u" presente."
        instrucCheck(arbol[3],Tabla)
    elif(arbol[1]==2):
        instrucCheck(arbol[3],Tabla)
        ret = expreCheck(arbol[4],Tabla)
        if not ('bool'==ret):
            errores = True
            if('error'==ret):
                print u"Error en línea "+str(arbol[6][1])+u", columna "+str(arbol[6][0])+u": Repeat  esperaba una expresion bool válida."
            else:
                print u"Error en línea "+str(arbol[6][1])+u", columna "+str(arbol[6][0])+u": Repeat  esperaba una expresion de tipo bool, pero expresion de tipo "+ret+u" presente."
        if(arbol[2]):
            instrucCheck(arbol[5],Tabla)


def ifCheck(arbol,Tabla):
    global data
    global lineas
    global errores
    ret = expreCheck(arbol[2],Tabla)
    if not ('bool'==ret):
        errores = True
        if('error'==ret):
            print u"Error en línea "+str(arbol[5][1])+u", columna "+str(arbol[5][0])+u": If  esperaba una expresion válida."
        else:
            print u"Error en línea "+str(arbol[5][1])+u", columna "+str(arbol[5][0])+u": If  esperaba una expresion de tipo bool, pero expresion de tipo "+ret+u" presente."
    instrucCheck(arbol[3],Tabla)
    if (arbol[1]):
        instrucCheck(arbol[4],Tabla)

def asignarCheck(arbol,Tabla):
    global data
    global lineas
    global errores
    y = Tabla.lookup(arbol[1])
    if not (y==None):
        if(not y[3]):
            errores = True
            print u"Error en línea "+str(arbol[3][1])+u", columna "+str(arbol[3][0])+u": La variable '"+arbol[1]+u"' no puede ser modificada en este alcance."
    else:
        errores = True
        print u"Error en línea "+str(arbol[3][1])+u", columna "+str(arbol[3][0])+u": La variable '"+arbol[1]+u"' no ha sido declarada en este alcance."
    ret = expreCheck(arbol[2],Tabla)
    if not (y[1]==ret):
        errores = True
        if (ret=='error'):
            print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Asignar a variable '"+arbol[1]+u"' de tipo "+y[1]+u", esperaba una expresion válida."
        else:
            print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Asignar a variable '"+arbol[1]+u"' de tipo "+y[1]+u", asignar expresion de tipo "+ret+u" no es posible."

def imprimirCheck(arbol,Tabla):
    for x in arbol[2]:
        if(x[0]=="st"):
            pass
        else:
            expreCheck(x,Tabla)

def expreCheck(arbol,Tabla):
    global data
    global lineas
    global errores
    if(arbol[1]=="id"):
        y = Tabla.lookup(arbol[2])
        if not (y == None):
            return y[1]
        else:
            errores = True
            print u"Error en línea "+str(arbol[3][1])+u", columna "+str(arbol[3][0])+u": La variable '"+arbol[2]+u"' no ha sido declarada en este alcance."
            return "error"
    elif(arbol[1]=="num"):
        return "int"
    elif(arbol[1]=="neg"):
        ret = expreCheck(arbol[3],Tabla)
        if (arbol[2] == "not"):
            esperado = "bool"
        else:
            esperado = "int"
        if (ret == "error"):
            return "error"
        elif (ret == esperado):
            return esperado
        else:
            errores = True
            print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Negación '"+arbol[2]+u"' esperaba una exprecion de tipo "+esperado+u", se encontro exprecion de tipo "+ret+u"."
            return "error"
    elif(arbol[1]=="setu"):
        ret = expreCheck(arbol[3],Tabla)
        if (ret == "error"):
            return "error"
        elif (ret == "set"):
            return "int"
        else:
            errores = True
            print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[2]+u"' esperaba una exprecion de tipo set, se encontro exprecion de tipo "+ret+u"."
            return "error"
    elif(arbol[1]=="base"):
        i = 0;
        for x in arbol[2]:
            i+=1
            ret = expreCheck(x,Tabla)
            if (ret == "error"):
                 return "error"
            elif (ret == "int"):
                pass
            else:
                errores = True
                print u"Error en línea "+str(arbol[3][1])+u", columna "+str(arbol[3][0])+u": Set esperaba una exprecion de tipo int, se encontro exprecion de tipo "+ret+u" en elemento "+str(i)+u" del set."
                return "error"
        return "set"
    elif(arbol[1]=="void"):
        return "set"
    elif(arbol[1]=="bool"):
        return "bool"
    else:
        if(arbol[1]=="==" or arbol[1]=="/="):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if(ret1==ret2):
                return "bool"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba expresiones del mismo tipo.(encontró: "+ret1+", "+ret2+")"
                return "error"
        elif(arbol[1]==">"or arbol[1]=="<"or arbol[1]==">="or arbol[1]=="<="):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if(ret1==ret2 and ret1 == "int"):
                return "bool"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba expresiones de tipo int.(encontró: "+ret1+", "+ret2+")"
                return "error"
        elif(arbol[1]=="+"or arbol[1]=="-"or arbol[1]=="*"or arbol[1]=="/" or arbol[1]=="%"):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if(ret1==ret2 and ret1 == "int"):
                return "int"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba expresiones de tipo int.(encontró: "+ret1+", "+ret2+")"
                return "error"
        elif(arbol[1]=="@"):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if("set"==ret2 and ret1 == "int"):
                return "bool"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba una expresion de tipo int y otra de tipo set.(encontró: "+ret1+", "+ret2+")"
                return "error"
        elif(arbol[1]=="and"or arbol[1]=="or"):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if(ret1==ret2 and ret1 == "bool"):
                return "bool"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba expresiones de tipo bool.(encontró: "+ret1+", "+ret2+")"
                return "error"
        elif(arbol[1]=="<+>"or arbol[1]=="<->"or arbol[1]=="<*>"or arbol[1]=="</>" or arbol[1]=="<%>"):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if("set"==ret2 and ret1 == "int"):
                return "set"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba una expresion de tipo int y otra de tipo set.(encontró: "+ret1+", "+ret2+")"
                return "error"
        elif(arbol[1]=="++"or arbol[1]=="\\"or arbol[1]=="><"):
            ret1 = expreCheck(arbol[2],Tabla)
            if(ret1=="error"):
                return "error"
            ret2 = expreCheck(arbol[3],Tabla)
            if(ret2=="error"):
                return "error"
            if(ret1==ret2 and ret1 == "set"):
                return "set"
            else:
                errores = True
                print u"Error en línea "+str(arbol[4][1])+u", columna "+str(arbol[4][0])+u": Operación '"+arbol[1]+u"' esperaba expresiones de tipo set.(encontró: "+ret1+", "+ret2+")"
                return "error"

def leerCheck(arbol,Tabla):
    global data
    global lineas
    global errores
    y = Tabla.lookup(arbol[1][0])
    if not (y==None):
        if(y[1]=="set"):
            errores = True
            print u"Error en línea "+str(arbol[1][1][1])+u", columna "+str(arbol[1][1][0])+u": Scan no admite variables de tipo set.(Variable: "+arbol[1][0]+")"
        if(not y[3]):
            errores = True
            print u"Error en línea "+str(arbol[1][1][1])+u", columna "+str(arbol[1][1][0])+u": La variable '"+arbol[1][0]+u"' no puede ser modificada en este alcance."
    else:
        errores = True
        print u"Error en línea "+str(arbol[1][1][1])+u", columna "+str(arbol[1][1][0])+u": La variable '"+arbol[1][0]+u"' no ha sido declarada en este alcance."

def declaracionCheck(arbol,Tabla):
    global data
    global lineas
    global errores
    for x in arbol[1]:
        if Tabla.local_contains(x[0]):
          errores = True
          print u"Error en línea "+str(x[1][1])+u", columna "+str(x[1][0])+u": La variable '"+x[0]+u"' ya ha sido declarada en este alcance."
        else:
          Tabla.insert((x[0],arbol[0],setlantable.defaults[arbol[0]],True))

def declaracionesCheck(arbol,Tabla):
    hijo = setlantable.symbolTable(Tabla)
    for x in arbol:
        declaracionCheck(x,hijo)
    return hijo

def bloqueCheck(arbol,Tabla):
    if(arbol[1]==0):
        pass
    elif(arbol[1]==1):
        for x in arbol[2]:
            instrucCheck(x,Tabla)
    elif(arbol[1]==2):
        hijo = declaracionesCheck(arbol[2],Tabla)
        Tabla.insertT(hijo)
        for x in arbol[3]:
            instrucCheck(x,hijo)

Tabla = setlantable.symbolTable(None)
progCheck(g,Tabla)
if (errores):
    quit()
if (flags["-t"]):
    imprime_tokens(t, data)#para imprimir los tokens
if (flags["-a"]):
    print "\nAST:\n\n"
    print_program(g,0)
if (flags["-s"]):
    print "\nSymbol Table:\n\n"
    for x in Tabla.subT:
        x.tablePrint(0)














