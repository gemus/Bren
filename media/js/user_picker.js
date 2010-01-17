jQuery.fn.keyboard_creator = function(callback_func) {
    var generate_key_link = function(key_letter) {
        if (key_letter == "Clear") {
            return '<a href="javascript:void(0);" id="clear_button">' + key_letter + '</a>';
        } else {
            return '<a href="javascript:void(0);" class="keyboard_letters">' + key_letter + '</a>';
        }
    }

    // Create a keyboard users can use to enter text
    return this.each(function() {
        var keys = [["Q","W","E","R","T","Y","U","I","O","P"],
                   ["A","S","D","F","G","H","J","K","L",],
                   ["Z","X","C","V","B","N","M", "Clear"]]

        // Write out the keys
        var collect = "";
        for (row in keys) {
            collect += "<div id='keyboard_row_"+row+"'>";
            for (col in keys[row]) {
                collect += generate_key_link(keys[row][col]);
            }
            collect += "</div>";
        }
        $(this).html(collect);

        // Call the callback_func pass it the text of the key pressed
        $(this).find("a.keyboard_letters").each(function() {
            $(this).click(function() {
                callback_func($(this).html());
            });
        })

    });
}

jQuery.fn.userPicker = function() {
    var generate_user_select_link = function(user_name, display_name) {
        return '<a username="'+user_name+'" href="javascript:void(0);" class="user_picker_names">'+display_name+'</a>';
    }

    var show_pin_pad = function() {
        if (!($("#userPickerCanvas").attr('is_shown') == 'true')) {
            $("#userPickerCanvas").animate({
                    marginLeft: "0px",
                  }, 500 , "swing", function() {
                      $("#login_content").css({'display': 'block'});
                      $("#login_content").animate({ opacity: "1.0" }, 500);
                  });
            $("#userPickerCanvas").attr({'is_shown': 'true'});

        }
    }

    var select_button = function(target) {
        $(target).parent().children().each(function() {
            $(this).removeClass("selected");
        });
        $(target).addClass("selected");
    }

    var namesClick = function(evnt) {
        select_button(this);
        $("#name_plate").html($(this).html());
        $("#id_username").val($(this).attr('username'));
        show_pin_pad();
    }

    // Create a user picker
    return this.each(function() {

        // Create places for things to go
        $(this).html("<h2>Enter Your First Name Please</h2>"+
                     "<div id='keyboard_keys_canvas'></div>"+
                     "<div id='keyboard_line_container'><input type='text' id='keyboard_line' disabled='disabled'></div>" +
                     "<div id='user_select_canvas'></div>");

        var search_callback = function(result, status) {
            var result = result.result;

            var collect = "";
            for (i in result) {
                collect += generate_user_select_link(
                                        result[i]['user_name'],
                                        result[i]['display_name']);
            }
            $("#user_select_canvas").html(collect);

            // Hook in the event handling
            $("#user_select_canvas").children().each(function() {
                $(this).click(namesClick);
            })
        }

        var keyboard_pressed_func = function(letter) {
            $("#keyboard_line").val($("#keyboard_line").val() + letter);

            var params = '["' + $("#keyboard_line").val() + '"]';
            $.getJSON("/json_api/", {"id": 1,
                                     "method": "get_users",
                                     "params" : params
                                     },
                                     search_callback)
        }

        $("#keyboard_keys_canvas").keyboard_creator(keyboard_pressed_func);

        // When the user clears the field
        $("#clear_button").click(function() {
            $("#keyboard_line").val("");
            $("#user_select_canvas").html("");
            $("#name_plate").html("");
            $("#id_username").val("");

            $("#errorBox").css({'opacity': 0.0});
        });

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