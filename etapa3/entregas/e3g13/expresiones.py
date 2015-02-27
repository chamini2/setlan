# -*- coding: utf-8 -*-'''
'''
Created on 19/1/2015

@author: Manuel Gonzalez 11-10390
         Jonathan Ng 11-10199
    
    Expresiones dadas al lexer para reconocer los tokens de setlan
'''
import ply.lex as lex

lexer_errors  = []
# Palabras reservadas
reservadas = {
   'program':'PROGRAM',
   'using'  : 'USING' ,
   'in'     : 'IN',
   'if'     : 'IF',
   'else'   : 'ELSE' ,
   'for'    : 'FOR'  ,
   'do'     : 'DO' ,
   'min'    : 'MIN',
   'max'    : 'MAX',
   'repeat' : 'REPEAT',
   'while'  : 'WHILE'  ,
   'and'    : 'AND'  ,
   'or'     : 'OR'   ,
   'not'    : 'NOT'  ,
   'false'  : 'FALSE',
   'true'   : 'TRUE' ,
   'scan'   : 'SCAN' ,
   'print'  : 'PRINT',
   'println': 'PRINTLN',
   'int'    : 'INT'  , 
   'set'    : 'SET'  ,
   'bool'   : 'BOOL' 
}


simbolos = {
   '{' :'LCURLY',
   '}' :'RCURLY',
   ';' :'SEMICOLON',
   ',' :'COMMA',
   '=' :'ASSIGN',
   '*' :'TIMES',
   '+' :'PLUS',
   '-' :'MINUS',
   '/' :'INTDIVISION',
   '%' :'RESTDIVISION',
   '\\':'COUNTERSLASH',
   '<' :'LESSTHAN',
   '>' :'GREATERTHAN',
   '@' :'BELONG',
   '(' :'LPARENT',
   ')' :'RPARENT'
}

op_mapeados = {
   '<+>':'MAPPLUS',
   '<->':'MAPMINUS',
   '<*>':'MAPTIMES',
   '</>':'MAPDIVIDE',
   '<%>':'MAPREST',
}

unarios_conjuntos = {
   '>?' :'MAXVALUESET',
   '<?' :'MINVALUESET',
   '$?' :'SIZESET',
}

simbolos_igual = {
   '<=' :'LESSOREQUALTHAN',
   '>=' :'GREATEROREQUALTHAN',
   '==' :'EQUALBOOL',
   '/=' :'UNEQUAL',
}

tokens = ['IDENTIFIER', 'INTEGER','DOUBLEPLUS','STRING','INTERSECCION']  + reservadas.values() + \
         simbolos.values() + op_mapeados.values()  + \
         unarios_conjuntos.values() + simbolos_igual.values()


t_ignore = ' \t'

def t_STRING(t):
    r'"[^"\\\r\n]*(?:\\.[^"\\\r\n]*)*"'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z\d_]*'    
    valor = reservadas.get(t.value,'IDENTIFIER')
    t.type = valor    # Check for reserved words
    return t

def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_MAPEADO(t):
    r'<[\+\-\*/%]>'
    valor = op_mapeados[t.value]
    t.type = valor
    return t

def t_INTERSECCION(t):        
    r'><'
    return t

def t_SIMBOLOS_CON_IGUAL(t):
    r'[><=/]='
    valor = simbolos_igual[t.value]
    t.type = valor
    return t
    
def t_UNARIO_CONJUNTO(t):
    r'[<>\$]\?'
    valor = unarios_conjuntos[t.value]
    t.type = valor
    return t

def t_DOUBLEPLUS(t):
    r'\+\+'
    return t

def t_SIMBOLO(t):
    r'[{};,=\*\+\-/%\\<>@\(\)]'
    valor = simbolos[t.value]
    t.type = valor
    return t

def t_COMMENTARIO(t):
    r'\#.*'
    pass

def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Encuentra la columna 
#     token instancia del token    
def obtener_columna(token):
    'Encuentra la columna del token'
    
    return obtener_columna_texto_lexpos(token.lexpos,token.lexer.lexdata)

# Encuentra la columna segun un lexpos
#     token instancia del token    

cont_archivo = None
def obtener_columna_texto_lexpos(lexpos,texto = None):
    'Encuentra la columna de u token dado su texto y su lexpos'    
    if cont_archivo is None: return
    
    if texto is None:
        ultimo_salto = cont_archivo.rfind('\n',0,lexpos)  # ultima posicion del salto de linea
    else:
        ultimo_salto = texto.rfind('\n',0,lexpos)  # ultima posicion del salto de linea
        
    if ultimo_salto < 0:
        ultimo_salto = -1
        
    columna = lexpos - ultimo_salto
    
    return columna

# Manejador de errores
def t_error(t):
    global lexer_errors
    mensage = "Error: se encontro  un caracter inesperado '%s' en la linea %d, Columna %d."
    datos = (t.value[0],t.lineno,obtener_columna(t))
    t.lexer.skip(1)
    if t.value[0] == '\r': return
    lexer_errors.append(mensage % datos)

def print_tokens(lexer,input):
    lexer.input(input)
    tokens = []
    for token in lexer:
        tokens.append(token)
    
    for token in tokens:
        print 'token',token.type,' '*(20 - len(token.type)),
        print "value (" + str(token.value) + ") at line ",token.lineno,\
             ", column " , obtener_columna(token)
             
def build_lexer():
    lexer = lex.lex()
    return lexer