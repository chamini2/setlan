class SymbolTable(object):
    def __init__(self):
        self.scope = dict()


    def insert(self, var):
        if not self.contains(var.name): self.scope[var.name] = var


    def delete(self, name):
        if self.contains(name): self.scope.pop(name)


    def update(scopes_list, old_varname, new_var):
        for scope in scopes_list[::-1]:
            if scope.contains(old_varname):
                scope.delete(old_varname)
                scope[new_var.name] = new_var
                break


    def contains(self, name):
        return name in self.scope.keys()


    def lookup(self, name):
        return self.scope[name] if self.contains(name) else None