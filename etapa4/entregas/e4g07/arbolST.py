#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 05/02/2015
Ult. Modificacion el 08/03/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''


# Importaciones necesarias
from tablaSimbolos import *
from lexer         import find_column
from functions     import *

# Errores de Tipo
type_error_list = []

# Empila una nueva tabla de simbolos
def empilar(objeto, alcance):
    if isinstance(objeto, Block):
        objeto.alcance.parent = alcance
        alcance.children.append(objeto.alcance)
    else:
        objeto.alcance = alcance

# Devuelve una tupla (linea, columna) en un string imprimible
def locationToString(location):
    string = '(Línea {0}, Columna {1}).'.format(location[0], location[1])
    return string

# Clase Expression.
class Expression:
    pass

#Siempre es el primer elemento de un codigo setlan. 
class Program(Expression):

    def __init__(self, statement):
        self.type      = "PROGRAM"
        self.statement = statement
        self.alcance   = tablaSimbolos()

    def printTree(self, level):
        printValueIdented(self.type, level)
        self.statement.printTree(level+1)

    def symbolcheck(self):
        empilar(self.statement, self.alcance)
        if self.statement.symbolcheck():
            return self.alcance

    def evaluate(self):
        self.statement.evaluate()

#Clase para la asignacion de expresiones
class Assign(Expression):

    def __init__(self, leftIdent, rightExp, location):
        self.type      = "ASSIGN"
        self.leftIdent = leftIdent
        self.rightExp  = rightExp
        self.location  = location
        self.alcance   = tablaSimbolos()

    def printTree(self,level):
        printValueIdented(self.type, level)
        #Impresion del identificador asignado
        printValueIdented("IDENTIFIER", level + 1)
        self.leftIdent.printTree(level + 2)
        #Impresion de la expresion asignada
        printValueIdented("VALUE", level + 1)
        self.rightExp.printTree(level + 2)

    def symbolcheck(self):
        empilar(self.rightExp, self.alcance)
        empilar(self.leftIdent, self.alcance)
    
        #Buscamos los tipos
        RightExpType  = self.rightExp.symbolcheck()
        LeftIdentType = self.leftIdent.symbolcheck()

        if LeftIdentType and RightExpType:
            #Verificamos que la asignacion cumpla el tipo del identificador
            if LeftIdentType != RightExpType: 
                mensaje  = "ERROR: No se puede asignar '" + RightExpType \
                           + "' a Variable '" + str(self.leftIdent) + "' de tipo '"\
                           + str(LeftIdentType) + "' "\
                           + locationToString(self.location)
                type_error_list.append(mensaje)

        if LeftIdentType:
            identifier = self.alcance.buscar(self.leftIdent.identifier)
            if not identifier.modifiable:
                mensaje = "ERROR: No se puede modificar " + str(self.leftIdent)\
                          + locationToString(self.location)
                type_error_list.append(mensaje)

    def evaluate(self):
        #Evaluamos las expresiones
        Identifier = str(self.leftIdent)
        result     = self.rightExp.evaluate()
        
        identifier = self.alcance.buscar(Identifier)
        #Actualizamos 
        if identifier.modifiable:
            self.alcance.update(Identifier,result)

# Clase para la impresion por consola
class Print(Expression):
 
    def __init__(self, printType, elements, location):
        self.type     = printType
        self.elements = elements
        self.location = location
        self.alcance  = tablaSimbolos()
 
    def printTree(self, level):
        printValueIdented(self.type,level)
        for element in self.elements:
            element.printTree(level + 1)

    def symbolcheck(self):
        acceptedTypes = ['string','int','bool','set']
        for element in self.elements:
            empilar(element, self.alcance)
            elemtype = element.symbolcheck()
    
            #Verificamos que se impriman expresiones de tipos permitidos
            if not elemtype in acceptedTypes:
                mensaje =  "ERROR: No se puede imprimir '"\
                           + str(elemtype) + "' "\
                           + locationToString(self.location)
                type_error_list.append(mensaje)

    def evaluate(self):
        for element in self.elements:
            print(element.evaluate()),
        if self.type == "PRINTLN":
            print

# Clase para la entrada de datos
class Scan(Expression):
    
    def __init__(self, identifier, location):
        self.type     = 'SCAN'
        self.value    = identifier
        self.location = location

    def printTree(self,level):
        printValueIdented(self.type,level)
        self.value.printTree(level + 1)

    def symbolcheck(self):
        acceptedTypes = ['int','bool']
        empilar(self.value, self.alcance)
        valueType = self.value.symbolcheck()

        #Verificamos que se admita el tipo permitido
        if not valueType in acceptedTypes:
            mensaje = "ERROR: scan no admite valores de tipo '"\
                      + valueType + "' "\
                      + locationToString(self.location)   
            type_error_list.append(mensaje) 

    def evaluate(self):
        #Buscamos la variable donde se almacenara el valor de entrada
        simbol  = self.alcance.buscar(self.value.identifier)

        if simbol:
            #Verificamos la accion a realizar segun el tipo
            if simbol.type == 'int':
                ejecutar = True                
                while ejecutar:
                    entrada    = raw_input()

                    #Verificamos si la entrada es un numero
                    for i in range(0,len(entrada)):
                        esNumero = entrada[i] in '-0123456789'
                        if not esNumero:
                            esNumero = False
                            break
                    if esNumero:
                        entrada = int(entrada)  

                    #Actualizamos el valor         
                    if isinstance(entrada, int) and simbol.modifiable == True:
                        self.alcance.update(self.value.identifier,entrada)
                        ejecutar = False
                    else:
                        ejecutar = True
            elif simbol.type == 'bool':
                ejecutar = True                
                while ejecutar:
                    entrada = raw_input()
                    if entrada in ['false','true'] and simbol.modifiable == True:
                        self.alcance.update(self.value.identifier,entrada)
                        ejecutar = False
                    else:
                        ejecutar = True

#Un bloque es una secuencia de Expresiones
class Block(Expression):
  
    def __init__(self, list_inst, declaraciones = None):
        self.type          = "BLOCK"
        self.list_inst     = list_inst
        self.declaraciones = declaraciones
        self.alcance       = tablaSimbolos()
  
    def printTree(self,level):
        printValueIdented(self.type,level)
        
        #Imprimimos la lista de declaraciones, si existe
        if self.declaraciones:
            self.declaraciones.printTree(level+1)
        #Imprimimos toda la lista de instrucciones
        if self.list_inst:
            for inst in self.list_inst:
                inst.printTree(level + 1)
      
        printValueIdented("BLOCK_END", level)

    def symbolcheck(self):
        if self.declaraciones:
            empilar(self.declaraciones, self.alcance)
            self.declaraciones.symbolcheck()
        if self.list_inst:
            for inst in self.list_inst:
                empilar(inst, self.alcance)
                inst.symbolcheck()
        return True

    def evaluate(self):
        for inst in self.list_inst:
            inst.evaluate()
 
#Clase para las declaraciones
class Using(Expression):
 
    def __init__(self, list_declare):
        self.type         = "USING"
        self.list_declare = list_declare
        self.alcance      = tablaSimbolos()
 
    def printTree(self,level):
        printValueIdented(self.type, level)
        #Se imprimen todas las declaraciones
        for declaration in self.list_declare:
            declaration.printTree(level)
        printValueIdented("IN", level)

    def symbolcheck(self):
        for declaration in self.list_declare:
            empilar(declaration, self.alcance)
            declaration.symbolcheck()

#Clase para los elementos de una declaracion.
class Declaration(Expression):
 
    def __init__(self, decType, list_id):
        self.type    = decType
        self.list_id = list_id
        self.alcance = tablaSimbolos()
 
    def printTree(self, level):
        self.type.printTree(level)
        for identifier in self.list_id:
            printValueIdented(identifier, level + 2)

    def symbolcheck(self):
        for var in self.list_id:
            self.alcance.insert(var, self.type.type)

    # La declaracion de variables no se evalua
    def evaluate(self):
        pass

#Clase para los condicionales
class If(Expression):   
    
    def __init__(self,condition,inst_if,location, inst_else = None):
        self.type      = 'IF'
        self.condition = condition
        self.inst_if   = inst_if
        self.location  = location
        self.inst_else = inst_else 

    def printTree(self,level):
        printValueIdented(self.type,level)
        printValueIdented("condition",level + 1)
        self.condition.printTree(level + 2)
        printValueIdented('THEN',level + 1)
        self.inst_if.printTree(level + 2)

        if self.inst_else is not None:
            printValueIdented('ELSE',level)
            self.inst_else.printTree(level +1)
        printValueIdented('END_IF',level)

    def symbolcheck(self):
        empilar(self.condition, self.alcance)
        
        conditionType = self.condition.symbolcheck()

        if self.inst_else:
            empilar(self.inst_else, self.alcance)
            inst_else_Type = self.inst_else.symbolcheck()

        if conditionType != 'bool':
            mensaje  = "ERROR: La condicion del IF debe ser tipo 'bool'"
            mensaje += locationToString(self.location)
            type_error_list.append(mensaje) 

    def evaluate(self):
        condition = self.condition.evaluate()
        if condition:
            self.inst_if.evaluate()
        elif self.inst_else:
            self.inst_else.evaluate()

#Clase para el ciclo for
class For(Expression):
    
    def __init__(self,identifier,direction,expre,inst, location):
        self.type       = 'FOR'
        self.identifier = identifier
        self.direction  = direction
        self.expre      = expre
        self.inst       = inst
        self.location   = location

    def printTree(self,level):
        printValueIdented(self.type,level)
        self.identifier.printTree(level + 1)
        self.direction.printTree(level + 1)
        printValueIdented('IN',level + 1)
        self.expre.printTree(level + 1)
        printValueIdented('DO',level + 1)
        self.inst.printTree(level + 2)
        printValueIdented('END_FOR',level)

    def symbolcheck(self):
        #Creamos la tabla para el alcance local del for        
        alcanceFor = tablaSimbolos()
        alcanceFor.parent = self.alcance
        alcanceFor.insert(str(self.identifier), 'int', False)
        self.alcance.children.append(alcanceFor)
        self.alcance = alcanceFor
        
        empilar(self.expre, self.alcance)
        empilar(self.identifier, self.alcance)
        self.inst.alcance = self.alcance

        self.identifier.symbolcheck()
        #Tipo de la expresion del for
        expreType = self.expre.symbolcheck()
        #Tipo de la direccion
        dirType   = self.direction.symbolcheck()

        if dirType != 'min' and dirType != 'max':
            mensaje = "ERROR: La direccion del for"\
                      + " debe ser 'max' o 'min' "\
                      + locationToString(self.location)   
            type_error_list.append(mensaje)
        if expreType != 'set':
            mensaje = "ERROR: La expresion del for"\
                      + " debe ser de tipo 'set' "\
                      + locationToString(self.location)   
            type_error_list.append(mensaje)

        self.inst.symbolcheck() 

    def evaluate(self):
        # Obtenemos los elementos del conjunto a iterar
        elements = setAListaDeEnteros(self.expre.evaluate())

        # Si el conjunto es vacio
        if elements == []:
            string  = "ERROR: No se puede iterar sobre el conjunto vacio "
            string += locationToString(self.location)
            print(string)
            exit()

        #Verificamos el orden del recorrido del conjunto
        if self.direction.evaluate() == 'min':   #Recorrido ascendente
            while elements != []:
                ubication = elements.index(min(elements)) 
                value     = elements.pop(ubication)
                self.alcance.update(str(self.identifier),value)
                #Evaluamos las instrucciones
                self.inst.evaluate()
        elif self.direction.evaluate() == 'max': #Recorrido descendente
            while elements != []:
                ubication = elements.index(max(elements)) 
                value     = elements.pop(ubication)
                self.alcance.update(str(self.identifier),value)
                #Evaluamos las instrucciones
                self.inst.evaluate()  

#Clase para la direccion de recorrido del conjunto del for 
class Direction(Expression):
    
    def __init__(self,value):
        self.type  = 'direction'
        self.value = value

    def printTree(self,level):
        printValueIdented(self.type, level)
        printValueIdented(self.value,level + 1)

    def symbolcheck(self):
        return self.value

    def evaluate(self):
        return self.value

#Clase para el ciclo repat-while-do
class RepeatWhileDo(Expression):
    
    def __init__(self,inst1,expre,inst2,location):
        self.type  = 'REPEAT'
        self.inst1 = inst1
        self.expre = expre
        self.inst2 = inst2
        self.location = location

    def printTree(self,level):
        printValueIdented(self.type,level)
        self.inst1.printTree(level + 1)
        printValueIdented('WHILE',level)
        printValueIdented('condition', level + 1)
        self.expre.printTree(level + 2)
        printValueIdented('DO',level)
        self.inst2.printTree(level + 1)

    def symbolcheck(self):
        
        empilar(self.inst1, self.alcance)
        empilar(self.expre, self.alcance)
        empilar(self.inst2, self.alcance)

        expreType = self.expre.symbolcheck()
        #Verificamos que la condicion sea booleana
        if expreType != 'bool':
            mensaje = "ERROR: La condicion del while debe ser de tipo 'bool'."
            mensaje += locationToString(self.location)            
            type_error_list.append(mensaje)  

        self.inst1.symbolcheck()
        self.inst2.symbolcheck()

    def evaluate(self):
        ejecutar = True
        while ejecutar:
            self.inst1.evaluate()
            if self.expre.evaluate(): #Verificamos que se cumpla la condicion
                self.inst2.evaluate()  
            else:
                ejecutar = False
    

#Clase para los ciclos while condicion do
class WhileDo(Expression):
    
    def __init__(self,expre,inst, location):
        self.type  = 'WHILE'
        self.expre = expre
        self.inst  = inst
        self.location = location
    
    def printTree(self, level):
        printValueIdented(self.type,level)
        printValueIdented('condition',level + 1)
        self.expre.printTree(level + 2)
        printValueIdented('DO',level)
        self.inst.printTree(level + 1)
        printValueIdented('END_WHILE',level)

    def symbolcheck(self):
        
        empilar(self.expre, self.alcance)
        empilar(self.inst, self.alcance)

        expreType = self.expre.symbolcheck()
        #Verificamos que la condicion sea booleana
        if expreType != 'bool':
            mensaje  = "ERROR: La condicion del while debe ser de tipo 'bool'."
            mensaje += locationToString(self.location)
            type_error_list.append(mensaje) 

        self.inst.symbolcheck()

    def evaluate(self):
        while self.expre.evaluate():
            self.inst.evaluate()

            
#Clase para los ciclos repeat instruccion while condicion do
class RepeatWhile(Expression):
    
    def __init__(self,inst,expre, location):
        self.type  = 'REPEAT'
        self.inst  = inst
        self.expre = expre
        self.location = location 
        
    def printTree(self,level):
        printValueIdented(self.type,level)
        self.inst.printTree(level + 1)
        printValueIdented('condition',level + 1)
        self.expre.printTree(level + 2) 

    def symbolcheck(self):

        empilar(self.inst, self.alcance)
        empilar(self.expre, self.alcance)

        expreType = self.expre.symbolcheck()
        #Verificamos que la condicion sea booleana
        if expreType != 'bool':
            mensaje  = "ERROR: La condicion del while debe ser de tipo 'bool'."
            mensaje += locationToString(self.location)
            type_error_list.append(mensaje)

        self.inst.symbolcheck() 

    def evaluate(self):
        self.inst.evaluate()
        while self.expre.evaluate():
            self.inst.evaluate()

#Clase para los numeros enteros
class Number(Expression):
    
    def __init__(self, number):
        self.type   = "int"
        self.number = number

    # Para poder ser imprimido por la instruccion print
    def __str__(self):
        return str(self.number)

    def printTree(self, level):
        printValueIdented(self.type, level)
        printValueIdented(self.number, level + 1)

    def symbolcheck(self):
        return 'int'

    def evaluate(self):
        return int(self.number)

# Clase para definir un string o cadena de caracteres.
class String(Expression):

    def __init__(self, string):
        self.type   = "STRING"
        self.string = string

    def __str__(self):
        textOnly = self.string[1:]
        textOnly = textOnly[:-1]
        return textOnly

    def printTree(self, level):
        printValueIdented(self.type, level)
        printValueIdented(self.string, level + 1)

    def symbolcheck(self):
        return 'string'

    def evaluate(self):
        return str(self)

# Clase para definir un identificador o variable.
class Identifier(Expression):

    def __init__(self, identifier, location):
        self.type       = "VARIABLE"
        self.identifier = identifier
        self.location   = location
        self.alcance    = tablaSimbolos()

    def __str__(self):
        return self.identifier

    def printTree(self, level):
        printValueIdented(self.type, level)
        printValueIdented(self.identifier, level + 1)

    def symbolcheck(self): 

        if self.alcance.globalContains(str(self.identifier)):
            identifier = self.alcance.buscar(self.identifier)
            return identifier.type
        else:
            mensaje =   "ERROR: Variable '" + str(self.identifier)\
                      + "' es asignada antes de ser declarada " \
                      + locationToString(self.location)
            if not mensaje in type_error_list: 
                type_error_list.append(mensaje)
            return str(self.identifier)

    def evaluate(self):
        return self.alcance.buscar(self.identifier).value

# Clase para definir una expresion booleana.
class Bool(Expression):
    
    def __init__(self, value):
        self.type  = 'bool'
        self.value = value

    def __str__(self):
        return str(self.value)

    def printTree(self,level):
        printValueIdented(self.type, level)
        printValueIdented(self.value, level + 1)

    def symbolcheck(self):
        return 'bool'

    def evaluate(self):
        return str(self.value)

#Clase para la parentizacion
class Parenthesis(Expression):
    
    def __init__(self, exp):
        self.type = 'PARENTHESIS'
        self.exp  = exp
        self.alcance = tablaSimbolos()

    def printTree(self,level):
        printValueIdented(self.type, level)
        self.exp.printTree(level + 1)

    def symbolcheck(self):
        empilar(self.exp, self.alcance)
        return self.exp.symbolcheck()

    def evaluate(self):
        return self.exp.evaluate()

# Clase para definir un Conjunto.
class Set(Expression):
 
    def __init__(self,list_expr, location):
        self.type = 'SET'
        self.list_expr = list_expr
        self.location  = location
        self.alcance   = tablaSimbolos()
 
    # Para poder ser imprimido por la instruccion print
    def __str__(self):
        return listaDeEnterosASet(self.list_expr)

    def printTree(self,level):
        printValueIdented(self.type, level)
        if self.list_expr:
            for expr in self.list_expr:
                expr.printTree(level + 1)

    def symbolcheck(self):
        if self.list_expr:
            # Un set solo puede contener numeros
            type_set = 'int'
            for exp in self.list_expr:
                empilar(exp, self.alcance)
                if type_set != exp.symbolcheck():
                    mensaje = "ERROR: 'set' esperaba un numero entero pero se encontro Variable '" \
                             + exp.symbolcheck() + "' "\
                             + locationToString(self.location)
                    type_error_list.append(mensaje)
                    return exp.symbolcheck()
            return 'set'

    def evaluate(self):
        listaEnteros = []
        if not self.list_expr:
            return listaDeEnterosASet(listaEnteros)

        for exp in self.list_expr:
            listaEnteros.append(exp.evaluate())
        return listaDeEnterosASet(listaEnteros)

# Clase para definir los tipos.
class Type(Expression):

    def __init__(self, typeName):
        self.type = typeName
 
    def printTree(self,level):
        printValueIdented(self.type, level + 1)

#Classe para los Operadores Binarios
class BinaryOperator(Expression):

    global binaryOperatorTypeTuples, evalBinaryFunctions
    binaryOperatorTypeTuples = {
            ('int', 'TIMES', 'int'): 'int',
            ('int', 'PLUS', 'int'): 'int',
            ('int', 'MINUS', 'int'): 'int',
            ('int', 'DIVIDE', 'int'): 'int',
            ('int', 'MODULE', 'int'): 'int',
            ('set', 'UNION', 'set'): 'set',
            ('set', 'DIFERENCE','set'): 'set',
            ('set', 'INTERSECTION','set'):'set',
            ('int', 'PLUSMAP', 'set'): 'set',
            ('int', 'MINUSMAP', 'set'): 'set',
            ('int', 'TIMESMAP', 'set'): 'set',
            ('int', 'DIVIDEMAP','set'): 'set',
            ('int', 'MODULEMAP', 'set'): 'set',
            ('bool', 'OR', 'bool'): 'bool',
            ('bool', 'AND', 'bool'): 'bool',
            ('int', 'LESS','int'): 'bool',
            ('int', 'GREAT', 'int'): 'bool',
            ('int', 'LESSEQ', 'int'): 'bool',
            ('int', 'GREATEQ', 'int'): 'bool',
            ('int', 'EQUAL', 'int'): 'bool',
            ('bool', 'EQUAL', 'bool'): 'bool',
            ('int', 'UNEQUAL', 'int'): 'bool',
            ('set', 'EQUAL', 'set'): 'set',
            ('bool', 'UNEQUAL', 'bool'): 'bool',
            ('set', 'UNEQUAL', 'set'): 'bool',
            ('int', 'CONTAINMENT', 'set'): 'bool'
        }

    evalBinaryFunctions = {
        # Aritmeticos
        'PLUS'  : suma,
        'MINUS' : resta,
        'TIMES' : multiplicacion,
        'DIVIDE': division,
        'MODULE': modulo,
        # Aritmetico-Logicos
        'LESS'  : menor,
        'GREAT': mayor,
        'LESSEQ': menorIgual,
        'GREATEQ': mayorIgual,
        'UNEQUAL': desigual,
        'EQUAL'  : igual,
        # Logicos
        'AND'   : logicAnd,
        'OR'    : logicOr,
        # Naturales Sobre Conjuntos
        'CONTAINMENT' : contiene,
        'UNION' : union,
        'INTERSECTION': interseccion,
        'DIFERENCE'   : diferencia,
        # Mapeo sobre conjuntos
        'PLUSMAP'  : mapeoSuma,
        'MINUSMAP' : mapeoResta,
        'TIMESMAP' : mapeoMultiplicacion,
        'DIVIDEMAP': mapeoDivision,
        'MODULEMAP': mapeoModulo
    }
 
    def __init__(self, leftExp, operator, rightExp, location):
        self.leftExp  = leftExp
        self.operator = Operator(operator)
        self.rightExp = rightExp
        self.location = location
        self.alcance  = tablaSimbolos()
 
    def printTree(self, level):
        self.operator.printTree(level)
        self.leftExp.printTree(level + 1)
        self.rightExp.printTree(level + 1)

    def symbolcheck(self):
        #Pasamos la tabla de simbolos
        empilar(self.leftExp, self.alcance)
        empilar(self.rightExp, self.alcance)
        #Verificamos los tipos de cada operando
        leftExpType     = self.leftExp.symbolcheck()
        rightExpType   = self.rightExp.symbolcheck()
        operatorName   = self.operator.symbolcheck()

        newTuple = (leftExpType, operatorName, rightExpType)
        if newTuple in binaryOperatorTypeTuples:
            return binaryOperatorTypeTuples[newTuple]
        else:
            mensaje = "ERROR: No se puede aplicar '" + operatorName\
                      + "' en operandos de tipo '" + leftExpType\
                      + "' y '" + rightExpType + "'."\
                      + locationToString(self.location)
            type_error_list.append(mensaje)
            return False

    def evaluate(self):
        operatorName   = self.operator.symbolcheck()
        # Evaluamos ambos lados del operando
        rigtOp         = self.rightExp.evaluate()
        leftOp         = self.leftExp.evaluate()

        # Aplicamos la operacion indicada y tomamos el resultado.
        try:
            result = evalBinaryFunctions[operatorName](leftOp, rigtOp)
        except Exception as Mensaje:
            string =  Mensaje.args[0] + locationToString(self.location)
            print string
            exit()
        return result

#Clase para los Oeradores Unarios
class UnaryOperator(Expression):

    global unaryOperatorTypeTuples, evalUnaryFunctions
    unaryOperatorTypeTuples = {
        ('MINUS','int') : 'int',
        ('MAXVALUE','set') : 'int',
        ('MINVALUE','set') : 'int',
        ('NUMELEMENTS','set'): 'int',
        ('NOT', 'bool') : 'bool'
    }

    evalUnaryFunctions = {
        'MINUS' : negativo,
        'NOT'   : negar,
        'MINVALUE' : minimo,
        'MAXVALUE' : maximo,
        'NUMELEMENTS': numElementos
    }
    
    def __init__(self,operator,expresion, location):
        self.operator  = Operator(operator)
        self.expresion = expresion
        self.location  = location
        self.alcance   = tablaSimbolos()

    def printTree(self,level):
        self.operator.printTree(level)
        self.expresion.printTree(level + 1)

    def symbolcheck(self):
        empilar(self.expresion, self.alcance)

        #Verificamos los tipos de los operandos.
        operatorName  = self.operator.symbolcheck()
        expresionType = self.expresion.symbolcheck()

        newTuple = (operatorName, expresionType)
        if newTuple in unaryOperatorTypeTuples:
            return unaryOperatorTypeTuples[newTuple]
        else:
            mensaje = "ERROR: No se puede aplicar '" + operatorName\
                      + "' en operando de tipo '" + expresionType + "' "\
                      + locationToString(self.location)
            type_error_list.append(mensaje)
            return False 

    def evaluate(self):
        operatorName   = self.operator.symbolcheck()
        # Evaluamos ambos lados del operando
        expresion     = self.expresion.evaluate()

        # Aplicamos la operacion indicada y tomamos el resultado.
        try:
            result = evalUnaryFunctions[operatorName](expresion)
        except Exception as Mensaje:
            string =  Mensaje.args[0] + locationToString(self.location)
            print string
            exit()
        return result    

# Classe para los operadores:
class Operator(Expression):
 
    #Todos ellos. Sin distincion Binaria/Unaria
    global operator_dicc
    operator_dicc = {
        '*'  :'TIMES',
        '+'  :'PLUS',
        '-'  :'MINUS',
        '/'  :'DIVIDE',
        '%'  :'MODULE',
        '++' :'UNION',
        '\\' :'DIFERENCE',
        '><' :'INTERSECTION',
        '<+>':'PLUSMAP',
        '<->':'MINUSMAP',
        '<*>':'TIMESMAP',
        '</>':'DIVIDEMAP',
        '<%>':'MODULEMAP',
        '>?' :'MAXVALUE',
        '<?' :'MINVALUE',
        '$?' :'NUMELEMENTS',
        'or' :'OR',
        'and':'AND',
        'not':'NOT',        
        '@'  :'CONTAINMENT',
        '<'  :'LESS',
        '>'  :'GREAT',
        '<=' :'LESSEQ',
        '>=' :'GREATEQ',
        '==' :'EQUAL',
        '/=' :'UNEQUAL',        
    }

################################################################################

    def __init__(self,operator):
        self.operator = operator
        self.name     = operator_dicc[operator]

    def __str__(self):
        return self.name
 
    def printTree(self,level):
        printValueIdented(self.name +" "+ self.operator, level)

    def symbolcheck(self):
        return self.name

