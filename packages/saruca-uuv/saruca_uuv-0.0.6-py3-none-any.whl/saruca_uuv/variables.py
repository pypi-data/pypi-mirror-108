# position vector
# other variables
from ..Classes.EntityLayer import EntityLayer

x = 221
y = 128
otherVar = ["circle", 24]
variableObject = EntityLayer((0, 0), otherVar, 0, "", (x, y))
print(variableObject.getOtherVariables() + variableObject.getPositionVector())
