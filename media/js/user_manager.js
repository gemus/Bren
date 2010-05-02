// ===================================================================
// = Lets get the ball rolling by applying all the love we just made =
// ===================================================================
jQuery.fn.userManager = function(user_name) {
    // If we need options. http://docs.jquery.com/Plugins/Authoring#Options

    // Initalize the userManager
    return this.each(function() {
        // Setup the HTML
        $(this).html('<div id="basic_details"></div>'+
                     '<div id="delete_user"></div>'+
                     '<div id="manage_pin"></div>'+
                     '<div style="clear: both; padding-top: 20px;" id="report_manager"></div>'+
                     '<div style="margin-top: 1em" id="recent_workouts"></div>'+
                     '<div style="width: 400px;"></div>');
        // Create the manager to get the ball rolling
        topManager = new TopManager(user_name, this);
    });
}

// ==============================================
// = TopManager - Used to coordinate everything =
// ==============================================
TopManager = function(user_name, dom_container) {
    var self = this;
    this.user_name = user_name;
    this.dom_container = dom_container;

    if (user_name == "_CREATE_USER") {
        this.createUserManager = new CreateUserManager(this, 'basic_details');
    } else {
        this.userDetailManager = new UserDetailManager(this, 'basic_details');
        this.deleteUserManager = new DeleteUserManager(this, 'delete_user');
        this.reportManager = new ReportManager(this, 'report_manager')
        this.recentWorkoutManager = new RecentWorkoutManager(this, 'recent_workouts')
    }
}

TopManager.prototype.notify_change = function(section) {
    // When user details are updated
    if (section == this.userDetailManager.notify_name) {
        // Update the scroller
        var name_tag = this.userDetailManager.user_obj['first_name'] + " " +
                            this.userDetailManager.user_obj['last_name'];
        $('#'+this.user_name+'').html(name_tag);
        this.reportManager.draw_view();
    } else if (section == this.deleteUserManager.notify_name) {
        $('#'+this.user_name+'').slideUp(); // Remove the user from the scroller
    }
}

TopManager.prototype.notify_load = function(section) {
    if (section == this.userDetailManager.notify_name) {
        this.reportManager.draw_view();
        this.deleteUserManager.draw_view();
    }
}

TopManager.prototype.hide_others = function(section) {
    $(this.dom_container).children(":not(#"+section+")").hide();
}

TopManager.prototype.show_all = function(section) {
    $(this.dom_container).children().show();
}

// =====================================================
// = BaseManager - Using some sexy OO style of coding. =
// =====================================================
function BaseManager(manager, canvas_id) {
    this.manager = manager;
    this.canvas_id = canvas_id;
}

BaseManager.prototype.getItem = function(selector_text) {
    // Return $("#basic_details selector_text")
    // So sub methods don't have to worry about name conflicts or grabbing wrong elemnts
    return $('#'+this.canvas_id + " " + (selector_text == undefined ? "" : selector_text));
}

function getUserEditForm(first_name_val, last_name_val, email_val, pin_example) {
    return '<div id="user_edit_canvas">' +
               '<div class="name_plate_edit">'+
                   '<input example_text="First Name" type="text" id="first_name" value="' + first_name_val + '" style="width: 150px;"> '+
                   '<input example_text="Last Name" type="text" id="last_name" value="'  + last_name_val  + '" style="width: 180px;"> '+
               '</div>'+
               '<div id="name_plate_error" class="error_plate" style="display: none;"></div>'+

               '<div class="email_plate_edit">'+
                   '<input example_text="Email Address" type="text" id="email" value="'  + email_val  + '" style="width: 250px;"> '+
               '</div>'+
               '<div id="email_plate_error" class="error_plate" style="display: none;"></div>'+

               '<div id="pin_edit_canvas">'+
                   '<input example_text="'+pin_example+'" type="text" id="pin_input" value="" style="width: 90px;"/>'+
               '</div>'+
               '<div id="pin_error" class="error_plate" style="display: none;"></div>'+
           '</div>';
}

function validate_pin(pin_val) {
    if (pin_val.length < 3) {
        return "PIN must be at least 3 digits";
    } else if (pin_val[0] == 0) {
        return "PIN can not start with '0'";
    } else if (!(/^[0-9]+$/).test(pin_val)) {
        return "PIN may only contain numbers";
    }
}

CreateUserManager.prototype = new BaseManager();
CreateUserManager.prototype.constructor = CreateUserManager;
CreateUserManager.prototype.parent = BaseManager.prototype;
function CreateUserManager(manager, canvas_id) {
    this.parent.constructor.call(this, manager, canvas_id);
    this.draw_form();
}
CreateUserManager.prototype.draw_form = function() {
    var self = this;
    var create_canvas = getUserEditForm("","","", "PIN #") +
                        '<div id="edit_actions">'+
                            '<a href="javascript:void(0);" id="save_button" class="button">Save</a> ' +
                            '<a href="javascript:void(0);" id="cancel_button" class="button">Cancel</a>' +
                        '</div>';
    this.getItem().hide();
    this.getItem().html(create_canvas);
    this.getItem().fadeIn();

    this.getItem("input").exampleInput({blurClass: 'blur'});
    this.getItem("#save_button").click(function(){ self.validate_and_save(); });
    this.getItem("#cancel_button").click(function(){
        // Grab the selected user and display them
        var user_name = $("div.user_button[is_selected=true]").attr('id');
        $(self.manager.dom_container).userManager(user_name);
    });
}

CreateUserManager.prototype.validate_and_save = function() {
    var self = this;

    this.getItem("input.blur").val(""); // Clear out the example texts

    var errors = new Array();
    var first_name_val = this.getItem("input#first_name").val();
    var last_name_val  = this.getItem("input#last_name").val();
    var email_val      = this.getItem("input#email").val();
    var pin_val        = this.getItem("input#pin_input").val();

    // Do some validation. Need all of these
    if (first_name_val == '') errors.push(['name', 'First Name']);
    if (last_name_val  == '') errors.push(['name', 'Last Name']);
    if (pin_val        == '') {
        errors.push(['pin',  'PIN Is Required']);
    } else if (pin_error = validate_pin(pin_val)) {
        errors.push(['pin', pin_error]);
    }

    // If we get an email, ensure that it is valid
    if (!validate_email_address(email_val) && email_val.length > 0 ) {
        errors.push(['email','Invalid Email Address']);
    }

    // No Errors so create the user
    if (errors.length == 0) {
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "create_user",
                                 "params" : JSON.stringify([{'first_name': first_name_val,
                                                             'last_name' : last_name_val,
                                                             'email'     : email_val,
                                                             'password'  : pin_val
                                                            }])
                                 },
                                 function(result, status) {
                                     var user_name = result.result;

                                     // Show the view screen for the user we just created
                                     self.getItem().parent().userManager(user_name);
                                 });

    // Validation Errors. Show the user the problems
    } else {
        // Clear out the old errors.
        this.getItem(".error_plate").hide();

        var name_errors  = new Array();
        var email_errors = new Array();
        var pin_errors   = new Array();
        for (i in errors) {
            if (errors[i][0] == 'name')  name_errors.push(errors[i][1]);
            if (errors[i][0] == 'email') email_errors.push(errors[i][1]);
            if (errors[i][0] == 'pin')   pin_errors.push(errors[i][1]);
        }

        if (name_errors.length > 0) {
            this.getItem("#name_plate_error").slideDown();
            this.getItem("#name_plate_error").html(name_errors.join(", ") + " Is Required");
        }
        if (email_errors.length > 0) {
            this.getItem("#email_plate_error").slideDown();
            this.getItem("#email_plate_error").html(email_errors[0]);
        }
        if (pin_errors.length > 0) {
            this.getItem("#pin_error").slideDown();
            this.getItem("#pin_error").html(pin_errors[0]);
        }

        // Re-add examples if needed
        this.getItem("input").exampleInput({blurClass: 'blur'});
    }
}

// ===============================================================
// = UserDetailManager - Manage basic user details (name, email) =
// ===============================================================
UserDetailManager.prototype = new BaseManager();
UserDetailManager.prototype.constructor = UserDetailManager;
UserDetailManager.prototype.parent = BaseManager.prototype;
function UserDetailManager(manager, canvas_id) {
    var self = this;
    this.parent.constructor.call(this, manager, canvas_id);

    this.notify_name = "user_details"; // Used when notifying others of changes
    this.user_obj; // For storing some hot user data pulled from the DB

    // Pull in needed data
    $.getJSON("/json_api/", {"id": 1,
                             "method": "get_user",
                             "params" : JSON.stringify([this.manager.user_name])
                             },
                             function(result, status) {
                                  self.user_obj = result.result;
                                  self.draw_view();
                                  self.manager.notify_load(self.notify_name);
                             });
}

UserDetailManager.prototype.draw_view = function() {
    var self = this;
    var view_canvas = '<div class="name_plate">' +
                          '<span>' + this.user_obj['first_name'] + '</span> '+
                          '<span>' + this.user_obj['last_name']  + '</span> '+
                      '</div>'+
                      '<div class="email_plate">'+
                          '<a href="mailto:'+ this.user_obj['email']+'">'+
                              this.user_obj['email'] +
                          '</a> '+
                      '</div>'+
                      '<div class="action_plate">'+
                          '<a href="javascript:void(0);" id="edit_button" class="button">Edit</a>' +
                      '</div>';
    this.getItem().hide();
    this.getItem().html(view_canvas);
    this.getItem().fadeIn();
    this.getItem("#edit_button").click(function(){ self.draw_edit(); });
    this.manager.show_all();
}

UserDetailManager.prototype.draw_edit = function() {
    var self = this;
    var edit_canvas = getUserEditForm(this.user_obj['first_name'],
                                      this.user_obj['last_name'],
                                      this.user_obj['email'],
                                      'Change Pin') +
                      '<div id="edit_actions">'+
                          '<a href="javascript:void(0);" id="save_button" class="button">Save</a>' +
                          '<a href="javascript:void(0);" id="cancel_button" class="button">Cancel</a>' +
                      '</div>';

    this.getItem().hide();
    this.getItem().html(edit_canvas);
    this.getItem().fadeIn();
    this.getItem("input").exampleInput({blurClass: 'blur'});
    this.getItem("#cancel_button").click(function(){ self.draw_view(); });
    this.getItem("#save_button").click(function(){ self.validate_and_save(); });
    this.manager.hide_others(this.canvas_id);
}

var validate_email_address = function(email_addy) {
    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    return reg.test(email_addy);
}

UserDetailManager.prototype.validate_and_save = function() {
    var self = this;

    this.getItem("input.blur").val(""); // Clear out the example texts

    var errors = new Array();
    var first_name_val = this.getItem("input#first_name").val();
    var last_name_val  = this.getItem("input#last_name").val();
    var email_val      = this.getItem("input#email").val();
    var pin_val        = this.getItem("input#pin_input").val();

    // Do some validation
    if (first_name_val == '') errors.push(['name', 'First Name']);
    if (last_name_val  == '') errors.push(['name', 'Last Name']);
    if (!validate_email_address(email_val) && email_val.length > 0 ) {
        errors.push(['email','Invalid Email Address']);
    }

    if (pin_val != '' && (pin_error = validate_pin(pin_val))) { // Only change PIN if it was set
        errors.push(['pin', pin_error]);
    }

    // No Errors so save the user
    if (errors.length == 0) {
        var data_to_send = {'user_name': this.manager.user_name,
                            'first_name': first_name_val,
                            'last_name' : last_name_val,
                            'email'     : email_val }

        if (pin_val != '') data_to_send['password'] = pin_val;

        $.getJSON("/json_api/", {"id": 1,
                                 "method": "update_user",
                                 "params" : JSON.stringify([data_to_send])
                                 },
                                 function(result, status) {
                                     // Update our user_obj to reflect the save
                                     self.user_obj['first_name'] = first_name_val;
                                     self.user_obj['last_name'] = last_name_val;
                                     self.user_obj['email'] = email_val;

                                     // Then draw the view screen
                                     self.draw_view();

                                     // Notify others of the change
                                     self.manager.notify_change(self.notify_name);
                                 });

    // Validation Errors. Show the user the problems
    } else {
        // Clear out the old errors.
        this.getItem(".error_plate").hide();

        var name_errors = new Array();
        var email_errors = new Array();
        var pin_errors = new Array();
        for (i in errors) {
            if (errors[i][0] == 'name') name_errors.push(errors[i][1]);
            if (errors[i][0] == 'email') email_errors.push(errors[i][1]);
            if (errors[i][0] == 'pin') pin_errors.push(errors[i][1]);
        }

        if (name_errors.length > 0) {
            this.getItem("#name_plate_error").slideDown();
            this.getItem("#name_plate_error").html(name_errors.join(", ") + " Is Required");
        }
        if (email_errors.length > 0) {
            this.getItem("#email_plate_error").slideDown();
            this.getItem("#email_plate_error").html(email_errors[0]);
        }
        if (pin_errors.length > 0) {
            this.getItem("#pin_error").slideDown();
            this.getItem("#pin_error").html(pin_errors[0]);
        }
    }
}

// ================================================
// = DeleteUserManager - Ability to Delete A user =
// ================================================
DeleteUserManager.prototype = new BaseManager();
DeleteUserManager.prototype.constructor = DeleteUserManager;
DeleteUserManager.prototype.parent = BaseManager.prototype;
function DeleteUserManager(manager, canvas_id) {
    this.parent.constructor.call(this, manager, canvas_id);
    this.notify_name = "delete_user"; // Used when notifying others of changes

    // Wait for the user manager to call us to load. Saves 'flickering' on the screen.
}
DeleteUserManager.prototype.draw_view = function() {
    var self = this;
    this.getItem().hide();
    this.getItem().html('<a href="javascript:void(0);" id="delete_user_button" class="button">Delete</a>');
    this.getItem().fadeIn();
    this.getItem("#delete_user_button").click(function(){
        if (confirm("Really Delete This User?")) self.delete_user();
    });
}
DeleteUserManager.prototype.draw_delete_confirm = function() {
    this.getItem().parent().html("<strong>User Deleted</strong>");
}
DeleteUserManager.prototype.delete_user = function() {
    var self = this;

    console.log(JSON.stringify([{'user_name': this.manager.user_name}]))

    $.getJSON("/json_api/", {"id": 1,
                             "method": "delete_user",
                             "params" : JSON.stringify([{'user_name': this.manager.user_name}])
                             },
                             function(result, status) {
                                 // Then draw the confirm screen for feedback
                                 self.draw_delete_confirm();

                                 // Notify others of the change
                                 self.manager.notify_change(self.notify_name);
                             });
}

// ============================================================
// = ReportManager - Manage reports for users : Email reports =
// ============================================================
ReportManager.prototype = new BaseManager();
ReportManager.prototype.constructor = ReportManager;
ReportManager.prototype.parent = BaseManager.prototype;
function ReportManager(manager, canvas_id) {
    this.parent.constructor.call(this, manager, canvas_id);
    this.notify_name = "report_manager"; // Used when notifying others of changes

    // Do not load yourself. Have to wait for the UserManager to finish loading
}
ReportManager.prototype.draw_view = function() {
    this.getItem().hide();
    this.getItem().html('<h2>Weekly Report Sender</h2>'+
                        '<div id="reports_status"></div>');
    this.getItem().fadeIn();
    this.get_permission();
}
ReportManager.prototype.get_permission = function() {
    var self = this;
    $.getJSON("/json_api/", {"id": 1,
                             "method": "has_email_permission",
                             "params" : JSON.stringify([{'user_name': this.manager.user_name}])
                             },
                             function(result, status) {
                                 if (result.result) {
                                     self.draw_has_permission();
                                 } else if (self.manager.userDetailManager.user_obj['email'] == ''){
                                     self.draw_no_email();
                                 } else {
                                     self.draw_no_permission();
                                 }
                             });
}
ReportManager.prototype.draw_no_email = function() {
    var first_name = this.manager.userDetailManager.user_obj['first_name'];
    this.getItem("#reports_status").html("<div>Can not send reports. "+first_name+" does not have an email address.");
}
ReportManager.prototype.draw_has_permission = function() {
    var self = this;
    var first_name = this.manager.userDetailManager.user_obj['first_name'];
    this.getItem("#reports_status").html('<span>Yes, weekly reports are being sent.</span><br>'+
                                         '<div id="permission_action_bar">'+
                                         '<a href="javascript:void(0);" id="unsubscribe_perm_request_button">Unsubscribe '+first_name+'</a>'+
                                         '</div>');
    this.getItem("#unsubscribe_perm_request_button").click(function() {
        if (confirm("Really stop sending reports to "+first_name+"?")) self.remove_permission_request();
    });
}
ReportManager.prototype.draw_no_permission = function() {
    var self = this;
    this.getItem("#reports_status").html('<span>No, reports are not being sent.</span><br>'+
                                         '<div id="permission_action_bar">'+
                                         '<a href="javascript:void(0);" id="send_perm_request_button">Ask To Send Reports</a>'+
                                         '</div>');
    this.getItem("#send_perm_request_button").click(function() {
        self.send_permission_request();
    });
}
ReportManager.prototype.send_permission_request = function() {
    var self = this;
    this.getItem("div#reports_status").html('<span>Sending Permission Request...</span>');
    $.getJSON("/json_api/", {"id": 1,
                             "method": "send_permission_request",
                             "params" : JSON.stringify([{'user_name': this.manager.user_name}])
                             },
                             function(result, status) {
                                 self.draw_sent_success();
                             });
}
ReportManager.prototype.draw_sent_success = function() {
    var first_name = this.manager.userDetailManager.user_obj['first_name'];
    this.getItem("div#reports_status").html('<span>Sent. '+first_name+' will receive a confirmation email.</span>');
}
ReportManager.prototype.remove_permission_request = function() {
    var self = this;
    $.getJSON("/json_api/", {"id": 1,
                             "method": "remove_permission_request",
                             "params" : JSON.stringify([{'user_name': this.manager.user_name}])
                             },
                             function(result, status) {
                                 console.log(result);
                                 self.draw_remove_success();
                             });

}
ReportManager.prototype.draw_remove_success = function() {
    this.getItem("div#reports_status").html('<span>Reports Will No Longer Be Sent</span>');
}

function date_to_str(date) {
    return [date.getFullYear(), date.getMonth()+1, date.getDate()].join('-');
}

// ============================================================
// = RecentWorkoutManager - Show recent workouts for the user =
// ============================================================
RecentWorkoutManager.prototype = new BaseManager();
RecentWorkoutManager.prototype.constructor = RecentWorkoutManager;
RecentWorkoutManager.prototype.parent = BaseManager.prototype;
function RecentWorkoutManager(manager, canvas_id) {
    this.parent.constructor.call(this, manager, canvas_id);
    this.notify_name = "recent_workout"; // Used when notifying others of changes

    this.draw_view();
}
RecentWorkoutManager.prototype.draw_view = function() {
    var self = this;

    var now = new Date();
    var end_date = date_to_str(now);
    now.setDate(now.getDate()-7);
    var start_date = date_to_str(now);

    var set_workout_url = function() {
        var start_date = self.getItem('input#start_date_picker').val();
        var end_date   = self.getItem('input#end_date_picker').val();

        var iframe_url = "/reports/"+self.manager.user_name+
                         "/completed_workouts/?start_date="+start_date+
                         "&end_date="+end_date;
        self.getItem('iframe#recent_workout_iframe').attr('src', iframe_url);
    }

    this.getItem().hide();
    this.getItem().html('<h2>Recent Workouts</h2>'+
                        '<div id="reports_action_bar">'+
                        '<label>Start Date</label>'+
                        '<input id="start_date_picker" type="text" value="'+start_date+'">' +
                        '<label style="margin-left: 1em;">End Date</label>'+
                        '<input id="end_date_picker" type="text" value="'+end_date+'">' +
                        '</div>'+
                        '<iframe width="600" height="300" id="recent_workout_iframe">'+
                        '  <p>Your browser does not support iframes.</p>'+
                        '</iframe>');
    set_workout_url();
    this.getItem().fadeIn();
    this.getItem("input").datepicker({ dateFormat: 'yy-mm-dd' });
    this.getItem("input").change(set_workout_url);
}
