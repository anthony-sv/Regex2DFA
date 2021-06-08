class Transition:
    def __init__(self, dict):
        self.dict = dict

    @staticmethod
    def getInitialStateFromTransition(transition):
        sl = []
        for x in transition.keys():
            sl.append(x[0])
            for y in transition[x]:
                sl.append(y)
        for z in sl:
            if z.getIsInitialState():
                return z
            else:
                pass

    @staticmethod
    def getFinalStateFromTransition(transition):#only works for NFA's
        sl = []
        for x in transition.keys():
            sl.append(x[0])
            for y in transition[x]:
                sl.append(y)
        for z in sl:
            if z.getIsFinalState():
                return z
            else:
                pass

    @staticmethod
    def printTransition(trans):
        for key, value in trans.items():
            gg = set([x.getName() for x in value])
            s = ', '.join(gg)
            print(f"δ({key[0].getName()}, {key[1]}) = {{{s}}} ")