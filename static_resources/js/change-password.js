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
	ajaxChangePassword();
});
