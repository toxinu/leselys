// Globals
importer = false;
setKeyboard();
global = {};
global.feedStatus = {};

function changePassword() {
  var password1 = document.getElementById('password1');
  var password2 = document.getElementById('password2');

  document.getElementById('password-status').innerHTML = "";
  document.getElementById('password-status').style.display = "none";
  document.getElementById('password-form').classList.remove('warning');
  document.getElementById('password-form').classList.remove('success');

  if (password1.value != password2.value) {
    document.getElementById('password-status').innerHTML = "Not same password";
    document.getElementById('password-form').classList.add('warning');
  } else if (!password1.value) {
    document.getElementById('password-status').innerHTML = "Password can't be empty";
    document.getElementById('password-form').classList.add('warning');
  } else {
    api.changePassword(password1.value);
    document.getElementById('password-status').innerHTML = "Password changed!";
    password1.value = "";
    password2.value = "";
    document.getElementById('password-form').classList.add('success');
  }

  document.getElementById('password-status').style.display = "block";
  setInterval(function() {
    document.getElementById('password-form').classList.remove('warning');
    document.getElementById('password-form').classList.remove('success');
  }, 1500);
}

function addFeed() {
  var url = document.getElementById('urlFeed').value;
  if (url == '') { return false }

  // Undisplay add popup
  addToggle();

  // Clean add input content
  var add = document.getElementById('urlFeed');
  add.value = '';

  // Clear help message if no subscriptions
  if (document.getElementById('menu').getElementsByClassName('empty-feed-list')) {
    document.getElementById('menu').getElementsByClassName('empty-feed-list')[0].style.display = "none";
    document.getElementById('menu').getElementsByClassName('feeds-list-title')[0].style.display = "";
  }

  var loader = crel("li", crel("i", {"class": "icon-tasks"}), " Loading...");
  loader.style.display = "none";
  loader = document.getElementById('menu').appendChild(loader);
  loader.style.display = "";

  api.addFeed(url, function(req, data) {
    if (data.success) {
      var feedId = data.feed_id;
      var feedTitle = data.title;
      var feedURL = data.url;
      var feedLink = data.link;
      var feedCounter = data.counter;

      var newFeed = crel('a', {'onClick': 'viewFeed("' + feedId + '")', 'href': '#' + feedId}, feedTitle + " ",
            crel('span', {'class': 'unread-counter muted'}, '(' + feedCounter + ')'));

      loader.style.display = "none";
      loader.innerHTML = newFeed.outerHTML;
      loader.id = feedId;
      loader.setAttribute('data-link', feedLink);
      loader.classList.add('feed');
      loader.style.display = "";

      if(feedCounter > 0) {
        loader.classList.add('unread');
      }

      // Add new feed in settings/feeds if opened
      if (document.getElementById('feeds-settings')) {
        // Remove message if feeds list is empty
        if (document.getElementById('feeds-settings').getElementsByClassName('empty-feed-list')) {
          document.getElementById('feeds-settings').getElementsByClassName('empty-feed-list')[0].style.display = "none";
        }
        var newFeedSetting = crel('li', {'id': feedId + "-feeds-settings"}, feedTitle,
              ' (',
              crel('a', {'class': 'muted', 'href': '#', 'onClick': 'deleteFeed("' + feedId + '")'}, 'remove'),
              ') - ',
              crel('a', {'href': feedURL, 'target': '_blank'}, feedURL));
        newFeedSetting.style.display = "none";
        newFeedSetting = document.getElementById('feeds-settings').getElementsByTagName('ul')[0].appendChild(newFeedSetting);
        newFeedSetting.style.display = "";
      }
    } else {
      if (data.callback == "/api/login") { window.location = "login" }
      loader.innerHTML = '<li><i class="icon-exclamation-sign"></i> Error: ' + data.output +'</li>';
      var clearLoader = function() {
        loader.style.display = "none";
      }
      setTimeout(clearLoader, 5000);
    }
  });
}

function setFeedSetting(feedId, settingKey, settingValue) {
  api.setFeedSetting(feedId, settingKey, settingValue, function(req, data) {
    if (data.success) {
      global.feedStatus.id = false;
      viewFeed(feedId);
    }
  });
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
      //api.importOPML(e.target.result, function(req, data) {
      api.importOPML(file, function(req, data) {

        if (data.success) {
          importer = false;
          document.getElementById("OPMLSubmit").innerHTML = "Importing, reload page later...";
          document.getElementById("OPMLSubmit").className += " disabled";
        } else {
          if (data.callback == "/api/login")
            window.location = "login"
          document.getElementById("OPMLSubmit").innerHTML = "Error: " + data.output;
          document.getElementById("OPMLSubmit").className += " disabled";
        }
      });
    }
  })(file);
  reader.readAsText(file);
}

function viewSettings(callback) {
  global.feedStatus.id = false;
  api.getSettings(function(req, data) {
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
      initTabs();
      initSettingsView();
      if (typeof callback != "undefined" ) {
        callback();
      }
      disableRibbon();
    } else {
      if (data.callback == "/api/login")
        window.location = "login"
    }
  });
}

function viewHome(callback) {
  global.feedStatus.id = false;
  api.getHome(function(req, data) {
    if (data.success) {
      var parser = new DOMParser();
      var div = parser.parseFromString(data.content, "text/html");
      var content = div.getElementById('content');
      var sidebar = div.getElementById('menu');
      document.getElementById("content").innerHTML = content.innerHTML;
      document.getElementById("menu").innerHTML = sidebar.innerHTML;
      initPage();
      disableRibbon();
      if (typeof callback != "undefined" ) {
          callback();
      }
    } else {
      if (data.callback == "/api/login")
        window.location = "login"
    }
  });
}

function deleteFeed(feedId) {
  api.deleteFeed(feedId, function(req, data) {
    if (data.success) {
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
    } else {
      if (data.callback == "/api/login")
        window.location = "login"
    }
  });
}

function listStories(feedId, data, append, callback) {
  var append = append || false;
  var storyListAccordion = crel('div', {'class': 'accordion', 'id': 'story-list-accordion'});

  if (!append) {
    var content = '';

    if (data.content.length == 0) {
      content = '<p style="text-align:center; margin-top: 50px"><em>Oups, there is no story here...</em></p>';
    }
  } else {
      var content = document.getElementById('story-list-accordion').innerHTML;
  }

  for (var i=0;i < data.content.entries.length;i++) {
    var item = data.content.entries[i];
    var storyId = item._id;
    var storyTitle = item.title;
    var storyAccordion = getStoryAccordionTemplate();
    var storyRead = item.read;

    if (item.feed_title)
      storyTitle = storyTitle + "<span class=\"feed-title-combined muted\"> - " + item.feed_title + "</span>";

    storyAccordion.id = storyId;
    storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute('onclick', 'readStory("' + storyId + '")');
    storyAccordion.getElementsByClassName("accordion-toggle")[0].innerHTML = storyTitle;
    storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute('name', storyId);

    if (storyRead == false) {
      storyAccordion.getElementsByClassName('accordion-toggle')[0].style.fontWeight = "bold";
      storyAccordion.classList.add('unread-story');
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
  enableRibbon(feedId, data.content.ordering);
  if (typeof callback != "undefined" ) {
    callback();
  }
}

function viewFeed(feedId, callback) {
    // Add selected feed class
  var feedTitle = document.getElementById(feedId);
  feedTitle.classList.add('selected-feed');
  for (var i=0;i < document.getElementsByClassName('feed').length;i++) {
    var feed = document.getElementsByClassName('feed')[i];
    if (feed.getAttribute('id') != feedId) {
      feed.classList.remove('selected-feed');
    }
  }

  // Already scrolled
  if (!global.feedStatus || global.feedStatus.id != feedId) {
    global.feedStatus.start = 0;
    global.feedStatus.stop = 50;
    global.feedStatus.id = feedId;
    var append = false;
    window.scrollTo(0, 0);
  } else {
    if (global.feedStatus.stop >= global.feedStatus.length) {
      return
    }
    global.feedStatus.start = global.feedStatus.start + 50;
    global.feedStatus.stop = global.feedStatus.stop + 50;
    var append = true;
  }

  var start = global.feedStatus.start;
  var stop = global.feedStatus.stop;

  var xhr = api.getFeed(feedId, start, stop, function(req, data) {
    if (data.success) {
      listStories(feedId, data, append, function() {
        global.feedStatus.length = data.content.detail.length;
        if (typeof callback != "undefined" )
          callback();
      });
      // Make the stories visible, for devices with small screens.
      var top = document.getElementById('content');
      if (top && top.scrollIntoView) top.scrollIntoView();
    } else {
      if (data.callback == "/api/login")
        window.location = "login"
    }
  });

}

function updateCounter(feedId, number) {
  var counter = cleanCounter(document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML);
  var counter = counter + number;
  document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = '(' + counter + ')';
  if (counter == 0) {
    document.getElementById(feedId).getElementsByClassName('unread-counter')[0].style.display = "none";
    document.getElementById(feedId).classList.remove('unread');
    document.getElementById(feedId).style.fontWeight = 'normal';
  } else {
    document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = '(' + counter + ')';
    document.getElementById(feedId).getElementsByClassName('unread-counter')[0].style.display = "";
      document.getElementById(feedId).classList.add('unread');
  }
  if (feedId != "combined-feed" && feedId != "stared-feed") {
    updateCounter("combined-feed", number);
  }
}

function readStory(storyId, ignore) {
  // Avoid "read" state if story have just been marked unread
  var ignore = ignore || false;
  if (ignore == true) {
    document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].setAttribute('onclick', 'readStory("' + storyId + '")');
    return true
  }

  var storyHeading = document.getElementById(storyId);
  storyHeading.classList.add('selected-story');
  var storyList = document.getElementsByClassName('accordion-group');
  for (var i=0;i < storyList.length;i++) {
    var story = storyList[i];
    if (story.getAttribute('id') != storyId) {
      story.classList.remove('selected-story');
    }
  }

  if (document.getElementById(storyId).getElementsByClassName('accordion-inner')[0].innerHTML == "") {
    document.getElementById(storyId).getElementsByClassName('accordion-inner')[0].innerHTML = '<center><i class="icon-spinner icon-spin icon-3x"></i></center>';
  }

  // window.location.hash = storyId;
  api.readStory(storyId, function(req, data) {
    if (!data.success) {
      if (data.callback == "/api/login")
        window.location = "login"
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

    // TODO unbind v when the user is no longer looking at stories?
    var storyLink = story.getElementsByClassName("story-link")[0];
    storyLink.href = data.content.link;
    Mousetrap.unbind('v');
    Mousetrap.bind('v',
                   function() { window.open(storyLink.href, '_blank'); });

    story.getElementsByClassName("story-read-toggle")[0].setAttribute('onclick', 'unreadStory("' + storyId + '")');
    story.getElementsByClassName("story-read-toggle")[0].innerHTML = 'Mark as unread';
    story.getElementsByClassName("story-read-toggle")[0].href = "#" + storyId;
    story.getElementsByClassName("story-content")[0].innerHTML = data.content.description;
    story.getElementsByClassName("story-date")[0].innerHTML = published;


    document.getElementById(storyId).getElementsByClassName("accordion-inner")[0].innerHTML = story.innerHTML;
    document.getElementById(storyId).getElementsByClassName("story-read-toggle")[0].addEventListener(
      'click', function(e) { e.preventDefault() }, false
    );

    if (data.success) {
      document.getElementById(storyId).classList.remove('unread-story');
      updateCounter(feedId, -1);
    }
  });
  document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].style.fontWeight = 'normal';
}

function unreadStory(storyId) {
  api.unreadStory(storyId, function(req, data) {
    if (data.success) {
      var feedId = data.content.feed_id;
      var story = document.getElementById(storyId);
      story.classList.add('unread-story');

      // Avoid next click on story title
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].setAttribute('onclick', 'readStory("' + storyId + '", true)');

      story.getElementsByClassName("story-read-toggle")[0].setAttribute('onclick', 'readStory("' + storyId + '")');
      story.getElementsByClassName("story-read-toggle")[0].innerHTML = 'Mark as read';

      updateCounter(feedId, 1)

      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].style.fontWeight = 'bold';
    } else {
      if (data.callback == "/api/login")
        window.location = "login"
    }
  });
}

function loadTheme(themeName, callback) {
  api.setTheme(themeName, function(req, data) {
    window.location = "";
  });
}

function refreshCounters() {
  api.getCounters(function(req, data) {
    if (data.success) {
      for (i=0;i < data.content.length;i++) {
        var feed = data.content[i];
        var feedId = feed[0];
        var feedCounter = feed[1];
        document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = '(' + feedCounter + ')';
        if (feedCounter > 0) {
          document.getElementById(feedId).classList.add('unread');
          document.getElementById(feedId).getElementsByClassName('unread-counter')[0].style.display = "";
        } else {
          document.getElementById(feedId).classList.remove('unread');
          document.getElementById(feedId).getElementsByClassName('unread-counter')[0].style.display = "none";
        }
      }
    } else {
      if (data.callback == "/api/login")
        window.location = "login"
    }
  });
}

function initAddFeed() {
  var addFeed = getAddFeedTemplate();
  document.getElementById('menu').appendChild(addFeed);
}

function initSettingsView() {
  document.getElementById('OPMLSubmit').addEventListener('click', handleOPMLImport, false);
  document.getElementById('OPMLFile').addEventListener('change', function() {
    document.getElementById('upload-file-info').innerHTML = document.getElementById('OPMLFile').value.replace("C:\\fakepath\\", "");
  });
  // Set enter key on password2 input
  document.getElementById('password2').onkeypress = function(e){
    if (!e) e = window.event;
    if (e.keyCode == '13'){
      changePassword();
      return false;
    }
  }
}

function initPage() {
  // Remove anchors binding for mobile view
  var feeds = document.getElementById('menu').getElementsByClassName('feed');
  addEventListenerList(feeds, 'click', function(e) {e.preventDefault()});

  var combinedFeed = document.getElementById('combined-feed');
  if (combinedFeed)
    combinedFeed.addEventListener('click', function(e) {e.preventDefault()});
  var staredFeed = document.getElementById('stared-feed');
  if (staredFeed)
    staredFeed.addEventListener('click', function(e) {e.preventDefault()});

  bindInfinityScroll();
  initAddFeed();
  setInterval(refreshCounters, 120000);
}



function bindInfinityScroll(){
    if(window.addEventListener) {
      document.addEventListener('scroll', function() {
        getScroll(function(height) {
          if (!global.loading) {
            if (height >= 70) {
              global.loading = true;
              viewFeed(getCurrentFeedId(), function() {
                global.loading = false;
              });
            }
          }
        })
      }, false);
    }
}

function getScroll(callback) {
  var percent = (document.documentElement.scrollTop + document.body.scrollTop) / (document.documentElement.scrollHeight - document.documentElement.clientHeight) * 100;

  if (typeof callback != "undefined" )
    callback(percent);
}

// Tabs for settings
function initTabs() {
  for (var i=0;i < document.getElementsByClassName('tabbable').length;i++) {
    var table = document.getElementsByClassName('tabbable')[i];
    for (var j=0;j < table.getElementsByClassName('nav-tabs')[0].getElementsByTagName('li').length;j++) {
      var tab = table.getElementsByClassName('nav-tabs')[0].getElementsByTagName('li')[j];
      var contentId = tab.getElementsByTagName('a')[0].getAttribute('href').substr(1);
      var content = document.getElementById(contentId);

      if (!content.classList.contains('active')) {
        content.style.display = "none";
      }

      tab.getElementsByTagName('a')[0].addEventListener('click', function (e) {
        var _id = this.getAttribute('href').substr(1);
        var content = document.getElementById(_id);
        this.parentNode.classList.add('active');
        content.classList.add('active');
        content.style.display = "block";
        hideTabs(this.parentNode);
        e.preventDefault();
      });
    }
  }
}

// Hide other tabs
function hideTabs(tab) {
  var contentId = tab.getElementsByTagName('a')[0].getAttribute('href').substr(1);
  var table = tab.parentNode.parentNode;
  for (var i=0;i < table.getElementsByClassName('nav-tabs')[0].getElementsByTagName('li').length;i++) {
    var tab = table.getElementsByClassName('nav-tabs')[0].getElementsByTagName('li')[i];
    var tabId = tab.getElementsByTagName('a')[0].getAttribute('href').substr(1);
    if (tabId != contentId) {
      tab.classList.remove('active');
      document.getElementById(tabId).classList.remove('active');
      document.getElementById(tabId).style.display = "none";
    }
  }
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

function markAllAsRead(feedId){
  api.markAllAsRead(feedId, function(req, data) {
      global.feedStatus.id = false;
      viewFeed(feedId);
      refreshCounters();
  });
}

function markAllAsUnread(feedId){
  api.markAllAsUnread(feedId, function(req, data) {
      global.feedStatus.id = false;
      viewFeed(feedId);
      refreshCounters();
  });
}

function enableRibbon(feedId, ordering) {
  var ribbon = document.getElementById('ribbon');
  ribbon.classList.remove('hidden');
  ribbon.classList.remove('ribbon-three');

  if (ordering == "unreaded") {
    ribbon.getElementsByClassName('order-unreaded')[0].classList.add('active');
    ribbon.getElementsByClassName('order-published')[0].classList.remove('active');
  } else if (ordering == "published") {
    ribbon.getElementsByClassName('order-unreaded')[0].classList.remove('active');
    ribbon.getElementsByClassName('order-published')[0].classList.add('active');
  }
  ribbon.getElementsByClassName('order-unreaded')[0].getElementsByTagName('a')[0].onclick = function () {setFeedSetting(feedId, 'ordering', 'unreaded')};
  ribbon.getElementsByClassName('order-published')[0].getElementsByTagName('a')[0].onclick = function () {setFeedSetting(feedId, 'ordering', 'published')};

  if (feedId == "combined-feed") {
    ribbon.getElementsByClassName('mark-all-as-unread')[0].classList.add('hidden');
    ribbon.classList.add('ribbon-three');
  } else if (feedId == "stared-feed") {
    ribbon.classList.add('hidden');
    return
  } else {
    ribbon.getElementsByClassName('mark-all-as-unread')[0].classList.remove('hidden');
  }

  ribbon.getElementsByClassName('mark-all-as-read')[0].getElementsByTagName('a')[0].onclick = function () {
    var onclick = "markAllAsRead(\"" + feedId + "\");TINY.box.hide();";
    var box = getMarkAllConfirmationTemplate('Mark all as read ?', feedId, onclick);
    TINY.box.show({'html': box.outerHTML,maskopacity:40,maskid:'confirmation-mask'});
  }
  ribbon.getElementsByClassName('mark-all-as-unread')[0].getElementsByTagName('a')[0].onclick = function () {
    var onclick = "markAllAsUnread(\"" + feedId + "\");TINY.box.hide();";
    var box = getMarkAllConfirmationTemplate('Mark all as unread ?', feedId, onclick);
    TINY.box.show({'html': box.outerHTML,maskopacity:40,maskid:'confirmation-mask'});
  }
}

function disableRibbon() {
  var ribbon = document.getElementById('ribbon');
  ribbon.classList.add('hidden');
}

function getCurrentFeedLink() {
  if (document.getElementsByClassName('selected-feed').length > 0)
    return document.getElementsByClassName('selected-feed')[0].getAttribute('data-link');
}

function getCurrentFeedId() {
  if (document.getElementsByClassName('selected-feed').length > 0)
    return document.getElementsByClassName('selected-feed')[0].id;
}

function getCurrentStory() {
  var story = document.getElementsByClassName('selected-story')[0];
  if (typeof story === "undefined") { return false }
  return story;
}

function getNextStory() {
  var story = document.getElementsByClassName('selected-story')[0];
  // If there is no selected story, try for the first story.
  if (typeof story === "undefined") {
    story = document.getElementsByClassName('accordion-group')[0];
    if (typeof story === "undefined") { return false; }
    return story;
  }
  if (story.nextSibling == null) { return false; }
  return story.nextSibling;
}

function getPreviousStory() {
  var story = document.getElementsByClassName('selected-story')[0];
  if (typeof story === "undefined") { return false }
  if (story.previousSibling == null) { return false }
  return story.previousSibling;
}

function toggleReadState(storyId) {
  var story = document.getElementById(storyId);
  if (story.classList.contains('unread-story')) {
    readStory(storyId);
  } else {
    unreadStory(storyId);
  }
}

// Keyboard
function setKeyboard(){
  Mousetrap.bind('g h', function() { viewHome(); });
  Mousetrap.bind('g a', function() { viewFeed('combined-feed'); });
  Mousetrap.bind('r', function() { refreshCounters(); });
  Mousetrap.bind('a', function() { addToggle(); });
  Mousetrap.bind('?', function() {
    viewSettings(function () {
      var navList = document.getElementById('content').getElementsByClassName('nav-tabs')[0].getElementsByTagName('li');
      var contentList = document.getElementById('content').getElementsByClassName('tab-content')[0].getElementsByClassName('tab-pane');
      for (i=0;i<navList.length;i++) {
        navList[i].classList.remove('active');
        contentList[i].classList.remove('active');
        if (navList[i].getElementsByTagName('a')[0].getAttribute('href') == '#help') {
          navList[i].classList.add('active');
          contentList[i].classList.add('active');
          contentList[i].style.display = "block";
        }
      }
    });
  });
  Mousetrap.bind('m', function() {
    var story = getCurrentStory();
    if (story == false) { return }
    toggleReadState(story.getAttribute('id'));
  });
  Mousetrap.bind('o', function() {
    var story = getCurrentStory();
    if (story == false) { return }
    story.getElementsByTagName('a')[0].click()
  });
  Mousetrap.bind('j', function() {
    var nextStory = getNextStory();
    if (nextStory == false) { return; }
    nextStory.getElementsByTagName('a')[0].click();
    nextStory.scrollIntoView();
  });
  Mousetrap.bind('k', function() {
    var previousStory = getPreviousStory();
    if (previousStory == false) { return; }
    previousStory.getElementsByTagName('a')[0].click();
    previousStory.scrollIntoView();
  });
  Mousetrap.bind('b', function() {
    var link = getCurrentFeedLink();
    if (link) {window.open(link, '_blank')}
  });
}

// Utils
function addEventListenerList(list, event, fn) {
  for (var i = 0, len = list.length; i < len; i++) {
    list[i].addEventListener(event, fn, false);
  }
}

function addToggle() {
  var add = document.getElementById('add');
  Mousetrap.reset();

  if (add.style.display == "block" ) {
    // hide the popover and reset state
    add.style.display = "none";
    setKeyboard();
    return;
  }

  // show the popover and set state
  add.style.display = "block";
  document.getElementById('urlFeed').focus();
  Mousetrap.bind('esc', function(e, combo) { addToggle(); });
}

function cleanCounter(counter) {
  return parseInt(counter.substr(1, counter.length-2));
}

/*
 * DOMParser HTML extension
 * 2012-09-04
 *
 * By Eli Grey, http://eligrey.com
 * Public domain.
 * NO WARRANTY EXPRESSED OR IMPLIED. USE AT YOUR OWN RISK.
 */

/*! @source https://gist.github.com/1129031 */
/*global document, DOMParser*/

(function(DOMParser) {
    "use strict";

    var
      DOMParser_proto = DOMParser.prototype
    , real_parseFromString = DOMParser_proto.parseFromString
    ;

    // Firefox/Opera/IE throw errors on unsupported types
    try {
        // WebKit returns null on unsupported types
        if ((new DOMParser).parseFromString("", "text/html")) {
            // text/html parsing is natively supported
            return;
        }
    } catch (ex) {}

    DOMParser_proto.parseFromString = function(markup, type) {
        if (/^\s*text\/html\s*(?:;|$)/i.test(type)) {
            var
              doc = document.implementation.createHTMLDocument("")
            ;

            doc.body.innerHTML = markup;
            return doc;
        } else {
            return real_parseFromString.apply(this, arguments);
        }
    };
}(DOMParser));

/* @source http://purl.eligrey.com/github/classList.js/blob/master/classList.js*/
"use strict";if(typeof document!=="undefined"&&!("classList" in document.createElement("a"))){(function(a){var f="classList",d="prototype",e=(a.HTMLElement||a.Element)[d],g=Object;strTrim=String[d].trim||function(){return this.replace(/^\s+|\s+$/g,"")},arrIndexOf=Array[d].indexOf||function(k){for(var j=0,h=this.length;j<h;j++){if(j in this&&this[j]===k){return j}}return -1},DOMEx=function(h,i){this.name=h;this.code=DOMException[h];this.message=i},checkTokenAndGetIndex=function(i,h){if(h===""){throw new DOMEx("SYNTAX_ERR","An invalid or illegal string was specified")}if(/\s/.test(h)){throw new DOMEx("INVALID_CHARACTER_ERR","String contains an invalid character")}return arrIndexOf.call(i,h)},ClassList=function(m){var l=strTrim.call(m.className),k=l?l.split(/\s+/):[];for(var j=0,h=k.length;j<h;j++){this.push(k[j])}this._updateClassName=function(){m.className=this.toString()}},classListProto=ClassList[d]=[],classListGetter=function(){return new ClassList(this)};DOMEx[d]=Error[d];classListProto.item=function(h){return this[h]||null};classListProto.contains=function(h){h+="";return checkTokenAndGetIndex(this,h)!==-1};classListProto.add=function(h){h+="";if(checkTokenAndGetIndex(this,h)===-1){this.push(h);this._updateClassName()}};classListProto.remove=function(i){i+="";var h=checkTokenAndGetIndex(this,i);if(h!==-1){this.splice(h,1);this._updateClassName()}};classListProto.toggle=function(h){h+="";if(checkTokenAndGetIndex(this,h)===-1){this.add(h)}else{this.remove(h)}};classListProto.toString=function(){return this.join(" ")};if(g.defineProperty){var c={get:classListGetter,enumerable:true,configurable:true};try{g.defineProperty(e,f,c)}catch(b){if(b.number===-2146823252){c.enumerable=false;g.defineProperty(e,f,c)}}}else{if(g[d].__defineGetter__){e.__defineGetter__(f,classListGetter)}}}(self))};
