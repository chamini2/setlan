#!/usr/bin/env ruby

class Simbolo
	def initialize(tipo, id)
		@id = id
		@tipo = tipo
		if tipo == "int"
			@valor = 0
		elsif tipo == "bool"
			@valor = false
		elsif tipo == "set"
			@valor = []
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
		if @valor.class == Array
			valors = @valor.to_s.gsub("[","{").gsub("]","}")
		else
			valors = @valor
		end
		return "Variable: #{@id} | Type: #{@tipo} | Value: #{valors}"
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
		print @duplicados
		puts ""
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
		lista.each do |x|
			if(x.class == Array)
				imprimir(x, ind+4)
			else
				puts " "*ind + x.to_s
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

	def delete
	end

	def update
	end

	def contains
	end

	def lookup(id, nivel, lista=@simbolos.first)
		posible = nil
		lista.each do |x|
			if x.class == Array and nivel > 0
				posible = lookup(id,nivel,x)
				if(nil != posible)
					return posible
				end
			elsif x.class != Array and posible == nil
				if id == x.getID
					return x
				end
			end
		end
		return posible
	end
end