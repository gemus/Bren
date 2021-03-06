jQuery.fn.userScroller = function(viewer_container_id) {
    // Where to tie the userManager to when a user item is clicked
    var viewer_container_id = viewer_container_id;

    var user_click = function() {
        $("#"+viewer_container_id+"").userManager(this.id);
        $("div#userScrollerCanvas div.user_button").removeAttr('is_selected');
        $(this).attr({'is_selected':'true'});
    }

    var performSearch = function(search_term, done_loading_callback) {
        var search_callback = function(result, status) {
            var user_results = result.result;
            var collect = "";
            for (var i=0; i<user_results.length; i++) {
                if (user_results[i]['display_name'] == " ") continue; // Skip users with no display name (admin people)
                collect += '<div class="user_button" id="'+user_results[i]['user_name']+'">'+
                                user_results[i]['display_name']+
                           '</div>';
            }
            if (user_results.length == 0) {
                collect = '<div class="no_results">We did not find results for: <strong>'+search_term+'</strong></div>';
            }
            $("#userScrollerCanvas").html(collect);
            $("#userScrollerCanvas div").click(user_click);

            if (done_loading_callback != undefined) done_loading_callback();
        }

        $.getJSON("/json_api/", {"id": 1,
                                 "method": "get_users",
                                 "params" : JSON.stringify([search_term, -1])
                                 },
                                 search_callback);
    }

    // Create a user picker
    return this.each(function() {
        $(this).html('<div>'+
                       '<input example_text="Search Users" type="text" value="" id="userScroller_searchBox">'+
                     '</div>'+
                     '<div id="userScrollerCanvas">Loading Users...</div>');

        // After scroller has loaded, 'click' the first person on the list
        var done_loading_callback = function() {
            $("div#userScrollerCanvas div.user_button:first").click();
        }
        // Start By Showing Everyone
        performSearch("", done_loading_callback);

        $("input#userScroller_searchBox").exampleInput({blurClass: 'blur'});

        // Search when typing in the search box
        $("#userScroller_searchBox").keyup(function() {
            performSearch(this.value);
        });
    });
}