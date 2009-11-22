jQuery.fn.numPadInput = function() {
    return this.each(function() {
        var num_pad_id = this.id + "_numpad_input";
        var input_field_id = this.id;
        var is_open = false;

        // ====================================
        // = When the User Focus On The Input =
        // ====================================
        $(this).focus(function() {
            if (!is_open) {
                var numPadHTML = '<div id="'+num_pad_id+'"><div>';
                numPadHTML += "Input Time"
                numPadHTML += "</div></div>";

                $(this).after(numPadHTML);
                is_open = true;
            }
        });


        // ===================
        // = User clicks off =
        // ===================
        $("body").click(function(e) {
            // Did the user click the popup widget, or the input box?
            if ($(e.target).parents().filter("#"+num_pad_id).length > 0 || $(e.target).is("#"+input_field_id)) {
                // pass
            } else {
                $("#"+num_pad_id).remove();
                is_open = false;
            }

        });
    });
}