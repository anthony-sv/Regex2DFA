class Alphabet:
    def __init__(self, listOfSymbols=[]):
        self.sigma = listOfSymbols
    def addSymbolToAlphabet(self, symbol):
        self.sigma.append(symbol)