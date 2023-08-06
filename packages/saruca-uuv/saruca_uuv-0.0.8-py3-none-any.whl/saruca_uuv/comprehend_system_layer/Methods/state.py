# state

from ..Classes.VehicleComprehendLayer import VehicleComprehendLayer

speed = 0
accel = 0.0
directory = ""
angle = 0.0
poolSize = [(25, 50, 2), (12.5, 25, 2)]


def state():
    vehicleState = VehicleComprehendLayer(speed, accel, directory, angle, poolSize)
    if vehicleState.getPoolSize() == [(25, 50, 2), (25, 50, 2)]:
        if vehicleState.getSpeed() > 15 and vehicleState.getAccel() > 2.0:
            return "highAccel"
        else:
            return "normalAccel"
    else:
        return "normalAccel"
