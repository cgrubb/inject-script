'''
Created on Aug 18, 2012

@author: cgrubb
'''
import os
import uuid
import tornado.ioloop
import tornado.web

from settings_socket import SettingSocket, SettingListener


_count = 0

class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        '''
        Build the skeleton
        Include the jquery and settings references
        '''
        self.write("""<html>
            <head>
                <title>Test Index</title>
                <link rel='stylesheet' href='static/lib/theme/default/style.css' />
                <link rel='stylesheet' href='static/lib/css/ui-lightness/jquery-ui-1.8.23.custom.css' />
                <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.css" />
                <script src="http://cdn.leafletjs.com/leaflet-0.7.3/leaflet.js"></script>
                <script type="text/javascript" src="https://www.google.com/jsapi"></script>
                <script type='text/javascript' src='static/lib/OpenLayers.js'></script>
                <script type='text/javascript' src='static/lib/jquery-1.8.0-min.js'></script>
                <script type='text/javascript' src='static/lib/js/jquery-ui-1.8.23.custom.min.js'></script>
                <script type='text/javascript' src='static/scripts/model.js'></script>
                <script type='text/javascript' src='static/scripts/view.js'></script>
                <script type='text/javascript' src='static/scripts/controller.js'></script>
                <script type='text/javascript' src='init.js'></script>
                <script type='text/javascript'>
                    google.load('earth','1.x');
                </script>
            </head>
            <body>
                <div id="main" style="height:100%;width:100%"></div>
            </body>
        </html>""")

class InitScriptHandler(tornado.web.RequestHandler):

    def get(self):
        '''
        Initialize the page and open the settings socket.
        The settings socket is used to inject other javascript
        to build up the page
        '''
        #TODO: Use global counter for testing
        #Eventually this will be replaced with a hash for each user
        socket_url = 'ws://{}/settings'.format(self.request.host)

        backup = "ws://192.168.10.104:8888/settings"
        sockets = "['{}']".format(socket_url)
        global _count
        _count += 1
        self.write("""
                    var index = {};
                    $(document).ready(function() {
                        index.model = new $.Model(%s,'%s');
                        index.view = new $.View();
                        index.controller = new $.Controller(index.model,index.view);
                        document.title = 'Client %s';
                    });
                   """ % (sockets,_count, _count))

if __name__ == "__main__":
    settings = {"static_path":os.path.join(os.path.dirname(__file__),"static")}
    app = tornado.web.Application([(r"/",IndexHandler),
                                   (r"/init.js",InitScriptHandler),
                                   (r"/settings",SettingSocket)],
                                   [dict(path=settings['static_path'])],
                                  **settings)
    app.listen(8888)
    listener = SettingListener()
    tornado.ioloop.IOLoop.instance().start()