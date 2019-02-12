The python program "serial_util.py" acts as a bi-directional conduit between 
a terminal (linux shell or windows Command Prompt) 
and a USB CDC device (such as an OmniPreSense OPS24x radar)

On Linux, it will work to turn off the echo feature that comes with devices that are attached to Linux hosts.
(The OPS24x doesn't want its transmissions echoed back to itself!)  Since windows was deveoped 
without the thought of having serial terminals attached, that feature is unneeded for windows. 

The usage is:
```
Usage: serial_util.py [options] arg

Options:
  -h, --help            show this help message and exit
  -p PORT_NAME, --port=PORT_NAME
                        read data from PORTNAME
  -b BAUDRATE, --baud=BAUDRATE
                        baud rate on serial port
  -t TIME_TO_LIVE, --timeToLive=TIME_TO_LIVE
```  
* The recent checkin allows of auto-detect of available ports on both Linux and Windows, so use of the --port option is optional.
* Time to live is useful for emptying out a host's USB buffer before starting a more useful program.
* Baudrate tends to be completely optional--USB manages that.

Requirements:
Python 3, pyserial.   ("pip install pyserial") 

