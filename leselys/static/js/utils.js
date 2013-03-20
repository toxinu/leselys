function fadeOut( elem, time ) {
  if (screen.width > 768) {
    var time = time || 1;
    elem.style['-webkit-transition'] = "visibility 0s " + time + "s, opacity " + time + "s linear";
    elem.style['-moz-transition'] = "visibility 0s " + time + "s, opacity " + time + "s linear";
    elem.style['-o-transition'] = "visibility 0s " + time + "s, opacity " + time + "s linear";
    elem.style['transition'] = "visibility 0s " + time + "s, opacity " + time + "s linear";
    elem.style['opacity'] = "0";
  }
  elem.style['visibility'] = "hidden";
  elem.style['opacity'] = "0";
}

function fadeIn( elem, time ) {
  elem.style.display = "";
  elem.style['visibility'] = "visible";
  if (screen.width > 768) {
    var time = time || 1;
    elem.style['-webkit-transition'] = "opacity " + time + "s linear";
    elem.style['-moz-transition'] = "opacity " + time + "s linear";
    elem.style['-o-transition'] = "opacity " + time + "s linear";
    elem.style['transition'] = "opacity " + time + "s linear";
  }
  elem.style['opacity'] = "1";
}
