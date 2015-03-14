#!/usr/bin/env python
# -*- coding: UTF8 -*-
# ------------------------------------------------------------
# Setlan
#
# AST del lenguaje Setlan
# CI-3725
#
# Gustavo Siñovsky 09-11207
# Luiscarlo Rivera 09-11020
# ------------------------------------------------------------

from settings import *
from table import Table
import sys

class Program:
    def __init__(self, val):
        self.val = val

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = 'PROGRAM\n' + tab + str(self.val.toString(tab,True))
        return palabra

    def verify(self):
        self.val.verify()

    def toStringTable(self, tab, booleano):
        palabra = str(self.val.toStringTable(tab,True))
        return palabra

    def execute(self):
        global ST
        ST = None
        self.val.execute()

class Condicional:
    def __init__(self, condicion, instruccion1, instruccion2, fila, columna):
        self.condicion = condicion
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "CONDICIONAL\n"
        palabra += tab + "condicion: " + str(self.condicion.toString(tab, False)) + "\n"
        palabra += tab + "instruccion 1: " + str(self.instruccion1.toString(tab, False))
        if (self.instruccion2 != None):
            palabra += "\n"+ tab + "instruccion 2: " +  str(self.instruccion2.toString(tab, False))
        return palabra

    def verify(self):
        self.condicion.verify()
        self.instruccion1.verify()
        if (self.instruccion2 != None):
            self.instruccion2.verify()
        if (self.condicion.getType() != "TypeError" and self.condicion.getType() != "bool"):
            global ErrorVer
            ErrorVer = True
            print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": condicion no de tipo \"bool\".")
    
    def toStringTable(self, tab, booleano):
        tab = tab + "\t"
        palabra = tab + str(self.instruccion1.toStringTable(tab, False))
        if (self.instruccion2 != None):
            palabra += "\n"+  str(self.instruccion2.toStringTable(tab, False))
        return palabra  

    def execute(self):
        if self.condicion.eval()=='true':
            self.instruccion1.execute()
        elif self.condicion.eval()=='false' and self.instruccion2!=None:
            self.instruccion2.execute()


class IteracionConjunto:
    def __init__(self,var, direccion, exp, instruccion1, fila, columna):
        self.var = var
        self.direccion = direccion
        self.exp = exp
        self.instruccion1 = instruccion1
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "ITERACION CONJUNTO\n"
        palabra += tab + "variable: " + str(self.var.toString(tab, False)) + "\n"
        palabra += tab + "direccion: " + str(self.direccion.toString(tab, False)) + "\n"
        palabra += tab + "condicion: " + str(self.exp.toString(tab, False)) + "\n"
        palabra += tab + "instruccion 1: " + str(self.instruccion1.toString(tab, False))
        return palabra

    def verify(self):
        global ST
        global ErrorVer
        self.exp.verify()
        if self.exp.getType() != 'set':
            ErrorVer = True
            print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": expresion en iteracion no es de tipo set")

        ST = Table(ST)
        if (not (ST.insertFor(self.var.getValor(), "int"))):
            ErrorVer = True
            print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": variable en iterador ya declarada.")
        if self.exp.getType() != 'set':
            ErrorVer = True
            print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": expresion en iteracion no es de tipo set")
        self.instruccion1.verify()

        ST = ST.getPadre()

    def toStringTable(self, tab, booleano):
        palabra = str(self.instruccion1.toStringTable(tab, False))
        return palabra      

    def execute(self):
        global ST
        ST = Table(ST)
        ST.insertFor(self.var.getValor(), "int")
        conjunto = self.exp.execute()
        if (self.direccion.getValor()=='max'):
            conjunto.reverse()

        for i in conjunto:
            ST.update(self.var.getValor(),i)
            self.instruccion1.execute()
        ST = ST.getPadre()

class IteracionIndeterminada:
    def __init__(self,instruccion1, exp, instruccion2, fila, columna):
        self.instruccion1 = instruccion1
        self.exp = exp
        self.instruccion2 = instruccion2
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "ITERACION INDETERMINADA\n"
        if (self.instruccion1 != None):
            palabra += tab + "REPEAT: " + str(self.instruccion1.toString(tab, False)) + "\n"
        palabra += tab + "condicion: " + str(self.exp.toString(tab, False)) + "\n"
        if (self.instruccion2 != None):
            palabra += tab + "DO: " + str(self.instruccion2.toString(tab, False))
        return palabra

    def verify(self):
        if self.instruccion1 != None:
            self.instruccion1.verify()
        if self.instruccion2 != None:
            self.instruccion2.verify()
        if self.exp != None:
            self.exp.verify()            
        if self.exp.getType() != 'bool':
            global ErrorVer
            ErrorVer = True
            print "Error en fila "+str(self.fila)+", columna "+str(self.columna)+": expresion de iteracion indeterminada debe ser booleana"

    def toStringTable(self, tab, booleano):
        palabra = "\n"
        if (self.instruccion1 != None):
            palabra += str(self.instruccion1.toStringTable(tab, False)) + "\n"
        if (self.instruccion2 != None):
            palabra += str(self.instruccion2.toStringTable(tab, False))

    def execute(self):
        if self.instruccion2 != None and self.instruccion1 != None:
            while True:
                self.instruccion1.execute()
                if self.exp.execute() == 'true':
                    self.instruccion2.execute()
                else:
                    break
        if self.instruccion2 == None:
            while True:
                self.instruccion1.execute()
                if self.exp.execute() == 'true':
                    pass
                else:
                    break
        if self.instruccion1 == None:
            while (self.exp.execute() == 'true'):
                self.instruccion2.execute()


class Bloque:
    def __init__(self, declaraciones, secuencia, fila, columna):
        self.declaraciones = declaraciones
        self.secuencia = secuencia
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano): 
        fin = tab + "FINBLOQUE"
        tab = tab + "\t"
        palabra = "BLOQUE\n"
        if(self.declaraciones == self.secuencia == None):
            return palabra + "\n" + fin
        if self.declaraciones != None:
            palabra += str(self.declaraciones.toString(tab, False)) + "\n"
        if self.secuencia != None:
            palabra += tab + str(self.secuencia.toString(tab, False) + "\n")
        palabra += fin
        return palabra

    def toStringTable(self,tab, booleano):
        fin = tab + "END_SCOPE"
        tab = tab + "\t"
        palabra = "SCOPE\n"
        if(self.declaraciones == self.secuencia == None):
            return palabra + "\n" + fin
        if self.declaraciones != None:
            palabra += str(self.declaraciones.toStringTable(tab, False)) + "\n"
        if self.secuencia != None:
            palabra += tab + str(self.secuencia.toStringTable(tab, False) + "\n")
        palabra += fin
        return palabra

    def verify(self):
        global ST
        global ErrorVer
        ST = Table(ST)
        if (self.declaraciones != None):
            decla = self.declaraciones
            while (decla!=None):
                var = decla.variables
                sig = var.getSecond()
                tipo =  decla.tipo
                while (sig != None):
                    if (not (ST.insert(sig.getValor(), tipo))):
                        ErrorVer = True                        
                        print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": la variable '%s' ya ha sido declarada." % sig.getValor())
                    var = var.getFirst()
                    sig = var.getSecond()
                if (not (ST.insert(var.getFirst().getValor(), tipo))):
                        ErrorVer = True                        
                        print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": la variable '%s' ya ha sido declarada." % var.getFirst().getValor())
                decla = decla.declaraciones
        if (self.secuencia!=None):
            self.secuencia.verify()
        ST = ST.getPadre()

    def execute(self):
        global ST
        ST = Table(ST)
        if (self.declaraciones != None):
            decla = self.declaraciones
            while (decla!=None):
                var = decla.variables
                sig = var.getSecond()
                tipo =  decla.tipo
                while (sig != None):
                    ST.insert(sig.getValor(), tipo)
                    var = var.getFirst()
                    sig = var.getSecond()
                ST.insert(var.getFirst().getValor(), tipo)
                decla = decla.declaraciones
        if (self.secuencia!=None):
            self.secuencia.execute()

        ST = ST.getPadre()


class Declaracion:
    def __init__(self, declaraciones, tipo, variables):
        self.declaraciones = declaraciones
        self.tipo = tipo
        self.variables = variables

    def toString(self, tab, booleano):
        palabra = tab + "USING\n"
        if self.declaraciones != None:
            palabra = tab + str(self.declaraciones.toString(tab, False)) + "\n" 
        tab = tab + "\t"
        palabra += tab + "tipo: " + self.tipo + "\n"
        palabra += tab +"\t" + str(self.variables.toString(tab+"\t", False)) + "\n"
        return palabra

    def getVariables(self):
        return self.variables

    def getType(self, flag=False):
        return self.tipo        

    def toStringTable(self, tab, booleano):
        palabra = tab + "Variable\n"
        if self.declaraciones != None:
            palabra = tab + str(self.declaraciones.toStringTable(tab, False)) + "\n" 
        tab = tab + "\t"
        palabra += tab + "tipo: " + self.tipo + "\n"
        palabra += tab +"\t" + str(self.variables.toStringTable(tab+"\t", False)) + "\n"
        return palabra        

class Variables:
    def __init__(self, variable1, variable2):
        self.variable1 = variable1
        self.variable2 = variable2

    def toString(self, tab, booleano):
        palabra = str(self.variable1.toString(tab, False)) + "\n"
        if self.variable2 != None:
            palabra +=  tab + str(self.variable2.toString(tab, False))
        return palabra

    def getFirst(self):
        return self.variable1

    def getSecond(self):
        return self.variable2

    def toStringTable(self, tab, booleano):
        palabra = str(self.variable1.toStringTable(tab, False)) + "\n"
        if self.variable2 != None:
            palabra += tab + str(self.variable2.toStringTable(tab, False))
        return palabra       

class Secuencia:
    def __init__(self, instruccion1, instruccion2):
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2

    def toString(self, tab, booleano):
        palabra = str(self.instruccion1.toString(tab, False)) + "\n"
        if self.instruccion2 != None:
            palabra +=  tab + str(self.instruccion2.toString(tab, False))
        return palabra

    def verify(self):
        self.instruccion1.verify()
        if self.instruccion2 != None:
            self.instruccion2.verify()      
    
    def toStringTable(self, tab, booleano):
        palabra = str(self.instruccion1.toStringTable(tab, False)) + "\n"
        if self.instruccion2 != None:
            palabra +=  str(self.instruccion2.toStringTable(tab, False))
        return palabra          

    def execute(self):
        self.instruccion1.execute()
        if self.instruccion2 != None:
            self.instruccion2.execute() 

class Asignacion:
    def __init__(self, var, val, fila, columna):
        self.var = var
        self.val = val
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "ASIGNACION\n"
        palabra += tab + "var: " + str(self.var.toString(tab, True, False)) + "\n"
        palabra += tab + "val: " + str(self.val.toString(tab, False))
        return palabra

    def verify(self):
        global ST
        global ErrorVer
        a = ST.lookup(self.var.getValor(), False)
        if (a != None):
            if (a.getReservado()):
                ErrorVer = True
                print("Error en fila "+str(self.var.fila)+", columna "+str(self.var.columna)+": se intenta modificar la variable \"%s\" la cual pertenece a una iteracion." % self.var.getValor())
            else: 
                if (self.val.getType() != "TypeError" and self.var.getType() != self.val.getType()): 
                    ErrorVer = True
                    print "Error en fila "+str(self.var.fila)+", columna "+str(self.var.columna)+": no puede asignar a la variable \'%s\', de tipo \'%s\', una expresión de tipo \'%s\'" % (self.var.getValor(), self.var.getType(), self.val.getType())
        else:
            ErrorVer = True
            print "Error en fila "+str(self.var.fila)+", columna "+str(self.var.columna)+": la variable \'%s\' no ha sido declarada" % self.var.getValor()
        
        self.val.verify()

    def toStringTable(self, tab, booleano):
        return ''       

    def execute(self):
        global ST
        ST.update(self.var.getValor(),self.val.execute())

class Simple:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano, bool2 = True):
        tab = tab + "\t"
        if (self.tipo == 'VARIABLE' or self.tipo == 'CADENA'):
            if (booleano == True and bool2 == True):
                palabra = "elemento: " + str(self.tipo) + "\n"
                if (self.tipo == 'VARIABLE'):
                    palabra += tab + "nombre: " + str(self.valor)
                else:
                    cadena = str(self.valor)
                    cadena = cadena.replace("\\n", " ")
                    cadena = cadena.replace("\\t", "    ")
                    cadena = cadena.replace("\\", "")
                    palabra += tab + "valor: " + cadena
            elif (booleano == True and bool2 == False):
                palabra = str(self.valor)
            elif (self.tipo == 'VARIABLE'):
                palabra = str(self.tipo) + "\n"
                palabra += tab + "nombre: " + str(self.valor)
            elif (self.tipo == 'CADENA'):
                palabra = str(self.tipo) + "\n"
                cadena = str(self.valor)
                cadena = cadena.replace("\\n", " ")
                cadena = cadena.replace("\\t", "    ")
                cadena = cadena.replace("\\", "")
                palabra += tab + "valor: " + cadena 
        else:
            if (booleano == True):
                palabra = "elemento: " + str(self.tipo) + "\n"
            else:
                palabra = str(self.tipo) + "\n"
            palabra += tab + "valor: " + str(self.valor)
        return palabra

    def getValor(self):
        return str(self.valor)

    def getType(self, flag = False):
        if (self.tipo == "LITERAL_NUM"):
            return "int"
        elif (self.tipo == "VARIABLE"):
            global ST
            if (ST.lookup(self.valor, False) == None):            
                return "TypeError" # No encontrado
            else:
                if (not flag):
                    return ST.lookup(self.valor, False).getType()
                else:
                    return "variable"
        elif(self.tipo == "BOOLEANO"):
            return "bool"
        else:
            return "CADENA"    

    def verify(self):
        global ST
        if self.tipo == "LITERAL_NUM":
            if self.valor > 2147483647 or self.valor < -2147483648:
                print "Error en fila "+str(self.fila)+", columna "+str(self.columna)+": overflow"
                exit(0)
        if (self.tipo == "VARIABLE"):
            if (ST.lookup(self.valor, False) == None):
                global ErrorVer
                ErrorVer = True
                print "Error en fila "+str(self.fila)+", columna "+str(self.columna)+": la variable \'%s\' no ha sido declarada" % self.valor
    
    def getVariable(self):
        return self.valor

    def getValor(self):
        return self.valor

    def toStringTable(self, tab, booleano):
        return str(self.valor)        

    def eval(self):
        if (self.tipo == "LITERAL_NUM"):
            return str(self.valor)
        elif (self.tipo == "VARIABLE"):
            global ST
            return imprimirVar(ST.lookup(self.valor, False))
        elif(self.tipo == "BOOLEANO"):
            return str(self.valor)
        elif (self.tipo == 'CADENA'):
            return str(formatString(self.valor[1:-1]))
         #   return self.valor

    def execute(self):
        if (self.tipo == "LITERAL_NUM"):
            return int(self.valor)
        elif (self.tipo == "VARIABLE"):
            global ST
            return ST.lookup(self.valor, False).getValor()
        elif(self.tipo == "BOOLEANO"):
            return str(self.valor)
        elif (self.tipo == 'CADENA'):
            return str(formatString(self.valor[1:-1]))

class Conjunto:
    def __init__(self,val, fila, columna):
        self.val = val
        self.fila = fila
        self.columna = columna

    def toString(self,tab,booleano):
        tab = tab + "\t"
        palabra = "CONJUNTO\n"
        if (self.val == None):
            palabra += tab + 'VACIO'
        else:
            palabra += tab+ str(self.val.toString(tab, False)) 
        return palabra

    def getType(self, flag=False):
        return 'set'

    def verify(self):
        global ErrorVer
        if (self.val != None):
            expresiones = self.val
            while (isinstance(expresiones, Expresiones)):
                exp = expresiones.getSecond()
                exp.verify()
                if(exp.getType()=='TypeError' or exp.getType()!='int'):
                    ErrorVer = True
                    print "Error en fila "+str(self.fila)+", columna "+str(self.columna)+": la expresion \'%s\' dentro del conjunto \'%s\' no es de tipo int" % (str(exp.getValor()), str(self.getValor()))#str(exp.toString("",False))
                expresiones = expresiones.getFirst()
            expresiones.verify()
            if(expresiones.getType()=='TypeError' or expresiones.getType()!='int'):
                    ErrorVer = True
                    print "Error en fila "+str(self.fila)+", columna "+str(self.columna)+": la expresion \'%s\' dentro del conjunto \'%s\' no es de tipo int" % (str(exp.getValor()), str(self.getValor())) #str(expresiones.toString("",False))
    
    def toStringTable(self, tab, booleano):
        return ''

    def getValor(self):
        conjunto = "}"
        if (self.val != None):
            expresiones = self.val
            while (isinstance(expresiones, Expresiones)):
                exp = expresiones.getSecond()
                conjunto = ", " + str(exp.getValor()) + conjunto
                expresiones = expresiones.getFirst()
            #print "Expresiones: " + expresiones.toString("",False)
            conjunto = str(expresiones.getValor()) + conjunto
        
        return "{" + conjunto

    def execute(self):
        conjunto = []
        if (self.val != None):
            expresiones = self.val
            while (isinstance(expresiones, Expresiones)):
                exp = expresiones.getSecond()
                if  not (exp.getValor() in conjunto):
                    conjunto.append(exp.execute())
                expresiones = expresiones.getFirst()
            if  not (expresiones.getValor() in conjunto):
                conjunto.append(expresiones.execute())
        conjunto = list(set(conjunto))
        conjunto.sort()
        return conjunto

    def eval(self):
        conjunto = []
        if (self.val != None):
            expresiones = self.val
            while (isinstance(expresiones, Expresiones)):
                exp = expresiones.getSecond()
                if  not (exp.getValor() in conjunto):
                    conjunto.append(exp.getValor())
                expresiones = expresiones.getFirst()
            if  not (expresiones.getValor() in conjunto):
                    conjunto.append(expresiones.getValor())
        conjunto = list(set(conjunto))
        conjunto.sort()
        return listToSet(conjunto)

class ExpBinaria:
    def __init__(self, operador, exp1, exp2, fila, columna):
        self.operador = operador
        self.exp1 = exp1
        self.exp2 = exp2
        self.fila = fila
        self.columna = columna
        self.relReturnBool = set(['IGUAL', 'DIFERENTE', 'MENOR', 'MENORIGUAL', 'MAYORIGUAL', 'MAYOR'])
        self.setReturnSet = set(['UNION', 'DIFERENCIA', 'INTERSECCION'])
        self.setReturnIntSet = set(['SETSUMA', 'SETRESTA', 'SETMULT', 'SETDIV', 'SETMOD'])
        self.returnInt = set(['MOD', 'DIV', 'RESTA', 'SUMA', 'MULT'])


    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "EXPRESION BINARIA\n"
        palabra += tab + str(self.operador) + "\n"
        palabra += tab + "\t" + str(self.exp1.toString(tab,False))+"\n"
        palabra += tab + "\t" + str(self.exp2.toString(tab,False))
        return palabra

    def getValor(self):
        return str(self.exp1.getValor()) + " " + str(self.operador) + " " +str(self.exp2.getValor())

    def getType(self, flag=False):
        # print "Intentando comparar un operador de tipo " + str(self.exp1.getType()) + " con otro de tipo " + str(self.exp2.getType()) + " con el operador " + str(self.operador)
        if (self.exp1.getType() == "TypeError" or self.exp1.getType() == "TypeError"):
            return "TypeError"
        if (self.operador == "OR" or self.operador == "AND" or self.operador == 'IGUAL' or self.operador == 'DIFERENTE'
            and (self.exp1.getType() == "bool" and self.exp2.getType() == "bool")):
            return "bool"
        if (self.operador in self.relReturnBool
            and (self.exp1.getType() == "int"  and self.exp2.getType() == "int")):
            return "bool"
        if (self.operador == 'CONTIENE'
            and (self.exp1.getType() == "int" and self.exp2.getType() == "set")):
            return "bool"
        if (self.operador in self.setReturnIntSet
            and (self.exp1.getType() == "int" and self.exp2.getType() == "set")):
            return "set"
        if ((self.operador in self.setReturnSet) 
            and (self.exp1.getType() == "set"  and self.exp2.getType() == "set")):
            return "set"          
        if ((self.operador == 'IGUAL' or self.operador == 'DIFERENTE')
            and (self.exp1.getType() == "set"  and self.exp2.getType() == "set")):
            return "bool"                  
        if (self.operador in self.returnInt
            and (self.exp1.getType() == "int"  and self.exp2.getType() == "int")):
            return "int"          
        return "TypeError"        

    def verify(self):        
        self.exp1.verify()
        self.exp2.verify()
        a = self.exp1
        b = self.exp2
        # print self.getType()
        if (self.getType() == "TypeError" and a.getType() != "TypeError" and b.getType() != "TypeError"):
            global ErrorVer
            ErrorVer = True
            impr = "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": no puede utilizar el operador \"" + str(self.operador) + "\" con la "
            if (a.getType(True) == "variable"):
                impr = impr + "variable \"" + str(a.getVariable()) + "\""
            else:
                impr = impr + "expresion \"" + str(a.getValor()) + "\""
            impr = impr + " del tipo \"" + a.getType() + "\" y una "
            if (b.getType(True) == "variable"):
                impr = impr + "variable \"" + str(b.getValor()) + "\""
            else:
                impr = impr + "expresion \"" + str(b.getValor()) + "\""
            impr = impr + " del tipo \"" + str(b.getType()) + "\"."
            print(impr)
            exit(0)


    def toStringTable(self, tab, booleano):
        return ''           

    def eval(self):
        izq = self.exp1.execute()
        der = self.exp2.execute()
        #self.relReturnBool = set(['IGUAL', 'DIFERENTE', 'MENOR', 'MENORIGUAL', 'MAYORIGUAL', 'MAYOR'])
        if (self.operador == "OR"):
            if(izq == 'true' or der=='true'):
                return 'true'
            elif(izq == 'false' and der=='false'):
                return 'false'
        if (self.operador == "AND"):
            if(izq == 'true' and der=='true'):
                return 'true'
            elif(izq == 'false' or der=='false'):
                return 'false'
        if (self.operador == 'CONTIENE'):    
            if izq in der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'IGUAL'):
            if izq == der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'DIFERENTE'):
            if izq != der:
                return 'true'
            else:
                return 'false'            
        if (self.operador == 'MENOR'):
            if izq < der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'MENORIGUAL'):
            if izq <= der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'MAYORIGUAL'):
            if izq >= der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'MAYOR'):
            if izq > der:
                return 'true'
            else:
                return 'false'
        #self.setReturnSet = set(['UNION', 'DIFERENCIA', 'INTERSECCION'])
        if (self.operador == 'UNION'):
            izq = set(izq)
            der = set(der)
            return listToSet(list(izq.union(der)))
        if (self.operador == 'DIFERENCIA'):
            izq = set(izq)
            der = set(der)
            return listToSet(list(izq.difference(der)))
        if (self.operador == 'INTERSECCION'):
            izq = set(izq)
            der = set(der)
            return listToSet(list(izq.intersection(der)))
        #self.returnInt = set(['MOD', 'DIV', 'RESTA', 'SUMA', 'MULT'])
        if (self.operador == 'MOD'):
            if (der == 0):
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")            
                exit(0)
            return str(izq % der)
        if (self.operador == 'DIV'):
            if (der == 0):
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)
            return str(izq / der)
        if (self.operador == 'RESTA'):
            if izq - der > 2147483647 or izq - der < -2147483648:
                print "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": overflow"
                exit(0)             
            return str(izq - der)
        if (self.operador == 'SUMA'):
            if izq + der > 2147483647 or izq + der < -2147483648:
                print "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": overflow"
                exit(0)             
            return str(izq + der)
        if (self.operador == 'MULT'):
            if izq * der > 2147483647 or izq * der < -2147483648:
                print "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": overflow"
                exit(0)             
            return str(izq * der)
        if (self.operador == 'SETSUMA'):
            der = set(der)
            return listToSet(list(map(lambda x: x+izq, der)))
        if (self.operador == 'SETRESTA'):
            der = set(der)
            return listToSet(list(map(lambda x: izq-x, der)))
        if (self.operador == 'SETMULT'):
            der = set(der)
            return listToSet(list(set(map(lambda x: x*izq, der))))
        if (self.operador == 'SETDIV'):
            der = set(der)
            if (0 in der):
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)
            return listToSet(list(set(map(lambda x: izq/x, der))))
        if (self.operador == 'SETMOD'):
            der = set(der)
            if (0 in der):
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)            
            return listToSet(list(set(map(lambda x: izq%x, der))))

    def execute(self):
        izq = self.exp1.execute()
        der = self.exp2.execute()
        if (self.operador == 'SETSUMA'):
            der = set(der)
            return list(map(lambda x: x+izq, der))
        if (self.operador == 'SETRESTA'):
            der = set(der)
            return list(map(lambda x: izq-x, der))
        if (self.operador == 'SETMULT'):
            der = set(der)
            return list(map(lambda x: x*izq, der))
        if (self.operador == 'SETDIV'):
            der = set(der)
            if 0 in der:
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)
            return list(set(map(lambda x: izq/x, der)))
        if (self.operador == 'SETMOD'):
            der = set(der)
            if 0 in der:
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)
            return list(set(map(lambda x: izq%x, der)))
        if (self.operador == 'MOD'):
            if (der == 0):
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)            
            return izq % der
        if (self.operador == 'DIV'):
            if (der == 0):
                print("Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": Division por cero.")
                exit(0)
            return izq / der
        if (self.operador == 'RESTA'):
            if izq - der > 2147483647 or izq - der < -2147483648:
                print "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": overflow"
                exit(0)            
            return izq - der
        if (self.operador == 'SUMA'):
            if izq + der > 2147483647 or izq + der < -2147483648:
                print "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": overflow"
                exit(0)            
            return izq + der
        if (self.operador == 'MULT'):
            if izq * der > 2147483647 or izq * der < -2147483648:
                print "Error en fila "+str(self.exp1.fila)+", columna "+str(self.exp1.columna)+": overflow"
                exit(0)            
            return izq * der 
        if (self.operador == 'UNION'):
            izq = set(izq)
            der = set(der)
            return list(izq.union(der))
        if (self.operador == 'DIFERENCIA'):
            izq = set(izq)
            der = set(der)
            return list(izq.difference(der))
        if (self.operador == 'INTERSECCION'):
            izq = set(izq)
            der = set(der)
            return list(izq.intersection(der))
        if (self.operador == 'CONTIENE'):    
            if izq in der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'IGUAL'):
            if type(izq) is list and type(der) is list:
                izq = set(izq)
                der = set(der)
            if izq == der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'DIFERENTE'):
            if type(izq) is list and type(der) is list:
                izq = set(izq)
                der = set(der)           
            if izq != der:
                return 'true'
            else:
                return 'false'            
        if (self.operador == 'MENOR'):
            if izq < der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'MENORIGUAL'):
            if izq <= der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'MAYORIGUAL'):
            if izq >= der:
                return 'true'
            else:
                return 'false'
        if (self.operador == 'MAYOR'):
            if izq > der:
                return 'true'
            else:
                return 'false'                                   

        if (self.operador == "OR"):
            if(izq == 'true' or der=='true'):
                return 'true'
            elif(izq == 'false' and der=='false'):
                return 'false'

        if (self.operador == "AND"):
            if(izq == 'true' and der=='true'):
                return 'true'
            elif(izq == 'false' or der=='false'):
                return 'false'
class ExpUnaria:
    def __init__(self, tipo, operador, operando, fila, columna):
        self.tipo = tipo
        self.operador = operador
        self.operando = operando
        self.fila = fila
        self.columna = columna
        self.setReturnInt = set(['VALOR_MAXIMO', 'VALOR_MINIMO', 'SIZE'])

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "OPERACION UNARIA\n"
        palabra += tab + "tipo: " + str(self.tipo) + "\n"
        palabra += tab + str(self.operando.toString(tab, False))
        return palabra     

    def getType(self,flag=False):
        if (self.operando.getType() == "TypeError"):
            return "TypeError"

        if (self.tipo == "NEGACION_BOOL" and self.operando.getType() == "bool"):
            return "bool"

        if ((self.tipo == "MENOS_UNARIO")
            and self.operando.getType() == "int"):
            return "int"

        if ((self.tipo in self.setReturnInt)
            and self.operando.getType() == "set"):
            return "int"            

        return "TypeError" 

    def eval(self):
        
        if self.operador == 'not':
            if (self.operando.execute()) == 'true':
                return 'false'
            if (self.operando.execute()) == 'false':
                return 'true'
        if self.operador == '-':
            return str(self.operando.execute()*-1)
        if self.operador == '>?':
            if self.operando.getValor() == '{}':
                print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": conjunto vacío.")
                exit(0)
            else:            
                return str(max(self.operando.execute()))
        if self.operador == '<?':
            if self.operando.getValor() == '{}':
                print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": conjunto vacío.")
                exit(0)
            else:            
                return str(min(self.operando.execute()))
        if self.operador == '$?':
            return str(len(self.operando.execute()))


    def execute(self):
        if self.operador == 'not':
            if (self.operando.execute()) == 'true':
                return 'false'
            if (self.operando.execute()) == 'false':
                return 'true'
        if self.operador == '-':
            return (self.operando.execute()*-1)
        if self.operador == '>?':
            if self.operando.getValor() == '{}':
                print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": conjunto vacío.")
                exit(0)
            else:
                return max(self.operando.execute())
        if self.operador == '<?':
            if self.operando.getValor() == '{}':
                print("Error en fila "+str(self.fila)+", columna "+str(self.columna)+": conjunto vacío.")
                exit(0)
            else:
                return min(self.operando.execute())
        if self.operador == '$?':
            return len(self.operando.execute())

    def getValor(self):
        return str(str(self.operador) + str(self.operando.getValor()))
    
    def verify(self):
        self.operando.verify()
        a = self.operando
        if (self.getType() == "TypeError" and a.getType() != "TypeError"):
            global ErrorVer
            ErrorVer = True
            impr = "Error en fila "+str(self.fila)+", columna "+str(self.columna)+": intento de uso del operador unario \"" + str(self.operador) + "\" con la "
            if (a.getType(True) == "variable"):
                impr = impr + "variable \"" + str(a.getVariable()) + "\""
            else:
                impr = impr + "expresion \"" + str(a.getValor()) + "\""

            impr = impr + " del tipo \"" + str(a.getType()) + "\"."
            print(impr)
    
    def toStringTable(self, tab, booleano):
        tab = tab + "\t"
        palabra = tab + str(self.operando.toStringTable(tab, False))
        return palabra             

class Expresiones:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1    
        self.exp2 = exp2

    def toString(self,tab,booleano):
        palabra = str(self.exp1.toString(tab,False)) +"\n"+tab+ str(self.exp2.toString(tab,False))
        return palabra

    def getFirst(self):
        return self.exp1

    def getSecond(self):
        return self.exp2        

    def toStringTable(self, tab, booleano):
        palabra = str(self.exp1.toStringTable(tab,False)) +"\n"+tab+ str(self.exp2.toStringTable(tab,False))
        return palabra

class Entrada:
    def  __init__(self, id, fila,  columna):
        self.id = id
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano):
        palabra = 'ENTRADA' + "\n"
        palabra += tab + "\t" + "IDENTIFICADOR: " + str(self.id.toString(tab, True, False))
        return palabra

    def getValor(self):
        return self.id

    def verify(self):
        global ST
        global ErrorVer
        a = ST.lookup(self.id.getValor(), False)    
        if (a == None):
            ErrorVer = True
            print "Error en fila "+str(self.id.fila)+", columna "+str(self.id.columna)+": la variable \'%s\' no ha sido declarada" % self.id.getValor()
        if a.getType() != 'bool' and a.getType() != 'int':
            ErrorVer = True
            print "Error en fila "+str(self.id.fila)+", columna "+str(self.id.columna)+": la variable \'%s\' para entrada no es de tipo \'int\' o \'bool\'" % self.id.getValor()            
        if (a.getReservado()):
            ErrorVer = True
            print("Error en fila "+str(self.id.fila)+", columna "+str(self.id.columna)+": se intenta modificar la variable \"%s\" la cual pertenece a una iteracion." % self.id.getValor())

    def toStringTable(self, tab, booleano):
        return ""

    def execute(self):
        global ST
        variable = ST.lookup(self.id.getValor(),False)
        entrada = raw_input()
        if (variable.getType()=='int'):
            if (IsInt(entrada)):
                entrada = int(entrada)
                if ((entrada > 2147483647) or (entrada < -2147483648)):
                    print("Error: El numero no se puede representar en 32 bits.")
                    exit(0)
                ST.update(self.id.getValor(), entrada)
            else:
                print("Error: no es un numero.")
                exit(0)
        elif (variable.getType()=='bool'):
            if ((entrada != "true") and (entrada != "false")):
                print("Error: No es un valor booleano.")
                exit(0)
            ST.update(self.id.getValor(), entrada)
           

class Salida:
    def  __init__(self, tipo, imprimibles, fila,  columna):
        self.imprimibles = imprimibles
        self.tipo = tipo
        self.fila = fila
        self.columna = columna

    def toString(self, tab, booleano):
        tab = tab + "\t" 
        palabra = 'SALIDA' + "\n"
        palabra += tab + str(self.tipo) + "\n" +tab +"\t"+ str(self.imprimibles.toString(tab+"\t", True))
        return palabra 

    def verify(self):
        global ST
        global ErrorVer
        imp = self.imprimibles

        while (isinstance(imp,Imprimibles)):
            val = imp.getSecond()
            val.verify()
            imp = imp.getFirst()
        imp.verify()

    def toStringTable(self, tab, booleano):
        return ""

    def execute(self):
        elems = []

        imp = self.imprimibles
        while (isinstance(imp,Imprimibles)):
            val = imp.getSecond()
            elems.append(val.eval())
            imp = imp.getFirst()
        elems.append(imp.eval())

        palabra = ""
        elems.reverse()
        for i in elems:
            palabra += i
        
        if self.tipo == 'PRINTLN':
           palabra+="\n"
        sys.stdout.write(palabra)

class Imprimibles:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def toString(self,tab,booleano):
        palabra = self.exp1.toString(tab, True) + "\n"
        palabra += tab + "elemento: " + str(self.exp2.toString(tab, False))
        return palabra

    def getFirst(self):
        return self.exp1

    def getSecond(self):
        return self.exp2  

    def toStringTable(self, tab, booleano):
        return ""              

class Direccion :
    def __init__(self,dir):
        self.dir = dir

    def toString(self,tab,booleano):
        tab = tab + "\t"
        palabra = "\n"+tab + str(self.dir)
        return palabra

    def toStringTable(self, tab, booleano):
        return "" 

    def getValor(self):
        return self.dir


def imprimirVar(var):
    if var.getType() == 'int':
        return str(var.getValor())
    elif var.getType() == 'set':
        return listToSet(var.getValor())
    elif var.getType() == 'bool':
        return str(var.getValor())

def listToSet(l):
    palabra = "{"
    if (len(l)==0):
        palabra+="}"    
        return palabra
    j = 0
    while j < len(l)-1:
        palabra+=str(l[j])+", "
        j+=1
    palabra+=str(l[j])+"}"
    return palabra

def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
