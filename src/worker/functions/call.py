'''
Created on Sep 2, 2012

@author: cgrubb
'''
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
