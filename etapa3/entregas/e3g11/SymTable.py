############################################################################
#Sanchez Jesus 10-10898
#Barrientos Jose 10-10800
############################################################################
#Clase Atributos, permitira crear tuplas tipo-valor, que seran los atributos
#para las claves en la tabla de simbolos.
class Atributos:

    def __init__(self,tipo,valor):
        self.tipo=tipo
        self.valor=valor

    def __str__(self):
        return str(self.tipo)

    def setTipo(self,tipo):
        self.tipo=tipo

    def setValor(self,valor):
        self.valor=valor

    def esTipoVacio(self):
        return self.tipo==''

    def esValorVacio(self):
        return self.valor==''

    def getTipo(self):
        return self.tipo

    def getValor(self):
        return self.valor	

############################################################################

#clase SymTable, permite la creacion de una tabla (diccionario en python)
# y sus respectivas operaciones todas recursivas por la forma en que se 
#implemento el proyecto.

# Todas las funciones que comienzan por aux_x tienen la misma funcionalidad
#que x pero son aplicadas para las tablas relacionadas con los FOR.

class SymTable:
    def __init__(self):
        self.tstack={}

    def insert(self,clave,valor):
        if self.tstack.has_key('1'):
            aux = self.tstack['1']
            aux.insert(clave,valor)
        else:
            self.tstack[clave]=valor

    def aux_insert(self,clave,valor):
        if self.tstack.has_key('2'):
            aux = self.tstack['2']
            aux.aux_insert(clave,valor)
        else:
            self.tstack[clave]=valor


    def delete(self):
        if self.tstack.has_key('1'):
            aux = self.tstack['1']
            if aux.tstack.has_key('1'):
                aux.delete()
            else:
                del self.tstack['1']
        else:
            self.tstack={}

    def aux_delete(self):
        if self.tstack.has_key('2'):
            aux = self.tstack['2']
            if aux.tstack.has_key('2'):
                aux.aux_delete()
            else:
                del self.tstack['2']
        else:
            self.tstack={}

    def update(self,clave,valor):
        booleano=False
        if self.tstack.has_key('1'):
            booleano= self.tstack['1'].update(clave,valor)
        else:
            if not(booleano) and self.tstack.has_key(clave):
                self.tstack[clave] = valor	
                booleano= True
        return booleano		

    def isMember(self,clave):
        if self.tstack.has_key(clave):
            return True 
        else:
            if self.tstack.has_key('1'):
                return self.tstack['1'].isMember(clave)
            else:
                return False

    def aux_isMember(self,clave):
        if self.tstack.has_key(clave):
            return True 
        else:
            if self.tstack.has_key('2'):
                return self.tstack['2'].aux_isMember(clave)
            else:
                return False
            
    def deepestMember(self,clave):
        
        booleano=False
        
        if self.tstack.has_key('1'):
            booleano=self.tstack['1'].deepestMember(clave)
            
        else:
            if booleano:
                return True 
            elif self.tstack.has_key(clave):
                
                booleano= True 
            else:
                booleano=False
            
        return booleano	

    def aux_deepestMember(self,clave):
        booleano=False
        if self.tstack.has_key('2'):
            booleano=self.tstack['2'].aux_deepestMember(clave)

        else:
            if not(booleano) and self.tstack.has_key(clave):
                booleano= True 
            
        return booleano		

    def find(self,clave):
        p=''
        if self.tstack.has_key('1'):
            p= self.tstack['1'].find(clave)
        if p != '':
            return p
        else:
            try:
                return self.tstack[clave]		
            except KeyError:
                return p

    def aux_find(self,clave):
        p=''
        if self.tstack.has_key('2'):
            p= self.tstack['2'].aux_find(clave)
        if p != '':
            return p
        else:
            try:
                return self.tstack[clave]		
            except KeyError:
                return p

    def hay_iter(self):
        return self.tstack.has_key('2')

    def __str__(self,indentar):
        result=""
        if (self.tstack.has_key("1")):
            result= self.tstack['1'].__str__(indentar)	
        else:
            for x,y in self.tstack.items():
                if (x!='2'):
                    ini=''
                    if(str(y)=='bool'):
                        ini='false'
                    elif(str(y)=='int'):
                        ini='0'
                    else:
                        ini='{}'
                        
                    result+=indentar+"variable: "+x+" | tipo: "+str(y)+" | valor: "+ini+"\n"
        return result
            
    def getKey(self,valor):
        for x,y in self.tstack.items():
            if y==valor:
                return x