jQuery.fn.userManager = function(user_name) {
    // If we need options. http://docs.jquery.com/Plugins/Authoring#Options

    // Initalize the userManager
    return this.each(function() {
        // Setup the HTML
        $(this).html('<div style="border: 1px solid #F00;" id="basic_details"></div>');
        // Create the manager to get the ball rolling
        new TopManager(user_name).init();
    });
}

// ==============================================
// = TopManager - Used to coordinate everything =
// ==============================================
TopManager = function(user_name) {
    var self = this;
    this.user_name = user_name;

    // The different sections
    this.userDetailManager = new UserDetailManager(this, 'basic_details');
}

TopManager.prototype.init = function() {
    this.userDetailManager.init();
}

TopManager.prototype.notify_change = function(section) {
    // When user details are updated
    if (section == this.userDetailManager.notify_name) {
        // Update the scroller
        var name_tag = this.userDetailManager.user_obj['first_name'] + " " +
                            this.userDetailManager.user_obj['last_name'];
        $('#'+this.user_name+'').html(name_tag);
    }
}

// ===============================================================
// = UserDetailManager - Manage basic user details (name, email) =
// ===============================================================
UserDetailManager = function(manager, canvas_id) {
    this.notify_name = "user_details"; // Used when notifying others of changes
    this.manager = manager;
    this.canvas_id = canvas_id;
    this.user_obj;
}

UserDetailManager.prototype.getItem = function(selector_text) {
    // Return #basic_details selector_text
    // So sub methods don't have to worry about name conflicts or grabbing wrong elemnts
    return $('#'+this.canvas_id + " " + (selector_text == undefined ? "" : selector_text));
}

UserDetailManager.prototype.init = function() {
    var self = this;
    // Pull in needed data
    $.getJSON("/json_api/", {"id": 1,
                             "method": "get_user",
                             "params" : JSON.stringify([this.manager.user_name])
                             },
                             function(result, status) {
                                  self.user_obj = result.result;
                                  self.draw_view();
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
                          '<a href="javascript:void(0);" id="edit_button">Edit</a>' +
                      '</div>';
    this.getItem().html(view_canvas);
    this.getItem("#edit_button").click(function(){ self.draw_edit(); });
}

UserDetailManager.prototype.draw_edit = function() {
    var self = this;
    var edit_canvas = '<div id="edit_canvas">' +
                          '<div class="name_plate_edit">'+
                              '<input type="text" id="first_name" value="' + this.user_obj['first_name'] + '"> '+
                              '<input type="text" id="last_name" value="'  + this.user_obj['last_name']  + '"> '+
                          '</div>'+
                          '<div id="name_plate_error" class="error_plate" style="display: none;"></div>'+

                          '<div class="email_plate_edit">'+
                              '<input type="text" id="email" value="'  + this.user_obj['email']  + '" style="width: 175px;"> '+
                          '</div>'+
                          '<div id="email_plate_error" class="error_plate" style="display: none;"></div>'+
                      '</div>' +
                      '<div id="edit_actions">'+
                          '<a href="javascript:void(0);" id="save_button">Save</a> ' +
                          '<a href="javascript:void(0);" id="cancel_button">Cancel</a>' +
                      '</div>';

    this.getItem().html(edit_canvas);
    this.getItem("#cancel_button").click(function(){ self.draw_view(); });
    this.getItem("#save_button").click(function(){ self.validate_and_save(); });
}

UserDetailManager.prototype.validate_and_save = function() {
    var self = this;
    var validate_email_address = function(email_addy) {
        var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
        return reg.test(email_addy);
    }

    var errors = new Array();
    var first_name_val = this.getItem("input#first_name").val();
    var last_name_val  = this.getItem("input#last_name").val();
    var email_val      = this.getItem("input#email").val();

    // Do some validation
    if (first_name_val == '') errors.push(['name', 'First Name']);
    if (last_name_val  == '') errors.push(['name', 'Last Name']);
    if (!validate_email_address(email_val) && email_val.length > 0 ) {
        errors.push(['email','Invalid Email']);
    }

    // No Errors so save the user
    if (errors.length == 0) {
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "update_user",
                                 "params" : JSON.stringify([{'user_name': this.manager.user_name,
                                              'first_name': first_name_val,
                                              'last_name' : last_name_val,
                                              'email'     : email_val
                                             }])
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
        var name_errors = new Array();
        var email_errors = new Array();
        for (i in errors) {
            if (errors[i][0] == 'name') name_errors.push(errors[i][1]);
            if (errors[i][0] == 'email') email_errors.push(errors[i][1]);
        }

        if (name_errors.length > 0) {
            this.getItem("#name_plate_error").slideDown();
            this.getItem("#name_plate_error").html(name_errors.join(", ") + " Is Required");
        }
        if (email_errors.length > 0) {
            this.getItem("#email_plate_error").slideDown();
            this.getItem("#email_plate_error").html("Invalid Email");
        }
    }
}