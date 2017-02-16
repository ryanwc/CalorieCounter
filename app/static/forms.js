// get data with ajax call, check uniqueness, and set HTML form as appropriate
// input node must be jQuery object b/c eventually uses addClass()/removeClass() method
function realTimeUniqueCheck(columnValue, tableName, columnName, inputNode) {

    // define callback to execute upon successful ajax table retrieval
    var sendTableToCheckUniqueAndSetHTML = function(JSONTable) {

        checkUniqueAndSetHTML(columnValue, JSONTable, columnName, inputNode);
    };

    // do the ajax table retrieval 
    getTableJSON(tableName, sendTableToCheckUniqueAndSetHTML);
}

// check uniqueness of a value in a table and set HTML form as appropriate
// input node must be jQuery object
// or could refactor to not use .addClass/.removeClass
function checkUniqueAndSetHTML(columnValue, JSONTable, column, inputNode) {

    var uniqueAlertID = inputNode.attr('id') + "UniqueAlert";
    var uniqueAlertNode = document.getElementById(uniqueAlertID);

    if (checkUnique(columnValue, JSONTable, column)) {

        uniqueAlertNode.innerHTML = "OK: Not in use yet";
        inputNode.addClass("unique").removeClass("notUnique");
    }
    else {

        uniqueAlertNode.innerHTML = "NOT OK: Already in use";
        inputNode.addClass("notUnique").removeClass("unique");
    }
}

// return true if columnValue is unique in the table
function checkUnique(columnValue, JSONTableObj, column) {

    for (var tableName in JSONTableObj) {

        var table = JSONTableObj[tableName];

        for (i = 0; i < table.length; i++) {

            var row = table[i];

            if (row.hasOwnProperty(column)) {

                var thisColumn = row[column];

                if (columnValue == thisColumn) {
                    return false;
                }
            }
        }
    }

    return true;
};

// TO-DO: refactor with helpers
function checkForm(form) {

    if (form.id == 'editUserForm') {

        var name = document.getElementById("name").value;
        // does not check for illegal chars (but this is done on server side)
        if (!validateName(name, 30, false, false)) {
            return false;
        }

        // TO-DO: validation
        return true;
    }
    else if (form.id == 'editCalorieForm') {

        var name = document.getElementById("").value;
        var description = document.getElementById("description").value;

        if (!validateName(name, 80, false, false)) {
            return false;
        }
    
        if (!validateDescription(description, maxlength, false)) {

                return false;
        }

        // TO-DO: validation

        return true;
    }
    else if (form.id == 'editUserTypeForm') {

        var name = document.getElementById("name").value;

        if (!validateName(name, 100, false, false)) {
            return false;               
        }

        // TO-DO: validation

        return true;
    }
    else if (form.id == 'addCalorieForm') {

        var name = document.getElementById("name").value;
        
        if (!validateName(name, 80, true, true)) {
            return false;
        }

        return true;
    }
    else if (form.id == 'addUserForm') {

        // TO-DO: validation
    }
    else if (form.id == 'addUserTypeForm') {

        // TO-DO: validation
    }
    else {

        window.alert("Sorry, this action is not supported yet.")
        return false;
    }
}

function validateName(name, maxlength, required, unique) {

    if (name.length < 1) {

        if (required) {

            window.alert("You must provide a name");
            return false;
        }
        else {

            return true;
        }
    }

    if (unique) {

        var uniqueAlert = document.getElementById('nameUniqueAlert').innerHTML;

        if (uniqueAlert != 'OK: Not in use yet') {

            window.alert("Name is not unique");
            return false;
        }
    }

    if (name.length > 30) {
        window.alert("Name is too long");
        return false;
    }

    return true;
}

function validateDescription(text, maxlength, required) {

    if (text.length < 1) {

        if (required) {
            window.alert("You must provide a description");
            return false;
        }
        else {
            return true;
        }
    }

    if (description.length > maxlength) {
        window.alert("Description is too long");
        return false;
    }

    return true;
}

function validateSelection(userSelectedValue, validSelectNodes, required) {

    if (userSelectedValue.length < 1) {

        if (required) {
            window.alert("You didn't select an option from a dropdown menu");
            return false;
        }
        else {
            return true;
        }
    }

    for (i = 0; i < validSelectNodes.length; i++) {

        if (userSelectedValue == validSelectNodes[i].value) {
            return true;
        }
    }

    window.alert("You selected an invalid dropdown menu selection");
    return false;
}
