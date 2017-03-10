var scoresScriptDelegate = {scoresChangeCallback: getComments};

$(document).ready(function() {
    getEverything();
});

function getEverything() {
    getRating();
    getAverageRating();
    getComments();
}

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

    getEverything();
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

function addComment() {
    if(isProcessing) {
        ajaxQueue.push(getComments);
        return;
    }

    var commentText = $("#commentText").val();
    var anonymously = $("#anonymousCheck").is(':checked');

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/addComment',
        data: {lecturerID: lecturerID, commentText: commentText, isAnonymous: anonymously},
        success: addCommentCallback
    });
}

function addCommentCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#addCommentArea").prop("hidden", true);
    $("#addCommentArea").find("#commentText").prop('id', "commentText-hidden");
    $("#addCommentArea").find("#anonymousCheck").prop('id', "anonymousCheck-hidden");

    getEverything();
}

function getComments() {
    if(isProcessing) {
        ajaxQueue.push(getComments);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/getComments',
        data: {lecturerID: lecturerID},
        success: getCommentsCallback
    });
}

function getCommentsCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#comments").html(data);
}

function editComment() {
    var commentText = $("#userCommentText").html();
    $("#userComment").prop("hidden", true);
    $("#editCommentDiv").prop("hidden", false);
    $("#commentText").val(commentText.trim());
    $("#commentText").focus();
}

function deleteComment(commentID) {
    if(isProcessing) {
        ajaxQueue.push({withArgs: true, call: deleteComment, args: [commentID]});
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/deleteComment',
        data: {commentID: commentID},
        success: deleteCommentCallback
    });
}

function deleteCommentCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#addCommentArea").prop("hidden", false);
    $("#addCommentArea").find("#commentText-hidden").prop('id', "commentText");
    $("#addCommentArea").find("#anonymousCheck-hidden").prop('id', "anonymousCheck");

    getEverything();
}
