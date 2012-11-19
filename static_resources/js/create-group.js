var count = 0;

function isEmail(email) {
	var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return regex.test(email);
}

function createGroup() {
	var $modal = $('#create-group');
	var emailArray = [];
	
	if (count > 0) {
		var $input;
		var email;
		
		for (var i = 0; i < count; i++) {
			$input = $('input[name="email' + i + '"]');
			email = $.trim($input.val());
			
			if (email == "" || !isEmail(email)) {
				continue;
			}
			
			emailArray.push(email);
		}
		// clean up so nothing gets submitted by the form
		count = 0;
		$('.people-list-header').hide();
		$('.add-invitee-btn').siblings('.people-list').html("");
	}
	
	$.post(
		"/create/",
		$('#create-group-form').serialize(),
		function(output) {
			if (output.location) {
				window.location.replace(output.location);
			} else {
				$modal.fadeOut(function() {
					count = 0;
					$modal.html($(output).html());
					$modal.find('ul.errorlist').addClass("alert alert-error")
					ajaxCreateGroup();
					if($.browser.msie && parseInt($.browser.version, 10) < 10) {
						$modal.find('input, textarea').placeholder();
					}
				});
				$modal.fadeIn();
			}
		}
	);
}

function addNewPersonField() {
	var fieldHtml = "<input type=\"text\" name=\"email" + count + "\" placeholder=\"Email Address " + count + "\" style=\"display: none;\" />";
	var validityHtml = "<span class=\"validity\"><span class=\"valid-email hide\">Valid email address</span><span class=\"invalid-email hide\">Please enter a valid email address</span></span>";
	var containerHtml = "<div class=\"person-email\"></div>";
	
	var $container = $(containerHtml);
	var $input = $(fieldHtml);
	var $validity = $(validityHtml);
	
	$container.append($input);
	$container.append($validity);
	
	$input.keyup(function() {
		if (isEmail($input.val())) {
			$validity.children('.valid-email').show();
			$validity.children('.invalid-email').hide();
		} else {
			$validity.children('.valid-email').hide();
			$validity.children('.invalid-email').show();
		}
	});
	
	var $peopleList = $('.add-invitee-btn').siblings('.people-list');
	$peopleList.append($container);
	$input.show("blind");
	count++;
}

function ajaxCreateGroup() {
	$('#create-group-form').submit(function(event) {
		event.preventDefault();
		createGroup();
	});
	
	$('#create-group-form a.btn.dismiss, #create-group-form .close').click(function() {
		$('#create-group-form input[type="text"]').val("");
		$('#create-group-form .errorlist').remove();
		count = 0;
		$('.people-list-header').hide();
		$('.add-invitee-btn').siblings('.people-list').html("");
	});
	
	$('.add-invitee-btn').click(function() {
        if (count == 0) {
            $('.people-list-header').show("blind", function () {
            	addNewPersonField();
            });
        } else {
        	addNewPersonField();
        }
        
    });
}

$(document).ready(function() {
	ajaxCreateGroup();
});