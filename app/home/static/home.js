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

    ccapp.controller("homeCtrl", function($scope, $http, $filter) {

        /* vars related to database info*/
        $scope.expCalMessage = "";

        $scope.curr_cal_dict = {};
        $scope.curr_user_dict = {};
        $scope.user_type_dict = {};

        $scope.curr_cal = {
            id: "",
            user_id: "",
            date_str: "",
            date: "",
            time_str: "",
            time: "",
            amnt: "",
            text: ""
        };

        $scope.post_cal = {
            id: "",
            user_id: "",
            date_str: "",
            date: "",
            time_str: "",
            time: "",
            amnt: "",
            text: ""
        };

        $scope.curr_user = {
            id: "",
            username: "",
            email: "",
            user_type_id: "",
            exp_cal_day: ""          
        };

        $scope.post_user = {
            id: "",
            username: "",
            email: "",
            user_type_id: "",
            exp_cal_day: ""         
        };

        $scope.log_user = {
            id: "",
            username: "",
            email: "",
            user_type_id: "",
            exp_cal_day: ""
        };

        /* vars related to user actions */
        $scope.viewingCalories = false;
        $scope.viewingCalorie = false;
        $scope.postingCalorie = false;
        $scope.addingCalorie = false;
        $scope.editingCalorie = false;

        $scope.viewingUsers = false;
        $scope.viewingUser = false;
        $scope.postingUser = false;
        $scope.addingUser = false;
        $scope.editingUser = false;

        /* permissions determiner functions */

        $scope.canCRUDSelf = function() {
            return $scope.log_user.user_type_id == 1 || 
                   $scope.log_user.user_type_id == 2 || 
                   $scope.log_user.user_type_id == 3;
        };

        $scope.canCRUDUsers = function() {
            return $scope.log_user.user_type_id == 2 || 
                   $scope.log_user.user_type_id == 3;
        };

        $scope.canCRUDAll = function() {
            return $scope.log_user.user_type_id == 3;
        };

        /* object functions */

        // sets the total data available to views by user type
        // makes ajax calls to get the data
        $scope.setTotalDataByUserType = function() {
            // fetch crudable calories and other users
            if ($scope.canCRUDAll()) {
                // get everything
                $scope.getUsers({}, $scope.setUsersFromServer);
                $scope.getCalories({}, $scope.setCalsFromServer);
            }
            else if ($scope.canCRUDUsers()) {
                // get all users, just logged in cals
                $scope.getUsers({}, $scope.setUsersFromServer);
                $scope.getCalories({id: $scope.log_user.id}, $scope.setCalsFromServer);
            }
            else if ($scope.canCRUDSelf()) {
                // get just logged in cals
                $scope.getCalories({id: $scope.log_user.id}, $scope.setCalsFromServer);
            }
        };

        // resets current calories with calories from the server
        $scope.setCalsFromServer = function (data) {
            $scope.curr_cal_dict = {};
            $scope.pushCalsFromServer(data);
        };

        // reset current users with users from server
        $scope.setUsersFromServer = function (data) {
            $scope.curr_user_dict = {};
            $scope.pushUsersFromServer(data);           
        };

        /* calorie view functions */

        // set the currently selected calorie to the given calorie
        $scope.setCurrCalorie = function(isClear, data) {

            $scope.curr_cal.id = isClear ? "" : data.id;
            $scope.curr_cal.user_id = isClear ? "" : data.user_id;
            $scope.curr_cal.date_str = isClear ? "" : data.date_str;
            $scope.curr_cal.date = isClear ? "" : data.date;
            $scope.curr_cal.time_str = isClear ? "" : data.time_str;
            $scope.curr_cal.time = isClear ? "" : data.time;
            $scope.curr_cal.amnt = isClear ? "" : data.amnt;
            $scope.curr_cal.text = isClear ? "" : data.text;
            console.log("curr cal is");
            console.log($scope.curr_cal);
        };

        // toggle the total calorie view on or off
        $scope.toggleViewCalories = function(isShow, userID) {
            if (isShow) {
                console.log($scope.curr_user_dict);
                $scope.setCurrUserInfo(false, $scope.curr_user_dict[parseInt(userID)]);
                $scope.viewingCalories = true;
            }
            else {
                $scope.viewingCalories = false;
                $scope.setCurrCalorie(true);
                $scope.toggleViewCalorie(false);
            }
        };   

        // toggle the specific calorie view on or off
        $scope.toggleViewCalorie = function(isShow, calID) {
            if (isShow) {
                $scope.viewingCalorie = true;
                $scope.setCurrCalorie(false, $scope.curr_cal_dict[parseInt(calID)]);
                $scope.togglePostCalorie(false, false);
            }
            else {
                $scope.viewingCalorie = false;
                $scope.setCurrCalorie(true);
                if (!$scope.addingCalorie) {
                    // if we're not adding a calorie, also turn cal form off
                    $scope.togglePostCalorie(false, false);
                }
            }
        };

        // toggle the add/edit calorie form on or off
        $scope.togglePostCalorie = function(isShow, isAdd) {

            if (isShow) {
                if (isAdd) {
                    $scope.addingCalorie = true;
                    $scope.editingCalorie = false;
                    $scope.setPostCalorie(true);
                    $scope.toggleViewCalorie(false);
                }
                else {
                    $scope.addingCalorie = false;
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
            $scope.post_cal.date_str = isClear ? "" : $scope.curr_cal.date_str;
            $scope.post_cal.date = isClear ? "" : $scope.curr_cal.date;
            $scope.post_cal.time_str = isClear ? "" : $scope.curr_cal.time_str;
            $scope.post_cal.time = isClear ? "" : $scope.curr_cal.time;
            $scope.post_cal.amnt = isClear ? "" : $scope.curr_cal.amnt;
            $scope.post_cal.text = isClear ? "" : $scope.curr_cal.text;
            console.log($scope.post_cal);
        };

        // initiate ajax call to post a calorie to server database
        $scope.postCalorie = function() {

            if ($scope.addingCalorie) {
                $scope.addCalorie($scope.pushCalsFromServer);
            }
            else if ($scope.editingCalorie) {
                $scope.editCalorie($scope.pushCalsFromServer);
            }
        };

        // do ajax call to add calorie to server database
        // pass list of calories from server to callback
        $scope.addCalorie = function(callback) {

            // TO-DO:loading graphic
            var user_id = $scope.curr_user.id;
            var date = $scope.post_cal.date.getFullYear() + "-" + ($scope.post_cal.date.getMonth()+1) + "-" + $scope.post_cal.date.getDate();
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
                callback(resp.data["Data"]);
                $scope.addingCalorie = false;
                $scope.editingCalorie = false;
                $scope.toggleViewCalorie(false);
                window.alert("Successfully added calorie");
            },function(error){
                window.alert('There was an error adding calorie to the server, check log');
                console.log(error);
            });
        };

        // do ajax call to edit calorie in server database
        $scope.editCalorie = function() {

            var calorie_id = $scope.post_cal.id;
            var user_id = $scope.curr_user.id;
            var date = $scope.post_cal.date.getFullYear() + "-" + ($scope.post_cal.date.getMonth()+1) + "-" + $scope.post_cal.date.getDate();
            var time = $scope.post_cal.time;
            var text = $scope.post_cal.text;
            var amnt = $scope.post_cal.amnt;

            $http({
                method:'POST',
                url: "/edit_calorie?calorie_id="+calorie_id+"&user_id="+user_id+"&date="+date+"&time="+time+"&text="+text+"&amnt="+amnt,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                $scope.onEditSuccessful(resp.data["Data"], "calorie");
                window.alert("Successfully edited calorie");
            },function(error){
                window.alert('There was an error editing the calorie on the server, check log');
                console.log(error);
            });
        };

        // update model/view on successful deletion from server
        $scope.onEditSuccessful = function(data, model) {

            console.log(data);
            if (model === "calorie") {
                $scope.editCalorieInCurr(data);
                $scope.setCurrCalorie(false, $scope.curr_cal_dict[data[0].id]);
                $scope.addingCalorie = false;
                $scope.editingCalorie = false;
                $scope.togglePostCalorie(false);
            }
            else {
                $scope.editUserInCurr(data);
                console.log("curr user dict is");
                console.log($scope.curr_user_dict);
                $scope.setCurrUserInfo(false, $scope.curr_user_dict[data[0].id]);
                $scope.editingUser = false;
                $scope.togglePostUser(false);
                if (data[0].id === $scope.log_user.id) {
                    $scope.setLoggedInUserInfo(false, data[0]);
                }
            }
        };

        // do ajax call to delete a calorie from server database
        // if successful, tell user and remove cal from curr_cal list and dict in angular
        $scope.deleteCalorie = function(callback) {

            // TO-DO:loading graphic
            $http({
                method:'POST',
                url: "/delete_calorie?calorie_id="+$scope.curr_cal.id,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                $scope.onDeleteSuccessful(resp.data);
                window.alert("Successfully deleted calorie");
            },function(error){
                window.alert('There was an error deleting the calorie from the server, check log');
                console.log(error);
            });
        };

        // update model/view on successful deletion from server
        $scope.onDeleteSuccessful = function(data) {

            console.log(data);
            if (data.Model === "calorie") {
                $scope.removeCalorieFromCurr(data.id);
                $scope.addingCalorie = false;
                $scope.editingCalorie = false;
                $scope.toggleViewCalorie(false);
            }
            else {
                if (data.id === $scope.log_user.id) {
                    // logged in user deleted themselves
                    $scope.signout();
                }
                else {
                    $scope.removeUserFromCurr(data.id);
                    $scope.addingUser = false;
                    $scope.editingUser = false;
                    $scope.toggleViewUser(false);
                }
            }
        };

        // remove a calorie from the model/view by id
        $scope.removeCalorieFromCurr = function(calID) {
            delete $scope.curr_cal_dict[parseInt(calID)];
        };

        $scope.editCalorieInCurr = function(data) {

            var cal = {
                id: data[0].id,
                user_id: data[0].user_id,
                date_str: data[0].date,
                date: new Date(data[0].date),
                time_str: data[0].time,
                time: parseInt(data[0].time.substring(0,2)),
                amnt: data[0].num_calories,
                text: data[0].text
            };
            
            console.log("before edit");
            console.log($scope.curr_cal_dict[data[0].id]);
            // replace with edited calorie
            $scope.curr_cal_dict[data[0].id] = cal;     
            console.log("after edit");
            console.log($scope.curr_cal_dict[data[0].id]);
        };

        // push calories from server to the current calorie list
        $scope.pushCalsFromServer = function(data) {

            for (var i = 0; i < data.length; i++) {
                console.log("pushing:");
                console.log(data[i]);

                var cal = {
                    id: data[i].id,
                    user_id: data[i].user_id,
                    date_str: data[i].date,
                    date: new Date(data[i].date),
                    time_str: data[i].time,
                    time: parseInt(data[i].time.substring(0,2)),
                    amnt: data[i].num_calories,
                    text: data[i].text
                };

                $scope.curr_cal_dict[cal.id] = cal;         
            }
        };

        // push users from server to the current user list
        $scope.pushUsersFromServer = function(data) {

            for (var i = 0; i < data.length; i++) {
                console.log("pushing:");
                console.log(data[i]);

                var user = {
                    id: data[i].id,
                    username: data[i].username,
                    user_type_id: data[i].user_type_id,
                    exp_cal_day: data[i].exp_cal_day,
                    email: data[i].email
                };
 
                $scope.curr_user_dict[user.id] = user;            
            }
            console.log("curr user dict is");
            console.log($scope.curr_user_dict);
        };

        // get list of calories from server, pass to callback
        $scope.getCalories = function(data, callback) {

            // TO-DO:loading graphic

            console.log(data);

            var calorie_id = data.hasOwnProperty("id") ? data.calorie_id : "";
            var user_id = data.hasOwnProperty("user_id") ? data.user_id : "";
            var date_from = data.hasOwnProperty("date_from") ? data.date_from : "";
            var date_to = data.hasOwnProperty("date_to") ? data.date_to : "";
            var time_from = data.hasOwnProperty("time_from") ? data.time_from : "";
            var time_to = data.hasOwnProperty("time_to") ? data.time_to : "";

            $http({
                method:'GET',
                url: '/calorie?id='+calorie_id+'&user_id='+user_id+"&date_from="+date_from+"&date_to="+date_to+"&time_from="+time_from+"&time_to="+time_to,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                callback(resp.data["Data"]);
            },function(error){
                console.log('There was an error retrieving calories from the server: ' + error);
            });
        };

        /* user view functions */
        
        // set the currently selected user to the user from the server
        $scope.setCurrUserInfo = function(isClear, data) {
            $scope.curr_user.id = isClear ? "" : data.id;
            $scope.curr_user.username = isClear ? "" : data.username;
            $scope.curr_user.user_type_id = isClear ? "" : data.user_type_id;
            $scope.curr_user.email = isClear ? "" : data.email;
            $scope.curr_user.exp_cal_day = isClear ? "" : data.exp_cal_day;

            console.log(isClear);
            console.log(data);
            if (isClear) {
                $scope.expCalMessage = "";    
                $scope.expIsSet = false;     
            }
            else if (data.exp_cal_day < 1) {
                console.log("here")
                $scope.expCalMessage = "No daily calorie goal set.";    
                $scope.expIsSet = false;
            }
            else {
                $scope.expCalMessage = "Daily calorie goal: " + data.exp_cal_day;
                $scope.expIsSet = true;
            }
        };

        // set the current user to the logged in user
        $scope.setCurrUserToLog = function() {
            $scope.curr_user.id = $scope.log_user.id;
            $scope.curr_user.username = $scope.log_user.username;
            $scope.curr_user.user_type_id = $scope.log_user.user_type_id;
            $scope.curr_user.exp_cal_day = $scope.log_user.exp_cal_day;
            $scope.curr_user.email = $scope.log_user.email;

            if ($scope.curr_user.exp_cal_day < 1) {
                $scope.expCalMessage = "No daily calorie goal set.";    
                $scope.expIsSet = false;
            }
            else {
                $scope.expCalMessage = "Daily calorie goal: " + $scope.curr_user.exp_cal_day;
                $scope.expIsSet = true;
            }
        };

        // toggle the total user view on or off
        $scope.toggleViewUsers = function(isShow) {
            if (isShow) {
                $scope.viewingUsers = true;
                $scope.toggleViewCalories(false);
            }
            else {
                // total reset
                $scope.viewingUsers = false;
                $scope.addingUser = false
                $scope.editingUser = false;
                $scope.toggleViewUser(false);
                $scope.togglePostUser(false); 
                $scope.toggleViewCalories(false);  
                $scope.togglePostCalorie(false, false);             
            }
            $scope.setCurrUserToLog();
        };   

        // toggle the user profile view on or off
        $scope.toggleViewUser = function(isShow, userID) {
            if (isShow) {
                $scope.viewingUsers = true;
                $scope.viewingUser = true;
                $scope.setCurrUserInfo(false, $scope.curr_user_dict[parseInt(userID)]);
                $scope.togglePostUser(false, false);
            }
            else {
                $scope.toggleViewCalories(false);
                $scope.setCurrUserToLog();
                $scope.viewingUser = false;
                if ($scope.log_user.user_type_id === 1) {
                    $scope.viewingUsers = false;
                }
                else if (!$scope.addingUser) {
                    // if we're not adding a user, also turn user form off
                    $scope.togglePostUser(false, false);
                }
            }
        };

        // toggle the user post view on or off by add or edit
        $scope.togglePostUser = function(isShow, isAdd) {
            if (isShow) {
                if (isAdd) {
                    $scope.addingUser = true;
                    $scope.editingUser = false;
                    $scope.setPostUser(true);
                    $scope.toggleViewUser(false);
                }
                else {
                    $scope.addingUser = false;
                    $scope.editingUser = true;
                    $scope.setPostUser(false);
                }
            }
            else {
                $scope.addingUser = false;
                $scope.editingUser = false;
                $scope.setPostUser(true);
            }
        };

        // set the information for the user to be edited
        $scope.setPostUser = function(isClear) {
            $scope.post_user.id = isClear ? "" : $scope.curr_user.id;
            $scope.post_user.username = isClear ? "" : $scope.curr_user.username;
            $scope.post_user.user_type_id = isClear ? "" : $scope.curr_user.user_type_id;
            $scope.post_user.email = isClear ? "" : $scope.curr_user.email;
            $scope.post_user.exp_cal_day = isClear ? "" : $scope.curr_user.exp_cal_day;
        };

        // do ajax call to edit user in server database
        $scope.editUser = function() {

            var user_id = $scope.post_user.id;
            var username = $scope.post_user.username;
            var email = $scope.post_user.email;
            var exp_cal_day = $scope.post_user.exp_cal_day;
            var user_type = $scope.canCRUDAll() ? $scope.post_user.user_type_id : "";

            var user_type_id = user_type.hasOwnProperty("id") ? user_type.id : user_type;

            console.log($scope.post_user.user_type_id);
            console.log(user_type_id);

            $http({
                method:'POST',
                url: "/edit_user?user_id="+user_id+"&username="+username+"&email="+email+"&exp_cal_day="+exp_cal_day+"&user_type_id="+user_type_id,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                $scope.onEditSuccessful(resp.data["Data"], "user");
                window.alert("Successfully edited user");
            },function(error){
                window.alert('There was an error editing the profile on the server, check log');
                console.log(error);
            });
        };

        // edit a user in current model
        $scope.editUserInCurr = function(data) {

            var user = {
                id: data[0].id,
                username: data[0].username,
                email: data[0].email,
                exp_cal_day: data[0].exp_cal_day,
                user_type_id: data[0].user_type_id
            };
            
            console.log("before edit");
            console.log($scope.curr_user_dict[data[0].id]);
            // replace with edited calorie
            $scope.curr_user_dict[data[0].id] = user;     
            console.log("after edit");
            console.log($scope.curr_user_dict[data[0].id]);
        };

        // remove a user from the current model/view
        $scope.removeUserFromCurr = function(userID) {
            delete $scope.curr_user_dict[parseInt(userID)];
        };

        // initiate ajax call to add/edit a user to server database
        $scope.postUser = function() {

            if ($scope.addingUser) {
                $scope.addUser($scope.pushUsersFromServer);
            }
            else if ($scope.editingUser) {
                $scope.editUser($scope.pushUsersFromServer);
            }
        };

        // do ajax call to add user to server database
        // pass list with added user from server to callback
        $scope.addUser = function(callback) {

            // TO-DO:loading graphic
            var username = $scope.post_user.username;
            var email = $scope.post_user.email;
            var exp_cal_day = $scope.post_user.exp_cal_day;
            var user_type = $scope.canCRUDAll() ? $scope.post_user.user_type_id : "";

            var user_type_id = user_type.hasOwnProperty("id") ? user_type.id : user_type;

            console.log(user_type_id);

            $http({
                method:'POST',
                url: "/add_user?username="+username+"&email="+email+"&exp_cal_day="+exp_cal_day+"&user_type_id="+user_type_id,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                callback(resp.data["Data"]);
                $scope.addingUser = false;
                $scope.editingUser = false;
                $scope.toggleViewUser(false);
                window.alert("Successfully added user");
            },function(error){
                window.alert('There was an error adding user the server, check log');
                console.log(error);
            });
        };

        // do ajax call to delete a user from server database
        // if successful, tell user and remove user from curr_user list and dict in angular
        // also sign out if curr_user === log_user
        $scope.deleteUser = function(callback) {

            // TO-DO:loading graphic
            $http({
                method:'POST',
                url: "/delete_user?user_id="+$scope.curr_user.id,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                $scope.onDeleteSuccessful(resp.data);
                window.alert("Successfully deleted user");
            },function(error){
                window.alert('There was an error deleting the user from the server, check log');
                console.log(error);
            });
        };

        // get list of users from server, pass to callback
        $scope.getUsers = function(data, callback) {

            console.log(data);

            var user_id = data.hasOwnProperty("id") ? data.user_id : "";
            var email = data.hasOwnProperty("email") ? data.date_from : "";
            var username = data.hasOwnProperty("username") ? data.date_to : "";

            $http({
                method:'GET',
                url: '/user?id='+user_id+'&email='+email+"&username="+username,
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                callback(resp.data["Data"]);
            },function(error){
                console.log('There was an error retrieving users from the server: ' + error);
            });
        };

        /* signin/out functions */

        // set the logged in user to the given user
        $scope.setLoggedInUserInfo = function(isClear, data) {
            $scope.log_user.id = isClear ? "" : data.id;
            $scope.log_user.username = isClear ? "" : data.username;
            $scope.log_user.user_type_id = isClear ? "" : data.user_type_id;
            $scope.log_user.exp_cal_day = isClear ? "" : data.exp_cal_day;
            $scope.log_user.email = isClear ? "" : data.email;
            console.log($scope.log_user.user_type_id);
            console.log($scope.user_type_dict);
            // ensure logged in user is active
            $scope.pushUsersFromServer([$scope.log_user])
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
                $scope.setLoggedInUserInfo(false, resp.data);
                $scope.setCurrUserInfo(false, resp.data);
                $scope.setTotalDataByUserType();
            },function(error){
                console.log(error);
                console.log('There was an error: ' + authResult['error']);
            });
        };

        $scope.signout = function(forUserDeletion=0) {
            // TO-DO: update this method

            $http({
                method:'POST',
                url: '/gdisconnect',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp);
                $scope.setLoggedInUserInfo(true, resp);
                $scope.setCurrUserInfo(true, resp.data);
                $scope.toggleViewCalories(false);
                $scope.toggleViewUsers(false);
                window.alert("Logged out");
            },function(error){
                console.log('There was an error disconnecting');
                console.log(error);
            });
        };

        // get and assign user types
        $scope.getAndAssignTypes = function() {

            $http({
                method:'GET',
                url: '/user_type',
                headers: {
                   'Content-Type': 'application/json;charset=utf-8'
                }
            })
            .then(function(resp){
                console.log(resp.data);
                for (var i = 0; i < resp.data["Data"].length; i++) {
                    $scope.user_type_dict[resp.data["Data"][i].id] = resp.data["Data"][i];
                };
                console.log($scope.user_type_dict);
            },function(error){
                console.log('There was an error getting user permission types from server');
                console.log(error);
            });
        };

        // auto get and assign functions once at start
        (function() {$scope.getAndAssignTypes();})();
    });
})(ccapp);

// callback when Google sends the user access code
function signInCallback(authResult) {

    console.log("called back");
    console.log(authResult);

    if (authResult['code']) {
        angular.element(document.getElementById('homeCtrlDiv')).scope().signin(authResult);   
    }
}
