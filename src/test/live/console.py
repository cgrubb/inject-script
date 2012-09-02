'''
Created on Aug 19, 2012

@author: cgrubb
'''
import time
import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:8890")

#for i in range(100):
#    socket.send("test_{0}".format(i))
#    print "sending..."
#    time.sleep(1)

msg = ''
while msg != 'exit':
    try:
        msg = raw_input("> ")
        socket.send(msg)
    except EOFError:
        break

socket.close()
context.term()