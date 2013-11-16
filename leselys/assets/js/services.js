'use strict';
var leselysServices = angular.module('leselysServices', []);

leselysServices.service('Reader', ['$http', function($http) {
	var Reader = {};
    Reader.folders = [];
    Reader.feeds = [];
    Reader.stories = [];
    Reader.getFolders = function(callback) {
    	if (!Reader.folders.length) {
    		$http.get('api/folder').success(function(data) {
    			Reader.folders = data;
				if (callback) callback(data);
			});
		} else
			if (callback) callback(Reader.folders);
	};
    Reader.getFeeds = function(callback) {
    	if (!Reader.feeds.length) {
    		$http.get('api/feed').success(function(data) {
    			Reader.feeds = data;
				if (callback) callback(data);
			});
		} else
			if (callback) callback(Reader.feeds);
    };
    Reader.getStories = function (feed, callback) {
        $http.get('api/story?feed=' + feed.id).success(function(data) {
        	Reader.stories = data;
	   	   if (callback) callback(data);
    	});
    };
    Reader.getFeed = function(feedId, callback) {
    	angular.forEach(Reader.feeds, function(value) {
			if (value.id == feedId)
				if (callback) callback(value); return;
		});
    };
    Reader.getStory = function(storyId, callback) {
      	$http.get('api/story/' + storyId, {cache:true}).success(function(data) {
			if (callback) callback(data);
		});
    };
    Reader.deleteFeed = function(feedId, callback) {
        $http.delete('api/feed/' + feedId).success(function(data) {
            angular.forEach(Reader.feeds, function(value, key) {
                if (value.id == feedId)
                    Reader.feeds.splice(key, 1); return;
            });
            if (callback) callback(data);
        });
    };
    Reader.deleteFolder = function(folderId, callback) {
       $http.delete('api/folder/' + folderId).success(function(data) {
            angular.forEach(Reader.folders, function(value, key) {
                if (value.id == folderId)
                    Reader.folders.splice(key, 1); return;
            });
            if (callback) callback(data);
        });
    };
    Reader.readStory = function(story, callback) {
        $http.put('api/story/' + story.id, {readed:true}).success(function(data) {
            angular.forEach(Reader.stories, function(value, key){
                if (value.id == data.id) {
                    if (!value.readed && data.readed){
                        Reader.getFeed(value.feed, function(feed) {
                            feed.unread_counter--;
                        });
                    };
                    Reader.stories[key].readed = data.readed;
                }
            });
            if (callback) callback();
        });
    };
    Reader.addFolder = function(folderName, callback) {
        $http.post('api/folder', {name:folderName}).success(function(data) {
            Reader.folders.push(data);
            if (callback) callback(data);
        });
    };
    Reader.addFeed = function(feedUrl, callback) {
    	$http.post('api/feed', {url:feedUrl, folder:1}).success(function(data) {
    		Reader.feeds.push(data);
            if (callback) callback(data);
    	});
    };
    Reader.renameFolder = function(folder, newName, callback) {
        $http.put('api/folder/' + folder.id, {name:newName}).success(function(data) {
            folder.name = newName;
            if (callback) callback(data);
        });
    };
    Reader.updateFeed = function(feed, callback) {
        $http.put('api/feed/' + feed.id, feed).success(function(data) {
            if (callback) callback(data);
        });
    };
    return Reader;
}]);
