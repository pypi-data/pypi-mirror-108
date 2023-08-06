# image processing
# variables

class EntityLayer:
    __boundingBox = []
    __otherVariables = []
    __objectType = ''
    __objectDistance = 0
    __positionVector = (0, 0)

    def __init__(self,
                 boundingBoxes=None,
                 objectType=None,
                 objectDistance=None,
                 otherVariables=None,
                 positionVector=None):
        if boundingBoxes is None:
            self.__boundingBox = []
        else:
            for __boundingBox in boundingBoxes:
                self.__boundingBox = boundingBoxes
        if otherVariables is None:
            self.__otherVariables = []
        else:
            for __otherVariables in otherVariables:
                self.__otherVariables = otherVariables
        if objectType is None:
            self.__objectType = ''
        else:
            self.__objectType = objectType
        if objectDistance is None:
            self.__objectDistance = 0
        else:
            self.__objectDistance = objectDistance
        if positionVector is None:
            self.__positionVector = (0, 0)
        else:
            self.__positionVector = positionVector

    def getBoundingBoxes(self):
        return self.__boundingBox

    def getOtherVariables(self):
        return self.__otherVariables

    def getObjectType(self):
        return self.__objectType

    def getObjectDistance(self):
        return self.__objectDistance

    def getPositionVector(self):
        return self.__positionVector
