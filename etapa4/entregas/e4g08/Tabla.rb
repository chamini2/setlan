#!/usr/bin/env ruby

require "./Expresiones"

class Simbolo
	def initialize(tipo, id)
		@id = id
		@tipo = tipo
		if tipo == "int"
			@valor = Enteros.new(0)
		elsif tipo == "bool"
			@valor = Booleanos.new(false)
		elsif tipo == "set"
			@valor = Conjuntos.new([])
		else
			puts "TIPO INVALIDO"
		end		
	end

	def getID
		return @id
	end

	def getTipo
		return @tipo
	end

	def getValor
		return @valor
	end

	def cambiarValor(valor)
		@valor = valor
	end

	def ==(otro)
		return @id == otro.getID
	end

	def !=(otro)
		return @id != otro.getID
	end

	def <=>(otro)
		return @id <=> otro.getID
	end

	def to_s
		return "Variable: #{@id} | Type: #{@tipo} | Value: #{@valor.to_s}"
	end
end

class Tabla
	def initialize
		@simbolos = []
		@act = @simbolos
		@ant = []
		@duplicados = []
	end

	def error
		@duplicados.sort!
		@duplicados.each_index do |i|
			if i+1 < @duplicados.length
				if @duplicados[i]!=@duplicados[i+1]
					print "\n"
				end
			end
			print @duplicados[i].getID + ", "
		end
	end

	def chequeo(lista=@simbolos)
		lista.each do |x|
			if x.class == Array
				chequeo(x)
			else
				if lista.rindex(x)!=lista.index(x)
					@duplicados << x
				end
			end
		end
		return @duplicados.length != 0
	end


	def imprimir(lista=@simbolos.first, ind=0)
		puts " "*ind + "Begin scope"
		if lista
			lista.each do |x|
				if(x.class == Array)
					imprimir(x, ind+4)
				else
					puts " "*ind + x.to_s
				end
			end
		end
		puts " "*ind + "End scope"
	end

	def addscope
		@ant << @act
		@act << []
		@act = @act.last
	end

	def endscope
		@act = @ant.pop
	end

	def insert(tipo, id)
		simbolo = Simbolo.new(tipo, id)
		@act << simbolo
	end


	def update(id, nivel, valor, lista=@simbolos.first)
		posible = nil
		if lista
			lista.each_index do |x|
				if lista[x].class == Array and nivel-1 > 0
					posible = update(id,nivel-1, valor, lista[x])
					if(nil != posible)
						#return posible
					end
					nivel = nivel-1
				elsif lista[x].class != Array and posible == nil
					if id == lista[x].getID
						lista[x].cambiarValor(valor)
						#return valor
					end
				end
			end
		end
	end

	def update2(id, nivel, valor, lista=@simbolos.first)
		posible = []
		if lista
			lista.each do |x|
				if x.class == Array
					posible << update(id,nivel-1, valor, x)
					nivel = nivel-1
				else
					puts id+" == "+x.getID
					if id == x.getID
						#x.cambiarValor(valor)
						posible << x
					end
				end
			end
		end
		print posible[0]
		puts ""
		return posible[0]
	end


	def lookup(id, nivel, lista=@simbolos.first)
		posible = nil
		if lista
			lista.each do |x|
				if x.class == Array and nivel-1 > 0
					posible = lookup(id,nivel-1,x)
					if(nil != posible)
						return posible
					end
					nivel = nivel-1
				elsif x.class != Array and posible == nil
					if id == x.getID
						return x
					end
				end
			end
		end
		return posible
	end
end