function changePassword() {
	var $form = $('#change-password-form');

	$.post(
		"/change_password/",
		$form.serialize(),
		function(data) {
			if (!data.success) {
				alert(data.error);
			} else {
				alert("Password changed");
				$('#change-password-form .close').click();
			}
		}, "json");
}


function ajaxChangePassword() {
	$('#change-password-form').submit(function(event) {
		event.preventDefault();
		changePassword();
	});
	
	$('#change-password-form a.btn, #change-password-form .close').click(function() {
		$('#change-password-form input[type="password"]').val("");
	});
}

$(document).ready(function() {
	ajaxChangePassword();
});