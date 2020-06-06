# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Sparkfun Alphanumeric 4-char I2C Displays
=================
"""

from time import sleep
import qwiic_i2c

# Lookup table of segments for Sparkfun Qwiic HT16K33
SEGMENT_TABLE = (
    # nmlkjihgfedcba
    0b00000000000000, #' ' (space)
    0b00001000001000, #'!'
    0b00001000000010, #'"'
    0b1001101001110,  #'#'
    0b1001101101101,  #'$'
    0b10010000100100, #'%'
    0b110011011001,   #'&'
    0b1000000000,     #'''
    0b111001,         #'('
    0b1111,           #')'
    0b11111010000000, #'*'
    0b1001101000000,  #'+'
    0b10000000000000, #','
    0b101000000,	  #'-'
    0b00000000000000, #'.'
    0b10010000000000, #'/'
    0b111111,         #'0'
    0b10000000110,	  #'1'
    0b101011011,	  #'2'
    0b101001111,	  #'3'
    0b101100110,	  #'4'
    0b101101101,	  #'5'
    0b101111101,	  #'6'
    0b1010000000001,  #'7'
    0b101111111,	  #'8'
    0b101100111,	  #'9'
    0b00000000000000, #':'
    0b10001000000000, #';'
    0b110000000000,   #'<'
    0b101001000,	  #'='
    0b01000010000000, #'>'
    0b01000100000011, #'?'
    0b00001100111011, #'@'
    0b101110111,	  #'A'
    0b1001100001111,  #'B'
    0b111001,         #'C'
    0b1001000001111,  #'D'
    0b101111001,	  #'E'
    0b101110001,	  #'F'
    0b100111101,	  #'G'
    0b101110110,	  #'H'
    0b1001000001001,  #'I'
    0b11110,          #'J'
    0b110001110000,   #'K'
    0b111000,         #'L'
    0b10010110110,	  #'M'
    0b100010110110,   #'N'
    0b111111,         #'O'
    0b101110011,	  #'P'
    0b100000111111,   #'Q'
    0b100101110011,   #'R'
    0b110001101,	  #'S'
    0b1001000000001,  #'T'
    0b111110,         #'U'
    0b10010000110000, #'V'
    0b10100000110110, #'W'
    0b10110010000000, #'X'
    0b1010010000000,  #'Y'
    0b10010000001001, #'Z'
    0b111001,         #'['
    0b100010000000,   #'\'
    0b1111,           #']'
    0b10100000000000, #'^'
    0b1000,			  #'_'
    0b10000000,		  #'`'
    0b101011111,	  #'a'
    0b100001111000,   #'b'
    0b101011000,	  #'c'
    0b10000100001110, #'d'
    0b1111001,        #'e'
    0b1110001,        #'f'
    0b110001111,	  #'g'
    0b101110100,	  #'h'
    0b1000000000000,  #'i'
    0b1110,           #'j'
    0b1111000000000,  #'k'
    0b1001000000000,  #'l'
    0b1000101010100,  #'m'
    0b100001010000,   #'n'
    0b101011100,	  #'o'
    0b10001110001,	  #'p'
    0b100101100011,   #'q'
    0b1010000,        #'r'
    0b110001101,	  #'s'
    0b1111000,        #'t'
    0b11100,          #'u'
    0b10000000010000, #'v'
    0b10100000010100, #'w'
    0b10110010000000, #'x'
    0b1100001110,	  #'y'
    0b10010000001001, #'z'
    0b10000011001001, #'{'
    0b1001000000000,  #'|'
    0b110100001001,   #'}'
    0b00000101010010, #'~'
    0b11111111111111, #Unknown character (DEL or RUBOUT)
)

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class instance.
# This allows higher level logic to rapidly create a index of qwiic devices at
# runtine
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic Alphanumeric"

# Some devices have multiple availabel addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
_AVAILABLE_I2C_ADDRESS = [0x70, 0x71, 0x72, 0x73]

# Device commands
_HT16K33_BLINK_CMD = 0x80
_HT16K33_BLINK_DISPLAYON = 0x01
_HT16K33_CMD_BRIGHTNESS = 0xE0
_HT16K33_OSCILATOR_ON = 0x21

# Memory addresses of display extras
_COLON_ADDRESS = 0x01
_DOT_ADDRESS = 0x03

class QwiicAlphanumeric(object):
    """Alpha-numeric, 14-segment display.

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The QwiicAlphanumeric device object.
        :rtype: Object
    """
    # Constructor
    device_name = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Constructor
    def __init__(self, address=None, i2c_driver=None):

        # Did the user specify an I2C address?
        self._address = address if address is not None else self.available_addresses[0]

        # load the I2C driver if one isn't provided

        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        self._buffer = bytearray(16)
        self._content = [None] * 4
        self._auto_write = True
        self._blink_rate = 0
        self._brightness = 1.0

    # ----------------------------------
    # isConnected()
    #
    # Is an actual board connected to our system?
    def is_connected(self):
        """
            Determine if a device is conntected to the system..

            :return: True if the device is connected, otherwise False.
            :rtype: bool

        """
        return qwiic_i2c.isDeviceConnected(self._address)

    connected = property(is_connected)

    def begin(self):
        """
            Initialize the operation of the Alphanumeric module

            :return: Returns true of the initialization was successful, otherwise False.
            :rtype: bool

        """
        self._write_cmd(_HT16K33_OSCILATOR_ON)
        self.clear()
        self.blink_rate = 0
        self.brightness = 1.0
        return True



    # ----------------------------------
    # Board commands
    # ----------------------------------
    def _write_cmd(self, byte):
        with self._i2c:
            self._i2c.writeCommand(self._address, byte)

    @property
    def blink_rate(self):
        """The blink rate. Range 0-3."""
        return self._blink_rate

    @blink_rate.setter
    def blink_rate(self, rate=None):
        if not 0 <= rate <= 3:
            raise ValueError("Blink rate must be an integer in the range: 0-3")
        rate = rate & 0x03
        self._blink_rate = rate
        self._write_cmd(_HT16K33_BLINK_CMD | _HT16K33_BLINK_DISPLAYON | rate << 1)

    @property
    def brightness(self):
        """The brightness. Range 0.0-1.0"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if not 0.0 <= brightness <= 1.0:
            raise ValueError(
                "Brightness must be a decimal number in the range: 0.0-1.0"
            )

        self._brightness = brightness
        xbright = round(15 * brightness)
        xbright = xbright & 0x0F
        self._write_cmd(_HT16K33_CMD_BRIGHTNESS | xbright)

    @property
    def auto_write(self):
        """Auto write updates to the display."""
        return self._auto_write

    @auto_write.setter
    def auto_write(self, auto_write):
        if isinstance(auto_write, bool):
            self._auto_write = auto_write
        else:
            raise ValueError("Must set to either True or False.")

    def show(self):
        """Refresh the display and show the changes."""
        with self._i2c:
            # Send display RAM.
            self._i2c.writeBlock(self._address, 0, self._buffer)

    def clear(self):
        for i in range(4):
            self._content[i] = ' '
        for i in range(16):
            self._buffer[i] = 0
        if self._auto_write:
            self.show()

    def print(self, value):
        """Print the value to the display."""
        self.clear()
        if isinstance(value, (str)):
            self._text(value)
        elif isinstance(value, (int, float)):
            self._number(value)
        else:
            raise ValueError("Unsupported display value type: {}".format(type(value)))
        if self._auto_write:
            self.show()

    def print_hex(self, value):
        """Print the value as a hexidecimal string to the display."""
        if isinstance(value, int):
            self.print("{0:X}".format(value))
        else:
            self.print(value)

    def __setitem__(self, key, value):
        self._put(value, key)
        if self._auto_write:
            self.show()

    def scroll(self, count=1):
        """Scroll the display by specified number of places."""
        if count < 0:
            count = abs(count)
            for x in range(4 - count, count - 1, -1):
                self._content[x] = self._content[x - count]
            for x in range(count):
                if x + count > 4:
                    break
                self._content[x] = ' '
        else:
           for x in range(4):
                if x + count > 3:
                   break
                self._content[x] = self._content[x + count]

           for x in range(count):
                if 3 - x < 0:
                    break
                self._content[3 - x] = ' '
        for x in range(4):
            self._putbits(SEGMENT_TABLE[ord(self._content[x]) - 32], x)

    def _erase_char(self, digit):
        for seg in range(14):
            addr, mask = self._getaddr(seg, digit)
            self._buffer[addr] &= ~mask

    def _put1seg(self, segment, digit):
        addr, mask = self._getaddr(segment, digit)
        self._buffer[addr] |= mask

    def _getaddr(self, segment, digit):
        if segment > 8:
            com = segment - 7
        elif segment == 8:    # I
            com = 0
        elif segment == 7:  # H
            com = 1
        else:
            com = segment

        row = digit
        if (segment > 6):   # G
            row += 4

        adr = com << 1
        if (row > 7):
            adr += 1
        dat = 1 << row
        return adr, dat

    def _putbits(self, bitmask, digit):
        self._erase_char(digit)
        for i in range(14):
            if bitmask >> i & 0b1:
                self._put1seg(i, digit)

    def _put(self, char, index=0):
        """Put a character at the specified place."""
        if not 0 <= index <= 3:
            return
        if not 32 <= ord(char) <= 127:
            return
        if char == ".":
            self.dpydot = True
            return
        if char == ":":
            self.colon = True
            return
        self._content[index] = char
        character = ord(char) - 32
        self._putbits(SEGMENT_TABLE[character], index)

    def _push(self, char):
        """Scroll the display and add a character at the end."""
        if (char != ".") & (char != ":"):
            self.scroll()
        self._put(char, 3)

    def _text(self, text):
        """Display the specified text."""
        for character in text:
            self._push(character)

    def _number(self, number):
        """
		Display a floating point or integer number

		Param: number - The floating point or integer number to be displayed, which must be
			in the range 0 (zero) to 9999 for integers and floating point or integer numbers
			and between 0.0 and 999.0 or 99.00 or 9.000 for floating point numbers.
		Param: decimal - The number of decimal places for a floating point number if decimal
			is greater than zero, or the input number is an integer if decimal is zero.

        Returns: The output text string to be displayed.
        """

        auto_write = self._auto_write
        self._auto_write = False
        stnum = str(number)
        dot = stnum.find(".")

        if (len(stnum) > 5) or ((len(stnum) > 4) and (dot < 0)):
            raise ValueError(
                "Input overflow - {0} is too large for the display!".format(number)
            )

        if dot < 0:
            # No decimal point (Integer)
            places = len(stnum)
        else:
            places = len(stnum[:dot])

        if places <= 0 < 1:
            self.clear()
            places = 4

            if "." in stnum:
                places += 1

        # Set decimal places, if number of decimal places is specified (decimal > 0)
        if places > 0 < 1 < len(stnum[places:]) and dot > 0:
            txt = stnum[: dot + 2]
        elif places > 0:
            txt = stnum[:places]

        if len(txt) > 5:
            raise ValueError("Output string ('{0}') is too long!".format(txt))

        self._text(txt)
        self._auto_write = auto_write

        return txt

    def set_digit_raw(self, index, bitmask):
        """Set digit at position to raw bitmask value. Position should be a value
        of 0 to 3 with 0 being the left most character on the display.

        bitmask should be 2 bytes such as: 0xFFFF
        If can be passed as an integer, list, or tuple
        """
        if not isinstance(index, int) or not 0 <= index <= 3:
            raise ValueError("Index value must be an integer in the range: 0-3")

        if isinstance(bitmask, (tuple, list)):
            bitmask = ((bitmask[0] & 0xFF) << 8) | (bitmask[1] & 0xFF)

        # Use only the valid potion of bitmask
        bitmask &= 0xFFFF

        # Set the digit bitmask value at the appropriate position.
        self._content[index] = ' '
        self._putbits(bitmask, index)
        if self._auto_write:
            self.show()

    @property
    def colon(self):
        return bool(self._buffer[_COLON_ADDRESS] & 0b01)

    @colon.setter
    def colon(self, turn_on):
        if turn_on:
            self._buffer[_COLON_ADDRESS] |= 0b01
        else:
            self._buffer[_COLON_ADDRESS] &= ~0b01
    @property
    def dpydot(self):
        return bool(self._buffer[_DOT_ADDRESS] & 0b01)

    @dpydot.setter
    def dpydot(self, turn_on):
        if turn_on:
            self._buffer[_DOT_ADDRESS] |= 0b01
        else:
            self._buffer[_DOT_ADDRESS] &= ~0b01
