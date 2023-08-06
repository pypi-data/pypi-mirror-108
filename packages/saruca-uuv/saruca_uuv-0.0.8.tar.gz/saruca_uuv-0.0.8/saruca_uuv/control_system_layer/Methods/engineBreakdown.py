"""
    engine breakdown
"""


from saruca_uuv.sensing_system_layer.Methods.variables import EntityLayer


def engineBreakdown():
    entity = EntityLayer([0, 0], "circle", 40, [8, "", 8], (2, 3))
    if entity.getOtherVariables() == ["", 1]:
        return 1
    else:
        return 0
