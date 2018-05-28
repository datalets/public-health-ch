$(document).ready(function() {

	// All external links in a new window
	$('a[href^="http"]').filter(function() {
		return this.hostname && this.hostname !== location.hostname;
	}).attr('target', '_blank');

	if ($('#carousel-banner').length) {
		// Initialise front page carousel component
		$('.carousel-inner').slick({
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

	} else if ($('.carousel-gallery').length) {
		// Load gallery component
		$('.carousel-gallery').slick({
			slidesToShow: 1,
			slidesToScroll: 1,
			arrows: false,
			fade: true,
			asNavFor: '.slider-nav'
		}).slickLightbox({
		  src: 'data-src',
		  itemSelector: 'img',
    	caption: 'caption',
			captionPosition: 'bottom'
		});
	}

	// Slider navigation
	$('.slider-nav').slick({
		slidesToShow: 3,
		slidesToScroll: 1,
		infinite: false,
		centerMode: true,
		focusOnSelect: true,
		asNavFor: '.carousel-gallery',
		// Responsive settings
		responsive: [
		{
			breakpoint: 768,
			settings: {
				arrows: false,
				centerMode: true,
				centerPadding: '30px',
				slidesToShow: 3
			}
		},
		{
			breakpoint: 480,
			settings: {
				arrows: false,
				centerMode: true,
				centerPadding: '30px',
				slidesToShow: 1
			}
		}
	],
		prevArrow: '<span class="arrow left glyphicon glyphicon-chevron-left" aria-hidden="true">Previous</span>',
		nextArrow: '<span class="arrow right glyphicon glyphicon-chevron-right" aria-hidden="true">Next</span>',
	});

	// Cookie notice via insites.com
	var langbase = $('.language-nav a.active').text().toLowerCase();
	window.cookieconsent.initialise({
	  "palette": {
	    "popup": {
	      "background": "#edeff5",
	      "text": "#838391"
	    },
	    "button": {
	      "background": "#4b81e8"
	    }
	  },
	  "theme": "edgeless",
	  "content": {
	    "message": langbase == 'fr' ?
			  "Ce site Web utilise des cookies pour vous permettre une utilisation optimale de notre site Web."
				: "Diese Website verwendet Cookies, um Ihnen eine optimale Nutzung unserer Website zu ermöglichen.",
	    "dismiss": langbase == 'fr' ?
				"D'accord"
				: "Zustimmen",
	    "link": langbase == 'fr' ?
				"Pour plus d'informations"
				: "Weitere informationen",
	    "href": "/" + langbase + "/privacy/"
	  }
	});

	// Pastel colors on live news
	// $('.feedpage-body .panel').each(function() {
	// 	var hue = Math.floor(Math.random() * 360);
	// 	var pastel = 'hsl(' + hue + ', 100%, 87.5%)';
	// 	$(this).css('border-top', '3px solid ' + pastel);
	// });

});
