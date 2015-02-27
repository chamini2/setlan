#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 24/02/2015
#
#proyecto 3 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#operadores del lenguaje setlan
#-----------------------------------------------



from setlan_TablSim import *
from setlan_lex import *

import sys

#Errores que se imprimiran por pantalla
not_declared      = "Error en linea %d, columna %d: la variable \'%s\' no ha sido declarada."
already_declared  = "Error en linea %d, columna %d: la variable \'%s\' ya ha sido declarada en este alcance."
iteration_var     = "Error en linea %d, columna %d: se intenta modificar la variable \'%s\' la cual pertenece a una iteracion." 
type_error_binary = "Error en linea %d, columna %d: intento de \'%s\' entre \'%s\' de tipo \'%s\' y \'%s\' de tipo \'%s\'."
type_error_unary  = "Error en linea %d, columna %d: intento de aplicar \'%s\' a \'%s\' de tipo \'%s\'."


#funcion para concatenar tabs
def tabs(num_tab):
  i = 0
  string_tab = ""
  while i < num_tab:
    string_tab = string_tab + "\t"
    i = i + 1
  return string_tab

#retorna el nombre del operador binario
def operador(op):
  if   op == "+":
    return "PLUS "
  elif op == "-":
    return "MINUS "
  elif op == "*":
    return "TIMES "
  elif op == "%":
    return "MOD "
  elif op == "/":
    return "DIV "
  elif op == ">":
    return "GREATER "
  elif op == "<":
    return "MINOR "
  elif op == ">=":
    return "GREATER_EQUAL "
  elif op == "<=":
    return "MINOR_EQUAL "
  elif op == "==":
    return "EQUALS"
  elif op == "/=":
    return "DIFERENT"
  elif op == "and":
    return op
  elif op == "or":
    return op
  else:
    return op

#retorna el nombre del operador unario 
def op_unario(op):
  if op == "-":
    return "menos unario"
  elif op == "not":
    return op
  else:
    return "OPERADOR NO DETERMINADO"

# Dado unos elementos los agrega a una tabla de simbolos y
# la retorna
def add_to_symtable(elements):
  size  = len(elements) - 1
  last  = elements[size]
  table = SymTable()
  table.new()
  print last
  i = 0
  while i < size:
    elem = Element(elements[i],last,None)
    table.insert(elem)
    i += 1
  return table     
  
# Funcion que dado un token busca su posicion, es decir
# la fila y la columna en la que se encuentra
def find_position(case,p,List):
  pos   = []
  new_p = ""
  
  if case == 1:
    new_p = p.value
  else:
    new_p = p
  for tok in List:
    if new_p == tok.value:
      pos.append(tok.lineno)
      pos.append(column(lexer.lexdata,tok))
      return pos
  return [-1, -1]
 
# Funcion que dado un error sintactico lo imprime por pantalla y termina
# la ejecucion del programa
def syntax_error(var,num_error,line):
  col = var.getColumn()
  v   = var.toString()
  if num_error   == 1:
    print not_declared % (line,col,v)
  elif num_error == 2:
    print already_declared % (line,col,v)
  elif num_error == 3:
    print iteration_var % (line,col,v)
  sys.exit()

#  Funcion que dado un error de tipos lo imprime por pantalla y termina
# la ejecucion del programa.
def type_error(num_error,op,var1,val1,var2,val2,line):
  _op = operador(op)
  str_1 = var1.toString()
  col1 = var1.getColumn()
  
  # Error de tipos en operaciones unarias
  if num_error   == 1:
    print type_error_unary % (line,col1,_op,str_1,val1)
  # Error de tipos en operaciones binarias 
  elif num_error == 2:
    str_2 = var2.toString()
    if _op == "menos":
      _op = "restar"
    print type_error_binary % (line,col1,_op,str_1,val1,str_2,val2) 
  sys.exit()

#  Funcion que dado una variable la busca en los alcances accesibles
# por ella
def find_in_scopes(var,count,father,scope,ins_type,line):
  
  v = None
  if count > 0:
    count -= 1
    v      = scope[count][father].find(var.toString())
    if v == None:
      # Busca en otro alcance
      new_father = scope[count][father].getFather()
      v          = find_in_scopes(var,count,new_father,scope,ins_type,line)
      
    # La variable se encuentra en uno de los alcances
    else:
      # Si la variable esta dentro de una iteracion no se puede
      # utilizar en ninguna asignacion.
      if v.getIt() and ins_type == "ASIGNACION":
        syntax_error(var,3,line)
  # La variable no se encuentra en ninguno de los alcances
  else:
    syntax_error(var,1,line)
  return v
  
# Funcion que dado un token ubica la columna en donde este se ecnuentra  
def column_index(data,t):
  last = data.rfind('\n', 0, t)
  col  = (t - last)
  return col

# Funcion que dado un operador determina si es relacional  
def is_relational(n,op):
  rel = []
  if n == 1:
    rel = [">","<",">=","<=","==","/="]
  else:
    rel = [">","<",">=","<="]
  
  for r in rel:
    if op == r:
      return True
  return False
