var $accordions = $('.accordion a.accordion-toggle');
$accordions.each(function() {
    var $this = $(this);
    $this.click(function(event) {
        var attr = $this.attr("href");
        if ($(attr).hasClass("in")) {
            event.preventDefault();
            event.stopImmediatePropagation();
        }
    });
});
var landing = true;