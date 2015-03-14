#!/usr/bin/env python
# ------------------------------------------------------------
# syntax_specs.py
#
# Setlan language syntactic specifications. Every grammar,
# precedence and associativity rule for Setlan are specified
# here.
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from exceptions import SetlanSyntaxError

from lexical_specs import tokens

from type import *

from ast import *

##########
## List of tokens to be used by ply.yacc
tokens = tokens
##########

################################################################################
###################### Precedence and associative rules ########################
################################################################################

precedence = (
    ('right', 'TkElse'),
    ('left', 'TkOr'),
    ('left', 'TkAnd'),
    ('nonassoc', 'TkGreatOrEq', 'TkLessOrEq', 'TkGreat', 'TkLess'),
    ('nonassoc', 'TkEquals', 'TkNotEq'),
    ('nonassoc', 'TkIsIn'),
    ('left', 'TkPlus', 'TkMinus'),
    ('left', 'TkTimes', 'TkDiv', 'TkMod'),
    ('left', 'TkUnion', 'TkDiff'),
    ('left', 'TkInter'),
    ('left', 'TkSPlus', 'TkSMinus'),
    ('left', 'TkSTimes', 'TkSDiv', 'TkSMod'),
    ('right', 'TkNot'),
    ('right', 'UMINUS'),
    ('right', 'TkGetMax', 'TkGetMin', 'TkSize')
   )

################################################################################
################### End of Precedence and associative rules ####################
################################################################################

################################################################################
################################ Grammar rules #################################
################################################################################
start = 'Setlan'

#Gramatic Definitions
def p_Setlan(p):
    '''
    Setlan : TkProgram Instruction
    '''
    p[0] = Setlan(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_Instruction(p):
    '''
    Instruction : Assignment
                | Block
                | Input
                | Output
                | Conditional
                | For
                | While
    '''
    p[0] = p[1]

def p_Assignment(p):
    '''
    Assignment : TkId TkAssign Expression
    '''
    p[0] = Assignment(Variable(p[1], position=(p.lineno(1), p.lexpos(1))), p[3], position=(p.lineno(1), p.lexpos(1)))

def p_Block(p):
    '''
    Block : TkOBrace VariableDeclarations InstructionsList TkCBrace
    '''
    p[0] = Block(p[2], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_VariableDeclarations(p):
    '''
    VariableDeclarations : TkUsing VariableDeclarationList TkIn
    '''
    p[0] = p[2]

def p_VariableDeclarations_lambda(p):
    '''
    VariableDeclarations : lambda
    '''
    p[0] = p[1]

def p_VariableDeclarationList_list(p):
    '''
    VariableDeclarationList : VariableDeclarationList VariableDeclaration TkSColon
    '''
    p[0] = p[1] + [p[2]]

def p_VariableDeclarationList(p):
    '''
    VariableDeclarationList : VariableDeclaration TkSColon
    '''
    p[0] = [p[1]]
    

def p_VariableDeclaration(p):
    '''
    VariableDeclaration : Type VariableList
    '''
    p[0] = VariableDeclaration(p[1], p[2], position=(p.lineno(1), p.lexpos(1)))


def p_Type_int(p):
    '''
    Type : TkInt
    '''
    p[0] = IntegerType(position=(p.lineno(1), p.lexpos(1)))


def p_Type_bool(p):
    '''
    Type : TkBool
    '''
    p[0] = BooleanType(position=(p.lineno(1), p.lexpos(1)))


def p_Type_set(p):
    '''
    Type : TkSet
    '''
    p[0] = SetType(position=(p.lineno(1), p.lexpos(1)))


def p_VariableList_list(p):
    '''
    VariableList : VariableList TkComma TkId
    '''
    p[0] = p[1] + [Variable(p[3], position=(p.lineno(3), p.lexpos(3)))]


def p_VariableList(p):
    '''
    VariableList : TkId
    '''
    p[0] = [Variable(p[1], position=(p.lineno(1), p.lexpos(1)))]

def p_InstructionList_list(p):
    '''
    InstructionsList : InstructionsList Instruction TkSColon
    '''
    p[0] = p[1] + [p[2]]

def p_InstructionList(p):
    '''
    InstructionsList : lambda
    '''
    p[0] = p[1]

def p_Input(p):
    '''
    Input : TkScan TkId
    '''
    p[0] = Input(Variable(p[2], position=(p.lineno(2), p.lexpos(2))), position=(p.lineno(1), p.lexpos(1)))

def p_Output(p):
    '''
    Output : Println
           | Print
    '''
    p[0] = p[1]

def p_Println(p):
    '''
    Println : TkPrintLn PrintableList 
    '''
    p[0] = Output(p[2], position=(p.lineno(1), p.lexpos(1)), sufix="\n")

def p_Print(p):
    '''
    Print : TkPrint PrintableList
    '''
    p[0] = Output(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_PrintableList_list(p):
    '''
    PrintableList : PrintableList TkComma Printable
    '''
    p[0] = p[1] + [p[3]]

def p_PrintableList(p):
    '''
    PrintableList : Printable
    '''
    p[0] = [p[1]]

def p_Printable_exp(p):
    '''
    Printable : Expression
    '''
    p[0] = p[1]

def p_Printable_str(p):
    '''
    Printable : TkString
    '''
    p[0] = String(p[1], position=(p.lineno(1), p.lexpos(1)))

def p_Conditional(p):
    '''
    Conditional : TkIf TkOPar Expression TkCPar Instruction Else
    '''
    p[0] = Conditional(p[3], p[5], p[6], position=(p.lineno(1), p.lexpos(1)))

def p_Else(p):
    '''
    Else : TkElse Instruction
    '''
    p[0] = p[2]

def p_Else_lambda(p):
    '''
    Else : lambda
    '''
    p[0] = None

def p_For(p):
    '''
    For : TkFor TkId Ordering Expression TkDo Instruction
    '''
    p[0] = ForLoop(Variable(p[2], position=(p.lineno(2), p.lexpos(2))), p[3], p[4], p[6], position=(p.lineno(1), p.lexpos(1)))

def p_Ordering_min(p):
    '''
    Ordering : TkMin
    '''
    p[0] = True

def p_Ordering_max(p):
    '''
    Ordering : TkMax
    '''
    p[0] = False


def p_While_1stForm(p):
    '''
    While : TkRepeat Instruction TkWhile TkOPar Expression TkCPar TkDo Instruction
    '''
    p[0] = RepeatWhileLoop(p[2], p[5], p[8], position=(p.lineno(1), p.lexpos(1)))


def p_While_2ndForm(p):
    '''
    While : TkWhile TkOPar Expression TkCPar TkDo Instruction
    '''
    p[0] = RepeatWhileLoop(None, p[3], p[6], position=(p.lineno(1), p.lexpos(1)))


def p_While_3rdForm(p):
    '''
    While : TkRepeat Instruction TkWhile TkOPar Expression TkCPar
    '''
    p[0] = RepeatWhileLoop(p[2], p[5], None, position=(p.lineno(1), p.lexpos(1)))


def p_Expression(p):
    '''
    Expression : BinaryExpression
               | UnaryExpression
               | Literal
    '''
    p[0] = p[1]


def p_Expression_parenthesized(p):
    '''
    Expression : TkOPar Expression TkCPar
    '''
    p[0] = p[2]


def p_Expression_variable(p):
    '''
    Expression : TkId
    '''
    p[0] = Variable(p[1], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Sum(p):
    '''
    BinaryExpression : Expression TkPlus Expression
    '''
    p[0] = Sum(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Subtraction(p):
    '''
    BinaryExpression : Expression TkMinus Expression
    '''
    p[0] = Subtraction(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Times(p):
    '''
    BinaryExpression : Expression TkTimes Expression
    '''
    p[0] = Times(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Division(p):
    '''
    BinaryExpression : Expression TkDiv Expression
    '''
    p[0] = Division(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Modulus(p):
    '''
    BinaryExpression : Expression TkMod Expression
    '''
    p[0] = Modulus(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Union(p):
    '''
    BinaryExpression : Expression TkUnion Expression
    '''
    p[0] = Union(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Difference(p):
    '''
    BinaryExpression : Expression TkDiff Expression
    '''
    p[0] = Difference(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Intersection(p):
    '''
    BinaryExpression : Expression TkInter Expression
    '''
    p[0] = Intersection(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_SSum(p):
    '''
    BinaryExpression : Expression TkSPlus Expression
    '''
    p[0] = SetSum(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_SSubtraction(p):
    '''
    BinaryExpression : Expression TkSMinus Expression
    '''
    p[0] = SetSubtraction(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_STimes(p):
    '''
    BinaryExpression : Expression TkSTimes Expression
    '''
    p[0] = SetTimes(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_SDivision(p):
    '''
    BinaryExpression : Expression TkSDiv Expression
    '''
    p[0] = SetDivision(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_SModulus(p):
    '''
    BinaryExpression : Expression TkSMod Expression
    '''
    p[0] = SetModulus(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_GreaterThan(p):
    '''
    BinaryExpression : Expression TkGreat Expression
    '''
    p[0] = GreaterThan(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_GreaterOrEqual(p):
    '''
    BinaryExpression : Expression TkGreatOrEq Expression
    '''
    p[0] = GreaterOrEqual(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_LessThan(p):
    '''
    BinaryExpression : Expression TkLess Expression
    '''
    p[0] = LessThan(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_LessOrEqual(p):
    '''
    BinaryExpression : Expression TkLessOrEq Expression
    '''
    p[0] = LessOrEqual(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_Equals(p):
    '''
    BinaryExpression : Expression TkEquals Expression
    '''
    p[0] = Equals(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_NotEquals(p):
    '''
    BinaryExpression : Expression TkNotEq Expression
    '''
    p[0] = NotEquals(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_And(p):
    '''
    BinaryExpression : Expression TkAnd Expression
    '''
    p[0] = And(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_Or(p):
    '''
    BinaryExpression : Expression TkOr Expression
    '''
    p[0] = Or(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_BinaryExpression_Boolean_IsIn(p):
    '''
    BinaryExpression : Expression TkIsIn Expression
    '''
    p[0] = IsIn(p[1], p[3], position=(p.lineno(1), p.lexpos(1)))

def p_UnaryExpression_UMinus(p):
    '''
    UnaryExpression : TkMinus Expression %prec UMINUS
    '''
    p[0] = Minus(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_UnaryExpression_GetMax(p):
    '''
    UnaryExpression : TkGetMax Expression
    '''
    p[0] = GetMax(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_UnaryExpression_GetMin(p):
    '''
    UnaryExpression : TkGetMin Expression
    '''
    p[0] = GetMin(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_UnaryExpression_GetSize(p):
    '''
    UnaryExpression : TkSize Expression
    '''
    p[0] = GetSize(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_UnaryExpression_Boolean_Not(p):
    '''
    UnaryExpression : TkNot Expression
    '''
    p[0] = Not(p[2], position=(p.lineno(1), p.lexpos(1)))

def p_Literal_Num(p):
    '''
    Literal : TkNum
    '''
    p[0] = Number(p[1], position=(p.lineno(1), p.lexpos(1)))

def p_Literal_True(p):
    '''
    Literal : TkTrue
    '''
    p[0] = TrueValue(position=(p.lineno(1), p.lexpos(1)))

def p_Literal_False(p):
    '''
    Literal : TkFalse
    '''
    p[0] = FalseValue(position=(p.lineno(1), p.lexpos(1)))

def p_Literal_Set(p):
    '''
    Literal : Set
    '''
    p[0] = Set(p[1], position=(p.lineno(1), p.lexpos(1)))

def p_Set(p):
    '''
    Set : TkOBrace ExpressionList TkCBrace
    '''
    p[0] = p[2]

def p_ExpressionList_list(p):
    '''
    ExpressionList : ExpressionList TkComma Expression
    '''
    p[0] = p[1] + [p[3]]

def p_ExpressionList_single(p):
    '''
    ExpressionList : Expression
    '''
    p[0] = [p[1]]

def p_ExpressionList(p):
    '''
    ExpressionList : lambda
    '''
    p[0] = p[1]

def p_lambda(p):
    '''
    lambda : 
    '''
    p[0] = []

################################################################################
############################ End of Grammar rules ##############################
################################################################################

# Error handling
def p_error(p):
    error = ""
    if p is None:
        error = "Unexpected End Of File (EOF)."
    else:
        error = "Unexpected %s." % p
    raise SetlanSyntaxError(error)