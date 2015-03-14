#Autor: Roberto Romero 10-10642
#Grupo: 15
#Fecha: 06/03/2015
#
#proyecto 4 Traductores e interpretadores ci3725
#
#-----------------------------------------------
#conjunto de instrucciones de setlan
#-----------------------------------------------

from setlan_func import *
from setlan_instr import *
from setlan_TablSim import *
from setlan_exp import *

class Instr: pass

#instruccion block
class Block(Instr):
  
   def __init__(self,block_type,instructions,table,scopeno,father,line):
    self.type         = block_type
    self.instructions = instructions
    self.table        = table
    self.scopeno      = scopeno
    self.father       = father
    self.line         = line
  
   def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    for ins in self.instructions:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_node(count + 1)
    print tab + "BLOCK_END"

   def setFather(self,father):
    self.father = father
  
   def traverse(self,count,scope,father,iswrong):
    tab = tabs(count)
    pos = -1
    self.scopeno = count
    for ins in self.instructions:
      if isinstance(ins,Using):
        if ins != None:
          ins.returnTable(self.table)
    if len(scope) - 1 < count:
      scope.append([self.table])
      pos = 0
    else:
      scope[count].append(self.table)
      pos = len(scope[count]) -1
    
    self.table.setFather(father)
    self.table.setScope(count)
    
    for ins in self.instructions:
      if isinstance(ins,Block):
        ins.setFather(pos)
      if not isinstance(ins,str):
        ins.traverse(count + 1,scope,pos,iswrong)

   def print_TablSim(self,count):
    tab = tabs(count)
    for ins in self.instructions:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_TablSim(count + 1)

   def execute(self,count,scope,father):
    for ins in self.instructions:
      ins.execute(count + 1,scope,self.father)

#instruccion using
class Using(Instr):
  
  def __init__(self,declarations,instructions,line,table):
    self.type = "USING"
    self.end = "IN"
    self.declarations = declarations
    self.instructions = instructions
    self.line = line
    self.table = table
    self.scopeno = None
    self.father = None
  
  def print_node(self,count):
    tab = tabs(count)
    i = 0
    print tab + self.type
    for dec in self.declarations:
      if not (i == len(self.declarations)-1):
        dec.print_node(count + 1)
        i += 1
    print tab + self.end
    self.table.print_table(tab)
    count = 1

    for ins in self.instructions:
      if not (ins == None):
        ins.print_node(count + 1)
        i += 1

  def returnTable(self,table):
    for var in self.declarations:
      if var != None:
        variable = var.getVariables()
        var_type = var.getType()
        for i in variable:
          i_name = i.name
          if var_type.value == 'int':
            valor = 0
          if var_type.value == 'bool':
            valor = False
          if var_type.value == 'set':
            valor = {}
          e = Element(i_name,var_type.value,valor,False)
          if not table.isMember(i_name):
            table.insert(e)
          else:
            syntax_error(i,2,self.line)
    return table

  def traverse(self,count,scope,father,iswrong): 
    self.returnTable(self.table)
    if len(scope) - 1 < count:
      scope.append([self.table])
      pos = 0
    else:
      scope[count].append(self.table)
      pos = len(scope[count]) -1
    for ins in self.instructions:
      if ins != None:
        ins.traverse(count + 1,scope,pos,iswrong)

  def print_TablSim(self,count):
    tab = tabs(count)
    self.table.print_table(tab)
    count = 1

    for ins in self.instructions:
      if not (ins == None):
        if not isinstance(ins,str):
          ins.print_TablSim(count + 1)
    print tab + "END_SCOPE"
     
  def execute(self,count,scope,father):
    for ins in self.instructions:
      if not (ins == None):
        ins.execute(count + 1,scope,father)

#instruccion declare
class Declare(Instr):

  def __init__(self,dec_type,dec_id,dec_line):
    self.type = dec_type
    self.id = dec_id
    self.line = dec_line

  def print_node(self,count):
    tab = tabs(count)
    self.type.print_node(count) 
    for idd in self.id:
      idd.print_node(count)

  def getVariables(self):
    return self.id

  def getType(self):
    return self.type
  
  def traverse(self,count,scope,father,iswrong): pass

  def print_TablSim(self,count):
   pass

  def execute(self,count,scope,father): pass

#instruccion scan
class Scan(Instr):
  
   def __init__(self,var,line,column):
    self.type   = "SCAN"
    self.var    = var
    self.line   = line
    self.column = column
    self.var.setLine(line)

   def getColumn(self):
    return self.column
  
   def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable"
    self.var.print_node(count + 2)

   def traverse(self,count,scope,father,iswrong): 
    find_in_scopes(self.var,count,father,scope,self.type,self.line)

   def print_TablSim(self,count):
     pass 

   def execute(self,count,scope,father):
    var = find_in_scopes(self.var,self.scopeno,self.father,scope,self.type,self.line)
    read = raw_input()
    read_array = read.split()

    #la variable es int
    if var.getType() == "int":
      if len(read_array) != 1:
        invalid("numero")
        self.execute(self.scopeno,scope,self.father)
      else:
        if isNumber(read_array[0]):
          overflow(int(read_array[0]),self.line)
          update_in_scopes(self.var.toString(),self.scopeno,self.father,scope,int(read_array[0]))
        else:
          invalid("numero")
          self.execute(self.scopeno,scope,self.father)
    #la variable bool
    else:
      if len(read_array) != 1:
        invalid("booleano")
        self.execute(self.scopeno,scope,self.father)
      else:
        if read_array[0] == "true" or read_array[0] == "false":
          bool = Bool(read_array[0],self.line,self.column)
          update_in_scopes(self.var.toString(),self.scopeno,self.father,scope,bool)
        else:
          invalid("booleano")
          self.execute(self.scopeno,scope,self.father)

#instruccion assign    
class Assign(Instr):
  
   def __init__(self,var,expr,line,column):
    self.type     = "ASIGNACION"
    self.var      = var
    self.expr     = expr
    self.line     = line
    self.column   = column
    self.var.setLine(line)
    self.scopeno = None
    self.father = None

   def getColumn(self):
    return self.column
    
   def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable "
    self.var.print_node(count + 1)
    print tab + "\tvalue " 
    self.expr.print_node(count + 1)
  
   def traverse(self,count,scope,father,iswrong): 
    self.scopeno = count 
    var_type  = find_in_scopes(self.var,count,father,scope,self.type,self.line)
    expr_type = self.expr.traverse(count,scope,father,iswrong)
    
    if var_type != None and expr_type != None:
      if var_type.getType() != expr_type:
        type_error(2,"asignar",self.var,var_type.getType(),self.expr,expr_type,self.line)
        iswrong.append(1)
    else:
      iswrong.append(1)

   def print_TablSim(self,count):
     pass

   def execute(self,count,scope,father):
    value = self.expr.evaluate(self.scopeno,scope,father)
    update_in_scopes(self.var.toString(),self.scopeno,father,scope,value)
    

#instruccion assign_Set
class Assign_set(Instr):
  
  def __init__(self,var,list_n):
    self.type = "ASSIGN"
    self.var = var
    self.list_n = list_n
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable "
    self.var.print_node(count + 1)
    print tab + "\tvalue "
    for i in range(len(self.list_n)):
      print tab + tab + str(self.list_n[i].value) 

  def traverse(self,count,scope,father,iswrong): pass

  def print_TablSim(self,count):
    pass

  def execute(self,count,scope,father):
    pass

#instrucciones print y println
class Fun_print(Instr):
  
   def __init__(self,class_type,variables,line,column):
    self.type      = class_type
    self.variables = variables
    self.line      = line
    self.column    = column
    self.scopeno   = None
    self.father    = None   

   def getColumn(self):
    return self.column
    
   def print_node(self,count):
    tab = tabs(count)
    for var in self.variables:
      print tab + "\telements "
      var.print_node(count + 2)

   def traverse(self,count,scope,father,iswrong):
    for var in self.variables:
      if isinstance(var,Id):
        var.setLine(self.line)
      var.traverse(count,scope,father,iswrong)

   def print_TablSim(self,count):
     pass

   def execute(self,count,scope,father):
      self.scopeno = count
      to_print = ""
      for elem in self.variables:
        if isinstance(elem,Id) or isinstance(elem,BinOp):
          _var = elem.evaluate(self.scopeno,scope,self.father)
          if isinstance(_var,int) or _var == None:
            to_print += str(_var)
          else:
            to_print += _var.toString()
        else:
          to_print += eval(elem.toString())
      print to_print
      if self.type == "PRINTLN":
        print ""

#instruccion for
class For(Instr):
  
  def __init__(self,var,direction,expression,instruction,line,table):
    self.type = "FOR"
    self.var = var
    self.direction = direction
    self.expression = expression
    self.instruction = instruction
    self.line = line
    self.table = table
    self.top = None
    self.bottom = None
    self.current = None
    self.scopeno = None
    self.father = None
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tvariable "
    self.var.print_node(count + 1)
    print tab + "\tdirection "
    print tab + tab + self.direction
    print tab + "\tIN " 
    self.expression.print_node(count + 1)
    print tab + "\tDO "
    for i in self.instruction:
      if not (i == None):
        i.print_node(count + 2)
      else:
        print tab + "BLOCK_END"

  def traverse(self,count,scope,father,iswrong):

    if len(scope) - 1 < count:
      scope.append([self.table])
      pos = 0
    else:
      scope[count].append(self.table)
      pos = len(scope[count]) -1
    for ins in self.instruction:
      if ins != None:
        ins.traverse(count + 1,scope,pos,iswrong)

  def print_TablSim(self,count):
    tab = tabs(count)
    for ins in self.instruction:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_TablSim(count + 1)


  def execute(self,count,scope,father):
    
    if isinstance(self.expression,Id):
      self.expression = find_in_scopes(self.expression,self.scopeno,self.father,scope,self.type,self.line)
      self.expression = self.expression.getValue()

    if self.bottom == None:
      self.expression = self.expression.evaluate(self.scopeno,scope,self.father)
      self.top = self.expression.top(self.scopeno,scope,self.father)
      if isinstance(self.expression,Id):
        self.bottom = find_in_scopes(self.expression,self.scopeno,self.father,scope,self.type,self.line)
      else:
        self.bottom = self.rang.bottom(self.scopeno,scope,self.father)
      scope[self.scopeno][self.current].update(self.var.toString(),None,self.bottom)
    
    var_it = int(scope[self.scopeno][self.current].find(self.var.toString()).getValue())
    
    if var_it <= self.top:
      for i in self.instruction:
        i.execute(self.scopeno,scope,self.father)
      scope[self.scopeno][self.current].update(self.var.toString(),None,var_it+1)
      self.execute(self.scopeno,scope,self.father)

#instruccion while
class While(Instr):
  
  def __init__(self,condition,instruction):
    self.type = "WHILE"
    self.condition = condition
    self.instruction = instruction
    
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tcondicion:"
    self.condition.print_node(count + 2)
    print tab + "\tinstruccion: "
    for i in self.instruction:
      i.print_node(count + 2)
  

  def traverse(self,count,scope,father,iswrong):
    
    if isinstance(self.condition,Id):
      self.condition.setLine(self.line)
    
    condition_type = self.condition.traverse(count,scope,father,iswrong)
    if condition_type != "bool":
      type_error(1,"iterar",self.condition,condition_type,None,None,self.line)
    
    for i in self.instruction:
      i.traverse(count,scope,father,iswrong)

  def print_TablSim(self,count):
    tab = tabs(count)
    for ins in self.instruction:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_TablSim(count + 1)

  def execute(self,count,scope,father): 
    if self.condition.evaluate(self.scopeno,scope,self.father).toString() == "true":
      for i in self.instruction:
        i.execute(self.scopeno,scope,self.father)
      self.execute(self.scopeno,scope,self.father)

#instruccion if then   
class IfThen(Instr):
  
  def __init__(self,condition,instruction):
    self.type = "IF THEN"
    self.condition = condition
    self.instruction = instruction
  
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tcondicion: "
    self.condition.print_node(count + 2)
    print tab + "\tverdadero: "
    for i in self.instruction:
      i.print_node(count + 2)

  def traverse(self,count,scope,father,iswrong):
    
    if isinstance(self.condition,Id):
      self.condition.setLine(self.line)
    
    condition_type = self.condition.traverse(count,scope,father,iswrong)
    if condition_type != "bool":
      type_error(1,"condicional",self.condition,condition_type,None,None,self.line)
   
    for ins in self.instruction:
      ins.traverse(count,scope,father,iswrong)

  def print_TablSim(self,count):
    tab = tabs(count)
    for ins in self.instruction:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_TablSim(count + 1)

  def execute(self,count,scope,father):
    if self.condition.evaluate(self.scopeno,scope,self.father).toString() == "true":
      for i in self.instruction:
        i.execute(self.scopeno,scope,self.father)

#instruccion if then else
class IfThenElse(Instr):
  
  def __init__(self,condition,instruction1,instruction2):
    self.type = "IF THEN ELSE"
    self.condition = condition
    self.instruction1 = instruction1
    self.instruction2 = instruction2
  
  def print_node(self,count):
    tab = tabs(count)
    print tab + self.type
    print tab + "\tcondicion: "
    self.condition.print_node(count + 2)
    print tab + "\tverdader: "
    for i1 in self.instruction1:
      i1.print_node(count + 2)
    print tab + "\tfalso:"
    for i2 in self.instruction2:
      i2.print_node(count + 2)  

  def traverse(self,count,scope,father):
    
    if isinstance(self.condition,Id):
      self.condition.setLine(self.line)
    
    condition_type = self.condition.traverse(count,scope,father)
    if condition_type != "bool":
      type_error(1,"condicional",self.condition,condition_type,None,None,self.line)
    
    for i1 in self.instruction1:
      i1.traverse(count,scope,father,iswrong)
    for i2 in self.instruction2:
      i2.traverse(count,scope,father,iswrong)

  def print_TablSim(self,count):
    tab = tabs(count)
    for ins in self.instruction1:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_TablSim(count + 1)
    for ins in self.instruction2:
      if not isinstance(ins,str):
        if not (ins == None):
          ins.print_TablSim(count + 1)

  def execute(self,count,scope,father): 
    if self.condition.evaluate(self.scopeno,scope,self.father).toString() == "true":
      for i1 in self.instruction1:
        i1.execute(self.scopeno,scope,self.father)
    else:
      for i2 in self.instruction2:
        i2.execute(self.scopeno,scope,self.father)


