'''
Created on Aug 19, 2012

@author: cgrubb
'''
import json
import zmq
from zmq.eventloop import zmqstream, ioloop
ioloop.install()

from functions.display import gen_display
from functions.map import gen_map
from functions.call import plot_call

fxn_map = {"map":gen_map,
           "plot_call":plot_call,
           "display":gen_display
           }

class Generator():
    '''
    Generate javascript objects on demand
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.context = zmq.Context()
        self.pull = self.context.socket(zmq.PULL)
        self.pull.bind("tcp://*:8890")
        self.pub = self.context.socket(zmq.PUB)
        self.pub.bind("tcp://*:8891")
        self.loop = ioloop.IOLoop.instance()
        self.stream = zmqstream.ZMQStream(self.pull)
        self.stream.on_recv(self.handle_msg)
        
    def handle_msg(self, message):
        '''
        Generate the requested javascript object and publish it
        '''
        try:
            msg = json.loads(message[0])
        except ValueError:
            return
        try:
            type = msg['type']
        except KeyError:
            return
        try:
            key = str(msg['key'])
        except KeyError:
            return
        try:
            gen_fxn = fxn_map[type]
            output = str(gen_fxn(**msg))
            self.pub.send_multipart([key,output])
        except KeyError:
            return
        
def main():
    gen = Generator()
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()