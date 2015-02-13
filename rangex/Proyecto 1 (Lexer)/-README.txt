CI3725 - Entrega 1 Grupo 7.
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285

Descripción del proyecto
Utilizamos  python  con  la  herramienta  Lex para facilitar el trabajo. se define en el 
diccionario "reserved"  la lista de palabras  reservadas del lenguaje para que estos
sean las primeras opciones a revisar al momento de validar un token. Luego, en  la
lista "tokens" se almacenan  los string  reservados  que  no  están conformados  por 
letras  sino  únicamente  por  símbolos. Luego, están  especificados  los  caracteres 
que el lenguaje hace caso omiso (espacios, tabulaciones y comentarios).

La función main recibe  un string y devuelve  la lista de tokens  válidos recibidos, en
caso de que consiga un error, devuelve la  lista  vacía  e imprime  por pantalla todos 
los errores conseguidos en el string pasado. 

Por último, escribimos el  main para que  si  el módulo es el  módulo principal,  pasa 
el lexer por el archivo pasado por línea de comando.