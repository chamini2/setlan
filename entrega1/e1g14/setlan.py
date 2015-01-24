
#CI3725
#Entrega 1 Grupo 14
#Angel Franco 07-40913
#Maria Lourdes Garcia 10-10264


#!/usr/bin/env python
import ply.lex as lex

#Palabras reservadas de setlan

reserved = {

    'program': 'PROGRAM',
    'using': 'USING',
    'in': 'IN',

    #tipos
    'int' : 'INT',
    'bool' : 'BOOL',
    'set' : 'SET',

    #valores
    'true': 'TRUE',
    'false': 'FALSE',

    #ciclos
    'do': 'DO',
    'while': 'WHILE',
    'for': 'FOR',
    'repeat': 'REPEAT',

     #condicionales
    'if' : 'IF',
    'else': 'ELSE',

    #expresiones y operadores
    'or': 'OR',
    'and': 'AND',
    'not': 'NOT',
    'min': 'MIN',
    'max': 'MAX',

    #entrada y salida
    'scan': 'SCAN',
    'print': 'PRINT',
    'println': 'PRINTLN',

}

#Tokens a ser encontrados
tokens = [
    'SEMICOLON',
    'COMMA',
    'ASSIGN',
    'NUMBER',
    'STRING',
    #identificadores
    'ID',
    #expresiones/operadores
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULE',
    'LPAREN',
    'RPAREN',
    'LCURLY',
    'RCURLY',
    'LESS',
    'LESSEQ',
    'GREAT',
    'GREATEQ',
    'EQUAL',
    'NOTEQUAL',
    'SETUNION',
    'SETINTERSECT',
    'SETDIFF',
    'SETCONTENTION',
    'MAPSUM',
    'MAPDIFF',
    'MAPTIMES',
    'MAPDIVIDE',
    'MAPMODULE',
    'SETMAX',
    'SETMIN',
    'SETSIZE',

] + list(reserved.values())

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_COMMA = r','
t_ASSIGN = r'='
t_SEMICOLON = r';'

def t_ID(t):
    r'\w[\w\d]*'
    #Si no es palabra reservada y cumple con las condiciones, es un ID
    t.type = reserved.get(t.value, 'ID')
    return t

t_STRING = r'".*?"'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'
t_SETUNION = r'\+\+'
t_PLUS = r'\+'
t_MINUS = r'-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RCURLY =  r'}'
t_LCURLY = r'{'
t_SETMAX = r'>\?'
t_SETMIN = r'<\?'
t_SETSIZE = r'\$\?'
t_SETINTERSECT = r'><'
t_MAPSUM = r'<\+>'
t_MAPDIFF = r'<->'
t_MAPTIMES = r'<\*>'
t_MAPDIVIDE = r'</>'
t_MAPMODULE = r'<%>'
t_LESS = r'<'
t_LESSEQ = r'<='
t_GREAT = r'>'
t_GREATEQ = r'>='
t_EQUAL = r'=='
t_NOTEQUAL = r'/='
t_SETDIFF = r'\\'
t_SETCONTENTION=r'@'

#Ignorar espacios y comentarios
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

#Encontrar el numero de columna
def find_column(text,token):
    last_char = text.rfind('\n',0,token.lexpos)
    if last_char < 0:
        last_char = -1
    column = token.lexpos - last_char
    return column

#salto de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

#Error que se muestra para caracteres inesperados
def t_error(t):
    lista_errores.append("Error: Se encontro un caracter inesperado '%s' en la linea %d, columna %d"
                       % (t.value[0], t.lineno, find_column(lexer.lexdata, t)))
    t.lexer.skip(1)

#Se pasa el archivo por el lexer
def lexear(archivo):

    global lista_errores, lexer

    lexer = lex.lex()
    tokens_list = []
    lista_errores = []

    lexer.input(archivo)


    for tok in lexer:
        tokens_list.append(tok)

    #Si no hay ningun caractger inesperado:
    if not lista_errores:
        return tokens_list
    else:
        #De lo contrario imprimir todoslos caracteres inesperados
        for error in lista_errores:
            print error

        #y retornar lista vacia porq hubo errores
        return []

def main(argv = None):

    import sys

    if argv is None:
        argv = sys.argv
    #abrir archivo
    archivo = open(argv[1], 'r')
    #leer archivo y pasarselo al Lexer
    tokens_list = lexear(archivo.read())
    for tok in tokens_list:
        print 'token(' + str(tok.type) + ')',
        print 'value(' + str(tok.value) + ')',
        print 'at line ' + str(tok.lineno) + ',',
        print 'column ' + str(find_column(lexer.lexdata, tok))


if __name__ == "__main__":
    main()