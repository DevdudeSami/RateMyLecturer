function documentLoaded() {
    // Setup CSRF
    setupCSRF();
    
    // Setup some of the form elements
    $("#id_repeat_password").after("<p id=\"passwordDisplay\"></p>");
    $("#id_username").after("<p id=\"userDisplay\"></p>");
    
    $("#id_username").keyup(checkUsername);
    $("#id_password").keyup(checkUsername);
    $("#id_repeat_password").keyup(checkUsername);
}

function checkPasswords() {
    var password = $("#id_password").val();
    var passwordRepeat = $("#id_repeat_password").val();
    var display = "";
    var returnValue = true;

    if(password.length < 6) {
        display = "<b style=\"color: blue;\">Password must be atleast 6 characters.</b>";
        returnValue = false;
    } else if (password != passwordRepeat) {
        display = "<b style=\"color: blue;\">Passwords must match.</b>";
        returnValue = false;
    }

    document.getElementById("passwordDisplay").innerHTML = display;
    return returnValue;
}

function checkUsername() {
    if(isProcessing) {
        ajaxQueue.push(checkUsername);
        return;
    }
    
    isProcessing = true;    
    if($('#id_username').val() != "") {
        $.ajax({
            type: 'post',
            url: '/log/requests/checkUsernameExists',
            data: {username: $('#id_username').val()},
            success: checkUserCallback
        });
    }
}

function checkUserCallback(data, textStatus, xhr) {
    nextAjaxRequest();
    
	if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/");
    }
    
    var display = "";

    if ($('#id_username').val().indexOf(' ') !== -1) {
        display = "<b style=\"color: blue;\">The username must be atleast 7 characters with no spaces.</b>";
        document.getElementById("submitButton").disabled = true;
    }
    else if ($('#id_username').val().length < 7) {
        display = "<b style=\"color: blue;\">The username must be atleast 7 characters with no spaces.</b>";
        document.getElementById("submitButton").disabled = true;
    }
    else if (data == "NO") {
        display = "<b style=\"color: red;\">The username you picked is already in use. Please try a different one.</b>";
        document.getElementById("submitButton").disabled = true;
    }
    else {
        display = "<b style=\"color: green;\">The username you picked is available.</b>";
        document.getElementById("submitButton").disabled = false;
    }

    if (($('#id_username').val().indexOf(' ') !== -1) || ($('#id_username').val().length < 7) || (data == "NO") || !checkPasswords()) {
        document.getElementById("submitButton").disabled = true;
    }

    if (display != "") {
        document.getElementById("userDisplay").innerHTML = display;
    }
}