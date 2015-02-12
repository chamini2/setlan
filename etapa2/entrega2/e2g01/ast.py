#!/usr/bin/env python
# -*- coding: UTF8 -*-

class Program:
    def __init__(self, val):
        self.val = val

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = 'PROGRAM\n' + tab + str(self.val.toString(tab,True))
        return palabra

class Condicional:
    def __init__(self, condicion, instruccion1, instruccion2):
        self.condicion = condicion
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "CONDICIONAL\n"
        palabra += tab + "condicion: " + str(self.condicion.toString(tab, False)) + "\n"
        palabra += tab + "instruccion 1: " + str(self.instruccion1.toString(tab, False))
        if (self.instruccion2 != None):
            palabra += "\n"+ tab + "instruccion 2: " +  str(self.instruccion2.toString(tab, False))
        return palabra

class IteracionConjunto:
    def __init__(self,var, direccion, exp, instruccion1):
        self.var = var
        self.direccion = direccion
        self.exp = exp
        self.instruccion1 = instruccion1

    def  toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "ITERACION CONJUNTO\n"
        palabra += tab + "variable: " + str(self.var.toString(tab, False)) + "\n"
        palabra += tab + "direccion: " + str(self.direccion.toString(tab, False)) + "\n"
        palabra += tab + "condicion: " + str(self.exp.toString(tab, False)) + "\n"
        palabra += tab + "instruccion 1: " + str(self.instruccion1.toString(tab, False))
        return palabra

class IteracionIndeterminada:
    def __init__(self,instruccion1, exp, instruccion2):
        self.instruccion1 = instruccion1
        self.exp = exp
        self.instruccion2 = instruccion2

    def  toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "ITERACION INDETERMINADA\n"
        if (self.instruccion1 != None):
            palabra += tab + "REPEAT: " + str(self.instruccion1.toString(tab, False)) + "\n"
        palabra += tab + "condicion: " + str(self.exp.toString(tab, False)) + "\n"
        if (self.instruccion2 != None):
            palabra += tab + "DO: " + str(self.instruccion2.toString(tab, False))
        return palabra

class Bloque:
    def __init__(self, declaraciones, secuencia):
        self.declaraciones = declaraciones
        self.secuencia = secuencia

    def toString(self, tab, booleano):
        fin = tab + "FINBLOQUE"
        tab = tab + "\t"
        palabra = "BLOQUE\n"
        if(self.declaraciones==self.secuencia==None):
            return palabra + "\n" + fin
        if self.declaraciones != None:
            palabra += str(self.declaraciones.toString(tab, False)) + "\n"
        palabra += tab + str(self.secuencia.toString(tab, False) + "\n")
        palabra += fin
        return palabra

class Declaracion:
    def __init__(self, declaraciones, tipo, variables):
        self.declaraciones = declaraciones
        self.tipo = tipo
        self.variables = variables

    def toString(self, tab, booleano):
        palabra = tab + "USING\n"
        if self.declaraciones != None:
            palabra = str(self.declaraciones.toString(tab, False)) + "\n" 
        tab = tab + "\t"
        palabra += tab + "tipo: " + self.tipo + "\n"
        palabra += tab+"\t" + str(self.variables.toString(tab+"\t", False)) + "\n"
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

class Secuencia:
    def __init__(self, instruccion1, instruccion2):
        self.instruccion1 = instruccion1
        self.instruccion2 = instruccion2

    def toString(self, tab, booleano):
        palabra = str(self.instruccion1.toString(tab, False)) + "\n"
        if self.instruccion2 != None:
            palabra +=  tab + str(self.instruccion2.toString(tab, False))
        return palabra

class Asignacion:
    def __init__(self, var, val):
        self.var = var
        self.val = val

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "ASIGNACION\n"
        palabra += tab + "var: " + str(self.var.toString(tab, True, False)) + "\n"
        palabra += tab + "val: " + str(self.val.toString(tab, False))
        return palabra

class Simple:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

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

class Conjunto:
    def __init__(self,val):
        self.val = val

    def toString(self,tab,booleano):
        tab = tab + "\t"
        palabra = "CONJUNTO\n"
        if (self.val == None):
            palabra += tab + 'VACIO'
        else:
            palabra += tab+ str(self.val.toString(tab, False)) 
        return palabra

class ExpBinaria:
    def __init__(self, operador, exp1, exp2):
        self.operador = operador
        self.exp1 = exp1
        self.exp2 = exp2

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "EXPRESION BINARIA\n"
        palabra += tab + str(self.operador) + "\n"
        palabra += tab + "\t" + str(self.exp1.toString(tab,False))+"\n"
        palabra += tab + "\t" + str(self.exp2.toString(tab,False))
        return palabra

class ExpUnaria:
    def __init__(self, tipo, operador, operando):
        self.tipo = tipo
        self.operador = operador
        self.operando = operando

    def toString(self, tab, booleano):
        tab = tab + "\t"
        palabra = "OPERACION UNARIA\n"
        palabra += tab + "tipo: " + str(self.tipo) + "\n"
        palabra += tab + str(self.operando.toString(tab, False))
        return palabra     

class Expresiones:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1    
        self.exp2 = exp2

    def toString(self,tab,booleano):
        palabra = str(self.exp1.toString(tab,False)) +"\n"+tab+ str(self.exp2.toString(tab,False))
        return palabra

class Entrada:
    def  __init__(self, id):
        self.id = id

    def toString(self, tab, booleano):
        palabra = 'ENTRADA' + "\n"
        palabra += tab + "\t" + "IDENTIFICADOR: " + str(self.id.toString(tab, True, False))
        return palabra

class Salida:
    def  __init__(self, tipo, id):
        self.id = id
        self.tipo = tipo

    def toString(self, tab, booleano):
        tab = tab + "\t" 
        palabra = 'SALIDA' + "\n"
        palabra += tab + str(self.tipo) + "\n" +tab +"\t"+ str(self.id.toString(tab+"\t", True))
        return palabra

class Imprimibles:
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2

    def toString(self,tab,booleano):
        palabra = self.exp1.toString(tab, True) + "\n"
        palabra += tab + "elemento: " + str(self.exp2.toString(tab, False))
        return palabra

class Direccion :
    def __init__(self,dir):
        self.dir = dir

    def toString(self,tab,booleano):
        tab = tab + "\t"
        palabra = "\n"+tab + str(self.dir)
        return palabra
