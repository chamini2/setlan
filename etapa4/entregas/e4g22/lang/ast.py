#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# ast.py
#
# Setlan Abstract Syntactic Tree
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from config import SetlanConfig

from type import *

from sym_table import SymTable

from exceptions import (
    SetlanTypeError,
    SetlanSyntaxError,
    SetlanStaticErrors,
    SetlanScopeError,
    SetlanZeroDivisionError,
    SetlanOverflowError,
    SetlanEmptySetError,
    SetlanZeroDivisionError,
    SetlanReadOnlyModificationError
    )

class Setlan(SetlanConfig):

    def __init__(self, instruction, *args, **kwargs):
        super(Setlan, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._instruction = instruction

    def __unicode__(self):
        string = self.print_ast(0)
        return string

    def print_ast(self, level):
        string = "Setlan Program:\n%s" % self._instruction.print_ast(level+1)
        return string

    def staticChecks(self):
        st = self._check(None)
        while st.getFather() is not None:
            st = st.getFather()
        return st

    def _check(self, symtable):
        check = self._instruction._check(symtable)
        if isinstance(check, SymTable):
            return check
        else:
            return SymTable(father=None)

    def execute(self):
        self._execute(None)

    def _execute(self, symtable):
        self._instruction._execute(symtable)


class Printable(Setlan):

    def __init__(self, *args, **kwargs):
        super(Printable, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)

    def print_ast(self, level):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)

    def isSet(self):
        return self._expected_type.isSet()

    def isInt(self):
        return self._expected_type.isInt()

    def isBool(self):
        return self._expected_type.isBool()


class Instruction(Setlan):

    def __init__(self, *args, **kwargs):
        super(Instruction, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)

    def print_ast(self, level):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)

    def _check(self, symtable):
        print "%s: Check function Not Implemented" % (self.__class__.__name__)

    def _check_for_counter_modification(self, name, symtable):
        print "%s: Check for counter modification Not Implemented" % (self.__class__.__name__)

    def _execute(self, symtable):
        print "%s: Execute function Not Implemented" % (self.__class__.__name__)

    def _evaluate(self, symtable):
        print "%s: Evaluate function Not Implemented" % (self.__class__.__name__)


class Declaration(Setlan):

    def print_ast(self, level):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)


class Expression(Printable):

    def __init__(self, *args, **kwargs):
        super(Expression, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._expected_type = Type(position=self._position)

    def _execute(self, symtable):
        print "%s: Execute function Not Implemented" % (self.__class__.__name__)

    def _evaluate(self, symtable):
        print "%s: Evaluate function Not Implemented" % (self.__class__.__name__)


class String(Printable):

    def __init__(self, value, *args, **kwargs):
        super(String, self).__init__(args,kwargs)
        self._value = value[1:len(value)-1]

    def print_ast(self, level):
        string = "%sString: %s" % (
            self._get_indentation(level),
            str(self._value)
            )
        return string

    def _check(self, symtable):
        return True

    def _evaluate(self, symtable):
        return self._value

    def isSet(self):
        return False

    def isInt(self):
        return False

    def isBool(self):
        return False


class Block(Instruction):

    def __init__(self, declarations, instructions, *args, **kwargs):
        super(Block, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._declarations = declarations
        self._instructions = instructions

    def print_ast(self, level):
        string = "%sBlock Instruction:" % self._get_indentation(level)
        if self._declarations is not None and self._declarations:
            string += "\n%sVariable Declarations:" % self._get_indentation(level+1)
            for declaration in self._declarations:
                string += "%s" % declaration.print_ast(level+2)
        if self._instructions is not None and self._instructions:
            string += "\n%sInstructions:" % self._get_indentation(level+1)
            for instruction in self._instructions:
                string += "\n%s" % instruction.print_ast(level+2)
        return string

    def _fill_symtable(self, symtable):
        new_symtable = None
        if self._declarations is not None and self._declarations:
            new_symtable = SymTable(father=symtable)
            for declaration in self._declarations:
                declaration._check(new_symtable)
        else:
            new_symtable = symtable
        return new_symtable

    def _check(self, symtable):
        new_symtable = self._fill_symtable(symtable)
        if self._instructions is not None and self._instructions:
            for instruction in self._instructions:
                instruction._check(new_symtable)
        if symtable is None:
            return new_symtable
        else:
            return True

    def _check_for_counter_modification(self, name, symtable):
        new_symtable = self._fill_symtable(symtable)
        if self._instructions is not None and self._instructions:
            for instruction in self._instructions:
                instruction._check_for_counter_modification(name, new_symtable)

    def _execute(self, symtable):
        new_symtable = self._fill_symtable(symtable)
        if self._instructions is not None and self._instructions:
            for instruction in self._instructions:
                instruction._execute(new_symtable)


class Assignment(Instruction):

    def __init__(self, variable, value, *args, **kwargs):
        super(Assignment , self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._variable = variable
        self._value    = value

    def print_ast(self, level):
        string = "%sAssignment Instruction:\n%sVariable:\n%s\n%sValue:\n%s" % (
            self._get_indentation(level),
            self._get_indentation(level+1),
            self._variable.print_ast(level+2),
            self._get_indentation(level+1),
            self._value.print_ast(level+2)
            )
        return string

    def _check(self, symtable):
        var_info = symtable.lookup(self._variable.getName(), self._position)
        val_type_class = self._value._check(symtable)
        if var_info is None:
            return True
        if not var_info.canAssign(val_type_class):
            error  = "In line %d, column %d, " % self._position
            error += "cannot assign a %s value to a %s variable." % (
                val_type_class,
                var_info.getType()
                )
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
        return True

    def _check_for_counter_modification(self, name, symtable):
        self._variable._check_for_counter_modification(name, symtable)


    def _execute(self, symtable):
        value = self._value._evaluate(symtable)
        symtable.update(self._variable.getName(), value, self._position)


class Input(Instruction):

    def __init__(self, variable, *args, **kwargs):
        super(Input, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._variable = variable

    def print_ast(self, level):
        string = "%sScan Instruction:\n%s" % (
            self._get_indentation(level),
            self._variable.print_ast(level+1)
            )
        return string

    def _check(self, symtable):
        type_class = self._variable._check(symtable)
        if not (type_class.isBool() or type_class.isInt()):
            error  = "In line %d, column %d, " % self._position
            error += "cannot read from standard input to a %s " % type_class
            error += "variable."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
        return True

    def _check_for_counter_modification(self, name, symtable):
        self._variable._check_for_counter_modification(name, symtable)

    def _execute(self, symtable):
        var = self._variable.getName()
        var_info = symtable.lookup(var, self._position)
        if var_info.isInt():
            type_class = "integer"
            parse = self.str2int
        elif var_info.isBool():
            type_class = "boolean"
            parse = self.str2bool
        valid_input = False
        while not valid_input:
            prompt = "Please enter a valid %s value:\n%s" % (type_class, self.PROMPT)
            read = raw_input(prompt)
            value = parse(read)
            if value is None:
                print "Invalid input"
            else:
                valid_input = True
        symtable.update(var, value, self._position)


    
class Output(Instruction):

    def __init__(self, printables, *args, **kwargs):
        super(Output, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._printables = printables
        self._lnsufix = kwargs.get('sufix',None)
        if self._lnsufix is None:
            self._op_name = 'Print'
        else :
            self._op_name = 'PrintLn'
            self._printables.append(String('"\n"', position=kwargs.get('position', None)))

    def print_ast(self, level):
        string = "%s%s Instruction:\n%sExpressions:" % (
            self._get_indentation(level),
            self._op_name,
            self._get_indentation(level+1)
            )
        for printable in self._printables:
            string += "\n%s" % (
                printable.print_ast(level+2)
                )
        return string

    def _check(self, symtable):
        if self._printables is not None and self._printables:
            for printable in self._printables:
                printable._check(symtable)
        return True

    def _check_for_counter_modification(self, name, symtable):
        pass

    def _execute(self, symtable):
        if self._printables is not None and self._printables:
            string = ''
            for printable in self._printables:
                value = printable._evaluate(symtable)
                if isinstance(value, set):
                    string += "{"
                    if value:
                        first = True
                        for elem in value:
                            if first:
                                first = not first
                                string += str(elem)
                            else:
                                string += ", " + str(elem)

                    string += "}"
                else:
                    string += str(value)
            import sys
            sys.stdout.write(string)



class Conditional(Instruction):

    def __init__(self, condition, instruction, alt_instruction=None, *args, **kwargs):
        super(Conditional, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._condition = condition
        self._instruction = instruction
        self._alt_instruction = alt_instruction

    def print_ast(self, level):
        string = "%sConditional Instruction:\n" % self._get_indentation(level)
        string += "%sCondition:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._condition.print_ast(level+2)
        string += "%sInstruction:\n" % self._get_indentation(level+1)
        string += "%s" % self._instruction.print_ast(level+2)
        if self._alt_instruction is not None:
            string += "\n%sAlternative Instruction:\n" % self._get_indentation(level+1)
            string += "%s" % self._alt_instruction.print_ast(level+2)
        return string

    def _check(self, symtable):
        condition_type = self._condition._check(symtable)
        instruction_check = self._instruction._check(symtable)
        if self._alt_instruction is not None:
            alt_instruction_check = self._alt_instruction._check(symtable)
        else:
            alt_instruction_check = True
        if not condition_type.isBool():
            error  = "In line %d, column %d, " % self._condition._position
            error += "conditional statement expression must be Boolean. "
            error += "Found '%s' instead." % condition_type
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
        return instruction_check and alt_instruction_check

    def _check_for_counter_modification(self, name, symtable):
        if self._instruction is not None:
            self._instruction._check_for_counter_modification(name, symtable)
        if self._alt_instruction is not None:
            self._alt_instruction._check_for_counter_modification(name, symtable)

    def _execute(self, symtable):
        if self._condition._evaluate(symtable):
            self._instruction._execute(symtable)
        else:
            if self._alt_instruction is not None:
                self._alt_instruction._execute(symtable)


class ForLoop(Instruction):

    def __init__(self, variable, ordering, set_exp, instruction, *args, **kwargs):
        super(ForLoop, self).__init__(args,kwargs)
        self._position    = kwargs.get('position', None)
        self._variable    = variable
        self._ordering    = ordering
        self._set         = set_exp
        self._instruction = instruction

    def print_ast(self, level):
        string = "%sFor Loop Instruction:\n" % self._get_indentation(level)
        string += "%sVariable:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._variable.print_ast(level+2)
        string += "%sOrdering: " % self._get_indentation(level+1)
        if self._ordering:
            string += "Ascendent"
        else :
            string += "Descendent"
        string += "\n%sIterable Set:\n" % self._get_indentation(level+1)
        string += "%s\n" % self._set.print_ast(level+2)
        string += "%sInstruction:\n" % self._get_indentation(level+1)
        string += "%s" % self._instruction.print_ast(level+2)
        return string

    def _update_symtable(self, symtable):
        new_symtable = SymTable(father=symtable)
        new_symtable.insert(
            self._variable.getName(),
            IntegerType(position=self._position),
            self._variable._position,
            read_only=True
            )
        return new_symtable

    def _check(self, symtable):
        # TODO: report error if internal variable is modified in for-loop's body
        new_symtable = self._update_symtable(symtable)
        set_type = self._set._check(symtable)
        if not set_type.isSet():
            error  = "In line %d, column %d, " % self._set._position
            error += "For loop expression must be of Set type. "
            error += "Found %s instead." % set_type
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
        if self._instruction is not None:
            self._instruction._check(new_symtable)
            self._instruction._check_for_counter_modification(self._variable.getName(), new_symtable)
        if symtable is None:
            return new_symtable
        else:
            return True

    def _check_for_counter_modification(self, name, symtable):
        new_symtable = self._update_symtable(symtable)
        if self._instruction is not None:
            self._instruction._check_for_counter_modification(name, new_symtable)

    def _execute(self, symtable):
        iterable = list(self._set._evaluate(symtable))
        iterable.sort()
        if not self._ordering:
            iterable.reverse()
        new_symtable = self._update_symtable(symtable)
        for i in iterable:
            var = self._variable.getName()
            new_symtable.update(var, i, self._position)
            self._instruction._execute(new_symtable)



class RepeatWhileLoop(Instruction):

    def __init__(self, prev_instruction, condition, instruction, *args, **kwargs):
        super(RepeatWhileLoop, self).__init__(args,kwargs)
        self._position         = kwargs.get('position', None)
        self._prev_instruction = prev_instruction
        self._condition        = condition
        self._instruction      = instruction

    def print_ast(self, level):
        string = "%sRepeate While Loop Instruction:\n" % self._get_indentation(level)
        if self._prev_instruction is not None:
            string += "%sPrevious Instruction:\n" % self._get_indentation(level+1)
            string += "%s\n" % self._prev_instruction.print_ast(level+2)
        string += "%sCondition:\n" % self._get_indentation(level+1)
        string += "%s" % self._condition.print_ast(level+2)
        if self._instruction is not None:
            string += "\n%sInstruction:\n" % self._get_indentation(level+1)
            string += "%s" % self._instruction.print_ast(level+2)
        return string

    def _check(self, symtable):
        if self._prev_instruction is None and self._instruction is None:
            error  = "In line %d, column %d, " % self._position
            error += "Repeat-While-Loop must have at least one instruction."
            raise SetlanSyntaxError(error)
        if self._prev_instruction is not None:
            prev_inst_check = self._prev_instruction._check(symtable)
        else:
            prev_inst_check = True
        if self._instruction is not None:
            instruction_check = self._instruction._check(symtable)
        else:
            instruction_check = True
        condition_type = self._condition._check(symtable)
        if not condition_type.isBool():
            error  = "In line %d, column %d, " % self._condition._position
            error += "conditional expression of the repeat-while-do loop "
            error += "statement must be Boolean. "
            error += "Found '%s' instead." % condition_type
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
        return prev_inst_check and instruction_check

    def _check_for_counter_modification(self, name, symtable):
        if self._prev_instruction is not None:
            self._prev_instruction._check_for_counter_modification(name, symtable)
        if self._instruction is not None:
            self._instruction._check_for_counter_modification(name, symtable)

    def _first_case(self, symtable):
        not_done = True
        while not_done:
            self._prev_instruction._execute(symtable)
            not_done = self._condition._evaluate(symtable)
            if not not_done:
                break
            else:
                self._instruction._execute(symtable)

    def _second_case(self, symtable):
        while self._condition._evaluate(symtable):
            self._instruction._execute(symtable)

    def _third_case(self, symtable):
        self._prev_instruction._execute(symtable)
        while self._condition._evaluate(symtable):
            self._prev_instruction._execute(symtable)

    def _execute(self, symtable):
        if self._prev_instruction is not None and self._instruction is not None:
            self._first_case(symtable)
        elif self._prev_instruction is None and self._instruction is not None:
            self._second_case(symtable)
        if self._prev_instruction is not None and self._instruction is None:
            self._third_case(symtable)



class VariableDeclaration(Declaration):

    def __init__(self, type_class, variables, *args, **kwargs):
        super(VariableDeclaration, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._type      = type_class
        self._variables = variables

    def print_ast(self, level):
        string = "\n%sVariable Declaration:\n" % self._get_indentation(level+1)
        string += "%sType:\n" % self._get_indentation(level+2)
        string += "%s" % self._type.print_ast(level+3)
        string += "%sVariables:" % self._get_indentation(level+2)
        for variable in self._variables:
            string += "\n%s" % variable.print_ast(level+3)
        return string

    def _check(self, symtable):
        if self._variables is not None and self._variables:
            for variable in self._variables:
                symtable.insert(variable.getName(), self._type, variable._position)
        else:
            error  = "In line %d, column %d, " % self._position
            error += "there must be at least one variable declared."
            raise SetlanSyntaxError(error)
        return True


class Variable(Expression):

    def __init__(self, tkid, *args, **kwargs):
        super(Variable, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._id = tkid

    def print_ast(self, level):
        string = "%sVariable: %s" % (self._get_indentation(level), self._id)
        return string

    def getName(self):
        return self._id

    def _check(self, symtable):
        var_info = None
        if symtable is not None:
            var_info = symtable.lookup(self.getName(),self._position)
        if var_info is not None:
            return var_info.getType()
        else:
            error  = "In line %d, column %d, " % self._position
            error += "trying to use variable '%s', " % self._id
            error += "but it has not been defined in current scope."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanScopeError(error))
            return Type(position=self._position)

    def _check_for_counter_modification(self, name, symtable):
        var_info = symtable.lookup(name, self._position)
        if var_info.isReadOnly():
            error  = "In line %d, column %d, " % self._position
            error += "trying to modify variable '%s', " % self._id
            error += "but it is a read only variable in this scope."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanScopeError(error))


    def _evaluate(self, symtable):
        return symtable.lookup(self.getName(), self._position).getValue()


class BinaryExpression(Expression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(BinaryExpression, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._left = left
        self._function = op
        self._right = right
        self._operation = ""

    def print_ast(self, level):
        string = "%s%s:\n%sLeft Operand:\n%s\n%sRight Operand:\n%s" % (
            self._get_indentation(level),
            self._operation,
            self._get_indentation(level+1),
            self._left.print_ast(level+2),
            self._get_indentation(level+1),
            self._right.print_ast(level+2)
            )
        return string

    def _check(self, symtable):
        return "%s%s: Not Implemented" % (self.SPACE, self.__class__.__name__)

    def _evaluate(self, symtable):
        return self._op(self._left._evaluate(symtable), self._right._evaluate(symtable))


class SameTypeBinaryExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(SameTypeBinaryExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if ((not isinstance(left_type, self._expected_type.__class__)) or
            left_type != right_type):
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s and %s expressions." % (
                self._symbol,
                left_type,
                right_type
                )
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
            return self._expected_type
        return left_type


class ComparationBinaryExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(ComparationBinaryExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if left_type != right_type:
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s and %s expressions." % (
                self._symbol,
                left_type,
                right_type
                )
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error)) 
        return BooleanType(position=self._position)


class IntSetSetExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(IntSetSetExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if ((not isinstance(left_type, IntegerType)) or
           (not isinstance(right_type, SetType))):
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s and %s expressions. " % (
                self._symbol,
                left_type,
                right_type
                )
            error += "Expected: Integer and Set, in this order."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
            return self._expected_type
        return right_type


class IntSetBooleanExpression(BinaryExpression):

    def __init__(self, left, op, right, *args, **kwargs):
        super(IntSetBooleanExpression, self).__init__(left,op,right,args,kwargs)
        self._position = kwargs.get('position', None)
    
    def _check(self, symtable):
        left_type = self._left._check(symtable)
        right_type = self._right._check(symtable)
        if ((not isinstance(left_type, IntegerType)) or
           (not isinstance(right_type, SetType))):
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s and %s expressions. " % (
                self._symbol,
                left_type,
                right_type
                )
            error += "Expected: Integer and Set, in this order."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
            return self._expected_type
        return BooleanType(position=self._position)


class UnaryExpression(Expression):

    def __init__(self, op, expression, *args, **kwargs):
        super(UnaryExpression, self).__init__(args,kwargs)
        self._position = kwargs.get('position', None)
        self._expected_type = None
        self._expression = expression
        self._function = op
        self._operation = ""

    def print_ast(self, level):
        string = "%s%s:\n%sOperand:\n%s" % (
            self._get_indentation(level),
            self._operation,
            self._get_indentation(level+1),
            self._expression.print_ast(level+2)
            )
        return string

    def _evaluate(self, symtable):
        return self._op(self._expression._evaluate(symtable))


class IntUnaryExpression(UnaryExpression):

    def __init__(self, op, expression, *args, **kwargs):
        super(IntUnaryExpression, self).__init__(op,expression,args,kwargs)
        self._position = kwargs.get('position', None)
        self._expected_type = IntegerType(position=self._position)
    
    def _check(self, symtable):
        type_class = self._expression._check(symtable)
        if not isinstance(type_class, IntegerType):
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s expression. " % (
                self._symbol,
                type_class
                )
            error += "Expected: Integer."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
            return self._expected_type
        return type_class

    def _evaluate(self, symtable):
        return self.checkOverflow(self._op(self._expression._evaluate(symtable)), self._position)


class SetUnaryExpression(UnaryExpression):

    def __init__(self, op, expression, *args, **kwargs):
        super(SetUnaryExpression, self).__init__(op,expression,args,kwargs)
        self._position = kwargs.get('position', None)
        self._expected_type = SetType(position=self._position)
    
    def _check(self, symtable):
        type_class = self._expression._check(symtable)
        if not isinstance(type_class, SetType):
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s expression. " % (
                self._symbol,
                type_class
                )
            error += "Expected: Set."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
            return self._expected_type
        return type_class


class BoolUnaryExpression(UnaryExpression):

    def __init__(self, op, expression, *args, **kwargs):
        super(BoolUnaryExpression, self).__init__(op,expression,args,kwargs)
        self._position = kwargs.get('position', None)
        self._expected_type = BooleanType(position=self._position)
    
    def _check(self, symtable):
        type_class = self._expression._check(symtable)
        if not isinstance(type_class, BooleanType):
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '%s' operation over %s expression. " % (
                self._symbol,
                type_class
                )
            error += "Expected: Boolean."
            errors_acc = SetlanStaticErrors.Instance()
            errors_acc.add_error(SetlanTypeError(error))
            return self._expected_type
        return type_class


class Sum(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Sum, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Sum"
        self._symbol = '+'
        self._expected_type = IntegerType(position=self._position)
        self._op = self._sum

    def _sum(self, left, right):
        return self.checkOverflow(left + right, self._position)


class Subtraction(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Subtraction, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Subtraction"
        self._symbol = '-'
        self._expected_type = IntegerType(position=self._position)
        self._op = self._subtraction

    def _subtraction(self, left, right):
        return self.checkOverflow(left - right, self._position)


class Times(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Times, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Times"
        self._symbol = '*'
        self._expected_type = IntegerType(position=self._position)
        self._op = self._times

    def _times(self, left, right):
        return self.checkOverflow(left * right, self._position)


class Division(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Division, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Division"
        self._symbol = '/'
        self._expected_type = IntegerType(position=self._position)
        self._op = self._division

    def _division(self, left, right):
        if right == 0:
            error  = "In line %d, column %d, " % self._position
            error += "cannot divide by zero value."
            raise SetlanZeroDivisionError(error)
        return self.checkOverflow(left / right, self._position)


class Modulus(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Modulus, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Modulus"
        self._symbol = '%'
        self._expected_type = IntegerType(position=self._position)
        self._op = self._modulus

    def _modulus(self, left, right):
        if right == 0:
            error  = "In line %d, column %d, " % self._position
            error += "cannot calculate modulus by zero value."
            raise SetlanZeroDivisionError(error)
        return self.checkOverflow(left % right, self._position)


class Union(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Union, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Union"
        self._symbol = '++'
        self._expected_type = SetType(position=self._position)
        self._op = self._union

    def _union(self, left, right):
        return left.union(right)


class Difference(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Difference, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Difference"
        self._symbol = '\\'
        self._expected_type = SetType(position=self._position)
        self._op = self._difference

    def _difference(self, left, right):
        return left.difference(right)


class Intersection(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Intersection, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Intersection"
        self._symbol = '><'
        self._expected_type = SetType(position=self._position)
        self._op = self._intersection

    def _intersection(self, left, right):
        return left.intersection(right)


class SetSum(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetSum, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetSum"
        self._symbol = '<+>'
        self._op = self._setsum

    def _setsum(self, integer, setval):
        return set(map(lambda e: self.checkOverflow(integer + e, self._position), setval))



class SetSubtraction(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetSubtraction, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetSubtraction"
        self._symbol = '<->'
        self._op = self._setsubtraction

    def _setsubtraction(self, integer, setval):
        return set(map(lambda e: self.checkOverflow(integer - e, self._position), setval))


class SetTimes(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetTimes, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetTimes"
        self._symbol = '<*>'
        self._op = self._settimes

    def _settimes(self, integer, setval):
        return set(map(lambda e: self.checkOverflow(integer * e, self._position), setval))


class SetDivision(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetDivision, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetDivision"
        self._symbol = '</>'
        self._op = self._setdivision

    def _division(self, left, right):
        if right == 0:
            error  = "In line %d, column %d, " % self._position
            error += "cannot divide by zero value."
            raise SetlanZeroDivisionError()
        return self.checkOverflow(left / right, self._position)

    def _division_wrapper(self, constant):
        return lambda elem: self._division(constant, elem)

    def _setdivision(self, integer, setval):
        return set(map(self._division_wrapper(integer), setval))


class SetModulus(IntSetSetExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(SetModulus, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "SetModulus"
        self._symbol = '<%>'
        self._op = self._setmodulus

    def _modulus(self, left, right):
        if right == 0:
            error  = "In line %d, column %d, " % self._position
            error += "cannot divide by zero value."
            raise SetlanZeroDivisionError()
        return self.checkOverflow(left % right, self._position)

    def _modulus_wrapper(self, constant):
        return lambda elem: self._modulus(constant, elem)

    def _setmodulus(self, integer, setval):
        return set(map(self._modulus_wrapper(integer), setval))


class GreaterThan(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(GreaterThan, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GreaterThan"
        self._symbol = '>'
        self._op = self._gt

    def _gt(self, left, right):
        return left > right



class GreaterOrEqual(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(GreaterOrEqual, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GreaterOrEqual"
        self._symbol = '>='
        self._op = self._geq

    def _geq(self, left, right):
        return left >= right


class LessThan(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(LessThan, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "LessThan"
        self._symbol = '<'
        self._op = self._lt

    def _lt(self, left, right):
        return left < right


class LessOrEqual(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(LessOrEqual, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "LessOrEqual"
        self._symbol = '<='
        self._op = self._leq

    def _leq(self, left, right):
        return left <= right


class Equals(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Equals, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Equals"
        self._symbol = '=='
        self._op = self._eq

    def _eq(self, left, right):
        return left == right


class NotEquals(ComparationBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(NotEquals, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "NotEquals"
        self._symbol = '/='
        self._op = self._neq

    def _neq(self, left, right):
        return left != right


class And(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(And, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "And"
        self._symbol = 'and'
        self._expected_type = BooleanType(position=self._position)
        self._op = self._and

    def _and(self, left, right):
        return left and right


class Or(SameTypeBinaryExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(Or, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Or"
        self._symbol = 'or'
        self._expected_type = BooleanType(position=self._position)
        self._op = self._or

    def _or(self, left, right):
        return left or right


class IsIn(IntSetBooleanExpression):

    def __init__(self, left, right, *args, **kwargs):
        super(IsIn, self).__init__(left, None, right, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "IsIn"
        self._symbol = '@'
        self._op = self._is_in

    def _is_in(self, left, right):
        return left in right


class Minus(IntUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(Minus, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Minus"
        self._symbol = '-'
        self._op = self._minus

    def _minus(self, value):
        return self.checkOverflow(- value, self._position)


class GetMax(SetUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetMax, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GetMax"
        self._symbol = '>?'
        self._op = self._max

    def _max(self, setvalue):
        try:
            return max(setvalue)
        except ValueError:
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '>?' operation over empty set."
            raise SetlanEmptySetError(error)



class GetMin(SetUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetMin, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GetMin"
        self._symbol = '<?'
        self._op = self._min

    def _min(self, setvalue):
        try:
            return min(setvalue)
        except ValueError:
            error  = "In line %d, column %d, " % self._position
            error += "cannot apply '<?' operation over empty set."
            raise SetlanEmptySetError(error)


class GetSize(SetUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(GetSize, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "GetSize"
        self._symbol = '$?'
        self._op = len


class Not(BoolUnaryExpression):

    def __init__(self, expression, *args, **kwargs):
        super(Not, self).__init__(None, expression, args, kwargs)
        self._position = kwargs.get('position', None)
        self._operation = "Not"
        self._symbol = 'not'
        self._op = lambda x: not x


class TrueValue(Expression):

    def __init__(self, *args, **kwargs):
        super(TrueValue, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._value = True

    def print_ast(self, level):
        string = "%sBoolean: True" % self._get_indentation(level)
        return string

    def _check(self, symtable):
        return BooleanType(position=self._position)

    def _evaluate(self, symtable):
        return True


class FalseValue(Expression):

    def __init__(self, *args, **kwargs):
        super(FalseValue, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._value = False

    def print_ast(self, level):
        string = "%sBoolean: False" % self._get_indentation(level)
        return string

    def _check(self, symtable):
        return BooleanType(position=self._position)

    def _evaluate(self, symtable):
        return False


class Number(Expression):

    def __init__(self, value, *args, **kwargs):
        super(Number, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._value = value

    def print_ast(self, level):
        string = "%sNumber: %s" % (self._get_indentation(level), str(self._value))
        return string

    def _check(self, symtable):
        return IntegerType(position=self._position)

    def _evaluate(self, symtable):
        return self.checkOverflow(self._value, self._position)


class Set(Expression):

    def __init__(self, elements, *args, **kwargs):
        super(Set, self).__init__(args, kwargs)
        self._position = kwargs.get('position', None)
        self._input = elements

    def print_ast(self, level):
        string = "%sSet:\n%s{" % (
            self._get_indentation(level), self._get_indentation(level+1))
        for index, element in enumerate(self._input):
            string += "\n%sElement[%d]:" % (
                self._get_indentation(level+2),
                index
                )
            string += "\n%s" % element.print_ast(level+3)
        string += "\n%s}" % self._get_indentation(level+1)
        return string

    def _check(self, symtable):
        return SetType(position=self._position)

    def _unpack(self, elems, symtable):
        list_of_elems = []
        for elem in elems:
            value = self.checkOverflow(elem._evaluate(symtable), self._position)
            list_of_elems.append(value)
        return list_of_elems

    def _evaluate(self, symtable):
        if self._input is not None and self._input:
            return set(self._unpack(self._input, symtable))
        elif self._input is not None and not self._input:
            return set()
        else:
            return set()