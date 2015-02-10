# -*- coding: utf-8 -*-

## Interpretador del lenguaje Setlan.
## Árbol Sintáctico Abstracto (AST)
## Autores:  - Mónica Figuera   11-10328
##           - Carlos Spaggiari 11-10987

operator = { "+" : "PLUS", "-" : "MINUS", "*" : "TIMES",
			"/" : "DIVIDE", "%" : "MODULE", "and" : "AND",
			"or" : "OR", "<" : "LESSTHAN",">" : "GREATERTHAN",
			"<=" : "LESSEQUALSTHAN",">=" : "GREATEREQUALTHAN",
			"@" : "BELONGSTO", "not" : "NOT", "++":"SETUNION",
			"==" : "EQUALS","/=" : "NOTEQUALS","\\" : "SETDIFF", 
			"><" : "SETINTERSECT", "<+>" : "SETMAPPLUS",
			"<->" : "SETMAPMINUS", "<*>" : "SETMAPTIMES", 
			"</>" : "SETMAPDIVIDE", "<%>" : "SETMAPMODULE", 
			">?" : "SETMAXVALUE", "<?" : "SETMINVALUE",
			"$?" : "SETSIZE"}

def indent(tabs):
	return "   "*tabs

class Program:
	def __init__(self,declarations="",instruction=""):
		self.declarations = declarations
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"PROGRAM\n"
		string += self.instruction.printTree(tabs+1)
		return string


class Instruction:
	def __init__(self,instruction = "",Id="",assign="",expression=""):
		self.instruction = instruction
		self.id = Id
		self.assign = assign
		self.expression = expression

	def printTree(self,tabs):
		string =""
		if self.assign == "":
			if isinstance(self.instruction, str):
				string += indent(tabs)+self.instruction
			else:
				string += self.instruction.printTree(tabs)
		else:
			string += indent(tabs)+"ASSIGN\n"
			string += self.id.printTree(tabs+1) 
			string += indent(tabs+1)+"value\n"
			string += self.expression.printTree(tabs+2)
		return string 


class Block:
	def __init__(self,lcurly, instructionBlock,rcurly):
		self.rcurly = rcurly
		self.lcurly = lcurly
		self.instructionBlock = instructionBlock

	def printTree(self,tabs):
		string  = indent(tabs)+"BLOCK\n"
		string += self.instructionBlock.printTree(tabs+1)
		string += indent(tabs)+"BLOCK_END\n"
		return string


class UsingInInst:
	def __init__(self,Using,declaration,In,instruction):
		self.Using = Using
		self.declaration = declaration
		self.In = In
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"USING\n"
		string += self.declaration.printTree(tabs+1)
		string += indent(tabs)+"IN\n"
		string += self.instruction.printTree(tabs+1)
		return string


class DeclarationBlock:
	def __init__(self,varType,Id,semicolon,declaration=""):
		self.varType = varType
		self.Id = Id
		self.semicolon = semicolon
		self.declaration = declaration

	def printTree(self,tabs):
		string = ""
		string += self.Id.printTree(tabs,self.varType)
		if isinstance(self.declaration, str):
			if self.declaration != "":
				string += indent(tabs)+self.declaration
		else:
			string += self.declaration.printTree(tabs)
		return string

		
class Type:
	def __init__(self,type):
		self.type = type

	def printTree(self,tabs):
		string = indent(tabs)+self.type
		return string


class ID:
	def __init__(self,value,comma="",IDrecursion=""):
		self.type = 'id'
		self.value = value
		self.IDrecursion = IDrecursion

	def printTree(self,tabs,varType=None):
		string = ""
		if varType:
			string += varType.printTree(tabs)
			string += " "+self.value+"\n"
		else:
			string += indent(tabs)+"variable\n"
			string += indent(tabs+1)+self.value+"\n"
		if not isinstance(self.IDrecursion,str):
			string += self.IDrecursion.printTree(tabs,varType)
		return string 


class InstructionBlock:
	def __init__(self,instruction="",semicolon="",instructionBlock=""):
		self.instruction = instruction
		self.semicolon = semicolon
		self.instructionBlock = instructionBlock

	def printTree(self,tabs):
		string = ""
		if self.instruction != "":
			string += self.instruction.printTree(tabs)
			if isinstance(self.instructionBlock, str):
				string += indent(tabs)+self.instructionBlock
			else:
				string += self.instructionBlock.printTree(tabs)
		return string


class IfInst:
	def __init__(self, If, lparen, expression, rparen, instruction, Else="", elseInstruction=""):
		self.If = If
		self.lparen = lparen
		self.expression = expression
		self.rparen = rparen
		self.instruction = instruction
		self.Else = Else
		self.elseInstruction = elseInstruction

	def printTree(self, tabs):
		string = indent(tabs)+"IF\n"
		string += indent(tabs+1)+"condition\n"
		string += self.expression.printTree(tabs+2)
		string += indent(tabs+1)+"THEN\n"
		string += self.instruction.printTree(tabs+2)
		if (self.Else != ""):
			string += indent(tabs)+"ELSE\n"
			string += self.elseInstruction.printTree(tabs+1)
		return string


class ForInst:
	def __init__(self,For,Id,Dir,Set,Do,instruction):
		self.For = For
		self.id = Id
		self.dir = Dir
		self.set = Set
		self.Do = Do
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"FOR\n"
		string += self.id.printTree(tabs+1)
		string += self.dir.printTree(tabs+1)
		string += indent(tabs+1)+"IN\n"
		string += self.set.printTree(tabs+1)
		string += indent(tabs+1)+"DO\n"
		string += self.instruction.printTree(tabs+2)
		return string


class Direction:
	def __init__(self,direction):
		self.direction = direction

	def printTree(self,tabs):
		string = indent(tabs)+"DIRECTION\n"
		string += indent(tabs+1)+self.direction+"\n"
		return string


class WhileInst:
	def __init__(self,While,lparen,expression,rparen,Do="",instruction=""):
		self.While = While
		self.expression = expression
		self.Do = Do
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"WHILE\n"
		string += indent(tabs+1)+"condition\n"
		string += self.expression.printTree(tabs+2)
		if not isinstance(self.instruction,str):
			string += indent(tabs)+"DO\n"
			string += self.instruction.printTree(tabs+1)
		return string


class RepeatInst:
	def __init__(self,repeat,instruction,While):
		self.While = While
		self.repeat = repeat
		self.instruction = instruction

	def printTree(self,tabs):
		string = indent(tabs)+"REPEAT\n"
		string += self.instruction.printTree(tabs+1)
		string += self.While.printTree(tabs)
		return string


class ScanInst:
	def __init__(self,scan,expression):
		self.scan = scan
		self.expression = expression

	def printTree(self,tabs):
		string = indent(tabs)+"SCAN\n"
		string += self.expression.printTree(tabs+1)
		return string


class PrintInst:
	def __init__(self,Print,output):
		self.Print = Print
		self.output = output

	def printTree(self,tabs):
		string = indent(tabs)+"PRINT"+"\n"
		string += indent(tabs+1)+"elements\n"
		string += self.output.printTree(tabs+2)
		if (self.Print == "println"):
			string += String("\"\\n\"").printTree(tabs+2)
		return string


class OutputType:
	def __init__(self,expression,comma="",outputRecursion=""):
		self.expression = expression
		self.comma = comma
		self.outputRecursion = outputRecursion

	def printTree(self,tabs):
		string = self.expression.printTree(tabs)
		if not isinstance(self.outputRecursion,str):
			string += self.outputRecursion.printTree(tabs)
		return string


class String:
	def __init__(self,string):
		self.string = string

	def printTree(self,tabs):
		string = indent(tabs)+"string\n"
		string += indent(tabs+1)+self.string+"\n"
		return string


class Expression:
    def __init__(self,left,op="",right=""):
        self.type  = "expression"
        self.left  = left
        self.right = right
        self.op    = op

    def printTree(self,tabs):
    	string = ""
    	if self.op != "":
    		if self.right == "":
    			if self.op == '-':
    				string += indent(tabs)+"NEGATE"+" "+self.op+"\n"
    			else:
	    			string += indent(tabs)+operator[self.op]+" "+self.op+"\n"
	    		string += self.left.printTree(tabs+1)
	    	else:
	    		if self.left == "(" and self.right == ")":
	    			string += self.op.printTree(tabs)
		    	else:
		    		string += indent(tabs)+operator[self.op]+" "+self.op+"\n"
		    		string += self.left.printTree(tabs+1)
		    		string += self.right.printTree(tabs+1)
    	else:
    		if isinstance(self.left, str):
    			string += self.left
    		else:
    			string += self.left.printTree(tabs)
    	return string


class Set:
	def __init__(self,lcurly,setNumbers,rcurly):
		self.lcurly = lcurly
		self.setNumbers = setNumbers
		self.rcurly = rcurly

	def printTree(self, tabs):
		string = indent(tabs)+"set\n"
		string += self.setNumbers.printTree(tabs+1)
		return string
		

class SetNumbers:
	def __init__(self, expression, comma="", setNumbersRecursion=""):
		self.expression = expression
		self.comma = comma
		self.setNumbersRecursion = setNumbersRecursion
		
	def printTree(self, tabs):
		string = self.expression.printTree(tabs)
		if not isinstance(self.setNumbersRecursion, str):
			string += self.setNumbersRecursion.printTree(tabs)
		return string


class BooleanValue:
	def __init__(self,value):
		self.value = value

	def printTree(self, tabs):
		string  = indent(tabs)+"bool\n"
		string += indent(tabs+1)+self.value+"\n"
		return string


class Number:
	def __init__(self,value):
		self.value = value

	def printTree(self,tabs):
		string  = indent(tabs)+"int\n"
		string += indent(tabs+1) + str(self.value) + "\n"
		return string
