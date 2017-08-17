var bot = new RiveScript();
var greetEnabled = 'False';
var greetMessage = 'hello';
var logMessage = '';

function chatAction(filename, message = 'hello', greet = 'False') {
    greetEnabled = greet.toString();
    greetMessage = message;
    bot.loadFile(filename, loadingDone, loadingError);
}

function loadingDone(batch_num) {
    console.log("Rivescript #" + batch_num + " has finished loading!");
    logMessage += '[' + Date() + ']\n';
    bot.sortReplies();
    if (greetEnabled == 'True') {
        getMessage(greetMessage);
    }
}

function loadingError(error) {
    console.log("Error when loading files: " + error);
}

function createMessage(messageId, messageString) {
    var clonedMessage = $(messageId).clone();
    clonedMessage.find("#messageTime").html(getTime());
    clonedMessage.find("#messageBody").html(messageString);
    clonedMessage.prop("hidden", false);
    return clonedMessage;
}

function getMessage(userMessage) {
    var botMessage = bot.reply("local-user", userMessage);
    createMessage("#botMessage", botMessage).appendTo("#chatBox");
    $("#chatLoader").remove();
    $("#chatButton, #chatInput").prop("disabled", false);
    $("#chatInput").val('');
    $("#chatBox").animate({
        scrollTop: $("#chatBox").prop("scrollHeight") - $("#chatBox").height()
    }, 500);
    $("#chatInput").focus();
    logMessage += '[' + getTime() + '] bot: ' + botMessage + '\n';
}

function sendMessage() {
    var userMessage = $("#chatInput").val();
    createMessage("#userMessage", userMessage).appendTo("#chatBox");
    $("#chatButton").prop("disabled", true);
    $("#chatInput").prop("disabled", true);
    $("#chatBox").append("<div id='chatLoader' class='container text-grey text-center'><span class='fa fa-cog fa-spin fa-3x fa-fw'></span></div>");
    logMessage += '[' + getTime() + '] user: ' + userMessage + '\n';
    getMessage(userMessage);
}

function executeChat(e) {
    if (e.keyCode == 13) {
        sendMessage();
    }
}

function getTime() {
    var d = new Date();
    var h = d.getHours();
    var m = d.getMinutes();
    var suffix = (h >= 12) ? 'PM' : 'AM';
    h = h % 12;
    h = h ? h : 12;
    h = h < 10 ? '0' + h : h;
    m = m < 10 ? '0' + m : m;
    return h + ":" + m + " " + suffix;
}

function logConversation() {
    $.ajax({
        type: "POST",
        url: "/teach/log",
        data: {
            'logText': logMessage
        },
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        async: false
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}