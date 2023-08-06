# orbital redirection

from saruca_uuv.sensing_system_layer.Methods.variables import EntityLayer


def orbit():
    entity = EntityLayer([0, 0], "circle", 40, [8, "", 8], (2, 3))
    if entity.getPositionVector() == (2, 3):
        return "forward/backward"
    else:
        return "right/left"
