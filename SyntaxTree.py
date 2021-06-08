from Tree import Tree
from Stack import Stack
from Symbol import Symbol
from SyntaxNode import SyntaxNode

class SyntaxTree(Tree):
    def __init__(self, n=SyntaxNode(), left=None, right=None):
        super().__init__(n=n, left=left, right=right)

    @staticmethod
    def postorderTraversalPos(root):
        res = []
        if root:
            res = SyntaxTree.postorderTraversalPos(root.getLeft())
            res = res + SyntaxTree.postorderTraversalPos(root.getRight())
            res.append(root.getNode().getPos())
        return res

    @staticmethod
    def postorderTraversalAnul(root):
        res = []
        if root:
            res = SyntaxTree.postorderTraversalAnul(root.getLeft())
            res = res + SyntaxTree.postorderTraversalAnul(root.getRight())
            res.append(root.getNode().getAnulable())
        return res

    @staticmethod
    def postorderTraversalPrim(root):
        res = []
        if root:
            res = SyntaxTree.postorderTraversalPrim(root.getLeft())
            res = res + SyntaxTree.postorderTraversalPrim(root.getRight())
            res.append(root.getNode().getPrimeros())
        return res

    @staticmethod
    def postorderTraversalUlt(root):
        res = []
        if root:
            res = SyntaxTree.postorderTraversalUlt(root.getLeft())
            res = res + SyntaxTree.postorderTraversalUlt(root.getRight())
            res.append(root.getNode().getUltimos())
        return res
