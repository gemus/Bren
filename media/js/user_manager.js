// ===================================================================
// = Lets get the ball rolling by applying all the love we just made =
// ===================================================================
jQuery.fn.userManager = function(user_name) {
    // If we need options. http://docs.jquery.com/Plugins/Authoring#Options

    // Initalize the userManager
    return this.each(function() {
        // Setup the HTML
        $(this).html('<div id="basic_details"></div>'+
                     '<div id="manage_pin"></div>');
        // Create the manager to get the ball rolling
        new TopManager(user_name);
    });
}

// ==============================================
// = TopManager - Used to coordinate everything =
// ==============================================
TopManager = function(user_name) {
    var self = this;
    this.user_name = user_name;

    if (user_name == "_CREATE_USER") {
        this.createUserManager = new CreateUserManager(this, 'basic_details');
    } else {
        this.userDetailManager = new UserDetailManager(this, 'basic_details');
        this.userPinManager = new UserPinManager(this, 'manage_pin');
    }
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

// =====================================================
// = BaseManager - Using some sexy OO style of coding. =
// =====================================================
function BaseManager(manager, canvas_id) {
    this.manager = manager;
    this.canvas_id = canvas_id;
}

BaseManager.prototype.getItem = function(selector_text) {
    // Return #basic_details selector_text
    // So sub methods don't have to worry about name conflicts or grabbing wrong elemnts
    return $('#'+this.canvas_id + " " + (selector_text == undefined ? "" : selector_text));
}

function getUserEditForm(first_name_val, last_name_val, email_val) {
    return '<div id="user_edit_canvas">' +
               '<div class="name_plate_edit">'+
                   '<input example_text="First Name" type="text" id="first_name" value="' + first_name_val + '"> '+
                   '<input example_text="Last Name" type="text" id="last_name" value="'  + last_name_val  + '"> '+
               '</div>'+
               '<div id="name_plate_error" class="error_plate" style="display: none;"></div>'+

               '<div class="email_plate_edit">'+
                   '<input example_text="Email Address" type="text" id="email" value="'  + email_val  + '" style="width: 175px;"> '+
               '</div>'+
               '<div id="email_plate_error" class="error_plate" style="display: none;"></div>'+
           '</div>';
}

function getPinEditForm() {
    return '<div id="pin_edit_canvas">'+
               '<input example_text="PIN #" type="text" id="pin_input" value=""/>'+
               '<div id="pin_error" class="error_plate" style="display: none;"></div>'+
           '</div>';
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
    var create_canvas = getUserEditForm("","","") +
                        getPinEditForm() +
                        '<div id="edit_actions">'+
                            '<a href="javascript:void(0);" id="save_button">Save</a> ' +
                        '</div>';
    this.getItem().html(create_canvas);

    this.getItem("input").exampleInput({blurClass: 'blur'});
    this.getItem("#save_button").click(function(){ self.validate_and_save(); });
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
                                                             'pin'       : pin_val
                                                            }])
                                 },
                                 function(result, status) {
                                     console.log(result);

                                     //// Update our user_obj to reflect the save
                                     //self.user_obj['first_name'] = first_name_val;
                                     //self.user_obj['last_name'] = last_name_val;
                                     //self.user_obj['email'] = email_val;
                                     //
                                     //// Then draw the view screen
                                     //self.draw_view();
                                     //
                                     //// Notify others of the change
                                     //self.manager.notify_change(self.notify_name);
                                 });

    // Validation Errors. Show the user the problems
    } else {
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
    var edit_canvas = getUserEditForm(this.user_obj['first_name'],
                                      this.user_obj['last_name'],
                                      this.user_obj['email']) +
                      '<div id="edit_actions">'+
                          '<a href="javascript:void(0);" id="save_button">Save</a> ' +
                          '<a href="javascript:void(0);" id="cancel_button">Cancel</a>' +
                      '</div>';

    this.getItem().html(edit_canvas);
    this.getItem("input").exampleInput({blurClass: 'blur'});
    this.getItem("#cancel_button").click(function(){ self.draw_view(); });
    this.getItem("#save_button").click(function(){ self.validate_and_save(); });
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

    // Do some validation
    if (first_name_val == '') errors.push(['name', 'First Name']);
    if (last_name_val  == '') errors.push(['name', 'Last Name']);
    if (!validate_email_address(email_val) && email_val.length > 0 ) {
        errors.push(['email','Invalid Email Address']);
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
            this.getItem("#email_plate_error").html(email_errors[0]);
        }
    }
}

// ===============================================================
// = UserDetailManager - Manage basic user details (name, email) =
// ===============================================================
UserPinManager.prototype = new BaseManager();
UserPinManager.prototype.constructor = UserPinManager;
UserPinManager.prototype.parent = BaseManager.prototype;
function UserPinManager(manager, canvas_id) {
    this.parent.constructor.call(this, manager, canvas_id);
    this.notify_name = "user_pin"; // Used when notifying others of changes
    this.draw_view();
}
UserPinManager.prototype.draw_view = function() {
    var self = this;
    this.getItem().html('<a href="javascript:void(0);" id="change_pin_button">Change Pin</a>');
    this.getItem("#change_pin_button").click(function(){ self.draw_edit(); });
}
UserPinManager.prototype.draw_edit = function() {
    var self = this;
    this.getItem().html(getPinEditForm() +
                        '<div id="edit_actions">'+
                            '<a href="javascript:void(0);" id="save_button">Save</a> ' +
                            '<a href="javascript:void(0);" id="cancel_button">Cancel</a>' +
                        '</div>');

    this.getItem("#cancel_button").click(function(){ self.draw_view(); });
    this.getItem("#save_button").click(function(){ self.validate_and_save(); });
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

UserPinManager.prototype.validate_and_save = function() {
    var self = this;
    var pin_val = this.getItem("input#pin_input").val();

    var error = validate_pin(pin_val);

    // No Errors so save the user
    if (error == undefined) {
        $.getJSON("/json_api/", {"id": 1,
                                 "method": "update_user",
                                 "params" : JSON.stringify([{'user_name': this.manager.user_name,
                                                             'password': pin_val }])
                                 },
                                 function(result, status) {
                                     // Then draw the view screen
                                     self.draw_view();

                                     // Notify others of the change
                                     self.manager.notify_change(self.notify_name);
                                 });

    // Validation Errors. Show the user the problems
    } else {
        this.getItem("#pin_error").slideDown();
        this.getItem("#pin_error").html(error);
    }
}
