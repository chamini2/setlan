#!/usr/bin/env ruby

require "./Tabla"
#require "./Expresiones"
require "./Instrucciones"

class Handler
	attr_reader :stack

	def initialize(tab)
		@stack = [[:ROOT]]
		@tabla = tab
		@errorTabla = false
		@errorTipo = false
		@nivel = -1
		@lista = []
	end

	def iObjeto(objeto)
		push objeto
	end 


	def imprimir(imp_token, tokens, imp_ast, imp_tabla)
		if imp_token
			tokens.imprimir
		end
		if imp_ast
			puts @ast
		end
		if imp_tabla
			@tabla.imprimir
		end
	end

	def impExpr(lista)
		case lista[0].first
		when :IDENTIFIER, :INTEGER, :TRUE, :FALSE, :SET_I
			print lista[0][1]
		end
		if lista[1] != nil
			case lista[1].first
			when :IDENTIFIER, :INTEGER, :TRUE, :FALSE, :SET_I
				impExpr(lista.drop(1))
			else
				print lista[1].first
				print " "
				impExpr(lista.drop(1).first)
			end
		end
	end

	def chequeoTipos
		raiz = @stack.first.last
		procesar2(raiz.first, raiz.drop(1))
	end

	def chequeo
		@errorTabla = @tabla.chequeo
		chequeoTipos
	end

	def hayErrorTabla
		return @errorTabla
	end

	def hayErrorTipo
		return @errorTipo
	end

	def tiposValidos(lista,nivel)
		if lista[0][0] == :IDENTIFIER
			simbolo = @tabla.lookup(lista[0][1],nivel)
			if nil == simbolo
			elsif simbolo.getTipo == "int"
				valorizq = :INTEGER
			elsif simbolo.getTipo == "set"
				valorizq = :SET_I
			elsif simbolo.getTipo == "bool"
				valorizq = :TRUE
			end		
		else
			valorizq = lista[0][0]
		end
		if lista[1] != nil
			case lista[1].first
			when :PLUS, :MINUS, :MULTIPLICATION, :DIVISION, :MOD
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if valorizq != :INTEGER or valorder != :INTEGER
					return false
				else
					return :INTEGER
				end
			when :UNION, :INTERSECTION, :DIFERENCE
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if valorizq != :SET_I or valorder != :SET_I
					return false
				else
					return :SET_I
				end
			when :EQUAL, :DIFFERENT
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if (valorizq != valorder) and 
					(valorizq != :FALSE or valorder != :TRUE) and 
					(valorizq != :TRUE or valorder != :FALSE) and
					return false
				else
					return :TRUE
				end
			when :LESS, :LESS_EQUAL, :GREATER, :GREATER_EQUAL
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if valorizq != :INTEGER or valorder != :INTEGER
					return false
				else
					return :TRUE
				end
			when :OR, :AND
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if (valorizq != :FALSE or valorder != :FALSE) and
					(valorizq != :FALSE or valorder != :TRUE) and 
					(valorizq != :TRUE or valorder != :FALSE) and
					(valorizq != :TRUE or valorder != :TRUE)
					return false
				else
					return valorder
				end
			when :NOT
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if valorder != :TRUE or valorder != :FALSE
					return false
				else
					return valorder
				end
			when :PLUS_ON_SET, :MINUS_ON_SET, :MULTIPLICATION_ON_SET, :DIVISION_ON_SET, :MOD_ON_SET
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if valorizq != :INTEGER or valorder != :SET_I
					return false
				else
					return :SET_I
				end
			when :BIGGEST_ON_SET, :LOWEST_ON_SET, :CARD_ON_SET
				valorder = tiposValidos(lista.drop(1).first,nivel)
				if valorder != :SET_I
					return false
				else
					return :INTEGER
				end
			else
				valorder = tiposValidos(lista.drop(1),nivel)
			end
		else
			return valorizq
		end

	end

	def procesar2(tipo, resto)
		case tipo
		when :ASSIGN
			if tiposValidos(resto,@nivel) == false
				@errorTipo = true
				#puts "mal"
				#impExpr(resto)
			end
		when :"CONDICIONAL"
			valor = tiposValidos(resto,@nivel)
			if valor != :TRUE and valor != :FALSE
				@errorTipo = true
				#puts "mal"
			end
		when :IN
			resto[0].map {|x| procesar2(x.first, x.drop(1)) }
		when :BLOQUE
			@nivel = @nivel + 1
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :FINB
			@nivel = @nivel-1
		when :FOR
			@nivel = @nivel + 1
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :INT, :BOOL, :SET
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :PROGRAM
			procesar2(resto.first.first, resto.first.drop(1))
		when :BLOQUE, :USING, :INT, :SET, :BOOL
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :PRINT, :PRINTLN, :SCAN, :IF, :ELSE_IF, :ELSE, :FOR
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :REPEAT, :WHILE, :DO, :ASSIGN
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :IDENTIFIER, :INTEGER, :SET_I, :TRUE, :FALSE, :STRING
		when :MINUS, :BIGGEST_ON_SET, :LOWEST_ON_SET, :CARD_ON_SET
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :NOT, :PLUS, :MULTIPLICATION, :DIVISION, :MOD, :UNION
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :DIFERENCE, :INTERSECTION, :PLUS_ON_SET, :MINUS_ON_SET
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :MULTIPLICATION_ON_SET, :DIVISION_ON_SET, :MOD_ON_SET
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :EQUAL, :DIFFERENT, :OR, :AND, :LESS, :GREATER, :BELONG
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :LESS_EQUAL, :GREATER_EQUAL
			resto.map {|x| procesar2(x.first, x.drop(1)) }
		when :MIN, :MAX
		end
	end

	def interpretar
		Instrucciones.cargar(@tabla)
		@lista.each do |x|
			x.execute()
		end
	end

	def result
		raiz = @stack.first.last
		@ast = ""
		procesar(raiz.first, raiz.drop(1), 0, 0)
	end

	def procesar(tipo, resto, ind, nivel)
		case tipo
		when :PROGRAM
			@ast << " "*ind + tipo.to_s + "\n"
			procesar(resto.first.first, resto.first.drop(1), ind+4, nivel)
		when :BLOQUE
			@tabla.addscope
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel+1) }
			@tabla.endscope
		when :IBLOQUE
			@tabla.addscope
			if nivel < 2
				@lista << Instrucciones.new(tipo, resto, nivel+1)
			end
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel+1) }
			@tabla.endscope
		when :FOR
			@tabla.addscope
			@tabla.insert("int", resto.first.last)
			resto.drop(1)
			if nivel < 2
				@lista << Instrucciones.new(tipo, resto, nivel+1)
			end
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel+1) }
			@tabla.endscope
		when :INT
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| @tabla.insert("int", x.last);
				procesar(x.first, x.drop(1), ind+4, nivel) }
		when :BOOL
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| @tabla.insert("bool", x.last);
				procesar(x.first, x.drop(1), ind+4, nivel) }
		when :SET
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| @tabla.insert("set", x.last);
				procesar(x.first, x.drop(1), ind+4, nivel) }
		when :USING
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :IN
			@ast << " "*ind + tipo.to_s + "\n"
			resto[0].map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :PRINT, :PRINTLN, :SCAN, :ASSIGN, :IF
			if nivel < 2
				@lista << Instrucciones.new(tipo, resto, nivel)
			end
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :REPEAT, :WHILE, :ELSE_IF, :ELSE
			if nivel < 2
				@lista << Instrucciones.new(tipo, resto, nivel)
			end
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :"("
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :IDENTIFIER, :INTEGER, :SET_I, :TRUE, :FALSE, :STRING
			@ast << " "*ind + resto[0] + "\n"
		when :MINUS, :BIGGEST_ON_SET, :LOWEST_ON_SET, :CARD_ON_SET
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :NOT, :PLUS, :MULTIPLICATION, :DIVISION, :MOD, :UNION
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :DIFERENCE, :INTERSECTION, :PLUS_ON_SET, :MINUS_ON_SET
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :MULTIPLICATION_ON_SET, :DIVISION_ON_SET, :MOD_ON_SET
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :EQUAL, :DIFFERENT, :OR, :AND, :LESS, :GREATER, :BELONG
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :LESS_EQUAL, :GREATER_EQUAL
			@ast << " "*ind + tipo.to_s + "\n"
			resto.map {|x| procesar(x.first, x.drop(1), ind+4, nivel) }
		when :MIN, :MAX
			@ast << " "*ind + tipo.to_s + "\n"
		end
	end


	private 

	def push(objeto)
		@stack.last << objeto
		@stack << objeto 
	end
end 


