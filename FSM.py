class Fsm:
    def __init__(self, Q, q0, Sigma):
        self.Q = Q
        self.q0 = q0
        self.Sigma = Sigma
    def getAllStates(self):
        #return [x.getStateName() for x in self.Q]
        return self.Q
    def getInitialState(self):
        #return self.q0.getStateName()
        return self.q0
    def getAlphabet(self):
        #return [x.getCharacter() for x in self.Sigma.sigma
        return self.Sigma.sigma