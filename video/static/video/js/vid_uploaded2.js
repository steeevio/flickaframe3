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
/*video.addEventListener('loadedmetadata', function() {
	console.log("loaded meta")


	

			// Calculate the ratio of the video's width to height
	ratio = video.videoWidth / video.videoHeight;

		//set the max height of the video for the page
	var max_height = $(window).height() * 0.6; 
	$("#my_video").height(max_height);
	var max_width = max_height * ratio;
	
	//match videos container width to video
	$("#video_container").width(max_width);

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
	
	*/

var canvas_draw_state, duration, vid, playbtn, seekslider, curtimetext, durtimetext, mutebtn, cur_group = 0, jumplink, createtab, w, h, ratio, curmins, cursecs, video_percent, tag_image, tag_draw, tag_objects, draw, eraser;
 
canvas_draw_state = false;

function initialisePlayer (){
	
	//set object references
	vid = document.getElementById("my_video");
	playbtn = document.getElementById("playpausebutton");
	draw = document.getElementById("draw");
//	seekslider = document.getElementById("seekslider");
	curtimetext = document.getElementById("curtimetext");
	durtimetext = document.getElementById("durtimetext");
	mutebtn = document.getElementById("mutebtn");
	createtab = document.getElementById("createtab");
	eraser = document.getElementById("eraser_button");

	//add event listeners
	playbtn.addEventListener("click", playPause, false);
	eraser.addEventListener("click", erase, false);
	draw.addEventListener("click", drawOnTag, false);
//	seekslider.addEventListener("change", vidSeek, false);
	vid.addEventListener("timeupdate", seekTimeUpdate, false);
	mutebtn.addEventListener("click", vidMute, false);	

	duration = vid.duration;
	console.log (duration);
};

// runs on upload to take a tag at a time supplied by the user
function setPoster(secs){
	video.addEventListener('loadedmetadata', function() {

		vid.currentTime = secs; //turn this on when not using the shitty django dev server and it might work
		console.log(secs);
		vid.oncanplaythrough = function() {
			setTimeout(function(){


				//grab the canvas
				// Define the size of the rectangle that will be filled (basically the entire element)
				context.fillRect(0, 0, w, h);
				// Grab the image from the video
				context.drawImage(video, 0, 0, w, h);
				var dataURL = canvas.toDataURL('image/jpeg'); // can also use 'image/png'

				var drawDataURL = vid_canvas.toDataURL('image/png'); // can also use 'image/png'
				var dataURLcomments =   dataURL ;
				tag_image = dataURLcomments
				
				$.ajax({
					url:"create_poster/", //the end point
					type: "POST", //http method
					data : { tag_image:tag_image }, // data sent with the post
					// handle success
					success : function(json){
						console.log("poster created")
					},

					// handle non success
					error : function(xhr,errmsg,err){
						$('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
						console.log(xhr.status + ": " + xhr.responseText)

					}
				});
				//back to the start
	   		
			console.log("has it been 0.5 secs?");
			}, 1000);	
		};

		
    
	});
	//playFromLoaded(0); // when off the dev server	

}

function checkTags(){
	var time = Math.floor(vid.currentTime);

	for (var i = 0; i < tag_objects.length; i++){
		
		this_start = Math.floor(tag_objects[i].startsecs);

		if(this_start == time){
			
			this_title = tag_objects[i].title;
			this_start = tag_objects[i].start;
			this_avatar = tag_objects[i].avatar;
			this_user = tag_objects[i].username;

			if (tag_objects[i].overlay != null) {
				this_overlay = tag_objects[i].overlay;
				document.getElementById( "overlay_vid" ).innerHTML = "<img src='" + static_url +"video/" + this_overlay + "'>";
			}

			if (tag_objects[i].slide != null) {
				this_slide = tag_objects[i].slide;
				document.getElementById( "display_slide" ).innerHTML =  this_slide;
				$('#slide_zoom').show();
			}


			document.getElementById( "current_tag" ).innerHTML = this_title;
			document.getElementById( "current_tag_avatar" ).innerHTML = this_avatar;
			document.getElementById( "current_tag_user" ).innerHTML = this_user;
			

			//show the div with the drawing if the video is paused
			if (vid.paused){
			$('#overlay_vid').show();
			}
			
			//show the drawing for a short time if the video is playing
			else {
			$('#overlay_vid').show();
			setTimeout(function() { $("#overlay_vid").hide(); }, 2000);
			
			}
		}
	};

	
};



//eraser drawing
function erase(){
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

	var max_height = $(window).height() * 0.6; 
	$("#my_video").height(max_height);
	var max_width = max_height * ratio;
	//match videos container width to video
	$("#video_container").width(max_width);


	vid_width = $("#my_video").innerWidth();
	vid_height = $("#my_video").innerHeight();
  	$('#overlay_vid').width(vid_width).height(vid_height);
});

$( document ).ready(function(response) {
 	
// set overlay size
	vid_width = $("#my_video").innerWidth();
	vid_height = $("#my_video").innerHeight();
	$('#overlay_vid').width(vid_width).height(vid_height);	

	console.log("loaded meta")


	

			// Calculate the ratio of the video's width to height
	ratio = video.videoWidth / video.videoHeight;

		//set the max height of the video for the page
	var max_height = $(window).height() * 0.6; 
	$("#my_video").height(max_height);
	var max_width = max_height * ratio;
	
	//match videos container width to video
	$("#video_container").width(max_width);

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




});






// event handler on tag submission - prevents default behaviour and calls function create_tag()
//$('#post_tag').on('submit', function(event){
//	createTab();
//	event.preventDefault();
//	console.log("seriously is this running on page load?") // just checking
//	create_post();
 
//});

function makeTag(){
	createTab();
	create_post();


}


//AJAX for posting
function create_post() {

	console.log("create post is working!") // just checking
	console.log($('#tag_title').val())
	console.log(seekTimeUpdate())
	console.log(video_percent)
	//console.log(tag_image)
	var title = $('#tag_title').val();
	var slide_id = $('#hidden_slide_id').html();
	console.log("This the slide id"+ slide_id)
	var time_secs = duration * (video_percent / 100);

	//start the video again
	vid.play();
	playbtn.innerHTML='<img src="'+ static_url +'video/img/pause.png"/>';//
		
	$('#tag_button').css({'background-color' : '#ccc'});
		

	 

	timeSecs = Math.floor(vid.currentTime)
		console.log(timeSecs)


	//if(vid_canvas.toDataURL() == document.getElementById('blank').toDataURL()){
	if (canvas_draw_state == false){	
		console.log("Its blank!")
        tag_draw = "blank";	
    }
	
	



	$.ajax({
		url:"create_tag/", //the end point
		type: "POST", //http method
		data : { slide_id: slide_id, cur_group: cur_group, tag_title: $('#tag_title').val(), tag_description: $('#tag_description').val(), tag_start_string: seekTimeUpdate(), tag_start: video_percent, tag_draw:tag_draw, tag_image:tag_image, time_secs:timeSecs }, // data sent with the post
		

		// handle success
		success : function(json){

			// remove all url before the last backslash on the tag image filename
			var str = json.tag_image;
			var n = str.lastIndexOf('\\');
			var image_result = str.substring(n + 1);

			var slide = json.slide_image;
			if(slide != null){
				insert_slide = "<img class= 'image_comments' src='" + media_url  + json.slide_image + "'>"
			}
			else{
				insert_slide = ""
			}
			var drawing = json.tag_draw;
			if(drawing != null){
				insert_drawing = "<img class= 'tag_overlay display' src='" + media_url  + json.tag_draw + "'>"
			}
			else{
				insert_drawing = ""
			}


			$('#tag_title').val('');//clears field
			$('#tag_description').val('');//clears field
			
			$('#tags_on_load').prepend(
				"<div id=\"tag_" + json.tagpk + "\">" +
					"<h3>" + json.tag_title + "</h3> " + 
					"<p>" + json.tag_description + "</p> " + 
					"</br> <img class= 'image_comments tatataat' src='" + media_url  + json.tag_image + "'> </br>" + 
					insert_slide + 
					"<button onclick = \"javascript:delete_tag( " + json.tagpk + "); \">Delete Tag</button>" + 
					"<div id=\"tag_username\">" + json.tag_user_email + "</div>"  +
					"<div id=\"tag_start\">" + json.tag_start_string + "</div>"  +
					insert_drawing + 
				"</div>")
			console.log(cur_group)
		},

		// handle non success

		error : function(xhr,errmsg,err){
			$('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
			console.log(xhr.status + ": " + xhr.responseText)

		}
	});
	erase();
	var this_avatar = $('.tag_avatar').first().html()
	var this_overlay = $('.tag_overlay').first().html()
	//makePopcornHandler(title, time_secs, this_avatar, this_overlay);
	
};




// seek / time update
function seekTimeUpdate(){
	var nt = vid.currentTime * (  100 / vid.duration );
	

	checkTags();
	
	//seekslider.value = nt;
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



    // need to check the tags everytime that it updates
    //$('.timeBar').css('width', video_percent+'%');
    //update HTML5 video current play time
   

    //edit custom time bar
    $('.timeBar').css('width', video_percent+'%');
	

	return curmins + ":" + cursecs;

	}


// bind mouse events to the custom time bar
var timeDrag = false;   /* Drag status */
$('.progressBar').mousedown(function(e) {
    timeDrag = true;
    updatebar(e.pageX);
});

$(document).mouseup(function(e) {
    if(timeDrag) {
        timeDrag = false;
        updatebar(e.pageX);
    }
});
$(document).mousemove(function(e) {
    if(timeDrag) {
        updatebar(e.pageX);
    }
});
 
//update Progress Bar control
var updatebar = function(x) {
    var progress = $('.progressBar');
    var maxduration = vid.duration; //Video duraiton
    var position = x - progress.offset().left; //Click pos
    var percentage = 100 * position / progress.width();
 
    //Check within range
    if(percentage > 100) {
        percentage = 100;
    }
    if(percentage < 0) {
        percentage = 0;
    }
 
    //Update progress bar and video currenttime
    $('.timeBar').css('width', percentage+'%');
    video.currentTime = maxduration * percentage / 100;
};

//create buffer bar
//loop to get HTML5 video buffered data
var startBuffer = function() {
    var maxduration = vid.duration;
    var currentBuffer = vid.buffered.end(0);
    var percentage = 100 * currentBuffer / maxduration;
    $('.bufferBar').css('width', percentage+'%');
 
    if(currentBuffer < maxduration) {
        setTimeout(startBuffer, 500);
    }
};
setTimeout(startBuffer, 500);






// Delete tag
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

//create tabs
function createTab(){
	
	//grab the canvas
	// Define the size of the rectangle that will be filled (basically the entire element)
			context.fillRect(0, 0, w, h);
			// Grab the image from the video
			context.drawImage(video, 0, 0, w, h);
	
	var dataURL = canvas.toDataURL('image/jpeg'); // can also use 'image/png'

	var drawDataURL = vid_canvas.toDataURL('image/png'); // can also use 'image/png'
	
	//console.log (dataURL);			

	var tag_title = document.getElementById('tag_title').value;
	var tag_description = document.getElementById('tag_description').value;
	var tag_description = "<span class= \"tag_description\">"+ tag_description + "</span>";
	
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
	btn.className += "newtag group_" + cur_group;  
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
	//var tag_title = "<span class= \"tag_title\">"+ tag_title + "</span>";
	
	var tagtimecomments = "<span class=\"time_comments\">"+ curmins + ":" + cursecs + "</span>";
	//var commentcomments = "<span class=\"tag_description\">"+ comment + "</span>";
	var dataURLcomments =   dataURL ;
	
	tag_image = dataURLcomments
	tag_draw = drawDataURL
	
}


function playFromLoaded(start){
	var seekto = vid.duration * (start / 100) ;
	vid.currentTime = seekto;
	$("#overlay_vid").hide();
	console.log("loaded works" + seekto);

	}

// Pause on typing in tag title

$( "#tag_title" ).keypress(function() {
	vid.pause();
		playbtn.innerHTML = "play";	
});
	

// Video Controls
/*
// video seek position
function vidSeek(){
	var seekto = vid.duration * (seekslider.value / 100) ;
	vid.currentTime = seekto ;
	$('#overlay_vid').hide();

	}
*/

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
		playbtn.innerHTML='<img src="' + static_url +'video/img/pause.png"/>';//
		$('#overlay_vid').delay(2000).hide();
		}
		
	else {
		vid.pause();
		playbtn.innerHTML='<img src="' + static_url +'video/img/play.png"/>';
			}
	}


//video mute
function vidMute(){
	if (vid.muted){
		vid.muted=false;
		mutebtn.innerHTML='<img src="' + static_url +'video/img/unmute.png"/>';
		}
	else {
		vid.muted=true;
		mutebtn.innerHTML='<img src="' + static_url +'video/img/mute.png"/>';	
	}
}










