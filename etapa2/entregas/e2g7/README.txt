NOMBRE : Analizador sintactico para Setlan
MATERIA: CI3725 - Traductores e Interpretadores
AUTORES: Aldrix Marfil     #10-10940
         Leonardo Martinez #11-10576
GRUPO  : 7

ULT. MODIFICACION: 08/02/2015

ESTADO ACTUAL DEL PROYECTO: Completado

PARA EJECUTAR:
    Se debe colocar en la terminal: ./setlan Nombre_archivo.stl
    
    Antes de ejecutar se deben activar todos los permisos para el archivo de 
    texto que contiene las instrucciones del lenguaje. Puede ser escribiendo lo
    siguiente en la terminal:
    
    chmod 777 setlan

IMPORTANTE:
    - Se anexa en un archivo de texto la gramatica definida para reconocer el
      lenguaje de programacion setlan.
    - El programa imprime None al final, pero no sabemos cual es la razon.

DETALLES: 
    Se programa el parser bajo el entorno de linux usando Python version 2.7 con
    un modulo llamado PLY en su version 3.4. Se usa especificamente el parser.

NOTA: Se implementa el Parser basado en la documentacion.
    
