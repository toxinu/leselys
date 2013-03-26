function addFeed() {
  var url = document.getElementById('urlFeed').value;
  if (url == '') { return false }

  // Undisplay add popup
  document.getElementById('add').style.display = "none";

  // Clear help message if no subscriptions
  if (document.getElementById('menu').getElementsByClassName('empty-feed-list')) {
    document.getElementById('menu').getElementsByClassName('empty-feed-list')[0].style.display = "none";
    document.getElementById('menu').getElementsByClassName('feeds-list-title')[0].style.display = "";
  }

  var loader = crel("li", crel("i", {"class": "icon-tasks"}), " Loading...");
  loader.style.display = "none";
  loader = document.getElementById('menu').appendChild(loader);
  loader.style.display = "";
  $.post("/api/add", {url: url}, function(data) {
    if (data.success == true) {
      var feedId = data.feed_id;
      var feedTitle = data.title;
      var feedURL = data.url;
      var feedCounter = data.counter;

      var newFeed = crel('a', {'onClick': 'viewFeed("' + feedId + '")', 'href': '/#' + feedId}, feedTitle + " ",
            crel('span', {'class': 'badge badge-inverse unread-counter'}, feedCounter));

      loader.style.display = "none";
      loader.innerHTML = newFeed.outerHTML;
      loader.id = feedId;
      loader.className += " story";
      loader.style.display = "";

      // Add new feed in settings/feeds if opened
      if (document.getElementById('feeds-settings')) {
        // Remove message if feeds list is empty
        if (document.getElementById('feeds-settings').getElementsByClassName('empty-feed-list')) {
          document.getElementById('feeds-settings').getElementsByClassName('empty-feed-list')[0].style.display = "none";
        }
        var newFeedSetting = crel('li', {'id': feedId}, feedTitle, 
              ' (',
              crel('a', {'class': 'muted', 'href': '#', 'onClick': 'deleteFeed("' + feedId + '")'}, 'remove'),
              ') - ',
              crel('a', {'href': feedURL, 'target': '_blank'}, feedURL));
        newFeedSetting.style.display = "none";
        newFeedSetting = document.getElementById('feeds-settings').getElementsByTagName('ul')[0].appendChild(newFeedSetting);
        newFeedSetting.style.display = "";
      }
    } else {
      if ( data.callback == "/api/login" ) { window.location = "/login" }
      loader.innerHTML = '<li><i class="icon-exclamation-sign"></i> Error: ' + data.output +'</li>';
      var clearLoader = function() {
        loader.style.display = "none";
      }
      setTimeout(clearLoader, 5000);
    }
  });
  $('#add').popover('hide')
}

function handleOPMLImport(evt) {
  if (document.getElementById("upload-file-info").innerHTML == "") { return false }
  if (importer) { return false }

  // Check if browser is FileRead object compatible
  if (window.File && window.FileReader && window.FileList && window.Blob) {
    // Great success! All the File APIs are supported.
  } else {
    alert('The File APIs are not fully supported in this browser.');
    return false;
  }

  // Retrieve file from form
  importer = true;
  var file = document.getElementById('OPMLFile').files[0];
  if (!file) { return false }
  var reader = new FileReader();

  reader.onload = (function(OPMLFile) {

    return function(e) {
      $.post('/api/import/opml', { file: e.target.result }, function(data) {
        if (data.success == true) {
          importer = false;
          document.getElementById("OPMLSubmit").innerHTML = "Importing, reload page later...";
          document.getElementById("OPMLSubmit").className += " disabled";
        } else {
          if (data.callback == "/api/login") { window.location = "/login" }
          document.getElementById("OPMLSubmit").innerHTML = "Error: " + data.output;
          document.getElementById("OPMLSubmit").className += " disabled";
        }
      });
    }
  })(file);
  reader.readAsText(file);
}

function viewSettings() {
  $.get('/settings?jsonify=true', function(data) {
    if (data.success) {
      var parser = new DOMParser();
      var div = parser.parseFromString(data.content, "text/html");
      var content = div.getElementById('content');
      var sidebar = div.getElementById('menu');
      document.getElementById("content").innerHTML = content.innerHTML;
      document.getElementById("menu").innerHTML = sidebar.innerHTML;

      if (importer) {
        document.getElementById("OPMLSubmit").innerHTML = "Last import not finished...";
        document.getElementById("OPMLSubmit").className += " disabled";
        return false;
      }
      if (document.getElementById("OPMLSubmit")) {
        document.getElementById('OPMLSubmit').addEventListener('click', handleOPMLImport, false);
      }
      initPage();
    } else {
      if (data.callback == "/api/login") { window.location = "/login" }
    }
  });
}

function viewHome() {
  $.get('/?jsonify=true', function(data) {
    if (data.success) {
      var parser = new DOMParser();
      var div = parser.parseFromString(data.content, "text/html");
      var content = div.getElementById('content');
      var sidebar = div.getElementById('menu');
      document.getElementById("content").innerHTML = content.innerHTML;
      document.getElementById("menu").innerHTML = sidebar.innerHTML;
      initPage();
    } else {
      if (data.callback == "/api/login") { window.location = "/login" }
    }
  });
}

function deleteFeed(feedId) {
  $.ajax({
    url: '/api/remove/' + feedId,
    type: 'DELETE',
    success: function(result) {
      if (result.success = false) {
        if (result.callback == "/api/login") { window.location = "/login" }
        window.location = "/";
      }
      document.getElementById(feedId).style.display = "none";
      // Remove feed in sidebar
      var _child = document.getElementById(feedId);
      var _parent = document.getElementById(feedId).parentNode;
      _parent.removeChild(_child);

      // Feeds settings
      var feedsNodes = document.getElementById('feeds-settings');
      if ( typeof feedsNodes != 'undefined' ) {
        // Remove feed in sidebar
        var _child = document.getElementById(feedId + "-settings");
        var _parent = document.getElementById(feedId + "-settings").parentNode;
        _parent.removeChild(_child);

        console.log(feedsNodes.getElementsByTagName('li').length);
        if ( feedsNodes.getElementsByTagName('li').length < 1 ) {
          document.getElementById('feeds-settings').getElementsByClassName('empty-feed-list')[0].style.display = "";
        }
      }

      // Sidebar
      var feedsNodes = document.getElementById('menu').getElementsByClassName('feed')
      if ( feedsNodes.length < 1 ) {
          document.getElementById('menu').getElementsByClassName('feeds-list-title')[0].style.display = "none";
          document.getElementById('menu').getElementsByClassName('empty-feed-list')[0].style.display = "";
      }
    }
  });
}

function viewFeed(feedId) {
  for (var i=0;i < requests.length;i++) {
    requests[i].abort();
    requests.shift();
  }
  var request = $.getJSON('/api/get/' + feedId, function(data) {
    if (data.success == false) {
      if (data.callback == "/api/login") { window.location = "/login" }
      window.location = "/";
    }

    var storyListAccordion = crel('div', {'class': 'accordion', 'id': 'story-list-accordion'});
    var content = '';

    for (var i=0;i < data.content.length;i++) {
      var item = data.content[i];
      var storyId = item._id;
      var storyTitle = item.title;
      var storyAccordion = getStoryAccordionTemplate();
      var storyRead = item.read;

      storyAccordion.id = storyId;
      storyAccordion.getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '")';
      storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
      storyAccordion.getElementsByClassName("accordion-toggle")[0].innerHTML = storyTitle;

      if (storyRead == false) {
        storyAccordion.getElementsByClassName('accordion-toggle')[0].style.fontWeight = "bold";
      }

      content += storyAccordion.outerHTML;
    }
    storyListAccordion.innerHTML = content;
    document.getElementById('content').innerHTML = storyListAccordion.outerHTML;

    var feedsList = document.getElementById('menu').getElementsByTagName('a');
    for (i=0;i < feedsList.length;i++) {
      feedsList[i].classList.remove('text-error');
    }
    document.getElementById(feedId).getElementsByTagName('a')[0].classList.add('text-error');
    initAccordion();
  });
  requests.push(request);
}

function readStory(storyId, ignore) {
  // Avoid "read" state if story have just been marked unread
  var ignore = ignore || false;
  if (ignore == true) {
    document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '")';
    document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
    return true
  }

  $.getJSON('/api/read/' + storyId, function(data) {
    if (data.success == false) {
      if (data.callback == "/api/login" ) { window.location = "/login" }
    }
    if (data.content.last_update == false) {
      var published = "No date";
    } else {
      // Minutes
      if (data.content.last_update['min'].toString().length == 1) {
        var minutes = "0" + data.content.last_update['min'];
      } else {
        var minutes = data.content.last_update['min'];
      }
      // Hours
      if (data.content.last_update['hour'].toString().length == 1) {
        var hours = "0" + data.content.last_update['hour'];
      } else {
        var hours = data.content.last_update['hour'];
      }
      var published = data.content.last_update['year'] + '-' + data.content.last_update['month'] +
                    '-' + data.content.last_update['day'] + "  " + hours + ":" + minutes;
    }

    var feedId = data.content.feed_id;
    var story = getStoryTemplate();


    story.getElementsByClassName("story-link")[0].href = data.content.link;
    story.getElementsByClassName("story-read-toggle")[0].onclick = 'unreadStory("' + storyId + '")';
    story.getElementsByClassName("story-read-toggle")[0].setAttribute("onclick", 'unreadStory("' + storyId + '")');
    story.getElementsByClassName("story-read-toggle")[0].innerHTML = 'Mark as unread';
    story.getElementsByClassName("story-read-toggle")[0].href = "#" + storyId;
    story.getElementsByClassName("story-content")[0].innerHTML = data.content.description;
    story.getElementsByClassName("story-date")[0].innerHTML = published;

    document.getElementById(storyId).getElementsByClassName("accordion-inner")[0].innerHTML = story.innerHTML;
    document.getElementById(storyId).getElementsByClassName("story-read-toggle")[0].addEventListener(
    'click', function(e) { e.preventDefault() }, false
    );
    if (data.success == true) {
      var counter = parseInt(document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML) - 1;
      document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = counter;
      if (counter == 0) {
        document.getElementById(feedId).getElementsByClassName('unread-counter')[0].style.display = "none";
      }
    }
  });
  document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].style.fontWeight = 'normal';
}

function unreadStory(storyId) {
  $.getJSON('/api/unread/' + storyId, function(data) {
    if (data.success == true) {
      var feedId = data.content.feed_id;
      var story = document.getElementById(storyId);

      // Avoid next click on story title
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '", true)';
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '", true)');

      story.getElementsByClassName("story-read-toggle")[0].onclick = 'readStory("' + storyId + '")';
      story.getElementsByClassName("story-read-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
      story.getElementsByClassName("story-read-toggle")[0].innerHTML = 'Mark as read';

      var counter = parseInt(document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML) + 1;

      if (counter == 1) {
        document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = counter;
        document.getElementById(feedId).getElementsByClassName('unread-counter')[0].style.display = "";
      } else {
        document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = counter;
      }
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].style.fontWeight = 'bold';
    } else {
      if (callback == "/api/login") { window.location = "/login" }
    }
  });
}

function loadTheme(theme, callback) {
  $.post('/api/settings/theme', {theme: theme}, function (data) {
    window.location = "/";
  })
}

function refreshCounters() {
  $.getJSON('/api/counters', function(data) {
    if (data.success == false) {
      if (data.callback == "/api/login") { window.location = "/login" }
    }
    for (i=0;i < data.content.length;i++) {
      var feed = data.content[i];
      var feedId = feed[0];
      var feedCounter = feed[1];
      if (feedCounter > 1) {
        $(document.getElementById(feedId).getElementsByClassName('badge')[0]).show();
      }
      document.getElementById(feedId).getElementsByClassName('badge')[0].innerHTML = feedCounter;
    }
  });
}

function initAddFeed() {
  var addFeed = getAddFeedTemplate();
  document.getElementById('menu').appendChild(addFeed);
}

function initPage() {
  // Remove anchors binding for mobile view
  var feeds = document.getElementById('menu').getElementsByClassName('feed');
  addEventListenerList(feeds, 'click', function(e) {e.preventDefault()});

  initAddFeed()
  setInterval(refreshCounters, 120000);
}

// Accordion for stories
function initAccordion() {
  for (var i=0;i < document.getElementsByClassName('accordion').length;i++) {
    var accordion = document.getElementsByClassName('accordion')[i];
    for (var j=0;j < accordion.getElementsByClassName('accordion-group').length;j++) {
      var accordionGroup = accordion.getElementsByClassName('accordion-group')[j];
      var heading = accordionGroup.getElementsByClassName('accordion-heading')[0];
      var body = accordionGroup.getElementsByClassName('accordion-inner')[0];

      heading.style.height = "auto";
      heading.addEventListener('click', function() {
        var body = this.parentNode.getElementsByClassName('accordion-inner')[0];
        if (body.style.display == "") {
          body.style.display = "none";

        } else {
          body.style.display = "";
          body.style.height = "auto";
          collapseIn(this.parentNode);
        }
      });

      body.style.display = "none";
      body.style.height = "0px";
      body.style.overflow = "hidden";
    }
  }
}

function collapseIn (accordionGroupRoot) {
  var accordion = accordionGroupRoot.parentNode;
  for (var i=0;i < accordion.getElementsByClassName('accordion-group').length;i++) {
    var accordionGroup = accordion.getElementsByClassName('accordion-group')[i];
    if (accordionGroup != accordionGroupRoot) {
      var heading = accordionGroup.getElementsByClassName('accordion-heading')[0];
      var body = accordionGroup.getElementsByClassName('accordion-inner')[0];
      body.style.display = "none";
      body.style.height = "0px";
    }
    
  }
}

// Utils
function addEventListenerList(list, event, fn) {
  for (var i = 0, len = list.length; i < len; i++) {
    list[i].addEventListener(event, fn, false);
  }
}

$(document).ready(function() {
  // Globals
  requests = new Array();
  importer = false;
});

function addToggle() {
  var add = document.getElementById('add');
  if (add.style.display == "block" ) {
    add.style.display = "none";
  } else {
    add.style.display = "block";
  }
  document.getElementById('urlFeed').focus();
}