/* Automatically makes an ajax call to 'update/' view
 * times out after 25s
 * after timeout or sucess, recursively calls itself again
 *
 * based on example from
 * http://techoctave.com/c7/posts/60-simple-long-polling-example-with-javascript-and-jquery
 */

// Pulls a list of notifications from the server and then inserts them into the inbox
function update() {
    $.ajax({url: "update/", success: function(data) { // Ajax retrieval
		$(data).find('li').each(function() { // For each notification in the list
			$data = $(this);
			if ($data.hasClass("notification")) {
				// returned data is a proper notification.
				var $newNotif = $data
				var $noNotif = $('.alert.alert-warning');
				$newNotif.hide();
				$newNotif.find(".avatar").show();
				$newNotif.find(".timeago").timeago().show();
	
				// Remove the "no updates" notification.
				removeNoUpdateWarning($noNotif);
				$("#notifications").prepend($newNotif);
				$newNotif.fadeIn();
				animateResize($newPost.find(".avatar"), $($newNotif).height());
			}
		});
    }, dataType: "html", complete: update, timeout: 25000});
}

function removeNoUpdateWarning($noNotif) {
    if ($noNotif.length != 0) {
        $noNotif.parent().append($("<ul id='notifications' class='media-list'></ul>"));
        $noNotif.slideUp(function() {
            $noNotif.remove();
        });
    }
}

function initDynamicAvatarSize() {
	$('.notification').each(function() { 
        var notifHeight = $(this).height();
        
        $(this).children('.avatar-container').each(function() { // Avatars within posts
            $(this).find('.avatar').each(function() {
                resizeAvatar(this, notifHeight);
            });
        });
        
        //$(this).find('.comment').each(function() { // Avatars within comments
        //    var commentHeight = $(this).height();
        //    $(this).find('.avatar').each(function() {
        //        resizeAvatar(this, commentHeight);
        //    });
        //});
    });
}

function resizeAvatar (avatar, parentHeight) {	
	$("<img/>")
		.attr("src", $(avatar).attr("src"))
		.load(function() {
			var scale = this.width/this.height;
			var computedHeight = Math.max(Math.min(this.height, parentHeight), 60);
			$(avatar).css('height',  computedHeight + 'px');
			$(avatar).css('min-width',  computedHeight*scale + 'px');
			$(avatar).css('margin-left',  -(computedHeight*scale - 60 )/3 + 'px');
			$(avatar).fadeIn();
    });
}

function animateResize (avatar, parentHeight) {	
	$("<img/>")
		.attr("src", $(avatar).attr("src"))
		.load(function() {
			var scale = this.width/this.height;
			var computedHeight = Math.max(Math.min(this.height, parentHeight), 60);
			$(avatar).animate({"margin-left": -(computedHeight*scale - 60 )/3 + 'px',
							   "min-width": computedHeight*scale + 'px',
							   "height": computedHeight + 'px'}, 400);
    });
}

function initShowNotifications() {
    $('.show-notifications').click(function(event) {
      event.preventDefault();
      var parent = this;
      var number = 0;
      $(this).parent().find('.hidden-notifications > .notification').each(function() {
        number++;
        if (number < 5) {
          $(parent).before(this);
          animateResize($(this).find(".avatar"), $(this).height());
        }
      });
      if ($(this).parent().find('.hidden-notifications > .notification').length == 0) {
        $(this).hide();
      }
    }
  );
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
	$('abbr.timeago').timeago().fadeIn();
  update();
	initShowNotifications();
});

$(window).load(function() {
    initDynamicAvatarSize();
	$('.avatar').fadeIn();
});
