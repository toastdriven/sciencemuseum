jQuery(window).load(function() {
	var $ = jQuery;
	if (!$('.polaroid img').length) {
		return;
	}
	// Add magnify icon to trigger zoomable view
	var icon = $(
		'<img src="/static/img/icons/magnifier_zoom_in.png" alt="Zoom" />'
	);
	icon.click(makeZoomable).css('cursor', 'pointer');
	var div = $('div.polaroid')
	div.css('position', 'relative');
	icon.css({
		'position': 'absolute',
		'top': div.find('img').height() - 25,
		'left': div.find('img').width() - 25,
		'border': 'none'
	}).appendTo(div).attr('title', 'Show close-up view');
	
	function makeZoomable() {
		var img = $('div.polaroid img:first');
		var big_src = img.attr('src').replace('size=Small', 'size=Large');
		img.css('opacity', 0.4);
		var wrapper = $('<div class="img-wrapper"></div>');
		wrapper.css({
			display: 'block',
			position: 'relative',
			marginBottom: '20px'
		}).width(img.width()).height(img.height());
		img.wrap(wrapper);
		var loading = $(
			'<img src="/static/img/icons/loading-bar.gif" alt="Loading" />'
		);
		loading.css({
			position: 'absolute',
			top: img.height() / 2,
			left: '50%',
			border: 'none',
			padding: 0,
			marginLeft: '-110px'
		});
		$('.img-wrapper').append(loading);
		icon.unbind('click');
		// Load the big image
		var big = new Image();
		big.src = big_src;
		$(big).load(function() {
			var big_width = big.width;
			var big_height = big.height;
			var r = big_height / img.width();
			loading.remove();
			var container = $('<div></div>');
			container.width(img.width());
			container.height(img.height());
			container.css({
				'background-image': 'url(' + big_src + ')',
				'background-repeat': 'no-repeat',
				'background-position': '0 0'
			});
			img.hide();
			container.appendTo($('.img-wrapper'));
			var pos = container.offset();
			container.mousemove(function(ev) {
				var x = ev.pageX - pos.left;
				var y = ev.pageY - pos.top;
				container.css(
					'background-position', -(r * x) + 'px ' + -(r * y) + 'px'
				);
			});
			
			// Now get the minus button to work
			icon.attr(
				'src', '/static/img/icons/magnifier_zoom_out.png'
			).attr('title', 'Zoom out');
			var zoomed = true;
			icon.click(function() {
				if (zoomed) {
					icon.attr(
						'src', '/static/img/icons/magnifier_zoom_in.png'
					).attr('title', 'Zoom in');
					container.hide();
					img.css('opacity', 1).show();
					zoomed = false;
				} else {
					icon.attr(
						'src', '/static/img/icons/magnifier_zoom_out.png'
					).attr('title', 'Zoom out');
					container.show();
					img.hide();
					zoomed = true;
				}
			});
			
		});
	}
});

jQuery(function($) {
	var div = $('.map-goes-here');
	if (div.length) {
		div.width(704).height(300).css('clear', 'both');
		var map = new GMap2(div[0]);
		map.setCenter(new GLatLng(43.8, -37.3), 1);
		var geocoder = new GClientGeocoder();
		var bounds = new GLatLngBounds();
		/* Now pull in the places */
		$('ul.places span.place-name').each(function() {
			var span = $(this);
			var location = span.text().replace(', World', '');
			geocoder.getLatLng(location, function(point) {
				var marker = new GMarker(point);
				map.addOverlay(marker);
				GEvent.addListener(marker, "click", function() {
					marker.openInfoWindowHtml(
						span.parent().html().replace(' - ', '<br>')
					);
				});
				bounds.extend(point);
				map.setCenter(
					bounds.getCenter(), Math.min(
						6, (map.getBoundsZoomLevel(bounds) - 1)
					)
				);
			});
		});
		div.wrap('<div class="map-container"></div>');
	}
});