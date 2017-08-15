function executeQuery(e) {
   if (e.keyCode == 13) {
        searchAction();
    }
}

function searchAction() {
    window.location.href = "?query=" + $("#searchInput").val() + "&page=1";
}

function goBack() {
    window.history.back();
}