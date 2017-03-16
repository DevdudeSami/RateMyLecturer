$(document).ready(onReady);

function onReady() {
    if(isProcessing) {
        ajaxQueue.push(onReady);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/main/requests/getAllUniversitiesAsOptions',
        data: {},
        success: universitiesGottenCallback
    });
}

function universitiesGottenCallback(data) {
    nextAjaxRequest();

    $("#universitiesSelect").html(data);
}

function universitiesSelectChanged() {
    if($("#universitiesSelect option:selected").val() != "NONE") {
        window.location.replace("/lecturer/universityPage/" + $("#universitiesSelect option:selected").val());
    }
}
