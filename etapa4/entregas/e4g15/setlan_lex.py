#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 06/03/2015
#
#proyecto 4 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#Se utiliza la herramienta de PLY: lex,
#
#Analizador lexicografico del lenguaje setlan
#-----------------------------------------------

from ply import *
import sys 

#Se abre el archivo a leer
archivo = open(sys.argv[1],'r')
entrada = archivo.read() 

#listas para almacenar los tokens y/o errores
lista_errores = []
lista_tokens  = []

#Tokens
tokens = ('TokenProgram','TokenUsing','TokenIn','TokenID','TokenPrint','TokenPrintln','TokenInt','TokenBool',
  'TokenSet','TokenFor','TokenIf','TokenThen','TokenElse','TokenRepeat','TokenWhile','TokenDo','TokenComma',
  'TokenOpenCurly','TokenCloseCurly','TokenSemicolon','TokenScan','TokenParenR','TokenParenL','TokenNotequal',
  'TokenPlus','TokenMinus','TokenMultiply','TokenDivide','TokenTrue','TokenFalse','TokenOr','TokenNot','TokenAnd',
  'TokenMinor','TokenGreater','TokenAssign','TokenEquals','TokenString','TokenNumber','TokenMod','TokenMin',
  'TokenUnion','TokenDifference','TokenIntersection','TokenSetplus','TokenSetMinus','TokenSetmultiply','TokenSetdivide',
  'TokenSetmod','TokenMinorequal','TokenGreaterequal','TokenSetgreater','TokenSetminor','TokenSetelements','TokenSetin','TokenMax')

#Palabras reservadas 
reserved = {'program' : 'TokenProgram','using' : 'TokenUsing','in' : 'TokenIn','print' : 'TokenPrint',
  'println' : 'TokenPrintln','for' : 'TokenFor','do' : 'TokenDo','int' : 'TokenInt','bool' : 'TokenBool',
  'set' : 'TokenSet','scan' : 'TokenScan','if' : 'TokenIf','then':'TokenThen','else' : 'TokenElse',
  'while' : 'TokenWhile','repeat' : 'TokenRepeat','true' : 'TokenTrue','false' : 'TokenFalse','or' : 'TokenOr',
  'not' : 'TokenNot','and' : 'TokenAnd','min' : 'TokenMin', 'max' : 'TokenMax'}

#Caracteres 

t_TokenPlus           = r'\+'
t_TokenMinus          = r'\-'
t_TokenMultiply       = r'\*'
t_TokenDivide         = r'/'
t_TokenAssign         = r'\='
t_TokenEquals         = r'\=='
t_TokenComma          = r','
t_TokenSemicolon      = r';' 
t_TokenParenL         = r'\('
t_TokenParenR         = r'\)'
t_TokenMinor          = r'<'
t_TokenGreater        = r'>'
t_TokenMinorequal     = r'<='
t_TokenGreaterequal   = r'>='
t_TokenOpenCurly      = r'{'
t_TokenCloseCurly     = r'}'
t_TokenMod            = r'\%'
t_TokenNotequal       = r'\/='
t_TokenUnion          = r'\+\+'
t_TokenDifference     = r'\\'
t_TokenIntersection   = r'\><'
t_TokenSetplus        = r'\<\+\>'
t_TokenSetMinus       = r'\<\-\>'
t_TokenSetmultiply    = r'\<\*\>'
t_TokenSetdivide      = r'\<\/\>'
t_TokenSetmod         = r'\<\%\>'
t_TokenSetgreater     = r'\>\?' 
t_TokenSetminor       = r'\<\?' 
t_TokenSetelements    = r'\$\?' 
t_TokenSetin          = r'\@'



#Los comentarios y las tabulaciones (los ignora)
t_ignore         = ' \t'
t_ignore_COMMENT = r'\#.*'


#Funcion que ubica la columna donde esta el token
#Retorna el numero de la columna
def column(data,t):
  last = data.rfind('\n', 0, t.lexpos)
  col  = (t.lexpos - last)
  return col

#Funcion que reconoce un salto de linea
def t_TokenNewline(t):
  r'\n+'
  t.lexpos = 0
  t.lexer.lineno += len(t.value)  

#Funcion que reconoce palabras reservadas y ID.
def t_TokenId(t):
  r'[a-zA-Z_][a-zA-Z_0-9]*'
  t.type = reserved.get(t.value,'TokenID')
  return t

#Funcion que reconoce numeros que son de 32 bits.
def t_TokenNumber(t):
  r'\d+'
  t.value = int(t.value)
  if is32(t.value):
    return t
  else:
    lista_errores.append(t)

#Funcion que reconoce los strings.
def t_TokenString(t):
  r'"(\\.|[^"])*"'
  t.value = str(t.value)
  return t

#Manejador de errores.
def t_error(t):
  columna = column(lexer.lexdata,t)
  linea   = t.lineno
  t.lexer.skip(1)
  return t

#Determina si un numero es de 32 bits o no.
def is32(n):
  try:
    bitstring=bin(n)
  except (TypeError, ValueError):
    return False
  if len(bin(n)[2:]) <=32:
    return True
  else:
    return False

#Funcion que imprime la lista de errores.
def imprimir_errores(errores):
  for err in errores:
    columna = column(lexer.lexdata,err)
    if err.type == 'TokenNumber':
      print "Error: Numero mayor que 32 bits: %s " % (str(err.value))
    else:
      print "Error: Se encontro un caracter inesperado \"%s\" en la linea %d, columna %d." % (err.value[0],err.lineno,columna)

#Funcion que imprime la lista de tokens
def imprimir_tokens(tokens):
  for tok in tokens:
    columna = column(lexer.lexdata,tok)
    print "%s('%s',Linea %d,Columna %d)" % (tok.type,tok.value,tok.lineno,column(lexer.lexdata,tok))
  
lexer = lex.lex()
lexer.input(entrada)  

#Se recorre el lexer y se almacenan los tokens y los errores
#y se imprime la lista correspondiente
while True:
  tok = lexer.token()
  if not tok: break
  if tok.type == 'error':
    lista_errores.append(tok)
  else:
    lista_tokens.append(tok)

#if lista_errores != []:
 # imprimir_errores(lista_errores)
#else:
 # imprimir_tokens(lista_tokens)
