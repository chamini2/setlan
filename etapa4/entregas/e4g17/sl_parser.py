# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Segunda entrega del proyecto.             #
#   Parser para el lenguaje Setlan            #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

import ply.yacc as yacc
from sl_lexer import tokens

# Variable global error_par

error_par = []

# Definicion de la clase Node utilizada para la construccion del AST

class Node:
	def __init__(self, type, children=None, val=None, lineno=0, colno=0):
		self.type = type
		if children: 
			self.children = children
		else:
			self.children = []
		self.val = val
		self.lineno = lineno
		self.colno = colno

	def to_string(self, nivel=1):
		s = str(self.val) + "\n"
		if self.children:
			for child in self.children:
				s = s + "\t"*(nivel) + child.to_string(nivel+1)
		return s

	def __str__(self):
		return self.to_string()

# PARSER

# PRECEDENCIA entre operadores, de menor a mayor

precedence = (
	# Asociatividad del 'else_stmt' con el 'if_stmt'-'then-stmt' mas cercano
	('right', 'THEN', 'ELSE'),

	# Operadores sobre bool
	('left', 'OR'),
	('left', 'AND'),
	('right', 'NOT'),

	# Operadores comparativos
	('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'LTOREQUAL', 'GTOREQUAL'),
	('nonassoc', 'EQUAL', 'NOTEQUAL'),

	# Operadores aritmeticos
	('left', 'PLUS', 'MINUS'),
	('left', 'ASTERISK', 'INTDIV', 'PERCENT'),
	('right', 'UMINUS'),

	# Operadores sobre conjuntos
	('left', 'UNION', 'COMPLEMENT'),
	('left', 'INTERSECTION'),

	# Operadores entre conjuntos-aritmeticas
	('nonassoc', 'SETSUM', 'SETSUBSTRACT'),
	('nonassoc', 'SETMULT', 'SETDIV', 'SETMOD'),
	('nonassoc', 'ARROBA'),

	# Operadores unarios sobre conjuntos
	('nonassoc', 'SETMAX', 'SETMIN', 'SETLENGTH'),
)

# REGLAS DE LA GRAMATICA

def p_program(p):
	'''program : PROGRAM start'''
	p[0] = Node("program", p[2], "PROGRAM")

def p_empty(p):
	'empty :'
	pass

def p_start(p):
	'''start : print
			 | block'''
	p[0] = p[1]

def p_block(p):
	'''block : LCURLY instr_block RCURLY
			 | LCURLY using instr_block RCURLY'''
	p[0] = [Node("block_end", None, "BLOCK_END")]
	if len(p) == 3: p[0] = [Node("block", None, "BLOCK")] + p[0]
	elif len(p) == 4: p[0] = [Node("block", p[2], "BLOCK")] + p[0]
	else:
		if p[3]: p[0] = [Node("block", p[2] + p[3], "BLOCK")] + p[0]
		else: p[0] = [Node("block", p[2], "BLOCK")] + p[0]

def p_instr(p):
	'''instr : assign
			 | scan
			 | print
			 | condition
			 | loop
			 | for_loop'''
	p[0] = p[1]

def p_instr_block(p):
	'''instr_block : instr SEMICOLON instr_block
				   | block SEMICOLON instr_block
			 	   | empty'''
	p[0] = p[1]
	if len(p) == 4 and p[3]: p[0] = p[0] + p[3]

def p_using(p):
	'''using : USING vardec IN'''
	p[0] = [Node("using", p[2], "USING"), Node("in", None, "IN")]

def p_vardec(p):
	'''vardec : type var_list SEMICOLON
			  | type var_list SEMICOLON vardec'''
	p[0] = []
	for var in p[2]:
		p[0] = p[0] + [Node("vardec", None, str(p[1]) + " " + str(var.val), lineno=var.lineno, colno=var.colno)]
	if len(p) == 5: p[0] = p[0] + p[4]

def p_type(p):
	'''type : INT
			| BOOL
			| SET'''
	p[0] = p[1]

def p_var_list(p):
	'''var_list : identifier
				| var_list COMMA identifier'''
	if len(p) == 2: p[0] = p[1]
	else: p[0] = p[1] + p[3]

def p_assign(p):
	'''assign : identifier ASSIGN expr'''
	p[0] = [Node("assign", [Node("var_stmt", p[1], "variable"), Node("value", p[3], "value")], "ASSIGN")]

def p_scan(p):
	'''scan : SCAN identifier'''
	p[0] = [Node("scan", [Node("var_stmt", p[2], "variable")], "SCAN")]

### INSTRUCCIONES PRINT

def p_print(p):
	'''print : PRINT elements'''
	p[0] = [Node("print", [Node("elem_stmt", p[2], "elements")], "PRINT")]

def p_println(p):
	'''print : PRINTLN elements'''
	p[0] = [Node("print", [Node("elem_stmt", p[2] + [Node("str_stmt", [Node("string", None, "\"\\n\"")], "string")], "elements")], "PRINT")]

def p_elements(p):
	'''elements : expr
				| string
				| elements COMMA expr
				| elements COMMA string'''
	if len(p) == 2: p[0] = p[1]
	else: p[0] = p[1] + p[3]

### TERMINOS

def p_integer(p):
	'''integer : INTEGER'''
	p[0] = [Node("int", None, str(p[1]))]

def p_term_int(p):
	'''term : integer'''
	p[0] = [Node("int_stmt", p[1], "int")]

def p_bool_const(p):
	'''bool : TRUE
			| FALSE'''
	p[0] = [Node("const", None, str(p[1]))]

def p_term_bool_const(p):
	'''term : bool'''
	p[0] = [Node("const_stmt", p[1], "constant")]

def p_identifier(p):
	'''identifier : IDENTIFIER'''
	p[0] = [Node("variable", None, str(p[1]), lineno=p.lineno(1), colno=p.lexpos(1))]

def p_term_id(p):
	'''term : identifier'''
	p[0] = [Node("var_stmt", p[1], "variable")]

def p_set(p):
	'''set : LCURLY empty RCURLY
		   | LCURLY setelem RCURLY'''
	p[0] = p[2]

def p_setelem(p):
	'''setelem : expr
			   | setelem COMMA expr'''
	if len(p) == 2: p[0] = p[1]
	else: p[0] = p[1] + p[3]

def p_term_set(p):
	'''term : set'''
	p[0] = [Node("set_stmt", p[1], "set")]

def p_string(p):
	'''string : STRING'''
	p[0] = [Node("str_stmt", [Node("string", None, str(p[1]))], "string")]

### EXPRESIONES

def p_expr_simple(p):
	'''expr : term
			| LPAREN expr RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[2]

def p_expr_binopr(p):
	'''expr : expr AND expr
			| expr OR expr
			| expr LESSTHAN expr
			| expr GREATERTHAN expr
			| expr LTOREQUAL expr
			| expr GTOREQUAL expr
			| expr EQUAL expr
			| expr NOTEQUAL expr
			| expr PLUS expr
			| expr MINUS expr
			| expr ASTERISK expr
			| expr INTDIV expr
			| expr PERCENT expr
			| expr UNION expr
			| expr INTERSECTION expr
			| expr COMPLEMENT expr
			| expr SETSUM expr
			| expr SETSUBSTRACT expr
			| expr SETMULT expr
			| expr SETDIV expr
			| expr SETMOD expr
			| expr ARROBA expr'''
	if p[2] == 'and': p[0] = [Node("bool_binopr", p[1] + p[3], "AND and")]
	elif p[2] == 'or': p[0] = [Node("bool_binopr", p[1] + p[3], "OR or")]

	elif p[2] == '<': p[0] = [Node("expr_cmpopr", p[1] + p[3], "LESS <")]
	elif p[2] == '>': p[0] = [Node("expr_cmpopr", p[1] + p[3], "GREATER >")]
	elif p[2] == '<=': p[0] = [Node("expr_cmpopr", p[1] + p[3], "LESSEQ <=")]
	elif p[2] == '>=': p[0] = [Node("expr_cmpopr", p[1] + p[3], "GREATEREQ >=")]
	elif p[2] == '==': p[0] = [Node("expr_cmpopr", p[1] + p[3], "EQUAL ==")]
	elif p[2] == '/=': p[0] = [Node("expr_cmpopr", p[1] + p[3], "UNEQUAL /=")]

	elif p[2] == '+': p[0] = [Node("expr_binopr", p[1] + p[3], "PLUS +")]
	elif p[2] == '-': p[0] = [Node("expr_binopr", p[1] + p[3], "MINUS -")]
	elif p[2] == '*': p[0] = [Node("expr_binopr", p[1] + p[3], "TIMES *")]
	elif p[2] == '/': p[0] = [Node("expr_binopr", p[1] + p[3], "INTDIV /")]
	elif p[2] == '%': p[0] = [Node("expr_binopr", p[1] + p[3], "PERCENT %")]

	elif p[2] == '++': p[0] = [Node("set_binopr", p[1] + p[3], "UNION ++")]
	elif p[2] == '><': p[0] = [Node("set_binopr", p[1] + p[3], "INTERSECTION ><")]
	elif p[2] == '\\': p[0] = [Node("set_binopr", p[1] + p[3], "COMPLEMENT \\")]

	elif p[2] == '<+>': p[0] = [Node("set_mapopr", p[1] + p[3], "SETPLUS <+>")]
	elif p[2] == '<->': p[0] = [Node("set_mapopr", p[1] + p[3], "SETMINUS <->")]
	elif p[2] == '<*>': p[0] = [Node("set_mapopr", p[1] + p[3], "SETTIMES <*>")]
	elif p[2] == '</>': p[0] = [Node("set_mapopr", p[1] + p[3], "SETDIVIDE </>")]
	elif p[2] == '<%>': p[0] = [Node("set_mapopr", p[1] + p[3], "SETMODULO <%>")]

	elif p[2] == '@': p[0] = [Node("expr_setcont", p[1] + p[3], "CONTAINS @")]

	p[0][0].lineno = p.lineno(2)
	p[0][0].colno = p.lexpos(2)

def p_expr_unropr(p):
	'''expr : NOT expr
			| SETMAX expr
			| SETMIN expr
			| SETLENGTH expr
			| MINUS expr %prec UMINUS'''
	if p[1] == "not": p[0] = [Node("not_stmt", p[2], "NOT not")]
	elif p[1] == ">?": p[0] = [Node("set_unropr", p[2], "MAX >?")]
	elif p[1] == "<?": p[0] = [Node("set_unropr", p[2], "MIN <?")]
	elif p[1] == "$?": p[0] = [Node("set_unropr", p[2], "SIZE $?")]
	elif p[1] == '-': p[0] = [Node("negate_stmt", p[2], "NEGATE -")]

	p[0][0].lineno = p.lineno(1)
	p[0][0].colno = p.lexpos(1)

### BLOQUES CONDICIONALES

def p_condition(p):
	'''condition : IF LPAREN expr RPAREN instr %prec THEN
				 | IF LPAREN expr RPAREN block %prec THEN
				 | IF LPAREN expr RPAREN instr ELSE instr
				 | IF LPAREN expr RPAREN instr ELSE block
				 | IF LPAREN expr RPAREN block ELSE instr
				 | IF LPAREN expr RPAREN block ELSE block'''
	if len(p) == 6:
		p[0] = [Node("if_stmt", [Node("cond_stmt", p[3], "condition"), Node("then_stmt", p[5], "THEN")], "IF")]
	else:
		p[0] = [Node("if_stmt", [Node("cond_stmt", p[3], "condition"), Node("then_stmt", p[5], "THEN"), Node("else_stmt", p[7], "ELSE")], "IF")]

	p[0][0].lineno = p.lineno(1)
	p[0][0].colno = p.lexpos(1)

### BLOQUES DE LOOP

def p_loop_repeat(p):
	'''loop : REPEAT instr WHILE LPAREN expr RPAREN
			| REPEAT block WHILE LPAREN expr RPAREN
			| REPEAT instr WHILE LPAREN expr RPAREN DO instr
			| REPEAT instr WHILE LPAREN expr RPAREN DO block
			| REPEAT block WHILE LPAREN expr RPAREN DO instr
			| REPEAT block WHILE LPAREN expr RPAREN DO block'''
	if len(p) == 9:
		p[0] = [Node("repeat_stmt", p[2], "REPEAT"), Node("while_stmt", [Node("cond_stmt", p[5], "condition")], "WHILE"), Node("do_stmt", p[8], "DO")]
	else:
		p[0] = [Node("repeat_stmt", p[2], "REPEAT"), Node("while_stmt", [Node("cond_stmt", p[5], "condition")], "WHILE")]

	p[0][1].lineno = p.lineno(3)
	p[0][1].colno = p.lexpos(3)

def p_loop_while(p):
	'''loop : WHILE LPAREN expr RPAREN DO instr
			| WHILE LPAREN expr RPAREN DO block'''
	p[0] = [Node("while_stmt", [Node("cond_stmt", p[3], "condition")], "WHILE", lineno=p.lineno(1), colno=p.lexpos(1)), Node("do_stmt", p[6], "DO")]

def p_for_loop(p):
	'''for_loop : FOR identifier direction expr DO instr
				| FOR identifier direction expr DO block'''
	p[0] = [Node("for_stmt", [Node("var_stmt", p[2], "variable")] + p[3] + [Node("in", None, "IN")] + p[4] + [Node("do_stmt", p[6], "DO")], "FOR")]

def p_direction(p):
	'''direction : MIN
				 | MAX'''
	p[0] = [Node("dir_stmt", [Node("dir", None, str(p[1]))], "direction")]

### ERROR DEL PARSER

def p_error(p):
	global error_par
	error_par.append(p)

def get_errors():
	global error_par
	return error_par

### CONSTRUCCION DEL PARSER

def build_parser():
	parser = yacc.yacc()
	return parser