'''
Created on 21/1/2015

@author: David Klie
@author : Gustavo Benzecri
'''
import sys
# Todos los posibles tokens del lenguaje Setlan
lex_error=[]
tokens = [
'BLOCK',
'IDENTIFIER',
'COMMA',
'PLUS',
'SEMICOLON',
'EQUALS',
'NOTEQUALS',
'END_BLOCK',
'ARROBA',
'MINUS',
'TIMES',
'DIVIDE',
'MOD',
'GREATERTHAN',
'LESSTHAN',
'GREATEREQUALTHAN',
'LESSEQUALTHAN',
'UNION',
'INTERSECTION',
'DIFFERENCE',
'SETPLUS',
'SETMINUS',
'SETTIMES',
'SETDIV',
'SETMOD',
'MAXSET',
'MINSET',
'CARDINALITY',
'LPAREN', 
'RPAREN',
'ASSIGN',
'INTEGER',
'STRING'
]

# Definicion de las expresiones regulares para los tokens sencillos   
t_BLOCK=r'\{'
t_COMMA=r'\,'
t_PLUS=r'\+'
t_SEMICOLON=r'\;'
t_EQUALS=r'\=\='
t_NOTEQUALS=r'/\='
t_END_BLOCK= r'\}'
t_ARROBA = r'\@'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'\%'
t_GREATERTHAN= r'\>'
t_LESSTHAN = r'\<'
t_GREATEREQUALTHAN = r'\>\='
t_LESSEQUALTHAN= r'<='
t_UNION= r'\+\+'
t_INTERSECTION = r'\>\<'
t_DIFFERENCE = r'\\'
t_SETPLUS= r'\<\+\>'
t_SETMINUS= r'\<-\>'
t_SETTIMES= r'\<\*\>'
t_SETDIV= r'\</\>'
t_SETMOD = r'\<\%\>'
t_MAXSET = r'\>\?'
t_MINSET = r'\<\?'
t_CARDINALITY = r'\$\?'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ASSIGN = r'\='
t_STRING = r'\"([^\"\\\n]|\\\\|\\"|\\t|\\r|\\s|\\r|\\f|\\b|\\a)*\"'
t_ignore = r' '

# Se deben consideras palabras reservadas como tokens tambien.     
reserved = {
'scan' : 'SCAN',
'bool' : 'BOOL',
'int' : 'INT',
'set' :  'SET',
'false' : 'FALSE',
'true' : 'TRUE',
'if' : 'IF',
'else' : 'ELSE',
'for': 'FOR',
'repeat' : 'REPEAT',
'while' : 'WHILE',
'do' : 'DO',
'or' : 'OR',
'and' : 'AND',
'not' : 'NOT',
'using' : 'USING',
'program': 'PROGRAM',
'print' : 'PRINT',
'println' : 'PRINTLN',
'in' : "IN",
'min' : 'MIN',
'max' : "MAX"
}
    
tokens+= list(reserved.values())

def find_column(input,token): # Calculo de columnas
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = (token.lexpos - last_cr) 
    return column
    
def t_IDENTIFIER(t): # Aqui se hace distincion entre palabras reservadas y posibles variables
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value,'IDENTIFIER')  # Es una palabra reservada (?)
    return t

def t_INTEGER(t): # Se procesa el string que represente un numero aqui.
    r'\d+'
    t.value=int(t.value)
    return t

def t_newline(t): # Conteo de lineas
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_Comment(t): # Los comentarios terminan con un salto de linea. 
    r'\#.*'
    pass

def t_error(t): # Los simbolos que no esten contemplados en el lenguaje generan error
    msj_err= "Error: Se encontro un caracter inesperado \'%s\' en la Linea %d,Columna %d"
    msj_err= msj_err % (t.value[0],t.lexer.lineno,find_column(t.lexer.lexdata,t))
    lex_error.append(msj_err)
    t.lexer.skip(1)

def t_TAB(t): # Las tabulaciones no deben ser consideradas
    r'\t'
    pass


        
