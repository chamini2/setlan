import setlantable
import sys
import re

types = {'set':type(set()),'int':type(0),'bool':type(True)}
enteros = re.compile(r"^(-?)(\d+)$")
booleanos = re.compile(r"^(false|true)$")

def evaluate(arbol,Tabla):
	if(arbol[1]=="id"):
		y = Tabla.lookup(arbol[2])
		return y[2]
	elif(arbol[1]=="num"):
		return int(arbol[2])
	elif(arbol[1]=="neg"):
		ret = evaluate(arbol[3],Tabla)
		if(arbol[2] == "not"):
			return (not ret)
		else:
			return (ret * -1)
	elif(arbol[1]=="setu"):
		ret = evaluate(arbol[3],Tabla)
		if (arbol[2] == ">?"):
			if(ret == set()):
				print 'ERROR: empty set in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			else:
				for item in ret:
					max=item
					break
				for item in ret:
					if(item > max):
						max=item
				return max
		elif (arbol[2] == "<?"):
			if(ret == set()):
				print 'ERROR: empty set in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			else:
				for item in ret:
					min=item
					break
				for item in ret:
					if(item < min):
						min=item
				return min
		else:
			retur = len(ret)
			if(retur>2147483647 or retur<(-2147483648)):
				print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			return retur
	elif(arbol[1]=="base"):
		retur = set()
		for x in arbol[2]:
			retur.add(evaluate(x,Tabla))
		return retur
	elif(arbol[1]=="void"):
		return set()
	elif(arbol[1]=="bool"):
		if(arbol[2]=="true"):
			return True
		return False
	else:
		ret1 = evaluate(arbol[2],Tabla)
		ret2 = evaluate(arbol[3],Tabla)
		if(arbol[1]=="=="):
			return (ret1 == ret2)
		elif(arbol[1]=="/="):
			return (ret1 != ret2)
		elif(arbol[1]==">"):
			return (ret1 > ret2)
		elif(arbol[1]=="<"):
			return (ret1 < ret2)
		elif(arbol[1]==">="):
			return (ret1 >= ret2)
		elif(arbol[1]=="<="):
			return (ret1 <= ret2)
		elif(arbol[1]=="and"):
			return (ret1 and ret2)
		elif(arbol[1]=="or"):
			return (ret1 or ret2)
		elif(arbol[1]=="++"):
			return (ret1 | ret2)
		elif(arbol[1]=="><"):
			return (ret1 & ret2)
		elif(arbol[1]=="\\"):
			return (ret1 - ret2)#no estoy seguro de como definen la diferencia ustedes, asi que me voy por lo que dice wikipedia, a\b da los elementos de a que no estan en b
		elif(arbol[1]=="@"):
			for x in ret2:
				if(ret1 == x):
					return True
			return False
		elif(arbol[1]=="+"):
			retur = ret1 + ret2
			if(retur>2147483647 or retur<(-2147483648)):
				print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			return retur
		elif(arbol[1]=="-"):
			retur = ret1 - ret2
			if(retur>2147483647 or retur<(-2147483648)):
				print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			return retur
		elif(arbol[1]=="*"):
			retur = ret1 * ret2
			if(retur>2147483647 or retur<(-2147483648)):
				print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			return retur
		elif(arbol[1]=="/"):
			if(ret2 == 0):
				print 'ERROR: division by zero in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			retur = ret1 / ret2
			if(retur>2147483647 or retur<(-2147483648)):
				print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			return retur
		elif(arbol[1]=="%"):
			if(ret2 == 0):
				print 'ERROR: division by zero in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			retur = ret1 % ret2
			if(retur>2147483647 or retur<(-2147483648)):
				print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
				quit()
			return retur
		elif(arbol[1]=="<+>"):
			retur = set()
			for x in ret2:
				operation = ret1 + x
				if(operation>2147483647 or operation<(-2147483648)):
					print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				retur.add(operation)
			return retur
		elif(arbol[1]=="<->"):
			retur = set()
			for x in ret2:
				operation = ret1 - x
				if(operation>2147483647 or operation<(-2147483648)):
					print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				retur.add(operation)
			return retur
		elif(arbol[1]=="<*>"):
			retur = set()
			for x in ret2:
				operation = ret1 * x
				if(operation>2147483647 or operation<(-2147483648)):
					print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				retur.add(operation)
			return retur
		elif(arbol[1]=="</>"):
			retur = set()
			for x in ret2:
				if(x == 0):
					print 'ERROR: division by zero in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				operation = ret1 / x
				if(operation>2147483647 or operation<(-2147483648)):
					print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				retur.add(operation)
			return retur
		elif(arbol[1]=="<%>"):
			retur = set()
			for x in ret2:
				if(x == 0):
					print 'ERROR: division by zero in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				operation = ret1 % x
				if(operation>2147483647 or operation<(-2147483648)):
					print 'ERROR: overflow in operation at line '+str(arbol[4][1])+', column '+str(arbol[4][0])
					quit()
				retur.add(operation)
			return retur

def execute(arbol,Tabla):
	subs = iter(Tabla.subT)
	instrucRun(arbol[1],Tabla,subs)

def instrucRun(arbol,Tabla,subs):
    if(arbol[0]=="bloque"):
        bloqueRun(arbol,Tabla,subs)
    elif(arbol[0]=="leer"):
        leerRun(arbol,Tabla,subs)
    elif(arbol[0]=="imprimir"):
        imprimirRun(arbol,Tabla,subs)
    elif(arbol[0]=="asignar"):
        asignarRun(arbol,Tabla,subs)
    elif(arbol[0]=="if"):
        ifRun(arbol,Tabla,subs)
    elif(arbol[0]=="ciclo"):
        cicloRun(arbol,Tabla,subs)

def leerRun(arbol,Tabla,subs):
	variable = Tabla.lookup(arbol[1][0])
	inp = raw_input()
	if(variable[1]=='int'):
		match = enteros.match(inp)
		if match:
			valor = int(match.group(2))
			if(match.group(1)=='-'):
				valor*=-1
			if(valor>2147483647 or valor<(-2147483648)):
				print 'ERROR: overflow scanning variable at line '+str(arbol[1][1][1])+', column '+str(arbol[1][1][0])
				quit()
			variable[2] = valor
		else:
			print 'ERROR: scanning variable at line '+str(arbol[1][1][1])+', column '+str(arbol[1][1][0])
			quit()
	else:
		match = booleanos.match(inp)
		if match:
			if(match.group(1)=='false'):
				valor = False
			else:
				valor = True
			variable[2] = valor
		else:
			print 'ERROR: scanning variable at line '+str(arbol[1][1][1])+', column '+str(arbol[1][1][0])
			quit()


def cicloRun(arbol,Tabla,subs):
	if(arbol[1]==0):
		ret = evaluate(arbol[4],Tabla)
		ret = list(ret)
		hijo = subs.next()
		if(len(ret)==0):
			return
		if(arbol[3]=="min"):
			ret.sort()
		else:
			ret.sort(reverse=True)
		for x in ret:
			subs2 = iter(hijo.subT)
			hijo.localforceupdate(arbol[2],x)
			instrucRun(arbol[5],hijo,subs2)
	elif(arbol[1]==1):
		ret = evaluate(arbol[2],Tabla)
		hijo = subs.next()
		subs2 = iter(hijo.subT)
		while(ret):
			instrucRun(arbol[3],hijo,subs2)
			ret = evaluate(arbol[2],Tabla)
			subs2 = iter(hijo.subT)
	elif(arbol[1]==2):
		hijo = subs.next()
		if(arbol[2]):
			hijo2 = subs.next()
			subs3 = iter(hijo2.subT)
		subs2 = iter(hijo.subT)
		instrucRun(arbol[3],hijo,subs2)
		ret = evaluate(arbol[4],Tabla)
		while(ret):
			if(arbol[2]):
				instrucRun(arbol[5],hijo2,subs3)
				subs3 = iter(hijo2.subT)
			subs2 = iter(hijo.subT)
			instrucRun(arbol[3],hijo,subs2)
			ret = evaluate(arbol[4],Tabla)

def ifRun(arbol,Tabla,subs):
	ret = evaluate(arbol[2],Tabla)
	if ret:
		hijo = subs.next()
		subs2 = iter(hijo.subT)
		instrucRun(arbol[3],hijo,subs2)
		if(arbol[1]):
			subs.next()
	else:
		subs.next()
		hijo = subs.next()
		subs2 = iter(hijo.subT)
		if(arbol[1]):
			instrucRun(arbol[4],hijo,subs2)

def asignarRun(arbol,Tabla,subs):
	ret = evaluate(arbol[2],Tabla)
	Tabla.update(arbol[1],ret)

def imprimirRun(arbol,Tabla,subs):
	global types
	imprimir=''
	for x in arbol[2]:
		if(x[0]=="st"):
			tam = len(x[1])
			if(tam>2):
				bool = False
				for c in x[1][1:tam-1]:
					if(bool):
						if(c=='\\'):
							imprimir+=c
						if(c=='n'):
							imprimir+="\n"
						if(c=='"'):
							imprimir+=c
						bool=False
						continue
					if(c=='\\'):
						bool=True
						continue
					imprimir+=c
		else:
			ret = evaluate(x,Tabla)
			if(type(ret)==types['bool']):
				if(ret):
					imprimir+='true'
				else:
					imprimir+='false'
			if(type(ret)==types['int']):
				imprimir+=str(ret)
			if(type(ret)==types['set']):
				imprimir+='{'
				lista = list(ret)
				lista.sort()
				tam = len(lista)
				if(tam>0):
					for x in lista[0:tam-1]:
						imprimir+=" "+str(x)+','
					imprimir+=" "+str(lista[tam-1])+' '
				imprimir+='}'
	if(arbol[1]=="println"):
		imprimir+="\n"
	sys.stdout.write(imprimir)

def bloqueRun(arbol,Tabla,subs):
	if(arbol[1]==0):
		pass
	elif(arbol[1]==1):
		hijo = subs.next()
		subs2 = iter(hijo.subT)
		for x in arbol[2]:
			instrucRun(x,hijo,subs2)
		hijo.resetLocal()
	elif(arbol[1]==2):
		hijo = subs.next()
		subs2 = iter(hijo.subT)
		for x in arbol[3]:
			instrucRun(x,hijo,subs2)
		hijo.resetLocal()