#-*- coding:utf-8 -*-

import time
import serial

from comm.eliochannel import eliochannel
from comm.elioprotocol import ElioProtocol
from comm.packet_t import packet_t

if __name__ == "__main__":

    PORT = '/dev/tty.usbmodem5BE1AEDDA4E82'
    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    with eliochannel(ser, ElioProtocol, packet_t) as p:
        while p.isDone():
            p.sendMotor();
            time.sleep(3)

