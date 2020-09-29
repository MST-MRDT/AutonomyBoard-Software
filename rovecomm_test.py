from core.rovecomm import RoveCommPacket
from core.rovecomm import RoveCommEthernetTcp
import core
import rovecomm_test
import time
import threading
import struct
import socket

rovecomm_test.variable = 0


def main() -> None:
    core.rovecomm_node.callbacks[4242] = addCounter
    packet = RoveCommPacket(4242, 'b', (1, 3), "", 11000)
    packet.SetIp('127.0.0.1')
    core.rovecomm_node.write(packet)

    RoveCommTCP = RoveCommEthernetTcp(HOST='127.0.0.1', PORT=11111)
    RoveCommTCP.callbacks[4242] = addCounter
    packet2 = RoveCommPacket(4242, 'b', (1, 3), "", 11111)
    packet2.SetIp('127.0.0.1')
    RoveCommTCP.write(packet2)

    # Test socket to try to send to RoveComm
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 11111))
    rovecomm_packet = struct.pack(">BHBB", 2, 4242, 2, 0)
    for i in (1, 3):
        rovecomm_packet = rovecomm_packet + struct.pack('>b', i)

    print(threading.enumerate())
    for i in range(5):
        s.send(rovecomm_packet)
        time.sleep(.5)
        print(rovecomm_test.variable)
    print("Closing Thread")
    print(threading.enumerate())
    core.rovecomm.collection.close_thread()
    print(threading.enumerate())


def addCounter(packet):
    rovecomm_test.variable += 1
