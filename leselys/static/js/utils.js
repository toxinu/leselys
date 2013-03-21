function hide( elem, callback ) {
//  elem.style.display = "none";
  elem.style.visibility = "hidden";
  if (callback) { return callback() }
}

function show( elem, callback ) {
//  elem.style.display = "";
  elem.style.visibility = "visible";
  if (callback) { return callback() }
}

function fadeOut( elem, time, callback) {
  console.log(screen.width);
  var time = time || "500ms";
//  if (screen.width > 768) {
    elem.style['-webkit-transition'] = "visibility 0s " + time + ", opacity " + time + "s linear";
    elem.style['-moz-transition'] = "visibility 0s " + time + ", opacity " + time + "s linear";
    elem.style['-o-transition'] = "visibility 0s " + time + ", opacity " + time + "s linear";
    elem.style['transition'] = "visibility 0s " + time + ", opacity " + time + "s linear";
//  }
  elem.style['visibility'] = "hidden";
  elem.style['opacity'] = "0";
  elem.style.top = "-100000px";
//  elem.style['display'] = "none";
  if (callback) { return callback() }
}

function fadeIn( elem, time, callback ) {
    var time = time || "500ms";
    elem.style.top = "";
    elem.style.display = "";
    elem.style['visibility'] = "visible";
    elem.style['opacity'] = "1";
    elem.style['-webkit-transition'] = "opacity " + time + " linear";
    elem.style['-moz-transition'] = "opacity " + time + " linear";
    elem.style['-o-transition'] = "opacity " + time + " linear";
    elem.style['transition'] = "opacity " + time + " linear";

//    elem.style.display = "";
    if (callback) { return callback() }
//  if (screen.width > 768) {
//  }
}
