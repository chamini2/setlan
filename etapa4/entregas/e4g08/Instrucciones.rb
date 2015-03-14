
require "./Expresiones"



class Instrucciones
	@@tabla

	def initialize(tipo, cosas, nivel)
		@tipo = tipo
		@cosas = cosas
		@nivel = nivel
	end

	def self.cargar(tabla)
		@@tabla = tabla
	end

	def execute()
		exps = Expresiones.new(@@tabla, @nivel)
		case @tipo
		when :ASSIGN
			id = @@tabla.lookup(@cosas[0][1], @nivel)
			resultado = exps.evaluate(@cosas[1])
			@@tabla.update(@cosas[0][1],@nivel,resultado)
		when :PRINT, :PRINTLN
			mensaje = ""
			@cosas.each do |x|
				case x[0]
				when :PLUS, :MINUS, :MULTIPLICATION , :DIVISION, :MOD, :UNION, :INTERSECTION, :DIFERENCE, :PLUS_ON_SET, :MINUS_ON_SET, :MULTIPLICATION_ON_SET, :DIVISION_ON_SET, :MOD_ON_SET, :BIGGEST_ON_SET, :LOWEST_ON_SET, :CARD_ON_SET, :OR, :AND, :BELONG , :GREATER, :GREATER_EQUAL, :LESS, :LESS_EQUAL, :EQUAL, :DIFFERENT
					resultado = exps.evaluate(x)
					mensaje << resultado.to_s
				when :IDENTIFIER
					id = @@tabla.lookup(x[1], @nivel)
					mensaje << id.getValor.get_value.to_s
				when :INTEGER, :SET_I, :TRUE, :FALSE, :STRING
					mensaje << x[1]
				end
			end
			print mensaje
			if(@tipo == :PRINTLN)
				puts ""
			end
		when :SCAN
			x = STDIN.gets.chomp
			id = @@tabla.lookup(@cosas[0][1], @nivel)

			if x =~ /^\d+$/
				entero = Enteros.new(x)
				@@tabla.update(@cosas[0][1],@nivel,entero)
			elsif x=="true" or x=="false"
				booleano = Booleanos.new(x)
				@@tabla.update(@cosas[0][1],@nivel,entero)
			else
				abort "ERROR: Entrada invalida"
			end			

			@@tabla.update(@cosas[0][1],@nivel,resultado)
		when :IF
			if exps.evaluate(@cosas[0][1]).get_value
				lista = @cosas[1].drop(1)
				if lista
					lista.each do |x|
						inst = Instrucciones.new(x[0], x.drop(1), @nivel+1)
						inst.execute
					end
				end
			elsif @cosas[2]
				if @cosas[2][1] == :IF
					inst = Instrucciones.new(@cosas[2][1][0], @cosas[2][1].drop(1), @nivel+1)
					inst.execute
				elsif @cosas[2][0] == :ELSE
					lista = @cosas[2][1].drop(1)
					if lista
						lista.each do |x|
							inst = Instrucciones.new(x[0], x.drop(1), @nivel+1)
							inst.execute
						end
					end	
				end
			end
		when :FOR
			resultado = exps.evaluate(@cosas[2])

			if @cosas[1][0] == :MIN
				resultado = resultado.order_mimax
			elsif @cosas[1][0] == :MAX
				resultado = resultado.order_mamix
			end

			if resultado.length == 0
				abort "Error: Conjunto vacio en un for"
			end
			
			resultado.each do |i|
				asd = @@tabla.update(@cosas[0][1], @nivel, Enteros.new(i))
				lista = @cosas[3].drop(1)
				if lista
					lista.each do |x|
						inst = Instrucciones.new(x[0], x.drop(1), @nivel+1)
						inst.execute
					end
				end
			end
		when :REPEAT
			cond = @cosas[1][1][1]
			lista1 = @cosas[0].drop(1)
			inst1 = []
			if lista1
				lista1.each do |x|
					inst1 << Instrucciones.new(x[0], x.drop(1), @nivel+1)
				end
			end
			lista2 = @cosas[1][3].drop(1)
			inst2 = []
			if lista2
				lista2.each do |x|
					inst2 << Instrucciones.new(x[0], x.drop(1), @nivel+1)
				end
			end
			begin
				inst1.each do |x|
					x.execute
				end
				res_cond = exps.evaluate(cond).get_value
				if(res_cond and inst2!=nil)
					inst2.each do |x|
						x.execute
					end
				end
			end while(res_cond)
		when :WHILE
			lista = @cosas[2].drop(1)
			inst = []
			if lista
				lista.each do |x|
					inst << Instrucciones.new(x[0], x.drop(1), @nivel+1)
				end
			end
			while(exps.evaluate(@cosas[0][1]).get_value)
				inst.each do |x|
					x.execute
				end
			end
		when :IBLOQUE
			if @cosas[0][0] == :USING
				@cosas = @cosas[1][1]
			end 

			if @cosas
				@cosas.each do |x|
					inst = Instrucciones.new(x[0], x.drop(1), @nivel+1)
					inst.execute()
				end
			end
		end
	end
end