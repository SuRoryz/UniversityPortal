var app = angular.module('postserviceApp', ['ngRoute', 'myApp.directives']);

app.config(function ($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/templates/login.html',
        controller: 'postserviceCtrl'
    }).otherwise({
        template: '',
        controller: 'routeCtrl'
    })
})

app.controller('routeCtrl', function($scope, $http, socket, $location, $compile) {
	 
    $scope.logout = function () {
        $('.btn-logout').remove();

        $http({url: '/api/logout', method: "POST"
            }).then(function (response) {
                if (response.data) {

                    if (response.data.status) {
                        $location.path('/');
                    }
                }
        }, function (response) {

                    $location.path('/');

                });
    };

    $scope.text = null;
    $http({
        url: '' + $location.path(),
        method: "GET",
    }).then(function (response) {
        if (response.data) {
            if (response.data.status) {
                let Element = angular.element(document.querySelector('ng-view'));
                let el = $compile(response.data.message)($scope);

                Element.append(el)
            } else {
                $location.path('/')
            }
        } else {
            console.log('Error')
        }
    })
})

app.controller('postserviceCtrl', function ($scope, $http, $location) {
    $scope.email = null;
    $scope.password = null;
	
	$scope.api_call = function (type, data) {
		socket.emit(`api:${type}`, {
		  data: data
		}, function (result) {
		  if (!result) {
			alert('API ERROR');
		  } else {
			  if (result.error) {
				alert(reult.error.msg);
				return;
			  }
		  }
		});
	  };


    $scope.postdata = function (email, password) {
        var data = {
            email: email,
            password: password
        };
	

    $http({url: '/api/login', method: "POST",
    data: data, headers: {'Content-Type': 'application/json'}}).then(function (response) {
        if (response.data) {

            if (response.data.status) {
                console.log($location.path())
                $location.path('/supersecret')
            }

            $scope.msg = "Post Data Submitted Successfully!";
            $scope.statusval = response.status;
            $scope.statustext = response.statusText;
            $scope.headers = response.data.message

        }
}, function (response) {

    $scope.msg = "Service not Exists";
    $scope.statusval = response.status;
    $scope.statustext = response.statusText;
    $scope.headers = response.response;
        });
    };
});