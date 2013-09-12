This is an experiment generating Javascript on the server, pushing to a browser via web socket, and then executing the Javascript in the browser.

Obviously this raises some interesting potential security questions, so do this at your own risk.

The JQuery MVC scripts are based on examples found here:

http://welcome.totheinter.net/tutorials/model-view-controller-in-jquery/phase-1

The basic idea was to create a basic framework for handling messages, and then build up the application dynamically using messages from the server.
In theory, this allows for live code updates with no need to reload any pages.

There are three parts to the system:
1. A web socket server.
2. A Javascript generator
3. A driver for initiating Javascript updates.

The web socket server is implemented in server/settings_socket.py.  The socket server listens for web socket connections and registers clients.  Currently client keys are assigned as sequential numbers.

The Javascript generator is worker/js_generator.py.  The generator listens for messages that direct the component to be generated and the client key to send the updated component to.

