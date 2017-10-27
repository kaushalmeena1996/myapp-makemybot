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
    $(element).blur();
    alertAction('code has been copied to clipboard.')
}

function settingAction(action) {
    switch (action) {
        case 0:
            $("#botUpload").click();
            $("#defaultCheckbox").prop('checked', false);
            break;

        case 1:
            $('#botImage').attr("src", $('#avtaarUrl').text());
            $("#defaultCheckbox").prop('checked', false);
            $("#botUpload").val('');
            break;

        case 2:
            $('#botImage').attr("src", "/media/avtaar/bot_default.png");
            $("#defaultCheckbox").prop('checked', true);
            $("#botUpload").val('');
            break;
    }
}

function toogleAction(action) {
    switch (action) {
        case 0:
            if ($("#visibleCheckbox").is(':checked')) {
                $("#formIcon00").removeClass('fa-eye-slash').addClass('fa-eye');
            } else {
                $("#formIcon00").removeClass('fa-eye').addClass('fa-eye-slash');
            }
            break;
        case 1:
            if ($("#greetCheckbox").is(':checked')) {
                $("#formIcon01").removeClass('fa-square-o').addClass('fa-check-square-o');
                $("#greetMessage").prop('disabled', false);

            } else {
                $("#formIcon01").removeClass('fa-check-square-o').addClass('fa-square-o');
                $("#greetMessage").prop('disabled', true);
            }
            break;
    }
}

function previewAction(event) {
    var input = $(event.currentTarget);
    var file = input[0].files[0];
    var reader = new FileReader();
    if (file.size > 64000) {
        alertAction('avtaar size must under 64 KB.');
        input.val('');
        return;
    }
    reader.onload = function (e) {
        var image_base64 = e.target.result;
        $("#botImage").attr("src", image_base64);
    };
    reader.readAsDataURL(file);
}

function alertAction(body) {
    $('#alertBody').text(body);
    $('#alertModal').modal('show');
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

function defaultAction() {
    alertAction('error occured while loading avtaar.');
}

function disqusAction(pageUrl, pageIdentifier) {
    /**
     *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
     *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables
     */

    var disqus_config = function () {
        this.page.url = pageUrl; // Replace PAGE_URL with your page's canonical URL variable
        this.page.identifier = 'bot_' + pageIdentifier; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };

    (function () { // DON'T EDIT BELOW THIS LINE
        var d = document,
            s = d.createElement('script');

        s.src = '//makemybotcom.disqus.com/embed.js';

        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
}