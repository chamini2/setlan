# -*- coding: utf-8 -*-
'''
Created on 2/2/2015

@author: David Klie
@author : Gustavo Benzecri

'''

import sys,operator
from SymbolTable import *
from _ast import Expression
from symtable import Symbol
import re
from decimal import Underflow

stack=SymbolTableStack()

def tab(level):
    return('    '*level)

def add(op1,op2):
    value=op1+op2
    if value>sys.maxint:
        raise OverflowError
    return value

def sub(op1,op2):
    value=op1-op2
    if value<-2**31:
        raise Underflow
    return value

def mult(op1,op2):
    value=op1*op2
    if value>sys.maxint:
        raise OverflowError
    if value<-2**31:
        raise Underflow
    return value

def setplus(value,a_set):
        ret_set=set()
        for i in a_set: ret_set.add(add(value,i))
        return ret_set

def setminus(value,a_set):
    ret_set=set()
    for i in a_set: ret_set.add(sub(i,value))
    return ret_set

def settimes(value,a_set):
    ret_set=set()
    for i in a_set: ret_set.add(mult(i,value))
    return ret_set

def setdiv(value,a_set):
    ret_set=set()
    for i in a_set: ret_set.add(i/value)
    return ret_set

def setmod(value,a_set):
    ret_set=set()
    for i in a_set: ret_set.add(i%value)
    return ret_set

class Program:
    
    def __init__(self,statement_block): # El nodo program contiene el bloque principal de instrucciones.
        self.statement_block=statement_block 
        
    def __str__(self, *args, **kwargs): # La impresion de este nodo genera la impresion del AST
        return('PROGRAM\n'+self.statement_block.printTree(1))
    
    def printTable(self): # Llama a sus hijos para que generen la tabla de variables
        if isinstance(self.statement_block, Scan) or isinstance(self.statement_block, Print) \
        or isinstance(self.statement_block, Assign):
            string=self.statement_block.isCorrect()
        else:
            string= self.statement_block.createTable()
            
        if string:
            return string
        else: 
            return ""
        
    def startExecution(self):
        self.statement_block.execute()
    
class Statement: pass
    
class Block(Statement):
    
    def __init__(self,using,blockinstructions): # Contiene una secuencia de instrucciones dentro de las llaves {...} 
        self.using=using # Declaracion de variables
        self.blockinstructions=blockinstructions # Lista de instrucciones
        self.line_col=None # Linea y columna donde comienza este bloque
    
    def printTree(self,level):
        # Imprime todas las instrucciones del AST hijas de este nodo. dentro de las palabras BLOCK 
        # y END BLOCK
        string=tab(level)+'BLOCK\n'
        if self.using!=None:
            string+=self.using.printTree(level+1) 
        if self.blockinstructions!=None: 
            for binst in self.blockinstructions:
                string+=binst.printTree(level+1)
        string+=tab(level)+'BLOCK_END'+'\n'
        return(string)
    
    def createTable(self): # Llama a la creacion de las tablas de simbolos dentro del bloque
        string=''
        if self.using:
            string+=self.using.printTable()
        if self.blockinstructions:
            for binst in self.blockinstructions:
                if isinstance(binst, Scan) or isinstance(binst, Print) or isinstance(binst, Assign):
                    binst.isCorrect()
                else:
                    string+=binst.createTable()
        if self.using: 
            stack.delete_symbol_table()
            string+=tab(stack.scope)+'END_SCOPE\n'
        return(string)
    
    def execute(self):
        if self.using:
            self.using.printTable()
        if self.blockinstructions:
            for binst in self.blockinstructions:
                binst.execute()
        if self.using:
            stack.delete_symbol_table()
        
class Using(Statement):
    
    def __init__(self,declarations): # Contiene las declaraciones de variables pertenecientes a su bloque padre
        self.declaration=declarations # Lista con las declaraciones del bloque
        self.line_col=None

        
    def printTree(self,level): # Imprime las variables declaradas en el bloque
        string=tab(level)+'USING\n'
        for i in self.declaration:
            for j in i[1]:
                string+=tab(level+1)+i[0]+' '+j+'\n'
        string+=tab(level)+'IN\n'
        return(string)
    
    def createTable(self):
        table=SymbolTable()
        stack.add_symbol_table(table)
        for i in self.declaration:
            for j in i[1]:
                table.insert(j,i[0],self.line_col)
        return table
    
    def printTable(self):
        # Crea una tabla de simbolos, agrega las variables declaradas y devuelve una
        # representacion en string de la misma
        table= self.createTable()
        return(table.showTable(stack.scope-1))

class Print(Statement):
    
    def __init__(self,print_type,values): # Nodo con informacion correspondiente a la sintruccion print y println
        self.print_type = print_type
        self.values=values # Valores a ser impresos por print\println
        self.line_col=None

        
    def printTree(self,level): # Rerpesentacion en string del nodo Print\println en el AST
        string = tab(level)+'PRINT\n'
        string += tab(level+1) + 'elements\n'
        string += self.values.printTree(level+1)
        if (self.print_type == 'println'):
            string += tab(level+2) + 'string\n' + tab(level+3) + '"\\n"' + '\n'
        return(string)
    
    def isCorrect(self): # Verifica que los valores a imprimir sean correctos
        if self.values:
            self.values.isCorrect()
            
    def execute(self):
        string=''
        aux=self.values
        while (aux is not None):
            string+=str(aux)
            aux = aux.values
        if self.print_type=='print':
            sys.stdout.write(string)
        else:
            print string
        del(aux)

class Values(Statement):
    
    def __init__(self, expression, values = None): # Lista de los valores que debe imprimir print\println
        self.expression = expression # Expresion  de tipo string o de la clase Expression 
        self.values = values # Siguiente elemento
        self.line_col=None
    
    def printTree(self,level):
        string = ''
        if (isinstance(self.expression, basestring)):
            string += tab(level+1) + 'string\n' + tab(level+2) + self.expression + '\n'
        else:
            string += self.expression.printTree(level+1)
        if (self.values is not None):
            string += self.values.printTree(level)
        return(string)
    
    def isCorrect(self): # Verifica la correctitud de los valores del print de no serlos, coloca
        # un mensaje de error en la lista de errores symbol_err
        if not isinstance(self.expression,str): self.expression.returnType()
        if self.values:
            self.values.isCorrect()
    
    def __str__(self):
        string=self.expression
        if not isinstance(string,str):
            string=self.expression.evaluate()
            if isinstance(string,set):
                aux=SetExpression()
                aux.set=string
                string=aux
            string=str(string)
        else:
            string=string[1:-1].replace('\\n','\n')
            string=string.replace('\\"','"')
            string=string.replace('\\\\', '\\')
        return string
            
    
    
class Assign(Statement):
    
    def __init__(self,identifier,expression): # Contiene la informacion referida a la sintruccion de asignacion
        self.identifier=identifier # Idenificador de la variable
        self.expression=expression # Expresion a asignar a la variable identificada por el identificador
        self.line_col=None 
    
    def printTree(self,level): # Representacion de la isntruccion en el AST
       string=tab(level)+"ASSIGN\n"+self.identifier.printTree(level+1)+tab(level+1)+'value\n'
       string+=self.expression.printTree(level+2)
       return(string)
    
    def isCorrect(self): # Determina si la asignacion esta bien definida
        is_defined=None
        type_var=self.expression.returnType()
        if type_var: # La expresion tiene un tipo definido para el lenguaje?
            for i in stack.table_stack: # Se busca en las tablas de simbolos el idntificador
                is_defined=i.lookup(str(self.identifier))
                if is_defined: break
                # Cuando se consiga un identificador que concuerde con el id de la variable se rompe el ciclo
            if  is_defined and is_defined[0]!=type_var: 
                # Si el ciclo se termina sin rompimientos la variable no estaba definida
                # Si el ciclo termina con un break y estamos en este caso la variable tiene otro tipo 
                msj_err='ERROR at line %s column %s: variable "%s" does not match with type of expression'
                msj_err=msj_err % (self.line_col[0],self.line_col[1],self.identifier)
                symbol_err.append(msj_err)
            elif is_defined and len(is_defined)==3:
                msj_err="ERROR at line %s column %s : variable \"%s\" is not assignable"
                msj_err=msj_err % (self.line_col[0],self.line_col[1],self.identifier)
                symbol_err.append(msj_err)
        else: # La expresion no tiene un tipo definido para el lenguaje
            msj_err='ERROR at line %s column %s: expression is not defined correctly'
            msj_err=msj_err % (self.line_col[0],self.line_col[1])
            symbol_err.append(msj_err)
        return
    
    def execute(self):
        table = None
        is_defined=None
        type_var=self.expression.returnType()
        if type_var: # La expresion tiene un tipo definido para el lenguaje?
            for i in stack.table_stack: # Se busca en las tablas de simbolos el idntificador
                is_defined=i.lookup(str(self.identifier))
                if is_defined:
                    table = i
                    break
                # Cuando se consiga un identificador que concuerde con el id de la variable se rompe el ciclo
        table.update(str(self.identifier),self.expression.evaluate())

class Scan(Statement):
    
    
    def __init__(self,scan_identifier): # Recibe de la consola alguna entrada para el identificador 
        self.identifier=scan_identifier
        self.line_col=None
        
    def printTree(self,level): # Representacion en string para el AST
        return tab(level)+'SCAN\n'+self.identifier.printTree(level+1)
    
    def isCorrect(self): # Se determina si la variable esta definida para su asignacion
        is_defined=None
        for i in stack.table_stack: # Se busca si la variable esta definida
            is_defined=i.lookup(str(self.identifier))
            if is_defined: break
        if not is_defined:
            symbol_err.append('ERROR at line %s, column %s in scan : variable "%s" is not defined yet'% \
            (self.line_col[0],self.line_col[1],str(self.identifier)))
        elif len(is_defined)>2:
            symbol_err.append('ERROR at line %s, column %s in scan : variable "%s" is not modifiable'% \
            (self.line_col[0],self.line_col[1],str(self.identifier)))
        elif is_defined[0]=='set':
            symbol_err.append('ERROR at line %s, column %s in scan : variable "%s" is of type \'set\''% \
            (self.line_col[0],self.line_col[1],str(self.identifier)))
        return
    
    def execute(self):
        linea=raw_input("insert value: ")
        linea=linea.strip(' ')
        is_defined=None
        value = None
        matchObject=re.match(r'([\d\(\)\*\+\-%/]+|true|false)',linea,re.M)
        if not matchObject:
            print "Invalid expression"
            self.execute()
        else:
            is_defined=None
            value=matchObject.group()
            value=value.capitalize()
            for i in stack.table_stack: # Se busca si la variable esta definida
                is_defined=i.lookup(str(self.identifier))
                if is_defined: break
            try:
                value=eval(value)
            except SyntaxError:
                self.execute()
                return
            if (type(value)==type(True) and is_defined[0]=='bool') or \
                (type(value)==type(0) and is_defined[0]=='int'):
                i.update(str(self.identifier),value)
            else:
                print 'Expected value of type %s'%is_defined[0]
                self.execute()

class if_statement(Statement):
    
    def __init__(self,condition,statement_block,else_clause=None): 
        self.condition=condition
        self.statement_block=statement_block
        self.else_clause=else_clause
        self.line_col=None
    
    def printTree(self,level):
        string=tab(level)+'IF\n'+tab(level+1)+'condition\n'+self.condition.printTree(level+2)
        string+=tab(level+1)+'THEN\n'+self.statement_block.printTree(level+2)
        if self.else_clause!=None:
            string+=self.else_clause.printTree(level+1)
        return(string)
    
    def createTable(self): # If puede tener una instruccion de tipo block por lo tanto es capaz de generar tablas
        string=''
        type_cond=self.condition.returnType()
        if type_cond!='bool': # La condicion es de tipo booleana?
            symbol_err.append('ERROR at line %s, column %s: if conditions must be of type bool'%self.condition.line_col)
        if isinstance(self.statement_block, Scan) or isinstance(self.statement_block, Print) \
        or isinstance(self.statement_block, Assign): # Los statements que no generan tablas
            self.statement_block.isCorrect()
        else: # Los demas pueden generar tablas
           string=self.statement_block.createTable()
        if self.else_clause:
            string+=self.else_clause.createTable()
        return string 
    
    def execute(self):
        condition=self.condition.evaluate()
        if condition:
            self.statement_block.execute()
        elif self.else_clause:
            self.else_clause.execute()
    
class else_statement(Statement):
    
    def __init__(self,block_or_if): # contienen la instruccion que va despues del else
        self.block_or_if=block_or_if
        self.line_col=None
        
    def printTree(self,level): # Representacion en string del else statement
        return tab(level)+"ELSE\n"+self.block_or_if.printTree(level+1)
    
    def createTable(self): # Como else puede generar una tabla debe tener este metodo
        string=''
        if isinstance(self.block_or_if, Scan) or isinstance(self.block_or_if, Print) \
        or isinstance(self.block_or_if, Assign): # Se revisa que no sea una instruccion hoja
            self.block_or_if.isCorrect()
        else:
           string=self.block_or_if.createTable() # Si no lo es se crea una tabla
        return string
    
    def execute(self):
        self.block_or_if.execute()
    
class repeat_statement(Statement):
    
    def __init__(self, statement):
        self.statement=statement # Instruccion dentro del repeat (Puede generar una tabla)
    
    def printTree(self,level): # Repsresentacion en string
        return(tab(level)+'REPEAT\n'+self.statement.printTree(level+1))
    
    def createTable(self): # El metodo es identico al de else
        string=''
        if isinstance(self.statement, Scan) or isinstance(self.statement, Print) \
        or isinstance(self.statement, Assign):
            self.statement.isCorrect()
        else:
           string=self.statement.createTable()
        return string
    
    def execute(self):
        self.statement.execute()
    
class while_statement(Statement):
    
    def __init__(self,condition): # While es una condicion hoja
        self.condition=condition
        self.line_col=None
    
    def printTree(self,level):
        return(tab(level)+'WHILE\n'+tab(level+1)+'condition\n'+self.condition.printTree(level+2))
    
    def isCorrect(self): # Se verifica que la condicion sea de tipo booleana
        if self.condition.returnType()!='bool':
            symbol_err.append('ERROR at line %s, column %s: while condition must be of type bool'%self.condition.line_col)
            
    def evaluate(self):
        return self.condition.evaluate()
    
class Do(Statement): # Estructura similar a la del else
    
    def __init__(self,block_statement):
        self.block_statement=block_statement 
        self.line_col=None
        
    def printTree(self,level):
        return tab(level)+'DO\n'+self.block_statement.printTree(level+1)
    
    def createTable(self):
        string=''
        if isinstance(self.block_statement, Scan) or isinstance(self.block_statement, Print) \
        or isinstance(self.block_statement, Assign):
            self.block_statement.isCorrect()
        else:
           string=self.block_statement.createTable()
        return string
    
    def execute(self):
        self.block_statement.execute()
    
class repeat_while_do(Statement): # Nodo que representa la instruccion repeat while do
    def __init__(self, Repeat = None, While = None, Do = None):
        self.repeat_statement = Repeat
        self.while_statement = While
        self.do_statement = Do
        self.line_col=None
        
    def printTree(self,level): # Representacion en String
        string = ''
        if (self.repeat_statement is not None):
            string += self.repeat_statement.printTree(level)
        if (self.while_statement is not None):
            string += self.while_statement.printTree(level)
        if (self.do_statement is not None):
            string += self.do_statement.printTree(level) 
        return(string)
    
    def createTable(self): # Como de este nodo se pueden generar bloques con using debe tener este metodo
        string=""
        if self.while_statement!=None and self.do_statement!= None and self.repeat_statement is None: # while do
            self.while_statement.isCorrect()
            string=self.do_statement.createTable()
        elif self.repeat_statement!=None and self.while_statement!=None and self.do_statement is None: # repeat while
            self.while_statement.isCorrect()
            string=self.repeat_statement.createTable()
        else: # repeat while do
            self.while_statement.isCorrect()
            string+=self.repeat_statement.createTable()
            string+=self.do_statement.createTable()
        return string
    
    def execute(self):
        if self.while_statement!=None and self.do_statement!= None and self.repeat_statement is None:
            while self.while_statement.evaluate():
                self.do_statement.execute()
        elif self.repeat_statement!=None and self.while_statement!=None and self.do_statement is None:
            self.repeat_statement.execute()
            while self.while_statement.evaluate():
                self.repeat_statement.execute()
        else:
            while True:
                self.repeat_statement.execute()
                if not self.while_statement.evaluate(): break
                self.do_statement.execute()
                
    
class For_statement(Statement):
    
    def __init__(self,dummy,direction,set_expression,do_statement):
        self.dummy=dummy # variable de iteracion
        self.direction=direction # de minimo a maximo o de maximo a minimo
        self.set_expression=set_expression # conjunto sobre el que se va a iterar
        self.do_statement=do_statement # acciones que se van a tomar por cada elemento de la expresion
        self.line_col=None
        
    def printTree(self,level): # Representacion en string
        string=tab(level)+'FOR\n'+self.dummy.printTree(level+1)
        string+=tab(level+1)+'direction\n'+tab(level+2)+self.direction+'\n'
        string+=tab(level+1)+'IN\n'+self.set_expression.printTree(level+1)+self.do_statement.printTree(level+1)
        return(string)
    
    def createTable(self):
        if self.set_expression.returnType()!='set': # La expresion es de tipo conjunto?
            symbol_err.append('ERROR at line %s, column %s in for statement expression must be of type set'%self.set_expression.line_col)
        table=SymbolTable()# Creacion de la tabla de la variable de iteracion
        table.insert(str(self.dummy),'int',self.line_col,iterator=True) # insercion de la variable en la tabla
        stack.add_symbol_table(table) # La tabla va a la punta de la pila 
        string=table.showTable(stack.scope-1)# se imprime la tabla
        string+=self.do_statement.createTable() # se crea la tabla de las instrucciones del ciclo si la hay
        stack.delete_symbol_table() # se elimina la tabla de la variable de iteraci�n
        string+=tab(stack.scope)+'END_SCOPE\n'
        return(string)
    
    def execute(self):
        table=SymbolTable()# Creacion de la tabla de la variable de iteracion
        table.insert(str(self.dummy),'int',self.line_col,iterator=True)
        stack.add_symbol_table(table) # La tabla va a la punta de la pila 
        elements=sorted(list(self.set_expression.evaluate()))
        if self.direction=='max': elements.reverse()
        for i in elements:
            table.update(str(self.dummy),i)
            self.do_statement.execute()
        stack.delete_symbol_table()
        del(table)

''' EXPRESIONES RECONOCIDAS POR SETLAN '''
class Expression: pass

class String(Expression): # Clase contenedora de un string de setlan
    
    def __init__(self,value):
        self.value=value
        self.line_col=None
        
    def __str__(self):
        return self.value
    
    def printTree(self,level):
        return tab(level)+"STRING\n"+tab(level+1)+self.value+'\n'
    
    def returnType(self):
        return 'string'
    
class Integer(Expression): # Clase contenedora de un entero en setlan
    
    def __init__(self,value):
        self.value=value
        
    def __str__(self, *args, **kwargs):
        return str(self.value)
        
    def printTree(self,level):
        return(tab(level)+'int\n'+tab(level+1)+str(self.value)+'\n')
    
    def returnType(self):
        return 'int'
    
    def evaluate(self):
        return self.value
    
class Variable(Expression): # Clase para una variable que puede ser de cualquier tipo
    
    def __init__(self,value):
        self.value=value
        self.line_col=None
    
    def printTree(self,level):
        return(tab(level)+'variable\n'+tab(level+1)+str(self.value)+'\n')
    
    def __str__(self):
        return str(self.value)
    
    def returnType(self): # Retorna el tipo de la primera ocurrencia del identificador en la tabla. 
        type_var=None
        for i in stack.table_stack:
            type_var=i.lookup(self.value)
            if type_var: break
        if type_var:
            type_var= type_var[0]
        else: 
            symbol_err.append('ERROR at line %s, column %s: Variable "%s" is not defined'% \
             (self.line_col[0],self.line_col[1],self.value))
        return type_var
    
    def evaluate(self): # Retorna el valor de la primera ocurrencia del identificador en la tabla. 
        type_value=None
        for i in stack.table_stack:
            type_value=i.lookup(self.value)
            if type_value: break
        if type_value:
            type_value= type_value[1]
        else: 
            symbol_err.append('ERROR at line %s, column %s: Variable "%s" is not defined'% \
             (self.line_col[0],self.line_col[1],self.value))
        return type_value
    
class Boolean(Expression): # True o False
    
    def __init__(self,value):
        self.value=value
        self.line_col=None
        
    def printTree(self,level):
        return (tab(level)+'bool\n'+tab(level+1)+str(self.value)+'\n')
    
    def returnType(self):
        return 'bool'
    
    def evaluate(self):
        if self.value=='true': return True
        elif self.value=='false': return False

class SetExpression(Expression): # Expresion de conjunto 
    
    def __init__(self,elements=None):
        self.elements=elements
        self.set=None
        
    def printTree(self,level):
        string=tab(level)+'set\n'
        if self.elements!=None:
            for e in self.elements:
                string+=e.printTree(level+1)
        return(string)
    
    def returnType(self): # Verifica que todos los elementos sean de tipo int, si no lo son retorna None
        type_set='set'
        if self.elements:
            c='int'
            for i in self.elements:
                if i.returnType()!=c:
                    c=None
                    break
            if not c: type_set=c
        return type_set
    
    def evaluate(self):
        conj= set()
        if self.elements:
            for i in self.elements: conj.add(i.evaluate())
        return(conj)
        
    def __str__(self):
        string='{'
        if self.set:
            for i in sorted(list(self.set)):
                string+=str(i)+','
            if len(string)>1:
                string=string[:-1]
        string+='}'
        return string

class GroupedExpression(Expression): # Expresion de parentizacion
    
    def __init__(self,expression):
        self.expression=expression
        self.line_col=None
    
    def printTree(self,level):
         return tab(level)+'LPAREN\n'+self.expression.printTree(level+1)+tab(level)+'RPAREN\n'
     
    def returnType(self): # Retorna el tipo de la expresion que encierran los parentesis
        return self.expression.returnType()
    
    def evaluate(self):
        return self.expression.evaluate()
    
    
    
class UnaryExpression(Expression): # Expresiones unaria
    
    def maxSet(a_set):
        return max(list(a_set))
    
    def minSet(a_set):
        return min(list(a_set))
    unaryOperators= {
    'not' : 'NOT',
    '-'   : 'UNARY_MINUS',
    '>?' : 'MAXSET',
    '<?' : 'MINSET',
    '$?' : 'CARDINALITY'          
    }
    
    type_requierd={
       'not': 'bool',
       '-' : 'int',
       '>?' : 'set',
       '<?' : 'set',
       '$?' : 'set'
    }
    
    operator_function={
       'not': operator.not_,
       '-' : operator.neg,
       '>?' : maxSet,
       '<?' : minSet,
       '$?' : len
    }
    
    def __init__(self,operator,operand):
        self.operator=operator
        self.operand=operand
        self.line_col=None
    
    def printTree(self,level):
        string=tab(level)+UnaryExpression.unaryOperators[self.operator]+' '+self.operator+'\n'
        string+=self.operand.printTree(level+1)
        return(string)
    
    def returnType(self): # Verifica que los operadores sean compatibles con la expresion sobre la que operan
        type_op1=self.operand.returnType()
        if type_op1=='bool' and self.operator=='not': # un not debe tener una expresion booleana
            type_expr='bool'
        elif type_op1=='int' and self.operator=='-': # Un menos unario un operador de tipo entero
            type_expr='int'
        elif (type_op1=='set' and self.operator in ['>?','<?','$?']): 
            # Maximo, Minimo y cardinalidad deben operar sobre conjuntos
            type_expr='int'
        else: # Si no concuerdan con ninguna de estas expresiones error y se retorna None
            string='ERROR at line %s, column %s: %s requires an expression of type %s'
            string=string%(self.operand.line_col[0],self.operand.line_col[1],self.operator,UnaryExpression.type_requierd[self.operator])
            symbol_err.append(string)
            type_expr=None
        return type_expr
    
    def evaluate(self):
        try:
            value=UnaryExpression.operator_function[self.operator](self.operand.evaluate())
        except ValueError:
            print >>sys.stderr, "RUNTIME ERROR at line %s, column %s : EMPTY SET DOESN'T HAVE MAX OR MIN"%self.line_col
            sys.exit(-1)
        return value
                
    
class BinaryExpression(Expression): # Clase para manejar operadores binarios
    

        
    BinaryExpr={
    '+' : 'PLUS',
    '-' : 'MINUS',
    '*' : 'TIMES',
    '/' : 'DIVIDE',
    '%' : 'MODULO',
    '>' : 'GREATER',
    '<' : 'LESS',
    '>=' : 'GREATEREQ',
    '<=' : 'LESSEQ',
    '@' : 'CONTAINS',
    '/=' : 'NOTEQUALS',
    '==' : 'EQUALS',
    '++' : 'UNION',
    '><' : 'INTERSECTION',
    '\\' : 'DIFERENCE',
    '<+>' : 'SETPLUS' ,
    '<->' : 'SETMINUS',
    '<*>' : 'SETTIMES',
    '</>' : 'SETDIV',
    '<%>' : 'SETMOD',
    'and' : 'AND',
    'or' : 'OR'
    }
    
    operator_function={
    '+' : add,
    '-' : sub,
    '*' : mult,
    '/' : operator.div,
    '%' : operator.mod,
    '>' : operator.gt,
    '<' : operator.lt,
    '>=' : operator.ge,
    '<=' : operator.le,
    '@' : operator.contains,
    '/=' : operator.ne,
    '==' : operator.eq,
    '++' : set.union,
    '><' : set.intersection,
    '\\' : set.difference,
    '<+>' : setplus ,
    '<->' : setminus,
    '<*>' : settimes,
    '</>' : setdiv,
    '<%>' : setmod,
    'and' : operator.and_,
    'or' : operator.or_ 
    }
    
    def __init__(self,operand1,operator,operand2):
        self.operand1=operand1
        self.operand2=operand2
        self.operator=operator
        self.line_col=None
        
    def printTree(self,level):
        string=tab(level)+BinaryExpression.BinaryExpr[self.operator]+' '+self.operator+'\n'
        string+=self.operand1.printTree(level+1)+self.operand2.printTree(level+1)
        return(string)
        
    def returnType(self): # Verifica la compatibilidad entre dos expresiones y el operador
        type_op1=self.operand1.returnType()
        type_op2=self.operand2.returnType()
        type_expr=None
        if type_op1==type_op2: # Operandos iguales
            if type_op1=='bool' and self.operator in ['and', 'or']: # Boleanos con and y or
                type_expr=type_op1
            elif type_op1=='int' and self.operator in ['+','-','*','/','%']: # Expresiones aritmeticas
                type_expr=type_op1
            elif  type_op1=='set' and self.operator in ['++','><','\\']: # Operaciones de conjuntos
                type_expr=type_op1
            elif type_op1=='int' and self.operator in ['<','>','<=','>=',]: # Comparadores aritmentidos
                type_expr='bool'
            elif self.operator in ['==','/=']: # Comparadores generales
                type_expr='bool'
        elif type_op1=='int' and type_op2=='set': # Tipos conjunto y entero
            if self.operator in ['<+>','<->','<*>','</>','<%>']: # Operaciones de mapeo sobre los conjuntos
                type_expr=type_op2
            elif self.operator=='@': # Contenci�n
                type_expr='bool'
        else:
            strerr='ERROR at line %s, column %s: \'%s\' requires arguments of type %s,%s'
            if self.operator in ['and', 'or']:
                strerr=strerr%(self.line_col[0],self.line_col[1],self.operator,'bool','bool')
            elif self.operator in ['+','-','*','/','%','<','>','<=','>=',]:
                strerr=strerr%(self.line_col[0],self.line_col[1],self.operator,'int','int')
            elif self.operator in  ['++','><','\\']:
                strerr=strerr%(self.line_col[0],self.line_col[1],self.operator,'set','set')
            elif self.operator in ['<+>','<->','<*>','</>','<%>','@']:
                strerr=strerr%(self.line_col[0],self.line_col[1],self.operator,'int','set')
            else:
                strerr='ERROR at line %s, column %s : \'%s\' requires arguments of the same type'
                strerr=strerr%(self.line_col[0],self.line_col[1],self.operator)
            symbol_err.append(strerr)
        return type_expr
    
    def evaluate(self):
        try:
            value=BinaryExpression.operator_function[self.operator](self.operand1.evaluate(),self.operand2.evaluate())
        except ZeroDivisionError:
            print >>sys.stderr, 'RUNTIME ERROR at line %s, column %s : ZERO DIVISION'%self.line_col
            sys.exit(-1)
        except TypeError as t:
            if self.operator=='@':
                value=BinaryExpression.operator_function[self.operator](self.operand2.evaluate(),self.operand1.evaluate())
            else:
                print str(t),'Oops ... We made a mistake :('
        except OverflowError:
            print >>sys.stderr, 'RUNTIME ERROR at line %s, column %s: OVERFLOW ERROR '%self.line_col
            sys.exit(-1)
        except Underflow:
            print >>sys.stderr, 'RUNTIME ERROR at line %s, column %s: UNDERFLOW ERROR '%self.line_col
            sys.exit(-1)
        return value
            
            
