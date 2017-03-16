function searchLecturers() {
    if($("#lecturer").val() == "") {
        $("#lecturerResults").html("");
        return;
    }

    if(isProcessing) {
        ajaxQueue.push(searchLecturers);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/searchLecturers',
        data: {searchTerm: $("#lecturer").val()},
        success: searchLecturersCallback
    });
}

function searchLecturersCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#lecturerResults").html(data);
}
