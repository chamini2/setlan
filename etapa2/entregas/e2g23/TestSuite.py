import unittest
from lexer import mainLexer
from parser import mainParser

class LexerTestSuite(unittest.TestCase):
    def testSimple(self):
        self.assertEqual(mainLexer('Tests/test1.txt'), open('Tests/answer1.txt','r').read())

    def testString(self):
        self.assertEqual(mainLexer('Tests/test2.txt'), open('Tests/answer2.txt','r').read())

    def testString2(self):
        self.assertEqual(mainLexer('Tests/test3.txt'), open('Tests/answer3.txt','r').read())

    def testSimpleError(self):
        self.assertEqual(mainLexer('Tests/test4.txt'), open('Tests/answer4.txt','r').read())

    def testCommentAndError(self):
        self.assertEqual(mainLexer('Tests/test5.txt'), open('Tests/answer5.txt','r').read())

    def testSample1(self):
        self.assertEqual(mainLexer('Tests/test6.txt'), open('Tests/answer6.txt','r').read())

    def testCommentAndError2(self):
        self.assertEqual(mainLexer('Tests/test7.txt'), open('Tests/answer7.txt','r').read())

    def testIfElse(self):
        self.assertEqual(mainLexer('Tests/test8.txt'), open('Tests/answer8.txt','r').read())

    def testOperators(self):
        self.assertEqual(mainLexer('Tests/test9.txt'), open('Tests/answer9.txt','r').read())

    def testSample2(self):
        self.assertEqual(mainLexer('Tests/test10.txt'), open('Tests/answer10.txt','r').read())

    def testBadVariables(self):
        self.assertEqual(mainLexer('Tests/test11.txt'), open('Tests/answer11.txt','r').read())

    def testJoins(self):
        self.assertEqual(mainLexer('Tests/test100.txt'), open('Tests/answer100.txt','r').read())

    def testAllContinue(self):
        self.assertEqual(mainLexer('Tests/test101.txt'), open('Tests/answer101.txt','r').read())    

    def testOperatorsWithoutSpaces(self):
        self.assertEqual(mainLexer('Tests/test12.txt'), open('Tests/answer12.txt','r').read())

    def testSetMinMaxContains(self):
        self.assertEqual(mainLexer('Tests/test13.txt'), open('Tests/answer13.txt','r').read())

    def testEscapeBackS(self):
        self.assertEqual(mainLexer('Tests/testCarlitos.txt'), open('Tests/answerCarlitos.txt','r').read())



class ParserTestSuite(unittest.TestCase):
    def testSimple1(self):
        self.assertEqual(mainParser('Tests/testSimple1.txt'), open('Tests/answerSimple1.txt','r').read())
    def testSimple2(self):
        self.assertEqual(mainParser('Tests/testSimple2.txt'), open('Tests/answerSimple2.txt','r').read())
    def testSimpleError(self):
        self.assertEqual(mainParser('Tests/testSimpleError.txt'), open('Tests/answerSimpleError.txt','r').read())
    def testIfThen(self):
        self.assertEqual(mainParser('Tests/testIfThen.txt'), open('Tests/answerIfThen.txt','r').read())
    def testIfThenElse(self):
        self.assertEqual(mainParser('Tests/testIfThenElse.txt'), open('Tests/answerIfThenElse.txt','r').read())
    def testAssign(self):
        self.assertEqual(mainParser('Tests/testAssign.txt'), open('Tests/answerAssign.txt','r').read())
    def testUsing(self):
        self.assertEqual(mainParser('Tests/testUsing.txt'), open('Tests/answerUsing.txt','r').read())
    def testUsingTwoDataTypes(self):
        self.assertEqual(mainParser('Tests/testUsingTwoDataTypes.txt'), open('Tests/answerUsingTwoDataTypes.txt','r').read())
    def testUsingThreeDataTypes(self):
        self.assertEqual(mainParser('Tests/testUsingThreeDataTypes.txt'), open('Tests/answerUsingThreeDataTypes.txt','r').read())
    def testScan(self):
        self.assertEqual(mainParser('Tests/testScan.txt'), open('Tests/answerScan.txt','r').read())
    def testCurlySet(self):
        self.assertEqual(mainParser('Tests/testCurlySet.txt'), open('Tests/answerCurlySet.txt','r').read())
    def testAssignErrors(self):
        self.assertEqual(mainParser('Tests/testAssignErrors.txt'), open('Tests/answerAssignErrors.txt','r').read())
    def testError(self):
        self.assertEqual(mainParser('Tests/testError.txt'), open('Tests/answerError.txt','r').read())
    def testError2(self):
        self.assertEqual(mainParser('Tests/testError2.txt'), open('Tests/answerError2.txt','r').read())
    def testIf2(self):
        self.assertEqual(mainParser('Tests/testIf2.txt'), open('Tests/answerIf2.txt','r').read())
    def testIfElse2(self):
        self.assertEqual(mainParser('Tests/testIfElse2.txt'), open('Tests/answerIfElse2.txt','r').read())
    def testSimpleFor(self):
        self.assertEqual(mainParser('Tests/testSimpleFor.txt'), open('Tests/answerSimpleFor.txt','r').read())
    def testSimpleForMultiOperations(self):
        self.assertEqual(mainParser('Tests/testSimpleForMultiOperations.txt'), open('Tests/answerSimpleForMultiOperations.txt','r').read())
    def testSimpleForInvertedDirection(self):
        self.assertEqual(mainParser('Tests/testSimpleForInvertedDirection.txt'), open('Tests/answerSimpleForInvertedDirection.txt','r').read())
    def testSimpleWhile(self):
        self.assertEqual(mainParser('Tests/testSimpleWhile.txt'), open('Tests/answerSimpleWhile.txt','r').read())
    def testNestedOperation(self):
        self.assertEqual(mainParser('Tests/testNestedOperation.txt'), open('Tests/answerNestedOperation.txt','r').read())
    def testRepeatWhileDo(self):
        self.assertEqual(mainParser('Tests/testRepeatWhileDo.txt'), open('Tests/answerRepeatWhileDo.txt','r').read())
    def testRepeatWhile(self):
        self.assertEqual(mainParser('Tests/testRepeatWhile.txt'), open('Tests/answerRepeatWhile.txt','r').read())
    def testNestedOperation2(self):
        self.assertEqual(mainParser('Tests/testNestedOperation2.txt'), open('Tests/answerNestedOperation2.txt','r').read())
    def testNestedOperationSets(self):
        self.assertEqual(mainParser('Tests/testNestedOperationSets.txt'), open('Tests/answerNestedOperationSets.txt','r').read())
    def testNestedOperationSets2(self):
        self.assertEqual(mainParser('Tests/testNestedOperationSets2.txt'), open('Tests/answerNestedOperationSets2.txt','r').read())
    def testFor(self):
        self.assertEqual(mainParser('Tests/testFor.txt'), open('Tests/answerFor.txt','r').read())
    def testSetsOperators(self):
        self.assertEqual(mainParser('Tests/testSetsOperators.txt'), open('Tests/answerSetsOperators.txt','r').read())
    def testIfElse3(self):
        self.assertEqual(mainParser('Tests/testIfElse3.txt'), open('Tests/answerIfElse3.txt','r').read())
    def testIfError1(self):
        self.assertEqual(mainParser('Tests/testIfError1.txt'), open('Tests/answerIfError1.txt','r').read())
    def testIfError2(self):
        self.assertEqual(mainParser('Tests/testIfError2.txt'), open('Tests/answerIfError2.txt','r').read())
    def testForInsideFor(self):
        self.assertEqual(mainParser('Tests/testForInsideFor.txt'), open('Tests/answerForInsideFor.txt','r').read())
    def testAll(self):
        self.assertEqual(mainParser('Tests/testAll.txt'), open('Tests/answerAll.txt','r').read())
    def testPrecedenceOperators(self):
        self.assertEqual(mainParser('Tests/testPrecedenceOperators.txt'), open('Tests/answerPrecedenceOperators.txt','r').read())
    def testAssociativeOperatorsSets(self):
        self.assertEqual(mainParser('Tests/testAssociativeOperatorsSets.txt'), open('Tests/answerAssociativeOperatorsSets.txt','r').read())
    def testFibonacci(self):
        self.assertEqual(mainParser('Tests/testFibonacci.txt'), open('Tests/answerFibonacci.txt','r').read())
    def testWhileInsideRepeat(self):
        self.assertEqual(mainParser('Tests/testWhileInsideRepeat.txt'), open('Tests/answerWhileInsideRepeat.txt','r').read())
    

if __name__ == '__main__':
    unittest.main()
