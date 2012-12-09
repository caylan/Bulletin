function register() {
	var $containerInPage = $('#register-form-container');
    $('#register-form-container .loading-spinner').removeClass("hide");
	$.post(
		$('#register-form').attr('action'),
		$('#register-form').serialize(),
		function(output) {
			var $nextPage = $('#register-form-container', output);
            if ($nextPage.length == 0) {
                $nextPage = $('#content-container', output)
            } else if (typeof landing != "undefined" && landing) {
                $nextPage.find('.back-btn').remove();
                $nextPage.find('.form-signin-heading').remove();
            }
			$containerInPage.fadeOut(function() {
				$containerInPage.html($nextPage.html());
				$containerInPage.find('ul.errorlist').addClass("alert alert-error");
				ajaxRegister();
				if($.browser.msie && parseInt($.browser.version, 10) < 10) {
					$('input, textarea').placeholder();
				}
			});
			$containerInPage.fadeIn();
		}
	);
}

function ajaxRegister() {
	$('#register-form').submit(function(event) {
		event.preventDefault();
		register();
	});
}

$(document).ready(function() {
	//$(function() {
	//    $.ajaxSetup({
	//	error: function(jqXHR, exception) {
	//	    if (jqXHR.status === 0) {
	//	    } else if (jqXHR.status == 404) {
	//	        alert('Requested page not found. [404]');
	//	    } else if (jqXHR.status == 500) {
	//	        alert('Internal Server Error [500].');
	//	    } else if (exception === 'parsererror') {
	//	        alert('Requested JSON parse failed.');
	//	    } else if (exception === 'timeout') {
	//	        alert('Time out error.');
	//	    } else if (exception === 'abort') {
	//	        alert('Ajax request aborted.');
	//	    }
	//	}
	//    });
	//});	
    ajaxRegister();
});