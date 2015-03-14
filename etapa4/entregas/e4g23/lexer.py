#!/usr/bin/python
import ply.lex as lex, sys
    
reserved = {
    'program' : 'Program',
    'or' : 'Or',
    'not' : 'Not',
    'and' : 'And',
    'using' : 'Using',
    'int' : 'Int',
    'scan' : 'Scan',
    'print' : 'Print',
    'println' : 'Println',
    'in' : 'In',
    'if' : 'If',
    'else' : 'Else',
    'true' : 'True',
    'false' : 'False',
    'bool' : 'Bool',
    'max' : 'Max',
    'min' : 'Min',
    'for' : 'For',
    'do' : 'Do',
    'return' : 'Return',
    'def' : 'Def',
    'repeat' : 'Repeat',
    'while' : 'While',
    'set' : 'Set'
    }

tokens = ['ID','OpenCurly','CloseCurly','Colon','OpenParen','CloseParen',
          'String','LessThan','GreaterThan','LessThanEq','GreaterThanEq',
          'Equals','Comma','Assign','Plus','Comment','NotEquals','Contains',
          'Len','PlusSet','MinusSet','TimesSet','DivSet','ModSet','Union',
          'MaxSet','MinSet','Difference','Intersect','Minus','Times','Div',
          'Mod','Number','Arrow','SemiColon'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
def t_LessThanEq(t):
    r'<='
    return t
def t_GreaterThanEq(t):
    r'>='
    return t
def t_Equals(t):
    r'=='
    return t
def t_PlusSet(t):
    r'<\+>'
    return t
def t_MinusSet(t):
    r'<->'
    return t
def t_TimesSet(t):
    r'<\*>'
    return t
def t_DivSet(t):
    r'</>'
    return t
def t_ModSet(t):
    r'<%>'
    return t
def t_MaxSet(t):
    r'>\?'
    return t
def t_MinSet(t):
    r'<\?'
    return t
def t_Union(t):
    r'\+\+'
    return t
def t_Intersect(t):
    r'><'
    return t
def t_Arrow(t):
    r'->'
    return t
def t_Number(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_String(t):
    r'"(?:[^"\\]|\\.)*"'

    if t.value.count('\n') > 0:
        taux = t
        taux.value = '\n'     
        t_error(taux)

    while t.value.count('\\n') > 0 :
        if t.value.count('\\n') > 0:
            aux = t.value.find('\\n')
            t.value = t.value[:aux] + '\n' + t.value[aux+2:] 

    while t.value.count(r'\"') > 0 :
        if t.value.count(r'\"') > 0:
            t.value = t.value[:t.value.find(r'\"')] + t.value[t.value.find(r'\"')+1:]
    aux = t.value.count(r'\\')
    while aux > 0 :
        if t.value.count(r'\\') > 0:
            t.value = t.value[:t.value.find(r'\\')] + t.value[t.value.find(r'\\')+1:]
            aux = aux - 1 
    return t


t_Colon = r':'
t_Difference = r'\\'
t_OpenCurly = r'\{'
t_CloseCurly = r'\}'
t_SemiColon = r';'
t_OpenParen = r'\('
t_CloseParen = r'\)'
t_LessThan = r'<'
t_GreaterThan = r'>'
t_Comma = r','
t_Assign = r'='
t_Plus = r'\+'
t_NotEquals = r'/='
t_Contains = r'@'
t_Len = r'\$\?'
t_Minus = r'-'
t_Times = r'\*'
t_Div = r'/'
t_Mod = r'%'


def t_newline(t): 
    r'\n+'
    global current_column
    t.lexer.lineno += t.value.count("\n")
    t.lexer.current_column = t.lexer.lexpos - 1

# Ignored characters 
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

# Global variables to return information
lexing_errors = ''

def t_error(t):
    global lexing_errors
    if t.value[0] == '\n':
        lexing_errors += 'Error: Se encontro un salto de Linea inesperado en la Linea '+str(t.lexer.lineno)+', Columna '+str(t.lexer.lexpos - t.lexer.current_column)+'.\n'
    else:    
        lexing_errors += 'Error: Se encontro un caracter inesperado "'+t.value[0]+'" en la Linea '+str(t.lexer.lineno)+', Columna '+str(t.lexer.lexpos - t.lexer.current_column)+'.\n'
    t.lexer.skip(1)

    
lexing_errors = ''

def mainLexer(arg):
    global lexing_errors, lexer
    lexer = lex.lex()
    lexer.current_column = -1
    lexer.input(open(arg,'r').read())
    return_message, lexing_errors = '', ''

    for t in iter(lexer.token, None):
        return_message += 'Token'+t.type+(': '+str(t.value) if t.type=='ID' or t.type=='String' or t.type=='Number' else '')+' (Linea '+str(t.lineno)+', Columna '+str(t.lexpos - lexer.current_column)+')\n'
    
    return return_message if len(lexing_errors) == 0 else lexing_errors
    
    
if __name__ == '__main__':
    print(mainLexer(sys.argv[1]))
    
