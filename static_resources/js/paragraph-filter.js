// Compresses a block of text into a set of paragraph tags.
function paragraph_filter($str) {
  // Change all breaks to newlines.
  $str.replace(["\r\n", "\r"], "\n");
  // Convert multi-newlines to two newlines.
  $str.replace("/\n\n+/", "/\n\n/");
  // Create two newlines into paragraph tags.
  $str.replace("\n\n", "</p>\n\n<p>");
}

$(document).ready(function() {
  // Paragraphify all of the comments and the posts.
  var $comments = $('.comment-message, .post-message');
  $comments.each(function() {
    $(this).html(paragraph_filter($(this).html()));
  });
});
