jQuery(function($) {
	//	Add the class "hasJS" to the body element.
	$('body').addClass('hasJS');
	console.log('here');
});

jQuery(window).load(function() {
	// Crazyweird fix lets us style abbr using CSS in IE 
	document.createElement('abbr');
});