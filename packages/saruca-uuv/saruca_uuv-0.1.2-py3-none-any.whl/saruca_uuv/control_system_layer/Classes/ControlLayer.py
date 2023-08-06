# assignment
# behaviour
# orbit
# command
"""
from ..Methods.assignment import assignment
from ..Methods.orbit import orbit
from ..Methods.command import command
from ..Methods.behaviour import behaviour
from ..Methods.engineBreakdown import engineBreakdown
"""


class ControlLayer:
    __assignment = ""
    __orbit = ""
    __command = ["", 5]
    __behaviour = ""
    __engineBreakdown = 0

    def __int__(self,
                assignment=None,
                orbit=None,
                command=None,
                behaviour=None,
                engineBreakdown=None):
        if assignment is None:
            self.__assignment = ""
        else:
            self.__assignment = assignment
        if orbit is None:
            self.__orbit = ""
        else:
            self.__orbit = orbit
        if command is None:
            self.__command = ["", 5]
        else:
            for __command in command:
                self.__command = command
        if behaviour is None:
            self.__behaviour = ""
        else:
            self.__behaviour = behaviour
        if engineBreakdown is None:
            self.__engineBreakdown = 0
        else:
            self.__engineBreakdown = engineBreakdown

    def getAssignment(self):
        return self.__assignment

    def getOrbit(self):
        return self.__orbit

    def getCommand(self):
        return self.__command

    def getBehaviour(self):
        return self.__behaviour

    def getEngineBreakdown(self):
        return self.__engineBreakdown
