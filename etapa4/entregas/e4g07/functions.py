#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 07/03/2015
Ult. Modificacion el 08/03/2015

Este archivo define las funciones necesarias para la ejecucion del 
lenguaje Setlan.

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

# OPERACIONES BINARIAS

# Suma para dos enteros
def suma(x,y):
    if x + y > 2147483646:
        raise Exception("\nError: Overflow de numero entero ")
    return x + y

# Resta para dos enteros
def resta(x,y):
    if x - y < -2147483646:
        raise Exception("\nError: Overflow de numero entero ")
    return x - y

# Multiplicacion de dos enteros
def multiplicacion(x,y):
    if x*y > 2147483646 or x*y < -2147483646:
        raise Exception("\nError: Overflow de numero entero ")
    return x*y

# Division entera de dos enteros.
def division(x,y):
    if y == 0:
        raise Exception("\nError: Division por cero ")
    return x//y

# Modulo de la division entera de dos enteros.
def modulo(x,y):
    if y == 0:
        raise Exception("\nError: Division por cero ")
    return x%y

# And logico 
def logicAnd(x,y):
    return x and y

# Or Logico
def logicOr(x,y):
    return x or y

# Menor  para enteros
def menor(x,y):
    return x < y

# Mayor para enteros
def mayor(x,y):
    return x > y

# Menor o igual para enteros
def menorIgual(x,y):
    return x <= y

# Mayor o igual para enteros
def mayorIgual(x,y):
    return x >= y

# Igualdad para enteros, conjuntos y booleanos
def igual(x,y):
    return x == y

# Desigualdad para enteros, conjuntos y booleanos
def desigual(x,y):
    return x != y

# OPERACIONES PARA BINARIOS SOBRE CONJUNTOS
def setAListaDeEnteros(s):
    if not s or str(s) == "{}":
        elements = []
        return elements

    expreSet = str(s)
    elements = expreSet[1:-1].split(',')
    elements = map(int,elements)
    return elements

def listaDeEnterosASet(l):
    if not l or l == []:
        return "{}"

    setString = "{"
    for item in l:
        setString += str(item) + ","
    setString = setString[:-1]
    setString += "}"
    return setString

# Retorna si un entero pertenece a un set determinado
def contiene(x,set):
    lista = setAListaDeEnteros(set)
    return x in lista

# Retorna un nuevo conjunto resultado de la union de dos conjuntos
def union(set1, set2):
    listaSet1 = setAListaDeEnteros(set1)
    listaSet2 = setAListaDeEnteros(set2)

    for elem in listaSet1:
        if not elem in listaSet2:
            listaSet2.append(elem)

    newSet = listaDeEnterosASet(listaSet2)
    return newSet

# Devuelve en un nuevo conjunto la interseccion de dos conjuntos
def interseccion(set1,set2):
    listaSet1 = setAListaDeEnteros(set1)
    listaSet2 = setAListaDeEnteros(set2)
    listaNewSet = []

    for elem in listaSet1:
        if elem in listaSet2:
            listaNewSet.append(elem)

    newSet = listaDeEnterosASet(listaNewSet)
    return newSet

# Retorna un el conjunto diferencia
def diferencia(set1,set2):
    listaSet1 = setAListaDeEnteros(set1)
    listaSet2 = setAListaDeEnteros(set2)

    for elem in listaSet2:
        if elem in listaSet1:
            listaSet1.remove(elem)

    newSet = listaDeEnterosASet(listaSet1)
    return newSet

# Retorna el mapeo suma sobre el conjunto
def mapeoSuma(x,set):
    listaSet = setAListaDeEnteros(set)
    listaNewSet = []

    for elem in listaSet:
        listaNewSet.append(suma(x,elem))

    newSet = listaDeEnterosASet(listaNewSet)
    return newSet

# Retorna el mapeo resta sobre el conjunto
def mapeoResta(x,set):
    listaSet = setAListaDeEnteros(set)
    listaNewSet = []

    for elem in listaSet:
        listaNewSet.append(resta(elem,x))

    newSet = listaDeEnterosASet(listaNewSet)
    return newSet

# Retorna el mapeo multiplicacion sobre el conjunto
def mapeoMultiplicacion(x,set):
    listaSet = setAListaDeEnteros(set)
    listaNewSet = []

    for elem in listaSet:
        listaNewSet.append(multiplicacion(x,elem))

    newSet = listaDeEnterosASet(listaNewSet)
    return newSet

# Retorna el mapeo division sobre el conjunto
def mapeoDivision(x,set):
    listaSet = setAListaDeEnteros(set)
    listaNewSet = []

    for elem in listaSet:
        listaNewSet.append(division(elem,x))

    newSet = listaDeEnterosASet(listaNewSet)
    return newSet

# Retorna el mapeo modulo sobre el conjunto
def mapeoModulo(x,set):
    listaSet = setAListaDeEnteros(set)
    listaNewSet = []

    for elem in listaSet:
        listaNewSet.append(modulo(elem,x))

    newSet = listaDeEnterosASet(listaNewSet)
    return newSet

# OPERACIONES BINARIAS UNARIAS

# Devuelve el numero negativo de un numero x
def negativo(x):
    return -x

# Devuelve el negacion de una expresion booleana.
def negar(boolean):
    if boolean == 'false':
        return 'true'
    else:
        return 'false'

# Retorna el valor minimo en un conjunto
def minimo(set):
    if not set or str(set) == "{}":
        raise Exception("\nError: Conjunto vacio no tiene 'minimo' ")

    listaSet = setAListaDeEnteros(set)
    return min(listaSet)

# Retorna el valor maximo en un conjunto
def maximo(set):
    if not set or str(set) == "{}":
        raise Exception("\nError: Conjunto vacio no tiene 'maximo' ")

    listaSet = setAListaDeEnteros(set)
    return max(listaSet)

# Retorna el numero de Elementos de un conjunto
def numElementos(set):
    if not set or str(set) == "{}":
        return 0

    listaSet = setAListaDeEnteros(set)
    return len(listaSet)


