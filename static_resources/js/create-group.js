var count = 0;

function isEmail(email) {
	var regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return regex.test(email);
}

function createGroup() {
	var $modal = $('#create-group');
	var param = {};
	
	$('#create-group .loading-spinner').show();
	
	$modal.find('.people-list').hide("blind", function() {
		if (count > 0) {
			var $input;
			var email;
			
			for (var i = 1; i <= count; i++) {
				$input = $('input[name="email' + i + '"]');
				email = $.trim($input.val());
				
				if (email == "" || !isEmail(email)) {
					continue;
				}
				
				param['email' + i] = email;
			}
			// clean up so nothing gets submitted by the form
			count = 0;
			$('.people-list-header').hide();
			$('.add-invitee-btn').siblings('.people-list').html("");
		}
	});
	
	param["name"] = $('#create-group input[name="name"]').val();
	param["csrfmiddlewaretoken"] = $('#create-group input[type="hidden"]').val();
	
	$.post(
		"/create/",
		param,
		function(output) {
			if (output.location) {
				window.location.replace(output.location);
			} else {
				$modal.fadeOut(function() {
					$modal.html($(output).html());
					count = $modal.find('input[type="text"]').length - 1;
					$modal.find('ul.errorlist').addClass("alert alert-error")
					ajaxCreateGroup();
					if($.browser.msie && parseInt($.browser.version, 10) < 10) {
						$modal.find('input, textarea').placeholder();
					}
				});
				$modal.fadeIn();
				$('#create-group .loading-spinner').hide();
			}
		}
	);
}

function addNewPersonField() {
	count++;
	var fieldHtml = "<input type=\"text\" name=\"email" + count + "\" placeholder=\"Email Address " + count + "\" />";
	var validityHtml = "<span class=\"validity\"><span class=\"valid-email hide\"><i class=\"icon-ok\"></i> Valid email address</span><span class=\"invalid-email hide\"><i class=\"icon-remove\"></i> Please enter a valid email address</span></span>";
	var containerHtml = "<div class=\"person-email hide\"></div>";
	
	var $container = $(containerHtml);
	var $input = $(fieldHtml);
	var $validity = $(validityHtml);
	
	$container.append($input);
	$container.append($validity);
	
	if($.browser.msie && parseInt($.browser.version, 10) < 10) {
		$input.placeholder();
	}
	
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
	$container.show("blind");
}

function ajaxCreateGroup() {
	$('#create-group-form').submit(function(event) {
		event.preventDefault();
		createGroup();
	});
	
	$('#create-group').on("hide", function() {
		$('#create-group-form input[type="text"]').val("");
		$('#create-group-form .errorlist').remove();
		count = 0;
		$('#create-group-form .people-list-header').hide();
		$('.add-invitee-btn').siblings('.people-list').html("");
	});
	
	$('#create-group .add-invitee-btn').click(function() {
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
