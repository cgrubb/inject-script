'''
Created on Aug 18, 2012

@author: cgrubb
'''
import json
import zmq
from zmq.eventloop import zmqstream, ioloop
ioloop.install()
from tornado import websocket

sockets = []
socket_dict = {}
reverse_lookup = {}
context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:8889")

class SettingSocket(websocket.WebSocketHandler):
    
    def open(self):
        print "Socket open"
        sockets.append(self)
    
    def on_close(self):
        print "Socket closed"
        sockets.remove(self)
        key = reverse_lookup[self]
        del(socket_dict[key])
        del(reverse_lookup[self])
        
    def on_message(self, message):
        print message
        msg = json.loads(message)
        if msg["event"] == "open":
            socket_dict[msg['key']] = self
            reverse_lookup[self] = msg['key']
            pub_socket.send(json.dumps(msg))
            
class SettingListener():
    
    def __init__(self):
        self.context = zmq.Context().instance()
        self.listener = self.context.socket(zmq.SUB)
        self.listener.setsockopt(zmq.SUBSCRIBE,'')
        self.listener.connect("tcp://localhost:8891")
        self.stream = zmqstream.ZMQStream(self.listener)
        self.stream.on_recv(self.handle_msg)
        
    def handle_msg(self, message):
        key = message[0]
        output = unicode(message[1])
        try:
            outsock = socket_dict[key]
            outsock.write_message(output)
        except KeyError:
            print "Socket not found: {}".format(key)
        
        