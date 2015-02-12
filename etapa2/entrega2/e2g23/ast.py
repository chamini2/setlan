class Program(object):
    def __init__(self, statement):
        self.statement = statement
        
    def repr(self):
        indent = 4
        if self.statement:
            sta = self.statement.__repr__() if not getattr(self.statement,'repr',None) else self.statement.repr(indent+4) 
            return 'Program\n' + indent*' ' + sta
        else:
            return 'Program\n'


class Statement(object): pass


class Assign(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def repr(self, indent): 
        var = self.variable.__repr__() if not getattr(self.variable,'repr', None) else self.variable.repr(indent+8)
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        return 'Assign\n' + indent*' ' + var + indent*' ' + 'Value\n' + (indent+4)*' ' + exp


class Block(Statement):
    def __init__(self, statement_list, declarations=None):
        self.statement_list = statement_list
        self.declarations = declarations

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
    def __init__(self, variable):
        self.variable = variable
        
    def repr(self, indent):
        var = self.variable.__repr__() if not getattr(self.variable,'repr',None) else self.variable.repr(indent+4)
        return 'Scan\n' + indent*' ' + var


class Print(Statement):
    def __init__(self, print_list):
        self.print_list = print_list

    def repr(self, indent):
        return_string = 'Print\n'
        for element in self.print_list:
            e = element.__repr__() if not getattr(element,'repr',None) else element.repr(indent+4)
            return_string += indent*' ' + e
        return return_string


class Println(Statement):
    def __init__(self, print_list):
        self.print_list = print_list

    def repr(self, indent):
        return_string = 'Println\n'
        for element in self.print_list:
            e = element.__repr__() if not getattr(element,'repr',None) else element.repr(indent+4)
            return_string +=  + indent*' ' + e
        return return_string


class If(Statement):
    def __init__(self, expression, statement1, statement2=None):
        self.expression = expression
        self.statement1 = statement1
        self.statement2 = statement2
    
    def repr(self, indent):
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        sta_1 = self.statement1.__repr__() if not getattr(self.statement1,'repr',None) else self.statement1.repr(indent+8)
        s = 'If\n' + indent*' ' + 'Condition\n' + (indent+4)*' ' + exp + indent*' ' + 'Statement True\n' + (indent+4)*' ' + sta_1
        if self.statement2:
            sta_2 = self.statement2.__repr__() if not getattr(self.statement2,'repr',None) else self.statement2.repr(indent+8)
            return s + indent*' ' + 'Statement False\n' + (indent+4)*' ' + sta_2 + (indent-4)*' ' + 'End If\n'
        return s + (indent-4)*' ' + 'End If\n'


class For(Statement):
    def __init__(self, variable, order, expression, statement):
        self.variable = variable
        self.order = order
        self.expression = expression
        self.statement = statement

    def repr(self, indent):
        var = self.variable.__repr__() if not getattr(self.variable,'repr',None) else self.variable.repr(indent+4)
        exp = self.expression.__repr__() if not getattr(self.expression,'repr',None) else self.expression.repr(indent+8)
        sta = self.statement.__repr__() if not getattr(self.statement,'repr',None) else self.statement.repr(indent+8)
        return 'For\n' + indent*' ' + var + indent*' ' + 'Direction\n' + (indent+4)*' ' + self.order + '\n' + indent*' ' + 'In\n' + (indent+4)*' '  + exp + indent*' ' + 'Do\n' + (indent+4)*' ' + sta + (indent-4)*' ' + 'End For\n'


class Repeat(Statement):
    def __init__(self, statement1, expression, statement2):
        self.statement1 = statement1
        self.expression = expression
        self.statement2 = statement2
    
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
        
    
class Expression(object): pass


class Variable(Expression):
    def __init__(self, name):
        self.name = name

    def repr(self, indent):
        if getattr(self.name,'repr',None):
            return str(self.name.repr(indent))
        else: 
            return 'Variable\n' + indent*' ' + self.name + '\n'
        
    

class Int(Expression):
    def __init__(self, value):
        self.value = value    
        
    def repr(self, indent):
        return 'Int\n' + indent*' ' + str(self.value) + '\n'
    
    
class Set(Expression):
    def __init__(self, elements):
        self.elements = elements   
        
    def repr(self, indent):
        s = 'Set\n' + indent*' '
        for e in self.elements:
            s += str(e.__repr__()) if not getattr(e,'repr',None) else str(e.repr(indent+4)) + indent*' '
        return s[:len(s)-indent]
    
    
class Bool(Expression):
    def __init__(self, value):
        self.value = value

    def repr(self, indent):
        return 'Bool\n' + indent*' ' + self.value + '\n'
    

class String(Expression):
    def __init__(self, value):
        self.value = value

    def repr(self, indent):
        return 'String\n' + indent*' ' + self.value + '\n'


class BinOp(Expression): 
    def __init__(self, operand1, operand2):
        self.operand1 = operand1
        self.operand2 = operand2

    def repr(self, indent):
        op1 = self.operand1.__repr__() if not getattr(self.operand1,'repr',None) else self.operand1.repr(indent+4)
        op2 = self.operand2.__repr__() if not getattr(self.operand2,'repr',None) else self.operand2.repr(indent+4)
        return self.__class__.__name__ + '\n' + indent*' ' + op1 + indent*' ' + op2


class Plus(BinOp): pass

class Minus(BinOp): pass

class Times(BinOp): pass

class Div(BinOp): pass
    
class Mod(BinOp): pass
    
class PlusSet(BinOp): pass
    
class MinusSet(BinOp): pass

class TimesSet(BinOp): pass
    
class DivSet(BinOp): pass

class ModSet(BinOp): pass
    
class LessThan(BinOp): pass
        
class LessThanEq(BinOp): pass
        
class GreaterThan(BinOp): pass
    
class GreaterThanEq(BinOp): pass
        
class Equals(BinOp): pass
        
class NotEquals(BinOp): pass

class Union(BinOp): pass
    
class Difference(BinOp): pass
        
class Intersect(BinOp): pass
        
class And(BinOp): pass
        
class Or(BinOp): pass
        
class Contains(BinOp): pass
    

class UnaryOp(Expression):
    def __init__(self, operand):
        self.operand = operand

    def repr(self, indent):
        op = self.operand.__repr__() if not getattr(self.operand,'repr',None) else self.operand.repr(indent+4)
        return self.__class__.__name__ + '\n' + indent*' ' + op
    
class Uminus(UnaryOp): pass

class Not(UnaryOp): pass
        
class Len(UnaryOp): pass    
        
class MaxSet(UnaryOp): pass
        
class MinSet(UnaryOp): pass    