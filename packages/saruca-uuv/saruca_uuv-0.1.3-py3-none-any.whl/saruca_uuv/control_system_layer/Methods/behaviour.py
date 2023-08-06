# water engine
from saruca_uuv.sensing_system_layer.Methods.variables import EntityLayer


def behaviour():
    entity = EntityLayer([0, 0], "circle", 40, [8, "", 8], (2, 3))
    return entity.getPositionVector()

print("Aracin davranisi saptandi.")