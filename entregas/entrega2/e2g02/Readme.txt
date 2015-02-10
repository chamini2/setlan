========================================
==      Proyecto II - CI3725  (Parser)==
==      Luis Colorado 09-11086        ==
==      Nicolas Manan 06-39883        ==
==      Grupo 02                      ==
========================================

Descripción del proyecto

Se utilizo la herramienta YACC de PLY (Python Lex Yacc)
para facilitar la implementacion

Para el desarrollo de el parser se escribio una gramatica que
reconociera el lenguaje Setlan, como se muestra en el archivo
GramaticaSetlan.txt.

De ser correcto el codigo leido, se representa en un arbol 
abstracto sintactico (ast).

=============================
==                         ==
==  Ejecución del programa ==
==                         ==
=============================

Para ejecutar el proyecto correr en el terminal:
	$./setlan <input.stl>


=============================
==                         ==
==  Problemas Encontrados  ==
==                         ==
=============================

Al ejecutar el programa al principio muetsra un WARNING
indicando que la regla t_error no esta definida

"WARNING: No t_error rule is defined "

Advertencia que no pudimos solventar.

EL codigo a evaluar puede no correr con ciertos ';' (punto y coma)
la verdad no nos quedo claro cuando podia, o no, haber esta puntuacion,
no solventamos la duda a tiempo por lo que no esta reflejado su uso en la gramatica,
"""para ciertos casos."""

ejemplo caso que no corre:

if (3<9)
{
	print " No proceso el signo :( "; 
}

Caso 2

<cualquier cosa> };   <- Error con el signo despues de corchete

Cualquier otro caso deberia estar bien programado.











