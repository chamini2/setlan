# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonathan Ng 11-10199
         Manuel Gonzalez 11-10390
    
    Clases para la representaciÃ³n de un Arbol abstracto del lenguaje setlan
'''
import sys
from symbol_table import SymbolTable
from expressions import get_column_text_lexpos
from functions import *

static_errors = []
interpreter_result = []

class Expre:
    
    def __init__(self):
        self.lexpos = -1
        self.lineno = -1
    
    def get_indent_number(self,level):
        return level * 4
    
    def get_ident_str(self,level):
        return self.get_indent_number(level) * r" "
    
    def print_with_indent(self,cad,level):
        print self.get_ident_str(level) + cad
    
    def check_types(self,symbolTable):
        pass
    
    def execute(self,symbolTable):
        pass

class Program(Expre):
    
    def __init__(self, statement):
        Expre.__init__(self)
        self.type = "PROGRAM"
        self.statement = statement
        self.symbolTable = None
        
    def print_tree(self,level = 0):
        self.print_with_indent(self.type, level)
        self.statement.print_tree(level + 1)
    
    def check_types(self):
        self.symbolTable = SymbolTable()
        self.statement.check_types(self.symbolTable)
        
    def execute(self):
        self.symbolTable = SymbolTable()
        self.statement.execute(self.symbolTable)
        
class Scan(Expre):
    
    def __init__(self,id_):
        Expre.__init__(self)
        self.type = "SCAN"
        self.var_to_read = id_
    
    def print_tree(self , level):
        self.print_with_indent(self.type,level)
        self.var_to_read.print_tree(level + 1)

    def check_types(self, symbolTable):
        type_var = self.var_to_read.check_types(symbolTable)
        if type_var == "": return ""
        
        if type_var not in ("int","bool"):
            static_error(self.var_to_read.lineno, self.var_to_read.lexpos,
                            "'SCAN' solo se puede usar para variables de tipo 'int' o 'bool' . '%s' es de tipo '%s'" % \
                                (self.var_to_read.name,type_var) )
    
    def execute(self, symbolTable):
        var = symbolTable.lookup(self.var_to_read.name) # Buscamos la variable en la tabla de simbolos
        in_type = "" # Tipo de valor de la entrada
        mensaje = "Ingrese una variable de tipo '%s':"%var.type 
        while(in_type != var.type):
            in_str = raw_input(mensaje)
            mensaje = ""
            in_str = in_str.strip() # Eliminamos espacios al inicio y al final
            if in_str == "true":
                in_type = "bool"
                in_value = True
                
            elif in_str == "false":
                in_type = "bool"
                in_value = False
            
            # Comprobamos transformando el valor a entero
            try:
                in_value = int(in_str)
                in_type = "int"
            except(ValueError):
                pass
                      
            if (in_type != var.type):
                mensaje= "Error el valor tiene que ser de tipo '%s' intente nuevamente: "%var.type
            else:
                if  in_type == "int" : 
                    if  in_value > MAX_INT or  in_value < - MAX_INT :
                        overflow_error(self.var_to_read.lineno, self.var_to_read.lexpos)
                
            if mensaje: in_type = "" 
        
        var.value = in_value # Actualiz.el valor de la var. en la tabla de simbolos
    
class Assign(Expre):
    
    def __init__(self, identifier, expression):
        Expre.__init__(self)
        self.type = "ASSIGN"
        self.id = identifier
        self.expression = expression
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.id.print_tree(level + 1)
        self.print_with_indent('value',level + 1)
        self.expression.print_tree(level + 2)
    
    def check_types(self, symbolTable):
        self.id.check_types(symbolTable)
        symbol = symbolTable.lookup(self.id.name)
        if symbol is not None:
            type_expres = self.expression.check_types(symbolTable)
            
            if type_expres ==  "" : return ""

            if symbol.type != type_expres:
                static_error(self.lineno, self.lexpos,
                                "No se puede asignar expresiones de tipo '%s' a la variable '%s' de tipo '%s'." \
                                     % (type_expres,self.id.name,symbol.type) )
            
            if "o" not in symbol.type_edit:
                static_error(self.id.lineno,self.id.lexpos,
                                 "La variable %s es de solo lectura." % (self.id.name) )
                
    def execute(self, symbolTable):
        value = self.expression.evaluate(symbolTable)
        symbolTable.update(self.id.name, value)
                  
class If(Expre):
    
    def __init__(self,condition,statement_if, statement_else = None):
        Expre.__init__(self)
        self.type = 'IF'
        self.condition = condition
        self.statement_if   = statement_if
        self.statement_else = statement_else
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent("condition",level+1)
        self.condition.print_tree(level + 2)
        
        self.print_with_indent('THEN', level+1)
        self.statement_if.print_tree(level + 2)
        
        if self.statement_else is not None:
            self.print_with_indent('ELSE',level)
            self.statement_else.print_tree(level + 1)
            
        self.print_with_indent('END_IF',level)
    
    def check_types(self, symbolTable):        
        type_cond = self.condition.check_types(symbolTable)
 
        if  type_cond != "bool":
            if type_cond == "":
                static_error(self.condition.lineno, self.condition.lexpos,
                                  "InstrucciÃ³n 'if' espera expresiones de tipo 'bool'.")
            else:
                static_error(self.condition.lineno,self.condition.lexpos,
                                  "InstrucciÃ³n 'if' espera expresiones de tipo 'bool', no de tipo '%s'." % type_cond)
        
        self.statement_if.check_types(symbolTable)
        if self.statement_else is not None:
            self.statement_else.check_types(symbolTable)
    
    def execute(self, symbolTable):
        condition = self.condition.evaluate(symbolTable)
        if condition:
            self.statement_if.execute(symbolTable)
        else:
            if self.statement_else is not None:
                self.statement_else.execute(symbolTable)
    
class For(Expre):
    
    def __init__(self,identifier,direction, expression , statement):
        Expre.__init__(self)
        self.type = 'FOR'
        self.identifier = identifier
        self.direction  = direction
        self.expression = expression
        self.statement  = statement
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.identifier.print_tree(level + 1)
        self.direction.print_tree(level + 1)
        
        self.print_with_indent('IN',level + 1)
        self.expression.print_tree(level + 1)

        self.print_with_indent('DO',level + 1)
        self.statement.print_tree(level + 2)
        self.print_with_indent('END_FOR',level)
    
    def check_types(self, symbolTable):
        type_expre = self.expression.check_types(symbolTable)
        #self.identifier.check_types(symbolTable) # Esto hay que hacerlo??
        if type_expre != "set":
            if type_expre == "":
                static_error(self.expression.lineno,self.expression.lexpos,
                               "La expression de un for debe ser de tipo 'set'")
            else:                          
                static_error(self.expression.lineno,self.expression.lexpos,
                                "La expression de un for debe ser de " +\
                                   "tipo 'set' no de tipo '%s'." % type_expre)
                
        symbolTable.add_scope() # Crea un nuevo alcance
        symbolTable.insert(self.identifier.name,"int","i") # Creacion simbolo de solo lectura
        self.statement.check_types(symbolTable)
        symbolTable.delete_scope() # Eliminar alcance saliendo del For
    
    def execute(self, symbolTable):
        set_iterator = self.expression.evaluate(symbolTable) # Conjunto a iterar
        direction = self.direction.evaluate(symbolTable)     # Direccion
        
        # Si es min, se ordena de forma ascendente. Si es max, en forma descendente
        if direction == "min":
            set_iterator = sorted(set_iterator)
        else: 
            set_iterator = sorted(set_iterator, reverse=True) 
        
        symbolTable.add_scope() # Crea un nuevo alcance
        symbolTable.insert(self.identifier.name,"int","i")   # Creacion simbolo de solo lectura
        var = symbolTable.lookup(self.identifier.name)       # Variable de iteracion  
        
        for i in set_iterator:
            symbolTable.update(var.name, i)     # Actualiza valor tabla simbolos
            self.statement.execute(symbolTable)
            
        symbolTable.delete_scope() # Eliminar alcance saliendo del For
        
class RepeatWhileDo(Expre):
    
    def __init__(self,statement1,expression,statement2):
        Expre.__init__(self)
        self.type = 'REPEAT'
        self.statement1 = statement1
        self.expression  = expression
        self.statement2 = statement2
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.statement1.print_tree(level + 1)
        
        self.print_with_indent('WHILE',level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

        self.print_with_indent('DO',level)
        self.statement2.print_tree(level + 1)
      
    def check_types(self, symbolTable):
        self.statement1.check_types(symbolTable)
        
        type_expre = self.expression.check_types(symbolTable)
        if type_expre != "bool":
            if type_expre == "":
                static_error(self.expression.lineno,self.expression.lexpos,
                                "Condicion del 'while' debe ser de tipo 'bool'.")
            else:
                static_error(self.expression.lineno,self.expression.lexpos,
                                  "Condicion del 'while' debe ser de tipo 'bool', no de tipo '%s'." % type_expre)
        
        self.statement2.check_types(symbolTable)
    
    def execute(self, symbolTable):
        self.statement1.execute(symbolTable)
        while(self.expression.evaluate(symbolTable)):
            self.statement2.execute(symbolTable)
            self.statement1.execute(symbolTable) 
               
class WhileDo(Expre):
    
    def __init__(self,expression,statement):
        Expre.__init__(self)
        self.type = 'WHILE'
        self.expression  = expression
        self.statement = statement
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

        self.print_with_indent('DO',level)
        self.statement.print_tree(level + 1)
        self.print_with_indent('END_WHILE',level)
    
    def check_types(self, symbolTable):
        type_expre = self.expression.check_types(symbolTable)
        if type_expre != "bool":
            if type_expre == "":
                static_error(self.expression.lineno, self.expression.lexpos,
                                "Condicion del 'while' debe ser de tipo 'bool'.")
            else:                          
                static_error(self.expression.lineno,self.expression.lexpos,
                                "Condicion del 'while' debe ser de " +\
                                    "tipo 'bool' no de tipo '%s'." % type_expre)
        
        self.statement.check_types(symbolTable)
    
    def execute(self, symbolTable):
        while(self.expression.evaluate(symbolTable)):
            self.statement.execute(symbolTable)
            
class RepeatWhile(Expre):
    
    def __init__(self,statement,expression):
        Expre.__init__(self)
        self.type = 'REPEAT'
        self.statement = statement
        self.expression  = expression
        
    def print_tree(self,level): 
        self.print_with_indent(self.type,level)
        self.statement.print_tree(level + 1)

        self.print_with_indent('WHILE',level)
        self.print_with_indent('condition',level + 1)
        self.expression.print_tree(level + 2)

    def check_types(self, symbolTable):
        self.statement.check_types(symbolTable)
        type_expre = self.expression.check_types(symbolTable)
        if type_expre != "bool":
            if type_expre == "":
                static_error(self.expression.lineno,self.expression.lexpos,
                                "Condicion del 'while' debe ser de tipo 'bool'.")
            else:                          
                static_error(self.expression.lineno,self.expression.lexpos,
                                "Condicion del 'while' debe ser de" +\
                                    "tipo 'bool' no de tipo '%s'." % type_expre)
    
    def execute(self, symbolTable):
        self.statement.execute(symbolTable)
        while(self.expression.evaluate(symbolTable)):
            self.statement.execute(symbolTable)
        
class Print(Expre):
    
    def __init__(self,type_print,lista_to_print):
        Expre.__init__(self)
        self.type = type_print
        self.lista_to_print = lista_to_print
        
    def print_tree(self,level): 
        self.print_with_indent(self.type.upper(), level)
        for var in self.lista_to_print:
            var.print_tree(level + 1)
 
    def check_types(self, symbolTable):
        for exp in self.lista_to_print:
            exp.check_types(symbolTable)
            
        return self.type
    
    def execute(self, symbolTable):
        out = ""
        for exp in self.lista_to_print:
            out = out + to_string(exp.evaluate(symbolTable))
            
        
        if self.type == "print":
            interpreter_result.append(out+" ")
        else:
            interpreter_result.append(out +"\n")
            out += "\n"
        sys.stdout.write(out)
        sys.stdout.flush() # Para que los muestre inmediatamente si aun no lo ha hecho
    
class Block(Expre):
    
    def __init__(self, list_st,declare = None): 
        Expre.__init__(self)
        self.type = "BLOCK"
        self.list_st = list_st
        self.declare = declare
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)
        
        if self.declare is not None:
            self.declare.print_tree(level + 1)

        for stat in self.list_st:
            stat.print_tree(level + 1)
            
        self.print_with_indent("BLOCK_END", level)
    
    def check_types(self, symbolTable):    
       
        if self.declare: # Vemos si el bloque tiene declaraciones
            symbolTable.add_scope() # Si el bloque tiene declaraciones, se agrega una nueva tabla
            self.declare.check_types(symbolTable)            
        
        for stat in self.list_st:
            stat.check_types(symbolTable)
        
        if self.declare: # Si hubo declaraciones, se desempila una tabla
            symbolTable.delete_scope()
    
    def execute(self, symbolTable):
        
        if self.declare:            # Vemos si el bloque tiene declaraciones
            symbolTable.add_scope() # Si posee declaraciones, se agrega una nueva tabla
            self.declare.execute(symbolTable)            
        
        for stat in self.list_st:
            stat.execute(symbolTable)
        
        if self.declare: # Si hubo declaraciones, se desempila una tabla
            symbolTable.delete_scope()
            
class Parenthesis(Expre):
    
    def __init__(self, expre):
        Expre.__init__(self)
        self.type = 'PARENTHESIS'
        self.condition = expre   
            
    def print_tree(self,level):  
        self.print_with_indent(self.type , level)
        self.condition.print_tree(level + 1)
        self.print_with_indent('PARENTHESIS_CLOSE', level)
    
    def check_types(self, symbolTable):
        return self.condition.check_types(symbolTable)
    
    def evaluate(self, symbolTable):
        return self.condition.evaluate(symbolTable)
    
class BinaryOP(Expre):
    bin_operators = {   
        # Int Operators
         "PLUS +"         : sum1,
         "MINUS -"        : minus,
         "TIMES *"        : times,
         "INTDIVISION /"  : int_division,
         "RESTDIVISION %" : rest_division,
         # Bool Operators
         "UNEQUAL /="        : unequal,
         "EQUALBOOL =="      : equal,
         "LESSTHAN <"        : less,
         "LESSOREQUALTHAN <=": less_equal,
         "GREATERTHAN >"     : greater,
         "GREATEROREQUALTHAN >=" : greater_equal,
         
         "and"    : binary_and,
         "or"     : binary_or,
         # Set Operators
         "UNION ++"        : union,
         "DIFFERENCE \\"   : difference,
         "INTERSECTION ><" : intersection,
         # int and set Operators
         "MAPPLUS <+>"     : map_plus,
         "MAPMINUS <->"    : map_minus,
         "MAPTIMES <*>"    : map_times, 
         "MAPDIVIDE </>"   : map_divide,
         "MAPREST <%>"     : map_rest,
         "BELONG @"        : belong
    }
    
    def __init__(self,expre1,type_op,expre2):
        Expre.__init__(self)
        self.expre1  = expre1
        self.type_op = type_op
        self.expre2  = expre2
        
    def print_tree(self,level):  
        self.print_with_indent(self.type_op, level)
        self.expre1.print_tree(level + 1)
        self.expre2.print_tree(level + 1)
            
    def check_types(self, symbols):
        #Check type for BinaryOP
        pass
    
    def evaluate(self, symbolTable):
        value1 = self.expre1.evaluate(symbolTable)
        value2 = self.expre2.evaluate(symbolTable)
        try:
            result = BinaryOP.bin_operators[self.type_op](value1, value2) # Evaluacion de funciones
        
        except(AssertionError):
            overflow_error(self.lineno, self.lexpos)
        except(ZeroDivisionError):
            zero_division_error(self.lineno, self.lexpos)
        
        return result
    
class BinaryOpInteger(BinaryOP):
    ''' 
    Integer Binary Operator
    ("PLUS +","MINUS -","TIMES *","INTDIVISION /","RESTDIVISION %")
    '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "int"):
            static_error(self.lineno,self.lexpos,
                            "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-1],type_expre1,type_expre2) )
            return "" 
          
        return "int"
        
class BinaryOpEquals(BinaryOP):
    ''' Equals Binary Operator ("UNEQUAL /=","EQUALBOOL ==") '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not ((type_expre1 == "bool" and type_expre2 == "bool") or \
                (type_expre1 == "set" and type_expre2 == "set")   or \
                (type_expre1 == "int" and type_expre2 == "int")) : 
            static_error(self.lineno,self.lexpos,
                            "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2))
            return "" 
             
        return "bool"

class BinaryOpLessGreater(BinaryOP):
    '''
    Binary Compare Operator 
    ("LESSTHAN <","LESSOREQUALTHAN <=","GREATERTHAN >","GREATEROREQUALTHAN >=")
    '''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "int") : 
            static_error(self.lineno,self.lexpos,
                            "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2) )
            return "" 
            
        return "bool"
    
class BinaryOpBelong(BinaryOP):
    ''' Belong Binary Operator "BELONG @" '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "set") : 
            static_error(self.lineno,self.lexpos,
                            "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-1],type_expre1,type_expre2) )
            return "" 
             
        return "bool" 

class BinaryOpBool(BinaryOP):
    ''' "and" , "or" Binary boolean operator'''    
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "bool" and type_expre2 == "bool") :    
            static_error(self.lineno, self.lexpos,
                          "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op,type_expre1,type_expre2) )
            return ""
             
        return "bool"       

class BinaryOpSet(BinaryOP):
    ''' Set binary op ("UNION ++","DIFFERENCE \\","INTERSECTION ><")'''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""

        if not (type_expre1 == "set" and type_expre2 == "set") : 
            static_error(self.lineno ,self.lexpos, 
                            "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2))
            return "" 
             
        return "set"
    
class BinaryOpMapToSet(BinaryOP):
    '''
    Map to Set Binary Operator
    ("MAPPLUS <+>","MAPMINUS <->","MAPTIMES <*>","MAPDIVIDE </>","MAPREST <%>")
    '''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "set") : 
            static_error(self.lineno,self.lexpos,
                            "Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-3:],type_expre1,type_expre2))
            return "" 
             
        return "set" 
    
class UnaryOP(Expre):
    ''' Unary Operator for Inheritance'''
    unary_operators = {
        "not"      : bool_not,   # Bool Operator
        "NEGATE -" : int_negate, # Integer Operator
        #Unary set Operator 
        "MAXVALUESET >?" : max_value_set,
        "MINVALUESET <?" : min_value_set,
        "SIZESET $?"     : size_set,
    }
    def __init__(self, type_op,expre1):
        Expre.__init__(self)
        self.type_op = type_op
        self.expre1  = expre1
            
    def print_tree(self,level):   
        self.print_with_indent(self.type_op , level)
        self.expre1.print_tree(level + 1)
           
    def check_types(self, symbols):
        # For type checking
        pass
    
    def evaluate(self, symbolTable):
        value = self.expre1.evaluate(symbolTable)
        try:
            result = UnaryOP.unary_operators[self.type_op](value)
        
        except(AssertionError):
            overflow_error(self.lineno, self.lexpos)
        except(ValueError):
            empty_set_error(self.lineno, self.lexpos)
        return result
        
class UnaryOpUminus(UnaryOP):
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""

        if type_expre != "int":
            static_error(self.lineno, self.lexpos,
                            "Operador unario '-' solo se puede aplicar a enteros" +\
                                 " no a expresiones del tipo '%s'" % type_expre)
            return ""
        
        return "int"

class UnaryOpNot(UnaryOP):
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""
        
        if type_expre != "bool":
            static_error(self.lineno, self.lexpos,
                            "Operador unario 'not' solo se puede aplicar a expresiones booleanas" +\
                                 " no a expresiones del tipo '%s'" % type_expre)
            return ""
          
        return "bool"

class UnaryOpSet(UnaryOP):
    ''' Unary set Operator ("MAXVALUESET >?","MINVALUESET <?","SIZESET $?")'''
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""
        
        if type_expre != "set":
            static_error(self.lineno, self.lexpos,
                            "Operador unario '%s' solo se puede aplicar a conjuntos" +\
                                 " no a expresiones del tipo '%s'" % (self.type_op[-2:],type_expre))
            return ""
            
        return "int"
    
class DeclareList(Expre):
    
    def __init__(self,declared_list):
        Expre.__init__(self)
        self.declared_list = declared_list
        
    def print_tree(self,level):
        self.print_with_indent('USING', level)
        for declaration_vars in self.declared_list:
            declaration_vars.print_tree(level)
        self.print_with_indent('IN', level)
        
    def check_types(self, symbolTable):
        for declaration_vars in self.declared_list:
            declaration_vars.check_types(symbolTable)
            
    def execute(self, symbolTable):
        for declaration_vars in self.declared_list:
            declaration_vars.execute(symbolTable)
    
class TypeList(Expre):
    
    def __init__(self,data_type,id_list):
        Expre.__init__(self)
        self.data_type = data_type
        self.id_list = id_list
    
    def print_tree(self,level):
        for identifier in self.id_list:
            self.print_with_indent(self.data_type + ' ' + identifier.name,level + 1)
    
    def check_types(self, symbolTable):
        for var in self.id_list:
            
            if symbolTable.contains(var.name):
                symbol = symbolTable.lookup(var.name)
                static_error(var.lineno, var.lexpos,
                                  "La variable '%s' ya ha sido declarada en este alcance " % (var.name) + \
                                    'en la linea %d, columna %d con tipo %s.' % \
                                        (symbol.ref.lineno,
                                            get_column_text_lexpos(symbol.ref.lexpos),
                                                symbol.type) )
            else:
                symbolTable.insert(var.name, self.data_type,'i/o',var)
        
    def execute(self, symbolTable):
        for var in self.id_list:
            symbolTable.insert(var.name, self.data_type,'i/o',var)
        
class Direction(Expre):
    
    def __init__(self,value):
        Expre.__init__(self)
        self.type = 'direction'
        self.value = value
        
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)
        
    def check_types(self, symbolTable):
        return self.value
    
    def evaluate(self, symbolTable):
        return self.value

class Set(Expre):
    
    def __init__(self, list_st): 
        Expre.__init__(self)
        self.type = "set"
        self.list_st = list_st
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)

        for exp in self.list_st:
            exp.print_tree(level + 1)
            
    def check_types(self, symbolTable):
        error = False
        for exp in self.list_st:
            type_expre = exp.check_types(symbolTable)
            if type_expre != "int":
                if type_expre != "":
                    static_error(exp.lineno, exp.lexpos,
                          "Los conjuntos solamente pueden contener elementos de tipo 'int' " + \
                          "se obtuvo un elemento de tipo '%s'" %(type_expre))
                else:
                    static_error(exp.lineno, exp.lexpos,
                          "Los conjuntos solamente pueden contener elementos de tipo 'int' ")
                error = True
        
        if error:
            return ""
        else:      
            return self.type
        
    def evaluate(self, symbolTable):
        set_list = []
        for elem in self.list_st:
            value = elem.evaluate(symbolTable)
            set_list.append(value)
        
        return set(set_list)
    
class Bool(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = "bool"
        self.value = value
    
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

    def check_types(self, symbolTable):
        return self.type
    
    def evaluate(self, symbolTable):
        if self.value == "true":
            return True
        else:
            return False
    
class Integer(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = "int"
        self.value = value
        
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(str(self.value), level + 1)
        
    def check_types(self, symbolTable):
        return self.type
    
    def evaluate(self, symbolTable):
        return self.value
    
class String(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = "string"
        self.value = value
    
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)
        
    def check_types(self, symbolTable):
        return self.type
    
    def evaluate(self, symbolTable):
        return self.value
    
class Identifier(Expre):
    
    def __init__(self , name):        
        Expre.__init__(self)
        self.name = name
        self.type = ""
        
    def print_tree(self , level):       
        self.print_with_indent("identifier"  , level )
        self.print_with_indent(self.name , level + 1 )
        
    def check_types(self, symbolTable):
        symbol = symbolTable.lookup(self.name)
        if symbol is None:
            static_error(self.lineno, self.lexpos,
                            "La variable '%s' aun no ha sido declarada."  % self.name)
        else:
            self.type = symbol.type
        return self.type
    
    def evaluate(self, symbolTable):
        symbol = symbolTable.lookup(self.name) 
        return symbol.value
    
############################  ERROR_HANDLING  ################################

def static_error(lineno,lexpos,message):
    error =  "Error en la linea %d, columna %d: %s" % \
                (lineno, get_column_text_lexpos(lexpos),message)
    
    static_errors.append(error)
        
def overflow_error(lineno, lexpos):
    print "Error en la linea %d, columna %d: Overflow." %\
                (lineno, get_column_text_lexpos(lexpos))
    exit()
    
def empty_set_error(lineno, lexpos):
    print "Error en la linea %d, columna %d: conjunto vacio." %\
                (lineno, get_column_text_lexpos(lexpos))
    exit()

def zero_division_error(lineno, lexpos):
    print "Error en la linea %d, columna %d: Division por cero." %\
            (lineno, get_column_text_lexpos(lexpos))
    exit()
    
def parsear_string(string_raw):
    i=0
    start_scape = False 
    out = ""
    
    while i < len(string_raw):
        if string_raw[i] == "\\" : # Si es el comienzo de un backlslash
            if start_scape: # Si resultaba ser el final de un backlslash
                out += "\\"
            start_scape = not start_scape
        elif start_scape: # Si este es un segundo caracter despues de un backslash
            if string_raw[i] == "\"": # Si es una comilla
                out += "\""
                
            elif string_raw[i] == "n": # Si es un salto de linea
                out += "\n"
            
            else: # Sie es un caracter no especial
                out += "\%c" % string_raw[i]
            
            start_scape = False # se deja de esperar por caracteres escapados
        else:
            out += string_raw[i]
        i += 1
    
    return out

def to_string(elem):
    if type(elem) is set:
        if len(elem) == 0:
            out = "{}"
        else:
            out = "{"
            for x in sorted(elem): # Imprimir elementos en orden ascendente
                out += "%d," % x
            
            out = out[:-1]+"}" # Remover ultima "," y cerrar el conjunto
            
    elif type(elem) is bool:
        if elem:
            out = "true"
        else:
            out = "false"
    elif type(elem) is str:
        out = parsear_string(elem)
    elif type(elem) is int:
        out = str(elem)

    return out