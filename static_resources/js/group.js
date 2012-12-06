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
        		// copy of message is returned via html, insert into page
        		/* comment_html = data;
        		 * form.parent().siblings('.comments').append($(comment_html));
        		 */

        		/* $('.comment.new').each(function() { 
        		 *     var postHeight = $(this).height();
        		 *     
        		 *     $(this).children('.avatar-container').each(function() { // Avatars within posts
        		 *         $(this).find('.avatar').each(function() {
        		 *             resizeAvatar(this, postHeight);
        		 *         });
        		 *     });
        		 * });
        		 */
        		/* $post = $(form).parents('.post');
        		 * var postHeight = $($post).height();
        		 * $($post).children('.avatar-container').each(function() { // Avatars within posts
        		 * 	$(this).find('.avatar').each(function() {
        		 * 		animateResize(this, postHeight);
        		 * 	});
        		 * });
        		 */
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

        		/* $('.timeago.new').timeago().fadeIn();
        		 */
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

function truncateComments () {
	$('.comments').each(function() {
			var comments = $(this).find('.comment');
			if (comments.length > 5) {
				for (var i = 0; i < comments.length - 3; i++) {
					$(comments[i]).hide();
				}
			}
		}
	);
}

function truncatePosts () {
	var posts = $(this).find('.post');
	if (posts.length > 10) {
		for (var i = 10; i < posts.length; i++) {
			$(posts[i]).hide();
		}
	}
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
	$('abbr.timeago').timeago().fadeIn();
    initCommentSlider();
    initCommentAjax();
    initPostAjax();
    update();
	lastCommentTimestamp();
});

$(window).load(function() {
    initDynamicAvatarSize();
	$('.avatar').fadeIn();
});
