'use strict';
var leselysControllers = angular.module('leselysControllers', []);

leselysControllers.controller('readerCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
		$scope.getFolders = function(callback) {
			$http.get('api/folder').success(function(data) {
				callback(data);
			});
		};
		$scope.getFeeds = function(callback) {
			$http.get('api/feed').success(function(data) {
				callback(data);
			});
		};
		$scope.getFeed = function(feedId, callback) {
			angular.forEach($scope.feeds, function(value) {
				if (value.id == feedId)
					callback(value); return;
			});
		};
		$scope.getStory = function(storyId, callback) {
			$http.get('api/story/' + storyId).success(function(data) {
				callback(data);
			});
		};
		$scope.getStories = function(selectedFeed, callback) {
			$http.get('api/story?feed=' + selectedFeed.id).success(function(data) {
				callback(data);
			});
		};

		// Get folders
		$scope.getFolders(function(folders) {
			$scope.folders = folders;
		});

		// Get feeds
		$scope.getFeeds(function(feeds) {
			$scope.feeds = feeds;
			// If feedId in url
			if ($routeParams.feedId)
				$scope.getFeed($routeParams.feedId, function(feed) {
					$scope.selectedFeed = feed;
				});
			// If feedId in url exists
			if ($scope.selectedFeed) {
				// Get stories
				$scope.getStories($scope.selectedFeed, function(stories) {
					$scope.stories = stories;
					// If storyId in url
					if ($routeParams.storyId)
						$scope.getStory($routeParams.storyId, function(story) {
							$scope.selectedStory = story;
						});
				});
			}
		});
}]);


leselysControllers.controller('settingsCtrl', ['$scope', function($scope) {

}]);
