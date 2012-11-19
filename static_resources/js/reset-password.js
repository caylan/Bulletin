function resetPassword() {
	var $containerInPage = $('#content-container');
	$.post(
		".",
		$('#reset-password-form').serialize(),
		function(output) {
			var $nextPage = $('#content-container', output);
			var $newState = $('h4', output);
			var $state = $('h4');
			$state.fadeOut(function() {
				$state.html($newState.html());
			});
			
			$containerInPage.fadeOut(function() {
				$containerInPage.html($nextPage.html());
				ajaxResetPassword();
				if($.browser.msie && parseInt($.browser.version, 10) < 10) {
					$('input, textarea').placeholder();
				}
			});
			$state.fadeIn();
			$containerInPage.fadeIn();
		}
	);
}

function ajaxResetPassword() {
	$('#reset-password-form').submit(function(event) {
		event.preventDefault();
		resetPassword();
	});
}

$(document).ready(function() {
	ajaxResetPassword();
});