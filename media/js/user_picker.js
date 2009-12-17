jQuery.fn.userPicker = function() {
    // Create a user picker
    return this.each(function() {
        // Create the base buttons
        var letter_buttons = ["ABC","DEF","GHI","JKL","MNO","PQRS","TUV","WXYZ"];
        var main_buttons_html = "";
        for (i in letter_buttons) {
            main_buttons_html += "<a class='user_picker' href='javascript:void(0);'>"+letter_buttons[i]+"</a>";
        }
        '<p>Pick A User</p>';
        $(this).html(main_buttons_html);

        var button_callback = function(result, status) {
            console.log(result);
        }

        var buttonClick = function(evnt) {
            $(this).parent().children().each(function() {
                $(this).removeClass("selected");
            });
            $(this).addClass("selected");

            $.getJSON("/json_api/", {"id": 1,
                                     "method": "get_users",
                                     "params" : [$(this).html()]},
                                     button_callback)
        }

        // Hook in the event handling
        $(this).children().each(function() {
            $(this).click(buttonClick);
        })
    });
}