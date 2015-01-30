- regex de strings está mal, *agarra* strings de una línea a la otra.
- regex de enteros está mal, *agarra* decimales (ejemplo: `3.14`), y números
en notación científica (ejemplo: `3.0e+2`)
- en varias líneas se pasan de 80 caracteres, en python se puede continuar la 
línea usando `\` al final de la línea
- considerar overflow/underflow de los enteros leídos