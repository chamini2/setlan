#!/usr/bin/env python
#
#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 06/03/2015
#
#proyecto 4 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#Analizador sintactico del lenguaje Setlan
#
#Imprime el arbol sintactico abstracto (AST)
#-----------------------------------------------

from ply import *
from setlan_lex import *
from setlan_instr import *
from setlan_exp import *
from setlan_func import *
from setlan_TablSim import *
import sys 
import argparse

scope = []
iswrong = []

#se define la precedencia de los operadores
precedence = (
              ('left','TokenOr','TokenAnd','TokenPlus','TokenMinus','TokenMultiply','TokenDivide','TokenMod'),
              ('right','TokenNot','TokenMinusU'),
              ('nonassoc','TokenMinor','TokenMinorequal','TokenGreater','TokenGreaterequal','TokenEquals','TokenNotequal')
             )

#estructura del inicio del programa
def p_program(p):
  '''program : TokenProgram instruction'''
  table = SymTable()
  table.new()
  p[0] = Block("PROGRAM",p[2],table,None,0,p.lineno(1))

#estructura de bloque
def p_blocks(p):
  '''block : TokenOpenCurly instruction TokenCloseCurly'''
  table = SymTable()
  table.new()
  p[0] = Block("BLOCK",p[2],table,None,0,p.lineno(1))

#estructura de using
def p_using(p):
  '''using : TokenUsing instruction TokenIn instruction'''
  table = SymTable()
  table.new()
  p[0] = Using(p[2],p[4],p.lineno(1),table)


#estructura de las instrucciones 
def p_instruction_bases(p):
  '''instruction : instructions'''
  p[0] = p[1]
  
def p_instructions(p):
  '''instructions : assign
                  | scan
                  | declare
                  | using
                  | print
                  | println
                  | if
                  | while
                  | for
                  | block'''
  p[0] = [p[1]]

def p_instruction(p):
  '''instruction : instructions TokenSemicolon instruction'''
  p[0] = p[1] + p[3]

#estructura de la declaracion de variables  
def p_declare_empty(p):
  '''declare : empty'''
  pass
          
#def p_declare(p):
  #'''declare : type id'''
  #p[0] = Declare(p[1],p[2],p.lineno(1))

def p_declare_list(p):
  '''declare : type list_id'''
  p[0] = Declare(p[1],p[2],p.lineno(1))

def p_list_id_uni(p):
  '''list_id : id '''
  p[0] = [p[1]]

def p_list_id(p):
  '''list_id : id TokenComma list_id'''
  p[0] = [p[1]] + p[3]

#estructura de if then/if then else
def p_if(p):
  '''if : if_then
        | if_then_else'''
  p[0] = p[1]
  
def p_if_then(p):
  '''if_then : TokenIf TokenParenL expression TokenParenR TokenOpenCurly instructions TokenCloseCurly'''
  p[0] = IfThen(p[3],p[6])
  
def p_if_then_else(p):
  '''if_then_else : TokenIf TokenParenL expression TokenParenR TokenOpenCurly instructions TokenCloseCurly TokenElse TokenOpenCurly  instructions TokenCloseCurly'''
  p[0] = IfThenElse(p[3],p[6],p[10])

#estructura de un while
def p_while(s):
  '''while : TokenWhile TokenParenL expression TokenParenR TokenDo TokenOpenCurly instructions TokenCloseCurly'''
  p[0] = While(p[3],p[7])

#estructura de un for  
def p_for_min(p):
  '''for : TokenFor id TokenMin TokenOpenCurly list_number TokenCloseCurly TokenDo instruction'''
  table = SymTable()
  table.new()
  p[0] = For(p[2],p[3],p[5],p[8],p.lineno(1),table)

def p_for_max(p):
  '''for : TokenFor id TokenMax TokenOpenCurly list_number TokenCloseCurly TokenDo instruction'''
  table = SymTable()
  table.new()
  p[0] = For(p[2],p[3],p[5],p[8],p.lineno(1),table)

#def p_repeat(p):
 # '''repeat : TokenRepeat instruction TokenWhile expression TokenDo instruction'''
  #pass
   
#estructura print y println
def p_print(p):
  '''print : TokenPrint list'''
  p[0] = Fun_print("PRINT",p[2],p.lineno(1),column_index(lexer.lexdata,p.lexpos(1)))

def p_println(p):
  '''println : TokenPrintln list'''
  p[0] = Fun_print("PRINTLN",p[2],p.lineno(1),column_index(lexer.lexdata,p.lexpos(1)))

def p_list(p):
  '''list : id TokenComma list
            | string TokenComma list'''
  p[0] = [p[1]] + p[3]

def p_list_base(p):
  '''list : expression
          | string'''
  p[0] = [p[1]]

#estructura de una asignacion
def p_assign(p):
  '''assign : id TokenAssign expression'''
  p[0] = Assign(p[1],p[3],p.lineno(2),column_index(lexer.lexdata,p.lexpos(2)))

def p_assign_set(p):
  '''assign : id TokenAssign TokenOpenCurly list_number TokenCloseCurly'''
  p[0] = Assign_set(p[1],p[4])

#estructura de scan  
def p_scan(p):
  '''scan : TokenScan id'''
  p[0] = Scan(p[2])

#estructura de las operaciones  
def p_expression_op(p):
  '''expression : expression TokenPlus expression
                | expression TokenMinus expression
                | expression TokenMultiply expression
                | expression TokenSetdivide expression
                | expression TokenUnion expression
                | expression TokenIntersection expression
                | expression TokenSetmod expression
                | expression TokenSetplus expression
                | expression TokenSetmultiply expression
                | expression TokenSetMinus expression
                | expression TokenMod expression
                | expression TokenDivide expression
                | expression TokenDifference expression
                | expression TokenOr expression
                | expression TokenAnd expression
                | expression TokenMinor expression
                | expression TokenGreater expression
                | expression TokenMinorequal expression
                | expression TokenGreaterequal expression
                | expression TokenEquals expression
                | expression TokenNotequal expression'''

  p[0] = BinOp(p[1],p[2],p[3],p.lineno(2),column_index(lexer.lexdata,p.lexpos(2)))
  

def p_expr_uminus(p):
  '''expression : TokenMinus expression %prec TokenMinusU
                  | TokenNot expression'''
  p[0] = UnOp(p[1],p[2])

def p_range(p):
  '''range : TokenOpenCurly list_number TokenCloseCurly'''

def p_paren(p):
  '''paren : TokenParenL expression TokenParenR'''
  p[0] = p[2]

def p_expression(p):
  '''expression : paren 
                | bool
                | id
                | number
                | range '''
  p[0] = p[1]


#estructura de las funciones
def p_function(p):
  '''function : function_id paren'''
  p[0] = Function(p[1],p[2])

def p_function_id(p):
  '''function_id : TokenSetgreater
                  | TokenSetminor
                  | TokenSetelements
                  | TokenSetin '''
  p[0] = p[1]

#estructura de los tipos de datos  
def p_type(p):
  '''type : TokenInt 
            | TokenBool 
            | TokenSet '''
  p[0] = Type(p[1])  

def p_bool(p):
  '''bool : TokenTrue
          | TokenFalse'''
  p[0] = Bool(p[1])  
  
  
#estructura de un numero
def p_number(p):
  '''number : TokenNumber'''
  p[0] = Number(p[1])

def p_list_number_uni(p):
  '''list_number : number '''
  p[0] = [p[1]]

def p_list_number(p):
  '''list_number : number TokenComma list_number'''
  p[0] = [p[1]] + p[3]

#estructura de un identificador (ID)  
def p_id(p):
  '''id : TokenID'''
  p[0] = Id(p[1],column_index(lexer.lexdata,p.lexpos(1)))
  

#estructura de un string  
def p_string(p):
  '''string : TokenString'''
  p[0] = String(p[1])  
  
#estructura de vacio 
def p_empty(p):
    '''empty :'''
    pass

#error de entrada
def p_error(p):
  if p == None:
    print "Error de sintaxis, token esperado al final de la entrada"
  else:
    error = "Error de sintaxis en la linea %d, columna %d: token \'%s\' inesperado"
    pos   = find_position(p,lista_tokens)
    if pos == [-1,-1]:
      pos = find_position(p,lista_errores)
      args = (pos[0],pos[1],p.value[0])
    else:
      args  = (pos[0],pos[1],p.value)
    print error % args
  sys.exit()

#dado un token busca su posicion
def find_position(p,List):
  pos = []
  for tok in List:
    if p.value == tok.value:
      pos.append(tok.lineno)
      pos.append(column(lexer.lexdata,tok))
      return pos
  return [-1, -1]

# Se construye el parser
parser = yacc.yacc()

# Se analiza el programa pasado por archivo.
result = parser.parse(entrada)

# Si hay errores durante las verificaciones estaticas se imprimen
# todos por pantalla y se aborta la ejecucion del programa.
if iswrong: sys.exit()

#Se recorre el arbol resultante para ejecutar y evaluar las instrucciones.
result.traverse(0,scope,0,iswrong)
result.execute(0,scope,0)

#FLAGS del programa

#flag que imprime la lista de tokens
#if sys.argv[2] == '-t':
 # print "\n" 
  #print "---------------------------------------LISTA DE TOKENS------------------------------------------"
  #print "\n" 
  #if lista_errores != []:
  #  imprimir_errores(lista_errores)
  #else:
  #  imprimir_tokens(lista_tokens)
#flag que imprime el AST
#elif sys.argv[2] == '-a':
 # print "\n" 
 # print "---------------------------------------------AST-------------------------------------------------"
 # print "\n" 
 # result.print_node(0)
#flag que imprime la tabla de simbolos
#elif sys.argv[2] == '-s':
 # print "\n" 
 # print "--------------------------------------TABLA DE SIMBOLOS-------------------------------------------"
 # print "\n" 
  # Se recorre el arbol resultante para realizar todas las operaciones.
 # result.traverse(0,scope,0)
 # result.print_TablSim(0)
 # print "\n" 
# IMPRIME LA LISTA DE TOKENS, EL AST Y LA TABLA DE SIMBOLOS
#elif sys.argv[2] == '-all' :
 # print "\n" 
 # print "---------------------------------------LISTA DE TOKENS------------------------------------------"
 # print "\n" 
 # if lista_errores != []:
 #   imprimir_errores(lista_errores)
 # else:
 #   imprimir_tokens(lista_tokens)
 # print "\n" 
 # print "---------------------------------------------AST-------------------------------------------------"
 # print "\n" 
  #se imprime el AST
 # result.print_node(0)
 # print "\n"  
 # print "--------------------------------------TABLA DE SIMBOLOS-------------------------------------------"
 # print "\n" 
  # Se recorre el arbol resultante para realizar todas las operaciones.
 # result.traverse(0,scope,0)
 # result.print_TablSim(0)
 # print "\n" 

