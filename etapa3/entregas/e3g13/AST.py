# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonathan Ng 11-10199
         Manuel Gonzalez 11-10390
    
    Clases para la representación de un Arbol abstracto del lenguaje setlan
'''

from symbol_table import SymbolTable ,Symbol
from expresiones import obtener_columna_texto_lexpos

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
    
    def fetch_symbols(self,context_parent,symbols):
        pass
    
    def check_types(self,symbols):
        pass

class Program(Expre):
    
    def __init__(self, statement):
        Expre.__init__(self)
        self.type = "PROGRAM"
        self.statement = statement
        self.symbols = SymbolTable()
        
    def print_tree(self,level = 0):
        self.print_with_indent(self.type, level)
        self.statement.print_tree(level + 1)
    
    def fetch_symbols(self):
        self.statement.fetch_symbols(-1,self.symbols)
        
    def check_types(self):
        self.statement.check_types(self.symbols)
        
class Scan(Expre):
    
    def __init__(self,id_):
        Expre.__init__(self)
        self.type = 'SCAN'
        self.var_to_read = id_
    
    def print_tree(self , level):
        self.print_with_indent(self.type,level)
        self.var_to_read.print_tree(level + 1)

    def fetch_symbols(self, context_parent, symbols):
        self.var_to_read.fetch_symbols(context_parent,symbols)
    
    def check_types(self, symbols):
        type_var = self.var_to_read.check_types(symbols)
        if type_var == "": return ""
        
        if type_var not in ('int','bool'):
            symbols.append_error((self.var_to_read.lineno,self.var_to_read.lexpos,"'SCAN' solo se puede usar para variables de tipo 'int' o 'bool' . '%s' es de tipo '%s'" % \
                            (self.var_to_read.name,type_var)))
        
class Assign(Expre):
    
    def __init__(self, identifier,expresion):
        Expre.__init__(self)
        self.type = "ASSIGN"
        self.id = identifier
        self.expresion = expresion
        self.context_parent = -1
        
    def print_tree(self,level):
        self.print_with_indent(self.type,level)
        self.id.print_tree(level + 1)
        self.print_with_indent('value',level + 1)
        self.expresion.print_tree(level + 2)
    
    def fetch_symbols(self, context_parent, symbols):
        self.context_parent = context_parent
        
        self.id.fetch_symbols(context_parent,symbols)
        self.expresion.fetch_symbols(context_parent,symbols)
    
    def check_types(self, symbols):
        symbol = symbols.lookup(self.id.name,self.context_parent)
        if symbol is not None:
            type_expres = self.expresion.check_types(symbols)
            
            if type_expres ==  "" : return ""

            if symbol.type != type_expres:
                symbols.append_error((self.lineno,self.lexpos,
                                      "No se puede asignar expresiones de tipo '%s' a la variable '%s' de tipo '%s'." % (type_expres,self.id.name,symbol.type)))
            
            if "o" not in symbol.type_edit:
                symbols.append_error((self.id.lineno,self.id.lexpos,
                                      "La variable %s es de solo lectura." % (self.id.name)))
                
                    
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
    
        
    def fetch_symbols(self,context_parent,symbols):        
        self.condition.fetch_symbols(context_parent,symbols)
        self.statement_if.fetch_symbols(context_parent, symbols)
        
        if self.statement_else is not None:
            self.statement_else.fetch_symbols(context_parent,symbols)
            
    def check_types(self,symbols):
        type_cond = self.condition.check_types(symbols)
        if  type_cond != "bool":
            if type_cond == "":
                symbols.append_error((self.lineno,self.lexpos,
                                  "Instrucción 'if' espera expresiones de tipo 'bool'."))
            else:
                symbols.append_error((self.lineno,self.lexpos,
                                  "Instrucción 'if' espera expresiones de tipo 'bool', no de tipo '%s'." % type_cond))
        
        self.statement_if.check_types(symbols)
        if self.statement_else is not None:
            self.statement_else.check_types(symbols)

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
    
    def fetch_symbols(self, context_parent, symbols):
        
        self.context = symbols.add_context()            
        if context_parent != -1:
            symbols.add_child(context_parent,self.context)
        symbols.insert(Symbol(self.identifier.name,"int",0,self.context,"i"))
        
        self.identifier.fetch_symbols(self.context,symbols)
        self.expression.fetch_symbols(self.context,symbols)
        self.statement.fetch_symbols(self.context,symbols)
    
    def check_types(self, symbols):
        type_expre = self.expression.check_types(symbols)
        if type_expre != "set":
            if type_expre == "":
                symbols.append_error((self.lineno,self.lexpos,"La expresion de un for debe ser de tipo 'set'"))
            else:                          
                symbols.append_error((self.lineno,self.lexpos,"La expresion de un for debe ser de " +\
                                 "tipo 'set' no de tipo '%s'." % type_expre))
                
        self.statement.check_types(symbols)

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
        
    def fetch_symbols(self, context_parent, symbols):
        self.statement1.fetch_symbols(context_parent,symbols)
        self.expression.fetch_symbols(context_parent,symbols)
        self.statement2.fetch_symbols(context_parent,symbols)
        
    def check_types(self, symbols):
        self.statement1.check_types(symbols)
        
        type_expre = self.expression.check_types(symbols)
        if type_expre != "bool":
            if type_expre == "":
                symbols.append_error((self.lineno,self.lexpos,"Condicion del 'while' debe ser de tipo 'bool'."))
            else:
                symbols.append_error((self.lineno,self.lexpos,
                                  "Condicion del 'while' debe ser de tipo 'bool', no de tipo '%s'." % type_expre))
        
        self.statement2.check_types(symbols)
        
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
        
    def fetch_symbols(self, context_parent, symbols):
        self.expression.fetch_symbols(context_parent,symbols)
        self.statement.fetch_symbols(context_parent,symbols)
    
    def check_types(self, symbols):
        type_expre = self.expression.check_types(symbols)
        if type_expre != "bool":
            if type_expre == "":
                symbols.append_error((self.lineno,self.lexpos,"Condicion del 'while' debe ser de tipo 'bool'."))
            else:                          
                symbols.append_error((self.lineno,self.lexpos,"Condicion del 'while' debe ser de" +\
                                 "tipo 'bool' no de tipo '%s'." % type_expre))
        
        self.statement.check_types(symbols)
    
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

    def fetch_symbols(self, context_parent, symbols):
        self.statement.fetch_symbols(context_parent,symbols)
        self.expression.fetch_symbols(context_parent,symbols)

    def check_types(self, symbols):
        self.statement.check_types(symbols)
        type_expre = self.expression.check_types(symbols)
        if type_expre != "bool":
            if type_expre == "":
                symbols.append_error((self.lineno,self.lexpos,"Condicion del 'while' debe ser de tipo 'bool'."))
            else:                          
                symbols.append_error((self.lineno,self.lexpos,"Condicion del 'while' debe ser de" +\
                                 "tipo 'bool' no de tipo '%s'." % type_expre))       
    
class Print(Expre):
    
    def __init__(self,type_print,lista_to_print):
        Expre.__init__(self)
        self.type = type_print.upper()
        self.lista_to_print = lista_to_print
        
    def print_tree(self,level): 
        self.print_with_indent(self.type, level)
        for var in self.lista_to_print:
            var.print_tree(level + 1)
    
    def fetch_symbols(self, context_parent, symbols):
        for var in self.lista_to_print:
            var.fetch_symbols(context_parent,symbols)    
     
    def check_types(self, symbols):
        for exp in self.lista_to_print:
            exp.check_types(symbols)
            
        return self.type
           
class Block(Expre):
    
    def __init__(self, list_st,declare = None): 
        Expre.__init__(self)
        self.type = "BLOCK"
        self.list_st = list_st
        self.declare = declare
        #self.declare.convert_identifier()
        self.context = -1
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)
        
        if self.declare is not None:
            self.declare.print_tree(level + 1)

        for stat in self.list_st:
            stat.print_tree(level + 1)
            
        self.print_with_indent("BLOCK_END", level)
    
    def fetch_symbols(self , context_parent , symbols):
        
        self.context = symbols.add_context()            
        if context_parent != -1:
            symbols.add_child(context_parent,self.context)
        
        if self.declare is not None:
            self.declare.add_to_symbols(self.context,symbols)
        
        for stat in self.list_st:
            stat.fetch_symbols(self.context , symbols)
    
    def check_types(self,symbols):
        for stat in self.list_st:
            stat.check_types(symbols)
    
class Parenthesis(Expre):
    
    def __init__(self, expre):
        Expre.__init__(self)
        self.type = 'PARENTHESIS'
        self.condition = expre   
            
    def print_tree(self,level):  
        self.print_with_indent(self.type , level)
        self.condition.print_tree(level + 1)
        self.print_with_indent('PARENTHESIS_CLOSE', level)
    
    def fetch_symbols(self, context_parent, symbols):
        self.condition.fetch_symbols(context_parent, symbols)
    
    def check_types(self, symbols):
        return self.condition.check_types(symbols)
    
class BinaryOP(Expre):
    
    def __init__(self,expre1,type_op,expre2):
        Expre.__init__(self)
        self.expre1  = expre1
        self.type_op = type_op
        self.expre2  = expre2
        self.context_parent = -1
        
    def print_tree(self,level):  
        self.print_with_indent(self.type_op, level)
        self.expre1.print_tree(level + 1)
        self.expre2.print_tree(level + 1)
      
    def fetch_symbols(self , context_parent , symbols):
        self.context_parent = context_parent
        self.expre1.fetch_symbols(context_parent,symbols)
        self.expre2.fetch_symbols(context_parent,symbols)
            
    def check_types(self, symbols):
        #Check type for BinaryOP
        pass
    
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
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-1],type_expre1,type_expre2)))
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
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2)))
            return "" 
             
        return "bool"

class BinaryOpLessGreater(BinaryOP):#######Listo
    '''
    Binary Compare Operator 
    ("LESSTHAN <","LESSOREQUALTHAN <=","GREATERTHAN >","GREATEROREQUALTHAN >=")
    '''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "int") : 
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2)))
            return "" 
            
        return "bool"
    
class BinaryOpBelong(BinaryOP):
    ''' Belong Binary Operator "BELONG @" '''
    def check_types(self,symbols):
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "int" and type_expre2 == "set") : 
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-1],type_expre1,type_expre2)))
            return "" 
             
        return "bool" 

class BinaryOpBool(BinaryOP):
    ''' "and" , "or" Binary boolean operator'''    
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""
        
        if not (type_expre1 == "bool" and type_expre2 == "bool") :    
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op,type_expre1,type_expre2)))
            return ""
             
        return "bool"       

class BinaryOpSet(BinaryOP):
    ''' Set binary op ("UNION ++","DIFFERENCE \\","INTERSECTION ><")'''
    def check_types(self,symbols):       
        type_expre1 = self.expre1.check_types(symbols)
        type_expre2 = self.expre2.check_types(symbols)
        if type_expre1 == "" or type_expre2 == "": return ""

        if not (type_expre1 == "set" and type_expre2 == "set") : 
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-2:],type_expre1,type_expre2)))
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
            symbols.append_error((self.lineno,self.lexpos,"Operando '%s' no sirve con operandos de tipo '%s' y '%s'." % \
                                (self.type_op[-3:],type_expre1,type_expre2)))
            return "" 
             
        return "set" 
    
class UnaryOP(Expre):
    ''' Unary Operator for Inheritance'''
    def __init__(self, type_op,expre1):
        Expre.__init__(self)
        self.type_op = type_op
        self.expre1  = expre1
            
    def print_tree(self,level):   
        self.print_with_indent(self.type_op , level)
        self.expre1.print_tree(level + 1)
        
    def fetch_symbols(self, context_parent, symbols):
        self.expre1.fetch_symbols(context_parent, symbols)
        
    def check_types(self, symbols):
        # For type checking
        pass
    
class UnaryOpUminus(UnaryOP):
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""

        if type_expre != "int":
            symbols.append_error((self.lineno,self.lexpos,"Operador unario '-' solo se puede aplicar a enteros" +\
                                 " no ha expresiones del tipo '%s'" % type_expre))
            return ""
        
        return "int"

class UnaryOpNot(UnaryOP):
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""
        
        if type_expre != "bool":
            symbols.append_error((self.lineno,self.lexpos,"Operador unario 'not' solo se puede aplicar a expresiones booleanas" +\
                                 " no ha expresiones del tipo '%s'" % type_expre))
            return ""
          
        return "bool"

class UnaryOpSet(UnaryOP):
    ''' Unary set Operator ("MAXVALUESET >?","MINVALUESET <?","SIZESET $?")'''
    def check_types(self, symbols):
        type_expre = self.expre1.check_types(symbols)
        if type_expre == "": return ""
        
        if type_expre != "set":
            symbols.append_error((self.lineno,self.lexpos,"Operador unario '%s' solo se puede aplicar a conjuntos" +\
                                 " no a expresiones del tipo '%s'" % (self.type_op[-2:],type_expre)))
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
        
    def add_to_symbols(self,context,symbols):
        for declaration_vars in self.declared_list:
            declaration_vars.add_to_symbols(context,symbols)
    
class TypeList(Expre):
    
    def __init__(self,data_type,id_list):
        Expre.__init__(self)
        self.data_type = data_type
        self.id_list = id_list
    
    def print_tree(self,level):
        for identifier in self.id_list:
            self.print_with_indent(self.data_type + ' ' + identifier.name,level + 1)
    
    def add_to_symbols(self,context_parent,symbols):
        if self.data_type == "int":
            default = 0
        elif self.data_type == "bool":
            default = False
        elif self.data_type == "set":
            default = []
            
        for identifier in self.id_list:    
            symbol_to_add = Symbol(identifier.name,self.data_type,default,context_parent,'i/o',identifier)
            symbol = symbols.lookup(identifier.name,context_parent)
            if symbols.contains(identifier.name,context_parent):
                symbols.append_error((identifier.lineno,identifier.lexpos,
                                      "La variable '%s' ya ha sido declarada en este alcance " % symbol_to_add.name + \
                                      'en la linea %d, columna %d con tipo %s.' % (symbol.ref.lineno,\
                                                                                      obtener_columna_texto_lexpos(symbol.ref.lexpos),
                                                                                      symbol.type)))
            else:
                symbols.insert(symbol_to_add)
        
        return True
    
class Direction(Expre):
    
    def __init__(self,value):
        Expre.__init__(self)
        self.type = 'direction'
        self.value = value
        
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

class Set(Expre):
    
    def __init__(self, list_st): 
        Expre.__init__(self)
        self.type = 'set'
        self.list_st = list_st
        
    def print_tree(self,level):
        self.print_with_indent(self.type, level)

        for exp in self.list_st:
            exp.print_tree(level + 1)
            
    def check_types(self, symbols):
        for exp in self.list_st:
            exp.check_types(symbols)
            
        return self.type
            
class Bool(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = 'bool'
        self.value = value
    
    def print_tree(self , level):
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)

    def check_types(self, symbols):
        return self.type
    
class Integer(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = 'int'
        self.value = value
        self.context_parent = -1
        
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(str(self.value), level + 1)
        
    def check_types(self, symbols):
        return self.type
        
class String(Expre):
    
    def __init__(self , value):
        Expre.__init__(self)
        self.type = 'string'
        self.value = value
    
    def print_tree(self , level):  
        self.print_with_indent(self.type, level)
        self.print_with_indent(self.value, level + 1)
        
    def check_types(self, symbols):
        return self.type

class Identifier(Expre):
    
    def __init__(self , name):        
        Expre.__init__(self)
        self.name = name
        self.context_parent = -1
        self.type = ""
        
    def print_tree(self , level):       
        self.print_with_indent("identifier"  , level )
        self.print_with_indent(self.name , level + 1 )
    
    def fetch_symbols(self, context_parent, symbols):
        self.context_parent = context_parent
        symbol = symbols.lookup(self.name,self.context_parent)
        if symbol is  None:
            symbols.append_error((self.lineno,self.lexpos,"La variable '%s' aun no ha sido declarada."  % self.name))
        else:
            self.type = symbol.type
        
    def check_types(self,symbols):
        return self.type