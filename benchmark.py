import timeit

class Device:
    def __init__(self, name):
        self.name = name

device = Device("Some Other Device Name")

def orig_callback():
    if "Redmi" in str(device.name) or "Buds" in str(device.name):
        pass

def new_callback():
    name = str(device.name)
    if "Redmi" in name or "Buds" in name:
        pass

print("Orig:", timeit.timeit(orig_callback, number=10000000))
print("New: ", timeit.timeit(new_callback, number=10000000))
