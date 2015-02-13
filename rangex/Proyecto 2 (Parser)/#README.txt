CI3725 - Entrega 2 Grupo 7.
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285

Parser de RangeX

Utilizando la entrega 1 del proyecto, a la cuál le hicimos una pequeña
modificación para que chequeara Overflow al encontrar un entero
(cosa que se nos olvidó para la primera entrega).

Usamos la herramienta YACC de PLY (Python Lex Yacc).

Primero escribimos una gramática que reconociera el lenguaje RangeX y
la pusimos en los términos que pide la herramienta, por lo menos, dándole
precedencia a operadores de expresiones.

El programa, de ser correcto, es representado en un árbol sintáctico, cuyas
clases están definidas en el archvio 'ast.py'.

El Parser funciona como esperado.

Al correr "./rangex <archivo.rgx>" pueden suceder tres cosas:
  - Imprime en pantalla todos los errores de Overflow o Caracteres inesperados,
    encontrados con el Lexer.
  - Si pasa el Lexer sin problemas, pasará el Parser, donde al conseguir algún
    error lo imprimirá en pantalla.
  - Si no hay errores de ningún tipo imprime el árbol sintáctico en pantalla.
