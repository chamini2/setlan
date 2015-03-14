#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 06/03/2015
#
#proyecto 4 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#operadores del lenguaje setlan
#-----------------------------------------------



from setlan_TablSim import *
from setlan_lex import *

import sys

#Errores que se imprimiran por pantalla
line_column          = "Error en linea %d, columna %d: "
just_line            = "Error en linea %d: "
iteration_var        = line_column + "se intenta modificar la variable \'%s\' la cual pertenece a una iteracion." 
type_error_binary    = line_column + "intento de \'%s\' entre \'%s\' de tipo \'%s\' y \'%s\' de tipo \'%s\'."
type_error_unary     = line_column + "intento de aplicar \'%s\' a \'%s\' de tipo \'%s\'."
not_initialized_msg  = line_column + "la variable \'%s\' no ha sido inicializada."
not_declared         = line_column + "la variable \'%s\' no ha sido declarada."
already_declared     = line_column + "la variable \'%s\' ya ha sido declarada."
overflow_msg         = just_line   + "el resultado no puede representarse en 32 bits."
div_by_zero_msg      = just_line   + "division por cero."


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
 
#Funcion que dado un error sintactico lo imprime por pantalla y termina
#la ejecucion del programa
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

#Funcion que dado un error de tipos lo imprime por pantalla y termina
#la ejecucion del programa.
def type_error(num_error,op,var1,val1,var2,val2,line):
  _op = operador(op)
  str_1 = var1.toString()
  col1 = var1.getColumn()
  
  #Error de tipos en operaciones unarias
  if num_error   == 1:
    print type_error_unary % (line,col1,_op,str_1,val1)
  #Error de tipos en operaciones binarias 
  elif num_error == 2:
    str_2 = var2.toString()
    if _op == "menos":
      _op = "restar"
    print type_error_binary % (line,col1,_op,str_1,val1,str_2,val2) 
  sys.exit()

#Funcion que dado una variable la busca en los alcances accesibles
#por ella
def find_in_scopes(var,count,father,scope,ins_type,line):
  v = None
  if count > 0:
    count -= 1
    v      = scope[count][father].find(var.toString())
    if v == None:
      #Busca en otro alcance
      new_father = scope[count][father].getFather()
      v          = find_in_scopes(var,count,new_father,scope,ins_type,line)
      
    #La variable se encuentra en uno de los alcances
    else:
      #Si la variable esta dentro de una iteracion no se puede
      #utilizar en ninguna asignacion.
      if v.getIt() and ins_type == "ASIGNACION":
        syntax_error(var,3,line)
  #La variable no se encuentra en ninguno de los alcances
  else:
    syntax_error(var,1,line)
  return v
  
#Funcion que dado un token ubica la columna en donde este se ecnuentra  
def column_index(data,t):
  last = data.rfind('\n', 0, t)
  col  = (t - last)
  return col

#Funcion que dado una division si el divisior es cero imprime por pantalla
#el error y termina la ejecucion del programa.
def div_by_zero(line):
  print div_by_zero_msg % (line)
  sys.exit()
  
#Funcion que dado dos rangos si la interseccion es vacia imprime por pantalla
#el error y termina la ejecucion del programa.
def disjoint_sets_error(line):
  print disjoint_sets_msg % (line)
  sys.exit()

#Funcion que dado un numero si produce un overflow imprime el error
#por pantalla y termina la ejecucion del programa.
def overflow(num,line):
  if not is32(num):
    print overflow_msg % (line)
    sys.exit()

#Funcion que dado una variable no inicializada imprime el error por pantalla
#y termina la ejecucion del programa
def not_initialized(var,line):
  col = var.getColumn()
  print not_initialized_msg % (line,col,var.toString())
  sys.exit()
  

#Funcion que actualiza el valor d euna variable en los scopes 
def update_in_scopes(var,count,father,scope,new_value):
  v = None
  if count > 0:
    count -= 1
    v      = scope[count][father].find(var)
    if v == None:
      #Busca en otro alcance
      new_father = scope[count][father].getFather()
      v          = update_in_scopes(var,count,new_father,scope,new_value)      
  #La variable no se encuentra en ninguno de los alcances
  else:
    print "NO SE CONSIGUE LA VARIABLE"
    sys.exit()
  scope[count][father].update(var,"int",new_value)
  
#Funcion que dado un token ubica la columna en donde este se ecnuentra  
def column_index(data,t):
  last = data.rfind('\n', 0, t)
  col  = (t - last)
  return col

#Funcion que dado un operador determina si es relacional  
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

#Determina si un numero es de 32 bits o no
def is32(n):
  try:
    bitstring=bin(n)
  except (TypeError, ValueError):
    return False
  if len(bin(n)[2:]) <=32:
    return True
  else:
    return False

#Funcion que dado 2 strings determina si son o no numeros
def areNumbers(n1,n2):
  try: 
    _top    = int(n2)
    _bottom = int(n1)
    if _top > _bottom: return True
    else: return False
  except ValueError:
    return False

#Funcion que dado un string determina si es numero o no
def isNumber(n):
  try: 
    _top = int(n)
    return True
  except ValueError:
    return False

#Funcion que dado un string recibido como entrada retorna
#sus componentes
def str_split(string_array,string):
  if len(string_array) == 1:
    tmp_array = string.split("..")
    if len(tmp_array) == 1:
      tmp_array = string.split(",")
      return [tmp_array[0],"..",tmp_array[1]]
  return string_array
  
  
  
  
  
  
