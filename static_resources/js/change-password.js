function changePassword() {
	var $form = $('#change-password-form');

	$.post(
		"/change_password/",
		$form.serialize(),
		function(data) {
			if (!data.success) {
        // TODO: Change the form so that it shows whether something was wrong
        // with the form.  A good idea might be to render a form such that we
        // have proper error messages when the field isn't set properly.
			} else {
        // We've successfully changed the password and can now hide the modal.
				$('#change-password').modal("hide");
			}
		}, "json");
}


function ajaxChangePassword() {
	$('#change-password-form').submit(function(event) {
		event.preventDefault();
		changePassword();
	});

	$('#change-password').on("hide", function() {
		$('#change-password-form input[type="password"]').val("");
	});
}

$(document).ready(function() {
	ajaxChangePassword();
});
