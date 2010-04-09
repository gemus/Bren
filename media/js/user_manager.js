jQuery.fn.userManager = function(user_name) {
    var container = this;
    var user_name = user_name;

    // Create a user picker
    return this.each(function() {
        var get_user_callback = function(result, status) {
            user = result.result;

            collect  = '<div class="name_plate">';
            collect += '<span id="first_name">' + user.first_name + '</span> ';
            collect += '<span id="last_name">'  + user.last_name + '</span>';
            collect += '</div>';
            collect += '<div class="email">';
            collect += '<a href="mailto:'+user.email+'">' + user.email + '</a> ';
            collect += '</div>';
            collect += '<div class="dates">';
            collect += '<label>Last Login</label><span id="last_login">'  + user.last_login + '</span><br>';
            collect += '<label>Date Joined</label><span id="date_joined">' + user.date_joined + '</span>';
            collect += '</div>';

            container.html(collect);
        }
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_user",
                                 "params" : '["'+user_name+'"]'
                                 },
                                 get_user_callback);
    });
}