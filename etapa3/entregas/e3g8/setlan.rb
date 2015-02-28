#!/usr/bin/env ruby

require_relative './Lexer'
require_relative './Parser'

argumentos = ARGV
imprimir_tokens = false
imprimir_ast = false
imprimir_tabla = false

if argumentos.count == 1
	imprimir_tabla = true
end

while argumentos.count > 1
	case argumentos.first
	when "-t"
		imprimir_tokens = true
	when "-a"
		imprimir_ast = true
	when "-s"
		imprimir_tabla = true
	end
	argumentos = argumentos.drop(1)
end

nombre_archivo = argumentos.first
archivo = open(nombre_archivo, "r")
tokens = Lexer.new
if tokens.analizar(archivo)
	parser = Parser.new(tokens)
	handler = parser.parse
	handler.result

	handler.chequeo
	if handler.hayErrorTabla
		puts "Existen variables declaradas varias veces en el mismo alcanze"
	end
	if handler.hayErrorTipo
		puts "Existen expresiones con errores de tipo"
	end
	if not (handler.hayErrorTabla or handler.hayErrorTipo)
		handler.imprimir(imprimir_tokens, tokens, imprimir_ast, imprimir_tabla)
	end
end
