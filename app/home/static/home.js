// angular Calorie Counter app

var ccapp = angular.module("ccapp", []);

(function(){
    "use strict";

    console.log("init angular home controller");
    // make jinja2 play with angular
    ccapp.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');
    });

    ccapp.controller("homeCtrl", function($scope, $http) {

        $scope.username = "";

        $scope.isSignedIn = function() {
            return $scope.username.length > 0;
        };

        $scope.signin = function() {
            console.log("trying ajax");
            $http({
                method:'POST',
                url:'http://127.0.0.1:5000/signin',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data:{username:'ryan',password:'connor'}
            })
            .then(function(resp){
                console.log(resp);
            },function(error){
                console.log(error);
            });
        };

        $scope.signout = function($event) {

        }
    });
})(ccapp);

/*
// Declare app level module which depends on views, and components
angular.module('ccapp', [
    'ngRoute',
    'ccapp.home'
])
.config(function($routeProvider) {
    $routeProvider
        .when('/home', {
            controller: 'HomeCtrl',
        })
        .otherwise({
            redirectTo: '/'
        });
});
*/

function signInCallback() {

}
