jQuery.fn.userScroller = function() {

    var performSearch = function(search_term) {
        var search_callback = function(result, status) {
            var user_results = result.result;
            var collect = "";
            for (var i=0; i<user_results.length; i++) {
                if (user_results[i]['display_name'] == " ") continue; // Skip users with no display name (admin people)
                collect += '<div class="user_button" id="'+user_results[i]['user_name']+'">'+
                                user_results[i]['display_name']+
                           '</div>';
            }
            $("#userScrollerCanvas").html(collect);
        }

        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_users",
                                 "params" : '["'+search_term+'", -1]'
                                 },
                                 search_callback);
    }

    // Create a user picker
    return this.each(function() {
        var search_default = "Search Users";

        $(this).html("");
        $(this).html('<div>'+
                       '<input class="empty_search" type="text" value="'+search_default+'" id="userScroller_searchBox">'+
                     '</div>'+
                     '<div id="userScrollerCanvas">Loading Users...</div>');

        // Start By Showing Everyone
        performSearch("");

        // Clear Search Box When Focused
        $("#userScroller_searchBox").focus(function() {
            if (this.value == search_default) {
                this.value = "";
                $(this).removeClass("empty_search");
            }
        });
        // Search when typing in the search box
        $("#userScroller_searchBox").keyup(function() {
            performSearch(this.value);
        });
    });
}