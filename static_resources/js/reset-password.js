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
	$(function() {
	    $.ajaxSetup({
		error: function(jqXHR, exception) {
		    if (jqXHR.status === 0) {
		    } else if (jqXHR.status == 404) {
		        alert('Requested page not found. [404]');
		    } else if (jqXHR.status == 500) {
		        alert('Internal Server Error [500].');
		    } else if (exception === 'parsererror') {
		        alert('Requested JSON parse failed.');
		    } else if (exception === 'timeout') {
		        alert('Time out error.');
		    } else if (exception === 'abort') {
		        alert('Ajax request aborted.');
		    }
		}
	    });
	});	
	ajaxResetPassword();
});