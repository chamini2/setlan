#!/usr/bin/env python
# -*- coding: UTF-8 -*-
defaults = {'int':0,'bool':False,'set':set()}

class symbolTable:
  def __init__(self,Padre):
    self.padre = Padre
    self.elems = []
    self.subT = []
  def resetLocal(self):
    for x in self.elems:
      x[2] = defaults[x[1]]
  def insert(self, In):
    self.elems.append(In)
  def insertT(self, In):
    self.subT.append(In)
  def delete(self, Out):
    for x in self.elems:
      if (x[0] == Out):
        self.elems.remove(x)
        break
  def localforceupdate(self, In,value):#solo usado por el for
    for x in self.elems:
      if (x[0] == In):
        x[2] = value
  def update(self, In,value):
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