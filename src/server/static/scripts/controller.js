jQuery.extend({
	Controller: function (model, view) {
		//Set up a model listener
		var mlistener = $.ModelListener({
			update: function(message) {
				eval(message);
			}
		});
		model.addListener(mlistener);
	},
});