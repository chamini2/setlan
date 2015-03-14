# -*- coding: utf-8 -*-'''
'''
Created on 21/2/2015

@author: Manuel Gonzalez 11-10390
         Jonathan Ng 11-10199
        
    Tabla de simbolos
'''

class SymbolTable:
    '''
     Administrador de una tabla de simbolos
    '''
    def __init__(self):
        '''
         Inicializa la tabla de contexto y la lista de errores.
        '''
        self.tableStack = [] # Pila de tablas (diccionarios)
        self.str = ""
        
    def add_scope(self):
        level = len(self.tableStack) # Nivel de alcance
        cad_indent = "   "*level
        self.str+= cad_indent + "SCOPE" + "\n"
        
        table = {} # Crea una tabla de simbolos para el nuevo alcance
        self.tableStack.append(table) # Empilar nueva tabla de simbolo
        
    def delete_scope(self):
        ''' Elimina el alcance actual (tope de la pila)'''
        self.tableStack.pop()
        
        level = len(self.tableStack) # Nivel de alcance
        cad_indent = "   "*level
        self.str+= cad_indent + "END_SCOPE" + "\n"
        
    def insert(self, name, data_type, type_edit, ref = None):
        'Inserta un simbolo en la tabla'
        table = self.tableStack[-1] # Obtenemos tope de la pila
        var = Symbol(name, data_type, type_edit, ref)
        table[name] = var
        
        #Impresion para el alcance
        level = len(self.tableStack) # Nivel de alcance
        cad_indent = "   "*level
        salida = ""
        salida += "Variable: " + var.name
        salida += " | Type: " + var.type 
        salida += " | Value: "
        if var.type == "int" or var.type == "bool":
            salida += str(var.value)
        elif var.type == "set":
            salida += "{"
            for i,value in enumerate(var.value):
                salida += str(value)
                if i != len(var.value) - 1:
                    salida += ","
            salida += "}"
            
        self.str+= cad_indent + salida + "\n" 
        
    def delete(self,name , context):
        'Borra un elemento de la tabla'
        pass
    
    def update(self, name, value):
        symbol = self.lookup(name)
        if symbol is None:
            print "No se encontro la variable "+name+" para este alcance"
            return 
        
        symbol.value = value
            
    def contains(self, name):
        'Verifica si una variable se encuentra en el alcance actual de la tabla'
        table = self.tableStack[-1]
        return name in table.keys()
        
    def lookup(self, name):
        '''
        Verifica que una variable se encuentra en el alcance actual o superior
        Devuelve el simbolo si se consigue, None en caso de que no se encuentre
        '''
        # Recorre la lista desde el final (Tope de la pila) hasta el inicio
        for table in self.tableStack[::-1]: 
            if name in table.keys():
                return table[name]
        
        return None # Retorna None en caso de no conseguir la variable
          
class Symbol:
    # Lista de valores por defecto para cada tipo
    default_list = {"int"  : 0, 
                    "bool" : False, 
                    "set"  : set() }
    
    def __init__(self, name, data_type, type_edit = "i/o", ref=None):
        self.name = name
        self.type = data_type
        self.value = Symbol.default_list[data_type]
        self.type_edit = type_edit
        self.ref = ref
