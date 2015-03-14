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
        return str(self.tipo)+" --- "+str(self.valor)
    
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
        
        if(self.tipo=='int' and self.valor==''):
            self.valor = '0'
        elif(self.tipo=='bool' and self.valor==''):
            self.valor = 'false'
        elif(self.tipo=='set' and self.valor==''):
            self.valor = '{}'
            
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
        if self.tstack.has_key('0'):
            aux = self.tstack['0']
            aux.insert(clave,valor)
        else:
            self.tstack[clave]=valor
            

    def aux_insert(self,clave,valor):
        if self.tstack.has_key('1'):
            aux = self.tstack['1']
            aux.aux_insert(clave,valor)
        else:
            self.tstack[clave]=valor
            

    def delete(self):
        if self.tstack.has_key('0'):
            aux = self.tstack['0']
            if aux.tstack.has_key('0'):
                aux.delete()
            else:
                del self.tstack['0']
        else:
            self.tstack={}

    def aux_delete(self):
        if self.tstack.has_key('1'):
            aux = self.tstack['1']
            if aux.tstack.has_key('1'):
                aux.aux_delete()
            else:
                del self.tstack['1']
        else:
            self.tstack={}
    #revisar                
    def update(self,clave,valor):
        booleano=False
        
        if self.tstack.has_key('0'):
            
            booleano= self.tstack['0'].update(clave,valor)  
        if not(booleano) and self.tstack.has_key(clave):            
            aux=self.tstack[clave]
            tmp= aux.getTipo()
            a=Atributos(tmp,valor)
            self.tstack[clave]=a
            booleano= True
        return booleano

    def aux_update(self,clave,valor):
        booleano=False
        if self.tstack.has_key('1'):
            booleano= self.tstack['1'].aux_update(clave,valor)
        
        if not(booleano) and self.tstack.has_key(clave):
            self.tstack[clave].setValor(valor)
            #print str(self.tstack[clave])  
            booleano= True
        return booleano 

    def isMember(self,clave):
        if self.tstack.has_key(clave):
            return True 
        else:
            if self.tstack.has_key('0'):
                return self.tstack['0'].isMember(clave)
            else:
                return False

    def aux_isMember(self,clave):
        if self.tstack.has_key(clave):
            return True 
        else:
            if self.tstack.has_key('1'):
                return self.tstack['1'].aux_isMember(clave)
            else:
                return False
    
    #busca el elemento mas interno en los bloques.
    def deepestMember_aux(self,clave):      
        booleano=False
        if self.tstack.has_key('0'):
            booleano=self.tstack['0'].deepestMember_aux(clave)          
        if booleano:
            return True 
        elif self.tstack.has_key(clave):                
            booleano= True 
        else:
            booleano=False          
        return booleano 
    #busca en si esta o no en el bloque mas interno.
    def deepestMember_aux2(self,clave):     
        booleano=False
        if self.tstack.has_key('0'):
            booleano=self.tstack['0'].deepestMember_aux2(clave)
        else:   
            if booleano:
                return True 
            elif self.tstack.has_key(clave):                
                booleano= True 
            else:
                booleano=False          
        return booleano 

    def buscar(self,inicio,fin):        
        result=''
        tmp=inicio
        while tmp<=fin:
            if self.tstack.has_key(tmp):
                return self
            else:
                tmp+=1
        if self.tstack.has_key('0'):
            result=self.tstack['0'].buscar(inicio,fin)
        
        if result!='':
            return result 
        else:
            result=''           
        return result   

    def perteneceCiclos(self,clave,numCiclo):       
        ciclo=2
        aux=numCiclo+1  
        if self.tstack.has_key('1'):
            ciclo=self.tstack['1'].perteneceCiclos(clave,aux)           
        if ciclo!=2:
            return ciclo 
        elif self.tstack.has_key(clave) and self.tstack.has_key(numCiclo):              
            ciclo=numCiclo
        else:
            ciclo=2         
        return ciclo

    def find(self,clave):
        p=''
        if self.tstack.has_key('0'):
            p= self.tstack['0'].find(clave)
        if p != '':
            return p
        else:
            try:
                return self.tstack[clave]       
            except KeyError:
                return p

    def aux_find(self,clave):
        p=''
        if self.tstack.has_key('1'):
            p= self.tstack['1'].aux_find(clave)
        if p != '':
            return p
        else:
            try:
                return self.tstack[clave]       
            except KeyError:
                return p

    def hay_iter(self):
        return self.tstack.has_key('1')

    def __str__(self,indentar):
        result=""
        if (self.tstack.has_key("0")):
            result= self.tstack['0'].__str__(indentar)	
        else:
            for x,y in self.tstack.items():
                if (x!='1'):
                    ini=''
                    if(str(y)=='bool'):
                        ini='false'
                    elif(str(y)=='int'):
                        ini='0'
                    else:
                        ini='{}'
                        
                    result+=indentar+"variable: "+str(x)+" | tipo: "+str(y)+" | valor: "+ini+"\n"
        return result
            
    def getKey(self,valor):
        for x,y in self.tstack.items():
            if y==valor:
                return x