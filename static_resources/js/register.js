function register() {
	var containerInPage = $('#content-container');
	var csrfMiddlewareToken = $('input[type=hidden]').val();
	var firstName = $('#id_first_name').val();
	var lastName = $('#id_last_name').val();
	var email = $('#id_email').val();
	var password1 = $('#id_password1').val();
	var password2 = $('#id_password2').val();
	
	$.ajax({
		type: "POST",
		url: ".",
		data: {
			csrfmiddlewaretoken: csrfMiddlewareToken,
			first_name: firstName,
			last_name: lastName,
			email: email,
			password1: password1,
			password2: password2
		}
	}).done(
			function(output) {
				var nextPage = $($("#content-container", output)[0]);
				containerInPage.fadeOut(function() {
					containerInPage.html(nextPage.html());
					containerInPage.find('ul.errorlist').addClass("alert alert-error")
					ajaxRegister();
				});
				containerInPage.fadeIn();
			});
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