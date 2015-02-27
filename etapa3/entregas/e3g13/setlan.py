#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 23/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
         
         Archivo principal de Setlan
         Para Ejecutar:  setlan <nombre archivo> <flags>
         Flags: -
'''
from  sys import argv as argumentos_consola
import expresiones
import parse
import ply.lex as lexi

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
            expresiones.cont_archivo = content
    except IOError as e :
        salir(str(e) + "\nError: Compruebe que el archivo existe o tiene permisos de lectura")
        
    lexer = expresiones.build_lexer()           # Construir Lexer
    tree = parse.build_parser(content,lexer) # Contruimos el Parser
    # Impresion de errores
    if expresiones.lexer_errors:
        for error in expresiones.lexer_errors:
            print error
        
    elif parse.parser_errors:
        for error in parse.parser_errors:
            print error
    else:
        if "-t" in argv:
            print "####################       LISTA DE TOKENS      ####################\n" 
            expresiones.print_tokens(expresiones.build_lexer(), content)
        
        if "-a" in argv:
            print "\n#################### ARBOL SINTACTICO ABSTRACTO ####################\n" 
            tree.print_tree()
        
        if "-s" in argv:
            print "\n####################      CHEQUEO DE TIPOS       ####################\n" 
            tree.fetch_symbols()
            tree.check_types()
            
        if tree.symbols.errors:
            for error in tree.symbols.errors:
                print "Error en la linea %d, columna %d: %s" % \
                       (error[0],expresiones.obtener_columna_texto_lexpos(error[1]),error[2])
        else:
            tree.symbols.print_context(0,0)

def salir(mensaje = "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo> [-t] [-a] [-s]",
                codigo = -1):
    print mensaje
    exit(codigo)    
             
if __name__ == '__main__':
    setlan()