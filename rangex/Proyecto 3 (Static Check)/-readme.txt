CI3725 - Entrega 3 Grupo 7.
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285

Parser de RangeX

Para este proyecto nos basamos en el código de la entrega pasada y la
modificamos para lograr las capacidades pedidas en para esta entrega.

Agregamos la restricción de que un STRING no es una expresión válida.

Se modificó constructores del AST y se hizo una clase SymTable para representar
un alcance en el programa.

Usamos la herramienta YACC de PLY (Python Lex-Yacc).

El programa, de ser correcto, es representado en un árbol sintáctico.

El proyecto funciona como esperado.

Reporta errores estáticos para:
  - Chequeo que una variable ya esté definida al momento de ser usada.
  - Chequeo de no declarar una variable dos veces en el mismo alcance.
  - Asignación de expresiones de un tipo a variables del mismo tipo.
  - Usar exclusivamente expresiones booleanas en un if.
  - Usar exclusivamente expresiones booleanas en un while.
  - Usar exclusivamente expresiones de entero en el principio de un case.
  - Usar exclusivamente expresiones de rango en los casos de un case.
  - Usar exclusivamente expresiones de rango en los casos de un case.
  - Usar exclusivamente expresiones de rango en el rango de un for.
  - No modificar la variable perteneciente a un for.
  - Hacer opraciones bonarias o unarias con tipos no permitidos, o uso indebido
    de funciones embebidas.
