'''
Created on May 23, 2014

@author: cgrubb
'''
def gen_leaflet(*args, **kwargs):
    return """
    $("#main").empty();
    $("#main").append($('<div id="map" />'));
    $("#map").css({
        'height': '100%'
    });
    var map = L.map('map').setView([40, -105], 13);
    L.tileLayer('http://{s}.tiles.mapbox.com/v3/examples.map-i86knfo3/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18}).addTo(map);
    index.map = map;
"""

def gen_leaflet_marker(*args, **kwargs):
    x = kwargs['x']
    y = kwargs['y']
    return """
        if (index.map !== null) {
            L.marker([%s, %s]).addTo(index.map);
        }"""%(y, x)