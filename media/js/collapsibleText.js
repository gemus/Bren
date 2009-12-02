if (document.getElementById) {
  document.write('<style type="text/css">.texter {display:none;}</style>') }


function expand(classname, theID) {
	var elements = document.getElementsByClassName(classname);
	for (var i=0; i < elements.length; i++) {
		if (elements[i].id == theID) {
			if (elements[i].style.display == "block") elements[i].style.display = "none";
			else elements[i].style.display = "block";
		}
		else elements[i].style.display = "none";
	}
}
