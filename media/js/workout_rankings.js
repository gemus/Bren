jQuery.fn.rankingManager = function(user_name) {

    // Initalize the userManager
    return this.each(function() {
        // Setup the HTML
        $(this).html('<div id="rankings_actions">'+
         			 '  <label for="attendance_date">Date</label><input type="text" name="attendance_date" value="" id="attendance_date">'+
         			 '  <label for="attendance_workout">Workout</label>'+
         			 '  <select name="attendance_workout" id="attendance_workout">'+
         			 '  </select>'+
         			 '  <div id="ranking_iframe_container">'+
         			 '      <iframe src="http://localhost:8000/reports/ranking/?workout_id=10&date=2010-01-29"></iframe>'+
         			 '  </div>'+
         			 '</div>');
        
        var today_date = date_to_str(new Date());

        $("input#attendance_date").datepicker({ dateFormat: 'yy-mm-dd' });
        $("input#attendance_date").change(function() {
            console.log('change');
        });
        $("input#attendance_date").val(today_date);
        $("input#attendance_date").change();
    });
}
