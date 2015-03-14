#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Autor: Jose Daniel Duran Toro
Carnet: 10-10222
'''
import lex
import sys

errores = False

def find_column(input,token):#encuentra numero de columna del token
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    if token.lineno>1:
        column-=1
    return column

def t_TokenID(t): #detecta los tokenid y los diferencia de las palabras reservadas
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'TokenID')
    return t

def t_TokenNumber(t):
    r'\d+'
    t.value = int(t.value)    
    global errores
    global errdata
    if (int(t.value)>2147483647):
        errores = True
        print u"Error: Overflow \"%s\" en la Línea %i, Columna %i." % (t.value, t.lineno, find_column(errdata,t))
        t.lexer.skip(1)
    return t

def t_newline(t): #cuenta las nuevas lineas
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    global errores
    global errdata
    errores = True
    print "Error: Se encontró un caracter inesperado \"%s\" en la Línea %i, Columna %i." % (t.value[0], t.lineno, find_column(errdata,t))
    t.lexer.skip(1)

def imprime_tokens(tokens, data):#imprime los tokens
    print "Tokens:\n\n"
    for t in tokens:
        if(t.type == 'TokenComentario'):
            pass
        else:
            i = len(t.type) # max 16
            print "token "+t.type+" "*(16-i+3)+"value ("+str(t.value)+") at line "+str(t.lineno)+", column "+str(find_column(data,t))

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

t_TokenString = r'"([^\\"\n]|(\\")|(\\n)|(\\\\))*"'
t_ignore_TokenComentario = r'\#.*'
t_TokenOpenCurly = r'{'
t_TokenCloseCurly = r'}'
t_TokenOpenParent = r'\('
t_TokenCloseParent = r'\)'
t_TokenSetSuma = r'<\+>'
t_TokenSetResta = r'<->'
t_TokenSetMult = r'<\*>'
t_TokenSetEnterDiv = r'</>'
t_TokenSetResto = r'<%>'
t_TokenSetMax = r'>\?'
t_TokenSetMin = r'<\?'
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
t_TokenComma = r','
t_TokenSemicolon = r';'
t_TokenAsing = r'='

reserved = {
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

t_ignore  = ' \t'
errdata = ''

def setlanLexer(data):#devuelve una lista con los tokens encontrados en el archivo
    global errdata
    errdata = data
    lexer = lex.lex()
    tokens = []
    lexer.input(data)
    while True: #en este loop se guardan todos los tokens en una lista
        tok = lexer.token()
        if not tok: break
        tokens+=[tok]
    global errores
    if(not errores):
        #if (flags["-t"]):
        #    imprime_tokens(tokens, data)#para imprimir los tokens
        return tokens
    else:
        quit()