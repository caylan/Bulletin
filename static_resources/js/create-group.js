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
	var createGroupBtn = $('#create-group-btn');
	createGroupBtn.click(function(event) {
		event.preventDefault();
		$(this).attr("disabled", "disabled");
		createGroup();
	});
}

$(document).ready(function() {
	ajaxCreateGroup();
});