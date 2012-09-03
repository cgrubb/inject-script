jQuery.extend({
	Model: function(url, key) {
		var that = this;
		var listeners = new Array();
		this.addListener = function(listener) {
			listeners.push(listener);
		};
		
		//open up a web socket and start listening
		this.socket = new WebSocket(url);
		//unique key for socket messages
		this.key = key;
		
		this.notifyUpdate = function(message) {
			$.each(listeners, function(i) {
				listeners[i].update(message);
			});
		};	
		
		this.socket.onopen = function() {
			this.send(JSON.stringify({"event":"open","key":that.key}));
		};
		this.socket.onmessage = function(message) {
			that.notifyUpdate(message.data)
		};
	},
	
	ModelListener: function(listener) {
		if (!listener) listener = {};
		return $.extend({
			update: function(message) {}
		}, listener);
	}
	
});