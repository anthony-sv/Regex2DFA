from Symbol import Symbol
from Stack import Stack
from AFD import Afd
from Tree import Tree
import os
class PlotTree():
    def __init__(self, tree):
        self.tree = tree
    
    def plotTree(self, regex):
        f = open("tree.gv", 'w')
        lines = ['digraph G {\n']
        s = Stack()
        auxdict = dict()
        for i,x in enumerate(Tree.postorderTraversalTree(self.tree)):
            if Symbol.isOperand(x.getNode().getData()) or x.getNode().getData() == '#':
                s.push(x)
                auxdict[x] = i
            elif Symbol.isOperator(x.getNode().getData()):
                if Symbol.isOr(x.getNode().getData()):
                    p1 = s.pop()
                    p2 = s.pop()
                    auxdict[x] = i
                    lines.append(f'\t{i} -> {auxdict[p2]}\n')
                    lines.append(f'\t{i} -> {auxdict[p1]}\n')
                    s.push(x)
                elif Symbol.isConcat(x.getNode().getData()):
                    p1 = s.pop()
                    p2 = s.pop()
                    auxdict[x] = i
                    lines.append(f'\t{i} -> {auxdict[p2]}\n')
                    lines.append(f'\t{i} -> {auxdict[p1]}\n')
                    s.push(x)
                elif Symbol.isStar(x.getNode().getData()):
                    p = s.pop()
                    auxdict[x] = i
                    lines.append(f'\t{i} -> {auxdict[p]}\n')
                    s.push(x)
        for i,value in enumerate(Tree.postorderTraversalTree(self.tree)):
            lines.append(f'\t{i} [label="{value.getNode().getData()}"]\n')
        lines.append('}')
        f.writelines(lines)
        f.close()
        os.system("dot tree.gv -Tpng > tree.png")
        os.system("xdg-open tree.png")
