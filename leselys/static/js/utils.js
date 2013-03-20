<<<<<<< HEAD
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
=======
function fadeIn(what, duration) {
  if (what.style.display == "none") {
    what.style.display = "block";
  }
  what.opct = 100;
  what.ih = window.setInterval(function() {
    what.opct++;
    if(what.opct) {
      what.MozOpacity = what.opct / 100;
      what.KhtmlOpacity = what.opct / 100;
      what.filter = "alpha(opacity=" + what.opct + ")";
      what.opacity = what.opct / 100;
    }else{
      window.clearInterval(what.ih);
      what.style.display = 'block';
    }
  }, 10 * duration);
}

function fadeOut(what, duration) {
  what.opct = 100;
  what.ih = window.setInterval(function() {
    what.opct--;
    if(what.opct) {
      what.MozOpacity = what.opct / 100;
      what.KhtmlOpacity = what.opct / 100;
      what.filter = "alpha(opacity=" + what.opct + ")";
      what.opacity = what.opct / 100;
    }else{
      window.clearInterval(what.ih);
      what.style.display = 'none';
    }
  }, 10 * duration);
>>>>>>> d43d78025a7c8a80b72951df560797cff04ced18
}
