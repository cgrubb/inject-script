'''
Created on Sep 15, 2012

@author: cgrubb
'''

def gen_earth(*args, **kwargs):
    return """

        $("#main").empty();
        $("#main").append($('<div id="ge" />'));
        index.earth = {};
        google.earth.createInstance('ge', function(instance) {
            var ge = instance;
            ge.getWindow().setVisibility(true);
            ge.getNavigationControl().setVisibility(ge.VISIBILITY_AUTO);
            var options = ge.getOptions();
            options.setStatusBarVisibility(true);
            options.setScaleLegendVisibility(true);
            options.setOverviewMapVisibility(true);
            index.earth.instance = ge;
        },
        function(errorCode) {
            alert(errorCode);
        });
    """

def plot_earth(*args, **kwargs):
    x = kwargs["x"]
    y = kwargs["y"]
    return """
    if (index.earth !== null) {
        var lookat =
            index.earth.instance.getView().copyAsLookAt(
                index.earth.instance.ALTITUDE_RELATIVE_TO_GROUND);
        lookat.setTilt(30);
        lookat.setLatitude(%s);
        lookat.setLongitude(%s);
        lookat.setHeading(0);
        lookat.setAltitude(0);
        lookat.setRange(1500);
        index.earth.instance.getView().setAbstractView(lookat);
    }
    """%(y,x)