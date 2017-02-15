$(document).ready(function() {
    setupCSRF();
});

function searchUniversities() {
    if($("#university").val() == "") { return; }

    if(isProcessing) {
        ajaxQueue.push(searchUniversities);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/searchUniversities',
        data: {searchTerm: $("#university").val()},
        success: searchUniversitiesCallback
    });
}

function searchUniversitiesCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#universityResults").html(data);
}

function pickUniversity(name) {
    $("#university").val(name);
    $("#university").prop("readonly", true);

    $("#universityResults").html("<button onclick='changeUniversity()'>Change University</button>");
}

function changeUniversity() {
    $("#university").val("");
    $("#university").prop("readonly", false);

    $("#universityResults").html("");
}
