'use strict';
var leselysControllers = angular.module('leselysControllers', []);

leselysControllers.controller('readerCtrl', ['$scope', '$http', '$routeParams', function($scope, $http, $routeParams) {
		$scope.getFolders = function(callback) {
			$http.get('api/folder', {cache:true}).success(function(data) {
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
		$scope.getStoryClass = function(story) {
			if (story.id == $scope.selectedStory.id)
				return 'strong';
			if (story.readed)
				return 'text-muted';
		};
		$scope.readStory = function(story) {
			$http.put('api/story/' + story.id, {readed:true}).success(function(data) {
				if (story.feed == $scope.selectedFeed.id) {
					angular.forEach($scope.stories, function(value, key){
						if (value.id == story.id) {
							console.log('READED', data.readed)
							$scope.stories[key].readed = data.readed;
						}
					});
				};
			});
		};
		// Get folders
		$scope.getFolders(function(folders) {
			$scope.folders = folders;
		});
		$scope.selectedStory = {};
		$scope.selectedFeed = {};

		// Get feeds
		$scope.getFeeds(function(feeds) {
			$scope.feeds = feeds;
			// If feedId in url
			if ($routeParams.feedId) {
				$scope.getFeed($routeParams.feedId, function(feed) {
					$scope.selectedFeed = feed;
				});
				// Get stories
				$scope.getStories($scope.selectedFeed, function(stories) {
					$scope.stories = stories;
					// If storyId in url
					if ($routeParams.storyId)
						$scope.getStory($routeParams.storyId, function(story) {
							$scope.selectedStory = story;
							if (!story.readed)
								$scope.readStory(story);
						});
				});
			}
		});
}]);


leselysControllers.controller('settingsCtrl', ['$scope', function($scope) {

}]);
