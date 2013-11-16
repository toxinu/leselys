'use strict';
var leselysControllers = angular.module('leselysControllers', []);

leselysControllers.controller('homeCtrl', ['$scope', 'Reader', function($scope, Reader) {
	$scope.addFeed = function(feedUrl) {
		Reader.addFeed(feedUrl);
	}
}]);

leselysControllers.controller('readerCtrl', ['$scope', '$http', '$routeParams', 'Reader', function($scope, $http, $routeParams, Reader) {
	$scope.getStoryClass = function(story) {
		if (story.id == $scope.selectedStory.id)
			return 'strong';
		if (story.readed)
			return 'text-muted';
	};
	$scope.readStory = function(story) {
		Reader.readStory(story, function() {
			Reader.getFeeds(function(feeds) {
				$scope.feeds = feeds;
				Reader.getStories($scope.selectedFeed, function(stories) {
					$scope.stories = stories;
				});
			});
		});
	};
	// Get folders
	Reader.getFolders(function(folders) {
		$scope.folders = folders;
	});
	$scope.selectedStory = {};
	$scope.selectedFeed = {};
	// Get feeds
	Reader.getFeeds(function(feeds) {
		$scope.feeds = feeds;
		// If feedId in url
		if ($routeParams.feedId) {
			Reader.getFeed($routeParams.feedId, function(feed) {
				$scope.selectedFeed = feed;
			});
			// Get stories
			Reader.getStories($scope.selectedFeed, function(stories) {
				$scope.stories = stories;
				// If storyId in url
				if ($routeParams.storyId)
					Reader.getStory($routeParams.storyId, function(story) {
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
