'''
Created on Sep 2, 2012
@author: cgrubb
'''

def gen_display(*args, **kwargs):
    return """
        $("#display").remove();        
        $("#main").append($('<div id="display" />').attr('class', 'ui-widget-content'));
        $("#display").resizable();
        $("#display").css({
            'position':'absolute',
            'top':'10%',
            'left':'0px',
            'width':'30%',
            'height':'90%',
            'background-color':'lightgray'
});      
    """