#!/usr/bin/env python
'''
Autor: Jose Daniel Duran Toro
Carnet: 10-10222
'''
import lex
import sys

def parseArgs(args): #evalua argumentos de entrada
    msg = "Error en la linea de comando:.\setlan.py <archivo_de_entrada>"
    if len(args) != 2:
        print(msg)
        sys.exit(1)
    return args[1]

def find_column(input,token):#encuentra numero de columna del token
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
	last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column

#int main(){
entrada = parseArgs(sys.argv)
with open(entrada, "r") as myfile:
    data=myfile.read()#.replace('\n', '')

tokens = (
   'TokenString',
   'TokenComentario',
   'TokenProgram',
   'TokenOpenCurly',
   'TokenCloseCurly',
   'TokenOpenParent',
   'TokenCloseParent',
   'TokenUsing',
   'TokenIn',
   'TokenIf',
   'TokenElse',
   'TokenFor',
   'TokenMin',
   'TokenMax',
   'TokenWhile',
   'TokenRepeat',
   'TokenDo',
   'TokenInt',
   'TokenSet',
   'TokenBool',
#operadores:
   'TokenOr',
   'TokenAnd',
   'TokenNot',
   'TokenSetSuma',
   'TokenSetResta',
   'TokenSetMult',
   'TokenSetEnterDiv',
   'TokenSetResto',
   'TokenSetMin',
   'TokenSetMax',
   'TokenSetSize',
   'TokenUnion',
   'TokenDif',
   'TokenIntersec',
   'TokenSetContains',
   'TokenMenorIgual',
   'TokenMayorIgual',
   'TokenMenorQue',
   'TokenMayorQue',
   'TokenIgualQue',
   'TokenNoIgual',
   'TokenSuma',
   'TokenResta',
   'TokenMult',
   'TokenEnterDiv',
   'TokenResto',
#otros:
   'TokenFalse',
   'TokenTrue',
   'TokenComma',
   'TokenSemicolon',
   'TokenScan',
   'TokenPrint',
   'TokenPrintln',
   'TokenAsing',
   'TokenID',
   'TokenNumber',
)

t_TokenString = r'"([^\\"]|\\\\|\\n|\\")*"'#print peligroso
t_TokenComentario = r'\#.*'
#t_TokenProgram = r'(?<![0-9A-Za-z.,"{}])program(?=[^0-9A-Za-z.,";])'
t_TokenOpenCurly = r'{'
t_TokenCloseCurly = r'}'
t_TokenOpenParent = r'\('
t_TokenCloseParent = r'\)'
#t_TokenUsing = r'(?<![0-9A-Za-z.,"])using(?=[^0-9A-Za-z.,";])'
#t_TokenIn = r'(?<![0-9A-Za-z.,"])in(?=[^0-9A-Za-z.,";])'
#t_TokenIf = r'(?<![0-9A-Za-z.,"])if(?=[^0-9A-Za-z.,";])'
#t_TokenElse = r'(?<![0-9A-Za-z.,"])else(?=[^0-9A-Za-z.,";])'
#t_TokenFor = r'(?<![0-9A-Za-z.,"])for(?=[^0-9A-Za-z.,";])'
#t_TokenMin = r'(?<=[\ ])min(?=[\ ])'
#t_TokenMax = r'(?<=[\ ])max(?=[\ ])'
#t_TokenWhile = r'(?<![0-9A-Za-z.,"])while(?=[^0-9A-Za-z.,";])'
#t_TokenRepeat = r'(?<![0-9A-Za-z.,"])repeat(?=[^0-9A-Za-z.,";])'
#t_TokenDo = r'(?<![0-9A-Za-z.,"])do(?=[^0-9A-Za-z.,";])'
#t_TokenInt = r'(?<![0-9A-Za-z.,"{}])int(?=[\ ])'
#t_TokenSet = r'(?<![0-9A-Za-z.,"{}])set(?=[\ ])'
#t_TokenBool = r'(?<![0-9A-Za-z.,"{}])bool(?=[\ ])'
#t_TokenOr = r'(?<=[\ \)])or(?=[\ \(])'
#t_TokenAnd = r'(?<=[\ \)])and(?=[\ \(])'
#t_TokenNot = r'(?<=[\ ])not(?=[\ \(])'
t_TokenSetSuma = r'<\+>'
t_TokenSetResta = r'<->'
t_TokenSetMult = r'<\*>'
t_TokenSetEnterDiv = r'</>'
t_TokenSetResto = r'<%>'
t_TokenSetMin = r'>\?'
t_TokenSetMax = r'<\?'
t_TokenSetSize = r'\$\?'
t_TokenUnion = r'\+\+'
t_TokenDif = r'\\'#print peligroso
t_TokenIntersec = r'><'
t_TokenSetContains = r'@'
t_TokenMenorIgual = r'<='
t_TokenMayorIgual = r'>='
t_TokenMenorQue = r'<'
t_TokenMayorQue = r'>'
t_TokenIgualQue = r'=='
t_TokenNoIgual = r'/='
t_TokenSuma = r'\+'
t_TokenResta = r'-'
t_TokenMult = r'\*'
t_TokenEnterDiv = r'/'
t_TokenResto = r'%'
#t_TokenFalse = r'(?<![0-9A-Za-z"])false(?=[^0-9A-Za-z"])'
#t_TokenTrue = r'(?<![0-9A-Za-z"])true(?=[^0-9A-Za-z"])'
t_TokenComma = r','
t_TokenSemicolon = r';'
#t_TokenScan = r'(?<![0-9A-Za-z.,"])scan(?=[\ ])'
#t_TokenPrint = r'(?<![0-9A-Za-z.,"])print(?=[\ ])'
#t_TokenPrintln = r'(?<![0-9A-Za-z.,"])println(?=[\ ])'
t_TokenAsing = r'='
#t_TokenID = r'(?<=[^0-9])([_A-Za-z])+([_A-Za-z0-9])*'
t_TokenNumber = r'([0-9])+(?=[^_A-Za-z0-9])'

# Define a rule so we can track line numbers

reserved = {#no sabia que podia hacer lo de la reserva antes de empezar, lo habia intentado hacer con ER pero luego descubri esto, no quiero borrar las ERs
  'program' : 'TokenProgram',
  'using' : 'TokenUsing',
  'in' : 'TokenIn',
  'if' : 'TokenIf',
  'scan' : 'TokenScan',
  'print' : 'TokenPrint',
  'println' : 'TokenPrintln',
  'else' : 'TokenElse',
  'for' : 'TokenFor',
  'min' : 'TokenMin',
  'max' : 'TokenMax',
  'while' : 'TokenWhile',
  'repeat' : 'TokenRepeat',
  'do' : 'TokenDo',
  'int' : 'TokenInt',
  'set' : 'TokenSet',
  'bool' : 'TokenBool',
  'or' : 'TokenOr',
  'and' : 'TokenAnd',
  'not' : 'TokenNot',
  'false' : 'TokenFalse',
  'true' : 'TokenTrue',
}

def t_TokenID(t): #detecta los tokenid y los diferencia de las palabras reservadas
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'TokenID')
    return t

def t_newline(t): #cuenta las nuevas lineas
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'
errores = False

def t_error(t):
    global errores
    global data
    errores = True
    print u"Error: Se encontró un caracter inesperado \"%s\" en la Línea %i, Columna %i." % (t.value[0], t.lineno, find_column(data,t))
    t.lexer.skip(1)

lexer = lex.lex()

tokens = []
lexer.input(data)
while True: #en este loop se guardan todos los tokens en una lista
    tok = lexer.token()
    if not tok: break
    tokens+=[tok]

if(not errores): #imprime los tokens si no hay errores
    for t in tokens:
        if(t.type == 'TokenString'):
            i = len(t.type) # max 16
            s = t.value.split("\\")
            sys.stdout.write("token "+t.type+" "*(16-i+3)+"value (")
            for r in s[:-1]:
                sys.stdout.write(r+"\\")
            sys.stdout.write(s[len(s)-1])
            print ") at line "+str(t.lineno)+",column "+str(find_column(data,t))
        elif(t.type == 'TokenComentario'):
            pass
        else:
            i = len(t.type) # max 16
            print("token "+t.type+" "*(16-i+3)+"value ("+t.value+") at line "+str(t.lineno)+",column "+str(find_column(data,t)))
else:
    quit()
