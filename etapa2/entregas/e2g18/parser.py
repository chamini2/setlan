#!/usr/bin/python
'''
Created on 7/02/2015

@author: Emmanuel De Aguiar     10-10179
@author: Daniel Pelayo          10-10539

'''

import yacc
import sys
import lexer as lexer
from arbol import *

tokens = lexer.tokens

def p_programa(p):
  '''programa : TokenProgram Instruccion'''
  p[0]=Programa(p[2])


##############################################################################################
#---------------------------------------INSTRUCCIONES DE SETLAN------------------------------#
##############################################################################################

#----------Conjunto de Instrucciones posibles:-----------#
def p_instruccion(p):
  '''Instruccion : Asignacion
                  | Bloque
                  | Entrada
                  | Salida
                  | Condicional
                  | CicloFor
                  | CicloIndeterminado'''
  p[0] = p[1]
#--------------------------------------------------------#

#-----------------------Asignacion----------------------#
def p_instruccion_asignacions(p):
	'''Asignacion : TokenID TokenAsignacion Expresion'''
	p[0] = Asignacion(p[1],p[3])
#-------------------------------------------------------#

#-----------------------Bloque----------------------------------------------------------------#
def p_instruccion_bloque(p):
  '''Bloque : TokenLlaveIzq ListaInstruccion TokenLlaveDer
            | TokenLlaveIzq TokenUsing ListaDeclaracion TokenIn ListaInstruccion TokenLlaveDer'''

  if len(p) == 4:
    p[0] = Bloque(p[2],[],False)
  else:
    p[0] = Bloque(p[5],p[3],True)

def p_instruccion_bloque_listaInstruccion(p):
  '''ListaInstruccion : Instruccion TokenPuntoComa
                      | Instruccion TokenPuntoComa ListaInstruccion'''
  if len(p) == 3:
    p[0] = [(p[1])]
  else:
    p[0] = p[3] + [p[1]]

def p_instruccion_bloque_listaDeclaracion(p):
  '''ListaDeclaracion : tipo listaVariables TokenPuntoComa
                      | tipo listaVariables TokenPuntoComa ListaDeclaracion'''
  if len(p) == 4:
    p[0] = [(p[1],p[2])]
  else:
    p[0] = p[4] + [(p[1],p[2])]

def p_instruccion_bloque_Declaracion_listaDeclaracion_listaVariables(p):
  '''listaVariables : TokenID
                    | TokenID TokenComa listaVariables'''

  if len(p) == 2:
    p[0] = [ID(p[1])]
  else:
    p[0] = p[3] + [ID(p[1])]

def p_tipos(p):
  '''tipo : TokenInt
          | TokenBool
          | TokenSet'''
  p[0] = p[1]

#----------------------------------------------------------------------------------------------#

#--------------CicloFor-------------------#
def p_instruccion_for(p):
  '''CicloFor : TokenFor TokenID TokenMax Expresion TokenDo Instruccion
              | TokenFor TokenID TokenMin Expresion TokenDo Instruccion'''

  direccion = p[3]
  p[0] = CicloFor(ID(p[2]),direccion,p[4],p[6])
#------------------------------------#

#--------------CiclosIndeterminados-------------------#
def p_instruccion_ciclo_indeterminado(p):
  '''CicloIndeterminado : TokenWhile Expresion TokenDo Instruccion
                        | TokenRepeat Instruccion TokenWhile Expresion
                        | TokenRepeat Instruccion TokenWhile Expresion TokenDo Instruccion'''
  if len(p) == 5:
    if p[1] == 'while':
      p[0] = CicloIndeterminadoWhileDo(p[2], p[4])
    else:
      p[0] = CicloIndeterminadoRepeatWhile(p[2],p[4])

  else:
    p[0] = CicloIndeterminadoRepeatWhileDo(p[2], p[4], p[6])
#----------------------------------------------------------------------------------------------#

#--------------condicionales-------------------#
def p_instruccion_condicional_if_then(p):
  '''Condicional : TokenIf Expresion Instruccion
                 | TokenIf Expresion Instruccion TokenElse Instruccion'''

  if len(p) == 4:
    p[0] = CondicionalIfThen(p[2],p[3])
  else:
    p[0] = CondicionalIfThenElse(p[2],p[3],p[5])
#------------------------------------#

#--------------entrada-------------------#
def p_instruccion_entrada(p):
  '''Entrada : TokenScan TokenID'''
  p[0] = Entrada(ID(p[2]))
#------------------------------------#

#--------------salida-------------------#
def p_instruccion_salida(p):
  '''Salida : TokenPrint listaExpresiones
            | TokenPrintLn listaExpresiones'''
  if str(p[1]) == 'print':
    p[0] = Salida(p[2])
  else:
    p[0] = Salida([String('"\\n"')] + p[2])



def p_instruccion_listaExpresiones_salida(p):
  '''listaExpresiones : Expresion
                      | Expresion TokenComa listaExpresiones'''
  if len(p) == 2:
    p[0] = [p[1]]
  else:
    p[0] = p[3] + [p[1]]
#------------------------------------#



##############################################################################################
#---------------------------------EXPRESIONES EN SETLAN--------------------------------------#
##############################################################################################

#--------expresiones que son "Terminales":(int,set,bool,string,id,string)----------------------#

#----numero entero----------#
def p_expresion_int(p):
  '''Expresion : TokenNumero'''
  p[0] = Int(p[1])
#---------------------------#

#-------Conjunto------------#
def p_expresion_set(p):
  '''Expresion : TokenLlaveIzq elementos TokenLlaveDer'''
  p[0] = Set(p[2])

def p_expresion_set_elementos(p):
  '''elementos : TokenNumero
                | elementos TokenComa TokenNumero'''

  if len(p) == 2:
    p[0] = [Int(p[1])]
  else:
    p[0] = p[1] + [Int(p[3])]
#--------------------------------------------------------#

#-------Booleano------------#
def p_expresion_bool(p):
  '''Expresion : TokenTrue
              | TokenFalse'''

  p[0] = Bool(p[1])
#---------------------------#

#--------Identificador------#
def p_expresion_id(p):
  '''Expresion : TokenID'''
  p[0] = ID(p[1])
#---------------------------#

#----------String--------------#
def p_expresion_string(p):
  '''Expresion : TokenString'''
  p[0] = String(p[1])
#------------------------------#

#-----------Expresion entre parentesis--------------------------#
def p_expresion_entre_parentesis(p):
  '''Expresion : TokenParentesisIzq Expresion TokenParentesisDer'''
  p[0] = p[2]
#---------------------------------------------------------------#


#-------------------------Expresiones de tipo Operaciones que se pueden hacer en SetLan-------------------------------------#

#Operaciones de Numeros:-------------------------------------------------------------#

#---------------------Operacion Binaria:   INT X INT --> INT----------------#
def p_expresion_operacion_numeros_binaria(p):
    '''Expresion : Expresion TokenMas   Expresion
                  | Expresion TokenMenos  Expresion
                  | Expresion TokenMult  Expresion
                  | Expresion TokenDiv Expresion
                  | Expresion TokenResto Expresion'''
    operador = {
        '+': 'TokenMas',
        '-': 'TokenMenos',
        '*': 'TokenMult',
        '/': 'TokenDiv',
        '%': 'TokenResto'
    }
    simbolo = p[2]
    p[0] = OperacionBinaria(p[1], p[3],operador[p[2]],simbolo)
#------------------------------------------------------------------------------#

#---------------------Operacion Unaria:  (-)INT-------------------#
def p_expresion_operacion_numeros_unaria(p):
    "Expresion : TokenMenos Expresion %prec TokenMenosU"
    p[0] = OperacionUnaria(p[2],'TokenMenos','-')
#-----------------------------------------------------------------#

#-------------------------------------------------------------------------------------#


#Operaciones de Conjuntos-------------------------------------------------------------#

#------------------Operacion Binaria Entre Conjuntos---------------------------------#
def p_expresion_operacion_entre_conjuntos(p):
  '''Expresion : Expresion TokenUnion Expresion
              | Expresion TokenIntersec Expresion
              | Expresion TokenDif Expresion'''
  operador = {
        '++': 'TokenUnion',
        '\\': 'TokenDif',
        '><': 'TokenIntersec'}
  simbolo = p[2]
  p[0] = OperacionBinaria(p[1], p[3],operador[p[2]],simbolo)

#------------------Operacion Binaria Sobre Conjuntos: INT X SET --> SET--------------#
def p_expresion_operacion_sobre_conjuntos_binaria(p):
  '''Expresion : Expresion TokenMapMas Expresion
               | Expresion TokenMapMenos Expresion
               | Expresion TokenMapMult Expresion
               | Expresion TokenMapDiv Expresion
               | Expresion TokenMapResto Expresion'''
  operador = {
        '<+>': 'TokenMapMas',
        '<->': 'TokenMapMenos',
        '<*>': 'TokenMapMult',
        '</>': 'TokenMapDiv',
        '<%>': 'TokenMapResto'
    }
  simbolo = p[2]
  p[0] = OperacionBinaria(p[1], p[3],operador[p[2]],simbolo)
#-------------------------------------------------------------------------------------#
#------------------Operacion Unaria Sobre Conjuntos: X SET --> INT--------------#
def p_expresion_operacion_sobre_conjuntos_unaria(p):
  '''Expresion : TokenValorMax Expresion
               | TokenValorMin Expresion
               | TokenNumElem Expresion'''
  operador = {
        '>?': 'TokenValorMax',
        '<?': 'TokenValorMin',
        '$?': 'TokenNumElem'
    }
  simbolo = p[1]
  p[0] = OperacionUnaria(p[2],operador[p[1]],simbolo)
#-------------------------------------------------------------------------------------#

#--------------------Operaciones de Booleanos-------------------------------------------#

#---------------------Operacion Binaria: BOOL X BOOL --> BOOL-------------------------#
def p_expresion_operacion_booleana_binaria(p):
    '''Expresion : Expresion TokenAnd   Expresion
                  | Expresion TokenOr  Expresion'''
    operador = {
        'and': 'TokenAnd',
        'or': 'TokenOr'}
    simbolo = p[2]
    p[0] = OperacionBinaria(p[1], p[3],operador[p[2]],simbolo)
#-------------------------------------------------------------------------------------#

#---------------------Operacion Unaria: (not)BOOL-------------------------#
def p_expresion_operacion_booleana_unaria(p):
  '''Expresion : TokenNot Expresion'''
  p[0] = OperacionUnaria(p[2],'TokenNot','not')
#-------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------

#--------------------------------------Operaciones Comparativas----------------------------#
def p_expresion_operacion_Comparativa(p):
    '''Expresion : Expresion TokenMenor Expresion
                  | Expresion TokenMenorIgual  Expresion
                  | Expresion TokenMayor Expresion
                  | Expresion TokenMayorIgual Expresion
                  | Expresion TokenEquivalente Expresion
                  | Expresion TokenDesigual Expresion
                  | Expresion TokenContencion Expresion'''
    operador = {
        '<': 'TokenMenor',
        '<=': 'TokenMenorIgual',
        '>': 'TokenMayor',
        '>=': 'TokenMayorIgual',
        '==': 'TokenEquivalente',
        '/=': 'TokenDesigual',
        '@': 'TokenContencion'}
    simbolo = p[2]
    p[0] = OperacionBinaria(p[1], p[3],operador[p[2]],simbolo)
#---------------------------------------------------------------------------------------------

#-----------------------Precedencia de los Operadores---------------------------------------#

precedence = (

  #----------------------OperadoresSobreBool:(bool x bool--> bool)
  ('left', 'TokenAnd'),
  ('left', 'TokenOr'),

  #----------------------OperadoresComparativos:
    #(int x set--> bool)
  ('nonassoc', 'TokenContencion'),
    #(Z x W--> bool)
  ('nonassoc', 'TokenEquivalente', 'TokenDesigual'),
    #(int x int--> bool)
  ('nonassoc', 'TokenMenor', 'TokenMenorIgual', 'TokenMayor', 'TokenMayorIgual'),

  #-----------------------OperadoresAritmeticos (int x int--> int):
  ('left', 'TokenMult', 'TokenDiv', 'TokenResto'),  
  ('left', 'TokenMas', 'TokenMenos'),

  #-----------------------OperadoresSobreConjunto (set x set--> set):
  ('left', 'TokenIntersec'),
  ('left', 'TokenUnion', 'TokenDif'),

  #-----------------------OperadoresConjuntoAritmeticas (int x set--> set):
  ('left', 'TokenMapMult', 'TokenMapDiv', 'TokenMapResto'),
  ('left', 'TokenMapMas', 'TokenMapMenos'),

  #--------------------OperadoresUnarios
    #bool  
  ('right', 'TokenNot'),
    #int
  ('right', 'TokenMenosU'),
    #set
  ('right', 'TokenValorMax', 'TokenValorMin', 'TokenNumElem'),
)
#---------------------------------------------------------------------------------------------#

##################################################################################################
#----------------------------------FUNCIONALIDAD DEL PARSER -------------------------------------#
##################################################################################################

#Lista de errores sintacticos: Para nuestro caso solo listaremos el primer error que consiga
errorSintaxis = []

def p_error(p):

  if (p <> None):
    errorSintaxis.append(p)
  else:
    print 'ERROR: los programas comienzan por la palabra \'programa\' seguido de instrucciones'
    exit()


def parsear(entrada):
    
    try:
    
        #Se abre el archivo de entrada
        arch = open(entrada)
         
        #Leemos el archivo y lo almacenamos en programa para luego analizarlo lexicograficamente
        programa = arch.read()
        
        #Construccion del PARSER
        parser = yacc.yacc()    
        arbol = parser.parse(programa)
        
        
    except IOError:
        
        print 'El archivo <%s> no puede ser abierto' %entrada
        exit()

    #Impresion por pantalla de la salida esperada
    #En caso de que consiga errores solo imprimira el primero que consiga

    if len(errorSintaxis) != 0:
      for e in errorSintaxis:
        elem = 'ERROR: unexpected token: \'%s\'' %(e.value)
        elem += ' at line %s, column %s'%(str(e.lineno), str(lexer.find_column(programa,e) + 1))
        print elem
    else:
      print arbol