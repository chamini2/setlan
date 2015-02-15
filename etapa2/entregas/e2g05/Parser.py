
# Analisis Sintactico

import sys
import Class
import Lexer as lexer
import ply.yacc as yacc

# Variable para almacenar el archivo
archivo = ""

def p_Program(p):
	'''programa : tokprogram opencurly bloque closecurly
				| tokprogram instruccion
				| tokprogram opencurly closecurly'''
	if len(p) == 3:
		p[0] = Class.Program(p[2])
	if len(p) == 5:
		p[0] = Class.Program(p[3])
	if len(p) == 4:
		p[0] = Class.Program()



def p_Comentario(p):
	'''comentario : comment
				  | comentario comment'''
	pass
	

def p_Using(p):
	'''bloque : tokusing declaracion tokin instruccion'''
	p[0] = Class.Using(p[2],p[4])

def p_Identificadores(p):
	'''idd : id'''
	p[0] = Class.Identifier(p[1])

#
# Funcion numerico
#
def p_Literal_Numerico(p):
	'''num : number'''
	p[0] = Class.Numeric(p[1])

#
# Funcion String
#
def p_String(p):
	'''str : string'''
	p[0] = Class.String(p[1])

#
# Funcion Declaracion de Variable
# t i;
# t i = e; (con inicializacion)
#
def p_Declaracion_Variable(p):
	'''declaracion : declaracion tipo idd semicolon
				   | declaracion tipo idd assignment expresion semicolon'''
	p[0] = p[1]
	if len(p) == 5:
		p[0].append(Class.Declaracion_Variable(p[2],p[3]))
	if len(p) == 7:
		p[0].append(Class.Declaracion_Variable(p[2],p[3],p[5]))

# Funcion auxiliar base para Declaracion de Variable
def p_Declaracion_Base(p):
	'''declaracion : tipo idd semicolon
			  	   | tipo idd assignment expresion semicolon'''
	p[0] = []
	if len(p) == 4:
		p[0].append(Class.Declaracion_Variable(p[1],p[2]))
	if len(p) == 6:
		p[0].append(Class.Declaracion_Variable(p[1],p[2],p[4]))


# Funcion Asignacion
# identificador = expresion
def p_Asignacion(p):
	'''asignacion : idd assignment expresion semicolon
				  | idd assignment expresion'''
	p[0] = Class.Asignacion(p[1],p[3])


# Funcion booleano
def p_Booleano(p):
	'''bool : toktrue
			| tokfalse'''
	p[0] = Class.Boolean(p[1])

def p_Set(p):
	'''set : tokset'''
	p[0] = Class.Set(p[1])


# Funcion not
# not bool
def p_Expr_Not(p):
	'''expresion : toknot expresion'''
	p[0] = Class.Expresion_Not(p[2])

def p_Expr_Unaria(p):
	'''expresion : minus expresion
			 	 | maxset expresion
				 | minset expresion
				 | lenset expresion'''
	p[0] = Class.Expresion_Unaria(p[1],p[2])

#
# Funcion con los posibles valores de una expresion
#
def p_Valor_Expresion(p):
	'''expresion : idd
				 | num
				 | bool
				 | set'''
	p[0] = p[1]



def p_Tipo(p):
	'''tipo : tokint
			| tokset
			| tokbool'''
	p[0] = p[1]


#
# Funcion con los operadores binarios
# e1 op e2
#
def p_Expr_Binaria(p):
	'''expresion     : expresion plus expresion
					 | expresion minus expresion
					 | expresion multip expresion
					 | expresion div expresion
					 | expresion modset expresion
					 | expresion mod expresion
					 | expresion union expresion
					 | expresion different expresion
					 | expresion intersection expresion
					 | expresion sumset expresion
					 | expresion minusset expresion
					 | expresion multipset expresion
					 | expresion divset expresion
					 | expresion tokor expresion
					 | expresion tokand expresion
					 | expresion less expresion
					 | expresion equalsless expresion
					 | expresion greater expresion
					 | expresion equalsgreater expresion
					 | expresion equals expresion
					 | expresion distinto expresion
					 | expresion arroba expresion'''
	p[0] = Class.Expresion_Binaria(p[1],p[2],p[3])

# Funcion que agrupa por parentesis
# (e)
#
def p_Expr_Parentesis(p):
	'''expresion : leftparen expresion rightparen'''
	p[0] = p[2]

# Funcion scan
def p_Scan(p):
	'''lectura : tokscan idd semicolon'''
	p[0] = Class.Scan(p[2])


# Funcion print
# print <string>
# print <identificador>
def p_print(p):
	'''escritura : tokprint argCadena semicolon 
				 | tokprint argCadena'''
	p[0] = Class.Print(p[2])

def p_println(p):
	'''escritura : tokprintln argCadena semicolon
				 | tokprintln argCadena'''
	p[0] = Class.Println(p[2])

# Funcion auxiliar que contiene la lista de los argumentos del print
def p_ArgCadenasCaracteres_Lista(p):
	'''argCadena : argCadena comma caracteres'''
	p[0] = p[1]
	p[0].append(p[3])

# Funcion auxiliar que contiene el argumento base del print
def p_ArgCadenasCaracteres_Base(p):
	'''argCadena : caracteres'''
	p[0] = []
	p[0].append(p[1])

# Funcion auxiliar que contiene los tipos de argumentos del print
def p_ArgCadenasCaracteres(p):
	'''caracteres : str
				  | expresion'''
	p[0] = p[1]

#
# Funcion Instruccion que contiene la lista de instrucciones
#
def p_Intruccion_Lista(p):
	'''instruccion : instruccion instr_base'''
	p[0] = p[1]
	p[0].append(p[2])

# Funcion auxiliar que contiene una instruccion
def p_Instruccion_Base(p):
	'''instruccion : instr_base'''
	p[0] = []
	p[0].append(p[1])

# Funcion auxiliar que contiene los posibles tipos de una instruccion
def p_Intruccion(p):
	'''instr_base : asignacion
				  | lectura
				  | escritura
				  | condicional
				  | for
				  | while
				  | bloque
				  | repeat'''
	p[0] = p[1]


# Funcion if 
def p_Condicional_If(p):
	'''condicional : tokif expresion instruccion 
	               | tokif expresion instruccion tokelse instruccion 
	               | tokelse instruccion
	               | tokif expresion opencurly instruccion closecurly semicolon
	               | tokelse opencurly instruccion closecurly'''
	if len(p) == 3:
		p[0] = Class.Condicional_Else(p[2])
	if len(p) == 4:					
		p[0] = Class.Condicional_If_Else(p[2],p[3])
	if len(p) == 6:
		p[0] = Class.Condicional_If_Else(p[2],p[3],p[5])
	if len(p) == 7:
		p[0] = Class.Condicional_If_Else(p[2],p[4])
	if len(p) == 5:
		p[0] = Class.Condicional_Else(p[3])

#ef p_Condicional_Else(p):
	#'''condicional:  tokelse opencurly instruccion closecurly semicolon'''
	#p[0] = Class.Condicional_Else(p[3])

def p_Direccion(p):
	''' direccion : tokmin
				  | tokmax'''
	p[0] = p[1]
#
# Funcion For
# for <variable> <direccion> <expresion set> do <instruccion>
#
def p_Ciclo_For(p):
	'''for : tokfor idd direccion expresion tokdo instruccion semicolon
		   | tokfor idd direccion expresion tokdo instruccion '''
	p[0] = Class.Ciclo_For(p[2],p[3],p[4],p[6])

# Funcion While

def p_Ciclo_While(p):
	'''while : tokwhile expresion tokdo  opencurly instruccion closecurly semicolon
	         | tokwhile expresion semicolon
	         | tokwhile expresion tokdo instruccion'''
	p[0] = Class.Ciclo_While(p[2],p[4])

def p_Repeat(p):
	'''repeat : tokrepeat instruccion while'''
	
	p[0] = Class.Ciclo_Repeat(p[2])

#

# Funcion de error
#
def p_error(p):
	if p is not None:	
		e = "Error de sintaxis \"%s\" (Linea: %d, Columna: %d)"
		print e % (p.value,p.lineno,lexer.column_token(archivo,p))
		exit()		
	else:
	    print "Error de sintaxis: falta de token lo que impide cumplimiento de gramatica"
	    exit()

#
# Lista de precedencia en los operandos
#
precedence = (
	('left','multip','div','mod'),
	('left','plus','minus'),
	('left','intersection'),
	('left','union','different'),
	('left','multipset','divset','modset'),
	('left','sumset','minusset'),	
	('left','arroba'),
	('left','equals','distinto'),	
	('left','greater','less','equalsgreater','equalsless'),
	('left','toknot'),
	('left','tokand'),
	('left','tokor'),
)

#
# Funcion que simula el analizador sintactico del lenguaje Setlan.
#
def analizador_sintactico(archivo_texto):

	try:

		tokens = lexer.tokens
		
		# Abrimos el archivo de texto
		f = open(archivo_texto)

		# Leemos el archivo de texto
		data = f.read()

		global archivo
		archivo = data

		parser = yacc.yacc()
		result = parser.parse(data)

		# Cerramos el archivo de texto
		f.close()

	except IOError:

		print 'ERROR: No se pudo abrir el archivo de texto \"%s\"' % archivo_texto
		exit()

# END Parser.py



