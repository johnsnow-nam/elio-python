#-*- coding:utf-8 -*-

import time
import serial

from comm.eliochannel import eliochannel
from comm.elioprotocol import ElioProtocol
from comm.packet_t import packet_t

if __name__ == "__main__":

    PORT = '/dev/tty.usbmodemE124B4CB8D5A2'
    ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    with eliochannel(ser, ElioProtocol, packet_t) as p:

        p.decideToUseSensor(1, 0, 0)
        while p.isDone():
            p.sendDC(90, 0)
            time.sleep(1)
            p.sendDC(0, 0)
            time.sleep(1)

            p.sendServo(50, 0)
            time.sleep(1)
            p.sendServo(0, 0)
            time.sleep(1)

            p.sendIO("IO4", 100)
            time.sleep(1)
            # p.sendIO("IO4", 0)
            time.sleep(1)

