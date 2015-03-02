Universidad Simón Bolívar

Departamento de Computación y Tecnología de la Información

CI3725 - Traductores e Interpretadores

Diciembre - Marzo 2014-2015

Nombre:

Carné:

# Quiz de Laboratorio (4%)

A continuación se presenta una breve especificación del
lenguaje de programación `expressive`, lea detenidamente cada
uno de los apartados:

## Lenguaje de programación `expressive`

### Especificación del lenguaje.

El lenguaje de programación `expressive` es un lenguaje de tipo
funcional que permite definir una serie de funciones y reportar
los resultados de evaluar una o más de éstas.

### Estructura de un programa

```
define
	<definición 0>
	<definición 1>
	...
	<definición n>
end

# Comentario

<aplicación 0>
<aplicación 1>
...
<aplicación m>
```

### Identificadores

Un identificador de funciones o argumentos es una cadena de
caracteres de cualquier longitud compuesta únicamente por las
letras de la `A` a la `Z` (mayúsculas o minúsculas), los
dígitos del `0` al `9` y el caracter `_`.

Los identificadores no pueden comenzar por un dígito y son
sensibles a mayúsculas.

### Tipos de datos

El lenguaje `expressive` **únicamente** cuenta con el tipo de
datos enteros `int`: Números enteros sin signo.

### Definiciones

Un programa en `expressive` _puede_ tener un bloque incial de
N-definiciones de funciones. Cada definición cumple con la
siguiente estructura:

    <identificador 0>(<identificador 1>, <identificador 2>, ..., <identificador n>) = <expresión>

Las funciones en `expressive` pueden ser recursivas. El
lenguaje permite la redefinición de funciones si una nueva
definición posee un número de argumentos **diferente** al
de una antigua definición.

El lenguaje cuenta **sólo** con las siguientes definiciones 
precargadas:

+ `negate(x)`: Devuelve el inverso aditivo del argumento `x`.
+ `sum(x,y)`: Suma aritmeticamente el argumento `x` con el
argumento `y`.
+ `ifz(x,then,else)`: Verifica si el argumento `x` es igual a `0`
y en caso de serlo evalúa el argumento `then`, caso contrario
evalúa `else`.
+ `iflt(x,y,then,else)`: Verifica si el argumento `x` es menor que
el argumento `y` y en caso de ser cierta la condición, evalúa
el argumento `then`, caso contrario evalúa `else`.

De acuerdo con lo anterior, las siguientes son definiciones
válidas del lenguaje `expressive`:

~~~
define
	#Operaciones Booleanas
	not(x) = ifz(x,1,0)
	and(x,y) = ifz(x,0,ifz(y,0,1))
	or(x,y) = and(not(x),not(y))

	#Comparaciones
	ifnz(x,then,else) = ifz(not(x),then,else)
	ifeq(x,y,then,else) = ifz(sub(x,y),then,else)
	ifne(x,y,then,else) = ifeq(x,y,else,then)

	#Aritmética
	sum(x,y,z) = sum(x,sum(y,z))
	sub(x,y) = sum(x,negate(y))
	mult(x,y) = iflt(x
					 ,0
					 ,negate(mult(negate(x),y))
					 ,iflt(y
						   ,0
						   ,negate(mult(x,negate(y)))
						   ,ifeq(x
								 ,1
								 ,y
								 ,mult(sub(x,1),sum(y,y))
								 )
						  )
					)
	square(x) = mult(x,x)

	#expressive es Turing-Completo
	loop() = loop()
end
~~~

### Expresiones

Una expresión puede ser una aplicación de una función o un
número entero.

### Aplicaciones

`expressive` permite la aplicación de funciones definidas
por el lenguaje o el programador. Al aplicar una función
su resultado es mostrado por salida estándar seguido de un
salto de línea. Las aplicaciones de funciones deben de seguir 
la siguiente estructura:

    <identificador 0>(<expresión 0>,<expresión 1>,...<expresión n>)

El número de argumentos utilizados en la aplicación de una
función debe de coincidir con el número de argumentos de
su definición.

### Comentarios

Los comentarios en `expressive` incian con un caracter
numeral (`#`) y culminan al final de la línea que sigue a
éste. Las líneas y saltos de línea en el lenguaje son
omitidos.

### Ejemplo de programa

Programa:

```
define
	sumatoria(n) = ifz(n,0,suma(n,sumatoria(n-1)))
end

sumatoria(1)
sumatoria(2)
sumatoria(3)
sumatoria(4)
sumatoria(5)
```

Salida correspondiente:

```
1
3
6
10
15
```

## Pregunta 0

A partir de la especificación del lenguaje `expressive`
resuelva los siguientes ejercicios:

1. Proponga la gramática para el lenguaje.
2. Indique si existen conflictos del tipo _shift/reduce_. Explique el porqué.
3. Suponga que el lenguaje cuenta con una tabla de símbolos cuyos
elementos son almacenados en forma de `tupla`: `(identificador,numArgumentos)`.
De acuerdo con esto, proponga cómo debe ser _llenada_ la
tabla de símbolos en cada regla que así lo requiera. Para este
apartado usted cuenta con los siguientes procedimientos:

    + `SymTable.new()`: Constructor de una tabla de símbolos vacía.
    + `SymTable.insert(tupla)`: Inserta un elemento en la tabla de
símbolos.
    + `SymTable.delete(tupla)`: Elimina un elemento de la tabla de
símbolos.
    + `SymTable.update(tupla)`: Actualiza la información de un elemento
de la tabla de símbolos, suponiendo que éste existe.
    + `SymTable.contains(tupla)`: Determina si un elemento está contenido
dentro de la tabla de símbolos.
    + `SymTable.find(tupla)`: Asumiendo que está contenido en ella,
retorna la información de un elemento de la tabla de símbolos.

4. Proponga un reporte de errores _estáticos_ básico para el
lenguaje. Para ello, puede suponer que existe un procedimiento 
`error()` que imprime un mensaje de error por salida estándar y
aborta la ejecución del analizador.

## Pregunta 1

Proponga un árbol de derivación del siguiente programa en
`expressive`:

```
define
	fibonacci(x) = ifz(x,0,ifeq(x,1,1,sum(fibonacci(x-1),fibonacci(x-2))))
end

fibonacci(3)
fibonacci(7)
```

## Pregunta 2

Proponga un programa en `expressive` que defina la función _factorial_.
