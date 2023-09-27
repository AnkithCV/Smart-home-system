from datetime import datetime
from abc import ABC, abstractmethod

# Define the Device class using Factory Method pattern
class DeviceFactory(ABC):
    @abstractmethod
    def create_device(self, device_id):
        pass

class LightFactory(DeviceFactory):
    def create_device(self, device_id):
        return Light(device_id)

class ThermostatFactory(DeviceFactory):
    def create_device(self, device_id):
        return Thermostat(device_id)

class DoorLockFactory(DeviceFactory):
    def create_device(self, device_id):
        return DoorLock(device_id)

# Define the Device class
class Device(ABC):
    def __init__(self, device_id):
        self.device_id = device_id

    def turn_on(self):
        pass

    def turn_off(self):
        pass

# Implement concrete Device classes
class Light(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.status = 'off'

    def turn_on(self):
        self.status = 'on'

    def turn_off(self):
        self.status = 'off'

class Thermostat(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.temperature = 70

    def set_temperature(self, temperature):
        self.temperature = temperature

class DoorLock(Device):
    def __init__(self, device_id):
        super().__init__(device_id)
        self.status = 'locked'

    def unlock(self):
        self.status = 'unlocked'

    def lock(self):
        self.status = 'locked'

# Define the SmartHomeSystem class
class SmartHomeSystem:
    def __init__(self):
        self.devices = {}
        self.scheduled_tasks = []
        self.automated_triggers = []

    def add_device(self, device_id, device_type):
        if device_id not in self.devices:
            factory = None
            if device_type == 'light':
                factory = LightFactory()
            elif device_type == 'thermostat':
                factory = ThermostatFactory()
            elif device_type == 'door':
                factory = DoorLockFactory()

            if factory:
                self.devices[device_id] = factory.create_device(device_id)

    def turn_on(self, device_id):
        if device_id in self.devices:
            self.devices[device_id].turn_on()

    def turn_off(self, device_id):
        if device_id in self.devices:
            self.devices[device_id].turn_off()

    def set_schedule(self, device_id, time, command):
        self.scheduled_tasks.append({'device': device_id, 'time': time, 'command': command})

    def add_trigger(self, condition, action):
        self.automated_triggers.append({'condition': condition, 'action': action})

    def execute_scheduled_tasks(self):
        current_time = datetime.now().strftime("%H:%M")
        for task in self.scheduled_tasks:
            if task['time'] == current_time:
                exec(task['command'])

# Example usage
if __name__ == "__main__":
    home_system = SmartHomeSystem()
    home_system.add_device(1, 'light')
    home_system.add_device(2, 'thermostat')
    home_system.add_device(3, 'door')

    home_system.turn_on(1)
    home_system.set_schedule(2, "06:00", "turn_on(1)")

    home_system.add_trigger("temperature > 75", "turn_off(1)")

    home_system.execute_scheduled_tasks()

    status_report = '"Light {} is {}. Thermostat is set to {} degrees. Door is {}."'.format(
        list(home_system.devices.keys())[0],
        list(home_system.devices.values())[0].status,
        list(home_system.devices.values())[1].temperature,
        list(home_system.devices.values())[2].status
    )

    scheduled_tasks = '[{}]'.format(', '.join(str(task) for task in home_system.scheduled_tasks))

    automated_triggers = '[{}]'.format(', '.join(str(trigger) for trigger in home_system.automated_triggers))

    print("Status Report: {}".format(status_report))
    print("Scheduled Tasks: {}".format(scheduled_tasks))
    print("Automated Triggers: {}".format(automated_triggers))
