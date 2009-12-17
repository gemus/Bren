jQuery.fn.userPicker = function() {
    // Create a user picker
    return this.each(function() {
        var main_buttons_html = '<p>Pick A User</p>';
        $(this).html(main_buttons_html);
    });
}