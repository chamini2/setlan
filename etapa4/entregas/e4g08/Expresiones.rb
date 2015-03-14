#!/usr/bin/env ruby

require_relative './Booleanos'
require_relative './Conjuntos'
require_relative './Enteros'


class Expresiones 

    def initialize(tabla, nivel)
        @tabla = tabla
        @nivel = nivel
    end 


    def evaluate(exp)
        result = nil 
        case exp[0] 

        when :IDENTIFIER
            simbolo = @tabla.lookup(exp[1], @nivel)
            case simbolo.getTipo 
            when  "int"
                result = Enteros.new (simbolo.getValor.get_value)
            when  "bool"
                result = Booleanos.new (simbolo.getValor.get_value)
            when  "set"
                result = Conjuntos.new (simbolo.getValor.get_value)
            end
                           

        when :INTEGER
            result = Enteros.new (exp[1])
        when :SET_I
            result = Conjuntos.new (exp[1])
        when :TRUE, :FALSE
            result = Booleanos.new (exp[1])
        when :PLUS
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.suma(result2)
        when :MINUS
            if exp.length == 3
                result1 = Enteros.new(evaluate(exp[1]).get_value)
                result2 = Enteros.new(evaluate(exp[2]).get_value)
                result  = result1.resta(result2)
            else
                result  = Enteros.new(evaluate(exp[1]).get_value)
                result  = result.negado
            end
        when :MULTIPLICATION 
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.multiplicacion(result2)
        when :DIVISION
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.division(result2)
        when :MOD
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.mod(result2)
        when :UNION
            result1 = Conjuntos.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.union(result2)
        when :INTERSECTION
            result1 = Conjuntos.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.interseccion(result2)
        when :DIFERENCE
            result1 = Conjuntos.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.diferencia(result2)
        when :PLUS_ON_SET
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.suma_set(result2)
        when :MINUS_ON_SET
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.resta_set(result2)
        when :MULTIPLICATION_ON_SET
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.multiplicacion_set(result2)
        when :DIVISION_ON_SET
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.division_set(result2)
        when :MOD_ON_SET
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.mod_set(result2)
        when :BIGGEST_ON_SET
            result  = Conjuntos.new(evaluate(exp[1]).get_value)
            result  = result.maximo_valor
        when :LOWEST_ON_SET
            result  = Conjuntos.new(evaluate(exp[1]).get_value)
            result  = result.minimo_valor
        when :CARD_ON_SET
            result  = Conjuntos.new(evaluate(exp[1]).get_value)
            result  = result.cardinalidad
        when :OR
            result1  = Booleanos.new(evaluate(exp[1]).get_value)
            result2  = Booleanos.new(evaluate(exp[2]).get_value)
            result   = result1.or(result2)
        when :AND
            result1  = Booleanos.new(evaluate(exp[1]).get_value)
            result2  = Booleanos.new(evaluate(exp[2]).get_value)
            result   = result1.and(result2)
        when :BELONG 
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Conjuntos.new(evaluate(exp[2]).get_value)
            result  = result1.pertenece_set(result2)
        when :GREATER
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.mayor(result2)
        when :GREATER_EQUAL
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.mayor_igual(result2)
        when :LESS
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.menor(result2)
        when :LESS_EQUAL
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.menor_igual(result2)
        when :EQUAL
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.igual(result2)
        when :DIFFERENT
            result1 = Enteros.new(evaluate(exp[1]).get_value)
            result2 = Enteros.new(evaluate(exp[2]).get_value)
            result  = result1.diferente(result2)
        end

        return result
    end 

end







