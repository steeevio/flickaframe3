//currently searching through every tag every 0.5 secs - not good!
	//Refresh tag objects every time different  group is shown - only objects should be currently visible - need group option first



// both startsecs and current time both round down at ppresent. What are the implications of this? What happens when two tags are close? round to 0.5?


// push currently made tags in the objects list





	// Get handles on the video 

var video = document.getElementById('video-placeholder');
// Initial playing state of youtube 
var myPlayerState = 2;

// creating the thumbnail on canvas
	//get image canvas element
		var canvas = document.getElementById('tag_canvas');
		// Get a handle on the 2d context of the canvas element
		var context = canvas.getContext('2d');
		// Define some vars required later
	
		// define canvas and context for drawing
		var vid_canvas = document.getElementById('video_canvas');
		var vid_context = vid_canvas.getContext('2d');

var canvas_draw_state, duration, vid, playbtn, seekslider, curtimetext, durtimetext, mutebtn, cur_group = 0, jumplink, createtab, w, h, ratio, curmins, cursecs, video_percent, tag_image, tag_draw, tag_objects, draw, eraser;



/*
Youtube api integration
*/

var youtube_id = $("#youtube_id").html();
console.log(youtube_id);
var player;

function onYouTubeIframeAPIReady() {
	console.log(youtube_id);



    player = new YT.Player('video-placeholder', {

       	width: 600,
       	height: 400,
        videoId: youtube_id,
        playerVars: {
            color: 'white',
            'autoplay': 0,
         	'controls': 0, 
         	'rel' : 0
      //      playlist: 'taJ60kskkns,FG0fTKAqZ5g'
        },
        events: {
            'onReady': initialize,
                   
        	onStateChange: onPlayerStateChange
        }
    });
}



function onPlayerStateChange(event) {
   //if (event.data == YT.PlayerState.PLAYING && !done) {
        // DO THIS
   // }
    myPlayerState = event.data;
    console.log(myPlayerState);
}




//my player initialisation
initialisePlayer();	


//Youtube initialisation
function initialize(){
 console.log("initialise works")
    // Update the controls on load
    updateTimerDisplay();
    updateProgressBar();
    
    duration = player.getDuration();
    console.log("initialize " + duration);
    // Clear any old interval.


    // Start interval to update elapsed time display and
    // the elapsed part of the progress bar every second.

    		   // var interval = setInterval(function () {
       			// updateTimerDisplay();
       				// updateProgressBar();
    				//}, 500);


    setInterval(function () {
        updateTimerDisplay();
        updateProgressBar();
    }, 500);

        //clearInterval(time_update_interval);
//setInterval(function(){ alert("Hello"); }, 3000);

	//sort out the vanvas size
		//dont know youtube video sizes so fix ratio to 16:9
	ratio = 16 / 9;
	
		//set the max height of the video for the page
	var max_height = $(window).height() * 0.6; 
	$("#video-placeholder").height(max_height);
	var max_width = max_height * ratio;
	$("#video-placeholder").width(max_width);

	//match videos container width to video
	$("#video_container").width(max_width);

			// Define the required width as 100 pixels smaller than the actual video's width
	w = video.videoWidth - 100;
			// Calculate the height based on the video's width and the ratio
	h = parseInt(w / ratio, 10);
			// Set the canvas width and height to the values just calculated
	canvas.width = w;
	canvas.height = h;	

	// set overlay size
	vid_width = $("#video-placeholder").innerWidth();
	vid_height = $("#video-placeholder").innerHeight();
	$('#overlay_vid').width(vid_width).height(vid_height);	

		//iff the screen is too narrow we need to adjust the maximum width of the video
	if (max_width > $("#video_outer").width()){
		//take off an extra 30px to fit placeholder inside container
		max_width = $("#video_outer").width() - 30;
		var max_height = max_width / ratio;
		
		$("#video-placeholder").height(max_height);
		$("#video-placeholder").width(max_width)
	
		//match videos container width to video
		$("#video_container").width(max_width);
	}

		// set the current time if coming from a tag url
	player.seekTo($('input[name=start_time_secs]').val());
	

}

// This function is called by initialize()
function updateTimerDisplay(){
    // Update current time text display.

    var time = player.getCurrentTime();

    $('#curtimetext').text(formatTime( time ));
    $('#durtimetext').text(formatTime( player.getDuration() ));
    checkTags();

   
}


function checkTags(){
	var time = Math.floor(player.getCurrentTime());
    	

	for (var i = 0; i < tag_objects.length; i++){
		
		this_start = Math.floor(tag_objects[i].startsecs);

		if(this_start == time){
			
			this_title = tag_objects[i].title;
			this_start = tag_objects[i].start;
			this_avatar = tag_objects[i].avatar;
			this_user = tag_objects[i].username;
			this_overlay = tag_objects[i].overlay;
			this_slide = tag_objects[i].tag_slide;
			//start_secs = duration * (this_start / 100)
			//makePopcornHandler(this_title, start_secs, this_avatar, this_overlay);
			//console.log(duration);
			//console.log(start_secs);


			document.getElementById( "current_tag" ).innerHTML = this_title;
			document.getElementById( "current_tag_avatar" ).innerHTML = this_avatar;
			document.getElementById( "current_tag_user" ).innerHTML = this_user;
			document.getElementById( "overlay_vid" ).innerHTML = "<img src='/static/video/" + this_overlay + "'>";
			document.getElementById( "display_slide" ).innerHTML = "<img src='/static/video/" + this_slide + "'>";
			$('#slide_zoom').show()
			//show the div with the drawing if the video is paused
			if (myPlayerState != 1){
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


function formatTime(time){
    time = Math.round(time);

    var minutes = Math.floor(time / 60),
    seconds = time - minutes * 60;

    seconds = seconds < 10 ? '0' + seconds : seconds;

    return minutes + ":" + seconds;
}

// This function is called by initialize()
function updateProgressBar(){
    // Update the value of our progress bar accordingly.
    $('#seekslider').val((player.getCurrentTime() / player.getDuration()) * 100);


}

var done = false;





//play pause function
function playPause(){
	if (myPlayerState != 1){ // check the youtube video state 1-5 - 1 is playing 2 is paused (-1 I think is stopped)
		player.playVideo();
		playbtn.innerHTML='<img src="/static/video/img/pause.png"/>';
		$('#overlay_vid').delay(2000).hide();
		}
		
	else {
		player.pauseVideo();
		playbtn.innerHTML='<img src="/static/video/img/play.png"/>';
			}
	}


//video mute
$('#mutebtn').on('click', function() {
    var mute_toggle = $(this);

    if(player.isMuted()){
        player.unMute();
        mutebtn.innerHTML='<img src="/static/video/img/unmute.png"/>';
    }
    else{
        player.mute();
        mutebtn.innerHTML='<img src="/static/video/img/mute.png"/>';	
    }
});


$('#seekslider').on('mouseup touchend', function (e) {

    // Calculate the new time for the video.
    // new time in seconds = total duration in seconds * ( value of range input / 100 )
    var newTime = player.getDuration() * (e.target.value / 100);

    // Skip video to new time.
    player.seekTo(newTime);

});





// Add a listener to wait for the 'loadedmetadata' state so the video's dimensions can be read
video.addEventListener('loadedmetadata', function() {


			// Calculate the ratio of the video's width to height
	//ratio = video.videoWidth / video.videoHeight;








	}, false);
	
	


 
canvas_draw_state = false;

function initialisePlayer (){
	
	//set object references
	vid = document.getElementById("video-placeholder");
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
	eraser.addEventListener("click", erase, false);
	draw.addEventListener("click", drawOnTag, false);
	//seekslider.addEventListener("change", vidSeek, false);
						
						//vid.addEventListener("timeupdate", seekTimeUpdate, false);

	//mutebtn.addEventListener("click", vidMute, false);	

	//duration = vid.duration;
	//console.log (duration);
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
	
	vid_width = $("#video-placeholder").innerWidth();
	vid_height = $("#video-placeholder").innerHeight();
	console.log (vid_height)
	vid_canvas.width  = vid_width;
	vid_canvas.height = vid_height;
	player.pauseVideo();

	//match the canvas div size to the current video size 
	$('#video_canvas').width(vid_width).height(vid_height);

	//display canvas div when drawing
	$('#video_canvas').show();
		
	//color the tag button to emphasise next click	
	$('#tag_button').css({'background-color' : '#00ff00'});
	canvas_draw_state = true;

	}


// on screen resize
$( window ).resize(function() {



	//dont know youtube video sizes so fix ratio to 16:9
	ratio = 16 / 9;
	
		//set the max height of the video for the page // control the video size to fit on the screen
	var max_height = $(window).height() * 0.6; 
	$("#video-placeholder").height(max_height);
	var max_width = max_height * ratio;
	$("#video-placeholder").width(max_width)
	
	//match videos container width to video
	$("#video_container").width(max_width);

			// Define the required width as 100 pixels smaller than the actual video's width
	w = video.videoWidth - 100;
			// Calculate the height based on the video's width and the ratio
	h = parseInt(w / ratio, 10);
			// Set the canvas width and height to the values just calculated
	canvas.width = w;
	canvas.height = h;	
	console.log($("#video_outer").width());

	//iff the screen is too narrow we need to adjust the maximum width of the video
	if (max_width > $("#video_outer").width()){
		//take off an extra 30px to fit placeholder inside container
		max_width = $("#video_outer").width() - 30;
		var max_height = max_width / ratio;
		
		$("#video-placeholder").height(max_height);
		$("#video-placeholder").width(max_width)
	
		//match videos container width to video
		$("#video_container").width(max_width);
	}
	


	vid_width = $("#video-placeholder").innerWidth();
	vid_height = $("#video-placeholder").innerHeight();
  	$('#overlay_vid').width(vid_width).height(vid_height);
});

$( document ).ready(function(response) {
 	
			// create an array of all users classes
    // create a hidden list of all the user_x generated in the html

    // Returns a NodeList
	var elems = document.getElementsByClassName( "hidden_user_class" );
	//console.log (elems);
	// Convert the NodeList to an Array
	var arr = jQuery.makeArray( elems );

	//random colours are annoying changing every instance so screw it...
	//end colours will be the ones used - see below
	colours = ["#3DA1FF", "#FFF", "#CCC", "#191970", "#C6064B", "#13B8E6", "#13B8E6", "#EA6626", "#3A4A83", "#6CF4D4", "#E49BED", "#DE0700", "#F55DE2", "#CA86EF", "#C8793B", "#40498B", "#E5EF05"]

    // for each item in an array  (This changes the colour everytime a class is used so probably a more effient way chnaging on unique classes)
    for (var i = 0; i < arr.length; i++) {
    	//console.log(arr[i].innerHTML)
    	var user_class = (arr[i].innerHTML)
    	//if $(arr[i].innerHTML) is unique
    	console.log(user_class)
    	
    	$("."+user_class).css("border-left-color", colours[i]);
    		
    	$("a."+user_class).css("color", colours[i]);
    	//$("a ."+user_class).attr('style', 'color:'+colours[i]+' !important')
    }



});




//create array for tag based on the loaded content in the DOM
function createTagObjects(){	

	tag_objects = [];

		$('.page_tags.newtag:visible').each(function(){
			tag_title_temp = $(this).find('h3').html()
			tag_start_temp = $(this).find('.tag_start').html()
			start_secs_temp = $(this).find('.tag_secs').html()
			tag_avatar = $(this).find('.tag_avatar').html()
			tag_username =$(this).find('.tag_username').html()
			tag_overlay = $(this).find('.tag_overlay').html()
		    var obj = {
		        id: this.id,
		        title: tag_title_temp,
		        start:tag_start_temp,
		        startsecs:start_secs_temp,
		        avatar:tag_avatar,
		        username:tag_username,
		        overlay:tag_overlay
		        //comments: []
		    };
		    tag_objects.push(obj);


		});
	};

createTagObjects();




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
	

							//console.log(seekTimeUpdate())
							//console.log(video_percent)
	var slide_id = $('#hidden_slide_id').html();						

	//console.log(tag_image)
	var title = $('#tag_title').val();
							//var time_secs = duration * (video_percent / 100);

	//start the video again
	player.playVideo();
	playbtn.innerHTML = "PAUSE";
	draw.innerHTML = "DRAW";	
	$('#tag_button').css({'background-color' : '#ccc'});
		
	var nt = player.getCurrentTime() * (  100 /  player.getDuration() );
	//seekslider.value = nt;
	video_percent = nt;
	console.log(video_percent);

	 

							timeSecs = Math.floor(player.getCurrentTime())
								console.log(timeSecs)


	//if(vid_canvas.toDataURL() == document.getElementById('blank').toDataURL()){
	if (canvas_draw_state == false){	
		console.log("Its blank!")
        tag_draw = "blank";	
    }
    tag_image = "blank";
	
	
    var tag_start_string = formatTime( timeSecs );
    console.log(tag_start_string)


	$.ajax({
		url:"create_tag/", //the end point
		type: "POST", //http method
		data : { slide_id: slide_id, cur_group: cur_group, tag_title: $('#tag_title').val(), tag_description: $('#tag_description').val(), tag_start_string: tag_start_string , tag_start: video_percent, tag_draw:tag_draw, tag_image:tag_image, time_secs:timeSecs }, // data sent with the post
		

		// handle success
		success : function(json){

			// remove all url before the last backslash on the tag image filename

			if (json.tag_image){
				var str = json.tag_image;
				var n = str.lastIndexOf('\\');
				var image_result = str.substring(n + 1);
			}

			$('#tag_title').val('');//clears field
			$('#tag_description').val('');//clears field
			
			$('#tags_on_load').prepend(
				"<div id=\"tag_" + json.tagpk  + " \" class=\"page_tags newtag user_"  + json.tag_user_id +  "  \" >" +
					"<div class=\"tag-left\">" +
						"<img class= 'image_comments' src='/static/video/uploaded_tag_images/default.png'>" + 
						"<div class=\"tag-time\">" + json.tag_start_string + "</div>"  +
						"<div class=\"tag_avatar\">" + 
							"<img class= \"user_avatar\" src=\"/static/video/" + json.user_avatar + "  \">" +
						"</div>"  +	
						"<div class=\"tag_username\">" + json.tag_username + "</div>" +
					"</div>" +

					"<div class=\"tag-right\">" +
					    "<h3>" + json.tag_title + "</h3>" +
						"<p>" + json.tag_description + "</p>" +
						"<div class=\"tag_start\">" + json.tag_start_string + "</div>" +
						"<div class=\"tag_secs\">" + json.time_secs + "</div>" +
						"<div class=\"tag_overlay\">" + json.tag_draw + "</div>" +
						"<button onclick = \"javascript:delete_tag( " + json.tagpk + "); \">Delete Tag</button>" + 
					"</div>" +

						
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




// seek / time update   --    not used in youtube
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
	
	//grab the canvas
	// Define the size of the rectangle that will be filled (basically the entire element)
									//context.fillRect(0, 0, w, h);
			// Grab the image from the video
									//context.drawImage(video, 0, 0, w, h); 
	
	//var dataURL = canvas.toDataURL('image/jpeg'); // can also use 'image/png'

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
	
	var tagtime = player.getCurrentTime() * (  100 / player.getDuration() );
	btn.style.left = tagtime +"%";
	
	btn.addEventListener("click", playFrom, false);
		function playFrom(){
		var seekto = player.getDuration() * (tagtime / 100) ;
		player.seekTo(seekto)

		//vid.currentTime = seekto ;
		}
	
// the below creates tag links at the bottom of the page - bit unneccessary now		
	// Create a <a> element
	//var taglink = document.createElement("button");        
	// Create a text node
	//var tnode = document.createTextNode(tag_title);       
	// Append the text to <button>
	//taglink.appendChild(tnode);     
	// Append <a> to <body>                           
	//document.getElementById('taglist').appendChild(taglink);
	
	// give the <a> a class
	//taglink.className += "newtaglink";  
	//position the button absolutely  
	
	
	//taglink.addEventListener("click", playFrom, false);
	
	
	// add a comment
	//var comment = document.getElementById("tag_description").value;
	  

	
	//output to comments box
	//var tag_title = "<span class= \"tag_title\">"+ tag_title + "</span>";
	
			
			//var tagtimecomments = "<span class=\"time_comments\">"+ curmins + ":" + cursecs + "</span>";
	//var commentcomments = "<span class=\"tag_description\">"+ comment + "</span>";
												//var dataURLcomments =   dataURL ;
	
												//tag_image = dataURLcomments
												tag_draw = drawDataURL
	
}
				

function playFromLoaded(start){
	var seekto = player.getDuration() * (start / 100) ;
	player.seekTo(seekto);
	$('#seekslider').val(start);
	$("#overlay_vid").hide();
	//console.log("loaded works" + seekto);
	var duration = player.getDuration();
	console.log("duration" + duration)
	}

// Pause on typeing in tag title

$( "#tag_title" ).keypress(function() {
	player.pauseVideo();
		playbtn.innerHTML = "play";	
});
	





