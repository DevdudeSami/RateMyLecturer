function scoreUp(comment_id) {
    if(isProcessing) {
        ajaxQueue.push({withArgs: true, call: scoreUp, args: [post_id]});
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/changeScoreForComment',
        data: {comment_id: comment_id, value: 1},
        success: scoreCallback
    });
}

function scoreDown(comment_id) {
    if(isProcessing) {
        ajaxQueue.push({withArgs: true, call: scoreDown, args: [comment_id]});
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/changeScoreForComment',
        data: {comment_id: comment_id, value: -1},
        success: scoreCallback
    });
}

function clearScore(comment_id) {
    if(isProcessing) {
        ajaxQueue.push({withArgs: true, call: clearScore, args: [comment_id]});
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/changeScoreForComment',
        data: {comment_id: comment_id, value: "CLEAR"},
        success: scoreCallback
    });
}

function scoreCallback(data, status, xhr) {
    nextAjaxRequest();

    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    if(typeof scoresScriptDelegate !== 'undefined') {
        scoresScriptDelegate.scoresChangeCallback();
    }
}
