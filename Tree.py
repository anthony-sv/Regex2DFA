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
    def inorderTraversal(root):
        res = []
        if root:
            res = Tree.inorderTraversal(root.__left)
            res.append(root.__node.getData())
            res = res + Tree.inorderTraversal(root.__right)
        return res

    @staticmethod
    def postorderTraversal(root):
        res = []
        if root:
            res = Tree.postorderTraversal(root.__left)
            res = res + Tree.postorderTraversal(root.__right)
            res.append(root.__node.getData())
        return res

    @staticmethod
    def postorderTraversalTree(root):
        res = []
        if root:
            res = Tree.postorderTraversalTree(root.__left)
            res = res + Tree.postorderTraversalTree(root.__right)
            res.append(root)
        return res

    # @staticmethod
    # def depth_first_search_recursive(graph, start, visited=None):
    #     if visited is None:
    #         visited = set()
    #     visited.add(start)
    #     for next in graph[start] - visited:
    #         Tree.depth_first_search_recursive(graph, next, visited)
    #     return visited
