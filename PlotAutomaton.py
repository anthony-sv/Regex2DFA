from State import State
import networkx as nx
import os
from AFD import Afd
class PlotAutomaton:
    def __init__(self, automaton):
        self.automaton = automaton

    def plotDFA(self, regex):
        f = open("dfa.gv", 'w')
        lines = ['digraph G {\n',
                 '\trankdir=LR\n',
                 '\tlabelloc="t";\n',
                 f'\tlabel="{regex}"\n',
                 '\t" " [shape=plaintext]']
        for x in self.automaton.Fsm.Q:
            maybefinal = "[peripheries=2]"
            lines.append(f'\t"{Afd.printDFAState(x)}" {maybefinal if x.getIsFinalState() else ""} \n')
        lines.append(f'\t" " -> "{Afd.printDFAState(self.automaton.Fsm.q0)}" \n')
        for key, value in self.automaton.Transition.dict.items():
            lines.append(f'\t"{Afd.printDFAState(key[0])}" -> "{Afd.printDFAState(value)}" [label="{key[1].getCharacter()}"]\n')
        lines.append('}')
        f.writelines(lines)
        f.close()
        os.system("dot dfa.gv -Tpng > dfa.png")
        os.system("xdg-open dfa.png")
