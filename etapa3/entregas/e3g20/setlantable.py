#!/usr/bin/env python
# -*- coding: UTF-8 -*-
defaults = {'int':0,'bool':'false','set':'{}'}

class symbolTable:
  def __init__(self,Padre):
    self.padre = Padre
    self.elems = []
    self.subT = []
  def insert(self, In):
    self.elems.append(In)
  def insertT(self, In):
    self.subT.append(In)
  def delete(self, Out):
    for x in self.elems:
      if (x[0] == Out):
        self.elems.remove(x)
        break
  def update(In,value): #esto no se pa que sirve, no se como implementarlo, no se indica que debe de hacer precisamente
    for x in self.elems:
      if (x[0] == In):
        if (x[3]):
          x[2] = value
          return True
        else:
          return False
    if (self.padre == None):
      return False
    else:
      return self.padre.update(In,value)
  def contains(self, In):
    for x in self.elems:
      if (x[0] == In):
        return True
    if (self.padre == None):
      return False
    else:
      return self.padre.contains(In)
  def lookup(self, In):
    for x in self.elems:
      if (x[0] == In):
        return x
    if (self.padre == None):
      return None
    else:
      return self.padre.lookup(In)
  def local_contains(self, In):
    for x in self.elems:
      if (x[0] == In):
        return True
    return False
  def tablePrint(self, num):
    print (" "*num)+"SCOPE"
    for x in self.elems:
      print (" "*(num+2))+str(x)
    for x in self.subT:
      x.tablePrint(num+2)
    print (" "*num)+"END_SCOPE"