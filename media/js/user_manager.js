jQuery.fn.userManager = function(user_name) {
    var container = this;
    var user_name = user_name;

    var change_view = function(view) {
        // View One of: 'edit', 'view'
        if (view == 'view') {
            $("#view_canvas").show();
            $("#view_actions").show();

            $("#edit_canvas").hide();
            $("#edit_actions").hide();
            $("#name_plate_error").hide();
        } else if (view == 'edit') {
            $("#edit_canvas").show();
            $("#edit_actions").show();

            $("#view_canvas").hide();
            $("#view_actions").hide();
        }
    }

    var validate_email_address = function(email_addy) {
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        return reg.test(email_addy);
    }

    var validate_and_save = function() {
        // Clear old validation errors
        $("#name_plate_error").hide();
        $("#email_plate_error").hide();

        var errors = new Array();
        var first_name_val = $('#first_name_input').val();
        var last_name_val = $('#last_name_input').val();
        var email_val = $('#email_input').val();

        // Do some validation
        if (first_name_val == '') errors.push(['name', 'First Name']);
        if (last_name_val  == '') errors.push(['name', 'Last Name']);
        if (!validate_email_address(email_val) && email_val.length > 0 ) {
            errors.push(['email','Invalid Email']);
        }

        var success_save_user_callback = function(result, status) {
            // Update the view name plate
            $('span#first_name').html(first_name_val);
            $('span#last_name').html(last_name_val);

            // Then update the scroller
            $('#'+user_name+'').html(first_name_val + " " + last_name_val);

            // Finally change the view
            change_view("view");
        }

        // No Errors so save the user
        if (errors.length == 0) {
            $("#name_plate_error").hide();
            $.getJSON("/json_api/", {"id": 1,
                                     "method": "update_user",
                                     "params" : JSON.stringify([{'user_name': user_name,
                                                  'first_name': first_name_val,
                                                  'last_name' : last_name_val
                                                 }])
                                     },
                                     success_save_user_callback);
        } else {
            var name_errors = new Array();
            var email_errors = new Array();
            for (i in errors) {
                if (errors[i][0] == 'name') name_errors.push(errors[i][1]);
                if (errors[i][0] == 'email') email_errors.push(errors[i][1]);
            }

            console.log(email_errors);

            if (name_errors.length > 0) {
                $("#name_plate_error").slideDown();
                $("#name_plate_error").html(name_errors.join(", ") + " Is Required");
            }
            if (email_errors.length > 0) {
                $("#email_plate_error").slideDown();
                $("#email_plate_error").html("Invalid Email");
            }
        }
    }

    // Create a user picker
    return this.each(function() {
        var get_user_callback = function(result, status) {
            user = result.result;

            collect='<div id="view_canvas">'+
                        '<div class="name_plate">' +
                            '<span id="first_name">' + user.first_name + '</span> '+
                            '<span id="last_name">'  + user.last_name  + '</span> '+
                        '</div>'+

                        '<div class="email_plate">'+
                            '<a id="email" class="email_link" href="mailto:'+user.email+'">' + user.email + '</a> '+
                        '</div>'+
                    '</div>' +

                    '<div id="edit_canvas" style="display: none;">' +
                        '<div class="name_plate_edit">'+
                            '<input type="text" id="first_name_input" value="' + user.first_name + '" style="width: 125px;"> '+
                            '<input type="text" id="last_name_input" value="'  + user.last_name  + '" style="width: 175px;"> '+
                        '</div>'+
                        '<div id="name_plate_error" class="error_plate" style="display: none;"></div>'+

                        '<div class="email_plate_edit">'+
                            '<input type="text" id="email_input" value="'  + user.email  + '" style="width: 175px;"> '+
                        '</div>'+
                        '<div id="email_plate_error" class="error_plate" style="display: none;"></div>'+
                    '</div>' +

                    '<div class="dates">'+
                        '<span id="last_login">'  + user.last_login + '</span> <label>Last Logged In</label><br>'+
                        '<span id="date_joined">' + user.date_joined + '</span> <label>Date Joined</label>'+
                    '</div>' +

                    '<div id="view_actions">'+
                        '<a href="javascript:void(0);" id="edit_button">Edit</a>' +
                    '</div>' +
                    '<div id="edit_actions" style="display: none;">'+
                        '<a href="javascript:void(0);" id="save_button">Save</a> ' +
                        '<a href="javascript:void(0);" id="cancel_button">Cancel</a>' +
                    '</div>';


            container.html(collect);

            // User clicks to edit it
            $("#edit_button").click(function(){
                change_view("edit");
            });

            // User cancels the edit
            $("#cancel_button").click(function(){
                change_view("view");

                // Reset the input fields
                $('input#first_name_input').val($('span#first_name').html());
                $('input#last_name_input').val($('span#last_name').html());
                $('input#email_input').val($('a#email').html());
            });

            // User clicks save
            $("#save_button").click(function(e){
                validate_and_save();
            });

        }
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_user",
                                 "params" : JSON.stringify([user_name])
                                 },
                                 get_user_callback);
    });
}