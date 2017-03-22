function searchLecturers() {
    if($("#lecturer").val() == ""){
        $("#lecturerResults").slideUp('slow').then(function() { $("#lecturerResults").html(""); });
        return;
    }
    else {
        $("#lecturerResults").slideDown('slow');
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

    $("#lecturerResults").html("<h2>Search Results</h2><button onclick=\"clearSearch()\">Clear</button><br>" + data);
}

function clearSearch() {
    $("#lecturer").val("");
    $("#lecturerResults").slideUp('slow').then(function() { $("#lecturerResults").html(""); });
}
