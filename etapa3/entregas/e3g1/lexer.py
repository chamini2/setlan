#!/usr/bin/env python
# -*- coding: UTF8 -*-
# ------------------------------------------------------------
# Setlan
#
# Lexer del lenguaje Setlan
# CI-3725
#
# Gustavo Siñovsky 09-11207
# Luiscarlo Rivera 09-11020
# ------------------------------------------------------------

import sys
import ply.lex as lex


# Palabras reservadas
reserved = {
    'program' : 'tkPROGRAM',
    'using' : 'tkUSING',
    'in' : 'tkIN',
    'scan' : 'tkSCAN',
    'print' : 'tkPRINT',
    'println' : 'tkPRINTLN',
    'int' : 'tkINT',
    'bool' : 'tkBOOL',
    'and' : 'tkAND',
    'not' : 'tkNOT',
    'or' : 'tkOR',
    'set' : 'tkSET',
    'true' : 'tkTRUE',
    'false' : 'tkFALSE',
    'if' : 'tkIF',
    'else' : 'tkELSE',
    'min' : 'tkMIN',
    'max' : 'tkMAX',
    'do' : 'tkDO',
    'while' : 'tkWHILE',
    'repeat' : 'tkREPEAT',
    'for' : 'tkFOR',
}

# Lista de nombre de tokens
tokens = [
    'tkID',
    'tkASSIGN',
    'tkPLUS', 'tkTIMES', 'tkMINUS', 'tkDIV', 'tkMOD',
    'tkGREATERTHAN', 'tkLESSTHAN', 'tkLESS', 'tkGREATER', 'tkEQUAL', 'tkNOTEQUAL',
    'tkLPAR', 'tkRPAR',
    'tkLCURLYBRACKET', 'tkRCURLYBRACKET',
    'tkCOMMA',
    'tkSEMICOLON',
    'tkUNION', 'tkDIFFERENCE', 'tkINTERSECTION',
    'tkSETPLUS', 'tkSETTIMES', 'tkSETMINUS', 'tkSETDIV', 'tkSETMOD',
    'tkMAXVALUE', 'tkMINVALUE', 'tkSIZE',
    'tkCONTAINS',
    'tkSTRING', 'tkNUM'
]+ list(reserved.values())



# Expresiones regulares que definen los tokens
t_tkASSIGN = r'\='
t_tkPLUS = r'\+'
t_tkTIMES = r'\*'
t_tkMINUS = r'\-'
t_tkDIV = r'/'
t_tkMOD = r'\%'
t_tkGREATERTHAN = r'\>='
t_tkLESSTHAN = r'\<='
t_tkLESS = r'\<'
t_tkGREATER = r'\>'
t_tkEQUAL = r'\=='
t_tkNOTEQUAL = r'\/='
t_tkLPAR = r'\('
t_tkRPAR = r'\)'
t_tkLCURLYBRACKET = r'{'
t_tkRCURLYBRACKET = r'}'
t_tkCOMMA = r'\,'
t_tkSEMICOLON = r'\;'
t_tkUNION = r'\+\+'
t_tkDIFFERENCE = r'\\'
t_tkINTERSECTION = r'\>\<'
t_tkSETPLUS = r'\<\+\>'
t_tkSETMINUS = r'\<\-\>'
t_tkSETTIMES = r'\<\*\>'
t_tkSETDIV = r'\</\>'
t_tkSETMOD = r'\<\%\>'
t_tkMAXVALUE = r'\>\?'
t_tkMINVALUE = r'\<\?'
t_tkSIZE = r'\$\?'
t_tkCONTAINS = r'@'


# Identificadores
def t_tkID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'tkID') # Chequeo para palabras reservadas
    return t

# Strings
def t_tkSTRING(t):
    r'"([^\\"\n]|\\["n\\])*"'
    str = t.value[1:-1]
    return t

# Números
def t_tkNUM(num):
    r'\d+(?![a-zA-Z_])'
    num.value = int(num.value)
    if (num.value > 2147483647 or num.value < -2147483648):
        t_error(num)
    return num

# Manejador de comentarios
def t_tkCOMMENT(t):
    r'\#.*'
    pass

# Numero de líneas
def t_line(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejador de columnas
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    return column    

# Caracter a ignorar
t_ignore = ' \t'