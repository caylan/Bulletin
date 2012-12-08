function changePassword() {
	var $form = $('#change-password-form');
  var $modal = $('#change-password');

	$.post(
		"/change_password/",
		$form.serialize(),
		function(output) {
			if (output.location) {
        window.location.replace(output.location);
			} else {
        // We've run into some sort of error.
        $modal.fadeOut(function() {
          $modal.html($(output).html());
          $modal.find('ul.errorlist').addClass("alert alert-error")
          ajaxChangePassword();
          if($.browser.msie && parseInt($.browser.version, 10) < 10) {
            $modal.find('input, textarea').placeholder();
          }
        });
        $modal.fadeIn();
			}
		} 
  );
}


function ajaxChangePassword() {
	$('#change-password-form').submit(function(event) {
		event.preventDefault();
		changePassword();
	});

	$('#change-password').on("hide", function() {
		$('#change-password-form input[type="password"]').val("");
        $('#change-password .alert-error').remove();
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
	ajaxChangePassword();
});
