#Lexer.py
# Oriana Graterol 10-11248
# Samuel Rodriguez 09-10728
#!/usr/bin/python


import ply.lex as lex

class Lexer:

	def __init__(self):

		#Lista donde estaran los errores que encontremos.
		self.list_error = []

		# Palabras reservadas.
		self.reserved = {
			'int' : 'tokint',
			'min' : 'tokmin',
			'max' : 'tokmax',
			'repeat' : 'tokrepeat',
			'false' : 'tokfalse',
			'true' : 'toktrue',
			'boolean' : 'tokboolean',
			'not' : 'toknot',
			'using' : 'tokusing',
			'print' : 'tokprint',
			'println' : 'tokprintln',
			'in' : 'tokin',
			'while' : 'tokwhile',
			'set' : 'tokset',
			'if' : 'tokif',
			'then' : 'tokthen',
			'else' : 'tokelse',
			'for' : 'tokfor',
			'do' : 'tokdo',
			'or' : 'tokor',
			'return': 'tokreturn',
			'scan' : 'tokscan',
			'and' : 'tokand',
			'program' : 'tokprogram',

		}

		self.tokens = [
			'semicolon',
			'assignment',
			'comma',
			'point',
			'greater',
			'equalsgreater',
			'less',
			'equalsless',
			'leftparen',
			'rightparen',
			'opencurly',
			'closecurly',
			'equals',
			'distinto',
			'plus',
			'minus',
			'multip',
			'igual',
			'div',
			'mod',
			'number',
			'id',
			'newline',
			'error',
			'comment',
			'string',
			'arroba',
			'desigual',
			'modset',
			'divset',
			'multipset',
			'minusset',
			'sumset',
			'intersection',
			'different',
			'union',
			'lenset',
			'maxset',
			'minset',
		] + list(self.reserved.values())


	# Definimos las expresiones regulares para cada uno de los tokens.

	t_semicolon = r'\;'
	t_assignment = r'\='
	t_comma = r'\,'
	t_point = r'\.'
	t_greater = r'\>'
	t_equalsgreater = r'\>='
	t_less = r'\<'
	t_equalsless = r'\<='
	t_leftparen = r'\('
	t_rightparen = r'\)'
	t_opencurly = r'\{'
	t_closecurly = r'\}'
	t_equals = r'\=='
	t_distinto = r'\/='
	t_plus = r'\+'
	t_minus = r'\-'
	t_multip = r'\*'
	t_igual = r'\='
	t_div = r'\/'
	t_mod = r'\%'
	t_desigual =  r'\='	
	t_arroba = r'\@'
	t_modset = r'\<\%>' 
	t_divset = r'\</>' 
	t_multipset = r'\<\*>'
	t_minusset = r'\<\\->' 
	t_sumset = r'\<\+>' 
	t_intersection = r'\><'
	t_different = r'\\'
	t_union = r'\+\+'
	t_lenset = r'\$\?'
	t_maxset = r'\>\?'
	t_minset = r'\<\?'

	# Para que no lea espacios y tabulaciones
	t_ignore = ' \t'


	# Convertir numero en entero 
	def t_number(self,t):
		r'[-+]?[0-9]*\.?[0-9]+'
		t.value = int(t.value)
		return 

	# Los identificadores.
	def t_id(self,t):
		r'[a-zA-Z][a-zA-Z_0-9]*'
		t.type = self.reserved.get(t.value,'id') 
		return t

	# Los newline (saltos de linea).
	def t_newline(self,t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	# Los caracteres inesperados, los cuales no se encuentran en el lenguaje.
	def t_error(self,t):
		self.list_error.append(t)
		t.lexer.skip(1)


	def t_comment(self,t):
		r'\#[^\n]*'
		t.type = self.reserved.get(t.value,'comment')
		pass

	#
	# Funcion que maneja una cadena de caracteres.
	#
	def t_string(self,t):
		r'\"([^\\\n]|(\\.))*?\"'
		valor = t.value[1:len(t.value)-1]
		t.value = valor.replace('\\"','"')
		t.type = self.reserved.get(t.value,'string')
		return t

	#
	# Funcion que calcula el numero de columna en el que se encuentra un token.
	#
	def column_token(self,input,token):
		last = input.rfind('\n',0,token.lexpos)
		if (last < 0):
			last = 1
			column = 1
		else:
			column = (token.lexpos - last)
		return column

	#
    # Constructor del lexer
    #
	def build(self,**kwargs):
		self.lexer = lex.lex(module=self,**kwargs)


	# Simulador del analizador lexicografico de setlan.
	def scanner(self,files):
		# Lista para guardar los tokens que encuentre
		tokens_found = []	
	
		try:

			# Abrir el archivo de texto
			archivo = open(files)

			
			# Leer el archivo
			data = archivo.read()

			self.lexer.input(data)

			# Obtener y guardar los tokens
			while True:
			    tok = self.lexer.token()
			    if not tok: break
			    # Se agrego el token a la lista 
			    tokens_found.append(tok)

			archivo.close()

		except IOError:
			# Si no se pudo encontrar el archivo

			print 'ERROR: No se pudo abrir el archivo de texto \"%s\"' % archivo_texto
			exit()

		# Encontrar e imprimir errores lexicos. 
		if (len(self.list_error) == 0):

			for i in tokens_found:
				if (i.type == 'string'):
					s1 = '(Linea: %d, Columna: %d) %s:("%s")'
					print s1 % (i.lineno,self.column_token(data,i),i.type,i.value)
				elif (i.type == 'id'):
					s2 = "(Linea: %d, Columna: %d) %s:%s"
					print s2 % (i.lineno,self.column_token(data,i),i.type,i.value)

				elif (i.type == 'number'):
					s3 = "(Linea: %d, Columna: %d) %s: %d"
					print s3 % (i.lineno,self.column_token(data,i),i.type,i.value)
				else:
					s4 = "(Linea: %d, Columna: %d) %s (%s)"
					print s4 % (i.lineno,self.column_token(data,i),i.type,i.value)

			# Si no encuentra errores devuelve el valor cero
			return 0

		else:

			for error in self.list_error:
				er = "ERROR: Caracter inesperado \"%s\" (Linea: %d, Columna: %d)"
				print er % (error.value[0],error.lineno,self.column_token(data,error))
			
			# Si encuentra un error devuelve el valor 1				
			return 1

# END lexer.py
