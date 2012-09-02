'''
Created on Aug 19, 2012

@author: cgrubb
'''
import json
import zmq
from zmq.eventloop import zmqstream, ioloop
ioloop.install()

def gen_display(*args, **kwargs):
    return """
        $("#display").remove();        
        $("#main").append($('<div id="display" />').attr('class', 'ui-widget-content'));
        $("#display").resizable();
        $("#display").css({
            'margin-right':'60px',
            'width':'30%',
            'height':'100%',
            'background-color':'green'
});      
    """

#Eventually this gets more sophisticated, lookup layers, controls, etc from database
def gen_map(*args, **kwargs):
    return """        
        $("#main").empty();
        $("#main").append($('<div id="map" />'));
        $("#map").css({
            'float':'right',
            'height':'100%',
            'width':'70%'
        });
        $("#map").resizable();
        index.map = {};
        index.map.olmap = new OpenLayers.Map({
            div: "map",
            resolutions: [0.087890625, 0.0439453125, 0.02197265625, 0.010986328125],
            controls: [
                new OpenLayers.Control.Navigation(
                    {dragPanOptions: {enableKinetic: true}}
                )
            ]
        });
        index.map.olmap.addLayer(new OpenLayers.Layer.TileCache("TileCache Layer",
            ["http://c0.tilecache.osgeo.org/wms-c/cache/",
             "http://c1.tilecache.osgeo.org/wms-c/cache/",
             "http://c2.tilecache.osgeo.org/wms-c/cache/",
             "http://c3.tilecache.osgeo.org/wms-c/cache/",
             "http://c4.tilecache.osgeo.org/wms-c/cache/"],
            "basic",
            {
                serverResolutions: [0.703125, 0.3515625, 0.17578125, 0.087890625,
                                    0.0439453125, 0.02197265625, 0.010986328125,
                                    0.0054931640625, 0.00274658203125, 0.001373291015625,
                                    0.0006866455078125, 0.00034332275390625, 0.000171661376953125,
                                    0.0000858306884765625, 0.00004291534423828125, 0.000021457672119140625],
                buffer: 4
            }
        ));        
        index.map.olmap.setCenter(new OpenLayers.LonLat(0, 0), 0);
        index.map.getMap = function() {
            return index.map.olmap;
        }
        index.map.markers = new OpenLayers.Layer.Markers("Markers");
        index.map.olmap.addLayer(index.map.markers);
        index.map.marker_popup = new OpenLayers.Popup();
        index.map.olmap.addPopup(index.map.marker_popup);
    """

def plot_call(*args,**kwargs):
    x = kwargs['x']
    y = kwargs['y']
    return """
        $("#display").text("call");
        if (index.map !== null) {  
            var olmap = index.map.getMap();
            olmap.removeLayer(index.map.markers);
            var lonlat = new OpenLayers.LonLat(%s,%s);
            olmap.panTo(lonlat);
            index.map.markers = new OpenLayers.Layer.Markers("Markers");
            olmap.addLayer(index.map.markers);
            var size = new OpenLayers.Size(21,25);
            var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
            var icon = new OpenLayers.Icon('http://www.openlayers.org/dev/img/marker.png',size,offset);
            index.map.markers.addMarker(new OpenLayers.Marker(lonlat,icon));
            olmap.removePopup(index.map.marker_popup);
            index.map.marker_popup = new OpenLayers.Popup.FramedCloud("call",
                lonlat,
                null,
                "call",
                null,
                true);
            olmap.addPopup(index.map.marker_popup);
        } 
    """%(x,y)

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