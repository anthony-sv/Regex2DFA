class Symbol:
    def __init__(self, c):
        self.character = c
    def getCharacter(self):
        return self.character

    @staticmethod
    def isOperator(character):
        if Symbol.isStar(character) or Symbol.isConcat(character) or Symbol.isOr(character):
            return True
        else:
            return False

    @staticmethod
    def isLeftParenthesis(character):
        if character == '(':
            return True

    @staticmethod
    def isRightParenthesis(character):
        if character == ')':
            return True

    @staticmethod
    def isStar(character):
        if character == "*":
            return True
        else:
            return False

    @staticmethod
    def isConcat(character):
        if character == '.':
            return True
        else:
            return False

    @staticmethod
    def isOr(character):
        if character == '|':
            return True
        else:
            return False

    @staticmethod
    def isOperand(character):
        if not Symbol.isOperator(character) and not Symbol.isLeftParenthesis(character) and not Symbol.isRightParenthesis(character):
            return True
        else:
            return False

    @staticmethod
    def checkPrecedence(x):
        if Symbol.isStar(x):
            return 2
        elif Symbol.isConcat(x):
            return 1
        elif Symbol.isOr(x):
            return 0