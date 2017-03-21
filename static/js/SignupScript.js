$(document).ready(function() {
    // Setup some of the form elements
    $("#id_repeat_password").after("<p id=\"passwordDisplay\"></p>");
    $("#id_username").after("<p id=\"userDisplay\"></p>");
    $("#id_university").after("<p id=\"universityDisplay\"></p>");

    $("#id_username").keyup(checkUsername);
    $("#id_password").keyup(checkUsername);
    $("#id_repeat_password").keyup(checkUsername);
    $("#id_university").change(universitySelectorChanged);
});

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

    if (($('#id_username').val().indexOf(' ') !== -1) || ($('#id_username').val().length < 7) || (data == "NO") || !checkPasswords() || !universityCorrect) {
        document.getElementById("submitButton").disabled = true;
    }

    if (display != "") {
        document.getElementById("userDisplay").innerHTML = display;
    }
}

function universitySelectorChanged() {
    if(isProcessing) {
        ajaxQueue.push(universitySelectorChanged);
        return;
    }

    // Start checking for email changes too
    $("#id_email").keyup(universitySelectorChanged);

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/getDomainForUniversityName',
        data: {universityName: $('#id_university option:selected').html()},
        success: recievedUniversityDomain
    });
}

var universityCorrect = true;
function recievedUniversityDomain(domain) {
    nextAjaxRequest();

    var display = "";

    var email = $("#id_email").val();
    var emailSplit = email.split("@");
    if(emailSplit.length == 2) {
        if(domain != emailSplit[1]) {
            universityCorrect = false;
            document.getElementById("submitButton").disabled = true;
            display = "<b style=\"color: red;\">Your email domain does not match the university you chose.</b>";
        }
    } else {
        universityCorrect = false;
        document.getElementById("submitButton").disabled = true;
        display = "<b style=\"color: red;\">Please enter a valid email address.</b>";
    }

    universityCorrect = true;
    $("#universityDisplay").html(display);
}
