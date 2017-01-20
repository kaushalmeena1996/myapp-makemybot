/**
 * scripts.js
 *
 */

function getDate() {
    var currentDate = new Date();
    var currentDay = currentDate.getDate();
    var currentMonth = currentDate.getMonth();
    var currentYear = currentDate.getFullYear();

    currentMonth = currentMonth + 1;

    if (currentDay < 10) currentDay = '0' + currentDay;
    if (currentMonth < 10) currentMonth = '0' + currentMonth;

    return currentDay + "." + currentMonth + "." + currentYear;
}

function getTime() {
    var currentDate = new Date();
    var currentHour = currentDate.getHours();
    var currentMinute = currentDate.getMinutes();

    var timeSuffix = (currentHour >= 12) ? 'PM' : 'AM';

    currentHour = currentHour % 12;
    currentHour = currentHour ? currentHour : 12;
    currentHour = currentHour < 10 ? '0' + currentHour : currentHour;
    currentMinute = currentMinute < 10 ? '0' + currentMinute : currentMinute;

    return " " + currentHour + ":" + currentMinute + " " + timeSuffix;
}

function createMessage(messageId, messageString) {
    var clonedMessage = $(messageId).clone();

    clonedMessage.find("#messageTime").html(getTime());
    clonedMessage.find("#messageBody").html(messageString);
    clonedMessage.prop("hidden", false);

    return clonedMessage;
}

var botTimer, bot_currentPage = 1;

function botAction(actionCode, botPage, botObject) {
    var botBox = $("#botContent");

    var botPattern = $("#botInput").val();

    var botId = $(botObject).find("#botId").attr("value");

    bot_currentPage = botPage;

    switch (actionCode) {
        case 0:
            botBox.fadeTo(300, 0, function() {
                botQuery("botBrowse", botBox, botId, botPattern, botPage);
            });
            break;

        case 1:
            clearTimeout(botTimer);

            botTimer = window.setTimeout(function() {
                if (botPattern !== '') {
                    botBox.fadeTo(300, 0, function() {
                        botQuery("botSearch", botBox, botId, botPattern, botPage);
                    });
                } else {
                    botBox.fadeTo(300, 0, function() {
                        botQuery("botBrowse", botBox, botId, botPattern, 1);
                    });
                }
            }, 500);
            break;

        case 2:
            botBox.fadeTo(300, 0, function() {
                botQuery("botSearch", botBox, botId, botPattern, botPage);
            });
            break;
    }
}

function botQuery(actionType, botBox, botId, botPattern, botPage) {

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            if (actionType == 'botBrowse') {
                botBox.html(xmlhttp.responseText);
                botBox.fadeTo(300, 1);
            } else if (actionType == 'botSearch') {
                botBox.html(xmlhttp.responseText);
                botBox.fadeTo(300, 1);
            }
        }
    };

    xmlhttp.open("POST", "/chatbots", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("actionType=" + actionType + "&botId=" + botId + "&botPattern=" + botPattern + "&botPage=" + botPage);
}

function bChat(actionCode, botId, e) {
    var messageString = $("#chatInput").val();

    switch (actionCode) {
        case 0:
            botChat(botId, "G", messageString);
            break;

        case 1:
            if (e.keyCode === 13 || e.button === 0) {
                botChat(botId, "Q", messageString);
            }
            break;

        case 2:
            botChat(botId, "E", messageString);
            break;
    }
}

function botChat(botId, messageType, messageString) {

    if (messageType == 'Q') {
        createMessage("#userMessage", messageString).appendTo("#chatBox");

        $("#chatButton").prop("disabled", true);
        $("#chatInput").prop("disabled", true);
        $("#chatBox").append("<div id='chatLoader' class='w3-container w3-text-col-grey w3-center w3-padding-32'><i class='fa fa-cog fa-spin fa-3x fa-fw' aria-hidden='true'></i></div>");
    }

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            if (messageType == 'G') {
                createMessage("#botMessage", xmlhttp.responseText).appendTo("#chatBox");
                $("#chatInput").focus();
            } else if (messageType == 'Q') {
                createMessage("#botMessage", xmlhttp.responseText).appendTo("#chatBox");

                $("#chatLoader").remove();
                $("#chatButton, #chatInput").prop("disabled", false);
                $("#chatInput").val('');

                $("#chatBox").animate({
                    scrollTop: $("#chatBox").prop("scrollHeight") - $("#chatBox").height()
                }, 500);

                $("#chatInput").focus();
            }
        }
    };

    xmlhttp.open("POST", "/chatbots/" + botId + "/chat", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("botId=" + botId + "&messageType=" + messageType + "&messageString=" + encodeURIComponent(messageString));
}


function cAction(actionCode, e) {
    var messageString = $("#chatInput").val();

    switch (actionCode) {
        case 0:
            chatAction("G", messageString);
            break;

        case 1:
            if (e.keyCode === 13 || e.button === 0) {
                chatAction("Q", messageString);
            }
            break;

        case 2:
            chatAction("E", messageString);
            break;
    }
}

function chatAction(messageType, messageString) {

    if (messageType == 'Q') {
        createMessage("#userMessage", messageString).appendTo("#chatBox");

        $("#chatButton").prop("disabled", true);
        $("#chatInput").prop("disabled", true);
        $("#chatBox").append("<div id='chatLoader' class='w3-container w3-text-col-grey w3-center w3-padding-32'><i class='fa fa-cog fa-spin fa-3x fa-fw' aria-hidden='true'></i></div>");
    }

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            if (messageType == 'G') {
                createMessage("#botMessage", xmlhttp.responseText).appendTo("#chatBox");
                $("#chatInput").focus();
            } else if (messageType == 'Q') {
                createMessage("#botMessage", xmlhttp.responseText).appendTo("#chatBox");

                $("#chatLoader").remove();
                $("#chatButton, #chatInput").prop("disabled", false);
                $("#chatInput").val('');

                $("#chatBox").animate({
                    scrollTop: $("#chatBox").prop("scrollHeight") - $("#chatBox").height()
                }, 500);

                $("#chatInput").focus();
            }
        }
    };

    xmlhttp.open("POST", "/chat", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("messageType=" + messageType + "&messageString=" + encodeURIComponent(messageString));
}

var sTimer, s_currentPage = 1;

function sAction(qPage) {
    var qBox = $("#searchResult");

    var qId = 0;
    var qType = "";
    var qPattern = $("#searchInput").val();
    var qTemplate = "";

    clearTimeout(sTimer);

    sTimer = window.setTimeout(function() {

        if (qPattern !== '') {
            s_currentPage = qPage;

            if (!(qBox.is(":visible"))) {
                qBox.fadeIn();
            }

            qBox.find("#boxContent").fadeTo(300, 0, function() {
                queryAction("sBrowse", qBox, qId, qType, qPattern, qTemplate, qPage);
            });
        }

    }, 500);
}

function utilityfadeOut(utilityId) {
    $(utilityId).fadeOut();
}

function utilityToggle(utilityId) {

    var qBox = $(utilityId);

    var qId = 0;
    var qType = "";
    var qPattern = "";
    var qTemplate = "";
    var qPage = 1;

    switch (utilityId) {
        case "#infoBox":
            queryAction("iInfo", qBox, qId, qType, qPattern, qTemplate, qPage);
            break;

        case "#addBox":
            $("#aPattern, #aTemplate").val('');
            $("#aSelect").val('Q');
            if (!(qBox.is(":visible"))) {
                $("#aSelect").val('Q');
                $("#aPattern").attr("placeholder", "< Enter question to be matched by bot. >");
            }
            break;

        case "#browseBox":
            if (!(qBox.is(":visible"))) {
                $("#bSelect01, #bSelect02").val('*');
            }
            qType = $("#bSelect01").val() + $("#bSelect02").val();
            queryAction("bBrowse", qBox, qId, qType, qPattern, qTemplate, qPage);
            break;

        case "#logBox":
            queryAction("lBrowse", qBox, qId, qType, qPattern, qTemplate, qPage);
            break;
    }

    qBox.fadeToggle();
}

function aAction(actionCode) {
    var qBox = $("#addBox");

    var qId = qBox.find("#qId").attr("value");
    var qType = $("#aSelect").val();
    var qPattern = $("#aPattern").val();
    var qTemplate = $("#aTemplate").val();
    var qPage = 1;

    switch (actionCode) {
        case 0:
            if ($("#aSelect").val() == 'Q') {
                $("#aTemplate").fadeIn();
                $("#aPattern").attr("placeholder", "< Enter question to be matched by bot. >");
                $("#aTemplate").attr("placeholder", "< Enter what bot should say in response to the above question. >");
            } else if ($("#aSelect").val() == 'G') {
                $("#aTemplate").fadeIn();
                $("#aPattern").attr("placeholder", "< Enter greeting message title to be matched by bot. >");
                $("#aTemplate").attr("placeholder", "< Enter bot greeting response to be displayed at starting of chat in response to the above greeting message title. >");
            } else if ($("#aSelect").val() == 'R') {
                $("#aTemplate").fadeOut();
                $("#aPattern").attr("placeholder", "< Enter question to be asked when bot can't find anything to say. >");
            }
            break;

        case 1:
            if (qPattern == '') {
                $("#aPattern").attr("placeholder", "< Please enter this section first. >");
                $("#aPattern").focus();
            } else {
                queryAction("aSave", qBox, qId, qType, qPattern, qTemplate, qPage);
            }
            break;

        case 2:
            $("#aPattern, #aTemplate").val('');
            $("#aSelect").val('Q');
            break;

        case 3:
            $("#addBox").fadeOut();
            break;

    }
}

var b_currentPage = 1;

function bAction(qPage) {
    var qBox = $("#browseBox");

    var qId = 0;
    var qType = $("#bSelect01").val() + $("#bSelect02").val();
    var qPattern = "";
    var qTemplate = "";

    b_currentPage = qPage;

    qBox.find("#boxContent").fadeTo(300, 0, function() {
        queryAction("bBrowse", qBox, qId, qType, qPattern, qTemplate, qPage);
    });
}

var l_currentPage = 1;

function lAction(qPage) {
    var qBox = $("#logBox");

    var qId = 0;
    var qType = "";
    var qPattern = "";
    var qTemplate = "";


    l_currentPage = qPage;

    qBox.find("#boxContent").fadeTo(300, 0, function() {
        queryAction("lBrowse", qBox, qId, qType, qPattern, qTemplate, qPage);
    });
}

function qAction(actionCode, qObject) {
    var qBox = $(qObject).parent().parent();
    var qId = qBox.find("#qId").attr("value");
    var qType = qBox.find("#qType").text();
    var qPattern = qBox.find("#qPattern").text();
    var qTemplate = qBox.find("#qTemplate").val();

    var qPage = 1;

    switch (actionCode) {
        case 0:
            queryAction("qDelete", qBox, qId, qType, qPattern, qTemplate, qPage);
            break;

        case 1:
            qBox.find("#qTemplate").fadeToggle();
            break;

        case 2:
            queryAction("qSave", qBox, qId, qType, qPattern, qTemplate, qPage);
            break;

        case 3:
            qBox.find("#qChanged").text("*");
            break;

        case 4:
            if (!(qBox.find("#qTemplate").is(":visible"))) {
                qBox.find("#qTemplate").fadeToggle();
            }
            takeShot(qBox.find("#qTemplate"));
            break;

        case 5:
            queryAction("lDelete", qBox, qId, qType, qPattern, qTemplate, qPage);
            break;
    }

}

function queryAction(actionType, qBox, qId, qType, qPattern, qTemplate, qPage) {

    if (window.XMLHttpRequest) {
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else {
        // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {

        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            if (actionType == 'sBrowse') {
                qBox.find("#boxContent").html(xmlhttp.responseText);
                qBox.find("#boxContent").fadeTo(300, 1);
            } else if (actionType == 'iInfo') {
                qBox.find("#boxContent").html(xmlhttp.responseText);
            } else if (actionType == 'aSave') {
                qBox.find("#boxContent").fadeTo(300, 0, function() {

                    $("#aPattern, #aTemplate").val('');
                    $("#aSelect").val('Q');

                    $("#aPattern").attr("placeholder", "< Enter question to be matched by bot. >");
                    $("#aTemplate").attr("placeholder", "< Enter what bot should say in response to the above question. >");

                    if ($('#browseBox').is(":visible")) {
                        bAction(b_currentPage);
                    }

                    if ($('#searchResult').is(":visible")) {
                        sAction(s_currentPage);
                    }

                }).fadeTo(300, 1);
            } else if (actionType == 'qSave') {
                qBox.find("#qTemplate").fadeToggle(function() {

                    if ($('#browseBox').is(":visible")) {
                        bAction(b_currentPage);
                    }

                    if ($('#searchResult').is(":visible")) {
                        sAction(s_currentPage);
                    }

                });
                qBox.find("#qChanged").text("");
            } else if (actionType == 'qDelete') {
                qBox.fadeOut(function() {

                    qBox.remove();

                    if ($('#browseBox').is(":visible")) {
                        bAction(b_currentPage);
                    }

                    if ($('#searchResult').is(":visible")) {
                        sAction(s_currentPage);
                    }
                });
            } else if (actionType == 'bBrowse') {
                qBox.find("#boxContent").html(xmlhttp.responseText);
                qBox.find("#boxContent").fadeTo(300, 1);
            } else if (actionType == 'lBrowse') {
                qBox.find("#boxContent").html(xmlhttp.responseText);
                qBox.find("#boxContent").fadeTo(300, 1);
            } else if (actionType == 'lDelete') {
                qBox.fadeOut(function() {
                    qBox.remove();
                    lAction(l_currentPage);
                });
            }
        }
    };

    xmlhttp.open("POST", "/teach", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("actionType=" + actionType + "&qId=" + qId + "&qType=" + qType + "&qPattern=" + qPattern + "&qTemplate=" + qTemplate + "&qPage=" + qPage);
}

function goBack() {
    window.history.back();
}

function takeShot(divID) {
    html2canvas($(divID), {
        onrendered: function(canvas) {
            var screenShot = document.createElement('a');
            screenShot.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
            screenShot.download = 'ScreenShot.png';
            screenShot.click();
        }
    });
}

function showDisqus(pageUrl, pageIdentifier) {
    /**
     *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
     *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables
     */

    var disqus_config = function() {
        this.page.url = pageUrl; // Replace PAGE_URL with your page's canonical URL variable
        this.page.identifier = 'bot_' + pageIdentifier; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };

    (function() { // DON'T EDIT BELOW THIS LINE
        var d = document,
            s = d.createElement('script');

        s.src = '//makemybotcom.disqus.com/embed.js';

        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
}

function showName() {

    if ($("#userContent").is(":visible")) {
        $("#userContent").fadeOut();
    } else {
        $("#userContent").fadeIn();
    }
}

function settingAction(actionCode) {
    var botImage = $('#botImage').attr("src");

    switch (actionCode) {
        case 0:
            $("input[type='file']").click();
            break;

        case 1:
            botImage = $('#botOld').val();
            $("#botContainer").val(botImage);
            $('#botImage').attr("src", botImage);
            break;

        case 2:
            botImage = 'data:image/png;base64,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';
            $("#botContainer").val(botImage);
            $('#botImage').attr("src", botImage);
            break;
    }
}

function previewImage(event) {
    var input = $(event.currentTarget);
    var file = input[0].files[0];

    var reader = new FileReader();

    if (file.size > 64000) {
        alert("image size must under 64 KB.");
        input.val('');
        return;
    }

    reader.onload = function(e) {
        var image_base64 = e.target.result;

        $("#botImage").attr("src", image_base64);

        $("#botContainer").val(image_base64);
    };
    reader.readAsDataURL(file);
}

function defaulImage() {
    botImage = 'data:image/png;base64,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';
    $("#botContainer").val(botImage);
    $('#botImage').attr("src", botImage);
}