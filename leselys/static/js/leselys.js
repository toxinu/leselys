function addFeed() {
  var url = document.getElementById('urlFeed').value;
  if (url == '') { return false }

  // Clear help message if no subscriptions
  if (document.getElementById('menu').getElementsByClassName('empty-feed-list')) {
    document.getElementById('menu').getElementsByClassName('empty-feed-list')[0].style.display = "none";
    document.getElementById('menu').getElementsByClassName('feeds-list-title')[0].style.display = "";
  }

  var loader = crel("li", crel("i", {"class": "icon-tasks"}), " Loading...");
  loader.style.display = "none";
  loader = document.getElementById('menu').appendChild(loader);
  $(loader).fadeIn();
  $.post("/api/add", {url: url}, function(data) {
    if (data.success == true) {
      var feedId = data.feed_id;
      var feedTitle = data.title;
      var feedURL = data.url;
      var feedCounter = data.counter;

      var newFeed = crel('a', {'onClick': 'viewFeed("' + feedId + '")', 'href': '/#' + feedId}, feedTitle + " ",
            crel('span', {'class': 'badge badge-inverse unread-counter'}, feedCounter));

      $(loader).fadeOut(function () {
        loader.innerHTML = newFeed.outerHTML;
        loader.id = feedId;
        loader.className += " story";
        $(loader).fadeIn();
      });

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
        $(newFeedSetting).fadeIn();
      }
    } else {
      if ( data.callback == "/api/login" ) { window.location = "/login" }
      loader.innerHTML = '<li><i class="icon-exclamation-sign"></i> Error: ' + data.output +'</li>';
      var clearLoader = function() {
        $(loader).hide();
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
          $('#OPMLSubmit').addClass('disabled');
        } else {
          if (data.callback == "/api/login") { window.location = "/login" }
          document.getElementById("OPMLSubmit").innerHTML = "Error: " + data.output;
          $('#OPMLSubmit').addClass('disabled');
        }
      });
    }
  })(file);
  reader.readAsText(file);
}

function viewSettings() {
  $.get('/settings?jsonify=true', function(data) {
    if (data.success) {
      var content = $(data.content).find('#content');
      var sidebar = $(data.content).find('#menu')
      document.getElementById("content").innerHTML = content.html();
      document.getElementById("menu").innerHTML = sidebar.html()
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
      var content = $(data.content).find('#content');
      var sidebar = $(data.content).find('#menu')
      document.getElementById("content").innerHTML = content.html();
      document.getElementById("menu").innerHTML = sidebar.html()
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
      $('#feeds-settings ul li#' + feedId).fadeOut(300, function() {
        $(this).remove();
        if ($('#feeds-settings ul li').length < 1) {
          $(document.getElementById('feeds-settings').getElementsByClassName('empty-feed-list')[0]).fadeIn();
        }
      });
      $('ul#menu li#' + feedId).fadeOut(300, function() {
        $(this).remove();
        if ($('ul#menu li').length < 6) {
          $(document.getElementById('menu').getElementsByClassName('feeds-list-title')[0]).fadeOut();
          $(document.getElementById('menu').getElementsByClassName('empty-feed-list')[0]).fadeIn();
        }
      });
    }
  });
}

function viewFeed(feedId) {
  $.each(requests, function(i, request) {
      request.abort();
      requests.shift();
  });
  var request = $.getJSON('/api/get/' + feedId, function(data) {
    if (data.success == false) {
      if (data.callback == "/api/login") { window.location = "/login" }
      window.location = "/";
    }

    var storyListAccordion = crel('div', {'class': 'accordion', 'id': 'story-list-accordion'});
    var content = '';

    $.each(data.content, function(i,item){
      var storyId = item._id;
      var storyTitle = item.title;
      var storyAccordion = getStoryAccordionTemplate();
      var storyRead = item.read;

      storyAccordion.id = storyId;
      storyAccordion.getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '")';
      storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
      storyAccordion.getElementsByClassName("accordion-toggle")[0].innerHTML = storyTitle;
      storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute("data-target", "#" + storyId + " .accordion-body");

      if (storyRead == false) {
        storyAccordion.getElementsByClassName('accordion-toggle')[0].style.fontWeight = "bold";
      }

      content += storyAccordion.outerHTML;
    });
    storyListAccordion.innerHTML = content;
    document.getElementById('content').innerHTML = storyListAccordion.outerHTML;

    $('#menu a').each(function(index) {
      $(this).css('font-weight', 'normal');
    });
    document.getElementById(feedId).getElementsByTagName('a')[0].style.fontWeight = "bold";
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

    document.getElementById(storyId).getElementsByClassName("accordion-body")[0].innerHTML = story.outerHTML;
    document.getElementById(storyId).getElementsByClassName("story-read-toggle")[0].addEventListener(
    'click', function(e) { e.preventDefault() }, false
    );
    if (data.success == true) {
      var counter = parseInt($("#" + feedId + " .unread-counter").html()) - 1;
      document.getElementById(feedId).getElementsByClassName('unread-counter')[0].innerHTML = counter;
      if (counter == 0) {
        $("#" + feedId + " .unread-counter").fadeOut();
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

      var counter = parseInt($("#" + feedId + " .unread-counter").html()) + 1;

      $('a[href=#' + storyId + ']').data('unreaded', true);
      if (counter == 1) {
        $("#" + feedId + " .unread-counter").html(counter);
        $("#" + feedId + " .unread-counter").fadeIn();
      } else {
        $("#" + feedId + " .unread-counter").html(counter);
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
    $.each(data.content, function(i, feed) {
      var feedId = feed[0];
      var feedCounter = feed[1];
      if (feedCounter > 1) {
        $(document.getElementById(feedId).getElementsByClassName('badge')[0]).show();
      }
      document.getElementById(feedId).getElementsByClassName('badge')[0].innerHTML = feedCounter;
    });
  });
}

function initAddFeed() {
  var addFeed = getAddFeedTemplate();
  $('#add').popover({'title': "<center>New feed</center>",
                     'html': true,
                     'content': addFeed.outerHTML,
                     'placement': "bottom"}
  );
  $("#add").on('click', function(){
    $("#urlFeed").focus();
  });
}

function initPage() {
  // Remove anchors binding for mobile view
  $(".feed").click(function(e) {  
    e.preventDefault();
  });

  initAddFeed()
  setInterval(refreshCounters, 120000);
}

$(document).ready(function() {
  // Globals
  requests = new Array();
  importer = false;
});
