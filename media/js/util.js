/*
 * Will put example text into the input if the value is blank. As well
 * as setting a blur css class. It is up to the user to clear the text.
 *
 * <input type="text" example_text="First Name" value="" id="first_name">
 * $("input#first_name").exampleInput();
 *
 */
 
(function ($) {
    $.extend($.fn, {
        exampleInput: function (options) {
            var defaults = {blurClass: 'blur'};
            options = $.extend(defaults, options);

            return this.each(function () {
                // Setup the example if there is nothing in the field
                var input = $(this);
                if (input.val() == "") {
                    input.addClass(options.blurClass)
                    .val(input.attr("example_text"))
                    .bind('focus.exampleInput', function() { // This is done so we can remove
                        input.val("")                        // it later without removing
                        .unbind('focus.exampleInput')        // other bound focus events
                        .removeClass(options.blurClass)
                    });
                }
            });
        }
    });
})(jQuery);