from Node import Node
class SyntaxNode(Node):
    def __init__(self, data=None, pos=None, anulable=None, primeros=None, ultimos=None):
        super().__init__(data=data)
        self.__pos = pos
        self.__anulable = anulable
        self.__primeros = primeros
        self.__ultimos = ultimos

    def getPos(self):
        return self.__pos

    def setPos(self, pos):
        self.__pos = pos

    def getAnulable(self):
        return self.__anulable

    def setAnulable(self, anulable):
        self.__anulable = anulable

    def getPrimeros(self):
        return self.__primeros

    def setPrimeros(self, primeros):
        self.__primeros = primeros

    def getUltimos(self):
        return self.__ultimos

    def setUltimos(self, ultimos):
        self.__ultimos = ultimos