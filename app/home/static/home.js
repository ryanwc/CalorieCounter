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

        $scope.signin = function(authResult) {
            console.log("trying ajax from angular");

            //loading graphic //$('#signIn').addClass('hiddenClass');

            // make ajax call to server to connect with oauth and handle result
            $http({
                method:'POST', // processData: false,
                url: '/gconnect?state=' + angular.element("#state").html(), // 'http://127.0.0.1:5000/signin', 
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data: authResult['code']
            })
            .then(function(resp){
                console.log(resp);
                $scope.handleSignInResult(resp);
            },function(error){
                console.log(error);
                console.log('There was an error: ' + authResult['error']);
            });

        };

        // make ajax call to server to connect with oauth and handle result
        $scope.handleSignInResult = function connect(urlWithState, data) {
            resultObj = JSON.parse(result);      
            // do stuff
        }

        $scope.signout = function(forUserDeletion=0) {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                    window.alert(xhttp.responseText);
                    if (forUserDeletion == 1) {
                        // returns to delete form onsubmit so lets deletion proceed
                        return true;
                    }
                    else {
                        location.reload();
                    }
                }
                else if (forUserDeletion == 1) {
                    return false;
                }
            }
            xhttp.open("POST", "/disconnect", true);
            xhttp.send();
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

// callback when Google sends the user access code
function signInCallback(authResult) {

    console.log("called back");
    console.log(authResult);

    if (authResult['code']) {
        angular.element(document.getElementById('homeCtrlDiv')).scope().signin(authResult);   
    }
}
