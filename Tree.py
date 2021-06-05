from Symbol import Symbol
from Regex import Regex
from Node import Node
from Stack import Stack
class Tree:
    def __init__(self, n=Node(), left=None, right=None):
        self.__left : Tree = left
        self.__right : Tree = right
        self.__node : Node = n

    def getNode(self) -> Node:
        return self.__node
    def setNode(self, node : Node) -> None:
        self.__node = node
    
    def getLeft(self) -> "Tree":
        return self.__left
    def setLeft(self, left : "Tree") -> None:
        self.__left = left
    
    def getRight(self) -> "Tree":
        return self.__right
    def setRight(self, right : "Tree") -> None:
        self.__right = right

    @staticmethod
    def getSyntaxTree(regexap: str) -> "Tree":
        s = Stack()
        for x in regexap:
            if Symbol.isOperand(x) or x == 'ε' or x == '#':
                tempN = Node(data=x)
                tempT = Tree(n=tempN)
                s.push(tempT)
            elif Symbol.isOperator(x):
                if Symbol.isOr(x):
                    p1 = s.pop()
                    p2 = s.pop()
                    tempN = Node(data=x)
                    tempT = Tree(n=tempN)
                    tempT.setLeft(p2)
                    tempT.setRight(p1)
                    s.push(tempT)
                elif Symbol.isConcat(x):
                    p1 = s.pop()
                    p2 = s.pop()
                    tempN = Node(data=x)
                    tempT = Tree(n=tempN)
                    tempT.setLeft(p2)
                    tempT.setRight(p1)
                    s.push(tempT)
                elif Symbol.isStar(x):
                    p = s.pop()
                    tempN = Node(data=x)
                    tempT = Tree(n=tempN)
                    tempT.setLeft(p)
                    s.push(tempT)
        return s.peek()

    @staticmethod
    def inorderTraversal(root):
        res = []
        if root:
            res = Tree.inorderTraversal(root.__left)
            res.append(root.__node.getData())
            res = res + Tree.inorderTraversal(root.__right)
        return res