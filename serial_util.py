#!/usr/bin/env python3
from optparse import OptionParser
from time import time

import serial
from serial.serialutil import SerialException

import sys 
import select 
import tty 
import termios
def key_available():
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port_name",
                      default="/dev/ttyACM0",
                      help="read data from PORTNAME")
    parser.add_option("-t", "--timeToLive",
                       default=0,
                       dest="time_to_live")
    (options, args) = parser.parse_args()
    time_to_live_val = float(options.time_to_live)

    serial_port = serial.Serial(
        timeout=0.1,
        writeTimeout=0.2,
        port=options.port_name
    )
    if not serial_port.is_open:
        print("Exiting.  Could not open serial port:",serial_port.port)
        sys.exit(1)

    old_tty_settings = termios.tcgetattr(sys.stdin)
    old_port_attr = termios.tcgetattr(serial_port.fileno())
    new_port_attr = termios.tcgetattr(serial_port.fileno())
    new_port_attr[3] = new_port_attr[3] & ~termios.ECHO 
    termios.tcdrain(serial_port.fileno())
    termios.tcsetattr(serial_port.fileno(), termios.TCSADRAIN, new_port_attr)
    start_time = time()

    try:
        tty.setcbreak(sys.stdin.fileno())

        serial_port.flushInput()
        serial_port.flushOutput()
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
            if time_to_live_val > 0:
                if (time() - start_time) > time_to_live_val:
                    print("Exiting.  Time to live elapsed")
                    sys.exit(0)

    except SerialException:
        print("Serial Port closed. terminate.")
    except KeyboardInterrupt:
        print("Break received,  Serial Port closing.")
    finally:
        termios.tcsetattr(serial_port.fileno(), termios.TCSADRAIN, old_port_attr)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty_settings)

if __name__ == "__main__":
    main()
