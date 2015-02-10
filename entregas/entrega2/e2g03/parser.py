import ply.yacc as yacc
from lexer import tokens, ERRORS, find_column
from sys import argv
from ast import *

def p_inicio(p):
	"inicio : PROGRAM instruccion"
	p[0] = Program(p[2])

def p_instruccion(p):
	"""instruccion : asignacion
					| if
					| scan
					| print
					| for 
					| repeat
					| bloque 
					| empty"""
	p[0]=p[1]

def p_asignacion(p):
	"asignacion : ID EQUALS expresion"
	p[0] = Assign(Variable(p[1]), p[3])

def p_if(p):
	"if : IF expresion instruccion else"
	p[0] = If(p[2], p[3],p[4])

def p_else(p):
	"""else : empty
		| ELSE instruccion
		| ELSE bloque SEMICOLON"""
	if len(p) != 2:
		p[0]=p[2]

def p_scan(p):
	"scan : SCAN ID"
	p[0] = Read(Variable(p[2]))

def p_print(p):
	"""print : PRINT lista
				| PRINTLN lista"""
	if p[1].upper() == 'PRINT':
		p[0] = Write(p[2])
	else:
		if len(p) == 3:
			p[0] = Write(p[2] + [String('"\\n"')])
		else:
			p[0] = Write([String('"\\n"')])

def p_lista(p):
	"""lista : expresion
				| STRING
				| lista COMMA expresion
				| lista COMMA STRING"""
	if len(p)==2:
		p[0] = [String(p[1])]
	else:
		p[0] = p[1] + [String(p[3])]

def p_orden(p):
	"""orden : MIN
				| MAX"""
	p[0]=p[1]

def p_for(p):
	"""for : FOR ID orden expresion DO instruccion"""
	p[0] = For(Variable(p[2]), p[4], p[6])

def p_repeat(p):
	"""repeat : REPEAT instruccion WHILE expresion
				| REPEAT instruccion WHILE expresion DO instruccion
				| WHILE expresion DO instruccion"""
	if len(p) == 5:
		if p[1].upper()== 'REPEAT':
			p[0] = While(p[4],p[2], None)
		else:
			p[0] = While(p[2], None, p[4])
	else:						
		p[0] = While(p[4], p[2], p[6])

def p_bloque(p):
	"""bloque : OPENCURLY listainstruc CLOSECURLY
				| OPENCURLY USING listad SEMICOLON IN listainstruc CLOSECURLY"""
	if len(p) == 4:
		p[0] = Block(p[2],None)
	else:
		p[0] = Block(p[6],p[3])


def p_listad(p):	
	"""listad : tipo listacoma
				| listad SEMICOLON tipo listacoma"""
	if len(p) == 3:
		p[0] = [(p[1], p[2])]
	else:
		p[0] = p[1] + [(p[3], p[4])]

def p_listacoma(p):
	"""listacoma : ID
					| listacoma COMMA ID"""
	if len(p) == 2:
		p[0] = [Variable(p[1])]
	else:
		p[0] = p[1] + [Variable(p[3])]

def p_tipo(p):
	"""tipo : INT
			| SET
			| BOOL"""
	p[0]=p[1]

def p_listainstruc(p):
	"""listainstruc : instruccion 
					| listainstruc SEMICOLON instruccion"""
	if len(p) == 2:
		p[0] = [p[1]]
	else:
		p[0] = p[1] + [p[3]]

def p_empty(p):
	"""empty :"""
	pass

def p_expresion_a(p):
	"""expresion : NUMBER"""
	p[0] = Int(p[1])

def p_expresion_b(p):
	"""expresion : TRUE
					| FALSE"""
	p[0] = Bool(p[1].upper())

def p_expresion_c(p):
	"""expresion : ID"""
	p[0] = Variable(p[1])

def p_expresion_d(p):
	"""expresion : OPENPAREN expresion CLOSEPAREN"""
	p[0] = p[2]

def p_expresion_e(p):
	"""expresion : expresion PLUS expresion
					| expresion MINUS expresion
					| expresion TIMES expresion
					| expresion DIVIDE expresion
					| expresion MOD expresion"""
	operator = {
		'+': 'PLUS',
		'-': 'MINUS',
		'*': 'TIMES',
		'/': 'DIVIDE',
		'%': 'MOD'
	}[p[2]]
	p[0] = Binary(operator, p[1], p[3])


def p_expresion_f(p):
	"""expresion : MINUS expresion
					| NOT expresion
					| MAXSET expresion
					| MINSET expresion
					| NSET expresion"""

	if p[1].upper() == 'MINUS':
		p[0] = Unary('MINUS', p[2])
	if p[1].upper() == 'NOT':
		p[0] = Unary('NOT', p[2])
	if p[1].upper() == 'MAXSET':
		p[0] = Unary('MAXSET', p[2])
	if p[1].upper() == 'MINSET':
		p[0] = Unary('MINSET', p[2])
	if p[1].upper() == 'NSET':
		p[0] = Unary('NSET', p[2])



def p_expresion_g(p):
	"""expresion : set"""
	p[0]=p[1]

def p_expresion_h(p):
	"""expresion : expresion INTERSECTION expresion
					| expresion  DIF expresion
					| expresion UNION expresion
					| expresion PLUSSET expresion
					| expresion MINUSSET expresion
					| expresion TIMESSET expresion
					| expresion DIVIDESET expresion
					| expresion MODSET expresion
					| expresion COMPARE expresion
					| expresion AT expresion
					| expresion AND expresion
					| expresion OR expresion
					| expresion NOT expresion
					| expresion LESSEQUALS expresion
					| expresion GREATEREQUALS expresion
					| expresion NOTEQUALS expresion
					| expresion LESS expresion
					| expresion GREATER expresion"""
	operator = {
		'><': 'INTERSECTION',
		'\\': 'DIF',
		'++': 'UNION',
		'<+>': 'PLUSSET',
		'<->': 'MINUSSET',
		'<*>': 'TIMESSET',
		'<%>': 'MODSET',
		'==': 'COMPARE',
		'@': 'AT',
		'and': 'AND',
		'or': 'OR',
		'not': 'NOT',
		'<=': 'LESSEQUALS',
		'>=': 'GREATEREQUALS',
		'/=': 'NOTEQUALS',
		'<': 'LESS',
		'>': 'GREATER'
	}[p[2]]
	p[0] = Binary(operator, p[1], p[3])


					
					
def p_set(p):
	"""set : OPENCURLY numeros CLOSECURLY"""
	p[0]=p[2]

def p_numeros(p):
	"""numeros : expresion sig"""
	if p[2]!=None:
		p[0]= [p[1]] + p[2]

def p_sig(p):
	"""sig : COMMA expresion sig
			| empty"""
	if (len(p)==4 and p[3]!=None):
		p[0] = [p[2]] + p[3]

precedence = (
	# bool
	("left", 'OR'),
	("left", 'AND'),
	("right", 'NOT'),

	# compare
	("nonassoc", 'AT'),
	("nonassoc", 'COMPARE', 'NOTEQUALS'),
	("nonassoc", 'LESS', 'LESSEQUALS', 'GREATER', 'GREATEREQUALS'),

	# set
	("left", 'INTERSECTION'),
	("left", 'UNION'),
	("right", 'DIF'),
	("left", 'PLUSSET', 'MINUSSET'),
	("left", 'TIMESSET', 'DIVIDESET', 'MODSET'),
	("right", 'MINSET', 'MAXSET', 'NSET'),
	
	# int
	("left", 'PLUS', 'MINUS'),
	("left", 'TIMES', 'DIVIDE', 'MOD'),

	# int
	("right", 'MINUS'),
)
	

def p_error(symbol):
    if symbol:
        text = symbol.lexer.lexdata
        message = "ERROR: Syntax error at line %d, column %d: "
        message += "Unexpected token '%s'"
        data = (symbol.lineno-len(open(argv[1]).readlines()), find_column(text, symbol), symbol.value)
        parser_error.append(message % data)
    else:
        parser_error.append("ERROR: Syntax error at EOF")


parser = yacc.yacc(start="inicio")
parser_error = []


def parsing(data, debug=0):
    parser.error = 0
    ast = parser.parse(data, debug=debug)
    if parser.error:
        ast = None
    return ast

def main(argv=None):
    import sys # argv, exit
    if argv is None:
        argv = sys.argv
    if len(argv) == 1:
        print "ERROR: No input file"
        return
    elif len(argv) > 3:
        print "ERROR: Invalid number of arguments"
        return
    if len(argv) == 3:
        debug = eval(argv[2])
    else:
        debug = 0

    file_string = open(argv[1], 'r').read()
    ast = parsing(file_string, debug)

    if ERRORS:
        ast = None
        for error in ERRORS:
            print error
    elif parser_error:
        ast = None
        for error in parser_error:
            print error
    else:
        print ast

    print ast

if __name__ == "__main__":
    main()
