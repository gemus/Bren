jQuery.fn.userPicker = function() {
    // Create a user picker
    return this.each(function() {
        // Create the base buttons
        var letter_buttons = ["ABC","DEF","GHI","JKL","MNO","PQRS","TUV","WXYZ"];
        var main_buttons_html = "<div id='letter_select_canvas'>";
        for (i in letter_buttons) {
            main_buttons_html += "<a class='user_picker_letters' href='javascript:void(0);'>"+letter_buttons[i]+"</a>";
        }
        main_buttons_html += "</div>";

        var user_select_canvas = "<div id='user_select_canvas'></div>"
        $(this).html(main_buttons_html +
                     user_select_canvas );

        var button_callback = function(result, status) {
            result = result.result
            var people = "";
            for (i in result) {
                people += "<a class='user_picker_names' href='javascript:void(0);'>" + result[i]['display_name'] + "</a>";
            }
            $("#user_select_canvas").html(people);
        }

        var buttonClick = function(evnt) {
            $(this).parent().children().each(function() {
                $(this).removeClass("selected");
            });
            $(this).addClass("selected");

            // Create the JSON array of letters. Eg: '["J","K","L"]'
            var letters = $(this).html();
            var letters_json = "[";
            for (i in letters) {
                letters_json += '"' + letters.charAt(i) + '",';
            }
            letters_json = letters_json.substring(0, letters_json.length-1) + "]";

            $.getJSON("/json_api/", {"id": 1,
                                     "method": "get_users",
                                     "params" : letters_json
                                     },
                                     button_callback)
        }

        // Hook in the event handling
        $("#letter_select_canvas").children().each(function() {
            $(this).click(buttonClick);
        })
    });
}