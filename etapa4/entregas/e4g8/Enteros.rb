#!/usr/bin/env ruby

require_relative './Booleanos'
require_relative './Conjuntos'

class Enteros
    def initialize(value)
        if value.class == String
            @value = value.to_i
        else 
            @value = value
        end
        if @value > 2147483648
            abort "Error: overflow"
        end
    end


    def get_value
        return @value
    end

    def to_s
        return @value.to_s
    end
    #########################
    # Operaciones int a int #
    #########################
    def suma (otros)
        return Enteros.new (@value + otros.get_value)
    end


    def resta (otros)
        return Enteros.new (@value - otros.get_value)
    end


    def multiplicacion (otros)
        return Enteros.new (@value *  otros.get_value)
    end


    def division (otros)
        if otros.get_value == 0
            abort "Division por 0"
        end
        return Enteros.new (@value / otros.get_value)
    end


    def negado (otros)
        return Enteros.new (@value * -1)
    end


    def mod (otros)
        return Enteros.new (@value % otros.get_value)
    end

    def menor (otros)
        return Booleanos.new( @value < otros.get_value )
    end

    def mayor (otros)
        return Booleanos.new( @value > otros.get_value )
    end

    def menor_igual (otros)
        return Booleanos.new( @value <= otros.get_value )
    end

    def mayor_igual (otros)
        return Booleanos.new( @value >= otros.get_value )
    end

    def igual (otros)
        return Booleanos.new( @value == otros.get_value )
    end

    def diferente (otros)
        return Booleanos.new( @value != otros.get_value )
    end



    #########################
    # Operaciones int a set #
    #########################

    def suma_set (otros)
        aux = []
        otros.get_value.each do |x|
            aux << x + @value
        end

        return Conjuntos.new(aux)
    end


    def resta_set (otros)
        aux = []
        otros.get_value.each do |x|
            aux << x - @value
        end

        return Conjuntos.new(aux)
    end

    def multiplicacion_set (otros)
        aux = []
        otros.get_value.each do |x|
            aux << x * @value
        end

        return Conjuntos.new(aux)
    end


    def division_set (otros)
        aux = []
        otros.get_value.each do |x|
            aux << x / @value
        end

        return Conjuntos.new(aux)
    end


    def mod_set (otros)
        aux = []
        otros.get_value.each do |x|
            aux << x % @value
        end

        return Conjuntos.new(aux)
    end

    def pertenece_set (otros)

        otros.get_value.each do |x|
            if x == @value
                return Booleanos.new(true)
            end
        end

        return Booleanos.new(false)
    end

end