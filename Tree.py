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
                    #tempT.setRight(Tree(n=Node()))
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

    @staticmethod
    def postorderTraversalPos(root):
        res = []
        if root:
            res = Tree.postorderTraversalPos(root.__left)
            res = res + Tree.postorderTraversalPos(root.__right)
            res.append(root.getNode().getPos())
        return res

    @staticmethod
    def postorderTraversalAnul(root):
        res = []
        if root:
            res = Tree.postorderTraversalAnul(root.__left)
            res = res + Tree.postorderTraversalAnul(root.__right)
            res.append(root.getNode().getAnulable())
        return res

    @staticmethod
    def postorderTraversalPrim(root):
        res = []
        if root:
            res = Tree.postorderTraversalPrim(root.__left)
            res = res + Tree.postorderTraversalPrim(root.__right)
            res.append(root.getNode().getPrimeros())
        return res

    @staticmethod
    def postorderTraversalUlt(root):
        res = []
        if root:
            res = Tree.postorderTraversalUlt(root.__left)
            res = res + Tree.postorderTraversalUlt(root.__right)
            res.append(root.getNode().getUltimos())
        return res

    @staticmethod
    def tryPos(root):
        res = Tree.postorderTraversalTree(root)
        count = 1
        for x in res:
            if Symbol.isOperand(x.getNode().getData()) or x.getNode().getData() == 'ε':
                x.getNode().setPos(count)
                count = count+1
        gg = Tree.postorderTraversalPos(root)
        return gg

    @staticmethod
    def tryAnulable(root):
        res = Tree.postorderTraversalTree(root)
        for x in res:
            if x.getNode().getData() == 'ε':
                x.getNode().setAnulable(True)
            elif x.getNode().getPos() != None:
                x.getNode().setAnulable(False)
            elif x.getNode().getData() == '|':
                op = x.getLeft().getNode().getAnulable() or x.getRight().getNode().getAnulable()
                x.getNode().setAnulable(op)
            elif x.getNode().getData() == '.':
                op = x.getLeft().getNode().getAnulable() and x.getRight().getNode().getAnulable()
                x.getNode().setAnulable(op)
            elif x.getNode().getData() == '*':
                x.getNode().setAnulable(True)
        gg = Tree.postorderTraversalAnul(root)
        return gg

    @staticmethod
    def tryPrimeros(root):
        res = Tree.postorderTraversalTree(root)
        for x in res:
            if x.getNode().getData() == 'ε':
                x.getNode().setPrimeros(set())
            elif x.getNode().getPos() != None:
                s = set()
                s.add(x.getNode().getPos())
                x.getNode().setPrimeros(s)
            elif x.getNode().getData() == '|':
                ppc1 = x.getLeft().getNode().getPrimeros()
                ppc2 = x.getRight().getNode().getPrimeros()
                x.getNode().setPrimeros(ppc1 | ppc2)
            elif x.getNode().getData() == '.':
                if x.getLeft().getNode().getAnulable() == True:
                    ppc1 = x.getLeft().getNode().getPrimeros()
                    ppc2 = x.getRight().getNode().getPrimeros()
                    x.getNode().setPrimeros(ppc1 | ppc2)
                else:
                    x.getNode().setPrimeros(x.getLeft().getNode().getPrimeros())
            elif x.getNode().getData() == '*':
                x.getNode().setPrimeros(x.getLeft().getNode().getPrimeros())
        gg = Tree.postorderTraversalPrim(root)
        return gg

    @staticmethod
    def tryUltimos(root):
        res = Tree.postorderTraversalTree(root)
        for x in res:
            if x.getNode().getData() == 'ε':
                x.getNode().setUltimos(set())
            elif x.getNode().getPos() != None:
                s = set()
                s.add(x.getNode().getPos())
                x.getNode().setUltimos(s)
            elif x.getNode().getData() == '|':
                ppc1 = x.getLeft().getNode().getPrimeros()
                ppc2 = x.getRight().getNode().getPrimeros()
                x.getNode().setUltimos(ppc2 | ppc1)
            elif x.getNode().getData() == '.':
                if x.getRight().getNode().getAnulable() == True:
                    ppc1 = x.getLeft().getNode().getPrimeros()
                    ppc2 = x.getRight().getNode().getPrimeros()
                    x.getNode().setUltimos(ppc2 | ppc1)
                else:
                    x.getNode().setUltimos(x.getRight().getNode().getPrimeros())
            elif x.getNode().getData() == '*':
                x.getNode().setUltimos(x.getLeft().getNode().getPrimeros())
        gg = Tree.postorderTraversalUlt(root)
        return gg

    @staticmethod 
    def trySiguientes(root):
        res = Tree.postorderTraversalTree(root)
        #init dict
        nodedict = dict()
        for x in res:
            if x.getNode().getPos() != None:
                nodedict[x.getNode().getPos()] = set()
        for x in res:
            if x.getNode().getData() == '.':
                for y in x.getLeft().getNode().getUltimos():
                    temp = nodedict[y]
                    for z in x.getRight().getNode().getPrimeros():
                        temp.add(z)
                    nodedict[y] = temp
            elif x.getNode().getData() == '*':
                upn = x.getNode().getUltimos()
                ppn = x.getNode().getPrimeros()
                for x in upn:
                    temp = nodedict[x]
                    for y in ppn:
                        temp.add(y)
                    nodedict[x] = temp
        return nodedict

    @staticmethod
    def getAlphabetFromRegex(regexs):
        l = [char for char in regexs]
        al = []
        for i in range(len(l)):
            if Symbol.isOperand(l[i]) and l[i] != '#' and l[i] != 'ε':
                al.append(l[i])
        return list(dict.fromkeys(al))

    @staticmethod
    def getAutomaton(root, alphabet):
        sig = Tree.trySiguientes(root)
        inits = root.getNode().getPrimeros()
        Destados = [inits]
        Dtrans = dict()
        sinmarcar = []
        sinmarcar.append(inits)
        res = Tree.postorderTraversalTree(root)
        auxdict = dict()
        for r in res:
            if r.getNode().getPos() != None:
                auxdict[r.getNode().getPos()] = r.getNode().getData()
        while sinmarcar:
            s = sinmarcar.pop()
            for sy in alphabet:
                u = set()
                for pos in s:
                    if auxdict[pos] == sy:
                        u = u | sig[pos]
                if u not in Destados:
                    Destados.append(u)
                    sinmarcar.append(u)
                Dtrans[frozenset(s),sy] = u
        print(inits)
        print(Destados)
        print(Dtrans)

    # @staticmethod
    # def depth_first_search_recursive(graph, start, visited=None):
    #     if visited is None:
    #         visited = set()
    #     visited.add(start)
    #     for next in graph[start] - visited:
    #         Tree.depth_first_search_recursive(graph, next, visited)
    #     return visited
