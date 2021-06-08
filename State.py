class State:
    def __init__(self, stateName, isInitial=False, isFinal=False):
        self.name = stateName
        self.isInitial = isInitial
        self.isFinal = isFinal
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name
    def getIsInitialState(self):
        return self.isInitial
    def setIsInitialState(self, isInitial=True):
        self.isInitial = isInitial
    def getIsFinalState(self):
        return self.isFinal
    def setIsFinalState(self, isFinal=True):
        self.isFinal = isFinal
