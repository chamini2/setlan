NOMBRE : Analizador lexicografico para Setlan
MATERIA: CI3725 - Traductores e Interpretadores
AUTORES: Aldrix Marfil     #10-10940
         Leonardo Martinez #11-10576
GRUPO  : 7

ULT. MODIFICACION: 23/01/2015

ESTADO ACTUAL DEL PROYECTO: Completado

IMPORTANTE:
    Antes de ejecutar se deben activar todos los permisos para el archivo de 
    texto que contiene las instrucciones del lenguaje. Puede ser escribiendo lo
    siguiente en la terminal:
    
    chmod 777 setlan

PARA EJECUTAR:
    Se debe colocar en la terminal: ./setlan Nombre_archivo.stl

DETALLES:
    Se programa el lexer bajo el entorno de linux usando Python version 2.7 con 
    un modulo llamado PLY en su version 3.4. Se usa especificamente el lexer.

DESICIONES DE IMPLEMENTACION:
    Se usa un diccionario de datos para las palabras que son reservadas y una
    lista de tokens para las palabras a ser reconocidas. Se reconocen dichas 
    palabras no reservadas mediante reglas definidas por expresiones regulares.
    
    Se implementa el Lexer basando en lo explicado en la documentacion.
