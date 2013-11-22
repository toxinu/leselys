'use strict';
var leselysServices = angular.module('leselysServices', []);

leselysServices.service('Reader', ['$http', function($http) {
	var Reader = {};
    Reader.folders = [];
    Reader.subscriptions = [];
    Reader.stories = [];
    Reader.getOrdering = function(callback) {
        $http.get('api/ordering', {cache:true}).success(function(data) {
            if (callback) callback(data);
        });
    };
    Reader.getFolders = function(callback) {
    	if (!Reader.folders.length) {
    		$http.get('api/folder').success(function(data) {
    			Reader.folders = data;
				if (callback) callback(data);
			});
		} else
			if (callback) callback(Reader.folders);
	};
    Reader.getSubscriptions = function(callback) {
    	if (!Reader.subscriptions.length) {
    		$http.get('api/subscription').success(function(data) {
    			Reader.subscriptions = data;
				if (callback) callback(data);
			});
		} else
			if (callback) callback(Reader.subscriptions);
    };
    Reader.getStories = function (subscription, callback) {
        $http.get('api/story?subscription=' + subscription.id).success(function(data) {
        	Reader.stories = data;
	   	   if (callback) callback(data);
    	});
    };
    Reader.getSubscription = function(subscriptionId, callback) {
    	angular.forEach(Reader.subscriptions, function(value) {
			if (value.id == subscriptionId)
				if (callback) callback(value); return;
		});
    };
    Reader.getStory = function(storyId, callback) {
      	$http.get('api/story/' + storyId, {cache:true}).success(function(data) {
			if (callback) callback(data);
		});
    };
    Reader.deleteSubscription = function(subscriptionId, callback) {
        $http.delete('api/subscription/' + subscriptionId).success(function(data) {
            angular.forEach(Reader.subscriptions, function(value, key) {
                if (value.id == subsscriptionId)
                    Reader.subscriptions.splice(key, 1); return;
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
                        Reader.getSubscription(value.subscription, function(subscription) {
                            subscription.unread_counter--;
                        });
                    };
                    Reader.stories[key].readed = data.readed;
                }
            });
            if (callback) callback();
        });
    };
    Reader.addFolder = function(folderName, callback) {
        $http.post('api/folder/', {name:folderName}).success(function(data) {
            Reader.folders.push(data);
            if (callback) callback(data);
        });
    };
    Reader.addSubscription = function(feedUrl, callback) {
    	$http.post('api/feed', {url:feedUrl}).
            success(function(data) {
    		  Reader.subscriptions.push(data);
                if (callback) callback(data);
            }).
            error(function(data) {
                console.log('!!erorr');
            });
    };
    Reader.renameFolder = function(folder, newName, callback) {
        $http.put('api/folder/' + folder.id, {name:newName}).success(function(data) {
            folder.name = newName;
            if (callback) callback(data);
        });
    };
    Reader.updateSubscription = function(subscription, callback) {
        $http.put('api/feed/' + subscription.id, feed).success(function(data) {
            if (callback) callback(data);
        });
    };
    Reader.polling = function(callback) {
        $http.get('api/polling').success(function(data) {
            console.log('request set')
        });
    };
    return Reader;
}]);
