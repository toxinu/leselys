function addFeed() {
  if (document.getElementById('urlFeed').innerHTML == '') { return false }

  // Clear help message if no subscriptions
  if ($("ul#menu li#empty-feed-list").length) {
    $("ul#menu li#empty-feed-list").hide();
    $("ul#menu li#listSubscriptions").show();
  }
  var loader = $('<li><i class="icon-tasks"></i> Loading...</li>');
  $("ul#menu").append(loader);
  $.post('/api/add', {url: url}, function(data) {
    if (data.success == true) {
      /////////////////////////////////////
      // Go login page if not connected ///
      if ($(data).find('.form-signin').length > 0) {
        window.location = "/login";
      }
      /////////////////////////////////////
      $(loader).hide();
      $(loader).html('<a onClick="viewSubscription(&quot;' + data.feed_id + '&quot;)" href="/#' + data.feed_id + '">' + data.title + ' <span id="unread-counter" class="badge badge-inverse">' + data.counter  + '</span></a>').fadeIn();
      $(loader).attr('id', data.feed_id);
      $(loader).addClass('story');
      // Add new feed in settings/feeds if opened
      if ($('#settings.tab-pane').length > 0) {
        // Remove message if feeds list is empty
        if ($('#feeds.tab-pane #empty-feed-list').length > 0) {
          $('#feeds.tab-pane #empty-feed-list').hide();
        }
        $('#feeds.tab-pane ul').append('<li id="' +  data.feed_id + '">' + data.title + ' <a onClick="delSubscription(&quot;' + data.feed_id + '&quot;);" href="#">(delete)</a></li>');
      }
    } else {
      /////////////////////////////////////
      // Go login page if not connected ///
      if ($(data).find('.form-signin').length > 0) {
        window.location = "/login";
      }
      /////////////////////////////////////
      $(loader).html('<li><i class="icon-exclamation-sign"></i> Error: ' + data.output +'</li>');
      var clearLoader = function() {
        $(loader).fadeOut();
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
        /////////////////////////////////////
        // Go login page if not connected ///
        if ($(data).find('.form-signin').length > 0) {
          window.location = "/login";
        }
        /////////////////////////////////////
        if (data.success == true) {
          importer = false;
          document.getElementById("OPMLSubmit").innerHTML = "Importing, reload page later...";
          $('#OPMLSubmit').addClass('disabled');
        }
      });
    }
  })(file);
  reader.readAsText(file);
}

function viewSettings() {
  $.get('/settings', function(body) {
    /////////////////////////////////////
    // Go login page if not connected ///
    if ($(body).find('.form-signin').length > 0) {
      window.location = "/login";
    }
    /////////////////////////////////////
    var content = $(body).find('#content');
    var sidebar = $(body).find('#menu')
    document.getElementById("content").innerHTML = content.html();
    document.getElementById("menu").innerHTML = sidebar.html()
    if (importer) {
      document.getElementById("OPMLSubmit").innerHTML = "Last import not finished...";
      $('#OPMLSubmit').addClass('disabled');
      return false;
    }
    if ($('#OPMLSubmit').length > 0) {
      document.getElementById('OPMLSubmit').addEventListener('click', handleOPMLImport, false);
    }
    initAddFeed();
  });
}

function viewHome() {
  $.get('/', function(body) {
    /////////////////////////////////////
    // Go login page if not connected ///
    if ($(body).find('.form-signin').length > 0) {
      window.location = "/login";
    }
    /////////////////////////////////////
    var content = $(body).find('#content');
    var sidebar = $(body).find('#menu')
    document.getElementById("content").innerHTML = content.html();
    document.getElementById("menu").innerHTML = sidebar.html()
    initAddFeed();
  });
}

function delFeed(feedId) {
  $.ajax({
    url: '/api/remove/' + feedId,
    type: 'DELETE',
    success: function(result) {
      /////////////////////////////////////
      // Go login page if not connected ///
      if ($(result).find('.form-signin').length > 0) {
        window.location = "/login";
      }
      /////////////////////////////////////
      $('#feeds ul li#' + feedId).fadeOut(300, function() {
        $(this).remove();
        if ($('#feeds ul li').length < 1) {
          $('#feeds.tab-pane #empty-feed-list').fadeIn(200);
        }
      });
      $('ul#menu li#' + feedId).fadeOut(300, function() {
        $(this).remove();
        if ($('ul#menu li').length < 6) {
          $('ul#menu li#listFeeds.nav-header').fadeOut(200);
          $('ul#menu li#empty-feed-list').fadeIn(200);
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
    /////////////////////////////////////
    // Go login page if not connected ///
    if ($(data).find('.form-signin').length > 0) {
      window.location = "/login";
    }
    /////////////////////////////////////
    var header = '<div class="accordion" id="story-list-accordion">';
    var footer = '</div>';
    var content = '';

    $.each(data.content, function(i,item){
      var storyId = item._id;
      var storyTitle = item.title;
      var storyAccordion = getStoryAccordionTemplate();

      storyAccordion.id = storyId;
      storyAccordion.getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '")';
      storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
      storyAccordion.getElementsByClassName("accordion-toggle")[0].innerHTML = storyTitle;

      storyAccordion.getElementsByClassName("accordion-toggle")[0].setAttribute("data-target", "#" + storyId + "-body");
      storyAccordion.getElementsByClassName("accordion-body")[0].id = storyId + "-body";

      if (item.read == false) {
        storyAccordion.getElementsByClassName('accordion-toggle')[0].style.fontWeight = "bold";
      }

      content += storyAccordion.outerHTML;
    });
    document.getElementById('content').innerHTML = header + content + footer;
    $('#menu a').each(function(index) {
      $(this).css('font-weight', 'normal');
    });
    $('#menu li#' + feedId + " a").css('font-weight', 'bold');
  });
  requests.push(request);
}

function refreshFeeds() {
  $.each($('#menu .story'), function(i, story) {
    var feedId = $(story).attr('id');
    $.getJSON('/api/refresh/' + feedId), function(data) {
      /////////////////////////////////////
      // Go login page if not connected ///
      if ($(data).find('.form-signin').length > 0) {
        window.location = "/login";
      }
      /////////////////////////////////////
      var feedTitle = data.content.title;
      var feedCounter = data.content.counter;
      $("#menu a[href=#" + feedId + "] span.badge").html(feedCounter);
    }
  });
}

function readStory(storyId, ignore) {
  // // Avoid "read" state if story have just been marked unread
  var ignore = ignore || false;
  if (ignore == true) {
    document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '")';
    document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
    return true
  }

  $.getJSON('/api/read/' + storyId, function(data) {
    /////////////////////////////////////
    // Go login page if not connected ///
    if ($(data).find('.form-signin').length > 0) {
      window.location = "/login";
    }
    /////////////////////////////////////
    if (data.content.last_update == false) {
      var published = "No date";
    } else {
      var published = data.content.last_update['year'] + '-' + data.content.last_update['month'] +
                    '-' + data.content.last_update['day'];
    }

    var feedId = data.content.feed_id;
    var story = getStoryTemplate();

    story.getElementsByClassName("story-link")[0].href = data.content.link;
    story.getElementsByClassName("story-read-toggle")[0].onclick = 'unreadStory("' + storyId + '")';
    story.getElementsByClassName("story-read-toggle")[0].setAttribute("onclick", 'unreadStory("' + storyId + '")');
    story.getElementsByClassName("story-read-toggle")[0].innerHTML = 'Mark as unread';
    story.getElementsByClassName("story-content")[0].innerHTML = data.content.description;
    story.getElementsByClassName("story-date")[0].innerHTML = published;

    document.getElementById(storyId).getElementsByClassName("accordion-body")[0].innerHTML = story.outerHTML;
    if (data.success == true) {
      var counter = parseInt($("#menu li#" + feedId + " #unread-counter").html()) - 1;
      if (counter == 0) {
        $("#menu li#" + feedId + " #unread-counter").html(counter);
        $("#menu li#" + feedId + " #unread-counter").fadeOut();
      } else {
        $("#menu li#" + feedId + " #unread-counter").html(counter);
      }
    }
  });
  document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].style.fontWeight = 'normal';
}

function unreadStory(storyId) {
  $.getJSON('/api/unread/' + storyId, function(data) {
    /////////////////////////////////////
    // Go login page if not connected ///
    if ($(data).find('.form-signin').length > 0) {
      window.location = "/login";
    }
    /////////////////////////////////////
    if (data.success == true) {
      var feedId = data.content.feed_id;
      var story = document.getElementById(storyId);

      // Avoid next click on story title
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].onclick = 'readStory("' + storyId + '", true)';
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '", true)');

      story.getElementsByClassName("story-read-toggle")[0].onclick = 'readStory("' + storyId + '")';
      story.getElementsByClassName("story-read-toggle")[0].setAttribute("onclick", 'readStory("' + storyId + '")');
      story.getElementsByClassName("story-read-toggle")[0].innerHTML = 'Mark as read';

      var counter = parseInt($("#menu li#" + feedId + " #unread-counter").html()) + 1;

      $('a[href=#' + storyId + ']').data('unreaded', true);
      if (counter == 1) {
        $("#menu li#" + feedId + " #unread-counter").html(counter);
        $("#menu li#" + feedId + " #unread-counter").fadeIn();
      } else {
        $("#menu li#" + feedId + " #unread-counter").html(counter);
      }
      document.getElementById(storyId).getElementsByClassName("accordion-toggle")[0].style.fontWeight = 'bold';
    }
  });
}

function initAddFeed() {
  var addFeed = getAddFeedTemplate();
  $('#add').popover({'title': "<center>New feed</center>",
                     'html': true,
                     'content': addFeed.outerHTML,
                     'placement': "bottom"}
  );
}

$(document).ready(function(){
  // Globals
  // Remove anchors binding for mobile view
  $('.feed').click(function(e) {
    e.preventDefault();
  });
  $('.accordion-group').click(function(e) {
    e.preventDefault();
  });
  $('.accordion-body').click(function(e) {
    e.preventDefault();
  });
  requests = new Array();
  importer = false;
});