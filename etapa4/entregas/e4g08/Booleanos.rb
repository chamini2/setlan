#!/usr/bin/env ruby


class Booleanos
    def initialize(value)

        if value.class == String
            if value == 'true'
                @value = true
            else
                @value = false
            end
        else
            @value = value
        end

    end 

    def get_value
        return @value
    end

    def to_s
        return @value.to_s
    end

    def or (otros)
        return Booleanos.new((@value or otros.get_value))
    end 

    def and (otros)
        return Booleanos.new((@value and otros.get_value))
    end 

    def not (otros)
        return Booleanos.new((not @value))
    end 

end