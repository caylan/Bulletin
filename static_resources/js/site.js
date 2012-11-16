$(document).ready(function() {
    $('.tabs-left').children().each(function() {
        $(this).css("height", $(this).parent().css("height"));
    });
    // Find ALL <form> tags
    $('form').submit(function(){
        // On submit disable its submit button
        $('.submit-btn', this).attr('disabled', 'disabled');
    });
});

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-36110349-1']);
_gaq.push(['_setDomainName', 'bulletinapp.net']);
_gaq.push(['_trackPageview']);

(function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

$(window).scroll(function(){
    if ($(window).scrollTop() != 0){
        $("#jump-top").show(500);
    } else {
        $("#jump-top").hide();
    }
});

$("#flipbox").flip({
	direction:'tb',
	onBefore: function(){
			console.log('before starting the animation');
	},
	onAnimation: function(){
			console.log('in the middle of the animation');
	},
	onEnd: function(){
			console.log('when the animation has already ended');
	}
});