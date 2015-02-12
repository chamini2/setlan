#!/usr/bin/python
'''
Created on 21/1/2015

@author: Emmanuel De Aguiar     10-10179
@author: Daniel Pelayo          10-10539

'''
import re
import lex
import sys

#Lista usada para guardar los errores (caracteres inesperados), si los hay
listaErrores = []

#Lista usada para guardar los tokens encontrados
tokensEncontrados=[]

#diccionario que contiene todas las palabras reservadas dl lenguaje
palabrasReservadas = {'program' : 'TokenProgram',#
                      'using'   : 'TokenUsing'  ,#
                      'scan'    : 'TokenScan'   ,#  
                      'int'     : 'TokenInt'    ,#
                      'bool'    : 'TokenBool'   ,#
                      'set'     : 'TokenSet'    ,#
                      'print'   : 'TokenPrint'  ,#
                      'println' : 'TokenPrintLn',#
                      'if'      : 'TokenIf'     ,#
                       #'then'    : 'TokenThen'   ,#
                      'else'    : 'TokenElse'   ,#
                      'for'     : 'TokenFor'    ,#
                      'do'      : 'TokenDo'     ,#
                      'repeat'  : 'TokenRepeat' ,#
                      'while'   : 'TokenWhile'  ,#
                      'min'     : 'TokenMin'    ,#
                      'max'     : 'TokenMax'    ,#
                       #'def'     : 'TokenDef'    ,#
                       #'return'  : 'TokenReturn' ,#
                      'true'    : 'TokenTrue'   ,#
                      'false'   : 'TokenFalse'  ,#
                      'and'     : 'TokenAnd'    ,#
                      'or'      : 'TokenOr'     ,#
                      'not'     : 'TokenNot'    ,#
                      'in'      : 'TokenIn',     #
                      }

#Lista que contiene todos los tokens del lenguaje
tokens = ['TokenMas'          ,#
          'TokenMenos'        ,#
          'TokenMult'         ,#
          'TokenDiv'          ,#
          'TokenResto'        ,#
          'TokenUnion'        ,#
          'TokenDif'          ,#
          'TokenIntersec'     ,#
          'TokenMapMas'       ,#
          'TokenMapMenos'     ,#
          'TokenMapMult'      ,#
          'TokenMapDiv'       ,#
          'TokenMapResto'     ,#
          'TokenValorMax'     ,#
          'TokenValorMin'     ,#
          'TokenNumElem'      ,#
          'TokenMayor'        ,#
          'TokenMenor'        ,#
          'TokenMayorIgual'   ,#
          'TokenMenorIgual'   ,#
          'TokenEquivalente'  ,#
          'TokenDesigual'     ,#
          'TokenContencion'   ,#
          'TokenParentesisDer',#
          'TokenParentesisIzq',#
          'TokenLlaveDer'     ,#
          'TokenLlaveIzq'     ,#
          'TokenPuntoComa'    ,#
          'TokenComa'         ,#
          'TokenID'           ,#
          'TokenString'       ,#
          'TokenAsignacion'   ,#
          'TokenNumero'        #
          ] + list(palabrasReservadas.values())
          
t_TokenMas          = r'\+'
t_TokenMenos        = r'-'
t_TokenMult         = r'\*'
t_TokenDiv          = r'\/'
t_TokenResto        = r'%'
t_TokenUnion        = r'\+\+'
t_TokenDif          = r'\\'
t_TokenIntersec     = r'><'
t_TokenMapMas       = r'<\+>'
t_TokenMapMenos     = r'<->'
t_TokenMapMult      = r'<\*>'
t_TokenMapDiv       = r'<\/>'
t_TokenMapResto     = r'<%>'
t_TokenValorMax     = r'>\?'
t_TokenValorMin     = r'<\?'
t_TokenNumElem      = r'\$\?'
t_TokenMayor        = r'>'
t_TokenMenor        = r'<'
t_TokenMayorIgual   = r'>='
t_TokenMenorIgual   = r'<='
t_TokenEquivalente  = r'=='
t_TokenDesigual     = r'\/='
t_TokenContencion   = r'@'
t_TokenParentesisDer = r'\)'
t_TokenParentesisIzq = r'\('
t_TokenLlaveDer     = r'}'
t_TokenLlaveIzq     = r'{'
t_TokenPuntoComa    = r';'
t_TokenComa         = r','
t_TokenAsignacion   = '='
t_ignore            = ' \t'
    
def t_COMMENT(t):
    r'\#.*'
    pass
def t_TokenID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palabrasReservadas.get(t.value,'TokenID')
    return t
def t_TokenString(t):
    r'\"(?:[^"\\]|\\.)*"|".*\\n".*"|".*\\/.*"|"[^"]*"'
    #t.value = str(t.value)
    return t
def t_TokenNumero(t):
    r'\d+'
    valor = int(t.value)
    if valor > 2147483648:
        t_error(t)

    t.value = valor  
    return t
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
        column = (token.lexpos - last_cr)+1
        return column
    column = (token.lexpos - last_cr)
    return column

def t_error(t):
    listaErrores.append(t)
    t.lexer.skip(1)

def analisisLexicoGrafico(entrada):
    
    try:
    
        #Se abre el archivo de entrada
        arch = open(entrada)
         
        #Leemos el archivo y lo almacenamos en programa para luego analizarlo lexicograficamente
        programa = arch.read()
        
        #Construccion del LEXER
        lexer = lex.lex()    
        lexer.input(programa)
        
        #Ciclo que ira consiguiendo los tokens en el archivo de entrada
        #mientras los va encontrando los almacena en la lista de tokens
        while True:
            Tokens = lexer.token()
            if not Tokens: 
                break
            tokensEncontrados.append(Tokens)
        
        #Se cierra el archivo de entrada
        arch.close()
        
    except IOError:
        
        print 'El archivo <%s> no puede ser abierto' %entrada
        exit()
    
    
    #Impresion por pantalla de la salida esperada
    #En caso de que consiga errores solo imprimira todos los errores existentes
    if (len(listaErrores) == 0):
        for x in tokensEncontrados:
          pass
        lexer.lineno =1
    else:
        for b in listaErrores:
            if type(b.value) == int:
                if int(b.value) > 2147483648:
                    print 'Error: Overflow en numero int \"%s\" en la Linea %s, Columna %s' %(str(b.value), str(b.lineno), str(find_column(programa,b)))
                    lexer.lineno =1
                else:
                    pass         
            else:
                print 'Error: se encontro un caracter inesperado \"%s\" en la Linea %s, Columna %s'%(b.value[0],str(b.lineno),str(find_column(programa,b)))
                lexer.lineno =1
        exit()