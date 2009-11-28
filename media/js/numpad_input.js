jQuery.fn.numPadInput = function(isTime, clearValue) {
    // Create a numpad for an input field.
    // isTime <bool> : Weather to display at time. Eg. 0:15

    if (clearValue == undefined) {
        if (isTime) {
            clearValue = "0:00";
        } else {
            clearValue = "0";
        }
    }

    return this.each(function() {

        var num_pad_id = this.id + "_numpad_input";
        var input_field_id = this.id;
        var is_open = false;

        var closeNumpad = function() {
            $("#"+num_pad_id).remove();
            is_open = false;
        }
        var clearField = function() {
            $("#"+input_field_id).val(clearValue);
        }
        var addNumber = function(number) {
            var theVal = $("#"+input_field_id).val();

            if ($("#"+input_field_id).val() == "") {
                $("#"+input_field_id).val(number);
            } else if (isTime) {
                // Normalize the input
                theVal = parseInt(theVal.replace(":", "").replace(/^0*/, "") + number);
                minutes = parseInt(theVal / 100);
                seconds = theVal % 100;
                if (seconds < 10) seconds = "0" + seconds;
                $("#"+input_field_id).val( minutes + ":" + seconds );
            } else {
                theVal = parseInt($("#"+input_field_id).val());
                $("#"+input_field_id).val(theVal*10 + parseInt(number));
            }
        }

        $("#"+input_field_id).addClass("numpad_input_field");
        clearField();

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
                        clearField();
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
        $("html").click(function(e) {
            // Did the user click the popup widget, or the input box?
            if ($(e.target).parents().filter("#"+num_pad_id).length > 0 || $(e.target).is("#"+input_field_id)) {
                // pass
            } else {
                closeNumpad();
            }

        });
    });
}