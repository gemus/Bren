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
                var input = $(this);
                var example_text = options.example_text || input.attr("example_text");
                input.blur(function () {
                    if (input.val() === '') {
                        input.val(example_text).addClass(options.blurClass);
                    }
                }).focus(function () {
                    if (input.hasClass(options.blurClass)) {
                        input.val('');
                    }
                    input.removeClass(options.blurClass);
                });
                input.blur();
            });
        }
    });
})(jQuery);