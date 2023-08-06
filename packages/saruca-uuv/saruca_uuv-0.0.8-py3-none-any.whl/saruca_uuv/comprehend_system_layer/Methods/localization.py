# localization

from saruca_uuv.control_system_layer.Methods.assignment import assignment
from saruca_uuv.control_system_layer.Methods.assignment import EntityLayer

vehicleLocation = assignment()


def localization():
    if EntityLayer.getPositionVector() == vehicleLocation:
        return 1
    else:
        return 0
