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

                    '<div class="name_plate_edit">'+
                        '<div style="float: right;">'+
                          '<a href="javascript:void();">Save</a> '+
                          '<a href="javascript:void();">Cancel</a>'+
                        '</div>'+
                        '<span id="first_name">' + user.first_name + '</span> '+
                        '<span id="last_name">'  + user.last_name + '</span> '+
                    '</div>'+


                    '<div class="email">'+
                        '<a href="mailto:'+user.email+'">' + user.email + '</a> '+
                    '</div>'+


                    '<div class="dates">'+
                        '<span id="last_login">'  + user.last_login + '</span> <label>Last Logged In</label><br>'+
                        '<span id="date_joined">' + user.date_joined + '</span> <label>Date Joined</label>'+
                    '</div>';

            container.html(collect);
        }
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_user",
                                 "params" : '["'+user_name+'"]'
                                 },
                                 get_user_callback);
    });
}