#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 23/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
         
         Archivo principal de Setlan

Para Ejecutar:  setlan <nombre archivo> <flags>

Flags:
    -t Imprime la lista de tokens del analizador lexicografico
    -a Imprime la estructura del Arbol de Sintaxis Abstracto
    -s Imprime las reglas de alcance de las variables, asi como sus tipos y valores
'''
from  sys import argv as argumentos_consola
from AST import static_errors, interpreter_result
import expressions
import parse

def setlan(argv = None):
    # Abrir ruta del archivo   
    if argv is None:
        argv = argumentos_consola
    
    if len(argv) < 2:
        salir()
     
    ruta_archivo = argv[1]
    try:
        with open(ruta_archivo) as file_input:
            content = file_input.read()
            content = content.expandtabs(4)
            expressions.cont_archivo = content
    except IOError as e :
        salir(str(e) + "\nError: Compruebe que el archivo existe o tiene permisos de lectura")
        
    lexer = expressions.build_lexer()           # Construir Lexer
    tree = parse.build_parser(content,lexer) # Contruimos el parser
    
    # Impresion de errores
    if expressions.lexer_errors:
        for error in expressions.lexer_errors:
            print error
        return
        
    elif parse.parser_errors:
        for error in parse.parser_errors:
            print error
        return
    
    else: # Pasa el lexer y el parserr
        tree.check_types() # Hacemos el chequeo estatico 
        # Impresion de errores
        if static_errors:
            for error in static_errors:
                print error
            return
    
    # Flags   
    if "-t" in argv:
        print "####################       LISTA DE TOKENS      ####################\n"
        # Construir el lexer denuevo, ya que el parser cambia el n° de lineas 
        expressions.print_tokens(expressions.build_lexer(), content) 
        print
    
    if "-a" in argv:
        print "\n#################### ARBOL SINTACTICO ABSTRACTO ####################\n" 
        tree.print_tree()
        print
        
    if "-s" in argv:
        print "\n####################      CHEQUEO DE TIPOS       ####################\n" 
        print tree.symbolTable.str
        print
        
    tree.execute() # Ejecutar el interpretador
    result = "".join(interpreter_result)
    return result

def salir(mensage = "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo> [-t] [-a] [-s]",
                code = -1):
    print mensage
    exit(code)
             
if __name__ == '__main__':
    setlan()
