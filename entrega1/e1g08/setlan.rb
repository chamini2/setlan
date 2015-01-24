#!/usr/bin/env ruby

PALABRAS_RESERVADAS = /^(?x)(program|println|print|scan|using|int|in|bool|set|
						else if|if|else|for|do|repeat|while|def|->|return|or|
						and|not)/

class Token
	def initialize(id, value=nil, pos)
		@id = id
		@value = value
		@pos = pos
	end

	def to_s
		if (@id <=> "ID") == 0 || (@id <=> "String") == 0
			return "Token#{@id}: \"#{@value}\"(Linea #{@pos[0]}, Columna #{@pos[1]})"
		else
			return "Token#{@id}(Linea #{@pos[0]}, Columna #{@pos[1]})"
		end
	end

end

class Lexer
	def self.analizar(archivo)
		tokens = Array.new
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
					if (palabra <=> "->") == 0
						tokens << Token.new("ReturnOp", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new(palabra[0].upcase+palabra[1..-1], palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Llaves
				when /^[\{\}]/
					palabra = linea[/[\{\}]/]
					linea = linea.partition(palabra).last
					if (palabra <=> "{") == 0
						tokens << Token.new("OpenCurly", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new("CloseCurly", palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Parentesis
				when /^[\(\)]/
					palabra = linea[/[\(\)]/]
					linea = linea.partition(palabra).last
					if (palabra <=> "{") == 0
						tokens << Token.new("OpenParenthesis", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new("CloseParenthesis", palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Coma y Punto y coma
				when /^[,;]/
					palabra = linea[/[,;]/]
					linea = linea.partition(palabra).last
					if (palabra <=> ",") == 0
						tokens << Token.new("Comma", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new("Semicolon", palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Nombre de variables
				when /^[a-zA-Z][a-zA-Z0-9_]*/
					palabra = linea[/[a-zA-Z][a-zA-Z0-9]*/]
					linea = linea.partition(palabra).last
					tokens << Token.new("ID", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Strings
				when /^".*"/
					palabra = linea[/".*"/]
					linea = linea.partition(palabra).last
					tokens << Token.new("String", palabra[1..-2], [nlinea, ncolumna])
					ncolumna += palabra.size
				# Numeros
				when /^[0-9]+/
					palabra = linea[/[0-9]+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Number", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores set
				when /^\+\+/
					palabra = linea[/^\+\+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Union", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\\/
					palabra = linea[/\\/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Diference", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\>\</
					palabra = linea[/\>\</]
					linea = linea.partition(palabra).last
					tokens << Token.new("Intersection", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\+\>/
					palabra = linea[/\<\+\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Plus_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\-\>/
					palabra = linea[/\<\-\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Minus_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\*\>/
					palabra = linea[/\<\*\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Multiplication_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\/\>/
					palabra = linea[/\<\/\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Division_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\%\>/
					palabra = linea[/\<\%\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Mod_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\>\?/
					palabra = linea[/\>\?/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Biggest_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\?/
					palabra = linea[/\<\?/]
					linea = linea.partition(palabra).last
					tokens << Token.new("lowest_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\$\?/
					palabra = linea[/\+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Card_on_set", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores int
				when /^\+/
					palabra = linea[/\+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Plus", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\-/
					palabra = linea[/\-/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Minus", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\*/
					palabra = linea[/\*/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Multiplication", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\//
					palabra = linea[/\//]
					linea = linea.partition(palabra).last
					tokens << Token.new("Division", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\%/
					palabra = linea[/\%/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Mod", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores booleanos
				when /^==/
					palabra = linea[/^==/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Equal", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\/=/
					palabra = linea[/^\/=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Different", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^<=/
					palabra = linea[/^<=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("LessEqual", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^</
					palabra = linea[/^</]
					linea = linea.partition(palabra).last
					tokens << Token.new("Less", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^>=/
					palabra = linea[/^>=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("GreaterEqual", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^>/
					palabra = linea[/^>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Greater", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^@/
					palabra = linea[/^@/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Belong", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operador
				when /^=/
					palabra = linea[/^=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("Union", palabra, [nlinea, ncolumna])
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
		if !error
			tokens.each do |i|
				puts "#{i}"
			end
		end
	end
end


nombre_archivo = ARGV.first
archivo = open(nombre_archivo, "r")

Lexer.analizar(archivo)