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

        /* vars related to database info*/
        $scope.curr_cals = [];
        $scope.curr_users = [];

        $scope.curr_cal = {
            id: "",
            user_id: "",
            date: "",
            time: "",
            amnt: "",
            text: ""
        };

        $scope.post_cal = {
            id: "",
            user_id: "",
            date: "",
            time: "",
            amnt: "",
            text: ""
        };

        $scope.curr_user = {
            id: "",
            username: "",
            user_type: "",
            exp_cal: ""           
        };

        $scope.post_user = {
            id: "",
            username: "",
            user_type: "",
            exp_cal: ""            
        };

        $scope.log_user = {
            id: "",
            username: "",
            user_type: "",
            exp_cal: ""   
        };

        /* vars related to user actions */
        $scope.viewingCalories = false;
        $scope.viewingCalorie = false;
        $scope.postingCalorie = false;
        $scope.addingCalorie = false;
        $scope.editingCalorie = false;


        /* permissions determiner functions */

        $scope.canCRUDSelf = function() {
            return $scope.log_user.user_type == 1 || 
                   $scope.log_user.user_type == 2 || 
                   $scope.log_user.user_type == 3;
        };

        $scope.canCRUDUsers = function() {
            return $scope.log_user.user_type == 2 || 
                   $scope.log_user.user_type == 3;
        };

        $scope.canCRUDAll = function() {
            return $scope.log_user.user_type == 3;
        };

        /* object functions */

        // sets the total data available to views by user type
        // makes ajax calls to get the data
        $scope.setTotalDataByUser = function() {
            if ($scope.canCRUDAll()) {
                $scope.getUsers({}, $scope.setUsersFromServer);
                $scope.getCalories({}, $scope.setCalsFromServer);
            }
            else if ($scope.canCRUDUsers()) {
                $scope.getUsers({}, $scope.setUsersFromServer);
                $scope.getCalories({user_id:$scope.log_user.id}, $scope.setCalsFromServer);
            }
            else if ($scope.canCRUDSelf()) {
                $scope.getCalories({user_id: $scope.log_user.id}, $scope.setCalsFromServer);
            }
        };

        // resets current calories with calories from the server
        $scope.setCalsFromServer = function (data) {

            $scope.curr_cals = [];
            $scope.pushCalsFromServer(data);
        };

        // reset current users with users from server
        $scope.setUsersFromServer = function (data) {

            /*
            $scope.curr_users = [];
            $scope.pushUsersFromServer(data);           
            */
        };

        /* calorie view functions */

        // set the currently selected calorie to the given calorie
        $scope.setCurrCalorie = function(data, isClear) {

            $scope.curr_cal.id = isClear ? "" : data.data.calorie_id;
            $scope.curr_cal.user_id = isClear ? "" : data.data.user_id;
            $scope.curr_cal.date = isClear ? "" : data.data.date;
            $scope.curr_cal.time = isClear ? "" : data.data.time;
            $scope.curr_cal.amnt = isClear ? "" : data.data.num_calories;
            $scope.curr_cal.text = isClear ? "" : data.data.text;
        };

        // toggle the total calorie view on or off
        $scope.toggleViewCalories = function(isShow) {
            if (isShow) {
                $scope.viewingCalories = true;
            }
            else {
                $scope.viewingCalories = false;
                $scope.toggleViewCalorie(false);
            }
        };   

        // toggle the specific calorie view on or off
        $scope.toggleViewCalorie = function(isShow) {
            if (isShow) {
                $scope.viewingCalorie = true;
            }
            else {
                $scope.viewingCalorie = false;
                $scope.togglePostCalorie(false, false);
            }
        };

        // toggle the add/edit calorie form on or off
        $scope.togglePostCalorie = function(isShow, isAdd) {

            if (isShow) {
                if (isAdd) {
                    $scope.addingCalorie = true;
                    $scope.setPostCalorie(true);
                }
                else {
                    $scope.editingCalorie = true;
                    $scope.setPostCalorie(false);
                }
            }
            else {
                $scope.addingCalorie = false;
                $scope.editingCalorie = false;
                $scope.setPostCalorie(true);
            }
        };

        // set the information for the calorie to be posted
        $scope.setPostCalorie = function(isClear) {
            console.log($scope.post_cal);
            $scope.post_cal.id = isClear ? "" : $scope.curr_cal.id;
            $scope.post_cal.user_id = isClear ? "" : $scope.curr_cal.user_id;
            $scope.post_cal.date = isClear ? "" : $scope.curr_cal.date;
            $scope.post_cal.time = isClear ? "" : $scope.curr_cal.time;
            $scope.post_cal.amnt = isClear ? "" : $scope.curr_cal.amnt;
            $scope.post_cal.text = isClear ? "" : $scope.curr_cal.text;
            console.log($scope.post_cal);
        };

        // initiate ajax call to post a calorie to server database
        $scope.postCalorie = function() {

            if ($scope.addingCalorie) {
                $scope.addCalorie($scope.pushCalorie);
            }
            else if ($scope.editingCalorie) {
                $scope.editCalorie($scope.pushCalorie);
            }
        };

        // do ajax call to add calorie to server database
        $scope.addCalorie = function(callback) {

            // TO-DO:loading graphic
            var user_id = $scope.log_user.id;
            var date = $scope.post_cal.date;
            var time = $scope.post_cal.time;
            var text = $scope.post_cal.text;
            var amnt = $scope.post_cal.amnt;

            $http({
                method:'POST',
                url: "/add_calorie?user_id="+user_id+"&date="+date+"&time="+time+"&text="+text+"&amnt="+amnt,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                callback(resp.data);
            },function(error){
                console.log('There was an error adding calories to the server');
                console.log(error);
            });
        };

        // do ajax call to edit calorie in server database
        $scope.editCalorie = function() {

        };

        // do ajax call to delete a calorie from server database
        $scope.deleteCalorie = function() {

        };

        // push calories from server to the current calorie list
        $scope.pushCalsFromServer = function(data) {

            for (var i = 0; i < data.length; i++) {
                $scope.curr_cals.push({
                    id: data[i].data.calorie_id,
                    user_id: data[i].data.user_id,
                    date: data[i].data.date,
                    time: data[i].data.time,
                    amnt: data[i].data.num_calories,
                    text: data[i].data.text
                });           
            }
        };

        // push users from server to the current user list
        $scope.pushUsersFromServer = function(data) {
            /*
            for (var i = 0; i < data.length; i++) {
                $scope.curr_cals.push({
                    id: data[i].data.calorie_id,
                    user_id: data[i].data.user_id,
                    date: data[i].data.date,
                    time: data[i].data.time,
                    amnt: data[i].data.num_calories,
                    text: data[i].data.text
                });           
            }*/
        };

        $scope.getCalories = function(data, callback) {

            // TO-DO:loading graphic

            console.log(data);

            var calorie_id = data.hasOwnProperty(calorie_id) ? data.calorie_id : "";
            var user_id = data.hasOwnProperty(user_id) ? data.user_id : "";
            var date_from = data.hasOwnProperty(date_from) ? data.date_from : "";
            var date_to = data.hasOwnProperty(date_to) ? data.date_to : "";
            var time_from = data.hasOwnProperty(time_from) ? data.time_from : "";
            var time_to = data.hasOwnProperty(time_to) ? data.time_to : "";

            $http({
                method:'GET',
                url: '/calorie?id='+calorie_id+'&user_id='+user_id+"&date_from="+date_from+"&date_to="+date_to+"&time_from="+time_from+"&time_to="+time_to,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                callback(resp.data);
            },function(error){
                console.log('There was an error retrieving calories from the server: ' + error);
            });
        };

        /* user view functions */
        
        // set the currently selected user to the given user
        $scope.setCRUDUserInfo = function(isClear, data) {
            $scope.crud_user_id = isClear ? "" : data.data.user_id;
            $scope.crud_username = isClear ? "" : data.data.username;
            $scope.crud_user_type = isClear ? "" : data.data.user_type;
            $scope.crud_exp_cal = isClear ? "" : data.data.exp_cal;
        };

        $scope.toggleViewUsers = function(isShow) {

        };   

        $scope.toggleViewUser = function(isShow) {

        };

        /* signin/out functions */

        // set the logged in user to the given user
        $scope.setLoggedInUserInfo = function(isClear, data) {
            $scope.log_user.id = isClear ? "" : data.data.user_id;
            $scope.log_user.username = isClear ? "" : data.data.username;
            $scope.log_user.user_type = isClear ? "" : data.data.user_type;
            $scope.log_user.exp_cal = isClear ? "" : data.data.exp_cal;
        };

        $scope.isSignedIn = function() {
            return $scope.log_user.username.length > 0;
        };

        // handle server OAuth ajax call with auth code from Google 
        $scope.signin = function(authResult) {
            console.log("trying ajax from angular");

            // TO-DO:loading graphic

            $http({
                method:'POST',
                url: '/gconnect?state=' + angular.element("#state").html(),
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                },
                data: authResult['code']
            })
            .then(function(resp){
                console.log(resp);
                $scope.setLoggedInUserInfo(false, resp);
                $scope.setTotalDataByUser();
            },function(error){
                console.log(error);
                console.log('There was an error: ' + authResult['error']);
            });
        };

        $scope.signout = function(forUserDeletion=0) {
            // TO-DO: update this method
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
        };
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
