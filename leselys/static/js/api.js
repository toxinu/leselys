api = {};

api.changePassword = function(password, callback) {
    return ajaxRequest({
        url: 'api/set_password',
        method: 'POST',
        params: {
            password: password
        },
        callback: callback
    });
}

api.addFeed = function(feedUrl, callback) {
    return ajaxRequest({
        url: 'api/add',
        method: 'POST',
        params: {
            url: feedUrl
        },
        callback: callback
    });
}

api.deleteFeed = function(feedId, callback) {
    return ajaxRequest({
        url: 'api/remove/' + feedId,
        method: 'DELETE',
        callback : callback
    });
}

api.setFeedSetting = function(feedId, settingKey, settingValue, callback) {
    return ajaxRequest({
        url: 'api/feedsettings',
        method: 'POST',
        params: {
            feed_id: feedId,
            key: settingKey,
            value: settingValue
        },
        callback: callback
    });
}

api.importOPML = function(file, callback) {
    return sendFile({
        url: 'api/import/opml',
        params: {
            fileInput: file
        },
        callback: callback
    });
}

api.getSettings = function(callback) {
    return ajaxRequest({
        url: 'settings',
        method: 'GET',
        params: {
            jsonify: true
        },
        callback: callback
    });
}

api.getHome = function(callback) {
    return ajaxRequest({
        url: '.',
        method: 'GET',
        params: {
            jsonify: true
        },
        callback: callback
    });
}

api.getFeed = function(feedId, start, stop, callback) {
    var start = start || 0;
    var stop = stop || 50;
    return ajaxRequest({
        url: 'api/get/' + feedId,
        params: {
            start: start,
            stop: stop
        },
        method: 'GET',
        callback: callback
    });
}

api.readStory = function(storyId, callback) {
    return ajaxRequest({
        url: 'api/read/' + storyId,
        method: 'GET',
        callback: callback
    });
}

api.unreadStory = function(storyId, callback) {
    return ajaxRequest({
        url: 'api/unread/' + storyId,
        method: 'GET',
        callback: callback
    });
}

api.setTheme = function(themeName, callback) {
    return ajaxRequest({
        url: 'api/settings/theme',
        method: 'POST',
        params: {
            theme: themeName
        },
        callback: callback
    });
}

api.getCounters = function(callback) {
    return ajaxRequest({
        url: 'api/counters',
        method: 'GET',
        callback: callback
    });
}

api.markAllAsRead = function(feedId, callback) {
    return ajaxRequest({
        url: 'api/all_read/' + feedId,
        method: 'GET',
        callback: callback
    });
}

api.markAllAsUnread = function(feedId, callback) {
    return ajaxRequest({
        url: 'api/all_unread/' + feedId,
        method: 'GET',
        callback: callback
    });
}
