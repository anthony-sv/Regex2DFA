from Postfix import Postfix
from AFN import Afn
from FSM import Fsm
from Alphabet import Alphabet
from Transition import Transition
from Symbol import Symbol
from State import State
from Stack import Stack
from Regex import Regex
from PlotAutomaton import PlotAutomaton
class Thompson:
    def __init__(self, regex):
        self.regex = Regex(regex)
        self.modRegex = self.modRegex()
        self.automata = Afn([],Fsm([],None, Alphabet()),Transition({}))
        self.pila = Stack()

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
        else:
            return False

    def modRegex(self):
        list = [char for char in self.regex.expression+'$']
        nlist = []
        for i in range(len(list)-1):
            if Thompson.isConcat(list[i], list[i+1]) and list[i+1] != '$':
                nlist.append(list[i])
                nlist.append('.')
            elif(list[i] != list[-1] and list[i+1] != '$'):
                nlist.append(list[i])
            else:
                nlist.append(list[i])
        return "".join(nlist)

    def getAlphabetFromRegex(self):
        l = [char for char in self.regex.expression]
        al = []
        for i in range(len(l)-1):
            if Symbol.isOperand(l[i]):
                al.append(l[i])
        return list(dict.fromkeys(al))

    def plantillaOperandoOEpsilon(self,x):
        if self.automata.Fsm.Q == []:
            ins = State('q0', True, False)
            fs = State('q1', False, True)
            di = {(ins, x): [fs]}
            self.pila.push(di)
            self.automata.Fsm.Q.append(ins)
            self.automata.Fsm.Q.append(fs)
        else:
            ns1n = 'q'+str(max([int(x.getName().split('q')[1]) for x in self.automata.Fsm.Q])+1)
            ns1 = State(ns1n, True, False)
            self.automata.Fsm.Q.append(ns1)
            ns2n = 'q'+str(max([int(x.getName().split('q')[1]) for x in self.automata.Fsm.Q])+1)
            ns2 = State(ns2n, False, True)
            self.automata.Fsm.Q.append(ns2)
            self.pila.push({(ns1, x): [ns2]})

    def plantillaEstrella(self):
        x = self.pila.stack.pop()
        ns1n = 'q'+str(max([int(x.getName().split('q')[1]) for x in self.automata.Fsm.Q])+1)
        ns1 = State(ns1n, True, False)
        self.automata.Fsm.Q.append(ns1)
        ns2n = 'q'+str(max([int(x.getName().split('q')[1]) for x in self.automata.Fsm.Q])+1)
        ns2 = State(ns2n, False, True)
        self.automata.Fsm.Q.append(ns2)
        initTrans = Transition.getInitialStateFromTransition(x)
        finalTrans = Transition.getFinalStateFromTransition(x)
        initTrans.setIsInitialState(False)
        finalTrans.setIsFinalState(False)
        starStates = [initTrans, ns2]
        x[(ns1, 'Ɛ')] = starStates
        x[(finalTrans, 'Ɛ')] = starStates
        self.pila.push(x)

    def plantillaConcatenacion(self):
        x1 = self.pila.pop()
        x2 = self.pila.pop()
        initTransx1 = Transition.getInitialStateFromTransition(x1)
        initTransx1.setIsInitialState(False)
        finTransx2 = Transition.getFinalStateFromTransition(x2)
        finTransx2.setIsFinalState(False)
        for key, value in x2.items():
            if finTransx2 in x2[key]:
                value.remove(finTransx2)
                value.append(initTransx1)
                x2[key] = value
        self.pila.push({**x2, **x1})
        self.automata.Fsm.Q.remove(finTransx2)

    def plantillaOr(self):
        x1 = self.pila.pop()
        x2 = self.pila.pop()
        initTransx1 = Transition.getInitialStateFromTransition(x1)
        initTransx1.setIsInitialState(False)
        finTransx1 = Transition.getFinalStateFromTransition(x1)
        finTransx1.setIsFinalState(False)
        initTransx2 = Transition.getInitialStateFromTransition(x2)
        initTransx2.setIsInitialState(False)
        finTransx2 = Transition.getFinalStateFromTransition(x2)
        finTransx2.setIsFinalState(False)
        ns1n = 'q'+str(max([int(x.getName().split('q')[1]) for x in self.automata.Fsm.Q])+1)
        ns1 = State(ns1n, True, False)
        self.automata.Fsm.Q.append(ns1)
        ns2n = 'q'+str(max([int(x.getName().split('q')[1]) for x in self.automata.Fsm.Q])+1)
        ns2 = State(ns2n, False, True)
        self.automata.Fsm.Q.append(ns2)
        newDict = {**x2, **x1}
        newDict[(ns1, 'Ɛ')] = [initTransx1, initTransx2]
        newDict[(finTransx1, 'Ɛ')] = [ns2]
        newDict[(finTransx2, 'Ɛ')] = [ns2]
        self.pila.push(newDict)

    def getAFNFromTransitions(self):
        self.automata.Transition.dict = self.pila.peek()
        self.automata.Fsm.Sigma = Alphabet([Symbol(x) for x in self.getAlphabetFromRegex()])
        self.automata.Fsm.q0 = Transition.getInitialStateFromTransition(self.pila.peek())
        self.automata.F = Transition.getFinalStateFromTransition(self.pila.peek())

    def ThompsonContruction(self):
        #compute transitions
        for x in Postfix(Regex(self.modRegex)).postfix:
            if Symbol.isOperand(x):
                self.plantillaOperandoOEpsilon(x)
            elif Symbol.isOperator(x):
                if Symbol.isStar(x):
                    self.plantillaEstrella()
                elif Symbol.isConcat(x):
                    self.plantillaConcatenacion()
                elif Symbol.isOr(x):
                    self.plantillaOr()
        self.getAFNFromTransitions()

    def printAutomaton(self):
        P = PlotAutomaton(self.automata)
        P.plotAutomaton(self.regex)
