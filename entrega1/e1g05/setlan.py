#setlan.py
# Oriana Graterol 10-11248
# Samuel Rodriguez 09-10728
#!/usr/bin/python


import sys
from Lexer import *

def main():

	# Construimos el Lexer 
	m = Lexer()
	m.build()
	if (len(sys.argv) > 1):
		m.scanner(sys.argv[1])
	else:
		print "Verifique que la sintaxis introducida es correcta."
		print ".\\setlan <nombre del archivo>\n"


if __name__ == "__main__":
	main()


# END trinity.py
