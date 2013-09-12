jQuery.extend({
	Model: function(url, key) {
		this.key = key;		
		var that = this;
		var listeners = new Array();		
		this.addListener = function(listener) {
			listeners.push(listener);
		};
		
		this.notifyUpdate = function(message) {
			$.each(listeners, function(i) {
				listeners[i].update(message);
			});
		};
		
		
		this.socket = new WebSocket(url[0]);
		this.socket.onopen = function() {
			this.send(JSON.stringify({"event":"open","key":that.key}));
		};
		this.socket.onclose = function() {
			alert(this);
		}
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