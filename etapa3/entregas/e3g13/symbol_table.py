'''
Created on 21/2/2015

@author: Manuel Gonzalez 11-10390
         Jonathan Ng 11-10199
        
    Tabla de simbolos
'''

class SymbolTable():
    '''
     Administrador de una tabla de simbolos
    '''
    def __init__(self):
        '''
         Inicializa la tabla de contexto y la lista de errores.
        '''
        self.errors = []
        self.context_table = ContextTable()
    
    def insert(self,symbol):
        'Inserta un simbolo en la tabla'
        if self.context_table.exists(symbol.context):
            self.context_table.contexts[symbol.context]['vars'].append(symbol)
    
    def delete(self,name , context):
        'Borra un elemento de la tabla'
        if not self.context_table.exists(context): return None
        
        for symbol in self.context_table.contexts[context]['vars']:
            if symbol.name == name:
                self.context_table.contexts[context]['vars'].remove(symbol)
    
    def update(self,name,context,value):
        symbol = self.lookup(name, context)
        if symbol is None:
            return 
        
        symbol.value = value
            
    def contains(self,name,context):
        'Verifica si cone'
        if not self.context_table.exists(context): return None

        for symbol_t in self.context_table.contexts[context]['vars']:
            if symbol_t.name == name: return True
            
        return False
    
    def lookup(self,name,context):
        if not self.context_table.exists(context): return None

        for symbol_t in self.context_table.contexts[context]['vars']:
            if symbol_t.name == name:
                return symbol_t
        
        return self.lookup(name,self.context_table.contexts[context]['parent'])
    
    def add_context(self):
        return self.context_table.add()
    
    def add_child(self,context, child_context):
        return self.context_table.add_children(context, child_context)
    
    def print_context(self,context,level):
        
        if not self.context_table.exists(context):return
        
        if not self.context_table.contexts[context]['vars'] and \
           not self.context_table.contexts[context]['childs']:
            return
        cad_indent = "   "*level
        print cad_indent + "SCOPE"
        
        for var in self.context_table.contexts[context]['vars']:
            salida = "   "
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
                
            print cad_indent + salida

        for child in self.context_table.contexts[context]['childs']:
            self.print_context(child, level + 1)
            
        print cad_indent + "END_SCOPE"
    
    #Solo para probar no definitivo
    def append_error(self,sms):
        self.errors.append(sms)

class ContextTable:
    
    def __init__(self):
        self.contexts = {}
    
    def add(self):
        new_context = len(self.contexts)
        self.contexts[new_context] = {'vars':[],\
                                  'childs':[],
                                  'parent':-1}
        return new_context
    
    def exists(self,context):
        return context in self.contexts.keys()
    
    def add_children(self,context,child_context):
        if self.exists(context) and self.exists(child_context) and \
           context != child_context: # Para evitar recursion infinita
            self.contexts[context]['childs'].append(child_context)
            self.contexts[child_context]['parent'] = context
            
class Symbol:
    def __init__(self,name,type_s,value,context,type_edit = "i/o",ref=None):
        self.name = name
        self.type = type_s
        self.value = value
        self.context = context
        self.type_edit = type_edit
        self.ref = ref