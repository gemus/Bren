jQuery.fn.numPadInput = function() {
    return this.each(function() {
        var num_pad_id = this.id + "_numpad_input";
        var input_field_id = this.id;
        var is_open = false;

        $("#"+input_field_id).addClass("numpad_input_field");

        var closeNumpad = function() {
            $("#"+num_pad_id).remove();
            is_open = false;
        }

        var addNumber = function(number) {
            var theVal = $("#"+input_field_id).val();
            // Normalize the input
            theVal = parseInt(theVal.replace(":", "").replace(/^0*/, "") + number);
            minutes = parseInt(theVal / 100);
            seconds = theVal % 100;
            if (seconds < 10) seconds = "0" + seconds
            $("#"+input_field_id).val( minutes + ":" + seconds );
        }

        // ====================================
        // = When the User Focus On The Input =
        // ====================================
        $(this).focus(function() {
            if (!is_open) {
                var numPadHTML = '<div id="'+num_pad_id+'" class="numpad_input_container"><div>';
                numPadHTML += "<table><tbody>";
                numPadHTML += "<tr><td>1</td><td>2</td><td>3</td></tr>";
                numPadHTML += "<tr><td>4</td><td>5</td><td>6</td></tr>";
                numPadHTML += "<tr><td>7</td><td>8</td><td>9</td></tr>";
                numPadHTML += "<tr><td>C</td><td>0</td><td>OK</td></tr>";
                numPadHTML += "</tbody></table>";
                numPadHTML += "</div></div>";

                $(this).after(numPadHTML);
                is_open = true;
            }

            $("#"+num_pad_id + " > div > table > tbody > tr > td ").each(function() {
                $(this).click(function() {
                    if (this.innerHTML == "C") {
                        $("#"+input_field_id).val("0:00");
                    } else if (this.innerHTML == "OK") {
                        closeNumpad();
                    } else {
                        addNumber(this.innerHTML);
                        //$("#"+input_field_id).val( $("#"+input_field_id).val() + this.innerHTML);
                    }
                })
            })
        });


        // ===================
        // = User clicks off =
        // ===================
        $("body").click(function(e) {
            // Did the user click the popup widget, or the input box?
            if ($(e.target).parents().filter("#"+num_pad_id).length > 0 || $(e.target).is("#"+input_field_id)) {
                // pass
            } else {
                closeNumpad();
            }

        });
    });
}