function register() {
	var containerInPage = $('#content-container');
	$('.loading-spinner').show();
	$.post(
		".",
		$('.form-signin').serialize(),
		function(output) {
			var nextPage = $("#content-container", output);
			containerInPage.fadeOut(function() {
				containerInPage.html(nextPage.html());
				containerInPage.find('ul.errorlist').addClass("alert alert-error")
				ajaxRegister();
				if($.browser.msie && parseInt($.browser.version, 10) < 10) {
					$('input, textarea').placeholder();
				}
			});
			containerInPage.fadeIn();
		}
	);
}

function ajaxRegister() {
	var registerBtn = $('.register-btn');
	registerBtn.click(function(event) {
		event.preventDefault();
		$(this).attr("disabled", "disabled");
		register();
	});
}

$(document).ready(function() {
	ajaxRegister();
});