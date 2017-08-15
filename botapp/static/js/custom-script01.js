var bot = new RiveScript();

function chatAction(filename) {
    bot.loadFile(filename, loadingDone, loadingError);
}

function loadingDone(batch_num) {
	console.log("Rivescript #" + batch_num + " has finished loading!");
	bot.sortReplies();

	//var reply = bot.reply("local-user", "Hello, bot!");
	//console.log("The bot says: " + reply);
}

function loadingError (error) {
	console.log("Error when loading files: " + error);
}

function createMessage(messageId, messageString) {
    var clonedMessage = $(messageId).clone();
    clonedMessage.find("#messageTime").html(getTime());
    clonedMessage.find("#messageBody").html(messageString);
    clonedMessage.prop("hidden", false);
    return clonedMessage;
}

function getMessage() {
    var botMessage = bot.reply("local-user", userMessage);
    createMessage("#botMessage", botMessage).appendTo("#chatBox");
    $("#chatLoader").remove();
    $("#chatButton, #chatInput").prop("disabled", false);
    $("#chatInput").val('');
    $("#chatBox").animate({ scrollTop: $("#chatBox").prop("scrollHeight") - $("#chatBox").height()}, 500);
    $("#chatInput").focus();
}

function sendMessage() {
    var userMessage = $("#chatInput").val();
    createMessage("#userMessage", userMessage).appendTo("#chatBox");
    $("#chatButton").prop("disabled", true);
    $("#chatInput").prop("disabled", true);
    $("#chatBox").append("<div id='chatLoader' class='container text-grey text-center'><span class='fa fa-cog fa-spin fa-3x fa-fw'></span></div>");
    getMessage();
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
    return " " + h + ":" + m + " " + suffix;
}