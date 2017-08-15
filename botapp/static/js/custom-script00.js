function executeQuery(e) {
    if (e.keyCode == 13) {
        searchAction();
    }
}

function searchAction() {
    window.location.href = "?query=" + $("#searchInput").val() + "&page=1";
}

function resetAction(element) {
    $(element).val('');
}

function copyAction(element) {
    $(element).select();
    document.execCommand("copy");
    alert('Code copied to clipboard.');
}

function userAction() {
    if ($("#userContent").is(":visible")) {
        $("#userContent").fadeOut();
    } else {
        $("#userContent").fadeIn();
    }
}

function backAction() {
    window.history.back();
}