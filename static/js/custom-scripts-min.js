function getDate(){var a=new Date,b=a.getDate(),c=a.getMonth(),d=a.getFullYear();return c+=1,b<10&&(b="0"+b),c<10&&(c="0"+c),b+"."+c+"."+d}function getTime(){var a=new Date,b=a.getHours(),c=a.getMinutes(),d=b>=12?"PM":"AM";return b%=12,b=b?b:12,b=b<10?"0"+b:b,c=c<10?"0"+c:c," "+b+":"+c+" "+d}function createMessage(a,b){var c=$(a).clone();return c.find("#messageTime").html(getTime()),c.find("#messageBody").html(b),c.prop("hidden",!1),c}function botAction(a,b,c){var d=$("#botContent"),e=$("#botInput").val(),f=$(c).find("#botId").attr("value");switch(bot_currentPage=b,a){case 0:d.fadeTo(300,0,function(){botQuery("botBrowse",d,f,e,b)});break;case 1:clearTimeout(botTimer),botTimer=window.setTimeout(function(){""!==e?d.fadeTo(300,0,function(){botQuery("botSearch",d,f,e,b)}):d.fadeTo(300,0,function(){botQuery("botBrowse",d,f,e,1)})},500);break;case 2:d.fadeTo(300,0,function(){botQuery("botSearch",d,f,e,b)})}}function botQuery(a,b,c,d,e){window.XMLHttpRequest?xmlhttp=new XMLHttpRequest:xmlhttp=new ActiveXObject("Microsoft.XMLHTTP"),xmlhttp.onreadystatechange=function(){4==xmlhttp.readyState&&200==xmlhttp.status&&("botBrowse"==a?(b.html(xmlhttp.responseText),b.fadeTo(300,1)):"botSearch"==a&&(b.html(xmlhttp.responseText),b.fadeTo(300,1)))},xmlhttp.open("POST","/chatbots",!0),xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded"),xmlhttp.send("actionType="+a+"&botId="+c+"&botPattern="+d+"&botPage="+e)}function bChat(a,b,c){var d=$("#chatInput").val();switch(a){case 0:botChat(b,"G",d);break;case 1:13!==c.keyCode&&0!==c.button||botChat(b,"Q",d);break;case 2:botChat(b,"E",d)}}function botChat(a,b,c){"Q"==b&&(createMessage("#userMessage",c).appendTo("#chatBox"),$("#chatButton").prop("disabled",!0),$("#chatInput").prop("disabled",!0),$("#chatBox").append("<div id='chatLoader' class='w3-container w3-text-col-grey w3-center w3-padding-32'><i class='fa fa-cog fa-spin fa-3x fa-fw' aria-hidden='true'></i></div>")),window.XMLHttpRequest?xmlhttp=new XMLHttpRequest:xmlhttp=new ActiveXObject("Microsoft.XMLHTTP"),xmlhttp.onreadystatechange=function(){4==xmlhttp.readyState&&200==xmlhttp.status&&("G"==b?(createMessage("#botMessage",xmlhttp.responseText).appendTo("#chatBox"),$("#chatInput").focus()):"Q"==b&&(createMessage("#botMessage",xmlhttp.responseText).appendTo("#chatBox"),$("#chatLoader").remove(),$("#chatButton, #chatInput").prop("disabled",!1),$("#chatInput").val(""),$("#chatBox").animate({scrollTop:$("#chatBox").prop("scrollHeight")-$("#chatBox").height()},500),$("#chatInput").focus()))},xmlhttp.open("POST","/chatbots/"+a+"/chat",!0),xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded"),xmlhttp.send("botId="+a+"&messageType="+b+"&messageString="+encodeURIComponent(c))}function cAction(a,b){var c=$("#chatInput").val();switch(a){case 0:chatAction("G",c);break;case 1:13!==b.keyCode&&0!==b.button||chatAction("Q",c);break;case 2:console.log(document.title),"MakeMyBot: Chat"==document.title&&chatAction("E",c)}}function chatAction(a,b){"Q"==a&&(createMessage("#userMessage",b).appendTo("#chatBox"),$("#chatButton").prop("disabled",!0),$("#chatInput").prop("disabled",!0),$("#chatBox").append("<div id='chatLoader' class='w3-container w3-text-col-grey w3-center w3-padding-32'><i class='fa fa-cog fa-spin fa-3x fa-fw' aria-hidden='true'></i></div>")),window.XMLHttpRequest?xmlhttp=new XMLHttpRequest:xmlhttp=new ActiveXObject("Microsoft.XMLHTTP"),xmlhttp.onreadystatechange=function(){4==xmlhttp.readyState&&200==xmlhttp.status&&("G"==a?(createMessage("#botMessage",xmlhttp.responseText).appendTo("#chatBox"),$("#chatInput").focus()):"Q"==a&&(createMessage("#botMessage",xmlhttp.responseText).appendTo("#chatBox"),$("#chatLoader").remove(),$("#chatButton, #chatInput").prop("disabled",!1),$("#chatInput").val(""),$("#chatBox").animate({scrollTop:$("#chatBox").prop("scrollHeight")-$("#chatBox").height()},500),$("#chatInput").focus()))},xmlhttp.open("POST","/chat",!0),xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded"),xmlhttp.send("messageType="+a+"&messageString="+encodeURIComponent(b))}function sAction(a){var b=$("#searchResult"),c=0,d="",e=$("#searchInput").val(),f="";clearTimeout(sTimer),sTimer=window.setTimeout(function(){""!==e&&(s_currentPage=a,b.is(":visible")||b.fadeIn(),b.find("#boxContent").fadeTo(300,0,function(){queryAction("sBrowse",b,c,d,e,f,a)}))},500)}function utilityfadeOut(a){$(a).fadeOut()}function utilityToggle(a){var b=$(a),c=0,d="",e="",f="",g=1;switch(a){case"#infoBox":queryAction("iInfo",b,c,d,e,f,g);break;case"#addBox":$("#aPattern, #aTemplate").val(""),$("#aSelect").val("Q"),b.is(":visible")||($("#aSelect").val("Q"),$("#aPattern").attr("placeholder","< Enter question to be matched by bot. >"));break;case"#browseBox":b.is(":visible")||$("#bSelect01, #bSelect02").val("*"),d=$("#bSelect01").val()+$("#bSelect02").val(),queryAction("bBrowse",b,c,d,e,f,g);break;case"#logBox":queryAction("lBrowse",b,c,d,e,f,g)}b.fadeToggle()}function aAction(a){var b=$("#addBox"),c=b.find("#qId").attr("value"),d=$("#aSelect").val(),e=$("#aPattern").val(),f=$("#aTemplate").val(),g=1;switch(a){case 0:"Q"==$("#aSelect").val()?($("#aTemplate").fadeIn(),$("#aPattern").attr("placeholder","< Enter question to be matched by bot. >"),$("#aTemplate").attr("placeholder","< Enter what bot should say in response to the above question. >")):"G"==$("#aSelect").val()?($("#aTemplate").fadeIn(),$("#aPattern").attr("placeholder","< Enter greeting message title to be matched by bot. >"),$("#aTemplate").attr("placeholder","< Enter bot greeting response to be displayed at starting of chat in response to the above greeting message title. >")):"R"==$("#aSelect").val()&&($("#aTemplate").fadeOut(),$("#aPattern").attr("placeholder","< Enter question to be asked when bot can't find anything to say. >"));break;case 1:""==e?($("#aPattern").attr("placeholder","< Please enter this section first. >"),$("#aPattern").focus()):queryAction("aSave",b,c,d,e,f,g);break;case 2:$("#aPattern, #aTemplate").val(""),$("#aSelect").val("Q");break;case 3:$("#addBox").fadeOut()}}function bAction(a){var b=$("#browseBox"),c=0,d=$("#bSelect01").val()+$("#bSelect02").val(),e="",f="";b_currentPage=a,b.find("#boxContent").fadeTo(300,0,function(){queryAction("bBrowse",b,c,d,e,f,a)})}function lAction(a){var b=$("#logBox"),c=0,d="",e="",f="";l_currentPage=a,b.find("#boxContent").fadeTo(300,0,function(){queryAction("lBrowse",b,c,d,e,f,a)})}function qAction(a,b){var c=$(b).parent().parent(),d=c.find("#qId").attr("value"),e=c.find("#qType").text(),f=c.find("#qPattern").text(),g=c.find("#qTemplate").val(),h=1;switch(a){case 0:queryAction("qDelete",c,d,e,f,g,h);break;case 1:c.find("#qTemplate").fadeToggle();break;case 2:queryAction("qSave",c,d,e,f,g,h);break;case 3:c.find("#qChanged").text("*");break;case 4:c.find("#qTemplate").is(":visible")||c.find("#qTemplate").fadeToggle(),takeShot(c.find("#qTemplate"));break;case 5:queryAction("lDelete",c,d,e,f,g,h)}}function queryAction(a,b,c,d,e,f,g){window.XMLHttpRequest?xmlhttp=new XMLHttpRequest:xmlhttp=new ActiveXObject("Microsoft.XMLHTTP"),xmlhttp.onreadystatechange=function(){4==xmlhttp.readyState&&200==xmlhttp.status&&("sBrowse"==a?(b.find("#boxContent").html(xmlhttp.responseText),b.find("#boxContent").fadeTo(300,1)):"iInfo"==a?b.find("#boxContent").html(xmlhttp.responseText):"aSave"==a?b.find("#boxContent").fadeTo(300,0,function(){$("#aPattern, #aTemplate").val(""),$("#aSelect").val("Q"),$("#aPattern").attr("placeholder","< Enter question to be matched by bot. >"),$("#aTemplate").attr("placeholder","< Enter what bot should say in response to the above question. >"),$("#browseBox").is(":visible")&&bAction(b_currentPage),$("#searchResult").is(":visible")&&sAction(s_currentPage)}).fadeTo(300,1):"qSave"==a?(b.find("#qTemplate").fadeToggle(function(){$("#browseBox").is(":visible")&&bAction(b_currentPage),$("#searchResult").is(":visible")&&sAction(s_currentPage)}),b.find("#qChanged").text("")):"qDelete"==a?b.fadeOut(function(){b.remove(),$("#browseBox").is(":visible")&&bAction(b_currentPage),$("#searchResult").is(":visible")&&sAction(s_currentPage)}):"bBrowse"==a?(b.find("#boxContent").html(xmlhttp.responseText),b.find("#boxContent").fadeTo(300,1)):"lBrowse"==a?(b.find("#boxContent").html(xmlhttp.responseText),b.find("#boxContent").fadeTo(300,1)):"lDelete"==a&&b.fadeOut(function(){b.remove(),lAction(l_currentPage)}))},xmlhttp.open("POST","/teach",!0),xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded"),xmlhttp.send("actionType="+a+"&qId="+c+"&qType="+d+"&qPattern="+e+"&qTemplate="+f+"&qPage="+g)}function goBack(){window.history.back()}function takeShot(a){html2canvas($(a),{onrendered:function(a){var b=document.createElement("a");b.href=a.toDataURL("image/png").replace("image/png","image/octet-stream"),b.download="ScreenShot.png",b.click()}})}function showDisqus(a,b){!function(){var a=document,b=a.createElement("script");b.src="//makemybotcom.disqus.com/embed.js",b.setAttribute("data-timestamp",+new Date),(a.head||a.body).appendChild(b)}()}function showName(){$("#userContent").is(":visible")?$("#userContent").fadeOut():$("#userContent").fadeIn()}function settingAction(a){var b=$("#botImage").attr("src"),c="/static/avtaar/";switch(a){case 0:$("input[type='file']").click();break;case 1:b=$("#botOld").val(),c+=b,$("#botContainer").val(c),$("#botImage").attr("src",c);break;case 2:c="/static/avtaar/bot_default.png",$("#botContainer").val(c),$("#botImage").attr("src",c)}}function previewImage(a){var b=$(a.currentTarget),c=b[0].files[0],d=new FileReader;return c.size>64e3?(alert("image size must under 64 KB."),void b.val("")):(d.onload=function(a){var b=a.target.result;$("#botImage").attr("src",b)},void d.readAsDataURL(c))}function defaulImage(){var a="/static/avtaar/bot_default.png";$("#botContainer").val(a),$("#botImage").attr("src",a)}function copyText(){$("#eEmbed").select(),document.execCommand("copy"),alert("code copied to clipboard.")}var botTimer,bot_currentPage=1,sTimer,s_currentPage=1,b_currentPage=1,l_currentPage=1;