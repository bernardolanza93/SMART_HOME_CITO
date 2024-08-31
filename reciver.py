#!/usr/bin/env python

from __future__ import division

import numpy as np
import socket
import struct
from datetime import datetime
import cv2
import time


MAX_DGRAM = 2 ** 16


def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break


def listen_for_TCP_string(string_from_tcp_ID):
    time.sleep(10)
    #port = 1025
    #ip = '127.0.0.1'
    port = 21001
    ip = '192.168.1.91' #mettere localhost per togliere errore '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((ip, port))
    print("reciving config: IP = {}, PORT = {}. ".format(ip, port))


    while True:

        seg, addr = s.recvfrom(MAX_DGRAM)  # here was the error lo da sempre e non legge mai la stringa inviata sara
        # perche deve stare in ascolto costante per poter beccare l esatto momento in cui arriva il pacchetto ,
        # unica proposta crea un nuovo processo parallelo che continua ad ascoltare e quando c e un  nuovo messaggio aggiorna il value di multiprocessing comune


        seg = seg.decode('utf-8')
        seg = str(seg)
        
        string_from_tcp_ID = seg
        
        
        
        print("FROM TCP SEGB:",seg)

        
    s.close()


def main():
    """ Getting image udp frame &
    concate before decode and output image """
    print("receiver listening")

    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Raddr = '127.0.0.1'
    #Rport = 5005
    Raddr = '192.168.1.91'
    Rport = 5005
    s.bind((Raddr, Rport))
    print("receiving config: IP = {}, PORT = {}. ".format(Raddr, Rport))
    dat = b''
    dump_buffer(s)

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            cv2.imwrite('plot_rec.png', img)
            print("recived and saved")

            # cv2.imshow('frame', img)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break
            dat = b''

    # cap.release()
    cv2.destroyAllWindows()
    s.close()


if __name__ == "__main__":
    main()
