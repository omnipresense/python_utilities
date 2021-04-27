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

## Alternatives

If this does not meet your needs, then perhaps the built in pyserial terminal will.  See [the documentation](https://pyserial.readthedocs.io/en/latest/tools.html). 
```
python -m serial.tools.miniterm
```


Alternatively, take a look at other community resources like:   
https://github.com/dhylands/usb-ser-mon/tree/master/usb_ser_mon

Of course, C-based programs are also useful.  
For linux, screen and minicom have proven themselves useful.  
On Windows, [TeraTerm](https://osdn.net/projects/ttssh2/releases/) is great for interaction and [yat](https://sourceforge.net/projects/y-a-terminal/) is great for simplifying testing.


