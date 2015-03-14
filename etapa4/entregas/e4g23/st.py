import config

def get_var_in_scope(var_name):
    for symbol_table in config.scopes_list[::-1]:
        var = symbol_table.lookup(var_name)
        if var: return var
    return None


class SymbolTable(object):
    def __init__(self):
        self.scope = dict()


    def insert(self, var):
        if not self.contains(var.name): self.scope[var.name] = var


    def delete(self, name):
        if self.contains(name): self.scope.pop(name)


    def contains(self, name):
        return name in self.scope.keys()


    @classmethod
    def update(self, var_name, value):
        var = get_var_in_scope(var_name)
        var.value = value


    def lookup(self, name):
        return self.scope[name] if self.contains(name) else None