# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # #
#	TRADUCTORES E INTERPRETADORES CI3725      #
#	Cuarta entrega del proyecto.              #
#   Interpretador para el lenguaje Setlan     #
#	Autores: Carlos Martínez 	- 11-10584    #
#			 Christian Teixeira - 11-11016    #
# # # # # # # # # # # # # # # # # # # # # # # #

from sys import stdout, stdin
printf = stdout.write
read = stdin.readline

error_intr = []
SymTab = None
lines = []
num_scopes = 0
indent_level = 0
scopes_stack = []

def interpreter_traverser(AST):
	global error_intr
	global num_scopes
	global indent_level
	global scopes_stack
	if AST.type == "block":
		num_scopes += 1
		indent_level += 1
		scopes_stack.append(num_scopes)

	elif AST.type == "for_stmt":
		iter_set = evaluate(AST.children[3])
		num_scopes += 1
		scopes_stack.append(num_scopes)
		iter_var = AST.children[0].children[0].val
		iter_dir = AST.children[1].children[0].val
		do_stmt = AST.children[4]
		iter_list = sorted(iter_set)
		for scope in scopes_stack:
			if SymTab.contains(iter_var, scope):
				act_scope = scope
		if iter_dir == "max": iter_list.reverse()
		for elem in iter_list:
			temp_stack = scopes_stack
			temp_numscopes = num_scopes
			SymTab.update(iter_var, act_scope, "int", str(elem), SymTab.lin_decof(iter_var, num_scopes))
			interpreter_traverser(do_stmt)
			scopes_stack = temp_stack
			num_scopes = temp_numscopes
		update_numscopes(do_stmt)
		scopes_stack.pop()
		return

	elif AST.type == "block_end":
		indent_level -= 1
		scopes_stack.pop()

	elif AST.type == "print":
		elements = AST.children[0].children
		string = ""
		for elem in elements:
			if elem.type == "str_stmt":
				act = elem.children[0].val[1:-1]

				# Identificar Regex
				act = act.split("\\n")
				for i in range(len(act)-1):
					string = string + act[i] + "\n"
				if act[-1] != "''":
					string = string + act[-1]
			else:
				act_value = evaluate(elem)
				if act_value is True or act_value is False:
					if act_value: act_string = "true"
					else: act_string = "false"
				else:
					act_string = str(act_value)
				if act_string[:3] == "set":
					act_string = "{"
					act_value = sorted(list(act_value))
					for elem in act_value:
						act_string += str(elem) + ","
					if act_string == "{":
						act_string = "{}"
					else:
						act_string = act_string[:-1] + "}"
				string += act_string
		printf(string)

	elif AST.type == "scan":
		max_int = 2147483646
		variable = AST.children[0].children[0]
		for scope in scopes_stack:
			if SymTab.contains(variable.val, scope):
				act_scope = scope
		varType = SymTab.typeof(variable.val, act_scope)
		
		value = read()
		value = value.split("\n")[0]
		valueType = ""

		try:
			value = int(value)
		except ValueError:
			pass
		else:
			valueType = "int"

		if value == "true" or value == "false":
			valueType = "bool"
		elif valueType != "int":
			valueType = "error"
		
		if valueType != varType:
			# Agrega el error a la lista
			if valueType == "bool" or valueType == "int":
				print("ERROR: No se le puede asignar a la variable '" + str(variable.val) + "' de tipo '" + str(varType) + "' una entrada de tipo '" + str(valueType) + "' en la fila " + str(variable.lineno) + ", columna " + str(getcol(variable.lineno,variable.colno)) + ".")
				exit(1)
			else:
				print("ERROR: No se reconoce la entrada.")
				exit(1)
		else:
			if valueType == "int" and value > max_int:
				print("ERROR: La entrada ha causado overflow.")
				exit(1)
			SymTab.update(variable.val, act_scope, varType, value, SymTab.lin_decof(variable.val, num_scopes))

	elif AST.type == "vardec":
		vardec = str(AST.val)
		vartype = vardec.split()[0]
		varname = vardec.split()[1]
		if vartype == "int": val = "0"
		elif vartype == "bool": val = "false"
		elif vartype == "set": val = "{}"
		SymTab.update(varname, num_scopes, vartype, val, SymTab.lin_decof(varname, num_scopes))


	elif AST.type == "assign":
		assign_var = AST.children[0].children[0].val
		expr = AST.children[1].children[0]
		expr_val = evaluate(expr)
		for scope in scopes_stack:
			if SymTab.contains(assign_var, scope):
				act_scope = scope
		assign_var_type = SymTab.typeof(assign_var, act_scope)
		if assign_var_type == "int":
			SymTab.update(assign_var, act_scope, assign_var_type, expr_val, SymTab.lin_decof(assign_var, num_scopes))
		elif assign_var_type == "bool":
			if expr_val:
				SymTab.update(assign_var, act_scope, assign_var_type, "true", SymTab.lin_decof(assign_var, num_scopes))
			else:
				SymTab.update(assign_var, act_scope, assign_var_type, "false", SymTab.lin_decof(assign_var, num_scopes))
		elif assign_var_type == "set":
			strto_assign = "{"
			expr_val = sorted(expr_val)
			for elem in expr_val:
				strto_assign += str(elem) + ","
			if strto_assign == "{":
				SymTab.update(assign_var, act_scope, assign_var_type, "{}", SymTab.lin_decof(assign_var, num_scopes))
			else:
				SymTab.update(assign_var, act_scope, assign_var_type, strto_assign[:-1]+"}", SymTab.lin_decof(assign_var, num_scopes))

	elif AST.type == "if_stmt":
		if_expr = AST.children[0].children[0]
		if_expr_val = evaluate(if_expr)
		if if_expr_val:
			interpreter_traverser(AST.children[1])
			return
		update_numscopes(AST.children[1])
		if len(AST.children) > 2:
			if not if_expr_val: interpreter_traverser(AST.children[2])
		return

	# Recorre los hijos del nodo actual
	if AST.children:
		to_ignore = []
		for i in range(len(AST.children)):
			ch = True
			if not i in to_ignore:
				if AST.children[i].type == "repeat_stmt":
					to_ignore.append(i+1)

					if i+1 < len(AST.children)-1:
						# Caso Repeat, While Do
						if AST.children[i+2].type == "do_stmt":
							exec_repeatwhile(AST.children[i], AST.children[i+1], AST.children[i+2])
						else:
							# Caso Repeat, While
							exec_repeatwhile(AST.children[i], AST.children[i+1], None)
					# Caso Repeat, While tambien
					else:
						exec_repeatwhile(AST.children[i], AST.children[i+1], None)
				elif AST.children[i].type == "while_stmt":
					exec_while(AST.children[i],AST.children[i+1])
				elif AST.children[i].type == "do_stmt":
					pass
				else:
					ch = interpreter_traverser(AST.children[i])
				if ch == False:
					return False


def execute(AST, ST, lineas):
	global SymTab
	global lines
	lines = lineas
	SymTab = ST
	inter = interpreter_traverser(AST)

	if inter == None:
		return True
	else:
		return False

def getcol(lineno, lexpos):
	global lines
	aux = 0
	for i in range(lineno - 1):
		aux = aux + len(lines[i])
	return str(lexpos - aux + 1)


def evaluate(expr):
	max_int = 2147483646

	# Casos base
	if expr.type == "int_stmt" or expr.type == "set_stmt":
		if expr.type == "set_stmt":
			actual_set = []
			for child in expr.children:
				toappend = evaluate(child)
				actual_set.append(int(toappend))
			return set(actual_set)
		else:
			return expr.children[0].val
	if expr.type == "const_stmt":
		return expr.children[0].val == "true"
	if expr.type == "var_stmt":
		for scope in scopes_stack:
			if SymTab.contains(expr.children[0].val, scope):
				act_scope = scope
		vartype = SymTab.typeof(expr.children[0].val, act_scope)
		if vartype == "int":
			return SymTab.valof(expr.children[0].val, act_scope)
		elif vartype == "bool":
			return SymTab.valof(expr.children[0].val, act_scope) == "true"
		elif vartype == "set":
			actual_set = SymTab.valof(expr.children[0].val, act_scope)
			if actual_set == "{}":
				return set([])
			else:
				actual_set = actual_set[1:-1].split(",")
				for i in range(len(actual_set)):
					actual_set[i] = int(actual_set[i])
				return set(actual_set)

	# Operadores de enteros
	if expr.type == "expr_binopr":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "+": to_return = int(opr_a) + int(opr_b)
		elif expr.val.split()[1] == "-": to_return = int(opr_a) - int(opr_b)
		elif expr.val.split()[1] == "*": to_return = int(opr_a) * int(opr_b)
		elif expr.val.split()[1] == "%":
			if int(opr_b) == 0:
				print("ERROR: Operador módulo por cero en la fila " + str(expr.lineno) + " columna " + str(getcol(expr.lineno, expr.colno)))
				exit(1)
			else:
				to_return = int(opr_a) % int(opr_b)
		elif expr.val.split()[1] == "/":
			if int(opr_b) == 0:
				print("ERROR: División por cero en la fila " + str(expr.lineno) + " columna " + str(getcol(expr.lineno,expr.colno)))
				exit(1)
			else:
				to_return = int(opr_a) / int(opr_b)
		if to_return > max_int:
			print("ERROR. Overflow en la operación en la linea " + str(expr.lineno) + " columna " + str(getcol(expr.lineno,expr.colno)))
			exit(1)
		return to_return

	if expr.type == "expr_cmpopr":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		if "set" in str(opr_a):
			if expr.val.split()[1] == "==": return opr_a == opr_b
			elif expr.val.split()[1] == "/=": return not opr_a == opr_b
		else:
			opr_a = int(opr_a)
			opr_b = int(opr_b)
			if expr.val.split()[1] == ">": return opr_a > opr_b
			elif expr.val.split()[1] == "<": return opr_a < opr_b
			elif expr.val.split()[1] == ">=": return opr_a >= opr_b
			elif expr.val.split()[1] == "<=": return opr_a <= opr_b
			elif expr.val.split()[1] == "==": return opr_a == opr_b
			elif expr.val.split()[1] == "/=": return not opr_a == opr_b

	if expr.type == "negate_stmt":
		opr_a = evaluate(expr.children[0])
		return -int(opr_a)

	# Operadores de booleanos

	if expr.type == "bool_binopr":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "or": return opr_a or opr_b
		if expr.val.split()[1] == "and": return opr_a and opr_b

	if expr.type == "not_stmt":
		opr_a = evaluate(expr.children[0])
		return not opr_a

	# Operadores de conjuntos

	if expr.type == "expr_setcont":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		return int(opr_a) in opr_b

	if expr.type == "set_binopr":
		opr_a = evaluate(expr.children[0])
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "++":
			if len(opr_a) == 0:
				return opr_b
			elif len(opr_b) == 0:
				return opr_a
			for elem in opr_b:
				opr_a.add(elem)
			return opr_a
		elif expr.val.split()[1] == "><":
			new_set = set([])
			for elem in opr_a:
				if elem in opr_b:
					new_set.add(elem)
			return new_set
		elif expr.val.split()[1] == "\\":
			new_set = set([])
			for elem in opr_a:
				if not elem in opr_b:
					new_set.add(elem)
			return new_set

	if expr.type == "set_mapopr":
		opr_a = int(evaluate(expr.children[0]))
		opr_b = evaluate(expr.children[1])
		if expr.val.split()[1] == "<+>":
			new_set = set([])
			for elem in opr_b:
				to_add = opr_a + elem
				if to_add > max_int:
					print("ERROR. Overflow en la operación en la linea " + str(expr.lineno) + " columna " + str(getcol(expr.lineno,expr.colno)))
					exit(1)
				new_set.add(opr_a + elem)
			return new_set
		elif expr.val.split()[1] == "<->":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a - elem)
			return new_set
		elif expr.val.split()[1] == "<*>":
			new_set = set([])
			for elem in opr_b:
				to_add = opr_a * elem
				if to_add > max_int:
					print("ERROR. Overflow en la operación en la linea " + str(expr.lineno) + " columna " + str(getcol(expr.lineno,expr.colno)))
					exit(1)
				new_set.add(to_add)
			return new_set
		elif expr.val.split()[1] == "</>":
			new_set = set([])
			for elem in opr_b:
				if elem == 0:
					print("ERROR: División por cero en la fila " + str(expr.lineno) + " columna " + str(getcol(expr.lineno,expr.colno)))
					exit(1)
				new_set.add(opr_a / elem)
			return new_set
		elif expr.val.split()[1] == "<%>":
			new_set = set([])
			for elem in opr_b:
				new_set.add(opr_a % elem)
			return new_set

	if expr.type == "set_unropr":
		opr_a = evaluate(expr.children[0])
		if expr.val.split()[1] == ">?" and len(opr_a) > 0: return max(opr_a)
		elif expr.val.split()[1] == "<?" and len(opr_a) > 0: return min(opr_a)
		elif expr.val.split()[1] == "$?": return len(opr_a)
		print("ERROR: Línea " + str(expr.lineno) + " columna " + str(getcol(expr.lineno,expr.colno)) + ". El operador '" + expr.val.split()[1] + "' no acepta conjuntos vacios.")
		exit(1)


def exec_while(while_stmt, do_stmt):
	global scopes_stack
	global num_scopes
	w_condition = while_stmt.children[0].children[0]
	while evaluate(w_condition):
		temp_stack = scopes_stack
		temp_numscopes = num_scopes
		interpreter_traverser(do_stmt)
		scopes_stack = temp_stack
		num_scopes = temp_numscopes
	update_numscopes(do_stmt)

def exec_repeatwhile(repeat_stmt, while_stmt, do_stmt):
	global scopes_stack
	global num_scopes
	if do_stmt is None:
		# Repeat While
		repeatdo_stmt = repeat_stmt.children[0]
		w_condition = while_stmt.children[0].children[0]
		temp_stack = scopes_stack
		temp_numscopes = num_scopes
		interpreter_traverser(repeat_stmt)
		scopes_stack = temp_stack
		num_scopes = temp_numscopes
		while evaluate(w_condition):
			temp_stack = scopes_stack
			temp_numscopes = num_scopes
			interpreter_traverser(repeat_stmt)
			scopes_stack = temp_stack
			num_scopes = temp_numscopes
		update_numscopes(repeat_stmt)
	else:
		# Repeat While Do
		repeatdo_stmt = repeat_stmt.children[0]
		w_condition = while_stmt.children[0].children[0]
		while True:
			temp_stack = scopes_stack
			temp_numscopes = num_scopes
			interpreter_traverser(repeatdo_stmt)
			if not evaluate(w_condition):
				break
			interpreter_traverser(do_stmt)
			scopes_stack = temp_stack
			num_scopes = temp_numscopes
		scopes_stack = temp_stack
		num_scopes = temp_numscopes
		update_numscopes(repeatdo_stmt)
		update_numscopes(do_stmt)

def update_numscopes(AST):
	global num_scopes
	if AST.type == "block" or AST.type == "for_stmt":
		num_scopes += 1
	for child in AST.children:
		update_numscopes(child)

def get_errors():
	global error_intr
	return error_intr