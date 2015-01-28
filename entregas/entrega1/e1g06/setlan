#!/usr/bin/env python

#######################################
# CI3715 Traductores e Interpretadores
# Entrega 1. Grupo 6
# Maria Victoria Jorge 11-10495
# Enrique Iglesias 11-10477
#######################################

import ply.lex as lex
import sys

# Palabras reservadas del lenguaje
reserved = {
    # Lenguaje
    'program' : 'Program',
    'using' : 'Using',
    'in' : 'In',

    # Condicionales
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',

    # Ciclos
    'for' : 'FOR',
    'min' : 'MIN',
    'max' : 'MAX',
    'repeat' : 'REPEAT',
    'while' : 'WHILE',
    'do' : 'DO',

    # E/S
    'scan' : 'Scan',
    'print' : 'Print',
    'println' : 'Println',

    # Tipos
    'int' : 'Int',
    'bool' : 'Boolean',
    'set' : 'Set',

    # Operadores Logicos
    'and' : 'And',
    'or' : 'Or',
    'not' : 'Not',

    # Valores Booleanos
    'true' : 'True',
    'false' : 'False'
}

# Tokens que se pueden reconocer
tokens = [
    # Identificadores
    'ID',

    # Operadores de mapeo
    'PlusMap',
    'MinusMap',
    'TimesMap',
    'DivideMap',
    'ModuleMap',

    # Cadena de caracteres
    'String',

    # Operadores de conjuntos
    'Union',
    'Intersection',
    'Diference',
    'MinSet',
    'MaxSet',
    'Size',
    'At',

    # Operadores relacionales
    'Less',
    'Greater',
    'GreaterEqual',
    'LessEqual',
    'Equals',
    'NotEqual',

    # Lenguaje
    'Number',
    'Comma',
    'Assign',
    'Semicolon',
    'OpenCurly',
    'CloseCurly',
    'Colon',
    'Rparen',
    'Lparen',

    # Operadores de enteros
    'Plus',
    'Minus',
    'Times',
    'Divide',
    'Module'
] + list(reserved.values())


def t_ID(t):
    r'[_A-Za-z]([_A-Za-z0-9])*'
    t.type = reserved.get(t.value,'ID')
    return t

t_PlusMap = r'<\+>'
t_MinusMap = r'<->'
t_TimesMap = r'<\*>'
t_DivideMap = r'</>'
t_ModuleMap = r'<%>'
t_String = r'"([^"\\]|\\"|\\\\|\\n)*"'
t_Union = r'\+\+'
t_Intersection = r'><'
t_Diference = r'\\'
t_MaxSet = r'>\?'
t_MinSet = r'<\?'
t_Size = r'\$\?'
t_At = r'@'
t_Less = r'>'
t_Greater = r'<'
t_GreaterEqual = r'>='
t_LessEqual = r'<='
t_Equals = r'=='
t_NotEqual = r'/='

# Retorna el valor de un numero usando el tipo int de Python
def t_Number(t):
    r'\d+'
    t.value = int(t.value)    
    return t

t_Comma = r','
t_Assign = r'='
t_Semicolon = r';'
t_OpenCurly = r'\{'
t_CloseCurly = r'\}'
t_Colon = r':'
t_Lparen = r'\('
t_Rparen  = r'\)'
t_Plus    = r'\+'
t_Minus   = r'-'
t_Times   = r'\*'
t_Divide  = r'/'
t_Module = r'%'


# Funcion para realizar un seguimiento de los numeros de linea. El unico caracter
# valido para el salto de linea es '\n'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
# Ignora tabs, espacios y comentarios (estilo Python)
t_ignore  = ' \t'
t_ignore_comments  = r'\#.*'

# Permite encontrar el numero de columna de la linea actual
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column
        
# Manejo de errores en caso de encontrar un caracter invalido
def t_error(t):
    error.append(t)
    t.lexer.skip(1)

if __name__ == '__main__':

    # Variable global donde se almacenan los errores en caso de existir
    global error
    error = []
    tokList = []
    lexer = lex.lex()

    if (len(sys.argv) != 2):
        sys.exit(1)

    myfile = open(sys.argv[1], "r")
    lexer.input(myfile.read())
    
    while True:
        tok = lexer.token()
        if not tok: break
        tokList.append(tok)

    if (len(error) != 0):
        for aux in error :
            print 'Error: Se encontro un caracter inesperado "' + str(aux.value[0]),
            print '" en la Linea ' + str(aux.lineno) +' ,Columna ',
            print str(find_column(lexer.lexdata,aux))
    else:
        for aux in tokList:
            if (aux.type == 'ID') or (aux.type == 'String') or (aux.type == 'Number'):
                print 'Token' + str(aux.type) +': "' +str(aux.value)+'"(Linea ',
                print  str(aux.lineno) +', Columna '+ str(find_column(lexer.lexdata,aux))+')'
            else:
                print 'Token'+str(aux.type)+'(Linea ' + str(aux.lineno) +', Columna ',
                print str(find_column(lexer.lexdata,aux))+')'
    myfile.close()