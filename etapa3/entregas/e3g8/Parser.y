#!/usr/bin/env ruby

class Parser

	prechigh
			right ELSE
			nonassoc S_if
			nonassoc S_elseif
			right IF
			rigth ASSIGN
			nonassoc Minus_unario
			left MULTIPLICATION DIVISION MOD
			left PLUS MINUS
			left UNION DIFERENCE
			left INTERSECTION
			right PLUS_ON_SET MINUS_ON_SET
			right MULTIPLICATION_ON_SET DIVISION_ON_SET MOD_ON_SET
			nonassoc BIGGEST_ON_SET LOWEST_ON_SET CARD_ON_SET
			nonassoc GREATER GREATER_EQUAL LESS LESS_EQUAL
			nonassoc EQUAL DIFFERENT
			nonassoc BELONG
			left OR
			left AND
			left NOT


	preclow

	token 	STRING INTEGER BOOL IDENTIFIER LCURLY RCURLY LPARENTHESIS RPARENTHESIS 
		  	COMMA SEMICOLON UNION DIFERENCE INTERSECTION PLUS_ON_SET MINUS_ON_SET
		   	MULTIPLICATION_ON_SET DIVISION_ON_SET MOD_ON_SET BIGGEST_ON_SET
		 	LOWEST_ON_SET CARD_ON_SET PLUS MINUS MULTIPLICATION DIVISION MOD EQUAL
			DIFFERENT LESS_EQUAL LESS GREATER_EQUAL GREATER BELONG ASSIGN
			PROGRAM PRINTLN PRINT SCAN USING INT IN BOOL SET IF ELSE FOR DO REPEAT 
			WHILE OR AND NOT MAX MIN TRUE FALSE SET_I

	rule

	###########################
	# Estructura del Programa #
	###########################
	S
	: iPrograma Estructura { @handler.fPrograma }
	;


	iPrograma
	: PROGRAM { @handler.iPrograma([:PROGRAM]) }
	;


	Estructura
	: iBloque Bloque RCURLY { @handler.fBloque }
	| Instruccion
	; 
	iBloque
	: LCURLY { @handler.iBloque([:BLOQUE]) }
	;

	Bloque
	: iUsing V_declaracion fUsing Inter { @handler.fIn }
	| Inter 
	;
	############################
	# Declaracion de Variables #
	############################
	iUsing
	: USING { @handler.iUsing([:USING]) }
	;
	fUsing
	: IN { @handler.fUsing; @handler.iIn([:IN]) }
	;
	
	V_declaracion
	: Declaracion V_declaracion
	| Declaracion
	;


	Declaracion
	: iTipo Variable SEMICOLON { @handler.fTipo }
	| iTipo Variable COMMA M_declaracion SEMICOLON { @handler.fTipo }
	;


	M_declaracion
	: Variable COMMA M_declaracion
	| Variable
	;
	############################
	# Instruciones y Argumentos#
	############################
	Inter
	: Instruccion SEMICOLON Inter
	| Instruccion SEMICOLON
	;

	Instruccion
	: iPrint Palabra { @handler.fPrint }
	| iScan Variable { @handler.fScan }
	| iIf Condicional Estructura =S_if { @handler.fIf }
	| iIf Condicional Estructura Else_i  { @handler.fIf }
	| iFor E_for { @handler.fFor } 
	| Loop
	| Asignacion
	;


	iPrint
	: PRINT { @handler.iPrint([:PRINT]) }
	| PRINTLN { @handler.iPrint([:PRINTLN]) }
	;

	Palabra
	: Expresiones
	| String COMMA Palabra
	| Expresiones COMMA Palabra
	| String
	;

	iScan
	: SCAN { @handler.iScan([:SCAN]) }
	;

	iIf
	: IF { @handler.iIf([:IF]) }
	;

	iFor
	: FOR { @handler.iFor([:FOR]) }

	E_for
	: Variable Dir Expresiones Do Estructura
	;

	Dir
	: MIN { @handler.Min([:MIN]) }
	| MAX { @handler.Max([:MAX]) }
	;

	Else_i
	: iElse_if Condicional Estructura Else_i   { @handler.fElse_if }
	| iElse_if Condicional Estructura =S_elseif { @handler.fElse_if }
	| iElse Estructura	 { @handler.fElse }
	;

	iElse
	: ELSE { @handler.iElse([:ELSE]) }
	;

	iElse_if
	: ELSE IF  { @handler.iElse([:ELSE_IF]) }
	;

	Loop
	: iRepeat Estructura iWhile Condicional Do Estructura { @handler.fDo; @handler.fWhile; @handler.fRepeat }
	| iWhile Condicional Do Estructura { @handler.fDo; @handler.fWhile }
	| iRepeat Estructura iWhile Condicional { @handler.fwhile; @handler.fRepeat }
	;

	iRepeat
	: REPEAT { @handler.iRepeat([:REPEAT]) }
	;

	iWhile
	: WHILE { @handler.iWhile([:WHILE]) }
	;
	Do
	: DO { @handler.iDo([:DO]) }
	;


	Variable
	: IDENTIFIER { @handler.Identifier([:IDENTIFIER, val[0]]) }
	;


	String
	: STRING { @handler.String([:STRING, val[0]]) }
	;


	Condicional
	:  iCondicional Expresiones RPARENTHESIS { @handler.fCondicional }
	;

	iCondicional
	: LPARENTHESIS { @handler.iCondicional([:"("]) }
	;
	############################
	# Expresiones y Operadores #
	############################
	Expresiones
	: Identificador 
	| Minus Identificador  =Minus_unario 
	| Biggest_on_set Expresiones { @handler.fBiggest_on_set }
	| Lowest_on_set Expresiones { @handler.fLowest_on_set }
	| Card_on_set Expresiones { @handler.fCard_on_set }
	| Not Expresiones { @handler.fNot }
	| Identificador Plus Expresiones { @handler.fPlus }
	| Identificador Minus Expresiones { @handler.fMinus }
	| Identificador Multiplication Expresiones { @handler.fMultiplication }
	| Identificador Division Expresiones { @handler.fDivision }
	| Identificador Mod Expresiones { @handler.fMod }
	| Identificador Union Expresiones { @handler.fUnion }
	| Identificador Diference Expresiones { @handler.fDiference }
	| Identificador Intersection Expresiones { @handler.fIntersection }
	| Identificador Plus_on_set Expresiones { @handler.fPlus_on_set }
	| Identificador Minus_on_set Expresiones { @handler.fMinus_on_set }
	| Identificador Multiplication_on_set Expresiones { @handler.fMultiplication_on_set }
	| Identificador Division_on_set Expresiones { @handler.fDivision_on_set }
	| Identificador Mod_on_set Expresiones { @handler.fMod_on_set }
	| Identificador Equal Expresiones { @handler.fEqual }
	| Identificador Different Expresiones { @handler.fDifferent }
	| Identificador Or Expresiones { @handler.fOr }
	| Identificador And Expresiones { @handler.fAnd }
	| Identificador Less Expresiones { @handler.fLess }
	| Identificador Less_equal Expresiones { @handler.fLess_equal }
	| Identificador Greater Expresiones { @handler.fGreater }
	| Identificador Greater_equal Expresiones { @handler.fGreater_equal }
	| Identificador Belong Expresiones { @handler.fBelong }
	;

	P_expresion
	: LPARENTHESIS { @handler.Lparenthesis([:LPARENTHESIS]) }

	Asignacion
	: Variable Assign Expresiones { @handler.fAssign }
	;

	Assign
	: ASSIGN { @handler.iAssign([:ASSIGN]) }
	;

	Minus
	: MINUS {@handler.iMinus([:MINUS]) }
	;

	Biggest_on_set
	: BIGGEST_ON_SET { @handler.iBiggest_on_set([:BIGGEST_ON_SET]) }
	;

	Lowest_on_set
	: LOWEST_ON_SET { @handler.iLowest_on_set([:LOWEST_ON_SET]) }
	;

	Card_on_set
	: CARD_ON_SET { @handler.iCard_on_set([:CARD_ON_SET]) }
	;

	Not
	: NOT { @handler.iNot([:NOT])}

	Plus
	: PLUS { @handler.iPlus([:PLUS]) }
	;

	Multiplication
	: MULTIPLICATION { @handler.iMultiplication([:MULTIPLICATION]) }
	;

	Division
	: DIVISION { @handler.iDivision([:DIVISION]) }
	;

	Mod 
	: MOD { @handler.iMod([:MOD]) }
	;

	Union
	: UNION { @handler.iUnion([:UNION]) }
	;

	Diference
	: DIFERENCE { @handler.iDiference([:DIFERENCE]) }
	;

	Intersection
	: INTERSECTION { @handler.iIntersection([:INTERSECTION]) }
	;

	Plus_on_set
	: PLUS_ON_SET { @handler.iPlus_on_set([:PLUS_ON_SET]) }
	;

	Minus_on_set
	: MINUS_ON_SET { @handler.iMinus_on_set([:MINUS_ON_SET]) }
	;

	Multiplication_on_set
	: MULTIPLICATION_ON_SET { @handler.iMultiplication_on_set([:MULTIPLICATION_ON_SET]) }
	;

	Division_on_set
	: DIVISION_ON_SET { @handler.iDivision_on_set([:DIVISION_ON_SET]) }
	;

	Mod_on_set
	: MOD_ON_SET { @handler.iMod_on_set([:MOD_ON_SET]) }
	;

	Equal
	: EQUAL { @handler.iEqual([:EQUAL]) }
	;

	Different
	: DIFFERENT { @handler.iDifferent([:DIFFERENT]) }
	;

	Or
	: OR { @handler.iOr([:OR]) } 
	;

	And
	: AND { @handler.iAnd([:AND]) }
	;

	Less
	: LESS { @handler.iLess([:LESS]) }
	;

	Less_equal
	: LESS_EQUAL { @handler.iLess_equal([:LESS_EQUAL]) }
	;

	Greater
	: GREATER { @handler.iGreater([:GREATER]) }
	;

	Greater_equal
	: GREATER_EQUAL { @handler.iGreater_equal([:GREATER_EQUAL]) }
	;

	Belong
	: BELONG { @handler.iBelong([:BELONG]) }
	;

	# Tipos de Datos

	Identificador
	: Numeros
	| Booleanos
	| Conjuntos
	| Variable
	| P_expresion Expresiones RPARENTHESIS { @handler.Rparenthesis([:RPARENTHESIS]) }
	;


	Numeros
	: INTEGER { @handler.Integer([:INTEGER, val[0]]) }
	;


	Booleanos
	: TRUE { @handler.True([:TRUE, val[0]]) }
	| FALSE	{ @handler.False([:FALSE, val[0]]) }
	;


	Conjuntos
	: SET_I { @handler.Set([:SET_I, val[0]]) }
	;


	iTipo
	: INT { @handler.iTipo([:INT]) }
	| BOOL { @handler.iTipo([:BOOL]) }
	| SET { @handler.iTipo([:SET]) }
	;


end 

---- inner

require "./Handler"
require "./Tabla"

attr_reader :handler
attr_reader :tabla

def initialize(tokens)
	@tokens = tokens
	@tabla = Tabla.new
	@handler = Handler.new @tabla
end

def next_token
	@tokens.next_token
end


def parse
	do_parse
	handler
end




