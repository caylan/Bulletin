// email invite count in the existing group
var countInvite = 0;

// adds a new input and the live email validation
function addNewPerson() {
	countInvite++;
	
	var fieldHtml = "<input type=\"text\" name=\"email" + countInvite + "\" placeholder=\"Email Address " + countInvite + "\" />";
	var validityHtml = "<span class=\"validity\"><span class=\"valid-email hide\"><i class=\"icon-ok\"></i> Valid email address</span><span class=\"invalid-email hide\"><i class=\"icon-remove\"></i> Please enter a valid email address</span></span>";
	var containerHtml = "<div class=\"person-email hide\"></div>";
	
	var $container = $(containerHtml);
	var $input = $(fieldHtml);
	var $validity = $(validityHtml);
	
	if (countInvite != 1) {
		$container.addClass("extra");
	}
	
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
	
	var $peopleList = $('#invite-people .add-invitee-btn').siblings('.people-list');
	$peopleList.append($container);
	$container.show("blind");
}

// where the submit is happening for inviting people
function invitePeople() {
	var $modal = $('#invite-people');
  var $form = $('#invite-people-form');
	var $input;
	var email;
	
	$('#invite-people .loading-spinner').show();
	
  // Trim all of the emails.
	for (var i = 1; i <= countInvite; i++) {
		$input = $('#invite-people input[name="email' + i + '"]');
		email = $.trim($input.val());
	}

  // The callback function.
  var callback_ = function(output) {
    if (output.success) {
      // close the modal
      $modal.modal('hide');
    } else {
      // TODO: show some sort of error message.
    }
    $('#invite-people .loading-spinner').hide();
  }
	
  // Fire the AJAX post.
	$.post("./send_invites/", $form.serialize(), callback_);
}

// to be called to initialize ajax submission
function ajaxInvitePeople() {
	$('#invite-people-form').submit(function(event) {
		event.preventDefault();
		invitePeople();
	});

	// what to do when the modal is hidden
	$('#invite-people').on("hide", function() {
		$(this).find('.extra').remove();
		countInvite = 1;
	});

	// what the "add a person" button does
	$('#invite-people .add-invitee-btn').click(function() {
    addNewPerson();
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
	ajaxInvitePeople();
	addNewPerson();
});
