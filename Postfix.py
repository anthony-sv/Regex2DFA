from Stack import Stack
from Regex import Regex
from Symbol import Symbol

class Postfix:
    def __init__(self, regex):
        self.__regex = regex.expression
        self.__modr = Postfix.modRegex(self.__regex)
        self.__pila = Stack()
        self.__postfix = self.convertInfixToPostfix()
    
    def getRegex(self):
        return self.__regex
    
    def getExtendedRegex(self):
        return self.__extended

    def getModifiedRegex(self):
        return self.__modr

    def getPostfix(self):
        return self.__postfix

    @staticmethod
    def isConcat(character, nextCharacter):
        if Symbol.isOperand(character) and Symbol.isOperand(nextCharacter):
            return True
        elif Symbol.isRightParenthesis(character) and Symbol.isLeftParenthesis(nextCharacter):
            return True
        elif Symbol.isStar(character) and Symbol.isOperand(nextCharacter):
            return True
        elif Symbol.isStar(character) and Symbol.isLeftParenthesis(nextCharacter):
            return True
        elif Symbol.isOperand(character) and Symbol.isLeftParenthesis(nextCharacter):
            return True
        elif Symbol.isRightParenthesis(character) and nextCharacter == "#":
            return True
        elif Symbol.isRightParenthesis(character) and Symbol.isOperand(nextCharacter):
            return True
        else:
            return False

    @staticmethod
    def modRegex(reg):
        list = [char for char in reg+'$']
        nlist = []
        for i in range(len(list)-1):
            if Postfix.isConcat(list[i], list[i+1]) and list[i+1] != '$':
                nlist.append(list[i])
                nlist.append('.')
            elif(list[i] != list[-1] and list[i+1] != '$'):
                nlist.append(list[i])
            else:
                nlist.append(list[i])
        return "".join(nlist)

    def convertInfixToPostfix(self):
        self.__pila.push('(')
        tempr = self.__modr+')'
        auxpost = ""
        for i in range(len(tempr)):
            if Symbol.isOperand(tempr[i]):
                auxpost += tempr[i]
            elif Symbol.isLeftParenthesis(tempr[i]):
                self.__pila.push(tempr[i])
            elif Symbol.isOperator(tempr[i]):
                while not self.__pila.isEmpty() and Symbol.isOperator(self.__pila.peek()) and (Symbol.checkPrecedence(self.__pila.peek()) >= Symbol.checkPrecedence(tempr[i])):
                    auxpost += self.__pila.pop()
                self.__pila.push(tempr[i])
            elif Symbol.isRightParenthesis(tempr[i]):
                while not self.__pila.isEmpty() and not Symbol.isLeftParenthesis(self.__pila.peek()):
                    auxpost += self.__pila.pop()
                self.__pila.pop()
        return auxpost