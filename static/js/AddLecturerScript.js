// 4 FUNCTIONS FOR HANDLING UNIS
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




// 4 FUNCTIONS FOR HANDLING DEPARTMENT
function searchDepartments() {
    if($("#department").val() == "") { return; }

    if(isProcessing) {
        ajaxQueue.push(searchDepartments);
        return;
    }

    isProcessing = true;
    $.ajax({
        type: 'post',
        url: '/lecturer/requests/searchDepartments',
        data: {searchTerm: $("#department").val(), university: $("#university").val()},
        success: searchDepartmentsCallback
    });
}

function searchDepartmentsCallback(data) {
    if(data == "invalidRequest5987@@!#inv_req") {
        window.location.replace("/log/login");
    }

    nextAjaxRequest();

    $("#departmentResults").html(data);
}

function pickDepartment(name) {
    $("#department").val(name);
    $("#department").prop("readonly", true);

    $("#departmentResults").html("<button onclick='changeDepartment()'>Change Department</button>");
}

function changeDepartment() {
    $("#department").val("");
    $("#department").prop("readonly", false);

    $("#departmentResults").html("");
}
