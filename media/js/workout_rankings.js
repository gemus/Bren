jQuery.fn.rankingManager = function(user_name) {
    function set_iframe_url() {
        var workout_id = $("select#attendance_workout").val();
        var workout_date = $("input#attendance_date").val();

        if (workout_id == -1) {
            $("iframe#ranking_iframe").hide();
            $("div#ranking_none_found").show();
        } else {
            var report_url = '/reports/ranking/?workout_id='+workout_id+'&date='+workout_date;
            $("iframe#ranking_iframe").show();
            $("div#ranking_none_found").hide();
        }

        $("iframe#ranking_iframe").attr('src', report_url);
    }

    // Initalize the userManager
    return this.each(function() {
        // Setup the HTML
        $(this).html('<div id="rankings_actions">'+
         			 '  <label for="attendance_date">Date</label><input type="text" name="attendance_date" value="" id="attendance_date">'+
         			 '  <label for="attendance_workout">Workout</label>'+
         			 '  <select name="attendance_workout" id="attendance_workout">'+
         			 '  </select>'+
         			 '  <div id="ranking_iframe_container">'+
         			 '      <iframe id="ranking_iframe"></iframe>'+
         			 '  </div>'+
         			 '  <div id="ranking_none_found" style="margin: 20px; display: none;">'+
         			 '    <p>No Workouts Found On Selected Date</p>'+
         			 '  </div>'+
         			 '</div>');

        var today_date = date_to_str(new Date());

        $("input#attendance_date").datepicker({ dateFormat: 'yy-mm-dd' });
        $("input#attendance_date").change(function() {
            function find_workout_callback(result, status) {
                result = result.result;
                var collect = "";
                for (var i in result) {
                    collect += '<option value="'+result[i]['workout_id']+'">'+result[i]['workout_name']+'</option>';
                }
                if (collect == "") {
                    collect = '<option value="-1">No Workouts Found On Selected Date</option>';
                }

                $("select#attendance_workout").html(collect);
                $("iframe#ranking_iframe").attr('src', $("select#attendance_workout").val());
                set_iframe_url();
            }

            var params = JSON.stringify([$("input#attendance_date").val()]);
            $.getJSON("/json_api/", {"id": 1,
                                     "method": "get_workouts",
                                     "params" : params,
                                     },
                                     find_workout_callback)
        });
        $("input#attendance_date").val(today_date);
        $("input#attendance_date").change();
        $("select#attendance_workout").change(set_iframe_url);
    });
}
