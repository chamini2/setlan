NOMBRE : Interpretador con verificaciones dinámicas
MATERIA: CI3725 - Traductores e Interpretadores
AUTORES: Aldrix Marfil     #10-10940
         Leonardo Martinez #11-10576
GRUPO  : 7

ULT. MODIFICACION: 08/03/2015

ESTADO ACTUAL DEL PROYECTO: Completado

PARA EJECUTAR:
    Se debe colocar en la terminal: ./setlan Nombre_archivo.stl -flag
    
    donde flag es: -t para mostrar los tokens del lexer
                   -a para mostrar el arbol sintactico
                   -s para mostrar la tabla de simbolos

    Antes de ejecutar se deben activar todos los permisos para el archivo de 
    texto que contiene las instrucciones del lenguaje. Puede ser escribiendo lo
    siguiente en la terminal:
    
    chmod 777 setlan

IMPORTANTE:
    - Se unifico la funcion execute con evaluate.
    - Si reporta los siguientes errores:
                  - Errores de división por cero.
                  - Errores de overflow.
                  - Errores de máximo y mínimo elemento de un conjunto vacío.

DETALLES: 
    Se programa el parser y el lexer bajo el entorno de linux usando Python 
    version 2.7 con un modulo llamado PLY en su version 3.4. 
