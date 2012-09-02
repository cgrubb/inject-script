'''
Created on Sep 2, 2012

@author: cgrubb
'''
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