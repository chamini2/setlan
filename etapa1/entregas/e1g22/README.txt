Python implementation of the language Setlan
============================================

Author: Victor De Ponte, 05-38087 ([email](mailto:rdbvictor19@gmail.com))


`setlan` is a python implementation for the language Setlan, defined
[here](http://ldc.usb.ve/~09-10285/files/def/setlan-3.pdf) (spanish). It was
made in order to fulfill the requirements for aproving the course CI-3725
_"Traductores e interpretadores"_ (Compilers and interpreters).

The whole project is divided into 4 phases. The current implementation goes up
to the first one, which contemplates the lexicographical analysis.

Test files with their corresponding outputs can be found in the test folder.

## List of Tokens

The tokens defined for the language are listed below. Each of the expressions
written in the examples have the value of `true`, with the exception of
numerical values and reserved words and instructions, which are not expressions.

| *Token*           | *Symbol*                                      | *Example*                                         |
|----------------   |-------------------------------------------    |------------------------------------------------   |
| TkProgram         | program                                       | program                                           |
| TkInt             | int                                           | int                                               |
| TkBool            | bool                                          | bool                                              |
| TkSet             | set                                           | set                                               |
| TkUsing           | using                                         | using                                             |
| TkIn              | in                                            | in                                                |
| TkScan            | scan                                          | scan                                              |
| TkPrint           | print                                         | if (1 < 2) {print "true"}                         |
| TkIf              | if                                            | if(1 < 2) {print "true"}                          |
| TkElse            | else                                          | if (1 < 2) {print "true"} else {print "false"}    |
| TkFor             | for                                           | for                                               |
| TkDo              | do                                            | do                                                |
| TkMin             | min                                           | min                                               |
| TkMax             | max                                           | max                                               |
| TkRepeat          | repeat                                        | repeat                                            |
| TkWhile           | while                                         | while                                             |
| TkOr              | or                                            | or                                                |
| TkAnd             | and                                           | and                                               |
| TkNot             | not                                           | not                                               |
| TkTrue            | true                                          | true                                              |
| TkFalse           | false                                         | false                                             |
| TkId              | Variable Identifier                           | foo                                               |
| TkNum             | Inmediate integer number                      | 42                                                |
| TkString          | String of characters (with double quotes)     | "This is a string"                                |
| TkOBrace          | {                                             | foo= {1,2,3}                                      |
| TkCBrace          | }                                             | foo= {1,2,3}                                      |
| TkComma           | ,                                             | foo= {1,2,3}                                      |
| TkAssign          | =                                             | foo= {1,2,3}                                      |
| TkSColon          | ;                                             | { foo = {1,2,3}; bar = {4,5,6} }                  |
| TkOPar            | (                                             | if (1 < 2) {print "true"}                         |
| TkCPar            | )                                             | if (1 < 2) {print "true"}                         |
| TkPlus            | +                                             | foo = 1 + 2                                       |
| TkMinus           | -                                             | foo = 2 - 1; bar = -42                            |
| TkTimes           | *                                             | foo = 6 * 7 == 42                                 |
| TkDiv             | /                                             | foo = 84 / 2 == 42                                |
| TkMod             | %                                             | foo = 42 % 2 == 0                                 |
| TkUnion           | ++                                            | foo = {1,2,3} ++ {4,5,6} == {1,2,3,4,5,6}         |
| TkDiff            | \                                             | foo = {1,2,3} \ {3,4,5} == {1,2}                  |
| TkIntersection    | ><                                            | foo = {1,2,3} >< {4,5,6} == {}                    |
| TkSPlus           | <+>                                           | foo = {1,2,3} <+> 1 == {2,3,4}                    |
| TkSMinus          | <->                                           | foo = {1,2,3} <-> 1 == {0,1,2}                    |
| TkSTimes          | <*>                                           | foo = {1,2,3} <*> 2 == {2,4,6}                    |
| TkSDiv            | </>                                           | foo = {2,4,6} </> 1 == {1,2,3}                    |
| TkSMod            | <%>                                           | foo = {2,4,6}  1 == {0,0,0} == {0}                |
| TkGetMin          | <?                                            | foo = <? {1,2,3} == 1                             |
| TkGetMax          | >?                                            | foo = >? {1,2,3} == 3                             |
| TkSize            | $?                                            | foo = $? {1,2,3,10,42} == 5                       |
| TkGreat           | >                                             | foo = 1 > 0                                       |
| TkGreatOrEq       | >=                                            | foo = 1 >= 0                                      |
| TkLess            | <                                             | foo = 1 < 0                                       |
| TkLessOrEq        | <=                                            | foo = 1 <= 0                                      |
| TkEquals          | ==                                            | foo = 1 ==1                                       |
| TkNotEquals       | /=                                            | foo = 1 /= 0                                      |
| TkIsIn            | @                                             | foo = 1 @ {1,2,3}                                 |

## Implementation decisions

The implementation was made following
[PLY's documentation](http://www.dabeaz.com/ply/ply.html), with the exception
of:

1. The column number is calculated for each token instead of only for error
   handling.

2. A new attribute is added to PLY's lexer object on the fly in case of lexical
   errors, which is a list of `SetlanLexicalError`s which are in turn printed
   *only* in case of errors.