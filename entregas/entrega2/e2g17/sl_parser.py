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
	def __init__(self, type, children=None, val=None):
		self.type = type
		if children: 
			self.children = children
		else:
			self.children = []
		self.val = val

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
			 | block
			 | empty'''
	p[0] = p[1]

def p_block(p):
	'''block : LCURLY RCURLY
			 | LCURLY print_inblock RCURLY
			 | LCURLY instr_block RCURLY
			 | LCURLY using instr_block RCURLY'''
	p[0] = [Node("block_end", None, "BLOCK_END")]
	if len(p) == 3:
		p[0] = [Node("block", None, "BLOCK")] + p[0]
	elif len(p) == 4:
		p[0] = [Node("block", p[2], "BLOCK")] + p[0]
	else:
		if p[3]:
			p[0] = [Node("block", p[2] + p[3], "BLOCK")] + p[0]
		else:
			p[0] = [Node("block", p[2], "BLOCK")] + p[0]

def p_instr(p):
	'''instr : print
			 | condition
			 | loop
			 | for_loop
			 | empty'''
	p[0] = p[1]

def p_instr_block(p):
	'''instr_block : assign instr_block
			 	   | scan instr_block
				   | print_inblock instr_block
				   | condition_block instr_block
				   | loop_block instr_block
				   | for_loop_block instr_block
				   | empty'''
	p[0] = p[1]
	if len(p) == 3 and p[2]:
		p[0] = p[0] + p[2]

def p_using(p):
	'''using : USING vardec IN'''
	p[0] = [Node("using", p[2], "USING"), Node("in", None, "IN")]

def p_vardec(p):
	'''vardec : type var_list SEMICOLON
			  | type var_list SEMICOLON vardec'''
	p[0] = []

	var_list = ""
	for var in p[2]:
		var_list = var_list + var + ", "
	var_list = var_list[:-2]

	p[0] = p[0] + [Node("vardec", None, str(p[1]) + " " + var_list)]
	if len(p) == 5:
		p[0] = p[0] + p[4]

def p_type(p):
	'''type : INT
			| BOOL
			| SET'''
	p[0] = p[1]

def p_var_list(p):
	'''var_list : identifier
				| identifier COMMA var_list'''
	p[0] = [p[1]]
	if len(p) == 4:
		p[0] = p[0] + p[3]

def p_assign(p):
	'''assign : identifier ASSIGN assign_expr SEMICOLON'''
	p[0] = [Node("assign", [Node("var_stmt", [Node("variable", None, str(p[1]))], "variable"), Node("value", p[3], "value")], "ASSIGN")]

def p_assign_expr(p):
	'''assign_expr : expr
				   | setexpr
				   | boolexpr'''
	p[0] = p[1]

def p_scan(p):
	'''scan : SCAN identifier SEMICOLON'''
	p[0] = [Node("scan", [Node("var_stmt", [Node("variable", None, str(p[2]))], "variable")], "SCAN")]

### INSTRUCCIONES PRINT

def p_print(p):
	'''print : PRINT elements'''
	p[0] = [Node("print", [Node("elem_stmt", p[2], "elements")], "PRINT")]

def p_print_inblock(p):
	'''print_inblock : PRINT elements SEMICOLON'''
	p[0] = [Node("print", [Node("elem_stmt", p[2], "elements")], "PRINT")]

def p_println(p):
	'''print : PRINTLN elements'''
	p[0] = [Node("print", [Node("elem_stmt", p[2] + [Node("str_stmt", [Node("string", None, "\"\\n\"")], "string")], "elements")], "PRINT")]

def p_println_inblock(p):
	'''print_inblock : PRINTLN elements SEMICOLON'''
	p[0] = [Node("print", [Node("elem_stmt", p[2] + [Node("str_stmt", [Node("string", None, "\"\\n\"")], "string")], "elements")], "PRINT")]

def p_elements(p):
	'''elements : expr
				| setexpr
				| boolexpr
				| elements COMMA elements'''
	p[0] = []
	if len(p) == 2:
		p[0] = p[1]
	else:
		if p[1]:
			p[0] = p[1] + p[3]

def p_elements_string(p):
	'''elements : STRING'''
	p[0] = [Node("str_stmt", [Node("string", None, str(p[1]))], "string")]

### TERMINOS

def p_integer(p):
	'''integer : INTEGER'''
	p[0] = p[1]

def p_term_int(p):
	'''term : integer'''
	p[0] = [Node("int_stmt", [Node("int", None, str(p[1]))], "int")]

def p_identifier(p):
	'''identifier : IDENTIFIER'''
	p[0] = p[1]

def p_term_id(p):
	'''term : identifier'''
	p[0] = [Node("var_stmt", [Node("variable", None, str(p[1]))], "variable")]

### EXPRESIONES ARITMETICAS

def p_expr_simple(p):
	'''expr : term
			| LPAREN expr RPAREN
			| MINUS expr %prec UMINUS'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if p[1] == '-': 
			p[0] = [Node("negate_stmt", p[2], "NEGATE -")]
		else: 
			p[0] = p[2]

def p_expr_binopr(p):
	'''expr : expr PLUS expr
			| expr MINUS expr
			| expr ASTERISK expr
			| expr INTDIV expr
			| expr PERCENT expr'''
	if p[2] == '+': p[0] = [Node("expr_binopr", p[1] + p[3], "PLUS +")]
	elif p[2] == '-': p[0] = [Node("expr_binopr", p[1] + p[3], "MINUS -")]
	elif p[2] == '*': p[0] = [Node("expr_binopr", p[1] + p[3], "TIMES *")]
	elif p[2] == '/': p[0] = [Node("expr_binopr", p[1] + p[3], "INTDIV /")]
	elif p[2] == '%': p[0] = [Node("expr_binopr", p[1] + p[3], "PERCENT %")]

### EXPRESIONES DE CONJUNTOS

def p_set(p):
	'''set : LCURLY setelem RCURLY
		   | identifier'''
	if len(p) == 4:
		p[0] = [Node("set_stmt", p[2], "set")]
	else:
		p[0] = [Node("var_stmt", [Node("variable", None, str(p[1]))], "variable")]

def p_setelem(p):
	'''setelem : expr
			   | expr COMMA setelem'''
	p[0] = p[1]
	if len(p) == 4:
		p[0] = p[0] + p[3]

def p_setexpr_simple(p):
	'''setexpr : LPAREN setexpr RPAREN'''
	p[0] = p[2]

def p_setexpr_binopr(p):
	'''setexpr : set
			   | setexpr UNION setexpr
			   | setexpr INTERSECTION setexpr
			   | setexpr COMPLEMENT setexpr'''
	if len(p) == 2:	
		p[0] = p[1]
	else:
		if p[2] == '++': p[0] = [Node("setexpr_binopr", p[1] + p[3], "UNION ++")]
		elif p[2] == '><': p[0] = [Node("setexpr_binopr", p[1] + p[3], "INTERSECTION ><")]
		elif p[2] == '\\': p[0] = [Node("setexpr_binopr", p[1] + p[3], "COMPLEMENT \\")]

def p_setexpr_mapopr(p):
	'''setexpr : term SETSUM set
			   | term SETSUBSTRACT set
			   | term SETMULT set
			   | term SETDIV set
			   | term SETMOD set'''
	if p[2] == '<+>': p[0] = [Node("setexpr_mapopr", p[1] + p[3], "SETPLUS <+>")]
	elif p[2] == '<->': p[0] = [Node("setexpr_mapopr", p[1] + p[3], "SETMINUS <->")]
	elif p[2] == '<*>': p[0] = [Node("setexpr_mapopr", p[1] + p[3], "SETTIMES <*>")]
	elif p[2] == '</>': p[0] = [Node("setexpr_mapopr", p[1] + p[3], "SETDIVIDE </>")]
	elif p[2] == '<%>': p[0] = [Node("setexpr_mapopr", p[1] + p[3], "SETMODULO <%>")]

def p_setexpr_unropr(p):
	'''setexpr : SETMAX set
			   | SETMIN set
			   | SETLENGTH set'''
	if p[1] == ">?": p[0] = [Node("setexpr_unropr", p[2], "MAX >?")]
	elif p[1] == "<?": p[0] = [Node("setexpr_unropr", p[2], "MIN <?")]
	elif p[1] == "$?": p[0] = [Node("setexpr_unropr", p[2], "SIZE $?")]

### EXPREISONES BOOLEANAS

def p_boolexpr_simple(p):
	'''boolexpr : term
				| NOT boolexpr
				| LPAREN boolexpr RPAREN'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 3:
		p[0] = [Node("not_stmt", p[2], "NOT not")]
	else:
		p[0] = p[2]

def p_boolexpr_const(p):
	'''boolexpr : TRUE
				| FALSE'''
	p[0] = [Node("const_stmt", [Node("const", None, str(p[1]))], "constant")]

def p_boolexpr_binopr(p):
	'''boolexpr : boolexpr AND boolexpr
				| boolexpr OR boolexpr'''
	if p[2] == 'and': p[0] = [Node("boolexpr_binopr", p[1] + p[3], "AND and")]
	elif p[2] == 'or': p[0] = [Node("boolexpr_binopr", p[1] + p[3], "OR or")]

def p_boolexpr_cmpopr(p):
	'''boolexpr : term LESSTHAN term
				| term GREATERTHAN term
				| term LTOREQUAL term
				| term GTOREQUAL term
				| term EQUAL term
				| term NOTEQUAL term'''
	if p[2] == '<': p[0] = [Node("boolexpr_cmpopr", p[1] + p[3], "LESS <")]
	elif p[2] == '>': p[0] = [Node("boolexpr_cmpopr", p[1] + p[3], "GREATER >")]
	elif p[2] == '<=': p[0] = [Node("boolexpr_cmpopr", p[1] + p[3], "LESSEQ <=")]
	elif p[2] == '>=': p[0] = [Node("boolexpr_cmpopr", p[1] + p[3], "GREATEREQ >=")]
	elif p[2] == '==': p[0] = [Node("boolexpr_cmpopr", p[1] + p[3], "EQUAL ==")]
	elif p[2] == '/=': p[0] = [Node("boolexpr_cmpopr", p[1] + p[3], "UNEQUAL /=")]

def p_boolexpr_seteqopr(p):
	'''boolexpr : set EQUAL set
				| set NOTEQUAL set'''
	if p[2] == '==': p[0] = [Node("boolexpr_seteqopr", p[1] + p[3], "EQUAL ==")]
	elif p[2] == '/=': p[0] = [Node("boolexpr_seteqopr", p[1] + p[3], "UNEQUAL /=")]

def p_boolexpr_setcont(p):
	'''boolexpr : term ARROBA set'''
	if p[2] == '@': p[0] = [Node("boolexpr_setcont", p[1] + p[3], "CONTAINS @")]	

### BLOQUES CONDICIONALES

def p_condition(p):
	'''condition : IF LPAREN boolexpr RPAREN instr
				 | IF LPAREN boolexpr RPAREN instr ELSE instr
				 | IF LPAREN boolexpr RPAREN instr ELSE instr_block
				 | IF LPAREN boolexpr RPAREN instr_block ELSE instr'''
	if len(p) == 6:
		p[0] = [Node("if_stmt", [Node("cond_stmt", p[3], "condition"), Node("then_stmt", p[5], "THEN")], "IF")]
	else:
		p[0] = [Node("if_stmt", [Node("cond_stmt", p[3], "condition"), Node("then_stmt", p[5], "THEN"), Node("else_stmt", p[7], "ELSE")], "IF")]

def p_condition_block(p):
	'''condition_block : IF LPAREN boolexpr RPAREN block
					   | IF LPAREN boolexpr RPAREN instr ELSE block SEMICOLON
					   | IF LPAREN boolexpr RPAREN instr_block ELSE block SEMICOLON
					   | IF LPAREN boolexpr RPAREN block ELSE instr
					   | IF LPAREN boolexpr RPAREN block ELSE instr_block
					   | IF LPAREN boolexpr RPAREN block ELSE block SEMICOLON
					   | condition'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 6:
		p[0] = [Node("if_stmt", [Node("cond_stmt", p[3], "condition"), Node("then_stmt", p[5], "THEN")], "IF")]
	else:
		p[0] = [Node("if_stmt", [Node("cond_stmt", p[3], "condition"), Node("then_stmt", p[5], "THEN"), Node("else_stmt", p[7], "ELSE")], "IF")]

### BLOQUES DE LOOP

def p_loop_repeat(p):
	'''loop : REPEAT instr WHILE LPAREN boolexpr RPAREN DO instr SEMICOLON
			| REPEAT instr WHILE LPAREN boolexpr RPAREN DO instr_block SEMICOLON
			| REPEAT instr_block WHILE LPAREN boolexpr RPAREN DO instr
			| REPEAT instr_block WHILE LPAREN boolexpr RPAREN DO instr_block
			| REPEAT instr WHILE LPAREN boolexpr RPAREN
			| REPEAT instr_block WHILE LPAREN boolexpr RPAREN'''
	if len(p) == 9:
		p[0] = [Node("repeat_stmt", p[2], "REPEAT"), Node("while_stmt", [Node("cond_stmt", p[5], "condition")], "WHILE"), Node("do_stmt", p[8], "DO")]
	else:
		p[0] = [Node("repeat_stmt", p[2], "REPEAT"), Node("while_stmt", [Node("cond_stmt", p[5], "condition")], "WHILE")]

def p_loop_while(p):
	'''loop : WHILE LPAREN boolexpr RPAREN DO instr
			| WHILE LPAREN boolexpr RPAREN DO instr_block'''
	p[0] = [Node("while_stmt", [Node("cond_stmt", p[3], "condition")], "WHILE"), Node("do_stmt", p[6], "DO")]

def p_loop_repeat_block(p):
	'''loop_block : REPEAT instr WHILE LPAREN boolexpr RPAREN DO block SEMICOLON
				  | REPEAT instr_block WHILE LPAREN boolexpr RPAREN DO block
				  | REPEAT block WHILE LPAREN boolexpr RPAREN DO instr
				  | REPEAT block WHILE LPAREN boolexpr RPAREN DO instr_block
				  | REPEAT block WHILE LPAREN boolexpr RPAREN DO block SEMICOLON
				  | REPEAT block WHILE LPAREN boolexpr RPAREN
				  | loop'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 9:
		p[0] = [Node("repeat_stmt", p[2], "REPEAT"), Node("while_stmt", [Node("cond_stmt", p[5], "condition")], "WHILE"), Node("do_stmt", p[8], "DO")]
	else:
		p[0] = [Node("repeat_stmt", p[2], "REPEAT"), Node("while_stmt", [Node("cond_stmt", p[5], "condition")], "WHILE")]

def p_loop_while_block(p):
	'''loop_block : WHILE LPAREN boolexpr RPAREN DO block SEMICOLON'''
	p[0] = [Node("while_stmt", [Node("cond_stmt", p[3], "condition")], "WHILE"), Node("do_stmt", p[6], "DO")]

def p_for_loop(p):
	'''for_loop : FOR identifier direction setexpr DO instr
				| FOR identifier direction setexpr DO instr_block'''
	p[0] = [Node("for_stmt", [Node("var_stmt", [Node("variable", None, str(p[2]))], "variable")] + p[3] + [Node("in", None, "IN")] + p[4] + [Node("do_stmt", p[6], "DO")], "FOR")]

def p_for_loop_block(p):
	'''for_loop_block : FOR identifier direction setexpr DO block
					  | for_loop'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = [Node("for_stmt", [Node("var_stmt", [Node("variable", None, str(p[2]))], "variable")] + p[3] + [Node("in", None, "IN")] + p[4] + [Node("do_stmt", p[6], "DO")], "FOR")]

def p_direction(p):
	'''direction : MIN
				 | MAX'''
	p[0] = [Node("dir_stmt", [Node("dir", None, str(p[1]))], "direction")]

### ERROR DEL PARSER

def p_error(p):
	global error_par
	error_par.append(p)

def get_errors():
	return error_par

### CONSTRUCCION DEL PARSER

def build_parser():
	parser = yacc.yacc()
	return parser