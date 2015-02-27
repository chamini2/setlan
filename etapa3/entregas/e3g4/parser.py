#!/usr/bin/python
#encoding: utf-8

#############################################################################
## 							   Proyecto traductores e Interpretadores  							   ##
##															    SETLAN												  		   ##
#############################################################################
#																																						#
#														---(Tercera Entrega)---									 				#
#														 ANALIZADOR SINTÁCTICO													#
#																		Parser																	#
#Integrantes:																																#
#		Nelson Saturno 09-10797																		 							#
#		Neylin Belisario 09-10093																	 							#
#												 																										#
#############################################################################

import sys
import lexer
import clases as Clase
import yacc

#inicio del programa
start = ""

# Gramatica para PROGRAM
def p_Program(p):
	'''Programa : Program Cuerpo'''
	p[0] = Clase.Program(p[2])


# Gramatica para los epsilon
def p_Epsilon(p):
	'''epsilon : '''
	pass


#Gramatica para los booleanos 
def p_Boolean(p):
	'''Boolean : False
			   		 | True'''
	p[0] = Clase.Boolean(p[1])


# Gramatica para los identificadores
def p_ID(p):
	'''id : ID'''
	p[0] = Clase.Identificador(p[1])


# Gramatica para los Strings
def p_String(p):
	'''Strings : String'''
	p[0] = Clase.String(p[1])


# Gramatica para los numeros
def p_Number(p):
	'''Numeros : Number'''
	p[0] = Clase.Number(p[1])


# Gramatica para los conjuntos
def p_Set(p):
	'''Sets : Llave_Abre ListaNumeros Llave_Cierra'''
	p[0] = Clase.Sets(p[2])


# Gramatica para la asignacion de conjuntos
def p_Asignacion_Conj(p):
	'''Asignacion_Conj : id Equal Llave_Abre Llave_Cierra
										 | id Equal Sets'''

	if len(p) == 5:
		p[4] = None;

	p[0] = Clase.Asignacion_Conj(p[1],p[3])


# Gramatica auxiliar para la lista de numeros
def p_Aux_ListaNumeros(p):
	'''Aux_ListaNumeros : Numeros
											| Expresion'''
	p[0] = p[1]


# Gramatica para la lista de numeros en un conjunto
def p_ListaNumeros(p):
	'''ListaNumeros : Aux_ListaNumeros
									| ListaNumeros Coma Aux_ListaNumeros'''
	if len(p) == 2:
		p[0] = []
		p[0].append(p[1])
	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])


# Gramatica para las asignaciones
def p_Asignacion(p):
	'''Asignacion : id Equal Expresion'''
	p[0] = Clase.Asignacion(p[1],p[3])


# Gramatica para la funcion scan
def p_Scaneo(p):
  '''Scaneo : Scan id'''
  p[0] = Clase.Scan_Entrada(p[2]) 

 
# Gramatica para los prints
def p_PrintLneo(p):
  '''PrintLneo : PrintLn ListaComa'''
  p[0] = Clase.ImprimirLn_Expresion(p[2])
 
 
# Gramatica para los prints
def p_Printeo(p):
  '''Printeo : Print ListaComa'''
  p[0] = Clase.Imprimir_Expresion(p[2])
 

# Gramatica para la separacion de tipos de impresion
def p_TipoImpresion(p): 
  '''TipoImpresion : Strings
                   | Expresion'''
  p[0] = p[1]
 

# Gramatica para lista de impresion
def p_ListaComaRecursive(p): 
  '''ListaComa : TipoImpresion
               | ListaComa Coma TipoImpresion'''
  if len(p) == 2:
      p[0] = []
      p[0].append(p[1])
  elif len(p) == 4:
      p[0] = p[1]
      p[0].append(p[3])


# Gramatica para los tipos de instrucciones que existen
def p_Instruccion_Type(p):
	'''Instruccion_Type : Asignacion
											| Bloque
											| Asignacion_Conj
											| Condicion
										 	| Ciclo_For
										 	| Ciclo_Repeat1
										 	| Ciclo_Repeat2
										 	| Ciclo_Repeat3'''
	p[0] = p[1]


# Gramatica para las instrucciones que no estan en un bloque
def p_Instruccion1(p):
	'''Instruccion1 : Instruccion_Type
									| Printeo
									| PrintLneo
									| Scaneo'''
	p[0] = p[1]


# Gramatica para las Instrucciones base
def p_Instruccion2_Base(p):
	'''Instruccion2_Base : Instruccion_Type Pto_Coma
											 | Printeo Pto_Coma
											 | PrintLneo Pto_Coma
											 | Scaneo Pto_Coma
											 | Ciclo_Repeat3 Pto_Coma
											 | Ciclo_Repeat1 Pto_Coma'''
	p[0] = p[1]


# Gramatica para las instrucciones que estan dentro de un bloque
def p_Instruccion2(p):
	'''Instruccion2 : Instruccion2_Base
									| Instruccion2 Instruccion2_Base'''
	if len(p) == 2:
		p[0] = []
		p[0].append(p[1])
	elif len(p) == 3:
		p[0] = p[1]
		p[0].append(p[2])


# Gramatica para la lista de variables
def p_ListaVariables(p):
	'''ListaVariables : Aux_ListaVariables
										| ListaVariables Coma Aux_ListaVariables'''
	if len(p) == 2:
		p[0] = []
		p[0].append(p[1])
	elif len(p) == 4:
		p[0] = p[1]
		p[0].append(p[3])


#Gramatica Auxiliar para la lista de variables
def p_Aux_ListaVariables(p):
	'''Aux_ListaVariables : id'''
	p[0] = p[1]


# Gramatica para la declaracion de variables Base
def p_Lista_Declaracion_Base(p):
	'''Lista_Declaracion_Base : Type ListaVariables Pto_Coma
														| Type id Equal Expresion Pto_Coma'''
	if len(p) == 4:
		p[0] = Clase.Lista_Declaracion_Base(p[1],p[2])
	else:
		p[0] = Clase.Lista_Declaracion_Base(p[1],p[2],p[4])


# Gramatica para la declaracion de variables con tipo
def p_Lista_Declaracion(p):
	'''Lista_Declaracion : Lista_Declaracion_Base
											 | Lista_Declaracion Lista_Declaracion_Base '''
	if len(p) == 2:
		p[0] = []
		p[0].append(p[1])
	elif len(p) == 3:
		p[0] = p[1]
		p[0].append(p[2])


# Gramatica para las declaraciones
def p_Declaracion(p):
	'''Declaracion : Using Lista_Declaracion In
								 | Using In
								 | epsilon'''
	if len(p) == 4:
		p[0] = Clase.Declaracion(p[2])


# Gramatica para los tipos
def p_Type(p):
	'''Type : Set
					| Bool
					| Int'''
	p[0] = p[1]


# Gramatica para los bloques
def p_Bloque(p):
	'''Bloque : Llave_Abre Declaracion Llave_Cierra
						| Llave_Abre Declaracion Instruccion2 Llave_Cierra'''
	if len(p) == 5:	
		p[0] = Clase.Bloque(p[2],p[3])
	else: 
		p[0] = Clase.Bloque(p[2],None)



# Gramatica para cuerpo de if y ciclos
def p_Cuerpo(p):
	'''Cuerpo : Instruccion1
						| Bloque'''
	p[0] = p[1]


# Gramatica para el IF
def p_Condicion(p):
	'''Condicion : If Par_Abre Expresion Par_Cierra Cuerpo
							 | If Par_Abre Expresion Par_Cierra Cuerpo Condicion_Else_If'''
	if len(p) == 6:
		p[0] = Clase.Condicion(p[5],p[3])
	elif len(p) == 7:
		p[0] = Clase.Condicion(p[5],p[3],p[6])


# Gramatica para el ELSE
def p_Condicion_Else(p):
	'''Condicion_Else : Else Cuerpo'''
	if len(p) == 3:
		p[0] = Clase.Condicion(p[2])
	elif len(p) == 2: 
		p[0] = Clase.Condicion(p[1])


# Gramatica para el ELSE IF
def p_Condicion_Else_If(p):
	'''Condicion_Else_If : ElseIf Par_Abre Expresion Par_Cierra Cuerpo
											 | ElseIf Par_Abre Expresion Par_Cierra Cuerpo Condicion_Else_If
											 | Condicion_Else'''
	if len(p) == 7:
		p[0] = Clase.Condicion(p[5],p[3],p[6])
	elif len(p) == 6:
		p[0] = Clase.Condicion(p[5],p[3])
	elif len(p) == 2:
		p[0] = p[1]


def p_Ciclo_For(p):
	'''Ciclo_For : For id Direccion id Do Cuerpo
							 | For id Direccion Expresion Do Cuerpo
							 | For id Direccion Llave_Abre ListaNumeros Llave_Cierra Do Cuerpo'''
	if len(p) == 7:
		p[0] = Clase.Expre_For(p[2],p[3],p[4],p[6])
	else:
		p[0] = Clase.Expre_For(p[2],p[3],p[5],p[8])


def p_Direccion(p):
	'''Direccion : Min
							 | Max'''
	p[0] = p[1]


def p_Ciclo_Repeat1(p):
	'''Ciclo_Repeat1 : Repeat Instruccion1 While Par_Abre Expresion Par_Cierra Do Instruccion1'''
	p[0] = Clase.Expre_Repeat1(p[2],p[5],p[8])
	


def p_Ciclo_Repeat2(p):
	'''Ciclo_Repeat2 : While Par_Abre Expresion Par_Cierra Do Bloque'''
	p[0] = Clase.Expre_Repeat2(p[3],p[5])



def p_Ciclo_Repeat3(p):
	'''Ciclo_Repeat3 : Repeat Bloque While Par_Abre Expresion Par_Cierra'''
	p[0] = Clase.Expre_Repeat3(p[2],p[5])


# Gramatica para los tipos de expresiones
def p_Expresion(p):
	'''Expresion : Boolean
							 | Numeros
							 | id
							 | Sets
							 | Llave_Abre Llave_Cierra'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		if len(p) == 3:
			p[2] = None
		#p[0] = Clase.Expre_Conjunto(p[2])


# Gramatica para las expresiones en parentesis
def p_Expresion_Paren(p):
	'''Expresion : Par_Abre Expresion Par_Cierra'''
	p[0] = p[2]


# Gramatica para el not 
def p_Expresion_Unaria(p):
	'''Expresion : Not Expresion
							 | Resta Expresion
							 | MaxConj Expresion
							 | MinConj Expresion
							 | NumElemConj Expresion'''
	p[0] = Clase.Exp_Unaria(p[1],p[2])


# Gramatica para los operadores binarios 
def p_Expresion_Binaria(p):
	'''Expresion : Expresion Suma Expresion
							 | Expresion Resta Expresion
							 | Expresion Mult Expresion
							 | Expresion Div Expresion
							 | Expresion Mod Expresion
							 | Expresion Union Expresion
							 | Expresion Dif Expresion
							 | Expresion Inter Expresion
							 | Expresion SumaConj Expresion
							 | Expresion Or Expresion
							 | Expresion And Expresion							 
							 | Expresion RestaConj Expresion
							 | Expresion MultConj Expresion
							 | Expresion DivConj Expresion
							 | Expresion ModConj Expresion
							 | Expresion Equiv Expresion
							 | Expresion Greater Expresion
							 | Expresion Less Expresion
							 | Expresion GreaterEqual Expresion
							 | Expresion LessEqual Expresion
							 | Expresion IsInConj Expresion
							 | Expresion NotEquiv Expresion'''
	p[0] = Clase.Exp_Binaria(p[1],p[2],p[3])


# Error
def p_error(p):
	if p is not None:
	        print "Syntax error at line " + str(p.lineno) +  " Unexpected token  " + str(p.value)
	        sys.exit(1)
	else:
	        sys.exit(1)


precedence = (

	("left",'Or'),
	("left",'And'),
	("right",'Not'),

	("left",'Equiv','NotEquiv'),	
	("nonassoc",'Greater','GreaterEqual','Less','LessEqual'),
	("nonassoc",'IsInConj'),
							 	
	("left",'Suma','Resta'),
	("left",'Mult','Div','Mod'),

	("left",'Union','Dif'),
	("left",'Inter'),

	("left",'SumaConj','RestaConj'),
	("left",'MultConj','DivConj','ModConj'),

	("right",'MaxConj','MinConj','NumElemConj'),		
)


def AnalizadorParser(Archivo):

	try:


		tokens = lexer.tokens
		#tokensEncontrados = Lexer.AnalizadorLex(ArchivoTrinitytxt)

		#Se abre el archivo 
		ArchivoSetlan = open(Archivo, 'r')
		
		global data

		#Se guarda en data lo que se encuentra en el ArchivoTrinity
		data = ArchivoSetlan.read()

		# Construimos el parser
		parser = yacc.yacc()

		parser.parse(data)

		#Se cierra el archivo
		ArchivoSetlan.close()

		return 0

	except IOError:

		print "ERROR: No se pudo abrir el ArchivoSetlan %s" % Archivo
		exit()	

