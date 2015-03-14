#!/usr/bin/env ruby

require_relative './Enteros'


class Conjuntos
 
    def initialize (value)
        if value.class == String
            @value = []
            while ( value.slice(/\d/) != nil )
                @value << value.slice(/\d/).to_i
                value = value.partition(/\d/).last
            end    
        else
            @value = value
        end 

        @value = @value.uniq
    end

    def get_value
        return @value
    end

    def to_s
        str = @value.to_s
        str[0] = "{"
        str[-1] = "}"
        return str
    end

    def union (otros)
        aux = @value
        otros.get_value.each do |x|
            aux << x
        end
        aux = aux.uniq
        return Conjuntos.new(aux)
    end

    def interseccion (otros)
        aux = []
        otros.get_value.each do |x|
            if @value.include?(x)
                aux << x
            end
        end
        return Conjuntos.new (aux)
    end


    def diferencia (otros)
        aux = @value

        otros.get_value.each do |x|
            aux.delete(x)
        end

        return Conjuntos.new (aux)
    end


    def maximo_valor
        aux = @value[0]
        @value.each do |x|
            if aux < x 
                aux = x
            end
        end

        return Enteros.new (aux)
    end

    def minimo_valor
        aux = @value[0]
        @value.each do |x|
            if aux > x 
                aux = x
            end
        end

        return Enteros.new (aux)
    end


    def cardinalidad
        return Enteros.new ( @value.length )
    end

    def order_mimax
        @value = @value.sort
    end

    def order_mamix
        @value = @value.sort
        @value = @value.reverse
    end
end 