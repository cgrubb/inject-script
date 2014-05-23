'''
Created on Sep 2, 2012

@author: cgrubb
'''
def gen_toolbar(*args, **kwargs):
    return """
        $("#toolbar").remove();
        $("#main").append($('<div id="toolbar" />'));
        $("#toolbar").css({
            'position':'absolute',
            'top':'0',
            'left':'0',
            'height':'10%',
            'width':'100%',
            'background-color':'#0E0E0E'});
    """
    
def gen_button(*args, **kwargs):
    try:
        text = kwargs['text']
    except KeyError:
        text = "Click me!"
    try:
        click = kwargs["click"]
    except KeyError:
        click = "function() { alert('you rang?'); }"
    return """
        $("#btnTest").remove();
        if ($("#toolbar") !== null) {
            $("#toolbar").append($('<input type="button" id="btnTest" />'));
            $("#btnTest").attr("value","%s");
            $("#btnTest").button();
            $("#btnTest").click( %s );
        }
    """ % (text, click)