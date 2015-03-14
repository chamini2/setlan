import config, sys
from st import SymbolTable, get_var_in_scope


class Program(object):
    def __init__(self, statement):
        self.statement = statement

    def execute(self):
        self.statement.execute()
        
    def repr(self):
        indent = 4
        if self.statement:
            sta = self.statement.__repr__() if not getattr(self.statement,'repr',None) else self.statement.repr(indent+4) 
            return 'Program\n' + indent*' ' + sta
        else:
            return 'Program\n'



class Statement(object): pass


class Assign(Statement):
    def __init__(self, variable, expression, lineno, column):
        self.variable = variable
        self.expression = expression
        self.lineno = lineno
        self.column = column

    def execute(self):
        SymbolTable.update(self.variable.name, self.expression.evaluate())

    def repr(self, indent): 
        var = self.variable.__repr__() if not getattr(self.variable,'repr', None) else self.variable.repr(indent+8)
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        return 'Assign\n' + indent*' ' + var + indent*' ' + 'Value\n' + (indent+4)*' ' + exp

    def typecheck(self):
        if isinstance(self.expression, Variable):
            var = get_var_in_scope(self.expression.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.expression.name+\
                    ' not defined in this scope, in line ' + str(self.lineno)+\
                    ', column ' + str(self.column)+'.\n'
        
        var = get_var_in_scope(self.variable.name)
        if not var:
            config.static_checking_errors += 'Error: Variable ' + self.variable.name+\
                ' not defined in this scope, in line ' + str(self.lineno)+\
                ', column ' + str(self.column)+'.\n'
        elif var.return_type != self.expression.return_type:
            config.static_checking_errors += 'Error: Incompatible types for statement '+\
                self.__class__.__name__+": '"+str(self.variable.return_type)+"' and '"+\
                str(self.expression.return_type)+"', in line "+str(self.lineno)+', column '+\
                str(self.column)+'.\n'
    


class Block(Statement):
    def __init__(self, statement_list, declarations=None):
        self.statement_list = statement_list
        self.declarations = declarations

    def execute(self):
        config.scopes_list.append(SymbolTable())
        if self.declarations != None:
            for (_,var_list) in self.declarations:
                for var in var_list:
                    config.scopes_list[len(config.scopes_list)-1].insert(var)
        for statement in self.statement_list:
            if statement != None: statement.execute()
        config.scopes_list.pop()
            
    def repr(self, indent):
        s = 'Block Start\n'
        if self.declarations:
            s += indent*' ' + 'Using\n'
            for var_list in self.declarations:
                datatype = var_list[0]
                for var in var_list[1]:
                    s += (indent+4)*' ' + datatype + '\n' + (indent+8)*' ' + var.repr(indent+12)
            s += indent*' ' + 'In\n'

        for statement in self.statement_list:
            sta = statement.__repr__() if not getattr(statement,'repr',None) else statement.repr(indent+4)
            if sta != 'None':
                s += indent*' ' + sta
        return s + (indent-4)*' ' + 'Block End\n'


class Scan(Statement):
    def __init__(self, variable, lineno, column):
        self.variable = variable
        self.lineno = lineno
        self.column = column
        
    def execute(self):
        SymbolTable.update(self.variable.name, raw_input())

    def repr(self, indent):
        var = self.variable.__repr__() if not getattr(self.variable,'repr',None) else self.variable.repr(indent+4)
        return 'Scan\n' + indent*' ' + var
    
    def typecheck(self):
        var = get_var_in_scope(self.variable.name)
        if not var:
            config.static_checking_errors += 'Error: Variable ' + self.variable.var_name+\
                ' not defined in this scope, in line ' + str(self.lineno)+\
                ', column ' + str(self.column)+'.\n'        
        elif var.return_type not in {'bool', 'int'} :
            config.static_checking_errors += 'Error: Incompatible type for statement '+\
                self.__class__.__name__ + ": '" + str(self.variable.return_type)+\
                "', in line "+str(self.variable.lineno)+', column ' + str(self.variable.column)+'.\n'


class Print(Statement):
    def __init__(self, print_list):
        self.print_list = print_list

    def execute(self):
        for e in self.print_list:
            if e.return_type == 'set': 
                s = '{'+','.join(map(lambda x: str(x), sorted(set(e.evaluate()))))+'}'
                sys.stdout.write(s)
                config.dynamic_checking_log += s
            else:
                s = str(e.evaluate())
                sys.stdout.write(s)
                config.dynamic_checking_log += s

    def repr(self, indent):
        return_string = self.__class__.__name__ + '\n'
        for element in self.print_list:
            e = element.__repr__() if not getattr(element,'repr',None) else element.repr(indent+4)
            return_string += indent*' ' + e
        return return_string


class Println(Print):
    def execute(self):
        Print.execute(self)
        sys.stdout.write('\n')
        config.dynamic_checking_log += '\n'


class If(Statement):
    def __init__(self, expression=None, statement1=None, statement2=None, lineno=None, column=None):
        self.expression = expression
        self.statement1 = statement1
        self.statement2 = statement2
        self.return_type = 'None'
        self.lineno = lineno
        self.column = column
    
    def execute(self):
        if self.expression.evaluate(): self.statement1.execute()
        elif self.statement2 != None: self.statement2.execute()
    
    def repr(self, indent):
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        sta_1 = self.statement1.__repr__() if not getattr(self.statement1,'repr',None) else self.statement1.repr(indent+8)
        s = 'If\n' + indent*' ' + 'Condition\n' + (indent+4)*' ' + exp + indent*' ' + 'Statement True\n' + (indent+4)*' ' + sta_1
        if self.statement2:
            sta_2 = self.statement2.__repr__() if not getattr(self.statement2,'repr',None) else self.statement2.repr(indent+8)
            return s + indent*' ' + 'Statement False\n' + (indent+4)*' ' + sta_2 + (indent-4)*' ' + 'End If\n'
        return s + (indent-4)*' ' + 'End If\n'

    def typecheck(self):
        if isinstance(self.expression, Variable):
            var = get_var_in_scope(self.expression.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.expression.name+\
                    ' not defined in this scope, in line ' + str(self.lineno)+\
                    ', column ' + str(self.column)+'.\n'
        if self.expression.return_type != 'bool':
            config.static_checking_errors += 'Error: Incompatible type for statement '+\
                self.__class__.__name__+": '"+str(self.expression.return_type)+\
                "', in line "+str(self.lineno)+', column '+str(self.column)+'.\n'
    

class For(Statement):
    def __init__(self, variable=None, order=None, expression=None, statement=None, lineno=None, column=None):
        self.variable = variable
        self.order = order
        self.expression = expression
        self.statement = statement
        self.lineno = lineno
        self.column = column

    def execute(self):
        config.scopes_list.append(SymbolTable())
        config.scopes_list[len(config.scopes_list)-1].insert(self.variable)
        for e in sorted(self.expression.evaluate(), reverse=True if self.order=='min' else False):
            SymbolTable.update(self.variable.name, e)
            self.statement.execute()
        config.scopes_list.pop()
        

    def repr(self, indent):
        var = self.variable.__repr__() if not getattr(self.variable,'repr',None) else self.variable.repr(indent+4)
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        sta = self.statement.__repr__() if not getattr(self.statement,'repr',None) else self.statement.repr(indent+8)
        return 'For\n' + indent*' ' + var + indent*' ' + 'Direction\n' + (indent+4)*' ' + self.order + '\n' + indent*' ' + 'In\n' + (indent+4)*' '  + exp + indent*' ' + 'Do\n' + (indent+4)*' ' + sta + (indent-4)*' ' + 'End For\n'

    def typecheck(self):
        if isinstance(self.expression, Variable):
            var = get_var_in_scope(self.expression.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.expression.name+\
                    ' not defined in this scope, in line ' + str(self.lineno)+\
                    ', column ' + str(self.column)+'.\n'
        if self.expression.return_type != 'set':
            config.static_checking_errors += 'Error: Incompatible type for statement '+\
                self.__class__.__name__+": '"+str(self.expression.return_type)+\
                "', in line "+str(self.lineno)+', column '+str(self.column)+'.\n'


class Repeat(Statement):
    def __init__(self, statement1=None, expression=None, statement2=None, lineno=None, column=None):
        self.statement1 = statement1
        self.expression = expression
        self.statement2 = statement2
        self.lineno = lineno
        self.column = column
    
    def execute(self):
        if self.statement1: self.statement1.execute()
        while self.expression.evaluate():
            if self.statement2: self.statement2.execute()
            if self.statement1: self.statement1.execute()
    
    def repr(self, indent):
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        if self.statement1:
            sta_1 = self.statement1.__repr__() if not getattr(self.statement1,'repr',None) else self.statement1.repr(indent+4)
            s = 'Repeat\n' + indent*' ' + sta_1 + (indent-4)*' ' + 'While\n' + indent*' ' + 'Condition\n' + (indent+4)*' ' + exp
            if self.statement2:
                sta_2 = self.statement2.__repr__() if not getattr(self.statement2,'repr',None) else self.statement2.repr(indent+4)
                return s + (indent-4)*' ' + 'Do\n' + indent*' ' + sta_2 + (indent-4)*' ' + 'End Repeat\n'
            else:
                return s + (indent-4)*' ' + 'End Repeat\n'
        else:
            sta_2 = self.statement2.__repr__() if not getattr(self.statement2,'repr',None) else self.statement2.repr(indent+8)
            return 'While\n' + indent*' ' + 'Condition\n' + (indent+4)*' ' + exp + indent*' ' + 'Do\n' + (indent+4)*' ' +  sta_2 + '\n' + indent*' ' + 'End While\n'

    def typecheck(self):
        if isinstance(self.expression, Variable):
            var = get_var_in_scope(self.expression.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.expression.name+\
                    ' not defined in this scope, in line ' + str(self.lineno)+\
                    ', column ' + str(self.column)+'.\n'
        if self.expression.return_type != 'bool':
            config.static_checking_errors += 'Error: Incompatible type for statement '+\
                self.__class__.__name__+": '"+str(self.expression.return_type)+\
                "', in line "+str(self.lineno)+', column '+str(self.column)+'.\n'    


class Expression(object): pass


class Variable(Expression):
    def __init__(self, name, return_type=None, value=None, lineno=None, column=None):
        self.name = name
        self.return_type = return_type
        self.value = value
        self.lineno = lineno
        self.column = column

        if return_type == None:
            var = get_var_in_scope(self.name)
            if var: self.return_type = var.return_type

    def evaluate(self):
        var = get_var_in_scope(self.name)
        if var == None:
            return 0
        return var.value

    def repr(self, indent):
        if getattr(self.name,'repr',None):
            return str(self.name.repr(indent))
        else: 
            return 'Variable\n' + indent*' ' + str(self.name) + '\n'


class Int(Expression):
    def __init__(self, value, lineno, column):
        self.value = value
        self.return_type = 'int'
        self.lineno = lineno
        self.column = column
    
    def evaluate(self):        
        return int(self.value)
    
    def repr(self, indent):
        return 'Int\n' + indent*' ' + str(self.value) + '\n' 
    
    def typecheck(self):
        pass
    
    
class Set(Expression):
    def __init__(self, elements, lineno, column):
        self.elements = elements
        self.return_type = 'set'
        self.lineno = lineno
        self.column = column

    def evaluate(self):
        return map(lambda x: x.evaluate(), self.elements)

    def repr(self, indent):
        s = 'Set\n' + indent*' '
        if self.elements:
            for e in self.elements:
                s += str(e.__repr__()) if not getattr(e,'repr',None) else str(e.repr(indent+4)) + indent*' '
        return s[:len(s)-indent]
    
    def typecheck(self):
        pass
    
    
class Bool(Expression):
    def __init__(self, value, lineno, column):
        self.value = value
        self.return_type = 'bool'
        self.lineno = lineno
        self.column = column

    def evaluate(self): return True if self.value == 'true' else False

    def repr(self, indent):
        return 'Bool\n' + indent*' ' + self.value + '\n'
    
    def typecheck(self):
        pass
    

class String(Expression):
    def __init__(self, value, lineno, column):
        self.value = value
        self.return_type = 'str'
        self.lineno = lineno
        self.column = column

    def evaluate(self): return self.value[1:len(self.value)-1]

    def repr(self, indent):
        return 'String\n' + indent*' ' + self.value + '\n'



class BinOp(Expression): 
    def __init__(self, operand1, operand2, lineno, column):
        self.operand1 = operand1
        self.operand2 = operand2
        self.lineno = lineno
        self.column = column
        self.init()

    def repr(self, indent):
        op1 = self.operand1.__repr__() if not getattr(self.operand1,'repr',None) else self.operand1.repr(indent+4)
        op2 = self.operand2.__repr__() if not getattr(self.operand2,'repr',None) else self.operand2.repr(indent+4)
        return self.__class__.__name__ + '\n' + indent*' ' + op1 + indent*' ' + op2
    
    def typecheck(self):
        if isinstance(self.operand1, Variable):
            var = get_var_in_scope(self.operand1.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.operand1.name+\
                    ' not defined in this scope, in line ' + str(self.operand1.lineno)+\
                    ', column ' + str(self.operand1.column)+'.\n'
                    
        if isinstance(self.operand2, Variable):
            var = get_var_in_scope(self.operand2.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.operand2.name+\
                    ' not defined in this scope, in line ' + str(self.operand2.lineno)+\
                    ', column ' + str(self.operand2.column)+'.\n'
                                 
        if self.operand1.return_type != self.expected_type1 or self.operand2.return_type != self.expected_type2:
            config.static_checking_errors += 'Error: Incompatible types for operator '+\
                self.__class__.__name__+": '"+str(self.operand1.return_type)+"' and '"+\
                str(self.operand2.return_type)+"', in line "+str(self.lineno)+', column '+\
                str(self.column)+'.\n'
    

class ArithmeticOp(BinOp):
    def init(self):
        self.expected_type1 = 'int'
        self.expected_type2 = 'int'
        self.return_type = 'int'
        
class Plus(ArithmeticOp): 
    def evaluate(self):
        aux = self.operand1.evaluate() + self.operand2.evaluate()         
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit()  
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return self.operand1.evaluate() + self.operand2.evaluate()

class Minus(ArithmeticOp):
    def evaluate(self): 
        aux = self.operand1.evaluate() - self.operand2.evaluate()         
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n' 
            sys.stdout.write(s)
            sys.exit() 
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return self.operand1.evaluate() - self.operand2.evaluate()

class Times(ArithmeticOp):
    def evaluate(self): 
        aux = self.operand1.evaluate() * self.operand2.evaluate()         
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n' 
            sys.stdout.write(s)
            sys.exit() 
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return self.operand1.evaluate() * self.operand2.evaluate()

class Div(ArithmeticOp):
    def evaluate(self):
        op2 = self.operand2.evaluate()
        if op2 == 0:
            s = '\nERROR: division by zero in line ' + str(self.operand2.lineno)+\
                    ', column ' + str(self.operand2.column)+'.\n'
            sys.stdout.write(s)
            sys.exit()
        aux = self.operand1.evaluate() / op2         
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n' 
            sys.stdout.write(s)
            sys.exit() 
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return self.operand1.evaluate() / op2

class Mod(ArithmeticOp):
    def evaluate(self): 
        op2 = self.operand2.evaluate()
        if op2 == 0:
            s = '\nERROR: division by zero in line ' + str(self.operand2.lineno)+\
                    ', column ' + str(self.operand2.column)+'.\n'
            sys.stdout.write(s)
            sys.exit()
        aux = self.operand1.evaluate() % op2
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n' 
            sys.stdout.write(s)
            sys.exit()
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit()
        return self.operand1.evaluate() % op2


class IntSetOp(BinOp): 
    def init(self):
        self.expected_type1 = 'int'
        self.expected_type2 = 'set'
        self.return_type = 'set'    
    
class PlusSet(IntSetOp):
    def evaluate(self):
        aux = self.operand1.evaluate()
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit()  
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return map(lambda x: str(self.operand1.evaluate() + int(x)), self.operand2.evaluate())

class MinusSet(IntSetOp):
    def evaluate(self): 
        aux = self.operand1.evaluate()
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit()  
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return map(lambda x: str(self.operand1.evaluate() - int(x)), self.operand2.evaluate())

class TimesSet(IntSetOp):
    def evaluate(self): 
        aux = self.operand1.evaluate()
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n' 
            sys.stdout.write(s)
            sys.exit() 
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'        
            sys.stdout.write(s)
            sys.exit() 
        return map(lambda x: str(self.operand1.evaluate() * int(x)), self.operand2.evaluate())

class DivSet(IntSetOp):
    def evaluate(self):
        aux = self.operand1.evaluate() 
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit() 
        return map(lambda x: str(self.operand1.evaluate() / int(x)), self.operand2.evaluate())

class ModSet(IntSetOp):
    def evaluate(self): 
        aux = self.operand1.evaluate()
        if (aux > 2**31-1):
            s = '\nError: Overflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit()  
        if (aux < -2**31 + 1):
            s = '\nError: Underflow in line '+ str(self.lineno)+\
                            ', column '+str(self.column) + '.\n'
            sys.stdout.write(s)
            sys.exit()  
        return map(lambda x: str(self.operand1.evaluate() / int(x)), self.operand2.evaluate())
        return map(lambda x: str(self.operand1.evaluate() % int(x)), self.operand2.evaluate())

class Contains(IntSetOp):
    def init(self):
        self.expected_type1 = 'int'
        self.expected_type2 = 'set'
        self.return_type = 'bool'
        
    def evaluate(self): return self.operand1.evaluate() in self.operand2.evaluate()


class IntIntOp(BinOp):
    def init(self):
        self.expected_type1 = 'int'
        self.expected_type2 = 'int'
        self.return_type = 'bool'

class LessThan(IntIntOp):
    def evaluate(self): return self.operand1.evaluate() < self.operand2.evaluate()
class LessThanEq(IntIntOp):
    def evaluate(self): return self.operand1.evaluate() <= self.operand2.evaluate()
class GreaterThan(IntIntOp):
    def evaluate(self): return self.operand1.evaluate() > self.operand2.evaluate()
class GreaterThanEq(IntIntOp):
    def evaluate(self): return self.operand1.evaluate() >= self.operand2.evaluate()


class Equals(BinOp):
    def init(self):
        self.expected_type1 = object
        self.expected_type2 = object
        self.return_type = 'bool'
        
    def evaluate(self): 
        op1 = self.operand1.evaluate()
        op2 = self.operand2.evaluate()
        if isinstance(op1, list) and isinstance(op2, list): return set(op1) == set(op2)
        return op1 == op2
        
    def typecheck(self):
        if isinstance(self.operand1, Variable):
            var = get_var_in_scope(self.operand1.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.operand1.name+\
                    ' not defined in this scope, in line ' + str(self.operand1.lineno)+\
                    ', column ' + str(self.operand1.column)+'.\n'
        if isinstance(self.operand2, Variable):
            var = get_var_in_scope(self.operand2.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.operand2.name+\
                    ' not defined in this scope, in line ' + str(self.operand2.lineno)+\
                    ', column ' + str(self.operand2.column)+'.\n'
                
    
class NotEquals(Equals): 
    def evaluate(self): return not Equals.evaluate(self)

class SetOp(BinOp):
    def init(self):
        self.expected_type1 = 'set'
        self.expected_type2 = 'set'
        self.return_type = 'set'        

class Union(SetOp):
    def evaluate(self): return self.operand1.evaluate() + self.operand2.evaluate()
class Difference(SetOp):
    def evaluate(self): return [e for e in self.operand1.evaluate() if e not in self.operand2.evaluate()]
class Intersect(SetOp):
    def evaluate(self): return [e for e in self.operand1.evaluate() if e in self.operand2.evaluate()]
        
       
class BoolOp(BinOp):
    def init(self):
        self.expected_type1 = 'bool'
        self.expected_type2 = 'bool'
        self.return_type = 'bool'
                
class And(BoolOp):
    def evaluate(self): return self.operand1.evaluate() and self.operand2.evaluate()
class Or(BoolOp):
    def evaluate(self): return self.operand1.evaluate() or self.operand2.evaluate()


class UnaryOp(Expression):
    def __init__(self, operand, lineno, column):
        self.operand = operand
        self.lineno = lineno
        self.column = column
        self.init()

    def repr(self, indent):
        op = self.operand.__repr__() if not getattr(self.operand,'repr',None) else self.operand.repr(indent+4)
        return self.__class__.__name__ + '\n' + indent*' ' + op
    
    def typecheck(self):
        if isinstance(self.operand, Variable):
            var = get_var_in_scope(self.operand.name)
            if not var:
                config.static_checking_errors += 'Error: Variable ' + self.operand.name+\
                    ' not defined in this scope, in line ' + str(self.operand.lineno)+\
                    ', column ' + str(self.operand.column)+'.\n'
        if self.operand.return_type != self.expected_type:
            config.static_checking_errors += 'Error: Incompatible types for operator '+\
                self.__class__.__name__+": '"+str(self.operand.return_type)+\
                "', in line "+str(self.lineno)+', column '+str(self.column)+'.\n'
    
class Uminus(UnaryOp):
    def init(self):
        self.expected_type = 'int'
        self.return_type = 'int'
    
    def evaluate(self): return -self.operand.evaluate()

class Not(UnaryOp):
    def init(self):
        self.expected_type = 'bool'
        self.return_type = 'bool'
        
    def evaluate(self): return not self.operand.evaluate()
        
class SetIntOp(UnaryOp):
    def init(self):
        self.expected_type = 'set'
        self.return_type = 'int'
        
class Len(SetIntOp):
    def evaluate(self): return len(set(self.operand.evaluate()))
class MaxSet(SetIntOp):
    def evaluate(self): return max(self.operand.evaluate())
class MinSet(SetIntOp):
    def evaluate(self): return min(self.operand.evaluate())
