#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 8/02/2015
#
#proyecto 2 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#operadores del lenguaje setlan
#-----------------------------------------------


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
