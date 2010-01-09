jQuery.fn.keyboard_creator = function() {
    // Create a keyboard users can use to enter text
    return this.each(function() {
        // Write out the keys
        $(this).html("KEYBOARD GOES HERE");
    });
}

jQuery.fn.userPicker = function() {
    // Create a user picker
    return this.each(function() {
        
        // Create places for things to go
        $(this).html("<div id='keyboard_keys_canvas'></div>"+
                     "<input type='text' id='keyboard_line'>" +
                     "<div id='user_select_canvas'></div>");

        $("#keyboard_keys_canvas").keyboard_creator()

    });
}

/*
jQuery.fn.userPicker = function() {
    // Create a user picker
    return this.each(function() {
        // Create the base buttons
        var letter_buttons = ["ABC","DE","FGH","IJ","KL","MNO","PQR","STUV","WXYZ"];
        var main_buttons_html = "<div id='letter_select_canvas'>";
        for (i in letter_buttons) {
            main_buttons_html += "<a class='user_picker_letters' href='javascript:void(0);'>"+letter_buttons[i]+"</a>";
        }
        main_buttons_html += "</div>";

        var user_select_canvas = "<div id='user_select_canvas'></div>"
        $(this).html(main_buttons_html +
                     user_select_canvas );

        var select_button = function(target) {
            $(target).parent().children().each(function() {
                $(this).removeClass("selected");
            });
            $(target).addClass("selected");
        }

        var show_pin_pad = function() {
            if (!($("#userPickerCanvas").attr('is_shown') == 'true')) {
                $("#userPickerCanvas").animate({
                        width: "800px",
                      }, 500 , "swing", function() {
                          $("#login_content").css({'z-index': 10 });
                          $("#login_content").animate({ opacity: "1.0" }, 500);
                      });
                $("#userPickerCanvas").attr({'is_shown': 'true'});

            }
        }

        var show_name_picker = function() {
            if (!($("#user_select_canvas").attr('is_shown') == 'true')) {
                $("#user_select_canvas").css({'opacity': 0.0});
                $("#user_select_canvas").animate({'opacity': 1.0});
                $("#user_select_canvas").attr({'is_shown': 'true'});
            }
        }

        var namesClick = function(evnt) {
            select_button(this);
            $("#name_plate").html($(this).html());
            $("#id_username").val($(this).attr('username'));
            show_pin_pad();
        }

        var button_callback = function(result, status) {
            result = result.result
            var people = "";
            for (i in result) {
                people += "<a class='user_picker_names' href='javascript:void(0);' username='"+result[i]['user_name']+"'>" + result[i]['display_name'] + "</a>";
            }
            $("#user_select_canvas").html(people);

            // Hook in the event handling
            $("#user_select_canvas").children().each(function() {
                $(this).click(namesClick);
            })
            show_name_picker();
        }

        var lettersClick = function(evnt) {
            select_button(this);

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
            $(this).click(lettersClick);
        })
    });
}
*/