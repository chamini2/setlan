========================================
==      Proyecto I - CI3725  (Lexer)  ==
==      Luis Colorado 09-11086        ==
==      Nicolas Manan 06-39883        ==
==      Grupo 02                      ==
========================================

Descripci�n del proyecto

Se utiliz� python con la herramienta Lex para facilitar la implementacion

Se cre� un diccionario con las palabras reservadas del lenguaje que ser revisaran
al momento de validar un token. En la lista de tokens se guardan los strings reservados 
que estan conformados por letras y simbolos que tienen un significado especial en el lenguaje.
Ademas se especifican los caracteres que el lenguaje hace caso omiso (espacios, tabulaciones y comentarios).

La funci�n main recibe el c�digo a leer y devuelve una lista con los tokens encontrados, en caso de que consiga errores imprimira por pantalla el error conseguido en la linea y columna. 


=============================
==                         ==
==  Ejecuci�n del programa ==
==                         ==
=============================
Para correr el programa hay que cambiar los permisos del codigo con el comando:
    $sudo chmod a+x setlan

Luego ejecutar en el terminal
    $./setlan <input.stl>
