from State import State
import networkx as nx
import os
from AFN import Afn
from AFD import Afd
class PlotAutomaton:
    def __init__(self, automaton):
        self.automaton = automaton
    
    def plotAutomaton(self, regex):
        G = nx.MultiDiGraph()
        for x in self.automaton.Fsm.Q:
            if x.getIsFinalState():
                G.add_node(x.getName(), peripheries=2)
            else:
                G.add_node(x.getName())
        for key, value in self.automaton.Transition.dict.items():
            if isinstance(self.automaton, Afn):
                for x in value:
                    G.add_edge(key[0].getName(), x.getName(), label=key[1])
            else:
                G.add_edge(key[0].getName(), x.getName(), label=key[1])
        nx.nx_agraph.write_dot(G, "nfa.gv")
        os.system("dot nfa.gv -Tpng > nfa.png")
        f = open("nfa.gv")
        lines = f.readlines()
        lines.insert(1, '\tlabelloc="t";\n')
        lines.insert(2, f'\tlabel="{regex.expression}";\n')
        lines.insert(3, '\trankdir=LR;\n')
        lines.insert(4, '\t" " [shape=plaintext];\n')
        lines.insert(5, f'\t" " -> {self.automaton.Fsm.q0.getName()};\n')
        f = open("nfa.gv", "w")
        for x in lines:
            f.write(x)
        f.close()
        os.system("dot nfa.gv -Tpng > nfa.png")
        os.system("xdg-open nfa.png")

    def plotDFA(self, regex):
        f = open("dfa.gv", 'w')
        lines = ['digraph G {\n',
                 '\trankdir=LR\n',
                 '\tlabelloc="t";\n',
                 f'\tlabel="{regex.expression}"\n',
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
