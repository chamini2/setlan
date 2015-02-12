#!/usr/bin/python
'''
Created on 7/02/2015

@author: Emmanuel De Aguiar     10-10179
@author: Daniel Pelayo          10-10539

'''


def identacion(nivel):
	return '   ' * nivel

class Programa(object):
	def __init__(self, instruccion):
		self.instruccion = instruccion

	def __str__(self):
		return '\nPrograma:\n' + self.instruccion.imprimir(1)


class Instruccion(object): pass

class Asignacion(Instruccion):
    def __init__(self, variable, valor):
        self.variable = variable
        self.valor = valor

    def imprimir(self, nivel):
        salida = identacion(nivel) + 'Asignacion:\n' + identacion(nivel + 1)
        salida += 'variable:\n'+ identacion(nivel +2)+ str(self.variable)
        salida += '\n' + identacion(nivel + 1)
        salida += 'valor:\n' + self.valor.imprimir(nivel + 2)
        return salida

class Bloque(Instruccion):
    def __init__(self,instrucciones,declaraciones,tiene):
        self.instrucciones = instrucciones
        self.declaraciones = declaraciones
        self.tieneDeclaraciones = tiene
    def imprimir(self, nivel):
        salida = identacion(nivel) + 'bloque:\n'
        if self.tieneDeclaraciones:
            salida += identacion(nivel + 1) + 'Using:'
            for elem in self.declaraciones[::-1]:
                for var in elem[1][::-1]:
                    salida+= '\n'+identacion(nivel +2) + elem[0] + ' ' +str(var)
                
            salida +='\n'+identacion(nivel + 1) + 'In:'
        
        
            for inst in self.instrucciones[::-1]:
                salida +=  '\n' + (inst.imprimir(nivel +1))
            salida += '\n' + identacion(nivel) + 'Fin bloque'
            return salida

        else:

            for elem in self.instrucciones[::-1]:
                salida += elem.imprimir(nivel +1) + '\n'
            salida += identacion(nivel) + 'Fin bloque'
            return salida


class Entrada(Instruccion):
    def __init__(self, entrada):
        self.entrada = entrada

    def imprimir(self, nivel):
        salida = identacion(nivel) + 'Entrada:\n'
        salida += self.entrada.imprimir(nivel + 1)
        return salida

class Salida(Instruccion):
    def __init__(self,salida):
        self.salida = salida

    def imprimir(self,nivel):
        result = identacion(nivel) + 'Salida:'
        for elem in self.salida[::-1]:
            result += '\n'+elem.imprimir(nivel+1)
        return result



class CondicionalIfThen(Instruccion):
    def __init__(self,condicion,instruccion):
        self.condicion = condicion
        self.instruccion = instruccion

    def imprimir(self,nivel):
        salida = identacion(nivel) + 'If:\n' + identacion(nivel + 1)
        salida += 'Condicion:\n'+ (self.condicion.imprimir(nivel + 2))
        salida += '\n' + identacion(nivel + 1)
        salida += 'Then:\n' + self.instruccion.imprimir(nivel + 2)
        return salida

class CondicionalIfThenElse(Instruccion):
    def __init__(self,condicion,instruccion,instruccion2):
        self.condicion = condicion
        self.instruccion = instruccion
        self.instruccion2 = instruccion2

    def imprimir(self,nivel):
        salida = identacion(nivel) + 'If:\n' + identacion(nivel + 1)
        salida += 'Condicion:\n'+ (self.condicion.imprimir(nivel + 2))
        salida += '\n' + identacion(nivel + 1)
        salida += 'Then:\n' + self.instruccion.imprimir(nivel + 2)
        salida += '\n'+identacion(nivel) + 'Else:\n' +(self.instruccion2.imprimir(nivel +1))
        return salida

class CicloFor(Instruccion):
    def __init__(self, variable, direccion, conjunto, instruccion):
        self.variable = variable
        self.direccion = direccion
        self.conjunto = conjunto
        self.instruccion = instruccion

    def imprimir(self,nivel):
        salida = identacion(nivel) + 'For:\n' + self.variable.imprimir(nivel+1) + '\n'
        salida += identacion(nivel+1)+'direccion:\n'+ identacion(nivel +2) +(self.direccion)
        salida += '\n' + identacion(nivel + 1) + 'In:\n' +self.conjunto.imprimir(nivel+2) +'\n'
        salida += identacion(nivel+1)+'Do:\n' + self.instruccion.imprimir(nivel + 2)
        return salida

class CicloIndeterminadoWhileDo(Instruccion):
    def __init__(self,condicion,instruccion):
        self.condicion = condicion
        self.instruccion = instruccion
    def imprimir(self,nivel):
        salida = identacion(nivel) + 'While:\n'
        salida += identacion(nivel+1)+'Condicion:\n'+ self.condicion.imprimir(nivel+2)
        salida += '\n' + identacion(nivel+1) + 'Do:\n' +self.instruccion.imprimir(nivel+2)
        return salida

class CicloIndeterminadoRepeatWhile(Instruccion):
    def __init__(self,instruccion,condicion):
        self.condicion = condicion
        self.instruccion = instruccion
    def imprimir(self,nivel):
        salida = identacion(nivel) + 'Repeat:\n'
        salida += self.instruccion.imprimir(nivel+1)+'\n'+identacion(nivel+1)+'While:\n'
        salida += self.condicion.imprimir(nivel+2)
        return salida


class CicloIndeterminadoRepeatWhileDo(Instruccion):
    def __init__(self,instruccion,condicion,instruccion2):
        self.condicion = condicion
        self.instruccion = instruccion
        self.instruccion2 = instruccion2
    def imprimir(self,nivel):
        salida = identacion(nivel) + 'Repeat:\n'
        salida += self.instruccion.imprimir(nivel+1)+'\n'+identacion(nivel+1)+'While:\n'
        salida += self.condicion.imprimir(nivel+2) + '\n'
        salida += identacion(nivel+2) + 'Do:\n' + self.instruccion2.imprimir(nivel+3)
        return salida



class Expresion(object):pass


class Int(Expresion):
    def __init__(self, numero):
        self.numero = numero

    def __str__(self):
        return str(self.numero)

    def imprimir(self, nivel):
        return identacion(nivel) + "int:\n" + identacion(nivel + 1) + str(self.numero)


class Bool(Expresion):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return str(self.valor)

    def imprimir(self, nivel):
        return identacion(nivel) + "bool:\n" + identacion(nivel + 1) + str(self.valor) 


class String(Expresion):
    def __init__(self, string):
        self.string = string

    def __str__(self):
        return str(self.string)

    def imprimir(self, nivel):
        return identacion(nivel) + "string:\n" + identacion(nivel + 1) + str(self.string) 


class ID(Expresion):
    def __init__(self, variable):
        self.variable = variable

    def __str__(self):
        return str(self.variable)

    def imprimir(self, nivel):
        return identacion(nivel) + "id:\n" + identacion(nivel + 1) + str(self.variable)


class Set(Expresion):
    def __init__(self, elementos):
        self.elementos = elementos
    def imprimir(self,nivel):
        salida = identacion(nivel) + 'set:'
        for elem in self.elementos:
            salida += '\n' + elem.imprimir(nivel +1)
        return salida


class OperacionBinaria(Expresion):
    def __init__(self, opIzq, opDer, operador,simbolo):
        self.opIzq = opIzq
        self.opDer = opDer
        self.operador = operador
        self.simb = '(%s)'%simbolo

    def imprimir(self, nivel):
        salida = identacion(nivel) + self.operador+' '+ self.simb+'\n'
        salida +=self.opIzq.imprimir(nivel+1) + '\n'
        salida += self.opDer.imprimir(nivel+1)
        """salida = identacion(nivel) + "OperacionBinaria:\n" + identacion(nivel + 1)
                                salida += "Operador: " + self.operador + '\n'
                                salida += identacion(nivel + 1) + "Operando Izquierdo:\n"
                                salida += self.opIzq.imprimir(nivel + 2) + '\n'
                                salida += identacion(nivel + 1) + "Operando Derecho:\n"
                                salida += self.opDer.imprimir(nivel + 2)"""
        return  salida


class OperacionUnaria(Expresion):
    def __init__(self, operando, operador,simbolo):
        self.operando = operando
        self.operador = operador
        self.simb = '(%s)'%simbolo

    def imprimir(self, nivel):
        salida = identacion(nivel) + str(self.operador) + ' ' +str(self.simb)+'\n'
        salida +=self.operando.imprimir(nivel+1)
        """        salida = identacion(nivel) + "OperacionUnaria:\n" + identacion(nivel + 1)
        salida += "Operador: " + str(self.operador) + '\n'
        salida += identacion(nivel + 1) + "Operando:\n"
        salida += self.operando.imprimir(nivel + 2)"""
        return salida