# state
# localization

class VehicleComprehendLayer:
    __speed = 0
    __accel = 0.0
    __directory = ""
    __angle = 0.0
    __poolSize = [(25, 50, 2), (12.5, 25, 2)]

    def __init__(self,
                 speed=None,
                 accel=None,
                 directory=None,
                 angle=None,
                 poolSize=None):
        if speed is None:
            self.__speed = 0
        else:
            self.__speed = speed
        if accel is None:
            self.__accel = 0.0
        else:
            self.__accel = accel
        if directory is None:
            self.__directory = ""
        elif directory == "forward" or directory == "ileri":
            self.__directory = "forward"
        else:
            self.__directory = directory
        if angle is None:
            self.__angle = 0.0
        else:
            self.__angle = angle
        if poolSize is None:
            self.__poolSize = [(25, 50, 2), (25, 50, 2)]
        else:
            self.__poolSize = poolSize

    def getSpeed(self):
        return self.__speed

    def getAccel(self):
        return self.__accel

    def getDirectory(self):
        return self.__directory

    def getAngle(self):
        return self.__angle

    def getPoolSize(self):
        return self.__poolSize
