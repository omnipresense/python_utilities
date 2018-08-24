#!/usr/bin/env python3
import serial
from serial.serialutil import SerialException

#
# magic code to read key-at-a-time
import sys 
import select 
import tty 
import termios
def key_available():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
old_settings = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())


#
# code to open the port as a serial interface
serial_port = serial.Serial(
    timeout=0.1,
    writeTimeout=2,
    port="/dev/ttyACM0"
)

if serial_port.is_open:
    serial_port.flushInput()
    serial_port.flushOutput()

#
# loop forever.  only allow the serial port the "timeout" value to respond
# after dealing with result from the serial port
# if there's a character, read it, print it, send it.
#
try:
    while serial_port.is_open:
        data_rx_bytes = serial_port.readline()
        data_rx_length = len(data_rx_bytes)
        if data_rx_length != 0:
            data_rx_str = str.rstrip(str(data_rx_bytes.decode('utf-8', 'strict')))
            print (data_rx_str)
        while key_available():
            c = sys.stdin.read(1)
            serial_port.write(c.encode('utf-8'))
            sys.stdout.write(c)
except SerialException:
    print("Serial Port closed. terminate.")
finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)