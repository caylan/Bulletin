// Compresses a block of text into a set of paragraph tags.
function paragraph_filter(str) {
  // Change all breaks to newlines.
  str = str.replace(/\r\n/g, "\n");
  str = str.replace(/\r/g, "\n");
  // Convert multi-newlines to two newlines.
  str = str.replace(/\n\n+/g, "\n\n");
  // Convert newline into <br /> tag
  str = str.replace(/\n/g, "<br />");
  alert(str);
  return str;
}

$(document).ready(function() {
  // Paragraphify all of the comments and the posts.
  var $messages = $('.comment-message, .post-message');
  $messages.each(function() {
    $(this).html(paragraph_filter($(this).html()));
  });
});
