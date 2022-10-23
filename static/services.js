(function () {
    'use strict';
    
    angular
        .module('app')
        .controller('HomeController', HomeController);
    
    HomeController.$inject = ['UserService', '$rootScope'];
    function HomeController(UserService, $rootScope) {
    
        $rootScope.bodylayout ='main_page_que';
        var vm = this;
    }
	
	app.factory('socket', function ($rootScope) {
	  var socket = io.connect();
	  return {
		on: function (eventName, callback) {
		  socket.on(eventName, function () {  
			var args = arguments;
			$rootScope.$apply(function () {
			  callback.apply(socket, args);
			});
		  });
		},
		emit: function (eventName, data, callback) {
		  socket.emit(eventName, data, function () {
			var args = arguments;
			$rootScope.$apply(function () {
			  if (callback) {
				callback.apply(socket, args);
			  }
			});
		  })
		}
	  };
	});
    })();