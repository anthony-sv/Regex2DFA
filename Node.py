class Node:
    def __init__(self, data=None):
        self.__data = data

    def getData(self):
        return self.__data
    def setData(self, data):
        self.__data = data