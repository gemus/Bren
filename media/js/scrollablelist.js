function styleToInt(el, style) {
	// Grab the style which is a string
	var theTop = el.getStyle(style);

	if (theTop == 'auto') return 0;

	// Chop the negative sign, and the 'px'
	return parseInt(theTop.substr(0, theTop.length-2));
}

//  __  __                  ___ _                 __  __
// |  \/  | ___ _ __  _   _|_ _| |_ ___ _ __ ___ |  \/  | __ _ _ __   __ _  __ _  ___ _ __
// | |\/| |/ _ \ '_ \| | | || || __/ _ \ '_ ` _ \| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
// | |  | |  __/ | | | |_| || || ||  __/ | | | | | |  | | (_| | | | | (_| | (_| |  __/ |
// |_|  |_|\___|_| |_|\__,_|___|\__\___|_| |_| |_|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
//                                                                         |___/
ScrollableListManager = function(scrollingDOMID, canvasDOMID) {
    this.scrollManager = new ScrollManager(scrollingDOMID, canvasDOMID);
    this.scrollingDOMID = scrollingDOMID;
}

ScrollableListManager.prototype.init = function() {
    this.redraw();
}

ScrollableListManager.prototype.redraw = function() {
	var callback = {
		success: this.menuItemCallBack,
		failure: this.menuItemCallBack_error,
		scope: this
	}

	var url = "/json_api/?id=1&method=get_all_users&params=null";

	YAHOO.util.Connect.asyncRequest('GET', url, callback, null);
}
ScrollableListManager.prototype.menuItemCallBack = function(o) {
	var data = YAHOO.lang.JSON.parse(o.responseText).result;
	this.drawMenuItems(data);
}
ScrollableListManager.prototype.menuItemCallBack_error = function(o) {
	alert("Error getting Items");
}
ScrollableListManager.prototype.drawMenuItems = function(data) {
	var letters = ["A","B","C","D","E","F","G","H","I","J","K",
					"L","M","N","O","P","Q","R","S","T","U",
					"V","W","X","Y","Z"]

	var collect = "";
	var menu_item_pos = 0;
	for (var i in letters) {
	    if (data[menu_item_pos] != null && data[menu_item_pos]['display_name'][0].toUpperCase() == letters[i]) {
    	    collect += "<dt>" + letters[i] + "</dt>\n";
		}
		while (menu_item_pos < data.length
							&& data[menu_item_pos]['display_name'][0].toUpperCase() == letters[i]) {
			collect += "<dd id=\"" + data[menu_item_pos]['user_name'] + "\">" + data[menu_item_pos]['display_name'] + "</dd>";
			menu_item_pos++;
		}
	}

	if (data.length == 0 ) {
        collect = "<div class=\"noItems\">No Items Found, Sorry</div>";
    }

	var toWriteTo = document.getElementById(this.scrollingDOMID);
	toWriteTo.innerHTML = collect;
	this.scrollManager.init();

    // Hook up the mouse click events
	var dds = this.scrollManager.scrollingrEl.getElementsByTagName('dd');
	for (var i=0; i<dds.length; i++) {
	    var data = {'self': this, 'id': dds[i].id, 'display_name': dds[i].innerHTML};
		new YAHOO.util.Element(dds[i]).addListener('mouseup', this.clickMenuItem, data);
	}
}

ScrollableListManager.prototype.clickMenuItem = function(evnt, data) {
    if (!data['self'].scrollManager.isDragging) {
        data['self'].pickItem(data['id'], data['display_name']);
    }
}

ScrollableListManager.prototype.pickItem = function(itemID, display_name) {
    var nodeApply = function(n) {
        // Lets do some fade action here :-)
        if (n.id == itemID) {
            var myAnim = new YAHOO.util.ColorAnim(n, {backgroundColor: { to: '#3C5F7F' }, color: { to: '#FFFFFF'}});
            myAnim.duration = 0.5;
            myAnim.animate();
            n.HAS_STYLE = true;
        } else if (n.HAS_STYLE) { // Only need to animate one of them back to normal state
            var myAnim = new YAHOO.util.ColorAnim(n, {backgroundColor: { to: '#FFFFFF' }, color: { to: '#1C3451'}});
            myAnim.duration = 0.25;
            myAnim.animate();
            n.HAS_STYLE = false;
        }
    }
    YAHOO.util.Dom.getElementsBy(function(n) {return true}, "dd", this.scrollingDOMID, nodeApply);

    // Fill in user username stuff
    $("#id_username").val(itemID);
    $("#id_password").val("");

    $("#name_plate").html(display_name);
}


//  ____                 _ _ __  __
// / ___|  ___ _ __ ___ | | |  \/  | __ _ _ __   __ _  __ _  ___ _ __
// \___ \ / __| '__/ _ \| | | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
//  ___) | (__| | | (_) | | | |  | | (_| | | | | (_| | (_| |  __/ |
// |____/ \___|_|  \___/|_|_|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
//                                                    |___/

/*
    TODO : Calc dragging velocity at intervals instead of over who drag event
*/

ScrollManager = function (scrollingDOMID, canvasDOMID) {
	this.scrollingDOMID = scrollingDOMID;
	this.canvasDOMID = canvasDOMID;
	this.isDragging = false;

	this.startScrollPos;
	this.startScrollTime;
}

ScrollManager.prototype.init = function() {
	this.scrollingrEl = new YAHOO.util.Element(this.scrollingDOMID);
	this.scrollingDD = new YAHOO.util.DD(this.scrollingDOMID);
	this.canvasEl = new YAHOO.util.Element(this.canvasDOMID);

	// Needed for on dragging events
	this.scrollingDD.scrollManager = this;

	// Only drag in Y-axis
	this.scrollingDD.setXConstraint(0, 0);

	this.scrollingDD.on('dragEvent', this.onDragging, this, true);
	this.scrollingDD.on('endDragEvent', this.onEndDragging, this, true);
	this.scrollingDD.on('startDragEvent', this.onStartDragging, this, true);

	this.scrollingrEl.on('mousedown', this.stopScrollingAnimation, this, true);

    // Rest the list to start at the top
	this.resetPosition();
}

ScrollManager.prototype.onDragging = function(ev) {
	//console.log("dragging!");
}

ScrollManager.prototype.onStartDragging = function(ev) {
	this.isDragging = true;
	this.startScrollPos = styleToInt(this.scrollingrEl, 'top');
	this.startScrollTime = new Date().getTime();

}

ScrollManager.prototype.onEndDragging = function(ev) {
	this.isDragging = false;

	var posDiff = this.startScrollPos - styleToInt(this.scrollingrEl, 'top');
	var timeDiff = new Date().getTime() - this.startScrollTime;

	this.animateList(posDiff, timeDiff);
}

ScrollManager.prototype.animateList = function(posDiff, timeDiff) {
	var deAcel = 3000; //px/sec/sec
	var velocity = posDiff/timeDiff * 1000; // px / sec
	var timeToStop = Math.abs(velocity/deAcel); // sec
	var distanceToMove = timeToStop * velocity * -1; // px

	// Don't let it scroll past the top or bottom
	var attributes;
	var currentTop = styleToInt(this.scrollingrEl, 'top');
	var scrollerHeight = styleToInt(this.scrollingrEl, 'height');
	var canvasHeight = styleToInt(this.canvasEl, 'height');
	if ( currentTop + distanceToMove > 0 ) {
		attributes = {
		   top: { to: 0 }
		};
	} else if (Math.abs(currentTop + distanceToMove) > scrollerHeight - canvasHeight) {
		attributes = {
		   top: { to: scrollerHeight*-1 + canvasHeight }
		};
	} else {
		attributes = {
		   top: { by: distanceToMove }
		};
	}

	this.scrollAnimation = new YAHOO.util.Anim(this.scrollingDOMID, attributes);
	this.scrollAnimation.method = YAHOO.util.Easing.easeOut;
	this.scrollAnimation.duration = timeToStop;
	this.scrollAnimation.animate();
}

ScrollManager.prototype.stopScrollingAnimation = function(ev) {
	this.scrollAnimation.stop(false);
}

ScrollManager.prototype.resetPosition = function() {
    this.scrollingrEl.setStyle('top', 0);
}

// ==============================================
// = OLD Basic Login Username Code using JQuery =
// ==============================================

/*	$.getJSON("/json_api/", {"id": 1, "method": "get_all_users", "params" : []}, function(result, status) {
		var result = result.result;

		var user_picker_html = "<dl><dd>Select User</dd>";
		for (i in result) {
			user_picker_html += "<dt><a href='javascript:void(0);' onclick='populate_user_field(\""+result[i]['user_name']+"\")'>" + result[i]['display_name'] + "</a></dt>";
		}
		user_picker_html += "</dl>";

		$("#user_picker").html(user_picker_html);

	});

	var populate_user_field = function(user_name) {
		$("#id_username").val(user_name);
	}

	$(document).ready(function() {
		$("#id_password").numPadInput(false, "");
	});
*/