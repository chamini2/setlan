# -*- coding: utf-8 -*-'''
'''
Created on 4/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
    
    Parser de SetLan
    Posee la gramatica pasada al parser
'''
import ply.yacc as yacc
from expressions import tokens,simbolos, simbolos_igual, op_mapeados, unarios_conjuntos, get_column
from AST import *

parser_errors = []

#############################  STATEMENTS   ##################################
def p_program(p):
    'program : PROGRAM statement'
    p[0] = Program(p[2])
    
def p_statement_assing(p):
    'statement : IDENTIFIER ASSIGN expression'
    iden = Identifier(p[1])
    iden.lineno = p.lineno(1)
    iden.lexpos = p.lexpos(1)
    p[0] = Assign(iden,p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)
    
def p_statement_block(p):
    'statement : LCURLY declare statement_list RCURLY'
    p[0] = Block(p[3],p[2])

#############################     IN/OUT    ##################################
def p_statement_function_scan(p):
    'statement : SCAN IDENTIFIER'
    id = Identifier(p[2])
    id.lineno = p.lineno(2)
    id.lexpos = p.lexpos(2) 
    p[0] = Scan(id)
    
def p_statement_function_print(p):
    '''statement : PRINT comma_list
                 | PRINTLN comma_list'''
    p[0] = Print(p[1],p[2])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)


#############################  IF STATEMENT   ################################
def p_statement_if(p):
    '''statement : IF LPARENT expression RPARENT statement ELSE statement
                 | IF LPARENT expression RPARENT statement '''
    if len(p) == 8:
        p[0] = If(p[3],p[5],p[7])
    else:
        p[0] = If(p[3],p[5])
    
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)

#############################  FOR STATEMENT     #############################
def p_statement_for(p):
    'statement :  FOR IDENTIFIER direction expression DO statement'
    p[0] = For(Identifier(p[2]),p[3],p[4],p[6])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)

def p_expression_direction(p):
    '''direction : MIN
                  | MAX
    '''
    p[0] = Direction(p[1])
    
####################      REPEAT-WHILE-DO STATEMENT     ###################### 
def p_statement_repeat_while_do(p):
    'statement :  REPEAT statement WHILE LPARENT expression RPARENT DO statement'
    p[0] = RepeatWhileDo(p[2],p[5],p[8])
    p[0].lineno = p.lineno(3)
    p[0].lexpos = p.lexpos(3)
    
def p_statement_while_do(p):
    'statement :  WHILE LPARENT expression RPARENT DO statement'
    p[0] = WhileDo(p[3],p[6])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)
    
def p_statement_repeat_while(p):
    'statement :  REPEAT statement WHILE LPARENT expression RPARENT'
    p[0] = RepeatWhile(p[2],p[5])
    p[0].lineno = p.lineno(3)
    p[0].lexpos = p.lexpos(3)

#############################    DECLARE     #################################
def p_declare_vars(p):
    'declare : USING declare_list IN'
    p[0] = DeclareList(p[2])

def p_declare_empty(p):
    'declare : empty'
    pass
    
def p_declare_list_type(p):
    'declare_list : type identifier_list SEMICOLON declare_list'
    p[0] = [TypeList(p[1],p[2])] + p[4]
    
def p_declare_list_type_empty(p):
    'declare_list : empty'
    p[0] = []

def p_identifier_list(p):
    'identifier_list : IDENTIFIER'
    ident = Identifier(p[1])
    ident.lineno = p.lineno(1)
    ident.lexpos = p.lexpos(1)
    p[0] = [ident]

def p_declare_list_continue_on(p):
    'identifier_list : IDENTIFIER COMMA identifier_list'
    ident = Identifier(p[1])
    ident.lineno = p.lineno(1)
    ident.lexpos = p.lexpos(1)
    p[0] = [ident] + p[3]

#########################     STATEMENT LIST(BLOCK)   ########################
def p_statement_list_continue(p):
    'statement_list : statement SEMICOLON statement_list'
    p[0] = [p[1]] + p[3]

def p_statement_list_empty(p):
    'statement_list : empty'
    p[0] = []
    
#############################   EXPRESSION    #################################
def p_expression_int(p):
    'expression : INTEGER'
    p[0] = Integer(p[1])

def p_expression_bool(p):
    '''expression : FALSE
                  | TRUE
    '''
    p[0] = Bool(p[1])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)
    
def p_expression_string(p):
    'expression : STRING'
    p[0] = String(p[1][1:-1]) # [1:-1] Sirve para eliminar comillas " " del string

def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = Identifier(p[1])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)
    
def p_expression_parent(p):
    ''' expression : LPARENT expression RPARENT'''
    p[0] = Parenthesis(p[2])   

def p_type_data(p):
    '''type : INT
            | BOOL
            | SET
    '''
    p[0] = p[1]
    
##############################     SETS      #################################
def p_expression_set(p):
    ''' expression : LCURLY set_list RCURLY'''
    p[0] = Set(p[2])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)

def p_set_list(p):
    '''set_list : comma_list'''
    p[0] = p[1]

def p_set_list_empty(p):
    'set_list : empty'
    p[0] = []

def p_comma_list_expression(p):
    'comma_list : expression'
    p[0] = [p[1]]
    
def p_comma_list_expression_comma_continue(p):
    'comma_list : expression COMMA comma_list'
    p[0] = [p[1]] + p[3]
  
#############################    BINARY OP     ###############################
def p_expression_op_bin_integer(p):
    '''expression : expression PLUS expression            
                 | expression MINUS expression            
                 | expression TIMES expression            
                 | expression INTDIVISION expression            
                 | expression RESTDIVISION expression            
    '''
    p[0] = BinaryOpInteger(p[1], simbolos[p[2]]+' '+p[2],  p[3])    
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)

def p_expression_op_bin_equals(p):
    '''expression : expression EQUALBOOL expression
                 | expression UNEQUAL expression
    '''
    p[0] = BinaryOpEquals(p[1], simbolos_igual[p[2]]+' '+p[2], p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)

def p_expression_op_bin_less_greater(p):
    '''expression : expression LESSTHAN expression
                 | expression LESSOREQUALTHAN expression
                 | expression GREATERTHAN expression
                 | expression GREATEROREQUALTHAN expression
    '''
    p[0] = BinaryOpLessGreater(p[1],
                    simbolos.get(p[2],simbolos_igual.get(p[2],None))+' '+p[2],
                                 p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)

def p_expression_op_bin_belong(p):
    '''expression : expression BELONG expression '''
    p[0] = BinaryOpBelong(p[1], simbolos[p[2]]+' '+p[2], p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)
            
def p_expression_op_bin_bool(p):
    '''expression : expression AND expression
                  | expression OR expression '''
    p[0] = BinaryOpBool(p[1], p[2], p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)
    
def p_expression_op_set(p):
    '''expression : expression DOUBLEPLUS expression
                 | expression COUNTERSLASH expression
                 | expression INTERSECCION expression
    '''
    operadores = {
        '++' : 'UNION',
        '\\' : 'DIFFERENCE',
        '><' : 'INTERSECTION'
    }
    p[0] = BinaryOpSet(p[1],  operadores[p[2]]+' '+p[2],  p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)


def p_expression_op_bin_map_to_set(p):
    '''expression : expression MAPPLUS expression
                 | expression  MAPMINUS expression
                 | expression  MAPTIMES expression
                 | expression  MAPDIVIDE expression
                 | expression  MAPREST expression
    '''
    p[0] = BinaryOpMapToSet(p[1], op_mapeados[p[2]]+' '+p[2],  p[3])
    p[0].lineno = p.lineno(2)
    p[0].lexpos = p.lexpos(2)
    
#############################    UNARY OP   ##################################
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryOpUminus("NEGATE " + p[1], p[2])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)

def p_expression_op_not(p):
    'expression : NOT expression'
    p[0] = UnaryOpNot(p[1], p[2])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)
    
def p_expression_op_unary_set(p):
    '''expression : MAXVALUESET expression
                  | MINVALUESET expression
                  | SIZESET expression'''
    p[0] = UnaryOpSet(unarios_conjuntos[p[1]]+' '+p[1],   p[2])
    p[0].lineno = p.lineno(1)
    p[0].lexpos = p.lexpos(1)

#############################    EMPTY    #################################### 
def p_empty(p):
    'empty :'
    pass

##################    PRECEDENCE DEFINED FOR EXPRESSION  #####################
precedence = (
    ("right", 'RPARENT'),
    # language
    ("right", 'IF'  ),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # compare
    ("nonassoc", 'LESSTHAN', 'LESSOREQUALTHAN', 'GREATERTHAN', 'GREATEROREQUALTHAN'),
    ("left", 'EQUALBOOL', 'UNEQUAL'),
    ("nonassoc", 'BELONG'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'INTDIVISION', 'RESTDIVISION'),
    #set
    ('left','DOUBLEPLUS','COUNTERSLASH'),
    ('left','INTERSECCION'),
    #map to set
    ('left','MAPPLUS','MAPMINUS'),
    ('left','MAPTIMES','MAPDIVIDE','MAPREST'),
    #unary over sets
    ('right','MAXVALUESET','MINVALUESET','SIZESET'),
    # int
    ("right", 'UMINUS'),
)

############################     ERRROR HANDLING       #######################
def p_error(p):
    global parser_errors
    if parser_errors: return
    
    if p:
        msg = 'Error de síntaxis en la línea %d , columna %d. '
        msg += 'No se esperaba Token "%s".'
        value = p.value
        try:
            value = p.value
        except TypeError:
            pass
        
        msg = msg % (p.lineno , get_column(p) , value)
    else:
        msg = 'Error de síntasis: No se esperaba final de archivo.'

    parser_errors.append(msg)


def build_parser(program,lexer):
    parser = yacc.yacc(debug=True)
    tree = parser.parse(program,lexer)
    return tree

if __name__ == '__main__':        
    pass