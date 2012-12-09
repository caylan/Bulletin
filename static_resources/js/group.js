/* Automatically makes an ajax call to 'update/' view
 * times out after 25s
 * after timeout or sucess, recursively calls itself again
 *
 * based on example from
 * http://techoctave.com/c7/posts/60-simple-long-polling-example-with-javascript-and-jquery
 */
function update() {
    $.ajax({url: "update/", success: function(data) {
    	$data = $(data);
    	if ($data.hasClass("comment")) {
            // returned data is a comment
            var postID = "#post-" + $data.attr("post");
            var $newComment = $data
            $newComment.hide();
            $newComment.find(".avatar").show();
            $newComment.find(".timeago").timeago().show();
            $(postID).find(".comment-form-container").before($newComment);
			$(postID).find(".comment-form-container input[type='text']").focus();
            $newComment.fadeIn();
            var $parentPost = $newComment.parents(".post");
            var $postAvatar = $parentPost.children(".avatar-container").find(".avatar");
            var postHeight = $parentPost.height();
            animateResize($postAvatar, postHeight);
			lastCommentTimestamp();
        } else if ($data.hasClass("post")) {
            // returned data is a post
            var $newPost = $data;
            var $noPost = $('.alert.alert-warning');
            $newPost.hide();
            $newPost.find(".avatar").show();
            $newPost.find(".timeago").timeago().show();

            removeNoPostWarning($noPost);
            $("#posts").prepend($newPost);
            $newPost.fadeIn();
			animateResize($newPost.find(".avatar"), $($newPost).height());
            initCommentSlider();
            initCommentAjax();
        }
    }, dataType: "html", complete: update, timeout: 25000});
}

function initCommentSlider() {
    $('.comment-unhide-btn').click(function(event) {
    	var $commentForm;
        var $post;

        event.preventDefault();
        $post = $(this).parents('.post');
        $commentForm = $post.find(".comment-form-container");
        $(this).parent().hide();
        $commentForm.fadeIn(function() {
			var scroll = $post.offset().top - $('.navbar').height();
			if (scroll + $(window).height() < $commentForm.offset().top + $commentForm.height()) {
				scroll += $commentForm.offset().top + $commentForm.height() - (scroll + $(window).height());
			}
            $('html, body').animate({
                scrollTop: scroll
            }, 500);
			$($commentForm).find('input[type="text"]').focus();
			var postHeight = $($post).height();
        
			$($post).children('.avatar-container').each(function() { // Avatars within posts
				$(this).find('.avatar').each(function() {
					animateResize(this, postHeight);
				});
			});
        });
    });
}

function initCommentAjax() {
	$('.comment-form').submit(function(event) {
        event.preventDefault();

        var $form = $(this);
        var $submitBtn = $form.find('input[type="submit"]');
        var url = '/post/' + $form.find('input[name="id_post"]').val() + '/comment/';
        var $msgContainer = $form.find('#id_message');
        var msg = $msgContainer.val();
        var csrf = $form.find('input[name="csrfmiddlewaretoken"]').val();
        var $loadingSpinner = $form.siblings('.loading-spinner');

        $msgContainer.attr("disabled", "disabled");
        $submitBtn.attr("disabled", "disabled");
        $loadingSpinner.show();

        $.ajax({type: 'POST',
        	url: url,
        	data: {message: msg, csrfmiddlewaretoken: csrf},
        	datatype: 'html',
        	success: function(data) {
        		$msgContainer.val("");
        		$commentForm = $($form).parents('.comment-form-container');
        		var scroll = window.pageYOffset - $('.navbar').height();
        		if (scroll + $(window).height() < $commentForm.offset().top + $commentForm.height()) {
        			scroll += $commentForm.offset().top + $commentForm.height() - (scroll + $(window).height());
        			$('html, body').animate({
        				scrollTop: scroll
        			}, 500, function() {
        				$($commentForm).find('input[type="text"]').focus();
        			});
        		} else {
        			$($commentForm).find('input[type="text"]').focus();
        		}
        	},
        	complete: function() {
        		$loadingSpinner.hide();
        		$submitBtn.removeAttr("disabled");
        		$msgContainer.removeAttr("disabled");
        	}});
	});
}

function initPostAjax() {
	$("#post_form").submit(function(event) {
		event.preventDefault();

		var $form = $(this);
		var $submitBtn = $form.find('input[type="submit"]');
		var url = 'post/';
		var $msgContainer = $form.find('#id_message');
		var msg = $msgContainer.val();
		var csrf = $form.find('input[name="csrfmiddlewaretoken"]').val();
		var $loadingSpinner = $form.find('.loading-spinner');
        var $noPost = $form.siblings('.alert.alert-warning');

        $msgContainer.attr("disabled", "disabled");
        $submitBtn.attr("disabled", "disabled");
        $loadingSpinner.show();

		$.ajax({type: "POST",
               url: url,
               data: {message: msg, csrfmiddlewaretoken: csrf},
               datatype: "html",
               success: function() {
                   removeNoPostWarning($noPost);
            	   $msgContainer.val("");
               },
               complete: function() {
            	   $loadingSpinner.hide();
            	   $submitBtn.removeAttr("disabled");
            	   $msgContainer.removeAttr("disabled");
               }});
	});
}

function removeNoPostWarning($noPost) {
    if ($noPost.length != 0) {
        $noPost.parent().append($("<ul id='posts' class='media-list'></ul>"));
        $noPost.slideUp(function() {
            $noPost.remove();
        });
    }
}

function initDynamicAvatarSize() {
	$('.post').each(function() { 
        var postHeight = $(this).height();
        $(this).children('.avatar-container').each(function() { // Avatars within posts
            $(this).find('.avatar').each(function() {
                resizeAvatar(this, postHeight);
            });
        });
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

function initShowComments () {
	$('.show-comments').click(function(event) {
            event.preventDefault();
			var parent = this;
			$(this).parent().find('.hidden-comments > .comment').each(function() {
				$(parent).before(this);
			});
			$(this).parent().find('.triangle.dark').removeClass("dark");
			$(this).hide();
		}
	);
}

$(document).ready(function() {
	$(".remove-user").click(function() {
		// var user_name = $(this).prev(".member-name").html();
		var user_name = $(this).prev("abbr").attr("title");
		// var member_id = $(this).prev(".member-name").attr("memid");
		var member_id = $(this).prev("abbr").find("img").attr("memid");
		$("#remove-user-confirm").find("#user-name-here").html(user_name);
		$("#remove-user-confirm").find("#user-name-here").attr("memid", member_id);
		$("#remove-user-confirm").modal();
	});
	$("#remove-user-btn").click(function() {
		$(this).attr("disabled", "disabled");
		var member_id = $(this).parents("#remove-user-confirm").find("#user-name-here").attr("memid");
		$.ajax({
			url: "/membership/" + member_id + "/remove/",
			error: function(data) {alert("failed to delete user");},
			success: function(){},
			complete: function() {
				$("#remove-user-btn").removeAttr("disabled");
				// $(".member-name[memid='" + member_id + "']").parent().hide();
				$("img[memid='" + member_id + "']").parent().parent().hide();
				$("#remove-user-confirm").modal('hide');
			}
		});
	});
	$(".remove-invite").click(function() {
		$(this).parent().parent().hide();
	});
});

function initShowPosts () {
	$('.show-posts').click(function(event) {
            event.preventDefault();
			var parent = this;
			var number = 0;
			$(this).parent().find('.hidden-posts > .post').each(function() {
				number++;
				if (number < 5) {
					$(parent).before(this);
					animateResize($(this).find(".avatar"), $(this).height());
				}
			});
			if ($(this).parent().find('.hidden-posts > .post').length == 0) {
				$(this).hide();
			}
		}
	);
}

function lastCommentTimestamp () {
	$('.comments').each(function() {
			var discuss = $(this).find('.discuss');
			$(this).find('.comment').each(function() {
				var comment = this;
				$(this).find('em').each(function() {
					var timestamp = this;
					$(this).hide();
					$(comment).unbind('mouseout');
					$(comment).unbind('mouseover');
					$(comment).find('.timeago').css('position', 'absolute');
					$(comment).find('em').css('width', '100%');
					$(comment).find('.timeago').css('background-color', 'white');
					$(comment).mouseover(function() {
						$(timestamp).show();
					});
					$(comment).mouseout(function() {
						$(timestamp).hide();
					});
				});
			});
			$(this).find('em:last').each(function() {
				$(this).parent().parent().parent().unbind('mouseout');
				$(this).show();
				$(this).find('.timeago').css('position', 'static');
				$(this).css('width', 'auto');
				$(this).find('.timeago').css('background-color', 'transparent');
			});
		}
	);
	$('.comment-form').find('input[type="text"]').focus(function() {
		//$(this).parent().find('input[type="submit"]').removeClass('btn-primary');
		//$(this).parent().find('input[type="submit"]').addClass('btn-primary');
		$(this).parent().find('input[type="submit"]').fadeIn(200);
	});
	$('.comment-form').find('input[type="text"]').blur(function() {
		//$(this).parent().find('input[type="submit"]').removeClass('btn-primary');
		$(this).parent().find('input[type="submit"]').fadeOut(200);

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
	$('abbr.timeago').timeago().fadeIn();
    initCommentSlider();
    initCommentAjax();
    initPostAjax();
    update();
	lastCommentTimestamp();
	initShowComments();
	initShowPosts();
	$('.hero-unit').css('min-height', $('#left-column').height() - 26);
});

$(window).load(function() {
    initDynamicAvatarSize();
	$('.avatar').fadeIn();
});
