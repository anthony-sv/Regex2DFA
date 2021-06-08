from Acceptor import Acceptor
from Transition import Transition

class Afd(Acceptor):
    def __init__(self, F, Fsm, T):
        super().__init__(F, Fsm)
        self.Transition = T

    @staticmethod
    def printDFAState(state):
        return f"{set([x.getName() for x in state.getName()])}"

    @staticmethod
    def printDFAStates(listofstates):
        lis = []
        for x in listofstates:
            lis.append(Afd.printDFAState(x))
        print(f"Q: {set([x for x in lis])}")

    @staticmethod
    def printAlphabet(alphabet):
        lis = []
        for x in alphabet:
            lis.append(x)
        print(f"Σ: {set([x.getCharacter() for x in lis])}")

    @staticmethod
    def printFinalStates(finalstateslist):
        lis = []
        for x in finalstateslist:
            lis.append(Afd.printDFAState(x))
        print(f"F: {set([x for x in lis])}")

    @staticmethod
    def printDFATransition(trans):
        for key, value in trans.items():
            print(f"δ({Afd.printDFAState(key[0])}, {key[1].getCharacter()}) = {Afd.printDFAState(value)}")
