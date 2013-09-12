jQuery.extend({
	Controller: function (model, view) {		
		var controller  = this;
		
		//Set up a model listener
		var mlistener = $.ModelListener({
			update: function(message) {
				view.exec(message);
			}
		});
		model.addListener(mlistener);
	},
});