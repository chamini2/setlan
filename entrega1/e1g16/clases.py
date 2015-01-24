# Proyecto 1.
# Tradutores
# Grupo 16
# Betzabeh Gonzalez Canonico: 08-10462
# Andel Nunez 08-10804

import sys

#Clase Token
class Token:
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = code

#Clases para palabras reservadas
class TokenProgram(Token):
    def __init__(self, line, col,code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenScan(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenPrint(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenPrintln(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenUsing(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenIn(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenIf(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       
        
class TokenElse(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenFor(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenDo(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenWhile(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenRepeat(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None  

class TokenInt(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenBool(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenSet(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenMin(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenMax(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenTrue(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenFalse(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenNot(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None

class TokenAnd(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenOr(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenNot(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None   

class TokenContenCjto(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None    

class TokenIgual(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenDesigual(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenMenor(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenMenorIgual(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenMayor(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None        

class TokenMayorIgual(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None        

class TokenMult(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None        

class TokenDivision(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None        

class TokenResto(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None    

class TokenSuma(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenResta(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None

class TokenNegEnteros(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenUnion(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenDiferencia(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenInterseccion(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenSumaCjto(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenRestaCjto(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenMultCjto(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenDivisionCjto(Token):
    def __init__(self, line, col,  code):
        self.line = line
        self.col  = col
        self.code = None

class TokenRestoCjto(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None

class TokenDosPuntos(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None     

class TokenPuntoYComa(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenParAbre(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenParCierra(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenComa(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenAsignacion(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None       

class TokenLlaveAbre(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None    

class TokenLlaveCier(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenString(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = None      

class TokenIdent(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = code

class TokenNum(Token):
    def __init__(self, line, col, code):
        self.line = line
        self.col  = col
        self.code = code
