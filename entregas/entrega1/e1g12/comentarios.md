- `setlan`, no `setlan.py`.
- programa no debe validar que la extensión sea `.stl`, eso es un detalle cosmético, debería funcionar para cualquier entrada válida
- el programa muestra *warnings* en las corridas
- el programa hace impresiones de más ("Leyendo el archivo de entrada: <casoX.stl>")
- el programa tiene impresiones de *debugging* ("C vale: 11Cvieja vale: 8")
- problema mostrando el número de columna
- considerar overflow/underflow de los enteros leídos
- regex de Strings mal:

para este ejemplo:

    "un string con \n, \\, \"", dos identificadores, "segundo string"

se espera la siguiente salida:

    # token STRING        value ("un string con \n, \\, \"") at line 1, column 1
    # token COMMA         value (,) at line 1, column 27
    # token IDENTIFIER    value (dos) at line 1, column 29
    # token IDENTIFIER    value (identificadores) at line 1, column 33
    # token COMMA         value (,) at line 1, column 48
    # token STRING        value ("segundo string") at line 1, column 50

pero su regex *agarra* el string desde el principio de la línea hasta el final, no se da cuenta de que ya se cerró el primer String:

    Token --> TkCadenaCaracteres , Identificador: '"un string con \n, \\, \"", dos identificadores, "segundo string"' , en la fila: 1 , columna: 1

El problema principal que le veo a la expresión regular es que hace un *or* `|`, para casos con caracteres escapados y casos sin ellos, si necesitan ayuda me pueden preguntar.
