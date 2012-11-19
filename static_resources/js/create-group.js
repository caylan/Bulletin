function createGroup() {
	var $modal = $('#create-group');
	$.post(
		"/create/",
		$('#create-group-form').serialize(),
		function(output) {
			if (output.location) {
				window.location.replace(output.location);
			} else {
				$modal.fadeOut(function() {
					$modal.html($(output).html());
					$modal.find('ul.errorlist').addClass("alert alert-error")
					ajaxCreateGroup();
					if($.browser.msie && parseInt($.browser.version, 10) < 10) {
						$('input, textarea').placeholder();
					}
				});
				$modal.fadeIn();
			}
		}
	);
}

function ajaxCreateGroup() {
	$('#create-group-form').submit(function(event) {
		event.preventDefault();
		createGroup();
	});
	
	$('#create-group-form a.btn, #create-group-form .close').click(function() {
		$('#create-group-form input[type="text"]').val("");
		$('#create-group-form .errorlist').remove();
	});
}

$(document).ready(function() {
	ajaxCreateGroup();
});