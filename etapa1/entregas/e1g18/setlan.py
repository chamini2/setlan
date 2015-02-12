#!/usr/bin/python
'''
Created on 22/1/2015

@author: Emmanuel De Aguiar     10-10179
@author: Daniel Pelayo          10-10539

'''
import lexer
import sys

def main():
    if (len(sys.argv) > 1):
        lexer.analisisLexicoGrafico(sys.argv[1])
    else:
        print 'No se pudo hacer el analisis lexicografico. Para ejecutar un archivo en SetLan recuerde usar\
: $./setlan.py <nombrearchivo>.stl'
    
if __name__ == '__main__':
    main()