// creating the thumbnail on canvas
	// Get handles on the video 
		var video = document.querySelector('video');

		//get image canvas element
		var canvas = document.getElementById('tag_canvas');
		// Get a handle on the 2d context of the canvas element
		var context = canvas.getContext('2d');
		// Define some vars required later
	
		// define canvas and context for drawing
		var vid_canvas = document.getElementById('video_canvas');
		var vid_context = vid_canvas.getContext('2d');


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
	initialisePlayer();	

	// set the current time if coming from a tag url
	this.currentTime = $('input[name=start_time_secs]').val();


	}, false);
	
	

var canvas_draw_state, duration, vid, playbtn, seekslider, curtimetext, durtimetext, mutebtn, jumplink, createtab, w, h, ratio, curmins, cursecs, video_percent, tag_image, tag_draw, tag_objects, draw, eraser;

canvas_draw_state = false;

function initialisePlayer (){
	
	//set object references
	vid = document.getElementById("my_video");
	playbtn = document.getElementById("playpausebutton");
	draw = document.getElementById("draw");
	seekslider = document.getElementById("seekslider");
	curtimetext = document.getElementById("curtimetext");
	durtimetext = document.getElementById("durtimetext");
	mutebtn = document.getElementById("mutebtn");
	createtab = document.getElementById("createtab");
	eraser = document.getElementById("eraser_button");

	//add event listeners
	playbtn.addEventListener("click", playPause, false);
	eraser.addEventListener("click", eraseDrawing, false);
	draw.addEventListener("click", drawOnTag, false);
	seekslider.addEventListener("change", vidSeek, false);
	vid.addEventListener("timeupdate", seekTimeUpdate, false);
	mutebtn.addEventListener("click", vidMute, false);	

	duration = vid.duration;
	console.log (duration);
};

//eraser drawing
function eraseDrawing(){
	//vid_context.clearRect(0, 0, vid_context.canvas.width, vid_context.canvas.height);
	//vid_canvas.sketch('actions',[]);
	tag_draw = "blank";	
	canvas_draw_state = false;
	$("#eraser_button").click();
	$("#video_canvas").hide();
	

}




//drawing over the video
 $(function() {
 	$('#video_canvas').sketch({defaultColor: "#fff"});
	});

function drawOnTag(){
	
	vid_width = $("#my_video").innerWidth();
	vid_height = $("#my_video").innerHeight();
	console.log (vid_height)
	vid_canvas.width  = vid_width;
	vid_canvas.height = vid_height;
	vid.pause();
	$('#video_canvas').width(vid_width).height(vid_height);

	
	$('#video_canvas').show();
		
	$('#tag_button').css({'background-color' : '#00ff00'});
	canvas_draw_state = true;

	}


// on screen resize
$( window ).resize(function() {

	vid_width = $("#my_video").innerWidth();
	vid_height = $("#my_video").innerHeight();
  	$('#overlay_vid').width(vid_width).height(vid_height);
});

$( document ).ready(function(response) {
 	
// set overlay size
	vid_width = $("#my_video").innerWidth();
	vid_height = $("#my_video").innerHeight();
$('#overlay_vid').width(vid_width).height(vid_height);	


//create array for tag based on the loaded content in the DOM
tag_objects = [];

	$('.page_tags').each(function(){
		tag_title_temp = $(this).find('h3').html()
		tag_start_temp = $(this).find('.tag_start').html()
		tag_avatar = $(this).find('.tag_avatar').html()
		tag_username =$(this).find('.tag_username').html()
		tag_overlay = $(this).find('.tag_overlay').html()
	    var obj = {
	        id: this.id,
	        title: tag_title_temp,
	        start:tag_start_temp,
	        avatar:tag_avatar,
	        username:tag_username,
	        overlay:tag_overlay
	        //comments: []
	    };
	    tag_objects.push(obj);
	});


});

// create timeline events with popcorn
var popcorn = Popcorn( "#my_video" );

function makePopcornHandler(this_title, this_start, this_avatar, this_overlay) {

	popcorn.code({
		start: this_start,
		
		onStart: function( options ) {
		document.getElementById( "current_tag" ).innerHTML = this_title;
		document.getElementById( "current_tag_avatar" ).innerHTML = this_avatar;
		document.getElementById( "current_tag_user" ).innerHTML = this_user;
		document.getElementById( "overlay_vid" ).innerHTML = "<img src='/static/video/" + this_overlay + "'>";
		
		//show the div with the drawing if the video is paused
		if (vid.paused){
		$('#overlay_vid').show()
		}
		
		//show the drawing for a short time if the video is playing
		else {
		$('#overlay_vid').show(0).delay(2000).hide(0);
		
		}
		

		

		}
	});
};

document.addEventListener( "DOMContentLoaded", function() {
	
	
	for (var i = 0; i < tag_objects.length; i++){
		this_title = tag_objects[i].title;
		this_start = tag_objects[i].start;
		this_avatar = tag_objects[i].avatar;
		this_user = tag_objects[i].username;
		this_overlay = tag_objects[i].overlay;
		start_secs = duration * (this_start / 100)
		makePopcornHandler(this_title, start_secs, this_avatar, this_overlay);
		console.log(start_secs);
	};
		

});



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
	//console.log(tag_image)
	var title = $('#tag_title').val();
	var time_secs = duration * (video_percent / 100);

	//start the video again
	vid.play();
	playbtn.innerHTML = "PAUSE";
	draw.innerHTML="DRAW";	
	$('#tag_button').css({'background-color' : '#ccc'});
		

	makePopcornHandler(title, time_secs); 

	timeSecs = Math.floor(vid.currentTime)
		console.log(timeSecs)


	//if(vid_canvas.toDataURL() == document.getElementById('blank').toDataURL()){
	if(canvas_draw_state == false){
		console.log("Its blank!")
        tag_draw = "blank";	
    }
	
	



	$.ajax({
		url:"create_tag/", //the end point
		type: "POST", //http method
		data : { tag_title: $('#tag_title').val(), tag_description: $('#tag_description').val(), tag_start_string: seekTimeUpdate(), tag_start: video_percent, tag_draw:tag_draw, tag_image:tag_image, time_secs:timeSecs }, // data sent with the post
		

		// handle success
		success : function(json){
			$('#tag_title').val('');//clears field
			$('#tag_description').val('');//clears field
			
			$('#tags_on_load').prepend(
				"<div id=\"tag_" + json.tagpk + "\">" +
					"<h3>" + json.tag_title + "</h3> " + 
					"<p>" + json.tag_description + "</p> " + 
					"</br> <img class=\"image_comments\" src=\" " + json.tag_image + " \"> </br>" + 
					"<button onclick = \"javascript:delete_tag( " + json.tagpk + "); \">Delete Tag</button>" + 
					"<div id=\"tag_username\">" + json.tag_user_email + "</div>"  +
					"<div id=\"tag_start\">" + json.tag_start_string + "</div>"  +
					"<div id=\"tag_overlay\">" + json.tag_draw + "</div>"  + 
				"</div>")
			
		},

		// handle non success

		error : function(xhr,errmsg,err){
			$('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
			console.log(xhr.status + ": " + xhr.responseText)

		}
	});
	
	eraseDrawing()
};



//array holding tag info	
//var alltagcontent = [];
//console.log (alltagcontent);	


// run function to preview group image on upload
//$("form input[name='group_images']").click(function () { 
//		upload_img(input) {
//			if (input.files && input.files[0]) {
//				var reader = new FileReader();

//				reader.onload = function (e) {
//					$('#img_id').attr('src', e.target.result);
//				}

//				reader.readAsDataURL(input.files[0]);
//			}
//		}
//});

function upload_img(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#img_id').attr('src', e.target.result);
                }

                reader.readAsDataURL(input.files[0]);
            }
        }

	
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

// Delete tag

//$("#videos_tags").on('click', 'a[id^=delete_tag-]', function(){  
//	var tag_primary_key = $(this).attr('id').split('-')[1];
	//console.log(tag_primary_key); //just checking
	//delete_tag(tag_primary_key);

function delete_tag(id){
	//if (confirm('Are you sure you want to delete this tag?')==true){
	//	$('#tag_id-'+ tag_primary_key ).hide();
	$.ajax({
		type: 'POST',
		url: "delete_tag/",
		data: {tag: id},
		dataType:'json',

		success: tag_delete_confirm,
		error : function(){alert('AJAX ERROR');}
	});
}
// recieve the response from ajax in json
function tag_delete_confirm(response){
	tag_id = JSON.parse(response);//deserialise the data returned from the view
	if (tag_id > 0) {
		console.log("we get the id")
		$('#tag_' + tag_id).remove();
		$('#tag_button_' + tag_id).remove();
	}
}

//create tabss
function createTab(){
	
	// Define the size of the rectangle that will be filled (basically the entire element)
			context.fillRect(0, 0, w, h);
			// Grab the image from the video
			context.drawImage(video, 0, 0, w, h);
	
	var dataURL = canvas.toDataURL('image/jpeg'); // can also use 'image/png'

	var drawDataURL = vid_canvas.toDataURL('image/png'); // can also use 'image/png'
	
	//console.log (dataURL);			

	var tag_title = document.getElementById('tag_title').value;
	var tag_description = document.getElementById('tag_description').value;
	
	// Create a <button> element
	var btn = document.createElement("div");        
	// Create a text node
	var t = document.createTextNode(tag_title);       
	// Append the text to <button>

	var span = document.createElement("span");
    
    span.appendChild(t);

	btn.appendChild(span);     
	// Append <button> to <body>                           
	
	document.getElementById('tag_tabs').appendChild(btn);
	
	// give the button a class
	btn.className += "newtag";  
	//position the button absolutely  
	
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
	  

	
	//output to comments box
	var tag_title = "<span class= \"tag_title\">"+ tag_title + "</span>";
	var tag_description = "<span class= \"tag_description\">"+ tag_description + "</span>";
	var tagtimecomments = "<span class=\"time_comments\">"+ curmins + ":" + cursecs + "</span>";
	//var commentcomments = "<span class=\"tag_description\">"+ comment + "</span>";
	var dataURLcomments =   dataURL ;
	
	tag_image = dataURLcomments
	tag_draw = drawDataURL
	
}


function playFromLoaded(start){
	var seekto = vid.duration * (start / 100) ;
	vid.currentTime = seekto;
	console.log("loaded works" + seekto)

	}

// Pause on typeing in tag title

$( "#tag_title" ).keypress(function() {
	vid.pause();
		playbtn.innerHTML = "play";	
});
	
// video seek position
function vidSeek(){
	var seekto = vid.duration * (seekslider.value / 100) ;
	vid.currentTime = seekto ;
	$('#overlay_vid').hide();

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
		eraseDrawing();
		$('#overlay_vid').delay(2000).hide();
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


function showSpecificToUser(user){
	$('.newtag').not('.user_' + user).hide();
	console.log(user);
	console.log("function running");
	$('.user_' + user).show();

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




