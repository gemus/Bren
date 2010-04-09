jQuery.fn.userManager = function(user_name) {
    var container = this;
    var user_name = user_name;

    // Create a user picker
    return this.each(function() {
        var get_user_callback = function(result, status) {
            user = result.result;

            collect='<div class="name_plate">' +
                        '<div style="float: right;" id="name_edit_link">'+
                            '<a href="javascript:void();">Edit</a>'+
                        '</div>' +
                        '<span id="first_name">' + user.first_name + '</span> '+
                        '<span id="last_name">'  + user.last_name  + '</span> '+
                    '</div>'+

                    '<div class="name_plate_edit" style="display: none;">'+
                        '<div style="float: right;">'+
                          '<a href="javascript:void();">Save</a> '+
                          '<a id="name_cancel_button" href="javascript:void();">Cancel</a>'+
                        '</div>'+
                        '<input type="text" id="first_name" value="' + user.first_name + '" style="width: 125px;"> '+
                        '<input type="text" id="last_name" value="'  + user.last_name  + '" style="width: 175px;"> '+
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
                $('input#first_name').val($('span#first_name').html());
                $('input#last_name').val($('span#last_name').html());
            });
        }
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_user",
                                 "params" : '["'+user_name+'"]'
                                 },
                                 get_user_callback);
    });
}