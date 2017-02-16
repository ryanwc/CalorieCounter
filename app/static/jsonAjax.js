/*
get a JSON object representing a table in the database
and base the JSON to the callback
*/
function getTableJSON(tableName, callBackFunction) {

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {

        if (xhttp.readyState == 4 && xhttp.status == 200) {

            response = JSON.parse(xhttp.responseText)

            if (typeof callBackFunction === 'function') {

                callBackFunction(response);
            }
            else {

                console.log("Callback was not a function");
            }
        }
    }

    if (tableName == 'User') {

        path = "/user/JSON";
    }
    else if (tableName == "UserType") {

        path = "/user_type/JSON"
    }
    else if (tableName == "Calorie") {

        path = "/calorie/JSON"
    }

    xhttp.open("GET", path, true);
    xhttp.send();
}

// get a JSON object representing a row in the database
function getRowJSON(rowJSONpath, callBackFunction) {

    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {

        if (xhttp.readyState == 4 && xhttp.status == 200) {

            response = JSON.parse(xhttp.responseText)

            if (typeof callBackFunction === 'function') {

                callBackFunction(response);
            }
            else {

                console.log("Callback was not a function");
            }
        }
    }

    xhttp.open("GET", rowJSONpath, true);
    xhttp.send();
}
