jQuery.fn.userPicker = function() {
    // Create a user picker
    return this.each(function() {
        var letter_buttons = ["ABC","DEF","GHI","JKL","MNO","PQRS","TUV","WXYZ"];

        var main_buttons_html = "";
        for (i in letter_buttons) {
            main_buttons_html += "<a href='#'>"+letter_buttons[i]+"</a>";
        }
        '<p>Pick A User</p>';
        $(this).html(main_buttons_html);
    });
}