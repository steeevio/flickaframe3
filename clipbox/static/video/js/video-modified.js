// creating the thumbnail on canvas
	// Get handles on the video and canvas elements
		var video = document.querySelector('video');
		var canvas = document.querySelector('canvas');
		// Get a handle on the 2d context of the canvas element
		var context = canvas.getContext('2d');
		// Define some vars required later
	
		
		// Add a listener to wait for the 'loadedmetadata' state so the video's dimensions can be read
		video.addEventListener('loadedmetadata', function() {
			// Calculate the ratio of the video's width to height
			ratio = video.videoWidth / video.videoHeight;
			// Define the required width as 100 pixels smaller than the actual video's width
			w = video.videoWidth - 100;
			// Calculate the height based on the video's width and the ratio
			h = parseInt(w / ratio, 10);
			// Set the canvas width and height to the values just calculated
			canvas.width = w;
			canvas.height = h;			
		}, false);
	
	

var vid, playbtn, seekslider, curtimetext, durtimetext, mutebtn, jumplink, createtab, w, h, ratio, curmins, cursecs, video_percent, tag_image;



function initialisePlayer (){
	
	//set object references
	vid = document.getElementById("my_video");
	playbtn = document.getElementById("playpausebutton");
	seekslider = document.getElementById("seekslider");
	curtimetext = document.getElementById("curtimetext");
	durtimetext = document.getElementById("durtimetext");
	mutebtn = document.getElementById("mutebtn");
//	jumplink = document.getElementById("jumplink");
	createtab = document.getElementById("createtab");

	
	
	
	
	//add event listeners
	playbtn.addEventListener("click", playPause, false);
	seekslider.addEventListener("change", vidSeek, false);
	vid.addEventListener("timeupdate", seekTimeUpdate, false);
	mutebtn.addEventListener("click", vidMute, false);
//	jumplink.addEventListener("click", jumpTo, false);
	createtab.addEventListener("click", createTab, false);
	
	
}



// event handler on tag submission - prevents default behaviour and calls function create_tag()
$('#post_tag').on('submit', function(event){
	createTab();
	event.preventDefault();
	console.log("form submitted!") // just checking
	create_post();
 
});

//AJAX for posting
function create_post() {

	console.log("create post is working!") // just checking
	console.log($('#tag_title').val())
	console.log(seekTimeUpdate())
	console.log(video_percent)

	$.ajax({
		url:"create_tag/", //the end point
		type: "POST", //http method
		data : { tag_title: $('#tag_title').val(), tag_description: $('#tag_description').val(), tag_start_string: seekTimeUpdate(), tag_start: video_percent, tag_image: tag_image }, // data sent with the post
		
		// handle success
		success:function(json){
			$('#tag_title').val(''); //clear the field
			$('#tag_description').val(''); //clear the field

		},

		// handle non success

		error : function(xhr,errmsg,err){
			$('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
			console.log(xhr.status + ": " + xhr.responseText)

		}
	});
};



//array holding tag info	
//var alltagcontent = [];
//console.log (alltagcontent);	



window.onload = initialisePlayer;


	
// seek / time update
function seekTimeUpdate(){
	var nt = vid.currentTime * (  100 / vid.duration );
	seekslider.value = nt;
	video_percent = nt;
	
	curmins = Math.floor(vid.currentTime / 60);
	cursecs = Math.floor(vid.currentTime - curmins * 60);
	durmins = Math.floor(vid.duration / 60);
	var dursecs = Math.floor(vid.duration - durmins * 60);
	
	if(cursecs < 10){ cursecs = "0" + cursecs;}	
	if(dursecs < 10){ dursecs = "0" + dursecs;}	
	if(curmins < 10){ curmins = "0" + curmins;}	
	if(durmins < 10){ durmins = "0" + durmins;}	
	
	curtimetext.innerHTML = curmins + ":" + cursecs ;
	durtimetext.innerHTML = durmins + ":" + dursecs;

	return curmins + ":" + cursecs;
	}

//create tabs
function createTab(){
	
	// Define the size of the rectangle that will be filled (basically the entire element)
			context.fillRect(0, 0, w, h);
			// Grab the image from the video
			context.drawImage(video, 0, 0, w, h);
	
	var dataURL = canvas.toDataURL('image/jpeg'); // can also use 'image/png'
	
	console.log (dataURL);			
		
	
	var tag_title = document.getElementById('tag_title').value;
	var tag_description = document.getElementById('tag_description').value;
	
	// Create a <button> element
	var btn = document.createElement("BUTTON");        
	// Create a text node
	var t = document.createTextNode(tag_title);       
	// Append the text to <button>
	btn.appendChild(t);     
	// Append <button> to <body>                           
	
	document.getElementById('video_controls_bar').appendChild(btn);
	
	// give the button a class
	btn.className += "newtag";  
	//position the button absolutely  
	btn.style.left = tagtime +"%";  
	var tagtime = vid.currentTime * (  100 / vid.duration );
	btn.style.left = tagtime +"%";
	
	btn.addEventListener("click", playFrom, false);
		function playFrom(){
		var seekto = vid.duration * (tagtime / 100) ;
		vid.currentTime = seekto ;
		}
	
	
	// Create a <a> element
	var taglink = document.createElement("button");        
	// Create a text node
	var tnode = document.createTextNode(tag_title);       
	// Append the text to <button>
	taglink.appendChild(tnode);     
	// Append <a> to <body>                           
	document.getElementById('taglist').appendChild(taglink);
	
	// give the <a> a class
	taglink.className += "newtaglink";  
	//position the button absolutely  
	
	
	taglink.addEventListener("click", playFrom, false);
	
	
	// add a comment
	var comment = document.getElementById("tag_description").value;
	  
	  
	   
	   
	  
	   
	   
	   
		//create the array
	var tagarray = [];
	tagarray.push(tag_title);
	tagarray.push(tagtime);
	tagarray.push(curtimetext);
	tagarray.push(tag_description);
	tagarray.push(dataURL);
	
	//document.getElementById('comments').innerHTML += tagarray ; 
	
	
	
	//document.getElementById('comments').innerHTML += tag ; 
	
	//output to comments box
	var tag_title = "<span class= \"tag_title\">"+ tag_title + "</span>";
	var tag_description = "<span class= \"tag_description\">"+ tag_description + "</span>";
	var tagtimecomments = "<span class=\"time_comments\">"+ curmins + ":" + cursecs + "</span>";
	//var commentcomments = "<span class=\"tag_description\">"+ comment + "</span>";
	var dataURLcomments = "<img class=\"image_comments\" src=\"  " + dataURL + " \"></img>";
	
	tag_image = dataURLcomments
	
	document.getElementById('comments').innerHTML += tag_title ; 
	document.getElementById('comments').innerHTML += tagtimecomments ;
	document.getElementById('comments').innerHTML += tag_description ;
	document.getElementById('comments').innerHTML += dataURLcomments ;
	//console.log(dataURL);
	
	//console.log(tagarray);

	//alltagcontent.push(tagarray);
	//console.log(alltagcontent);
	
	//console.log(alltagcontent[0][1]); 
	
	//Create a JSON object

//	var json_obj = '{ "tagdetails" : [' +
//'{ "tag":tag_title , "tagtime":tagtimecomments, "tag_title":commentcomments, "tagscreengrab":dataURLcomments } ]}';

//console.log(JSON.stringify(json_obj));


// Post object to PHP

//function submitAndsaveData() {  
		    
//	$.ajax({
  //      url:"savedata2.php",
    //    type: "post",
      //  data :json_obj,
        //dataType:"json",			
		
	    //success: function () {
		    
		//		console.log("I think you got to php");
		    			
		    
		  
	    //},
	    //error : function(XMLHttpRequest, textStatus, errorThrown) {
		  //  alert(textStatus);
	    //}
	//});
	
	
    //return false;    
	
}





	
// video seek position
function vidSeek(){
	var seekto = vid.duration * (seekslider.value / 100) ;
	vid.currentTime = seekto ;
	}
	
//jump to position	
function jumpTo (){
	
    vid.play();
    vid.pause();
    vid.currentTime = 100;
    vid.play();
	}	

//play pause function
function playPause(){
	if (vid.paused){
		vid.play();
		playbtn.innerHTML = "pause";
		}
		
	else {
		vid.pause();
		playbtn.innerHTML = "play";	
			}
	}


//video mute
function vidMute(){
	if (vid.muted){
		vid.muted=false;
		mutebtn.innerHTML="MUTE";
		}
	else vid.muted=true;
	mutebtn.innerHTML="UNMUTE";	
	}






// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});




