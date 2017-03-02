$(document).ready(function() {
    getRating();
    getAverageRating();
});

function rateLecturer(rating) {
    if(isProcessing) {
        ajaxQueue.push({withArgs: true, call: rateLecturer, args: [rating]});
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/rateLecturer',
        data: {value: rating, lecturerID: lecturerID},
        success: rateLecturerCallback
    });
}

function rateLecturerCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    getRating();
    getAverageRating();
}

function getRating() {
    if(isProcessing) {
        ajaxQueue.push(getRating);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/getRatingForLecturer',
        data: {lecturerID: lecturerID},
        success: getRatingForLecturerCallback
    });
}

function getRatingForLecturerCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    if(data != "NONE") {
        $(".rateLecturerButton").prop("src", starURL);

        for(var i=1; i<=data; i++) {
            $("#rateLecturerButton" + i).prop("src", selectedStarURL);
        }
    }
}

function getAverageRating() {
    if(isProcessing) {
        ajaxQueue.push(getAverageRating);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/getAverageRating',
        data: {lecturerID: lecturerID},
        success: getAverageRatingCallback
    });
}

function getAverageRatingCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#averageRating").html(data);
}