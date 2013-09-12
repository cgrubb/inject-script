jQuery.extend({
	View: function() {
		var that = this;
		var listeners = new Array();
		
		this.exec = function(code) {
			eval(code);
		}
		
		this.addListener = function(listener) {
			listeners.push(listener);
		}
	},
	

	ViewListener: function(listener) {
		if (!listener) listener = {};
		$.extend({
			display: function(obj) {}
		},listener);
	}

});