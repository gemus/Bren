jQuery.fn.userScroller = function() {

    var search_box_focus = function() {

    }

    // Create a user picker
    return this.each(function() {
        var search_default = "Search Users";

        $(this).html("<h2>Loading Users...</h2>");
        $(this).before('<div>'+
                        '<input class="empty_search" type="text" value="'+search_default+'" id="userScroller_searchBox">'+
                        '</div>');

        // Clear Search Box When Focused
        $("#userScroller_searchBox").focus(function() {
            if (this.value == search_default) {
                this.value = "";
                $(this).removeClass("empty_search");
            }
        });

    });
}


/*var search_callback = function(result, status) {
    var result = result.result;

    var collect = "";
    for (i in result) {
        console.log(result[i]['display_name']);
    }
}


var params = '[""]';
$.getJSON("/json_api/", {"id": 1,
                         "method": "get_users",
                         "params" : params
                         },
                         search_callback);
                         */