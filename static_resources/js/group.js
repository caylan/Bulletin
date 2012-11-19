function initCommentSlider() {
    $('.comment-unhide-btn').click(function(event) {
    	var $commentForm;
        var $post;

        event.preventDefault();
        $post = $(this).parents('.post');
        $commentForm = $post.find(".comment-form-container");
        $(this).parent().fadeOut();
        $commentForm.show("blind", function() {
            $('html, body').animate({
                scrollTop: $post.offset().top - $('.navbar').height()
            }, 500);
        });
    });
}

function initCommentAjax() {
	$('.comment-form').submit(function(event) {
        event.preventDefault();

        var form = $(this);
        var url = 'post/' + form.find('input[name="id_post"]').val() + '/comment/';
        var msg = form.find('#id_message').val();
        var csrf = form.find('input[name="csrfmiddlewaretoken"]').val();

        $.post(url, {message: msg, csrfmiddlewaretoken: csrf}, function(data) {
            // copy of message is returned via json, insert into page
            comment_html = "<li class=\"media new comment\"> \
                           <div class=\"avatar-container pull-left media-object\"> \
                    <img class=\"avatar new pull-left media-object\" src=\"http://www.gravatar.com/avatar/" + md5(data.author.email) + "?s=300&d=mm" + "\" alt=\"commenters's gravatar\" /> </div>\
	                <div class=\"media-body\"> \
                   		<span class=\"media-heading\"> \
	                        <strong class=\"pull-left name\">" + data.author.first_name + " " + data.author.last_name + "</strong> \
	                        <em class=\"pull-right\"><abbr class=\"timeago new\" title=\"" + data.time_stamp + "\">" + data.date_posted + "</abbr></em> \
	                        <br /> \
	                    </span> \
	                    <div class=\"comment-message\">" + data.message + "</div> \
	                </div> \
	            </li>";
            form.parent().siblings('.comments').append($(comment_html));
            form.find("#id_message").val("");
            $('abbr.timeago').timeago();
            
            $('.comment.new').each(function() { 
                var postHeight = $(this).height();
                
                $(this).children('.avatar-container').each(function() { // Avatars within posts
                    $(this).find('.avatar').each(function() {
                        resizeAvatar(this, postHeight);
                    });
                });
            });
            
            $('.comments').find('.timeago.new').each(function() {$(this).fadeIn()});
        }, 'json');
    });
}

function initDynamicAvatarSize() {
	$('.post').each(function() { 
        var postHeight = $(this).height();
        
        $(this).children('.avatar-container').each(function() { // Avatars within posts
            $(this).find('.avatar').each(function() {
                resizeAvatar(this, postHeight);
            });
        });
        
        $(this).find('.comment').each(function() { // Avatars within comments
            var commentHeight = $(this).height();
            $(this).find('.avatar').each(function() {
                resizeAvatar(this, commentHeight);
            });
        });
    });
}

function resizeAvatar (avatar, parentHeight) {
    var img = document.createElement('img'); // This might have fixed the IE problem
    img.src = avatar.src;
    var scale = img.width/img.height;
    var computedHeight = Math.max(Math.min(img.height, parentHeight), 65);
    $(img).load(function() {
        $(avatar).css('height',  computedHeight + 'px');
        $(avatar).css('min-width',  computedHeight*scale + 'px');
        $(avatar).css('margin-left',  -(computedHeight*scale - 65 )/3 + 'px');
        $(avatar).fadeIn();
    });
}

$(document).ready(function() {
	$('abbr.timeago').timeago().fadeIn();
    
    initCommentSlider();
    initCommentAjax();
});

$(window).load(function() {
    initDynamicAvatarSize();
});