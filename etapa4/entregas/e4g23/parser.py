from lexer import *
import ply.yacc as yacc
import config
from ast import *
from st import *


def p_program(p):
    "program : Program statement"
    p[0] = Program(p[2])


def p_assign(p):
    "statement : ID Assign expression"
    global lexer, static_checking, parsing_errors
    p[0] = Assign(Variable(p[1], lineno=p.lineno(1), 
                           column=p.lexpos(1) - lexer.current_column), 
                  p[3],
                  lineno=p.lineno(2), column=p.lexpos(2) - lexer.current_column)
    try:
        if int(p[3]):
            if (p[3] > 2**31-1):
                config.static_checking_errors += 'Error: Overflow in line '+ str(p.lineno(1))+', column '+str( p.lexpos(1) - lexer.current_column) + '.\n' 
            if (p[3] < -2**31 + 1):
                config.static_checking_errors += 'Error: Underflow in line '+ str(p.lineno(1))+', column '+str( p.lexpos(1) - lexer.current_column) + '.\n'
    except:
        pass
    if static_checking: p[0].typecheck()


def p_block(p):
    """statement : OpenCurly statement_list SemiColon CloseCurly
                 | OpenCurly Using new_scope declarations_list SemiColon scope_filled In statement_list CloseCurly
                 | """
    global static_checking
    if len(p) == 5:  p[0] = Block(p[2])
    elif len(p) == 10:
        p[0] = Block(p[8],p[4])
        if static_checking:
            indent = (len(config.scopes_list)-1)*4 
            config.static_checking_log += indent*' ' + 'End Scope\n'
            config.scopes_list.pop()
    else: p[0] = None


def p_scope_filled(p):
    'scope_filled :'
    global static_checking
    if static_checking:
        indent = (len(config.scopes_list)-1)*4
        config.static_checking_log += indent*' ' + 'Scope\n'
        for v in config.scopes_list[len(config.scopes_list)-1].scope.values():
            config.static_checking_log += (indent+4)*' ' + 'Variable: ' + v.name + ' | Type: ' + \
                                    v.return_type + ' | Value: ' + str(v.value) + '\n'


def p_new_scope(p):
    'new_scope :'
    global static_checking
    if static_checking: config.scopes_list.append(SymbolTable())


def error_redeclaration(var):
    config.static_checking_errors += 'Error: Redeclaration: variable \''+var.name+\
        '\', in line '+str(var.lineno)+', column '+str(var.column)+'.\n'


def p_declarations_list(p):
    """declarations_list : type variable_list
                         | declarations_list SemiColon type variable_list"""
    global static_checking, dynamic_checking
    if len(p) == 3:
        p[0] = [(p[1], p[2])]
        if static_checking or dynamic_checking: 
            for var in p[2]:
                if config.scopes_list[len(config.scopes_list)-1].contains(var.name):
                    error_redeclaration(var)
                else:
                    config.scopes_list[len(config.scopes_list)-1].insert(var)
    else:
        p[0] = p[1] + [(p[3], p[4])]
        if static_checking or dynamic_checking: 
            for var in p[4]:
                if config.scopes_list[len(config.scopes_list)-1].contains(var.name):
                    error_redeclaration(var)
                else:
                    config.scopes_list[len(config.scopes_list)-1].insert(var)


def p_variable_list(p):
    """variable_list : ID
                     | variable_list Comma variable_list"""
    global lexer
    var_value = False if actual_type == 'bool' else (0 if actual_type == 'int' else {})
    if len(p) == 2:
        p[0] = [Variable(p[1], return_type=actual_type, value=var_value, lineno=p.lineno(1), column=p.lexpos(1)-lexer.current_column)]
    else: p[0] = p[1] + p[3]


def p_statement_list(p):
    """statement_list : statement
                      | statement_list SemiColon statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_type(p):
    """type : Int
            | Bool
            | Set"""
    global static_checking, actual_type
    p[0] = p[1]
    if static_checking: actual_type = p[1]


def p_scan(p):
    "statement : Scan ID"
    global static_checking, lexer
    p[0] = Scan(Variable(p[2], lineno=p.lineno(2), 
                         column=p.lexpos(2)-lexer.current_column),
                lineno=p.lineno(1), column=p.lexpos(1)-lexer.current_column)
    if static_checking: p[0].typecheck()


def p_print(p):
    """statement : Print expression_list
                 | Println expression_list"""
    if p[1] == 'print':
        p[0] = Print(p[2])
    else:
        p[0] = Println(p[2])


def p_expression_list(p):
    """expression_list : expression
                       | expression_list Comma expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_bool_expression(p):
    'if_expression : expression'
    global static_checking
    p[0] = p[1]
    if static_checking:
        If(p[1],lineno=p[1].lineno,column=p[1].column).typecheck()


def p_if(p):
    """statement : If OpenParen if_expression CloseParen statement
                 | If OpenParen if_expression CloseParen statement Else statement"""
    global dynamic_checking
    if len(p) == 6:
        p[0] = If(expression=p[3], statement1=p[5],lineno=p[3].lineno,
                  column=p[3].column)
    else:
        p[0] = If(expression=p[3], statement1=p[5], statement2=p[7],
                  lineno=p[3].lineno, column=p[3].column)


def p_ID_for(p):
    'ID_for : ID'
    global static_checking
    p[0] = p[1]
    if static_checking:
        config.scopes_list[len(config.scopes_list)-1].insert(Variable(p[1],
                                                return_type='int',value=0,
                                                lineno=p.lineno(1),
                                                column=p.lexpos(1)-lexer.current_column))


def p_for_expression(p):
    'for_expression : expression'
    global static_checking
    p[0] = p[1]
    if static_checking:
        For(expression=p[1], lineno=p[1].lineno, column=p[1].column).typecheck()


def p_for(p):
    """statement : For new_scope ID_for scope_filled Min for_expression Do statement
                 | For new_scope ID_for scope_filled Max for_expression Do statement"""
    global lexer, static_checking
    p[0] = For(Variable(p[3], return_type='int',value=0,
                        lineno=p.lineno(3),column=p.lexpos(3)-lexer.current_column), 
                        order=p[5], expression=p[6], statement=p[8])
    if static_checking:
        indent = (len(config.scopes_list)-1)*4
        config.static_checking_log += indent*' ' + 'End Scope\n'
        config.scopes_list.pop()


def p_repeat_expression(p):
    'repeat_expression : expression'
    global static_checking
    p[0] = p[1]
    if static_checking:
        Repeat(expression=p[1], lineno=p[1].lineno, column=p[1].column).typecheck()


def p_repeat(p):
    """statement : Repeat statement While OpenParen repeat_expression CloseParen Do statement
                 | Repeat statement While OpenParen repeat_expression CloseParen
                 | While OpenParen repeat_expression CloseParen Do statement"""
    if len(p) == 9:
        p[0] = Repeat(p[2], p[5], p[8])
    elif p[1] == 'repeat':
        p[0] = Repeat(p[2], p[5], None)
    elif p[1] == 'while':
        p[0] = Repeat(None, p[3], p[6])
        

precedence = (
    # bool x bool -> bool
    ("left", 'Or'),
    ("left", 'And'),
    ("right", 'Not'),
    # int x int -> bool
    ("nonassoc", 'LessThan', 'LessThanEq', 'GreaterThan', 'GreaterThanEq'),
    # int|set x int|set -> bool
    ("nonassoc", 'Equals', 'NotEquals'),
    # int x set -> bool
    ("nonassoc", 'Contains'),     
    # int
    ("left", 'Plus', 'Minus'),
    ("left", 'Times', 'Div', 'Mod'),
    # set x set -> set
    ("left", 'Union', 'Difference'),
    ("left", 'Intersect'),
    # int x set -> set
    ("left", 'PlusSet', 'MinusSet'),
    ("left", 'TimesSet', 'DivSet', 'ModSet'),          
    # set -> set    (unary set operators)
    ("right", 'MaxSet'),
    ("right", 'MinSet'),
    ("right", 'Len'),
    # Unary minus / negation
    ("right", 'Uminus'),
)


def p_int(p):
    "expression : Number"
    global lexer
    p[0] = Int(p[1],p.lineno(1),p.lexpos(1)-lexer.current_column)


def p_bool(p):
    """expression : True
                  | False"""
    global lexer
    p[0] = Bool(p[1].lower(), p.lineno(1), p.lexpos(1) - lexer.current_column)


def p_string(p):
    "expression : String"
    global lexer
    p[0] = String(p[1], p.lineno(1), p.lexpos(1) - lexer.current_column)


def p_id(p):
    "expression : ID"
    global lexer
    p[0] = Variable(p[1], lineno = p.lineno(1), column = p.lexpos(1) - lexer.current_column)


def p_set_elements_list(p):
    """set_elements_list : Number
                         | arithmetic_op
                         | ID
                         | set_elements_list Comma Number
                         | set_elements_list Comma ID
                         | set_elements_list Comma arithmetic_op"""
    global lexer
    if len(p) == 2:
        try:
            if int(p[1]): p[0] = [Int(p[1], p.lineno(1), p.lexpos(1) - lexer.current_column)]
        except:
            p[0] = [Variable(p[1], lineno=p.lineno(1),
                             column=p.lexpos(1) - lexer.current_column)]
    else:
        try:
            if int(p[3]):
                p[0] = p[1] + [Int(p[3], p.lineno(1), p.lexpos(1) - lexer.current_column)]
        except:
            if p[1] == None: p[1] = [Int('0',p.lineno(1), p.lexpos(1) - lexer.current_column)]
            p[0] = p[1] + [Variable(p[3], lineno=p.lineno(1), 
                                    column=p.lexpos(1) - lexer.current_column)]


def p_set(p):
    """expression : OpenCurly set_elements_list CloseCurly
                  | OpenCurly CloseCurly"""
    global lexer
    p[0] = Set(p[2], p.lineno(1), p.lexpos(1) - lexer.current_column)


def p_parenthesis(p):
    """expression : OpenParen expression CloseParen"""
    p[0] = p[2]


def p_arithmetic_op(p):
    """arithmetic_op : expression Plus expression
                     | expression Minus expression
                     | expression Times expression
                     | expression Div expression
                     | expression Mod expression"""
    
    global lexer, static_checking, parsing_errors
    if p[2] == '+': p[0] = Plus(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
    elif p[2] == '-': p[0] = Minus(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
    elif p[2] == '*': p[0] = Times(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
    elif p[2] == '/': p[0] = Div(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
    elif p[2] == '%': p[0] = Mod(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
    if static_checking: p[0].typecheck()


def p_binop_(p):
    """expression : expression PlusSet expression
                  | expression MinusSet expression
                  | expression TimesSet expression
                  | expression DivSet expression
                  | expression ModSet expression
                  | expression LessThan expression
                  | expression LessThanEq expression
                  | expression GreaterThan expression
                  | expression GreaterThanEq expression
                  | expression Equals expression
                  | expression NotEquals expression
                  | expression Union expression
                  | expression Difference expression
                  | expression Intersect expression
                  | expression And expression
                  | expression Or expression
                  | expression Contains expression
                  | arithmetic_op"""

    if len(p) != 2:
        global lexer
        if p[2] == '<+>': p[0] = PlusSet(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '<->': p[0] = MinusSet(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '<*>': p[0] = TimesSet(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '</>': p[0] = DivSet(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '<%>': p[0] = ModSet(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '<': p[0] = LessThan(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '<=': p[0] = LessThanEq(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '>': p[0] = GreaterThan(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '>=': p[0] = GreaterThanEq(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '==': p[0] = Equals(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '/=': p[0] = NotEquals(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '++': p[0] = Union(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '\\': p[0] = Difference(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column) 
        elif p[2] == '><': p[0] = Intersect(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == 'and': p[0] = And(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == 'or': p[0] = Or(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        elif p[2] == '@': p[0] = Contains(p[1], p[3], p.lineno(2), p.lexpos(2)-lexer.current_column)
        if static_checking: p[0].typecheck()
    else:
        p[0] = p[1]


def p_unary_op(p):
    """expression : Minus expression %prec Uminus
                  | Not expression
                  | Len expression
                  | MaxSet expression
                  | MinSet expression"""
    global static_checking, parsing_errors
    if p[1] == '-': p[0] = Uminus(p[2], p.lineno(1), p.lexpos(1)-lexer.current_column)
    elif p[1] == 'not': p[0] = Not(p[2], p.lineno(1), p.lexpos(1)-lexer.current_column)
    elif p[1] == '$?': p[0] = Len(p[2], p.lineno(1), p.lexpos(1)-lexer.current_column)
    elif p[1] == '>?': p[0] = MaxSet(p[2], p.lineno(1), p.lexpos(1)-lexer.current_column)
    elif p[1] == '<?': p[0] = MinSet(p[2], p.lineno(1), p.lexpos(1)-lexer.current_column)
    if static_checking: p[0].typecheck()


def p_error(p):
    global parsing_errors, lexer
    parsing_errors += 'Error: Unexpected \''+str(p.value)+'\' in line '+str(p.lineno)+', column '+str(p.lexpos - lexer.current_column)+'.\n'


parsing_errors = ''
config.static_checking_log = ''
actual_type = None
static_checking = True


def mainFlags(argv):
    global parsing_errors, lexer, actual_type, static_checking
    lexer_return = mainLexer(argv[1])

    if lexer_return.count('Error:') != 0: return lexer_return
    if '-t' in argv:
        if len(argv) == 3: return lexer_return
        else: print lexer_return

    lexer = lex.lex()
    lexer.current_column = -1
    lexer.input(open(argv[1],'r').read())
    config.static_checking_log = ''
    config.scopes_list = []
    actual_type = None
    parsing_errors = ''
    static_checking = True
    dynamic_checking = False
    config.static_checking_errors = ''
    parser = yacc.yacc()
    input_file = open(argv[1],'r').read()
    ast = parser.parse(input_file)

    if parsing_errors != '': return parsing_errors
    if '-a' in argv:
        if len(argv) == 3: return ast.repr()
        else: print ast.repr()

    if config.static_checking_errors != '':
        return config.static_checking_errors
    if '-s' in argv:
        if len(argv) == 3: return config.static_checking_log
        else: print config.static_checking_log
    if len(argv) != 2: return
    static_checking = False
    config.dynamic_checking_log = ''
    config.scopes_list = []
    ast.execute()
    if '--testing' in argv:
        print 'WWOWOWOWOWOWOWOW'
        return config.dynamic_checking_log



if __name__ == '__main__':
    print(mainFlags(sys.argv))




