/**
 * scripts.js
 *
 * Global JavaScript, if any.
 */
 
function getDate() {
   var currentDate = new Date();
   var currentDay = currentDate.getDate();
   var currentMonth = currentDate.getMonth();
   var currentYear = currentDate.getFullYear();
   
   currentMonth = currentMonth + 1;
   
   if(currentDay < 10) currentDay = '0' + currentDay;
   if(currentMonth < 10) currentMonth = '0' + currentMonth;
   
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

function botAction(actionCode, botPage, botObject)
{
	var botBox = $("#botContent");
	
	var botPattern = $("#botInput").val();

	var botId = $(botObject).find("#botId").attr("value");
	
	bot_currentPage = botPage;

	switch (actionCode) {
    case 0:
        botBox.fadeTo(300, 0, function () {
			botQuery("botBrowse", botBox, botId, botPattern, botPage);
        });
        break;

    case 1:
		clearTimeout(botTimer);
	
		botTimer = window.setTimeout(function () {
			if (botPattern !== '') {
				botBox.fadeTo(300, 0, function () {
					botQuery("botSearch", botBox, botId, botPattern, botPage);
				});
			}
			else
			{
				botBox.fadeTo(300, 0, function () {
					botQuery("botBrowse", botBox, botId, botPattern, 1);
				});	
			}
		}, 500);
        break;
		
	case 2:
        botBox.fadeTo(300, 0, function () {
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

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			
			if (actionType == 'botBrowse')
			{	
				botBox.html(xmlhttp.responseText);
				botBox.fadeTo(300, 1);
			}
			else if (actionType == 'botSearch')
			{
				botBox.html(xmlhttp.responseText);
				botBox.fadeTo(300, 1);	
			}
        }
    };

    xmlhttp.open("POST", "/chatbots", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("actionType=" + actionType + "&botId=" + botId +  "&botPattern=" + botPattern +"&botPage=" + botPage);
}

function bChat(actionCode, botId, e)
{
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
	
	if (messageType == 'Q')
	{
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

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			
			if (messageType == 'G')
			{		
				createMessage("#botMessage", xmlhttp.responseText).appendTo("#chatBox");
				$("#chatInput").focus();
			}
			else if (messageType == 'Q')
			{		
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


function cAction(actionCode, e)
{
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
	
	if (messageType == 'Q')
	{
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

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			
			if (messageType == 'G')
			{		
				createMessage("#botMessage", xmlhttp.responseText).appendTo("#chatBox");
				$("#chatInput").focus();
			}
			else if (messageType == 'Q')
			{		
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
	
	sTimer = window.setTimeout(function () {
          
		if (qPattern !== '') {
			s_currentPage = qPage;

			if (!(qBox.is(":visible"))) {
            qBox.fadeIn();
			}

			qBox.find("#boxContent").fadeTo(300, 0, function () {
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
        if ($("#aSelect").val() == 'Q') 
		{
			$("#aTemplate").fadeIn();
			$("#aPattern").attr("placeholder", "< Enter question to be matched by bot. >");
			$("#aTemplate").attr("placeholder", "< Enter what bot should say in response to the above question. >");
        } 
		else if ($("#aSelect").val() == 'G') 
		{
			$("#aTemplate").fadeIn();
			$("#aPattern").attr("placeholder", "< Enter greeting message title to be matched by bot. >");
			$("#aTemplate").attr("placeholder", "< Enter bot greeting response to be displayed at starting of chat in response to the above greeting message title. >");
        } 
		else if ($("#aSelect").val() == 'R') 
		{
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

    qBox.find("#boxContent").fadeTo(300, 0, function () {
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

    qBox.find("#boxContent").fadeTo(300, 0, function () {
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

    xmlhttp.onreadystatechange = function () {

        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

            if (actionType == 'sBrowse') {
                qBox.find("#boxContent").html(xmlhttp.responseText);
                qBox.find("#boxContent").fadeTo(300, 1);
            } else if (actionType == 'iInfo') {
                qBox.find("#boxContent").html(xmlhttp.responseText);
            } else if (actionType == 'aSave') {
                qBox.find("#boxContent").fadeTo(300, 0, function () {

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
                qBox.find("#qTemplate").fadeToggle(function () {

                    if ($('#browseBox').is(":visible")) {
                        bAction(b_currentPage);
                    }

                    if ($('#searchResult').is(":visible")) {
                        sAction(s_currentPage);
                    }

                });
                qBox.find("#qChanged").text("");
            } else if (actionType == 'qDelete') {
                qBox.fadeOut(function () {

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
                qBox.fadeOut(function () { qBox.remove(); lAction(l_currentPage); });
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

function takeShot(divID)
{
    html2canvas($(divID), 
    {
      onrendered: function (canvas) {
        var screenShot = document.createElement('a');
        screenShot.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
        screenShot.download = 'ScreenShot.png';
        screenShot.click();
      }
    });
}

function showDisqus(pageUrl, pageIdentifier)
{
	/**
     *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
     *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables
     */
    
    var disqus_config = function () {
        this.page.url = pageUrl;  // Replace PAGE_URL with your page's canonical URL variable
        this.page.identifier = 'bot_' + pageIdentifier; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    
    (function() {  // DON'T EDIT BELOW THIS LINE
        var d = document, s = d.createElement('script');
        
        s.src = '//makemybotcom.disqus.com/embed.js';
        
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
    })();
}

function showName() {
	
	var uContent = $("#userContent");

	if(uContent.is(":visible"))
	{

	  uContent.fadeOut();
	}
	else
	{
	  uContent.fadeIn();	
	}
}

function settingAction(actionCode)
{
	var botImage = $('#botImage').attr("src");
	
	switch (actionCode) {
    case 0:
		$("input[type='file']").click();
        break;

    case 1:
		setImage();
		
		$("#botAction").val("2");
		
		botImage = $('#botImage').attr('src');
		
		$("#botContainer").val(botImage);
        break;
		
	case 2:
	    $('#botImage').attr("src",'..\\avtaar\\bot_default.png');
		
		$("#botAction").val("2");
		
		botImage = $('#botImage').attr("src");
		
		$("#botContainer").val(botImage);	
        break;
    }
}

function previewImage(event)
{
	var input = $(event.currentTarget);
	var file = input[0].files[0];
	
	var reader = new FileReader();
	
	if (file.size > 64000) 
    {
        alert("Image size must under 64 KB."); 
		input.val('');
		return;
    }
	
	reader.onload = function(e){
		var image_base64 = e.target.result;
		
		$("#botAction").val("1");
		
		$("#botImage").attr("src", image_base64);
		
		$("#botContainer").val(image_base64);
	}; 
	reader.readAsDataURL(file);
}

function setImage()
{
	var botId = $("#botId").attr("value");
	
	var ext = ['png','gif','jpg','jpeg'];
	
	var counter, flag = 0;
	
	var path = "..\\avtaar\\bot_image_" +  botId + ".";
	
	for (counter = 0; counter < ext.length; ++counter) 
	{
		if (urlExists(path + ext[counter]) == 200)
		{
			flag = 1; break;
		}
	}
	
	if (flag == 1)
	{
		path = path + ext[counter];  $('#botImage').attr(path);
	}
	else
	{
		$("#botImage").attr("src", "..\\avtaar\\bot_default.png");	
	}	
}

function urlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    
	http.send();
    
	return http.status;
}







   
                

                   
                



