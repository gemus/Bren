var search_callback = function(result, status) {
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