#!/usr/bin/env python3
from optparse import OptionParser
from time import time

import serial
import serial.tools.list_ports
from serial.serialutil import SerialException

import sys
import select
from platform import system
if system() == "Linux":
    import tty
    import termios
elif system() == "Windows":
    from msvcrt import kbhit, getche # or getch() for echo-less getch

def key_available():
    if system() == "Linux":
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
    elif system() == "Windows":
        return kbhit()


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port_name",
                      help="read data from PORTNAME")
    parser.add_option("-b", "--baud", dest="baudrate",
                      default="57600",
                      help="baud rate on serial port")
    parser.add_option("-t", "--timeToLive",
                      default=0,
                      dest="time_to_live")
    parser.add_option("-i", "--interval_time",
                      default=0,
                      dest="interval_time")
    parser.add_option("-s", "--interval_send",
                      default="",
                      dest="interval_send")
    (options, args) = parser.parse_args()
    time_to_live_val = float(options.time_to_live)
    interval_time_val = float(options.interval_time)
    interval_send = options.interval_send
    last_interval_time = time() # don't send interval str at boot, wait at least...


    baudrate_int = int(options.baudrate)
    if baudrate_int <= 0:
        baudrate_int = 57600
    serial_port = serial.Serial(
        timeout=0.1,
        writeTimeout=0.2,
        baudrate=baudrate_int
    )
    port_value = "";
    if options.port_name is None or len(options.port_name) < 1:
        if len(serial.tools.list_ports.comports()):
            serial_port.port = serial.tools.list_ports.comports()[0].device
        elif system() == "Linux":
            serial_port.port = "/dev/ttyACM0"  # good for linux
        else:
            serial_port.port = "COM4"  # maybe we'll luck out on windows
    else:
        serial_port.port = options.port_name
    serial_port.open()

    if not serial_port.is_open:
        print("Exiting.  Could not open serial port:", serial_port.port)
        sys.exit(1)

    if system() == "Linux":
        # suppress echo on terminal.
        old_tty_settings = termios.tcgetattr(sys.stdin)
        old_port_attr = termios.tcgetattr(serial_port.fileno())
        new_port_attr = termios.tcgetattr(serial_port.fileno())
        new_port_attr[3] = new_port_attr[3] & ~termios.ECHO
        termios.tcdrain(serial_port.fileno())
        termios.tcsetattr(serial_port.fileno(), termios.TCSADRAIN, new_port_attr)
    start_time = time()

    try:
        if system() == "Linux":
            tty.setcbreak(sys.stdin.fileno())

        serial_port.flushInput()
        serial_port.flushOutput()
        while serial_port.is_open:
            data_rx_bytes = serial_port.readline()
            data_rx_length = len(data_rx_bytes)
            if data_rx_length != 0:
                data_rx_str = str.rstrip(str(data_rx_bytes.decode('utf-8', 'strict')))
                print(data_rx_str)
            while key_available():
                if system() == "Linux":
                    c = sys.stdin.read(1)
                    serial_port.write(c.encode('utf-8'))
                    sys.stdout.write(c)
                elif system() == "Windows":
                    c = getche()   # change to getch() to remove echo
                    serial_port.write(c)
            if time_to_live_val > 0:
                if (time() - start_time) > time_to_live_val:
                    print("Exiting.  Time to live elapsed")
                    sys.exit(0)
            if interval_time_val > 0:
                if (time() - last_interval_time) > interval_time_val:
                    serial_port.write(interval_send.encode('utf-8'))
                    last_interval_time = time()

    except SerialException:
        print("Serial Port closed. terminate.")
    except KeyboardInterrupt:
        print("Break received,  Serial Port closing.")
    finally:
        if system() == "Linux":
            # reinstate original condition (reinstate echo if it was there)
            termios.tcsetattr(serial_port.fileno(), termios.TCSADRAIN, old_port_attr)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty_settings)


if __name__ == "__main__":
    main()
