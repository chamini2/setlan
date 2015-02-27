# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Analizador Sintáctico (Parser)
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

import sys
import ply.lex  as lex
import ply.yacc as yacc
from   lexer    import tokens, findColumn
from   AST      import *

# Precedencia de operadores (de menor a mayor)
precedence = (
    ('right','ELSE'),

    # Booleanos
    ('left','OR'),
    ('left','AND'),
    ('right','NOT'),

    # Comparativos
    ('nonassoc', 'EQUALS', 'NOTEQUALS'),
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUALTHAN', 'GREATEREQUALTHAN'),
    ('nonassoc', 'BELONGSTO'),

    # Aritméticos
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULE'),
    
    # Conjuntos
    ('left', 'SETUNION', 'SETDIFF'),    
    ('left','SETINTERSECT'),

    # Conjuntos aritméticos
    ('left','SETMAPPLUS','SETMAPMINUS'),    
    ('left', 'SETMAPTIMES', 'SETMAPDIVIDE', 'SETMAPMODULE'),

    # Unarios
    ('right','SETMINVALUE','SETMAXVALUE','SETSIZE','NEGATE'),

    ('left','LPAREN'),
)

# Regla program: Indica el inicio de un programa en el lenguaje Setlan
def p_program(p):
    '''program : PROGRAM instruction'''
    p[0] = Program(p[1],p[2])

# Regla instruction: Contiene todas las instrucciones válidas del lenguaje
def p_instruction(p):
    '''instruction : block
                   | ifInst
                   | forInst 
                   | whileInst 
                   | repeatInst 
                   | scanInst
                   | printInst
                   | identifier ASSIGN expression'''
    if (len(p)==2):
        p[0] = Instruction(p[1])
    else:
        p[0] = Instruction("",p[1],p[2],p[3])

# Regla block: Indica la existencia de un conjunto de instrucciones
def p_block(p):
    '''block : LCURLY usingInInst RCURLY 
             | LCURLY instructionBlock RCURLY'''
    p[0] = Block(p[1],p[2],p[3])

# Regla usingInInst: Sintaxis de la declaración de variables, seguida de un bloque de instrucciones
def p_usingInInst(p):
    '''usingInInst : USING declarationBlock IN instructionBlock'''
    p[0] = UsingInInst(p[1],p[2],p[3],p[4])

# Regla declarationBlock: Lista de variables declaradas dentro de su bloque respectivo (Luego de un USING)
def p_declarationBlock(p):
    '''declarationBlock : type idList SEMICOLON declarationBlock
                        | type idList SEMICOLON'''
    if len(p) == 5:
        p[0] = DeclarationBlock(p[1],p[2],p[3],p[4])
    else:
        p[0] = DeclarationBlock(p[1],p[2],p[3],"")

# Regla type: Tipos de variables válidas del lenguaje
def p_type(p):
    '''type : INT 
                | BOOL 
                | SET'''
    p[0] = Type(p[1])

# Regla idList: identificador o lista de identificadores dentro de un bloque de declaraciones
def p_idList(p):
    '''idList : IDENTIFIER COMMA idList
              | IDENTIFIER'''
    if len(p) == 4:
        p[0] = IDList(p[1],p[2],p[3],p.lineno(1),findColumn(p.lexer.lexdata,p.lexpos(1)))
    else:
        p[0] = IDList(p[1],"","",p.lineno(1),findColumn(p.lexer.lexdata,p.lexpos(1)))

# Regla instruccionBlock: Contiene las instrucciones dentro de un bloque (block).
#                         Por estar dentro de un bloque terminan con ';'
def p_instructionBlock(p):
    '''instructionBlock : instruction SEMICOLON instructionBlock
                        |'''
    if len(p) == 3:
        p[0] = InstructionBlock(p[1],p[2])
    elif len(p) == 4:
        p[0] = InstructionBlock(p[1],p[2],p[3])
    else:
        p[0] = InstructionBlock()

# Regla ifInst: Regla para la sintaxis de la instrucción if
def p_ifInst(p):
    '''ifInst : IF LPAREN expression RPAREN instruction
              | IF LPAREN expression RPAREN instruction ELSE instruction '''
    if len(p) == 6:
        p[0] = IfInst(p[1],p[2],p[3],p[4],p[5],"","",p.lineno(2),findColumn(p.lexer.lexdata,p.lexpos(2)))
    else:
        p[0] = IfInst(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p.lineno(2),findColumn(p.lexer.lexdata,p.lexpos(2)))

# Regla forInst: Regla para la sintaxis de la instrucción for
def p_forInst(p):
    '''forInst : FOR identifier direction expression DO instruction'''
    p[0] = ForInst(p[1],p[2],p[3],p[4],p[5],p[6])

# Regla direction: Direcciones válidas para el orden de ejecución en una instrucción for.
#                  (de menor a mayor: min, de mayor a menor: max)
def p_direction(p):
    '''direction : MIN
                 | MAX'''
    p[0] = Direction(p[1],p.lineno(1),findColumn(p.lexer.lexdata,p.lexpos(1)+4))

# Regla whileInst: Regla para la sintaxis de la instrucción while
def p_whileInst(p):
    '''whileInst : WHILE LPAREN expression RPAREN DO instruction
                 | WHILE LPAREN expression RPAREN'''
    if len(p) == 7:
        p[0] = WhileInst(p[1],p[2],p[3],p[4],p[5],p[6],p.lineno(2),findColumn(p.lexer.lexdata,p.lexpos(2)))
    else:
        p[0] = WhileInst(p[1],p[2],p[3],p[4],"","",p.lineno(2),findColumn(p.lexer.lexdata,p.lexpos(2)))

# Regla repeatInst: Regla para la sintaxis de la instrucción repeat
def p_repeatInst(p):
    '''repeatInst : REPEAT instruction whileInst'''
    p[0] = RepeatInst(p[1],p[2],p[3])

# Regla scanInst: Regla para la sintaxis de la instrucción scan
def p_scanInst(p):
    '''scanInst : SCAN expression'''
    p[0] = ScanInst(p[1],p[2],p.lineno(1),findColumn(p.lexer.lexdata,p.lexpos(1)))

# Regla printInst: Regla para la sintaxis de la instrucción print/println
def p_printInst(p):
    '''printInst : PRINT outputType
                 | PRINTLN outputType'''
    p[0] = PrintInst(p[1],p[2],p.lineno(1),findColumn(p.lexer.lexdata,p.lexpos(1)))

# Regla outputType: Tipos de salida válidos de la instrucción print/println
def p_outputType(p):
    '''outputType : expression COMMA outputType
                  | expression
                  | string COMMA outputType
                  | string'''
    if (len(p) == 2):
        p[0] = OutputType(p[1])
    else:
        p[0] = OutputType(p[1],p[2],p[3])

# Regla string: Regla que contiene un string (creada para la impresión del árbol)
def p_string(p):
    '''string : STRING'''
    p[0] = String(p[1])

# Regla expression: Regla que contiene todas las expresiones binarias y unarias del lenguaje
def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULE expression
                  | expression AND expression
                  | expression OR expression
                  | expression LESSTHAN expression
                  | expression LESSEQUALTHAN expression
                  | expression GREATERTHAN expression
                  | expression GREATEREQUALTHAN expression
                  | expression EQUALS expression
                  | expression NOTEQUALS expression
                  | expression SETUNION expression
                  | expression SETDIFF expression
                  | expression SETINTERSECT expression
                  | expression SETMAPPLUS expression
                  | expression SETMAPMINUS expression
                  | expression SETMAPTIMES expression
                  | expression SETMAPDIVIDE expression
                  | expression SETMAPMODULE expression
                  | expression BELONGSTO expression
                  | NOT expression
                  | SETMINVALUE expression
                  | SETMAXVALUE expression
                  | SETSIZE expression
                  | MINUS expression %prec NEGATE
                  | LPAREN expression RPAREN
                  | booleanValue
                  | set
                  | identifier
                  | number'''
    if len(p) == 2:
      p[0] = Expression(p[1])
    elif len(p) == 3:
        p[0] = Expression(p[2],p[1])
    else:
        p[0] = Expression(p[1],p[2],p[3])

# Regla booleanValue: Regla que contiene los tipos de expresiones booleanas
def p_booleanValue(p):
    ''' booleanValue : TRUE
                     | FALSE'''
    p[0] = BooleanValue(p[1])

# Regla string: Regla que contiene un identificador (creada para la impresión del árbol)
def p_identifier(p):
    '''identifier : IDENTIFIER'''
    p[0] = ID(p[1],p.lineno(1),findColumn(p.lexer.lexdata,p.lexpos(1)))

# Regla set: Regla para la sintaxis de los conjuntos
def p_set(p):
    '''set : LCURLY setNumbers RCURLY
           | LCURLY RCURLY'''
    if len(p) == 4:
        p[0] = Set(p[1],p[2],p[3])
    else:
        p[0] = Set(p[1],"",p[2])

# Regla setNumber: Regla que contiene el o los números dentro de un conjunto
def p_setNumbers(p):
    '''setNumbers : expression COMMA setNumbers
                  | expression'''
    if len(p) == 2:
        p[0] = SetNumbers(p[1])
    else:
        p[0] = SetNumbers(p[1],p[2],p[3])

# Regla número: Regla que contiene un número (creada para la impresión del árbol)
def p_number(p):
    '''number : NUMBER'''
    p[0] = Number(p[1])

# Regla error: Regla que atrapa los errores de sintaxis y los guarda en una lista
def p_error(p):
    if p:
        yaccError.append('''ERROR: Se encontró un token inesperado "%s" en la Línea %d, Columna %d.''' \
            % (p.value, p.lineno, findColumn(p.lexer.lexdata,p.lexpos)))
    else:
        yaccError.append('''ERROR: No se puede leer. El archivo llegó a su fin.''')

# Construcción del parser
parser = yacc.yacc()
yaccError = []