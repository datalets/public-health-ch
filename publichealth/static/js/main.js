$(document).ready(function() {

	// All external links in a new window
	$('a[href^="http"]').filter(function() {
		return this.hostname && this.hostname !== location.hostname;
	}).attr('target', '_blank');

	// Initialise front page carousel component
	$('.carousel-inner.slick').slick({
		autoplay: true,
		autoplaySpeed: '10000',
		dots: true,
		infinite: true,
		speed: 1000,
		fade: true,
		cssEase: 'linear',
		prevArrow: '<span class="arrow left glyphicon glyphicon-chevron-left" aria-hidden="true">Previous</span>',
		nextArrow: '<span class="arrow right glyphicon glyphicon-chevron-right" aria-hidden="true">Next</span>',
	});

	// Pastel colors on live news
	// $('.feedpage-body .panel').each(function() {
	// 	var hue = Math.floor(Math.random() * 360);
	// 	var pastel = 'hsl(' + hue + ', 100%, 87.5%)';
	// 	$(this).css('border-top', '3px solid ' + pastel);
	// });

});
