'use strict';
var leselysControllers = angular.module('leselysControllers', []);

leselysControllers.controller('readerCtrl', ['$scope', '$http', '$routeParams', '$timeout', 'Reader', function($scope, $http, $routeParams, $timeout, Reader) {
	$scope.getStoryClass = function(story) {
		if (story.id == $scope.selectedStory.id)
			return 'strong';
		if (story.readed)
			return 'text-muted';
	};
	$scope.readStory = function(story) {
		Reader.readStory(story, function() {
			Reader.getSubscriptions(function(subscriptions) {
				$scope.subscriptions = subscriptions;
				Reader.getStories($scope.selectedSubscription, function(stories) {
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
	$scope.selectedSubscription = {};
	// Get subscriptions
	Reader.getSubscriptions(function(subscriptions) {
		$scope.subscriptions = subscriptions;
		// If subscriptionId in url
		if ($routeParams.subscriptionId) {
			Reader.getSubscription($routeParams.subscriptionId, function(subscription) {
				$scope.selectedSubscription = subscription;
			});
			// Get stories
			Reader.getStories($scope.selectedSubscription, function(stories) {
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

	// Polling
	(function tick() {
        Reader.polling(function(data){
        	$scope.polls = data;
        });
        $timeout(tick, 10000);
    })();
}]);


leselysControllers.controller('settingsCtrl', ['$scope', 'Reader', function($scope, Reader) {
	$scope.addFolder = function(folderName) {
		Reader.addFolder(folderName, function() {
			$scope.folder.name = "";
		});
	};
	$scope.renameFolder = function(folder, newName) {
		Reader.renameFolder(folder, newName, function() {
			folder.settingsOpen = false;
			$scope.newName = "";
		});
	};
	$scope.deleteSubscription = function(subscription) {
		Reader.deleteSubscription(subscription.id);
	};
	$scope.deleteFolder = function(folder) {
		Reader.deleteFolder(folder.id);
	};
	$scope.updateSubscription = function(subscription) {
		Reader.updateSubscription(subscription, function(){
			subscription.settingsOpen = false;
		});
	};
	$scope.addSubscription = function(subscriptionUrl) {
		Reader.addSubscription(subscriptionUrl);
	};

	Reader.getFolders(function(folders) {
		$scope.folders = Reader.folders;
		Reader.getSubscriptions(function(subscriptions) {
			$scope.subscriptions = Reader.subscriptions;
		});
	});
	Reader.getOrdering(function(ordering) {
		$scope.ordering = ordering;
	});
}]);

leselysControllers.controller('navbarCtrl', ['$scope', '$route', 'Reader', function($scope, $route, Reader) {
	$scope.addSubscription = function(feedUrl) {
		Reader.addSubscription(feedUrl);
	};
	$scope.getClass = function(menuName) {
		if ($route.current) {
			if ($route.current.state == 'read' && menuName == 'home')
				return 'active';
			if ($route.current.state == 'settings' && menuName == 'settings')
				return 'active';
			if ($route.current.state == 'about' && menuName == 'about')
				return 'active';
		} else
			return '';
	};
}]);
