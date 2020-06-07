#-*- coding:utf-8 -*-
import binascii

from comm.protocol import Protocol

UDP = 0x30;
CMD_EXECUTE = 0x01;

class ElioProtocol(Protocol):
    packet = None

    def __init__(self):
        pass

    # 연결 시작시 발생
    def connection_made(self, transport):
        self.transport = transport
        self.running = True


    # 연결 종료시 발생
    def connection_lost(self, exc):
        self.transport = None

    #데이터가 들어오면 이곳에서 처리함.
    def data_received(self, data, len):
        #입력된 데이터와 키맵을 비교해서 있다면
        cmd = data[0];
        udp = data[1];

        self.DC1 = data[2];
        self.DC2 = data[3];

        self.SV1 = data[4];
        self.SV2 = data[5];

        self.V3 = data[6];
        self.V5 = data[7];

        self.IO1 = data[8];
        self.IO2 = data[9];
        self.IO3 = data[10];
        self.IO4 = data[11];

        self.SONIC = (data[12] | data[13] << 8)
        self.LINE1 = (data[14] | data[15] << 8) == 0 if 1 else 0;
        self.LINE2 = (data[16] | data[17] << 8) == 0 if 1 else 0;


    # 데이터 보낼 때 함수
    def write(self,data, len):
        print(binascii.hexlify(data))
        self.transport.packet.send_packet(data, len)

    def write_packet(self, data):
        # print(data)
        self.transport.write(data)

    # 종료 체크
    def isDone(self):
        return self.running

    def initializeData(self):
        pass
        # init = bytearray([0x20, 0x50, 0x00, 0x00, 0x00])
        # p.write(init)

    def sendIO(self, which_io, value):
        print ('sendIO')
        buffer = [-128 for i in range(10)]
        if (which_io == "3V"):
            buffer[4] = value
        elif (which_io == "5V"):
            buffer[5] = value
        elif (which_io == "IO1"):
            buffer[6] = value
        elif (which_io == "IO2"):
            buffer[7] = value
        elif (which_io == "IO3"):
            buffer[8] = value
        elif (which_io == "IO4"):
            buffer[9] = value
        self.send_command('M', buffer, 10);

    def sendDC(self, dc1, dc2):
        print ('sendDC')
        buffer = [-128 for i in range(10)]
        buffer[0] = dc1;
        buffer[1] = dc2;

        self.send_command('M', buffer, 10);

    def sendServo(self, sv1, sv2):
        print ('sendServo')
        buffer = [-128 for i in range(10)]
        buffer[2] = sv1;
        buffer[3] = sv2;
        self.send_command('M', buffer, 10)

    def sendMotor(self):
        buffer = bytearray(15)
        buffer[0] = UDP;
        buffer[1] = CMD_EXECUTE;

        buffer[2] = 0;
        buffer[3] = 100;
        buffer[4] = 3;
        buffer[5] = 4;
        buffer[6] = 5;
        buffer[7] = 6;
        buffer[8] = 7;
        buffer[9] = 8;
        buffer[10] = 9;
        buffer[11] = 10;

        buffer[12] = 0;
        buffer[13] = 0;
        buffer[14] = 0;
        self.write(buffer, 15)

    def sendTXRX(self):
        buffer = bytearray(4)
        buffer[0] = UDP;
        buffer[1] = 0xf5;
        buffer[2] = 1;
        buffer[3] = 'a';
        self.write(buffer, 4)