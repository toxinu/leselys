'use strict';
var leselysServices = angular.module('leselysServices', []);

leselysServices.service('Reader', ['$http', function($http) {
	var Reader = {};
    Reader.folders = null;
    Reader.feeds = null;
    Reader.stories = null;
    Reader.getFolders = function(callback) {
    	if (!Reader.folders) {
    		$http.get('api/folder').success(function(data) {
    			Reader.folders = data;
				callback(data);
			});
		} else
			callback(Reader.folders);
	};
    Reader.getFeeds = function(callback) {
    	if (!Reader.feeds) {
    		$http.get('api/feed').success(function(data) {
    			Reader.feeds = data;
				callback(data);
			});
		} else
			callback(Reader.feeds);
    };
    Reader.getStories = function (feed, callback) {
        if (!Reader.stories) {
        	$http.get('api/story?feed=' + feed.id).success(function(data) {
        		Reader.stories = data;
				callback(data);
			});
        } else
        	callback(Reader.stories);
    };
    Reader.getFeed = function(feedId, callback) {
    	angular.forEach(Reader.feeds, function(value) {
			if (value.id == feedId)
				callback(value); return;
		});
    };
    Reader.getStory = function(storyId, callback) {
      	$http.get('api/story/' + storyId, {cache:true}).success(function(data) {
			callback(data);
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
            callback();
        });
    };
    Reader.addFeed = function(feedUrl, callback) {
    	$http.post('api/feed', {url:feedUrl, folder:1}).success(function(data) {
            if (!Reader.stories)
                Reader.stories = {};
    		Reader.stories.push(data);
    		callback(data);
    	});
    };
    return Reader;
}]);
