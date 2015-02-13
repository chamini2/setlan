CI3725 - Entrega 4 Grupo 7.
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285

Parser de RangeX

Para este proyecto nos basamos en el código de la entrega pasada y la
modificamos para lograr las capacidades pedidas para esta entrega.

Se modificó constructores del AST.

Usamos la herramienta YACC de PLY (Python Lex-Yacc).

El programa, de pasar todas las verificaciones de lexer, parser y estáticas,
corre normalmente, si consigue algún error dinámico, lo reporta y termina la
ejecución.

El proyecto funciona como esperado.

Reporta errores dinámicos para:
  - overflow en operaciones.
  - división por cero.
  - rangos vacios

Chequea la entrada del usuario para:
  - entrada con formato válido
  - overflow en entrada
