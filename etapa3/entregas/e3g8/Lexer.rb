#!/usr/bin/env ruby

#require_relative "Parser.rb"
PALABRAS_RESERVADAS = /^(?x)(program|println|print|scan|using|int|in|bool|set|
						else if|if|else|for|do|repeat|while|or|
						and|not|max|min)/

class Token
	def initialize(id, value=nil, pos)
		@id = id
		@value = value
		@pos = pos
	end

	def get_id()
		return @id
	end 

	def get_value()
		return @value
	end

	def get_pos()
		return @pos
	end

	def get_token()
		return [@id, @value]
	end 

	def to_s
		if (@id <=> "STRING") == 0
			return "token %-16s value (\"%s\") at line %d, column %d" % [@id, @value, @pos[0], @pos[1]]
			#return "token #{@id}\t\tvalue (\"#{@value}\") at line #{@pos[0]}, column #{@pos[1]})"
		else
			return "token %-16s value (%s) at line %d, column %d" % [@id, @value, @pos[0], @pos[1]]
			#return "token #{@id}\t\tvalue (#{@value}) at line #{@pos[0]}, column #{@pos[1]})"
		end
	end
end



class Lexer

	def initialize
		@tokens = Array.new
	end
	def analizar(archivo)
		nlinea = 0
		error = false
		archivo.each_line do |linea|
			nlinea += 1
			ncolumna = 1
			while linea != ""
				case linea
				# Palabras reservadas
				# El orden en la expresion regular importa, Ej:
				# println antes que print y int antes que in
				when PALABRAS_RESERVADAS
					palabra = linea[PALABRAS_RESERVADAS]
					linea = linea.partition(palabra).last
					@tokens << Token.new(palabra.upcase.intern, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size()
				# Strings
				when /^".*?"/
					palabra = linea[/".*?"/]
					# Procesar correctamente \", \\, \n
					palabra.gsub!(/\\"/, "\"")
					palabra.gsub!(/\\n/, "\n")
					palabra.gsub!(/\\\\/, "\\")
					linea = linea.partition(palabra).last
					@tokens << Token.new(:STRING, palabra[1..-2], [nlinea, ncolumna])
					ncolumna += palabra.size
				# Numeros
				when /^[0-9]+/
					if palabra.to_i > 2147483647
						linea = linea.partition(palabra).last
						palabra = palabra.partition(/\s/).first
						palabra.each_char do |i|
							puts "Error: Se analizo un int  #{palabra} que sobrepasa la capacidad del tipo" \
							" en la Linea #{nlinea} Columna #{ncolumna}"
							ncolumna += 1
						end
						error = true
					else
						palabra = linea[/[0-9]+/]
						linea = linea.partition(palabra).last
						@tokens << Token.new(:INTEGER, palabra, [nlinea, ncolumna])
						ncolumna += palabra.size
					end
				# Set
				when /^{ *\d+( *, *\d+)* *}/
					palabra = linea[/^{ *\d+( *, *\d+)* *}/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:SET_I, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size()
				%
				# Boolean
				when /^(true|false)/
					palabra = linea[/^(true|false)/]
					linea = linea.partition(palabra).last
					if (palabra <=> "true")
						@tokens << Token.new(:TRUE, palabra, [nlinea, ncolumna])
					else
						@tokens << Token.new(:FALSE, palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Nombre de variables
				when /^[a-zA-Z][a-zA-Z0-9_]*/
					palabra = linea[/[a-zA-Z][a-zA-Z0-9]*/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:IDENTIFIER, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Llaves
				when /^(\{\s|\})/
					palabra = linea[/[\{\}]/]
					linea = linea.partition(palabra).last
					if (palabra <=> "{") == 0
						@tokens << Token.new(:LCURLY, palabra, [nlinea, ncolumna])
					else
						@tokens << Token.new(:RCURLY, palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Parentesis
				when /^[\(\)]/
					palabra = linea[/[\(\)]/]
					linea = linea.partition(palabra).last
					if (palabra <=> "(") == 0
						@tokens << Token.new(:LPARENTHESIS, palabra, [nlinea, ncolumna])
					else
						@tokens << Token.new(:RPARENTHESIS, palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Coma y Punto y coma
				when /^[,;]/
					palabra = linea[/[,;]/]
					linea = linea.partition(palabra).last
					if (palabra <=> ",") == 0
						@tokens << Token.new(:COMMA, palabra, [nlinea, ncolumna])
					else
						@tokens << Token.new(:SEMICOLON, palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Operadores set
				when /^\+\+/
					palabra = linea[/^\+\+/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:UNION, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\\/
					palabra = linea[/\\/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:DIFERENCE, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\>\</
					palabra = linea[/\>\</]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:INTERSECTION, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\+\>/
					palabra = linea[/\<\+\>/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:PLUS_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\-\>/
					palabra = linea[/\<\-\>/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:MINUS_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\*\>/
					palabra = linea[/\<\*\>/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:MULTIPLICATION_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\/\>/
					palabra = linea[/\<\/\>/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:DIVISION_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\%\>/
					palabra = linea[/\<\%\>/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:MOD_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\>\?/
					palabra = linea[/\>\?/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:BIGGEST_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\?/
					palabra = linea[/\<\?/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:LOWEST_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\$\?/
					palabra = linea[/^\$\?/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:CARD_ON_SET, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operador booleano que necesitaba precedencia
				when /^\/=/
					palabra = linea[/^\/=/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:DIFFERENT, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores int
				when /^\+/
					palabra = linea[/\+/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:PLUS, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\-/
					palabra = linea[/\-/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:MINUS, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\*/
					palabra = linea[/\*/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:MULTIPLICATION, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\//
					palabra = linea[/\//]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:DIVISION, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\%/
					palabra = linea[/\%/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:MOD, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores booleanos
				when /^==/
					palabra = linea[/^==/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:EQUAL, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^<=/
					palabra = linea[/^<=/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:LESS_EQUAL, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^</
					palabra = linea[/^</]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:LESS, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^>=/
					palabra = linea[/^>=/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:GREATER_EQUAL, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^>/
					palabra = linea[/^>/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:GREATER, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^@/
					palabra = linea[/^@/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:BELONG, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operador
				when /^=/
					palabra = linea[/^=/]
					linea = linea.partition(palabra).last
					@tokens << Token.new(:ASSIGN, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Ignorar comentarios
				when /^#/
					linea = ""
				# Ignorar whitespace
				when /^\s+/
					palabra = linea[/^\s+/]
					linea = linea.partition(palabra).last
					ncolumna += palabra.size()
				else
					palabra = linea[/./]
					linea = linea.partition(palabra).last
					palabra = palabra.partition(/\s/).first
					palabra.each_char do |i|
						puts "Error: Se encontro un caracter inesperado #{palabra}" \
						" en la Linea #{nlinea} Columna #{ncolumna}"
								ncolumna += 1
					end
					error = true
				end
			end
		end
		if error
			@tokens.drop(@tokens.length())
			return false
		end
		return true
	end

	def next_token
		if (token = @tokens.shift) != nil
			return token.get_token
		else
			return nil
		end
	end

	def imprimir
		@tokens.each do |x|
			puts x
		end
	end

end

#nombre_archivo = ARGV.first
#archivo = open(nombre_archivo, "r")
#tokens = Lexer.new
#tokens.analizar(archivo) 
#parser = Parser.new(tokens)
#parser.parse

