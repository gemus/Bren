jQuery.fn.userManager = function(user_name) {
    var container = this;
    var user_name = user_name;

    var validate_and_save_name = function() {
        var errors = new Array();
        var first_name_val = $('#first_name_input').val();
        var last_name_val = $('#last_name_input').val();

        if (first_name_val == '') errors.push('first_name');
        if (last_name_val  == '') errors.push('last_name');

        var save_user_callback = function(result, status) {
            console.log("SAVED!");
        }

        // No Errors so save the user
        if (errors.length == 0) {
            $.getJSON("/json_api/", {"id": 1,
                                     "method": "update_user",
                                     "params" : JSON.stringify([{'user_name': user_name,
                                                  'first_name': first_name_val,
                                                  'last_name' : last_name_val
                                                 }])
                                     },
                                     save_user_callback);
        }
    }

    // Create a user picker
    return this.each(function() {
        var get_user_callback = function(result, status) {
            user = result.result;

            collect='<div class="name_plate">' +
                        '<div style="float: right;" id="name_edit_link">'+
                            '<a href="javascript:void(0);">Edit</a>'+
                        '</div>' +
                        '<span id="first_name">' + user.first_name + '</span> '+
                        '<span id="last_name">'  + user.last_name  + '</span> '+
                    '</div>'+

                    '<div class="name_plate_edit" style="display: none;">'+
                        '<div style="float: right;">'+
                          '<a id="name_save_button" href="javascript:void(0);">Save</a> '+
                          '<a id="name_cancel_button" href="javascript:void(0);">Cancel</a>'+
                        '</div>'+
                        '<input type="text" id="first_name_input" value="' + user.first_name + '" style="width: 125px;"> '+
                        '<input type="text" id="last_name_input" value="'  + user.last_name  + '" style="width: 175px;"> '+
                    '</div>'+


                    '<div class="email">'+
                        '<a href="mailto:'+user.email+'">' + user.email + '</a> '+
                    '</div>'+


                    '<div class="dates">'+
                        '<span id="last_login">'  + user.last_login + '</span> <label>Last Logged In</label><br>'+
                        '<span id="date_joined">' + user.date_joined + '</span> <label>Date Joined</label>'+
                    '</div>';

            container.html(collect);

            // User clicks to edit it
            $("div.name_plate").click(function(){
                $('div.name_plate').hide();
                $('div.name_plate_edit').show();
            });

            // User cancels the edit
            $("#name_cancel_button").click(function(){
                $('div.name_plate').show();
                $('div.name_plate_edit').hide();

                // Reset the input fields
                $('input#first_name_input').val($('span#first_name').html());
                $('input#last_name_input').val($('span#last_name').html());
            });

            // User clicks save
            $("#name_save_button").click(function(e){
                validate_and_save_name();
            });

        }
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_user",
                                 "params" : '["'+user_name+'"]'
                                 },
                                 get_user_callback);
    });
}