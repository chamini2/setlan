#!/usr/bin/env ruby

PALABRAS_RESERVADAS = /^(?x)(program|println|print|scan|using|int|in|bool|set|
						else if|if|else|for|do|repeat|while|or|
						and|not|max|min)/
INSTRUCCIONES_RESERVADAS = /(PRINTLN|PRINT|SCAN|IF|FOR|REPEAT|WHILE|ELSE)/

OPERADORES = /(?x)(UNION|DIFERENCE|INTERSECTION|PLUS_ON_SET|MINUS_ON_SET|MULTIPLICATION_ON_SET|
				DIVISION_ON_SET|MOD_ON_SET|BIGGEST_ON_SET|lOWEST_ON_SET|CARD_ON_SET|
				PLUS|MINUS|MULTIPLICATION|DIVISION|MOD|EQUAL|DIFFERENT|LESSEQUAL|
				LESS|GREATEREQUAL|GREATER|BELONG)/
TIPOS = /(?x)(BOOL|INT|SET)/

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
					tokens << Token.new(palabra.upcase, palabra, [nlinea, ncolumna])
					ncolumna += palabra.size()
				# Strings
				when /^".*?"/
					palabra = linea[/".*?"/]
					# Procesar correctamente \", \\, \n
					palabra.gsub!(/\\"/, "\"")
					palabra.gsub!(/\\n/, "\n")
					palabra.gsub!(/\\\\/, "\\")
					linea = linea.partition(palabra).last
					tokens << Token.new("STRING", palabra[1..-2], [nlinea, ncolumna])
					ncolumna += palabra.size
				# Numeros
				when /^[0-9]+/
					palabra = linea[/[0-9]+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("INTEGER", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Set
				when /^{ *\d+( *, *\d+)* *}/
					palabra = linea[/^{ *\d+( *, *\d+)* *}/]
					linea = linea.partition(palabra).last
					tokens << Token.new("SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size()
				# Boolean
				when /^(true|false)/
					palabra = linea[/^(true|false)/]
					linea = linea.partition(palabra).last
					tokens << Token.new("BOOL", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size()
				# Nombre de variables
				when /^[a-zA-Z][a-zA-Z0-9_]*/
					palabra = linea[/[a-zA-Z][a-zA-Z0-9]*/]
					linea = linea.partition(palabra).last
					tokens << Token.new("IDENTIFIER", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Llaves
				when /^(\{\s|\})/
					palabra = linea[/[\{\}]/]
					linea = linea.partition(palabra).last
					if (palabra <=> "{") == 0
						tokens << Token.new("LCURLY", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new("RCURLY", palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Parentesis
				when /^[\(\)]/
					palabra = linea[/[\(\)]/]
					linea = linea.partition(palabra).last
					if (palabra <=> "(") == 0
						tokens << Token.new("LPARENTHESIS", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new("RPARENTHESIS", palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Coma y Punto y coma
				when /^[,;]/
					palabra = linea[/[,;]/]
					linea = linea.partition(palabra).last
					if (palabra <=> ",") == 0
						tokens << Token.new("COMMA", palabra, [nlinea, ncolumna])
					else
						tokens << Token.new("SEMICOLON", palabra, [nlinea, ncolumna])
					end
					ncolumna += palabra.size()
				# Operadores set
				when /^\+\+/
					palabra = linea[/^\+\+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("UNION", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\\/
					palabra = linea[/\\/]
					linea = linea.partition(palabra).last
					tokens << Token.new("DIFERENCE", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\>\</
					palabra = linea[/\>\</]
					linea = linea.partition(palabra).last
					tokens << Token.new("INTERSECTION", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\+\>/
					palabra = linea[/\<\+\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("PLUS_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\-\>/
					palabra = linea[/\<\-\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("MINUS_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\*\>/
					palabra = linea[/\<\*\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("MULTIPLICATION_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\/\>/
					palabra = linea[/\<\/\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("DIVISION_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\%\>/
					palabra = linea[/\<\%\>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("MOD_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\>\?/
					palabra = linea[/\>\?/]
					linea = linea.partition(palabra).last
					tokens << Token.new("BIGGEST_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\<\?/
					palabra = linea[/\<\?/]
					linea = linea.partition(palabra).last
					tokens << Token.new("lOWEST_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\$\?/
					palabra = linea[/\+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("CARD_ON_SET", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores int
				when /^\+/
					palabra = linea[/\+/]
					linea = linea.partition(palabra).last
					tokens << Token.new("PLUS", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\-/
					palabra = linea[/\-/]
					linea = linea.partition(palabra).last
					tokens << Token.new("MINUS", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\*/
					palabra = linea[/\*/]
					linea = linea.partition(palabra).last
					tokens << Token.new("MULTIPLICATION", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\//
					palabra = linea[/\//]
					linea = linea.partition(palabra).last
					tokens << Token.new("DIVISION", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\%/
					palabra = linea[/\%/]
					linea = linea.partition(palabra).last
					tokens << Token.new("MOD", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operadores booleanos
				when /^==/
					palabra = linea[/^==/]
					linea = linea.partition(palabra).last
					tokens << Token.new("EQUAL", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^\/=/
					palabra = linea[/^\/=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("DIFFERENT", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^<=/
					palabra = linea[/^<=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("LESSEQUAL", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^</
					palabra = linea[/^</]
					linea = linea.partition(palabra).last
					tokens << Token.new("LESS", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^>=/
					palabra = linea[/^>=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("GREATEREQUAL", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^>/
					palabra = linea[/^>/]
					linea = linea.partition(palabra).last
					tokens << Token.new("GREATER", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				when /^@/
					palabra = linea[/^@/]
					linea = linea.partition(palabra).last
					tokens << Token.new("BELONG", palabra, [nlinea, ncolumna])
					ncolumna += palabra.size
				# Operador
				when /^=/
					palabra = linea[/^=/]
					linea = linea.partition(palabra).last
					tokens << Token.new("ASSIGN", palabra, [nlinea, ncolumna])
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
			#tokens.each do |t|
			#	puts t
			#end
			return tokens
		end
	end
end

class Parser
	@@tokens = []
	@@arbol = ""
	def self.analizar(tokens)
		@@tokens = tokens 
		if Parser.program()
			puts @@arbol
		end
	end

	def self.program()
		token = @@tokens[0]
		@@tokens = @@tokens.drop(1)
		if token.get_id() ==  "PROGRAM"
			@@arbol = @@arbol + "PROGRAM" + "\n"
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if token.get_id() == "LCURLY"
				@@arbol = @@arbol + "    BLOCK" + "\n"
				if not Parser.declaracion(token, "        ")
					return false
				end
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if not Parser.instruciones(token, "RCURLY", "        ")
					return false
				end
				@@arbol = @@arbol + "    BLOCK_END" + "\n"

			elsif token.get_id() =~ INSTRUCCIONES_RESERVADAS
				if not Parser.instruciones(token, "ONELINE", "    ")
					return false
				end
			else
				Parser.error(token, 2)
				return false
			end
		else
			Parser.error(token, 2)
			return false
		end
		
		return true
	end 

	def self.instruciones(token, stop, indem)
		if (token.get_id() == "PRINTLN") ||  (token.get_id() == "PRINT")
			ins = token.get_id()
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if (token.get_id() == "STRING") || (token.get_id() == "IDENTIFIER") 
				while (token.get_id() == "STRING") \
					|| (token.get_id() == "IDENTIFIER") do

					@@arbol = @@arbol + indem+ins+" "+token.get_value() + "\n"
					#Parser.palabra(token)
					if (@@tokens[0].get_id() == "COMMA")
						@@tokens = @@tokens.drop(1)
						token = @@tokens[0]
						@@tokens = @@tokens.drop(1)
					elsif (@@tokens[0].get_id() == "MULTIPLICATION")
						@@tokens = @@tokens.drop(1)
						token = @@tokens[0]
						@@tokens = @@tokens.drop(1)						
						@@arbol[@@arbol.length - 1] = " * a\n" 
					else
						break
					end
				end
			else 
				Parser.error(token, stop)
			end
		elsif (token.get_id() == "SCAN")
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if token.get_id() == "IDENTIFIER"
				@@arbol = @@arbol + indem+"SCAN "+token.get_value() + "\n"
				#Parser.palabra(token)
			else 
				Parser.error(token, 2)
				return false
			end

		elsif (token.get_id() == "IF")
			@@arbol = @@arbol + indem+"IF" + "\n"
			elseindem = indem
			indem = indem+"    "
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if token.get_id() == "LPARENTHESIS"
				@@arbol = @@arbol + indem+"(" + "\n"
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if not Parser.expresion(token, indem+"    ")
					return false
				end
				if token.get_id() == "RPARENTHESIS"
					@@arbol = @@arbol + indem+")" + "\n"
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)
					if (token.get_id() == "LCURLY")
						@@arbol = @@arbol + indem+"BLOCK" + "\n"
						token = @@tokens[0]
						@@tokens = @@tokens.drop(1)
						if not Parser.instruciones(token,"RCURLY", indem+"    ")
							return false
						end
						@@arbol = @@arbol + indem+"BLOCK_END" + "\n"
						token = @@tokens[0]
					else
						if not Parser.instruciones(token,"ONELINE", indem)
							return false
						end
					end
				else
					token = Token.new("", ")", token.get_pos)
					Parser.error(token, 1)
					return false
				end
			else
				token = Token.new("", "(", token.get_pos)
				Parser.error(token, 1)
				return false
			end
			if (@@tokens[0].get_id() == "ELSE")
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				@@arbol = @@arbol + elseindem+"ELSE" + "\n"
				elseindem = elseindem+"    "
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if (token.get_id() == "LCURLY")
					@@arbol = @@arbol + elseindem+"BLOCK" + "\n"
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)
					if not Parser.instruciones(token,"RCURLY", elseindem+"    ")
						return false
					end
					@@arbol = @@arbol + indem+"BLOCK_END" + "\n"
				else
					if not Parser.instruciones(token,"ONELINE", elseindem)
						return false
					end
				end
			end


		elsif (token.get_id() == "FOR")
			@@arbol = @@arbol + indem+"FOR" + "\n"
			indem = indem+"    "
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)

			if token.get_id() == "IDENTIFIER"
				@@arbol = @@arbol + indem+token.get_value() + "\n"
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)

				if (token.get_id() == "MIN") || (token.get_id() == "MAX")
					@@arbol = @@arbol + indem+token.get_id() + "\n"
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)

					if (token.get_id() == "IDENTIFIER") or (token.get_id() == "SET")
						@@arbol = @@arbol + indem+token.get_value() + "\n"
						token = @@tokens[0]
						@@tokens = @@tokens.drop(1)
						if (token.get_id() == "DO")
							@@arbol = @@arbol + indem+token.get_id() + "\n"
							indem = indem+"    "
							token = @@tokens[0]
							@@tokens = @@tokens.drop(1)
							if (token.get_id() == "LCURLY")
								@@arbol = @@arbol + indem+"BLOCK" + "\n"
								token = @@tokens[0]
								@@tokens = @@tokens.drop(1)
								if not Parser.instruciones(token,"RCURLY", idem+"    ")
									return false
								end
								@@arbol = @@arbol + indem+"BLOCK_END" + "\n"

							else
								if not Parser.instruciones(token,"ONELINE")
									return false
								end
							end
						else
							Parser.error(token, 2)
							return false
						end
					else
						Parser.error(token, 2)
						return false
					end
				else
					Parser.error(token,2)
					return false
				end

			else
				Parser.error(token, 2)
				return false
			end
		elsif (token.get_id() == "WHILE")
			@@arbol = @@arbol + indem+"WHILE" + "\n"
			indem = indem+"    "
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if (token.get_id() == "LPARENTHESIS")
				@@arbol = @@arbol + indem+"(" + "\n"
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if not Parser.expresion(token, indem+"    ")
					return false
				end
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if (token.get_id() == "RPARENTHESIS")
					@@arbol = @@arbol + indem+")" + "\n"
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)
					if (token.get_id() == "DO")
						@@arbol = @@arbol + indem+token.get_id() + "\n"
						indem = indem+"    "
						token = @@tokens[0]
						@@tokens = @@tokens.drop(1)
						if (token.get_id() == "LCURLY")
							@@arbol = @@arbol + indem+"BLOCK" + "\n"
							token = @@tokens[0]
							@@tokens = @@tokens.drop(1)
							if not Parser.instruciones(token,"RCURLY", indem+"    ")
								return false
							end
							@@arbol = @@arbol + indem+"BLOCK_END" + "\n"
						else
							if not Parser.instruciones(token,"ONELINE")
								return false
							end
						end
					else
						Parser.error(token, 2)
					end
				else
					token = Token.new("", ")", token.get_pos)
					Parser.error(token,1)
					return false
				end
			else
				token = Token.new("", "(", token.get_pos)
				Parser.error(token,1)
				return false
			end
		elsif (token.get_id() == "REPEAT")
			@@arbol = @@arbol + indem+"REPEAT" + "\n"
			whileindem = indem
			indem = indem+"    "
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if (token.get_id() == "LCURLY")
				@@arbol = @@arbol + indem+"BLOCK" + "\n"
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if not Parser.instruciones(token,"RCURLY",indem+"    ")
					return false
				end
				@@arbol = @@arbol + indem+"BLOCK_END" + "\n"
			else
				if not Parser.instruciones(token,"ONELINE", indem)
					return false
				end
			end

			# While del Repeat
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if (token.get_id() == "WHILE")
				@@arbol = @@arbol + whileindem+"WHILE" + "\n"
				whileindem = whileindem+"    "
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if (token.get_id() == "LPARENTHESIS")
					@@arbol = @@arbol + whileindem+"(" + "\n"
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)
					if not Parser.expresion(token, indem+"    ")
						return false
					end
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)
					if (token.get_id() == "RPARENTHESIS")
						@@arbol = @@arbol + whileindem+")" + "\n"
						token = @@tokens[0]
						@@tokens = @@tokens.drop(1)
						if (token.get_id() == "DO")
							@@arbol = @@arbol + whileindem+"DO" + "\n"
							whileindem = whileindem+"    "
							token = @@tokens[0]
							@@tokens = @@tokens.drop(1)
							if (token.get_id() == "LCURLY")
								@@arbol = @@arbol + whileindem+"BLOCK" + "\n"
								token = @@tokens[0]
								@@tokens = @@tokens.drop(1)
								if not Parser.instruciones(token,"RCURLY",whileindem+"    ")
									return false
								end
								@@arbol = @@arbol + whileindem+"BLOCK_END" + "\n"
							else
								if not Parser.instruciones(token,"ONELINE",indem)
									return false
								end
							end
						else
							Parser.error(token,2)
							return false
						end
					else
						token = Token.new("", ")", token.get_pos)
						Parser.error(token,1)
						return false
					end
				else
					token = Token.new("", "(", token.get_pos)
					Parser.error(token,1)
					return false
				end
			else
				Parser.error(token,2)
				return false
			end
		elsif (token.get_id() == "IDENTIFIER")
			@@arbol = @@arbol + indem+"ASSIGN" + "\n"
			if not Parser.asignacion(token,indem+"   ")
				return false
			end
		else 
			Parser.error(token, 2)
		end 

		if (stop == "ONELINE")
			#pass
		elsif (stop == "RCURLY")
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if (token.get_id() == "SEMICOLON")
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if (token.get_id() == "RCURLY") and (@@tokens[0] == nil)
					Parser.finalizacion()	
				elsif (token.get_id() == "RCURLY")
					
					#pass
				else
					if not Parser.instruciones(token, "RCURLY", indem)
						return false
					end
				end
			else
				token = Token.new("", ";", token.get_pos)
				Parser.error(token,1)
				return false
			end
		else 
			#Parser.error(token)
		end
					
		return true
	end

	def self.finalizacion()
		#Termino el programa
	end 


	def self.palabra(token)
		if (token.get_id() == "STRING")
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if not Parser.palabra(token)
				return false
			end
		elsif (token.get_id() == "COMMA")
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if not Parser.palabra(token)
				return false
			end
		else
			# Que la expresion se encargue del error.
			if not Parser.expresion(token, indem)
				return false
			end
		end
		
		return true
	end

	def self.asignacion(token,indem)
		@@arbol = @@arbol + indem+" " + token.get_value + "\n"
		token = @@tokens[0]
		@@tokens = @@tokens.drop(1)
		if (token.get_id() == "ASSIGN")
			@@arbol = @@arbol + indem + token.get_value + "\n"
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if not Parser.expresion(token,indem)
				return false
			end
		else
			Parser.error(token, 2)
			return false
		end
		
		return true
	end

	def self.declaracion(token, indem)
		token = @@tokens[0]
		@@tokens = @@tokens.drop(1)
		if ( token.get_id() == "USING")
			@@arbol = @@arbol + indem+"USING" + "\n"
			while(token.get_id() != "IN") do
				if not Parser.declaracion(token, indem+"    ") 
					return false
				end
				token = @@tokens[0]
			end
			@@arbol = @@arbol + indem+"IN" + "\n"
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
		elsif ( token.get_id() =~ TIPOS )
			tipo = token.get_id()
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			while ( token.get_id() == "IDENTIFIER") do
				@@arbol = @@arbol + indem+tipo+" "+token.get_value() + "\n"
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if ( token.get_id() == "COMMA")
					token = @@tokens[0]
					@@tokens = @@tokens.drop(1)
				elsif ( token.get_id() == "SEMICOLON")
					break
				else
					Parser.error(token, 2)
					return false
				end
			end
		else 
			Parser.error(token, 2)
			return false
		end
		
		return true
	end


	def self.expresion(token, indem)
		if(token.get_id() == "INTEGER") or (token.get_id() == "SET") or
				(token.get_id() == "BOOL") or (token.get_id() == "IDENTIFIER")
			@@arbol = @@arbol + indem + token.get_value + "\n"
			if(@@tokens[0].get_id() =~ OPERADORES)
				token = @@tokens[0]
				@@tokens = @@tokens.drop(1)
				if not Parser.expresion2(token,indem)
					return false
				end
			end
		elsif token.get_id() == "LPARENTHESIS"
			@@arbol = @@arbol + indem + token.get_value + "\n"
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if not Parser.expresion(token, indem+"    ")
				return false
			end
			if @@tokens[0].get_id() == "RPARENTHESIS"
				@@arbol = @@arbol + indem + token.get_value + "\n"
				if(@@tokens[1].get_id() =~ OPERADORES)
					token = @@tokens[1]
					@@tokens = @@tokens.drop(2)
					if not Parser.expresion(token, indem)
						return false
					end
				end		
			else
				token = Token.new("", ")", @@tokens[0].get_pos)
				Parser.error(token, 1)
				return false
			end
		elsif token.get_id() == "MINUS"
			@@arbol = @@arbol + indem + token.get_value + "\n"
			token = @@tokens[0]
			@@tokens = @@tokens.drop(1)
			if not Parser.expresion(token,indem)
				return false
			end
		else
			Parser.error(token, 2)
			return false
		end
		
		return true
	end

	def self.expresion2(token,indem)
		@@arbol = @@arbol + indem + token.get_value + "\n"
		token = @@tokens[0]
		@@tokens = @@tokens.drop(1)
		recursion_sigue = /(INTEGER|SET|BOOL|IDENTIFIER|LPARENTHESIS|MINUS)/
		if token.get_id() =~ recursion_sigue
			if not Parser.expresion(token,indem)
				return false
			end
		else
			Parser.error(token,2)
			return false
		end

		return true
	end

	def self.error(token, opcion)
		if(opcion == 1)
			puts "ERROR: missing token '#{token.get_value}' near line #{token.get_pos[0]}, column #{token.get_pos[1]}." + "\n"
		elsif (opcion == 2)
			puts "ERROR: unexpected token '#{token.get_value}' at line #{token.get_pos[0]}, column #{token.get_pos[1]}."
		else
			puts "ERROR: unspecified syntax error."
		end
		
	end


end 

nombre_archivo = ARGV.first
archivo = open(nombre_archivo, "r")

tokens = Lexer.analizar(archivo)
#Lexer.analizar(archivo)
Parser.analizar(tokens)