#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################
#  Proyecto I - CI3725     #
#  Grupo 2                 #
#  Luis Colorado 09-11086  #
#  Nicolas Manan 06-39883  #
############################



import ply.lex as lex

# Palabras reservadas del lenguaje
reserved = {
    
    # Del lenguaje
    'program' : 'TokenProgram',
    'using'   : 'TokenUsing',
    'scan'    : 'TokenScan',
    'print'   : 'TokenPrint',
    'println' : 'TokenPrintln',

    # Tipos de datos
    'int'   : 'TokenInt',
    'set'   : 'TokenSet',
    'bool'  : 'TokenBool',

    # Booleanos
    'true'  : 'TokenTrue',
    'false' : 'TokenFalse',

    # -------
    'in'      : 'TokenIn',

    # Condicionales
    'if'   : 'TokenIf',
    'else' : 'TokenElse',

    # Ciclos
    'do'    : 'TokenDo',
    'while' : 'TokenWhile',
    'repeat': 'TokenRepeat',
    'for'   : 'TokenFor',

    # Operadores
    'or'  : 'TokenOr',
    'and' : 'TokenAnd',
    'not' : 'TokenNot',
    'min' : 'TokenMin',
    'max' : 'TokenMax',

}

# Tokens a reconocer
tokens = [
    

    # Identificador
    'TokenID',

    # Operadores
    'TokenNumber',
    'TokenComma',
    'TokenAssign',
    'TokenSemicolon',
    'TokenOpenCurly',
    'TokenCloseCurly',
    'TokenString',
    'TokenPlus',
    'TokenMinus',
    'TokenTimes',
    'TokenDivide',
    'TokenModule',
    'TokenLParen',
    'TokenRParen',
    'TokenIntersection',
    'TokenLess',
    'TokenLesseq',
    'TokenGreat',
    'TokenGreateq',
    'TokenEqual',
    'TokenUnequal',
    'TokenUnion',
    'TokenSubset',
    'TokenMinValue',
    'TokenMaxValue',
    'TokenNumberElements',
    'TokenMinusMap',
    'TokenPlusMap',
    'TokenDivideMap',
    'TokenTimesMap',
    'TokenModuleMap'
] + list(reserved.values())

# Devuelve el valor actual del tipo entero
def t_TokenNumber(t):
    r'\d+'
    valor = int(t.value)
    if valor > 2147483648:
        error_TokenNumber(t)

    t.value = valor
    return t


# Si no coinciden con las palabras reservadas,
# entonces es identificador
def t_TokenID(t):
    r'\w[\w\d]*'
    t.type = reserved.get(t.value, 'TokenID')
    return t

# Definiendo los simbolos
t_TokenComma = r','
t_TokenAssign = r'='
t_TokenSemicolon = r';'
t_TokenString = r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'
t_TokenOpenCurly = r'{'
t_TokenCloseCurly = r'}'
t_TokenPlus = r'\+'
t_TokenMinus = r'-'
t_TokenTimes = r'\*'
t_TokenDivide = r'/'
t_TokenModule = r'%'
t_TokenLParen = r'\('
t_TokenRParen = r'\)'
t_TokenIntersection = r'><'
t_TokenLess = r'<'
t_TokenLesseq = r'<='
t_TokenGreat = r'>'
t_TokenGreateq = r'>='
t_TokenEqual = r'=='
t_TokenUnequal = r'/='
t_TokenUnion = r'\+\+'
t_TokenMinValue = r'<\?'
t_TokenMaxValue = r'>\?'
t_TokenNumberElements = r'\$\?'
t_TokenPlusMap = r'<\+>'
t_TokenMinusMap = r'<->'
t_TokenTimesMap = r'<\*>'
t_TokenDivideMap = r'</>'
t_TokenModuleMap = r'<%>'
t_TokenSubset = r'@'

# Comentarios, espacios y tabuladores son ignorados
t_ignore = " \t"
t_ignore_COMMENT = r'[#].*'

# El salto de linea se considera
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Funcion que busca el numero de la columna y linea
# actual
def find_column(text,token):
    last_cr = text.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

lex.lex()
lexer_error = []

# Funcion que muestar el Error si se encuentra un caracter
# inesperado en el programa y su ubicacion en fila y columna
def t_error(t):
    text = t.lexer.lexdata
    message = "ERROR: Se encontro un caracter inesperado \"%s\" en la linea %d, columna %d"
    data = (t.value[0], t.lineno, find_column(text, t))
    lexer_error.append(message % data)
    t.lexer.skip(1)

def error_NUMBER(token):
    text = token.lexer.lexdata
    message = "ERROR: Overflow for int '%s' at line %d, column %d"
    data = (token.value, token.lineno, find_column(text, token))
    lexer_error.append(message % data)

# Funcion que a traves del lexer toma el archivo a ser leido 
# y devuelve la lista de tokens
def lexing(file_string, debug=0):

    lexer = lex.lex()
    tokens_list = []

    lexer.input(file_string)

    for tok in lexer:
        tokens_list.append(tok)

    if not lexer_error:
        return tokens_list
    else:

        for error in lexer_error:
            print error

        return []

# Modulo main
def main(argv = None):
    import sys    # argv, exit

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No encuentra el archivo"
        sys.exit() #return
    elif len(argv) > 3:
        print "ERROR: Numero invalido de argumentos"
    
    if len(argv) == 3:
        debug = argv[2]
    else:
        debug = 0

    # Abre el archivo a interpretar
    file_string = open(argv[1], 'r').read()

    # Lee el archivo que se le esta pasando a Lexer
    tokens_list = lexing(file_string, debug)

    for tok in tokens_list:
        print 'tok(' + str(tok.type) + ')' + '            '[:-(len(tok.type))],
        print 'val(' + str(tok.value) + ')',
        print 'at line ' + str(tok.lineno) + ',',
        print 'column ' + str(find_column(file_string, tok))

# Modulo para correr el programa
if __name__ == "__main__":
    main()