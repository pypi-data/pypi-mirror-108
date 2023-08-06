# data send operations

from saruca_uuv.sensing_system_layer.Methods.variables import EntityLayer


def command():
    entity = EntityLayer([0, 0], "circle", 40, [8, "", 8], (2, 3))
    return entity.getOtherVariables()

print("Komut metodu calistirildi...")