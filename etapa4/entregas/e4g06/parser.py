# -*- coding: UTF-8 -*-

##########################################
# CI3725 Traductores e Interpretadores   #
# Entrega 3. Grupo 6                     #
# Maria Victoria Jorge 11-10495          #
# Enrique Iglesias 11-10477              # 
##########################################

from SymTable import *
global errorDeclaracion
global TS
TS = None
errorDeclaracion = []

class Program:
    def __init__(self,inst):
        self.inst = inst

    def toString(self,tabs):
        return 'PROGRAM\n' + self.inst.toString(2)

    def check(self,line):
        return self.inst.check(line)

    def printSymTable(self,tabs):
        return self.inst.printSymTable(tabs)

    def execute(self,line):
        self.inst.execute(line)

class Bloque:
    def __init__(self,dec,exp):
        self.exp = exp
        self.dec = dec

    def toString(self,tabs):
        string = ' '*tabs + 'BLOCK_BEGIN\n'
        if (self.dec!=None):
            string += self.dec.toString(tabs + 2) 
        if (self.exp!=None):
            string += self.exp.toString(tabs + 2)
        string += ' '*tabs + 'BLOCK_END\n'
        return string

    def check(self,line):
        global TS
        if (self.dec != None):
            self.dec.check(line)
        if (self.exp != None):
            self.exp.check(line)
        if (self.dec != None):
            TS = TS.getFather()

    def printSymTable(self,tabs):
        if (isinstance(self.dec, Declarar)):
            string = ' '*tabs + 'SCOPE\n'
            string += self.dec.printSymTable(tabs + 2)
            if (self.exp != None):
                string += self.exp.printSymTable(tabs + 2)
            string += ' '*tabs + 'END_SCOPE\n'
            return string
        if (self.exp != None):
            return self.exp.printSymTable(tabs)

    def execute(self,line):
        global TS
        if (self.dec != None):
            self.dec.addValues(line)
        if (self.exp != None):
            self.exp.execute(line)
        if (self.dec != None):
            TS = TS.getFather()

class Declarar:
    def __init__(self,lista):
        self.lista = lista

    def toString(self,tabs):
        string = ' '*tabs + 'USING\n'
        string += self.lista.toString(tabs + 2) 
        string += ' '*tabs + 'IN\n'
        return string

    def check(self,line):
        global TS
        TS = Tabla(TS) #Enlazo las tablas
        self.lista.check(line)

    def printSymTable(self,tabs):
        return self.lista.printSymTable(tabs)

    def addValues(self,line):
        global TS
        TS = Tabla(TS) #Enlazo las tablas
        self.lista.addValues(line)

class Condicional:
    def __init__(self, cond, inst, inst2,linea,columna):
        self.cond = cond
        self.inst = inst
        self.inst2 = inst2
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + 'IF\n'
        string += ' '*(tabs + 2) + 'condition\n'
        string += self.cond.toString(tabs + 4) 
        string += ' '*(tabs + 2) + 'THEN\n'
        string += self.inst.toString(tabs + 4) 
        if (self.inst2 != None):
            string += ' '*(tabs + 2) + 'ELSE\n'
            string += self.inst2.toString(tabs + 4) 
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        self.cond.check(line)
        if (isinstance(self.cond,Simple)):
            if (TS != None):
                valores = TS.lookup(self.cond.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (self.cond.tipo == 'id') and (valores != None) and (auxTipo != 'bool'):
                    msg = "Error en linea "+str(self.linea - line) + ", columna " + str(self.colum)
                    msg += ": Instruccion 'if' espera expresiones de tipo bool y no "+ auxTipo + "\n"
                    errorDeclaracion.append(msg)    
                elif ((self.cond.tipo == 'int') or (self.cond.tipo == 'set')):
                    msg = "Error en linea "+str(self.linea - line) + ", columna " + str(self.colum)
                    msg += ": Instruccion 'if' espera expresiones de tipo bool y no "+ self.cond.tipo + "\n"
                    errorDeclaracion.append(msg)    
        elif (self.cond.tipoExpresion() != 'bool'):
            msg = "Error en linea "+str(self.linea - line) + ", columna " + str(self.colum)
            msg += ": Instruccion 'if' espera expresiones de tipo bool y no "+ self.cond.tipoExpresion() + "\n"
            errorDeclaracion.append(msg)
        self.inst.check(line)
        if (self.inst2 != None):
            self.inst2.check(line)
        
    def printSymTable(self,tabs):
        string = self.inst.printSymTable(tabs)
        if (self.inst2 != None):
            string += self.inst2.printSymTable(tabs)
        return string

    def execute(self,line):
        if (self.cond.evaluate(line)):
            self.inst.execute(line)
        else:
            if (self.inst2 != None):
                self.inst2.execute(line)

class Asignacion:
    def __init__(self,var,valor,linea,columna):
        self.var = var
        self.valor = valor
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + 'ASSIGN\n'
        string += self.var.toString(tabs + 2) 
        string += ' '*(tabs + 2) + 'value\n'
        string += self.valor.toString(tabs + 4) 
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        if (TS==None):
            msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
            msg += ": La variable "+str(self.var.valor)+" no ha sido declarada\n"
            errorDeclaracion.append(msg)
        elif not(TS.contains(self.var.valor)):
            msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
            msg += ": La variable "+str(self.var.valor)+" no ha sido declarada\n"
            errorDeclaracion.append(msg)
        else:
            info = TS.lookup(self.var.valor)
            self.valor.check(line) # Reviso primero que la expresión sea correcta
            if (info[1] == 'iter'):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": No puede modificar la variable "+str(self.var.valor)+" ya que es el iterador de una instrucción For\n"
                errorDeclaracion.append(msg)    
            else:
                if (isinstance(self.valor,Simple)):
                    infoAsig = TS.lookup(self.valor.valor)
                    if (infoAsig != None): 
                        if (infoAsig[1] == 'iter'):
                            auxTipo  = 'int'
                        else:
                            auxTipo = infoAsig[1]
                    if (self.valor.tipo == 'id') and (infoAsig != None) and (auxTipo != info[1]):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": No puede asignar algo de tipo "+auxTipo+" a una variable de tipo "+info[1]+"\n"
                        errorDeclaracion.append(msg)
                    elif (self.valor.tipo != 'id') and (self.valor.tipo != info[1]):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": No puede asignar algo de tipo "+self.valor.tipo+" a una variable de tipo "+info[1]+"\n"
                        errorDeclaracion.append(msg)
                else:
                    tipoOperador = self.valor.tipoExpresion()
                    if (tipoOperador != info[1]):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": No puede asignar algo de tipo "+tipoOperador+" a una variable de tipo "+info[1]+"\n"
                        errorDeclaracion.append(msg)

    def printSymTable(self,tabs):
        return ''

    def execute(self,line):
        global TS
        valAct = TS.lookup(self.var.valor)
        valNuevo = self.valor.evaluate(line)
        TS.update(self.var.valor,valNuevo,valAct[1]) # ID viejo, valor nuevo y tipo viejo

class For:
    def __init__(self, id1, direc, exp, inst,linea,columna):
        self.id1 = id1
        self.direc = direc
        self.exp = exp
        self.inst = inst
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + 'FOR\n'
        string += self.id1.toString(tabs + 2) 
        string += ' '*(tabs + 2) + 'direction\n'
        string += ' '*(tabs + 4) + self.direc.lower() +'\n'
        string += ' '*(tabs + 2) + 'IN\n'
        string += self.exp.toString(tabs + 4) 
        string += ' '*(tabs + 2) + 'DO\n'
        string += self.inst.toString(tabs + 4)
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        TS = Tabla(TS)
        TS.insert(self.id1.valor,0,'iter') #Tipo especial para la variable de iteración del For
        self.exp.check(line)
        if (isinstance(self.exp,Simple)):
            if (TS != None):
                valores = TS.lookup(self.exp.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (self.exp.tipo == 'id') and (valores != None) and (auxTipo != 'set'):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": Solo acepta expresiones de tipo 'set' no "+auxTipo+"\n"
                    errorDeclaracion.append(msg)

                elif ((self.exp.tipo == 'bool') or (self.exp.tipo == 'int')):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": Solo acepta expresiones de tipo 'set' no "+self.exp.tipo+"\n"
                    errorDeclaracion.append(msg)
        else:
            if (self.exp.tipoExpresion() != 'set'):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": Solo acepta expresiones de tipo 'set' no "+self.exp.tipoExpresion()+"\n"
                errorDeclaracion.append(msg)
        self.inst.check(line)
        TS = TS.getFather()

    def printSymTable(self,tabs):
        string = ' '*tabs + 'SCOPE\n'
        string += ' '*(tabs +2) + 'Variable: ' + self.id1.valor + ' | Type: int' 
        string += ' | Value: 0\n'
        string += self.inst.printSymTable(tabs + 2)
        string += ' '*tabs + 'END_SCOPE\n'
        return string

    def execute(self,line):
        global TS
        TS = Tabla(TS)
        TS.insert(self.id1.valor,0,'iter') #Tipo especial para la variable de iteración del For
        if (isinstance(self.exp,Simple)):
            valAct = TS.lookup(self.exp.valor)
            if (valAct != None):
                arreglo = valAct[0]
            else:
                arreglo = self.exp.evaluate(line)
        else:
            arreglo = self.exp.evaluate(line)
        if (self.direc == 'max'):
            arreglo = sorted(arreglo,reverse = True)
        else:
            arreglo = sorted(arreglo)
        for x in arreglo:
            TS.update(self.id1.valor,x,'iter')
            self.inst.execute(line)
        TS = TS.getFather()

class While:
    def __init__(self,exp,inst,linea,columna):
        self.exp = exp
        self.inst = inst
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + 'WHILE\n'
        string += ' '*(tabs + 2) + 'condition\n'
        string += self.exp.toString(tabs + 4) 
        string += ' '*tabs + 'DO\n' 
        string += self.inst.toString(tabs + 2)
        return string

    def check(self,line):
        global errorDeclaracion
        self.exp.check(line)
        if (isinstance(self.exp,Simple)): 
            if (TS != None):
                valores = TS.lookup(self.exp.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (self.exp.tipo == 'id') and (valores != None) and (auxTipo != 'bool'):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": Solo acepta expresiones de tipo 'bool' no"+auxTipo+"\n"
                    errorDeclaracion.append(msg)
                elif ((self.exp.tipo == 'int') or (self.exp.tipo == 'set')):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": Solo acepta expresiones de tipo 'bool' no"+self.exp.tipo+"\n"
                    errorDeclaracion.append(msg)
        else:
            if (self.exp.tipoExpresion() != 'bool'):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": Solo acepta expresiones de tipo 'bool' no"+self.exp.tipoExpresion()+"\n"
                errorDeclaracion.append(msg)
        self.inst.check(line)

    def printSymTable(self,tabs):
        return self.inst.printSymTable(tabs)

    def execute(self,line):
        while (self.exp.evaluate(line)):
            self.inst.execute(line)

class EntradaSalida:
    def __init__(self,flag,exp,linea,columna):
        self.flag = flag
        self.exp = exp
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + self.flag.upper() + '\n'
        if (self.flag =='scan'):
            string += self.exp.toString(tabs + 2)
        else:
            string += ' '*(tabs + 2) + 'elements\n'
            string += self.exp.toString(tabs + 4) 
            if (self.flag =='println'):
                string += ' '*(tabs + 4) + 'string\n'
                string += ' '*(tabs + 6) + '"\\n"' + '\n'
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        if (self.flag == 'scan'):
            if (TS != None):
                valores = TS.lookup(self.exp.valor)
                if (valores != None):
                    if (valores[1] == 'set'):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": La instrucción 'scan' solo acepta variables de tipo 'int' y 'bool' no "+valores[1]+"\n"
                        errorDeclaracion.append(msg)
                    elif (valores[1] == 'iter'):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": No puede modificar la variable "+str(self.exp.valor)+" ya que es el iterador de una instrucción For\n"
                        errorDeclaracion.append(msg)  
        self.exp.check(line)

    def printSymTable(self,tabs):
        return ''

    def execute(self,line):
        global TS
        if (self.flag == 'scan'):
            valores = TS.lookup(self.exp.valor)
            esValido = False
            while not(esValido):
                nuevo = raw_input()
                esValido = self.esValido(valores[1],nuevo)
            if (valores[1] == 'int'):
                nuevo = int(nuevo)
            else:
                nuevo = bool(nuevo)
            TS.update(self.exp.valor,nuevo,valores[1])
        else:
            string = ""
            aux = self.exp.evaluate(line)
            if (isinstance(aux,set)):
                setTmp = list(aux)
                setTmp.sort()
                if (setTmp == []):
                    string += '{}'
                else:
                    string += '{'
                    for elem in range(len(setTmp)):
                        if (elem < len(setTmp)-1):
                            string += str(setTmp[elem]) + ','
                        else:
                            string += str(setTmp[elem]) + '}'
            elif (isinstance(aux,bool)):
                string += str(aux).lower()
            else:
                string += str(aux)
            if (self.flag == 'print'):
                print string, # La coma está para que no se vaya a una nueva línea
            else:
                print string

    def esValido(self, tipo, nuevo):
        try:
            if (tipo == 'int'):
                nuevo = int(nuevo)
                if ((nuevo > 2147483647) or (nuevo < -2147483648)):
                    print "ERROR: El número ingresado no puede representarse en 32 bits"
                    return False
            else:
                if (nuevo!='true') and (nuevo!='false'):
                    print "ERROR: Los valores válidos para un booleano son true y false"
                    return False
            return True
        except ValueError:
            print "ERROR: Valor erróneo para una variable de tipo int"
            return False


class Opbin:
    def __init__(self,izq,op,der,linea,columna):
        self.izq = izq
        self.op = op
        self.der = der
        self.opMixtos = set(['<+>','<->','<*>','</>','<%>','@'])
        self.tipoOperandos = {
            '+'     : 'int',
            '-'     : 'int',
            '*'     : 'int',
            '/'     : 'int',
            '%'     : 'int',
            '++'    : 'set',
            '><'    : 'set',
            '\\'    : 'set',
            '<+>'   : 'set',
            '<->'   : 'set',
            '<*>'   : 'set',
            '</>'   : 'set',
            '<%>'   : 'set',
            '<'     : 'int',
            '<='    : 'int',
            '>'     : 'int',
            '>='    : 'int',
            '=='    : 'esp', # especial porque los operandos pueden ser de cualquier tipo
            '/='    : 'esp',
            '@'     : 'bool',
            'or'    : 'bool',
            'and'   : 'bool' 
        }
        self.linea = linea
        self.colum = columna

    def tipoExpresion(self):
        operadores = {
            '+'     : 'int',
            '-'     : 'int',
            '*'     : 'int',
            '/'     : 'int',
            '%'     : 'int',
            '++'    : 'set',
            '><'    : 'set',
            '\\'    : 'set',
            '<+>'   : 'set',
            '<->'   : 'set',
            '<*>'   : 'set',
            '</>'   : 'set',
            '<%>'   : 'set',
            '<'     : 'bool',
            '<='    : 'bool',
            '>'     : 'bool',
            '>='    : 'bool',
            '=='    : 'bool',
            '/='    : 'bool',
            '@'     : 'bool',
            'or'    : 'bool',
            'and'   : 'bool'
        }
        return operadores.get(self.op)

    def toString(self,tabs):
        operadores = {
            '+'     : 'PLUS',
            '-'     : 'MINUS',
            '*'     : 'TIMES',
            '/'     : 'DIVIDE',
            '%'     : 'MODULE',
            '++'    : 'UNION',
            '><'    : 'INTERSECTION',
            '\\'    : 'DIFERENCE',
            '<+>'   : 'PLUS_MAP',
            '<->'   : 'MINUS_MAP',
            '<*>'   : 'TIMES_MAP',
            '</>'   : 'DIVIDE_MAP',
            '<%>'   : 'MODULE_MAP',
            '<'     : 'LESS',
            '<='    : 'LESS_EQUAL',
            '>'     : 'GREATER',
            '>='    : 'GREATER_EQUAL',
            '=='    : 'EQUALS',
            '/='    : 'NOT_EQUAL',
            '@'     : 'AT',
            'or'    : 'Or',
            'and'   : 'And'
        }
        string = ' '*tabs + operadores[self.op] +' ' + self.op + '\n'
        if (isinstance(self.izq,Simple)):
            if (self.izq.tipo=='id'):
                string += ' '*(tabs + 2) + 'variable\n'
                string += ' '*(tabs + 4) + self.izq.valor + '\n'
            else:
                string += self.izq.toString(tabs + 2) 
        else:
            string += self.izq.toString(tabs + 2) 

        if (isinstance(self.der,Simple)):
            if (self.der.tipo=='id'):
                string += ' '*(tabs + 2) + 'variable\n'
                string += ' '*(tabs + 4) + self.der.valor + '\n'
            else:
                string += self.der.toString(tabs + 2) 
        else:
            string += self.der.toString(tabs + 2) 
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        tipoOperandos = self.tipoOperandos.get(self.op)
        esOpEspecial = (self.tipoOperandos.get(self.op) == 'esp')

        self.izq.check(line)
        self.der.check(line)

        if (isinstance(self.izq,Simple)):
            if (TS != None):
                valores = TS.lookup(self.izq.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (valores != None) and (self.izq.tipo == 'id') and (auxTipo != None):
                    if (self.op in self.opMixtos):
                        if (auxTipo != 'int'):
                            msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                            msg += ": El operador "+self.op+" espera una expresion de tipo int no " + auxTipo + "\n"
                            errorDeclaracion.append(msg)    
                    elif (auxTipo != tipoOperandos) and not(esOpEspecial):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": El operador "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+auxTipo+"\n"
                        errorDeclaracion.append(msg)
                elif (self.op in self.opMixtos):
                    if (self.izq.tipo != 'int') and (self.izq.tipo!='id'):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": El operador "+self.op+" espera una expresion de tipo int no " + self.izq.tipo + "\n"
                        errorDeclaracion.append(msg)
                elif (self.izq.tipo!='id') and (self.izq.tipo != tipoOperandos) and not(esOpEspecial):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": El operador "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+self.izq.tipo+"\n"
                    errorDeclaracion.append(msg)
        else:
            if (self.op in self.opMixtos):
                if (self.izq.tipoExpresion() != 'int'):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": El operador "+self.op+" espera una expresion de tipo int no " + self.izq.tipoExpresion() + "\n"
                    errorDeclaracion.append(msg)
            elif (self.izq.tipoExpresion() != tipoOperandos) and not(esOpEspecial):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": El operador "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+self.izq.tipoExpresion()+"\n"
                errorDeclaracion.append(msg)

        if (isinstance(self.der,Simple)):
            if (TS != None):
                valores = TS.lookup(self.der.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (valores != None) and (self.der.tipo == 'id') and (auxTipo != None):
                    if (self.op in self.opMixtos):
                        if (auxTipo != 'set'):
                            msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                            msg += ": El operador "+self.op+" espera una expresion de tipo set no " + auxTipo + "\n"
                            errorDeclaracion.append(msg)    
                    elif (auxTipo != tipoOperandos) and not(esOpEspecial):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": El operador "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+auxTipo+"\n"
                        errorDeclaracion.append(msg)
                elif (self.op in self.opMixtos): 
                    if (self.der.tipo != 'set'):
                        msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                        msg += ": El operador "+self.op+" espera una expresion de tipo set no " + self.der.tipo + "\n"
                        errorDeclaracion.append(msg)
                elif (self.der.tipo != tipoOperandos) and not(esOpEspecial):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": El operador "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+self.der.tipo+"\n"
                    errorDeclaracion.append(msg) 
        else:
            if (self.op in self.opMixtos): 
                if (self.der.tipoExpresion() != 'set'):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": El operador "+self.op+" espera una expresion de tipo set no " + self.der.tipoExpresion() + "\n"
                    errorDeclaracion.append(msg)
            elif (self.der.tipoExpresion() != tipoOperandos) and not(esOpEspecial):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": El operador "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+self.der.tipoExpresion()+"\n"
                errorDeclaracion.append(msg)

    def printSymTable(self,tabs):
        return ''

    def evaluate(self,line):
        if (self.op == '+'):
            res = self.izq.evaluate(line) + self.der.evaluate(line)
            if ((res > 2147483647) or (res < -2147483648)):
                print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
        elif (self.op == '-'):
            res = self.izq.evaluate(line) - self.der.evaluate(line)
            if ((res > 2147483647) or (res < -2147483648)):
                print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
        elif (self.op == '*'):
            res = self.izq.evaluate(line) * self.der.evaluate(line)
            if ((res > 2147483647) or (res < -2147483648)):
                print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
        elif (self.op == '/'):
            if (self.der.evaluate(line) == 0):
                print "ERROR: división por cero en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            res = self.izq.evaluate(line) / self.der.evaluate(line)
            if ((res > 2147483647) or (res < -2147483648)):
                print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
        elif (self.op == '%'):
            if (self.der.evaluate(line) == 0):
                print "ERROR: división por cero en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            res = self.izq.evaluate(line) % self.der.evaluate(line)
            if ((res > 2147483647) or (res < -2147483648)):
                print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
        elif (self.op == '++'):
            res = self.izq.evaluate(line).copy()
            res |= self.der.evaluate(line)
        elif (self.op == '><'):
            res = self.izq.evaluate(line).copy()
            res &= self.der.evaluate(line)
        elif (self.op == '\\'):
            res = self.izq.evaluate(line).copy()
            res -= self.der.evaluate(line)
        elif (self.op == '<+>'):
            aux = self.der.evaluate(line).copy()
            num = self.izq.evaluate(line)
            res = set()
            for elem in aux:
                if ((num + elem > 2147483647) or (num + elem < -2147483648)):
                    print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    exit(0)
                res.add(num + elem)
        elif (self.op == '<->'):
            aux = self.der.evaluate(line).copy()
            num = self.izq.evaluate(line)
            res = set()
            for elem in aux:
                if ((num - elem > 2147483647) or (num - elem < -2147483648)):
                    print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    exit(0)
                res.add(num - elem)
        elif (self.op == '<*>'):
            aux = self.der.evaluate(line).copy()
            num = self.izq.evaluate(line)
            res = set()
            for elem in aux:
                if ((num * elem > 2147483647) or (num * elem < -2147483648)):
                    print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    exit(0)
                res.add(num * elem)
        elif (self.op == '</>'):
            if (self.izq.evaluate(line) == 0):
                print "ERROR: división por cero en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            aux = self.der.evaluate(line).copy()
            num = self.izq.evaluate(line)
            res = set()
            for elem in aux:
                if ((num / elem > 2147483647) or (num / elem < -2147483648)):
                    print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    exit(0)
                res.add(num / elem)
        elif (self.op == '<%>'):
            if (self.izq.evaluate(line) == 0):
                print "ERROR: división por cero en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            aux = self.der.evaluate(line).copy()
            num = self.izq.evaluate(line)
            res = set()
            for elem in aux:
                if ((num % elem > 2147483647) or (num % elem < -2147483648)):
                    print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    exit(0)
                res.add(num % elem)
        elif (self.op == '<'):
            res = self.izq.evaluate(line) < self.der.evaluate(line)
        elif (self.op == '<='):
            res = self.izq.evaluate(line) <= self.der.evaluate(line)
        elif (self.op == '>'):
            res = self.izq.evaluate(line) > self.der.evaluate(line)
        elif (self.op == '>='):
            res = self.izq.evaluate(line) >= self.der.evaluate(line)
        elif (self.op == '=='):
            res = self.izq.evaluate(line) == self.der.evaluate(line)
        elif (self.op == '/='):
            res = self.izq.evaluate(line) != self.der.evaluate(line)
        elif (self.op == '@'):
            res = self.izq.evaluate(line) in self.der.evaluate(line)
        elif (self.op == 'and'):
            res = self.izq.evaluate(line) and self.der.evaluate(line)
        elif (self.op == 'or'):
            res = self.izq.evaluate(line) or self.der.evaluate(line)
        return res


class Simple:
    def __init__(self,tipo,valor,linea,columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        if (self.tipo=='id'):
            string = ' '*tabs + 'variable' + '\n'
            string += ' '*(tabs + 2) + str(self.valor) + '\n'
        elif (self.tipo=='set'):
            string = ' '*tabs + self.tipo + '\n'
            if (self.valor != None):
                string += self.valor.toString(tabs + 2)
        else:    
            string = ' '*tabs + self.tipo + '\n'
            string += ' '*(tabs + 2) + str(self.valor) + '\n'
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        if (self.tipo == 'id') and ((TS == None) or (TS.contains(self.valor) == None)):
            msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
            msg += ": La variable "+self.valor+" no ha sido declarada\n"
            errorDeclaracion.append(msg)

    def printSymTable(self,tabs):
        return ''

    def evaluate(self,line):
        global TS
        if (self.tipo == 'int'):
            return self.valor
        elif (self.tipo == 'bool'):
            return (self.valor == 'true')
        elif (self.tipo == 'id'):
            valores = TS.lookup(self.valor)
            return valores[0]
        else:
            if (self.valor == None): # Caso de conjunto vacío
                return set()
            if not(isinstance(self.valor,ListaNumero)): # Caso que es un singleton
                res = set()
                res.add(self.valor.evaluate(line))
                return res
            return self.valor.evaluate(line)


class Repeat:
    def __init__(self,inst1,exp,inst2,linea,columna):
        self.inst1 = inst1
        self.exp = exp
        self.inst2 = inst2
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + 'REPEAT\n'
        string += self.inst1.toString(tabs + 2) 
        string += ' '*tabs + 'WHILE\n'
        string += ' '*(tabs + 2) + 'condition\n'
        string += self.exp.toString(tabs + 4) 
        if (self.inst2!=None):
            string += ' '*tabs + 'DO\n'
            string += self.inst2.toString(tabs + 2)
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        self.inst1.check(line)
        self.exp.check(line)
        if (isinstance(self.exp,Simple)):
            if (TS != None):
                valores = TS.lookup(self.exp.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (self.exp.tipo == 'id') and (valores != None) and (auxTipo!='bool'):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": Solo acepta expresiones de tipo 'bool' no "+auxTipo+"\n"
                    errorDeclaracion.append(msg)
                elif ((self.exp.tipo == 'set') or (self.exp.tipo == 'int')):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": Solo acepta expresiones de tipo 'bool' no "+self.exp.tipoExpresion()+"\n"
                    errorDeclaracion.append(msg)
        else:
            if (self.exp.tipoExpresion() != 'bool'):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": Solo acepta expresiones de tipo 'bool' no "+self.exp.tipoExpresion()+"\n"
                errorDeclaracion.append(msg)
        if (self.inst2 != None):
            self.inst2.check(line)

    def printSymTable(self,tabs):
        string = self.inst1.printSymTable(tabs)
        if (self.inst2 != None):
            string += self.inst2.printSymTable(tabs)
        return string

    def execute(self,line):
        while (True):
            self.inst1.execute(line)
            if (self.exp.evaluate(line)):
                if (self.inst2 != None):
                    self.inst2.execute(line)
            else:
                break            

class Uniop:
    def __init__(self,op,val,linea,columna):
        self.val = val
        self.op = op
        self.linea = linea
        self.colum = columna
        self.tipoOperandos = {
            '-'     :   'int',
            '<?'    :   'set',
            '>?'    :   'set',
            '$?'    :   'set',
            'not'   :   'bool'
        }

    def tipoExpresion(self):
        operadores = {
            '-'     : 'int',
            '<?'    : 'int',
            '>?'    : 'int',
            '$?'    : 'int',
            'not'   : 'bool'
        }
        return operadores.get(self.op)

    def toString(self,tabs):
        operadores = {
            '-'     : 'UMINUS',
            '<?'    : 'MIN_SET',
            '>?'    : 'MAX_SET',
            '$?'    : 'SIZE',
            'not'   : 'Not'
        }
        string = ' '*tabs + operadores[self.op] + '\n'
        string += self.val.toString(tabs + 2) 
        return string

    def check(self,line):
        global errorDeclaracion
        global TS
        tipoOperandos = self.tipoOperandos.get(self.op)
        if (isinstance(self.val,Simple)):
            if (TS != None):
                valores = TS.lookup(self.val.valor)
                if (valores != None): 
                    if (valores[1] == 'iter'):
                        auxTipo  = 'int'
                    else:
                        auxTipo = valores[1]
                if (self.val.tipo == 'id') and (valores != None) and (auxTipo != tipoOperandos):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+auxTipo+"\n"
                    errorDeclaracion.append(msg)
                elif (self.val.tipo != tipoOperandos) and (self.val.tipo != 'id'):
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                    msg += ": "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+self.val.tipo+"\n"
                    errorDeclaracion.append(msg)
        else:
            if (self.val.tipoExpresion() != tipoOperandos):
                msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                msg += ": "+self.op+" solo acepta expresiones de tipo '"+tipoOperandos+"' no "+self.val.tipoExpresion()+"\n"
                errorDeclaracion.append(msg)
        self.val.check(line)

    def printSymTable(self,tabs):
        return ''

    def evaluate(self,line):
        global TS
        if (self.op == 'not'):
            return not (self.val.evaluate(line))
        elif (self.op == '$?'):
            return len(self.val.evaluate(line))
        elif (self.op == '-'):
            res = self.val.evaluate(line)
            res = -res
            if ((res > 2147483647) or (res < -2147483648)):
                print "ERROR: se produjo overflow en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            else:
                return res
        elif (self.op == '<?'):
            if (len(self.val.evaluate(line)) == 0):
                print "ERROR: conjunto vacío en la operación '<?' en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            else:
                return min(self.val.evaluate(line))
        else:
            if (len(self.val.evaluate(line)) == 0):
                print "ERROR: conjunto vacío en la operación '>?' en la linea "+str(self.linea - line)+", columna "+str(self.colum)
                exit(0)
            else:
                return max(self.val.evaluate(line))


class CadenaString:
    def __init__(self,string):
        self.string = string

    def toString(self,tabs):
        string = ' '*tabs + 'string\n'
        string += ' '*(tabs + 2) + '"' + self.string + '"' + '\n'
        return string

    def check(self,line):
        pass

    def printSymTable(self,tabs):
        return ''

    def evaluate(self,line):
        string = ""
        i = 0
        while (i < len(self.string)):
            if (self.string[i]=='\\'):
                if (self.string[i+1]=='n'):
                    string += '\n'
                elif (self.string[i+1]=='"'):
                    string += '"'
                elif (self.string[i+1]=='\\'):
                    string += '\\'
                i = i + 2
            else:
                string += self.string[i]
                i = i + 1
        return string


class ListaInstruccion:
    def __init__(self,inst1,inst2):
        self.inst1 = inst1
        self.inst2 = inst2

    def toString(self,tabs):
        string = self.inst1.toString(tabs)
        if (self.inst2 != None):
            string += self.inst2.toString(tabs)
        return string

    def check(self,line):
        global TS
        self.inst1.check(line)
        if (self.inst2 != None):
            self.inst2.check(line)
        
    def printSymTable(self,tabs):
        string = self.inst1.printSymTable(tabs)
        if (self.inst2 != None):
            string += self.inst2.printSymTable(tabs)
        return string

    def execute(self,line):
        self.inst1.execute(line)
        if (self.inst2 != None):
            self.inst2.execute(line)

class ListaDeclaracion:
    def __init__(self, tipo, idList, decList,linea,columna):
        self.tipo = tipo
        self.idList = idList
        self.decList = decList
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ' '*tabs + self.tipo + '\n'
        string += self.idList.toString(tabs + 2)
        if (self.decList!=None):
            string += self.decList.toString(tabs)
        return string

    def check(self,line):
        global TS
        global errorDeclaracion
        valDefecto = {
            'int'   :   0,
            'bool'  :   False,
            'set'   :   set()
        }
        lista = self.idList
        if (TS.isInTable(lista.id1.valor)):
                msg = "Error en linea "+ str(self.linea - line) + ", columna " + str(self.colum)
                msg += ": La variable "+ lista.id1.valor +" ya se encuentra declarada en este alcance\n"
                errorDeclaracion.append(msg)
        else:
            TS.insert(lista.id1.valor,valDefecto.get(self.tipo),self.tipo)

        if (isinstance(lista.idList,ListaID)):
            while (lista.idList != None):
                if (TS.isInTable(lista.idList.id1.valor)):
                    msg = "Error en linea "+ str(self.linea - line) + ", columna " + str(self.colum)                    
                    msg += ": La variable "+ lista.idList.id1.valor +" ya se encuentra declarada en este alcance\n"
                    errorDeclaracion.append(msg)
                else:
                    TS.insert(lista.idList.id1.valor,valDefecto.get(self.tipo),self.tipo)
                lista = lista.idList

        if (isinstance(self.decList,ListaDeclaracion)):
            self.decList.check(line)

    def printSymTable(self,tabs):
        valDefecto = {
            'int'   :   0,
            'bool'  :   False,
            'set'   :   '{}'
        }
        lista = self.idList
        string = ' '*tabs + 'Variable: ' + lista.id1.valor + ' | Type: ' + self.tipo
        string += ' | Value: ' + str(valDefecto.get(self.tipo)) + '\n'
        if (isinstance(lista.idList,ListaID)):
            while (lista.idList != None):
                string += ' '*tabs + 'Variable: ' + lista.idList.id1.valor + ' | Type: ' + self.tipo
                string += ' | Value: ' + str(valDefecto.get(self.tipo)) + '\n'
                lista = lista.idList

        if (isinstance(self.decList,ListaDeclaracion)):
            string += self.decList.printSymTable(tabs)
        return string

    def addValues(self,line):
        global TS
        valDefecto = {
            'int'   :   0,
            'bool'  :   False,
            'set'   :   set()
        }
        lista = self.idList
        TS.insert(lista.id1.valor,valDefecto.get(self.tipo),self.tipo)
        if (isinstance(lista.idList,ListaID)):
            while (lista.idList != None):
                TS.insert(lista.idList.id1.valor,valDefecto.get(self.tipo),self.tipo)
                lista = lista.idList
        if (isinstance(self.decList,ListaDeclaracion)):
            self.decList.addValues(line)

class ListaID:
    def __init__(self,idList,id1):
        self.idList = idList
        self.id1 = id1

    def toString(self,tabs):
        string = ''
        if (self.idList != None):
            string += self.idList.toString(tabs)
        string += self.id1.toString(tabs)
        return string

    def check(self,line):
        pass

    def printSymTable(self,tabs):
        return ''

class ListaNumero:
    def __init__(self,numList,num,linea,columna):
        self.numList = numList
        self.num = num
        self.linea = linea
        self.colum = columna

    def toString(self,tabs):
        string = ''
        if (self.numList!=None):
            string += self.numList.toString(tabs)
        string += self.num.toString(tabs)
        return string

    def check(self,line):
        global TS
        global errorDeclaracion
        if (isinstance(num,Simple)): 
            if ((self.num.tipo == 'bool') or (self.num.tipo == 'set')):
                msg = "Error en linea "+ str(self.linea - line)+ ", columna " + str(self.colum) 
                msg += ": Los conjuntos solo aceptan elementos de tipo 'int' no de tipo "+ self.num.tipo + '\n'
                errorDeclaracion.append(msg)
            elif (num.tipo == 'id'): # Chequear si corresponde a un entero
                tipo = TS.lookup(self.num.valor)
                if (tipo != None): #Existe en alguna tabla
                    if (tipo[1] != 'int') and (tipo[1] != 'iter'):
                        msg = "Error en linea "+ str(self.linea - line) + ", columna " + str(self.colum) 
                        msg += ": Los conjuntos solo aceptan elementos de tipo 'int' no de tipo "+ tipo[1] + '\n'
                        errorDeclaracion.append(msg)
                else:
                    msg = "Error en la linea "+str(self.linea - line)+", columna "+str(self.colum) 
                    msg += ": La variable "+self.num.valor+" no ha sido declarada\n"
                    errorDeclaracion.append(msg)

        self.numList.check(line)

    def printSymTable(self,tabs):
        return ''

    def evaluate(self,line):
        global TS
        conjunto = set()
        conjunto.add(self.num.evaluate(line))
        lista = self.numList
        while (isinstance(lista,ListaNumero)):
            conjunto.add(lista.num.evaluate(line))
            lista = lista.numList
        conjunto.add(lista.evaluate(line))
        return conjunto


class ListaImpresion:
    def __init__(self,listExp,exp):
        self.listExp = listExp
        self.exp = exp

    def toString(self,tabs):
        string = ''
        if (self.listExp!=None):
            string += self.listExp.toString(tabs)
        string += self.exp.toString(tabs)
        return string

    def check(self,line):
        self.exp.check(line)
        self.listExp.check(line)

    def printSymTable(self,tabs):
        return ''

    def evaluate(self,line):
        string = self.listExp.evaluate(line)
        if (isinstance(string,set)):
            setTmp = list(string)
            setTmp.sort()
            if (setTmp == []):
                string = '{}'
            else:
                string = '{'
                for elem in range(len(setTmp)):
                    if (elem < len(setTmp)-1):
                        string += str(setTmp[elem]) + ','
                    else:
                        string += str(setTmp[elem]) + '}'
        elif (isinstance(string,bool)):
            string = str(string).lower()
        else:
            string = str(string)
        aux = self.exp.evaluate(line)
        if (isinstance(aux,set)):
            setTmp = list(aux)
            setTmp.sort()
            if (setTmp == []):
                string += '{}'
            else:
                string += '{'
                for elem in range(len(setTmp)):
                    if (elem < len(setTmp)-1):
                        string += str(setTmp[elem]) + ','
                    else:
                        string += str(setTmp[elem]) + '}'
        elif (isinstance(aux,bool)):
                string += str(aux).lower()
        else:
            string += str(aux)
        return string

        
precedence = (
    # Precedencia del if
    ('right','IFX'),
    ('right','ELSE'),

    # Operadores booleanos
    ('left', 'Or'),
    ('left', 'And'),        
    ('right', 'Not'),

    # Operadores comparativos
    ('nonassoc','Greater','GreaterEqual', 'Less','LessEqual'),    
    ('left','Equals','NotEqual'),
    ('nonassoc','At'),

    # Operadores aritméticos
    ('left', 'Plus', 'Minus'),
    ('left','Times','Divide','Module'),

    # Operadores de conjuntos
    ('left','Union','Diference'),
    ('left','Intersection'),

    # Operadores conjunto-aritméticos
    ('left','PlusMap','MinusMap'),
    ('left', 'TimesMap','DivideMap','ModuleMap'),

    # Operadores unarios
    ('right', 'UMINUS','MinSet','MaxSet','Size')
    )

def p_program(p):
    '''PROGRAM : Program INST'''
    p[0] = Program(p[2])

def p_tipos(p):
    ''' TIPOS   : Int 
                | Set 
                | Boolean '''
    p[0] = p[1]

def p_enumList(p): 
    '''ENUM_LIST    : String
                    | EXP
                    | ENUM_LIST Comma EXP
                    | ENUM_LIST Comma String'''
    if (len(p)==2):
        if (isinstance(p[1],str)):
            p[0] = CadenaString(p[1])
        else:
            p[0] = p[1]
    else:
        if (isinstance(p[3],str)):
            p[0] = ListaImpresion(p[1],CadenaString(p[3]))
        else:
            p[0] = ListaImpresion(p[1],p[3])


def p_declarar(p):
    '''DECLARAR : Using DEC_LIST In'''
    p[0] = Declarar(p[2])

def p_epsilon(p):
    ''' EPSILON : '''
    pass

def p_decList(p):
    '''DEC_LIST   : TIPOS ID_LIST Semicolon DEC_LIST
                  | TIPOS ID_LIST Semicolon '''

    if (len(p)==4):
        p[0] = ListaDeclaracion(p[1],p[2],None,p.lineno(3),find_column2(p.lexer.lexdata,p,3)-4)
    else:
        p[0] = ListaDeclaracion(p[1],p[2],p[4],p.lineno(3),find_column2(p.lexer.lexdata,p,3)-4)


def p_instList(p):
    '''INST_LIST    : INST Semicolon INST_LIST
                    | EPSILON '''
    if (len(p)==4):
        p[0] = ListaInstruccion(p[1],p[3])
    elif (len(p)==2):
	pass


def p_idList(p):
    '''ID_LIST    : ID_LIST Comma ID 
                    | ID '''
    if (len(p)==2):
        p[0] = ListaID(None,Simple('id',p[1],p.lineno(1),find_column2(p.lexer.lexdata,p,1)))
    else:
        p[0] = ListaID(p[1],Simple('id',p[3],p.lineno(2),find_column2(p.lexer.lexdata,p,1)))

def p_exp(p):
    '''EXP  : Number
            | ID
            | OpenCurly NUMBER_LIST CloseCurly
            | OpenCurly CloseCurly
            | Lparen EXP Rparen
            | Minus EXP %prec UMINUS
            | EXP Plus EXP
            | EXP Minus EXP
            | EXP Times EXP
            | EXP Divide EXP
            | EXP Module EXP
            | EXP PlusMap EXP
            | EXP MinusMap EXP
            | EXP TimesMap EXP
            | EXP DivideMap EXP
            | EXP ModuleMap EXP
            | EXP Union EXP
            | EXP Intersection EXP
            | EXP Diference EXP
            | MaxSet EXP
            | MinSet EXP
            | Size EXP
            | True
            | False 
            | EXP And EXP
            | EXP Or EXP
            | Not EXP
            | EXP Equals EXP
            | EXP Greater EXP
            | EXP GreaterEqual EXP
            | EXP Less EXP
            | EXP LessEqual EXP
            | EXP NotEqual EXP
            | EXP At EXP '''

    if (len(p)==2):
        if (isinstance(p[1],int)):
            tipo = 'int'
        elif (p[1]=='true') or (p[1]=='false'):
            tipo = 'bool'
        else:
            tipo = 'id'
        p[0] = Simple(tipo,p[1],p.lineno(1),find_column2(p.lexer.lexdata,p,1))

    elif (len(p)==3):
        if (p[1] == '{'):
            p[0] = Simple('set',None,p.lineno(1),find_column2(p.lexer.lexdata,p,1))
        else:
            p[0] = Uniop(p[1],p[2],p.lineno(1),find_column2(p.lexer.lexdata,p,1))

    else:
        if (p[1]=='('):
            p[0] = p[2]
        elif (p[1]=='{'):
            p[0] = Simple('set',p[2],p.lineno(1),find_column2(p.lexer.lexdata,p,1))
        else:
            p[0] = Opbin(p[1],p[2],p[3],p.lineno(2),find_column2(p.lexer.lexdata,p,2))


def p_inst(p):
    '''INST : ID Assign EXP
            | OpenCurly DECLARAR INST_LIST CloseCurly
            | OpenCurly INST_LIST CloseCurly
            | Scan ID
            | Print ENUM_LIST
            | Println ENUM_LIST
            | IF Lparen EXP Rparen INST %prec IFX
            | IF Lparen EXP Rparen INST ELSE INST
            | FOR ID DIRECCION EXP DO INST
            | REPEAT INST WHILE EXP
            | REPEAT INST WHILE EXP DO INST
            | WHILE EXP DO INST'''
    if (len(p)==3):
        if (p[1]=='scan'):
            p[0] = EntradaSalida(p[1],Simple('id',p[2],p.lineno(2),find_column2(p.lexer.lexdata,p,2)),p.lineno(1),find_column2(p.lexer.lexdata,p,2))
        else:
            p[0] = EntradaSalida(p[1],p[2],p.lineno(1),find_column2(p.lexer.lexdata,p,2))

    elif (len(p)==4):
        if (p[1]=='{'):
            p[0] = Bloque(None,p[2])
        else:
            p[0] = Asignacion(Simple('id',p[1],p.lineno(1),find_column2(p.lexer.lexdata,p,1)),p[3],p.lineno(1),find_column2(p.lexer.lexdata,p,1))
    elif (len(p)==5):
        if (p[1]=='{'):
            p[0] = Bloque(p[2],p[3])
        elif (p[1]=='repeat'):
            p[0] = Repeat(p[2],p[4],None,p.lineno(1),find_column2(p.lexer.lexdata,p,1))
        else:
            p[0] = While(p[2],p[4],p.lineno(1),find_column2(p.lexer.lexdata,p,1))

    elif (len(p)==6):
        p[0] = Condicional(p[3],p[5],None,p.lineno(1),find_column2(p.lexer.lexdata,p,1))

    elif (len(p)==7):
        if (p[1]=='for'):
            p[0] = For(Simple('int',p[2],p.lineno(1),find_column2(p.lexer.lexdata,p,1)),p[3],p[4],p[6],p.lineno(1),find_column2(p.lexer.lexdata,p,1))
        else:
            p[0] = Repeat(p[2],p[4],p[6],p.lineno(3),find_column2(p.lexer.lexdata,p,3))
    else:
        p[0] = Condicional(p[3],p[5],p[7],p.lineno(1),find_column2(p.lexer.lexdata,p,1))

def p_direccion(p):
    ''' DIRECCION : MIN
                  | MAX '''
    p[0] = p[1]

def p_numberList(p):
    '''NUMBER_LIST  : NUMBER_LIST Comma EXP 
                    | EXP '''
    if (len(p)==2):
        p[0] = p[1]
    else:
        p[0] = ListaNumero(p[1],p[3],p.lineno(1),find_column2(p.lexer.lexdata,p,1))

def p_error(p):
    global parser_error
    if (p is not None):
        msg = "Error de sintaxis. Se encontró token " + str(p.value) + " en la linea "
        msg += str(p.lineno - find_row2(p.lexer.lexdata)) + ", columna " + str(find_column(p.lexer.lexdata,p))
    else:
        msg = "Error de sintaxis al final del archivo"
    print msg
    parser_error = True

def iserror():
    global parser_error
    return parser_error

def find_row(input):
    nro_linea = 0
    with open(input,'r') as archivo:
        for linea in archivo:
            nro_linea += 1
    return nro_linea

def find_row2(input):
    row = input.count('\n')
    return row  

# Permite encontrar el numero de columna de la linea actual
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column 

def find_column2(input,token,nro):
    last_cr = input.rfind('\n',0,token.lexpos(nro))
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos(nro) - last_cr
    return column 

global parser_error
parser_error = False