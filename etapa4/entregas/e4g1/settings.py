global ST
global ErrorLex
global ErrorVer
global ErrorSin
ST = None
ErrorSin = False
ErrorLex = False
ErrorVer = False

def formatString(s):
  s = s.replace("\\\\","\\") 
  s = s.replace('\\"','\"') 
  s = s.replace("\\n","\n") 
  return s