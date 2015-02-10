'''
Created on 2/2/2015

@author: David Klie
@author : Gustavo Benzecri

'''
def tab(level):
    return('    '*level)

class Program:
    
    def __init__(self,statement_block):
        self.statement_block=statement_block 
        
    def __str__(self, *args, **kwargs):
        return('PROGRAM\n'+self.statement_block.printTree(1))

class Statement: pass
    
class Block(Statement):
    
    def __init__(self,using,blockinstructions):
        self.using=using
        self.blockinstructions=blockinstructions
    
    def printTree(self,level):
        string=tab(level)+'BLOCK\n'
        if self.using!=None:
            string+=self.using.printTree(level+1) 
        if self.blockinstructions!=None: 
            for binst in self.blockinstructions:
                string+=binst.printTree(level+1)
        string+=tab(level)+'BLOCK_END'+'\n'
        return(string)
        
class Using(Statement):
    
    def __init__(self,declarations):
        self.declaration=declarations
        
    def printTree(self,level):
        string=tab(level)+'USING\n'
        for i in self.declaration:
            for j in i[1]:
                string+=tab(level+1)+i[0]+' '+j+'\n'
        string+=tab(level)+'IN\n'
        return(string)

class Print(Statement):
    
    def __init__(self,print_type,values):
        self.print_type = print_type
        self.values=values
        
    def printTree(self,level):
        string = tab(level)+'PRINT\n'
        string += tab(level+1) + 'elements\n'
        string += self.values.printTree(level+1)
        if (self.print_type == 'println'):
            string += tab(level+2) + 'string\n' + tab(level+3) + '"\\n"' + '\n'
        return(string)
    
class Values(Statement):
    
    def __init__(self, expression, values = None):
        self.expression = expression
        self.values = values
    
    def printTree(self,level):
        string = ''
        if (isinstance(self.expression, basestring)):
            string += tab(level+1) + 'string\n' + tab(level+2) + self.expression + '\n'
        else:
            string += self.expression.printTree(level+1)
        if (self.values is not None):
            string += self.values.printTree(level)
        return(string)
    
class Assign(Statement):
    
    def __init__(self,identifier,expression):
        self.identifier=identifier
        self.expression=expression
    
    def printTree(self,level):
       string=tab(level)+"ASSIGN\n"+self.identifier.printTree(level+1)+tab(level+1)+'value\n'
       string+=self.expression.printTree(level+2)
       return(string)
   
class Scan(Statement):
    
    def __init__(self,scan_identifier):
        self.identifier=scan_identifier
        
    def printTree(self,level):
        return tab(level)+'SCAN\n'+self.identifier.printTree(level+1)
  
class if_statement(Statement):
    
    def __init__(self,condition,statement_block,else_clause=None):
        self.condition=condition
        self.statement_block=statement_block
        self.else_clause=else_clause
    
    def printTree(self,level):
        string=tab(level)+'IF\n'+tab(level+1)+'condition\n'+self.condition.printTree(level+2)
        string+=tab(level+1)+'THEN\n'+self.statement_block.printTree(level+2)
        if self.else_clause!=None:
            string+=self.else_clause.printTree(level+1)
        return(string)
    
class else_statement:
    
    def __init__(self,block_or_if):
        self.block_or_if=block_or_if
        
    def printTree(self,level):
        return tab(level)+"ELSE\n"+self.block_or_if.printTree(level+1)
    
class repeat_statement(Statement):
    
    def __init__(self, statement):
        self.statement=statement
    
    def printTree(self,level):
        return(tab(level)+'REPEAT\n'+self.statement.printTree(level+1))
    
class while_statement(Statement):
    
    def __init__(self,condition):
        self.condition=condition
    
    def printTree(self,level):
        return(tab(level)+'WHILE\n'+tab(level+1)+'condition\n'+self.condition.printTree(level+2))
    
class Do(Statement):
    
    def __init__(self,block_statement):
        self.block_statement=block_statement
        
    def printTree(self,level):
        return tab(level)+'DO\n'+self.block_statement.printTree(level+1)
    
class repeat_while_do(Statement):
    def __init__(self, Repeat = None, While = None, Do = None):
        self.repeat_statement = Repeat
        self.while_statement = While
        self.do_statement = Do
        
    def printTree(self,level):
        string = ''
        if (self.repeat_statement is not None):
            string += self.repeat_statement.printTree(level)
        if (self.while_statement is not None):
            string += self.while_statement.printTree(level)
        if (self.do_statement is not None):
            string += self.do_statement.printTree(level) 
        return(string)
    
class For_statement(Statement):
    
    def __init__(self,dummy,direction,set_expression,do_statement):
        self.dummy=dummy
        self.direction=direction
        self.set_expression=set_expression
        self.do_statement=do_statement
        
    def printTree(self,level):
        string=tab(level)+'FOR\n'+self.dummy.printTree(level+1)
        string+=tab(level+1)+'direction\n'+tab(level+2)+self.direction+'\n'
        string+=tab(level+1)+'IN\n'+self.set_expression.printTree(level+1)+self.do_statement.printTree(level+1)
        return(string)
    
''' EXPRESIONES RECONOCIDAS POR SETLAN '''
class Expression: pass

class String(Expression):
    
    def __init__(self,value):
        self.value=value
        
    def __str__(self):
        return self.value
    
    def printTree(self,level):
        return tab(level)+"STRING\n"+tab(level+1)+self.value+'\n'
    
class Integer(Expression):
    
    def __init__(self,value):
        self.value=value
        
    def printTree(self,level):
        return(tab(level)+'int\n'+tab(level+1)+str(self.value)+'\n')
    
class Variable(Expression):
    
    def __init__(self,value):
        self.value=value
    
    def printTree(self,level):
        return(tab(level)+'variable\n'+tab(level+1)+str(self.value)+'\n')
    
class Boolean(Expression):
    
    def __init__(self,value):
        self.value=value
        
    def printTree(self,level):
        return (tab(level)+'bool\n'+tab(level+1)+str(self.value)+'\n')
    
class SetExpression(Expression):
    
    def __init__(self,elements=None):
        self.elements=elements
        
    def printTree(self,level):
        string=tab(level)+'set\n'
        if self.elements!=None:
            for e in self.elements:
                string+=e.printTree(level+1)
        return(string)
    
class GroupedExpression(Expression):
    
    def __init__(self,expression):
        self.expression=expression
    
    def printTree(self,level):
         return tab(level)+'LPAREN\n'+self.expression.printTree(level+1)+tab(level)+'RPAREN\n'
    
class UnaryExpression(Expression):
    
    unaryOperators= {
    'not' : 'NOT',
    '-'   : 'UNARY_MINUS',
    '>?' : 'MAXSET',
    '<?' : 'MINSET',
    '$?' : 'CARDINALITY'          
    }
    
    def __init__(self,operator,operand):
        self.operator=operator
        self.operand=operand
    
    def printTree(self,level):
        string=tab(level)+UnaryExpression.unaryOperators[self.operator]+' '+self.operator+'\n'
        string+=self.operand.printTree(level+1)
        return(string)
    
class BinaryExpression(Expression):
    
    BinaryExpression={
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
    
    def __init__(self,operand1,operator,operand2):
        self.operand1=operand1
        self.operand2=operand2
        self.operator=operator
        
    def printTree(self,level):
        string=tab(level)+BinaryExpression.BinaryExpression[self.operator]+' '+self.operator+'\n'
        string+=self.operand1.printTree(level+1)+self.operand2.printTree(level+1)
        return(string)
        
