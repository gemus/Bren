jQuery.fn.userManager = function(user_id) {
    var container = this;
    var user_id = user_id;
    
    // Create a user picker
    return this.each(function() {
        var get_user_callback = function(result, status) {
            user = result.result;
            
            collect  = '<div>';
            collect += '<span id="first_name">' + user.first_name + '</span> ';
            collect += '<span id="last_name">'  + user.last_name + '</span>';
            collect += '</div>';
            collect += '<div>';
            collect += '<span id="email">' + user.email + '</span> ';
            collect += '</div>';
            collect += '<div>';
            collect += '<span id="last_login">'  + user.last_login + '</span> ';
            collect += '<span id="date_joined">' + user.date_joined + '</span>';
            collect += '</div>';
            
            container.html(collect);
        }
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_user",
                                 "params" : '['+user_id+']'
                                 },
                                 get_user_callback);

    });
}