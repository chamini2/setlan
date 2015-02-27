========================================
==      Proyecto III - CI3725         ==
==      Luis Colorado 09-11086        ==
==      Nicolas Manan 06-39883        ==
==      Grupo 02                      ==
========================================

Descripción del proyecto

Se utilizo python para la elaboracion de el proyecto, en esta entrega
se verifico la validez de la semantica del programa con ayuda de una tabla 
de simbolos y un chequeo de los tipos de variables, datos asignados a las mmismas y 
operaciones realizadas entre ellos, ademas de verificar la buena escritura de bloques 
de estructuras.

De ser correcto el codigo leido, se representa en un arbol abstracto sintactico (ast) o una tabla de simbolos.

De ser incorrecto se indicara el error en la linea y columna correspondiente al codigo.

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

- Fue corregido el WARNING mostrado que senalaba un t_error ademas de los shift/reduces

- Se encontraron problemas al asignar a una variable Set un conjunto
	ej: Set s;
		s = { 'cualquier cosa en esta linea da error'  }

- Se imprime la tabla de simbolos pero las variables siempre toman el valor por defecto

- Los ; antes de fin de bloque no son reconocidos aun....

- Se intento implementar los FLAGS importando la libreria 'argparser' y luego 
  fueron declarados los argumentos -a -t -s -h donde t: imprime la lista de 
  Tokens, a: imprime el AST, s: imprime la tabla de simbolos y h: es un comando
  de ayuda, pero encontramos problemos al parsear la entrada los flags requerian
  un argumento y el archivo que pasamos por entrada no era un argumento reconocido
  por esta libreria   










