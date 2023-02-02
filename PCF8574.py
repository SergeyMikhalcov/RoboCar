from typing import Any, Iterable, List
import smbus 

class IOPort:
    """
    Represents the PCF8574 IO port as a list of boolean values.
    """
    def __init__(self, pcf8574) -> None:
        self.pcf8574 = pcf8574

    def __setitem__(self, key: int, value: int) -> None:
        """
        Set an individual output pin.
        """
        self.pcf8574.set_output(key, value)

    def __getitem__(self, key: int) -> None:
        """
        Get an individual pin state.
        """
        return self.pcf8574.get_pin_state(key)

    def __repr__(self) -> str:
        """
        Represent port as a list of booleans.
        """
        state = self.pcf8574.bus.read_byte(self.pcf8574.address)
        ret = []
        for i in range(8):
            ret.append(bool(state & 1 << 7 - i))
        return repr(ret)

    def __len__(self) -> int:
        return 8

    def __iter__(self) -> Iterable[bool]:
        for i in range(8):
            yield self[i]

    def __reversed__(self) -> Iterable[bool]:
        for i in range(8):
            yield self[7 - i]

class PCF8574:
    """
    A software representation of a single PCF8574 IO expander chip.
    """

    def __init__(self, i2c_bus_no: int, address: int) -> None: 
        self.bus_no = i2c_bus_no
        self.bus = smbus.SMBus(i2c_bus_no)
        self.address = address

    def __repr__(self) -> str:
        return "PCF8574(i2c_bus_no=%r, address=0x%02x)" % (self.bus_no, self.address)

    @property
    def port(self) -> IOPort:
        """
        Represent IO port as a list of boolean values.
        """
        return IOPort(self)

    @port.setter
    def port(self, value: List[bool]) -> None:
        """
        Set the whole port using a list.
        """
        assert len(value) == 8
        new_state = 0
        for i, val in enumerate(value):
            if val:
                new_state |= 1 << 7 - i
        self.bus.write_byte(self.address, new_state)

    def set_output(self, output_number: int, value: bool) -> None:
        """
        Set a specific output high (True) or low (False).
        """
        assert output_number in range(
            8
        ), "Output number must be an integer between 0 and 7"
        current_state = self.bus.read_byte(self.address)
        bit = 1 << 7 - output_number
        new_state = current_state | bit if value else current_state & (~bit & 0xFF)
        self.bus.write_byte(self.address, new_state)

    def get_pin_state(self, pin_number: int) -> bool:
        """
        Get the boolean state of an individual pin.
        """
        assert pin_number in range(8), "Pin number must be an integer between 0 and 7"
        state = self.bus.read_byte(self.address)
        return bool(state & 1 << 7 - pin_number)


