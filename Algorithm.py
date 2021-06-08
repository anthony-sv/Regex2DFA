
from PlotTree import PlotTree
from Stack import Stack
from SyntaxNode import SyntaxNode
from SyntaxTree import SyntaxTree
from Symbol import Symbol
from Tree import Tree
from Postfix import Postfix
from Regex import Regex
from AFD import Afd
from FSM import Fsm
from Alphabet import Alphabet
from Transition import Transition
from State import State
from PlotAutomaton import PlotAutomaton
class Algorithm:
    def __init__(self,regex):
        self.__regex = Regex(regex).expression
        self.__fregex = None
        self.__tree = None
        self.__afd = None

    def getRegex(self):
        return self.__regex
    def setRegex(self,r):
        self.__regex = r

    def getFRegex(self):
        return self.__fregex
    def setFRegex(self,fr):
        self.__fregex = fr

    def getTree(self):
        return self.__tree
    def setTree(self, t):
        self.__tree = t

    def getAfd(self):
        return self.__afd
    def setAfd(self, dfa):
        self.__afd = dfa

    @staticmethod
    def extendRegex(regex):
        l = ['(']
        for x in regex:
                l.append(x)
        return "".join(l)+")#"

    def getSyntaxTree(self):
        s = Stack()
        for x in self.__fregex:
            if Symbol.isOperand(x) or x == 'ε' or x == '#':
                tempN = SyntaxNode(data=x)
                tempT = SyntaxTree(n=tempN)
                s.push(tempT)
            elif Symbol.isOperator(x):
                if Symbol.isOr(x):
                    p1 = s.pop()
                    p2 = s.pop()
                    tempN = SyntaxNode(data=x)
                    tempT = SyntaxTree(n=tempN)
                    tempT.setLeft(p2)
                    tempT.setRight(p1)
                    s.push(tempT)
                elif Symbol.isConcat(x):
                    p1 = s.pop()
                    p2 = s.pop()
                    tempN = SyntaxNode(data=x)
                    tempT = SyntaxTree(n=tempN)
                    tempT.setLeft(p2)
                    tempT.setRight(p1)
                    s.push(tempT)
                elif Symbol.isStar(x):
                    p = s.pop()
                    tempN = SyntaxNode(data=x)
                    tempT = SyntaxTree(n=tempN)
                    tempT.setLeft(p)
                    #tempT.setRight(Tree(n=Node()))
                    s.push(tempT)
        self.__tree = s.peek()

    def tryPos(self):
        res = Tree.postorderTraversalTree(self.__tree)
        count = 1
        for x in res:
            if Symbol.isOperand(x.getNode().getData()) or x.getNode().getData() == 'ε':
                x.getNode().setPos(count)
                count = count+1

    def tryAnulable(self):
        res = Tree.postorderTraversalTree(self.__tree)
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

    def tryPrimeros(self):
        res = Tree.postorderTraversalTree(self.__tree)
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

    def tryUltimos(self):
        res = Tree.postorderTraversalTree(self.__tree)
        for x in res:
            if x.getNode().getData() == 'ε':
                x.getNode().setUltimos(set())
            elif x.getNode().getPos() != None:
                s = set()
                s.add(x.getNode().getPos())
                x.getNode().setUltimos(s)
            elif x.getNode().getData() == '|':
                upc1 = x.getLeft().getNode().getUltimos()
                upc2 = x.getRight().getNode().getUltimos()
                x.getNode().setUltimos(upc1 | upc2)
            elif x.getNode().getData() == '.':
                if x.getRight().getNode().getAnulable() == True:
                    upc1 = x.getLeft().getNode().getUltimos()
                    upc2 = x.getRight().getNode().getUltimos()
                    x.getNode().setUltimos(upc2 | upc1)
                else:
                    x.getNode().setUltimos(x.getRight().getNode().getUltimos())
            elif x.getNode().getData() == '*':
                x.getNode().setUltimos(x.getLeft().getNode().getUltimos())

    def trySiguientes(self):
        res = Tree.postorderTraversalTree(self.__tree)
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

    def getSharpPos(self):
        res = Tree.postorderTraversalTree(self.__tree)
        for x in res:
            if x.getNode().getData() == '#':
                return x.getNode().getPos()

    def getAutomaton(self):
        sig = self.trySiguientes()
        inits = self.__tree.getNode().getPrimeros()
        Destados = [inits]
        Dtrans = dict()
        sinmarcar = []
        sinmarcar.append(inits)
        res = Tree.postorderTraversalTree(self.__tree)
        auxdict = dict()
        for r in res:
            if r.getNode().getPos() != None:
                auxdict[r.getNode().getPos()] = r.getNode().getData()
        while sinmarcar:
            s = sinmarcar.pop()
            for sy in Algorithm.getAlphabetFromRegex(self.__fregex):
                u = set()
                for pos in s:
                    if auxdict[pos] == sy:
                        u = u | sig[pos]
                if u not in Destados and len(u) != 0:
                    Destados.append(u)
                    sinmarcar.append(u)
                if len(u) != 0:
                    Dtrans[State(s), Symbol(sy)] = State(u)
        #construct automaton
        D = Afd([], Fsm([], None, Alphabet()), Transition({}))
        D.Fsm.q0 = State(inits, True, False)
        for x in Destados:
            D.Fsm.Q.append(State(x))
        D.Transition.dict = Dtrans
        for x in Algorithm.getAlphabetFromRegex(self.__fregex):
            D.Fsm.Sigma.sigma.append(Symbol(x))
        for y in D.Fsm.Q:
            if self.getSharpPos() in y.getName():
                y.setIsFinalState()
        for z in D.Fsm.Q:
            if State.getIsFinalState(z):
                D.F.append(z)
        self.setAfd(D)

    def TreeAlgorithm(self):
        self.setFRegex(Postfix(Regex(Algorithm.extendRegex(self.__regex))).getPostfix())
        self.getSyntaxTree()
        self.tryPos()
        self.tryAnulable()
        self.tryPrimeros()
        self.tryUltimos()
        self.trySiguientes()
        self.getAutomaton()
    
    def printDFA(self):
        PT = PlotTree(self.__tree)
        PT.plotTree(self.getSyntaxTree())
        print("\nEl AFD para la expresión regular es:")
        print("")
        Afd.printDFAStates(self.getAfd().Fsm.Q)
        Afd.printAlphabet(self.getAfd().Fsm.Sigma.sigma)
        print("q0: ",Afd.printDFAState(self.getAfd().Fsm.q0))
        Afd.printFinalStates(self.getAfd().F)
        Afd.printDFATransition(self.getAfd().Transition.dict)
        PA = PlotAutomaton(self.getAfd())
        PA.plotDFA(self.getRegex())
