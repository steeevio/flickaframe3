
// accept/reject moderation items
function acceptReject(tag, response){ //2:accept 3:reject

console.log(tag + response+ "ajax bitch");
    $.ajax({
        url:"respond_moderation/", //the end point
        type: "POST", //http method
        data : { tag:tag, response:response }, // data sent with the post
        

        // handle success
        success : function(json){

            if (response == 3){
                $('.confirmation').prepend(
                    "<h5>You have rejected this tag</h5>")
            }

            if (response == 2){
                $('.confirmation').prepend(
                    "<h5>Tou have accepted this tag</h5>")
            }

            $(".moderation-item-" + tag).hide()
           
        },        

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
        
};



//showhide group settings
function displayManagersSettings(){
    $('.managers_settings').toggle(300);
}
function displayModerate(){
    $('.moderation').toggle(300);
}
// show hide upload form - youtube / upload
function showHide(show, hide){
    $(show).show(500);
    $(hide).hide(500);
    //empty the value that is hidden
    $('input[name=youtube_id]').val("");
    $('input[name=video_file]').val("");
    $('input[name=poster_time]').val(0);
    console.log(show, hide)
}


// display comment reply form
function displayCommentReply(comment_id){
    $('#comment_form_' + comment_id).show()
}




//adds a comment via ajax - on tag page currently -
//levels : 1 = tag comment , 2= video comment, 3 = group coment, 4 = reply to a comment
function makeComment(comment_id, level){
    var parent = 0;
    var comment = $('#comment_entry').val();
    var level = level;
    var group = 0;

    if ($('#current_group_id').length){ // we are saving on a video so we need to pass which group is showing
        group = $('#current_group_id').html()
    }


    if (level == 4){ //then we know  that this is a reply to a comment
        var parent = comment_id
        var comment = $('#comment_entry_' + comment_id).val();
        $('#comment_form_' + comment_id).hide()
    }

    console.log("making a comment");
    $.ajax({
        url:"comment/", //the end point
        type: "POST", //http method
        data : { comment:comment, level:level, parent:parent, group:group }, // data sent with the post

        // handle success
        success : function(json){
        var level = json.level
        var parent_id = json.parent_id

        if (level < 4){
            $('#comments').prepend(
                "<div class='comment_outer comment_reply comment_reply_" + json.comment_id + "'> " +
                "<div class='comment_" + json.comment_id +"'></div>" +
                "<div class='comment_avatar'> " +
                    " <img class='user_avatar' src='/media/" + json.user_avatar + "' > "+
                "</div> " +
                "<h4>" + json.comment + "</h4>" +
                "<h6>"+ json.user_name + "</h6>" +
                
            "</div>")   
            }
        else{
            $('#comment_replies_'+ parent_id ).prepend(

            "<div class='comment_outer comment_reply comment_reply_" + json.comment_id + "'> " +
                "<div class='comment_" + json.comment_id +"'></div>" +
                "<div class='comment_avatar'> " +
                    " <img class='user_avatar' src='/media/" + json.user_avatar + "' > "+
                "</div> " +
                "<h4>" + json.comment + "</h4>" +
                "<h6>"+ json.user_name + "</h6>" +
                
            "</div>"  
            )   
            $('#comment_form_' + comment_id).hide()
            }
            console.log('#comment_replies_'+ parent_id)
        },        

        // handle non success
        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
    
}



//resive div heights for tags on page resize - equal heights

$(window).resize(function(){
        
    var highestBox = 0;
    $('.block_item').each(function(){
    
        if($(this).height() > highestBox) 
           highestBox = $(this).height(); 
        });  

    $('.block_item').height(highestBox);          

});


// resize the slide on click zoom icon

$( "#slide_zoom" ).click(function() {
    console.log('click works')
    $('#display_slide').toggleClass('zoom_slide');

    if ($( "#display_slide" ).hasClass( "zoom_slide" )){
       $('#slide_zoom').html('<img src="'+ static_url + 'video/img/zoom-in.png"/>')

    } 
    else{
        $('#slide_zoom').html('<img src="'+ static_url + 'video/img/zoom-out.png"/>')
    }
    
});



// also need to get the groupspecific thing working 

function editContent(){
    $('.edit_button').hide();
    $('.save_button').show();
    $('#slides_dropdown_hidden').show();
    //get the content of the fields
    var titleHtml = $(".editable_title").html();
    var descHtml = $(".editable_description").html();
// create dynamic textareas
    var editableTitle  = $("<textarea />");
    var editableDescription = $("<textarea />");
    //add classes to style textareas
    editableTitle.addClass('form_title')
    editableDescription.addClass('form_content')
    // fill the textarea with the div's text
    editableTitle.val(titleHtml);
    editableDescription.val(descHtml);
    $('.editable_title').replaceWith(editableTitle);
    $('.editable_description').replaceWith(editableDescription);
}

function saveContent(){
    var oldSlide = $("#old_slide").html();
    $('#id_old_slide').val(oldSlide);

    var newSlide = $("#hidden_slide_id").html();
    $('#id_slide').val(newSlide);

    var title = $('.form_title').val()
    $('#id_title').val(title);

    var desc = $('.form_content').val()
    $('#id_description').val(desc);


    $('#hidden_form').submit();
    

}


//create arrays 
var groups_manager = []
var groups_accepted = []

//loop through list of groups
function checkGroupMembership(group){
    console.log("lol" + groups_accepted)
    var number_of_groups_manager = 0;
    var number_of_groups_accepted = 0;
    var group_taggers_status = $('.group_tagger_status_'+ group).html();
    var group_drawing_status = $('.group_drawing_status_'+ group).html();
    console.log("lol2" + group_taggers_status)
    var group_taggers_status_int = parseInt(group_taggers_status);
    var group_drawing_status_int = parseInt(group_drawing_status);
    //looping through each group
    // we cycle through each group we are a manager of and if it is 
    //the same as the current group the var number goes up - if it's more than 0 we  are a member
    for (var i = 0; i < groups_manager.length; i++) {
        if(groups_manager[i] == group){
            number_of_groups_manager++;    
        }
    }
    for (var i = 0; i < groups_accepted.length; i++) {
        if(groups_accepted[i] == group){
           
            number_of_groups_accepted++;    
            
        }
    }
    console.log("checking membership")
    if (number_of_groups_manager > 0){ //you all is a manager so you can tag what you like
        $('.member_status_form').css({'display' : 'block'});
        $('.member_status_message').css({'display' : 'none'});
        $('#right-column').prepend("Manager");
        $('#draw').css({'display' : 'block'});//show the draw button for managers
        $('#eraser_button').css({'display' : 'block'});
        
        console.log("test"+1)
    }
    else if(number_of_groups_accepted > 0 && group_taggers_status_int == 1){ //your a member and members are allowed to tag on this group
        $('.member_status_form').css({'display' : 'block'});
        $('.member_status_message').css({'display' : 'none'});
        if(group_drawing_status_int == 2){
            $('#draw').show();
            $('#eraser_button').css({'display' : 'block'});
        }
        else {
            $('#draw').hide();
            $('#eraser_button').hide()
        }
        console.log("test"+2)
    }
    else if(number_of_groups_manager == 0 && number_of_groups_accepted == 0) {// you aint a member sonny
        $('.member_status_form').css({'display' : 'none'});
        $('.member_status_message').html("You need to join this group before you can add tags to it, <a href='/video/social_group/" + group +"/''>click here</a>")
        $('.member_status_message').css({'display' : 'block'});
        $('#draw').hide();
        $('#eraser_button').hide()
        console.log("test"+3)
    }

    else { // you're a member but members cant tag
        $('.member_status_form').css({'display' : 'none'});
        $('.member_status_message').html("Sorry only managers are allowed to tag on this group")
        $('.member_status_message').css({'display' : 'block'});
        $('#draw').hide();
        $('#eraser_button').hide()
        console.log("test"+4)
            
    }
}    

//create array for tag based on the loaded content in the DOM
function createTagObjects(){    
    console.log("why cant i zee dis?");

    tag_objects = [];

        $('.page_tags.newtag:visible').each(function(){
            tag_title_temp = $(this).find('h5').html()
            
            tag_start_temp = $(this).find('.tag_start').html()
            start_secs_temp = $(this).find('.tag_secs').html()
            tag_avatar = $(this).find('.tag_avatar').html()
            tag_username =$(this).find('.tag_username').html()
            tag_overlay = $(this).find('.tag_overlay').html()
            tag_slide = $(this).find('.tag_slide').html()
            var obj = {
                id: this.id,
                title: tag_title_temp,
                start:tag_start_temp,
                startsecs:start_secs_temp,
                avatar:tag_avatar,
                username:tag_username,
                overlay:tag_overlay,
                slide:tag_slide,
                //comments: []
            };
            tag_objects.push(obj);

           


        });
    };





$( document ).ready(function(response) {

    console.log("BOOM")

// move the color changing into generic

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

 



    //create an array of all the groups the member is accepted
    $(".groups_accepted_id").each(function() { groups_accepted.push($(this).text()) });
    console.log(groups_accepted)
    //create an array of all the groups the member is manager of
    $(".groups_manager_id").each(function() { groups_manager.push($(this).text()) });
    console.log(groups_accepted)

    // video view from a group needs to check the group and run showSpecificToGroup- 
    group_id = $("#current_group_id").html()
    console.log(group_id + "hello")
    group_title = $("#group_showing").html()

    if (group_id > 0){
        console.log("checking on load");

        showSpecificToGroup(group_title, group_id);
    }
 
    // submit comment on click - prevents default action so ajax runs
    $('#comment_form').on('submit', function(event){
    makeComment();
    
    event.preventDefault();
    
    
    });

    // moving stupid radio labels below inputs so foundation can style them to switches/// 
    // First remove the ul and li tags - if there are any
    $('.radio ul').contents().unwrap();
    $('.radio li').contents().unwrap();
    //get the contents of the input
    var label_contents = $('.radio > label > input').html();
    // Then move the input to outside of the label
    $('.radio > label > input').each(function() {
        //getting the label
        var label_contents = $(this).parent().text();
        console.log("this html" + label_contents);
        $(this).parent().parent().prepend(label_contents);

        //move it before
        $(this).parent().before(this);

    });
    $('.radio label:first-of-type').remove()
    // Then apply the jQuery UI buttonset
    //$( ".radio" ).buttonset();

});

$(window).load(function()  {

    //make all the page_tags the same height - equal height
    var highestBox = 0;
    $('.block_item').each(function(){
        console.log($(this).height())
        if($(this).height() > highestBox) {
           highestBox = $(this).height(); 
        }
       console.log(" height" + highestBox)
        });  

    $('.block_item').height(highestBox);     
});



function message(message){

    alert("You need to login or create an account to join this group");
}

//generic funtions

// run function to preview image on upload
function upload_img(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#img_id').attr('src', e.target.result);
                }

                reader.readAsDataURL(input.files[0]);
            }
        }



// Show specific tags based on user class
function showSpecificToUser(user, username, group_id, group_title){
	
	$('.newtag').not('.user_' + user).addClass( "tag_hide" )

	console.log(user);
	console.log("function running");
	
	$('.user_' + user).removeClass( "tag_hide" )
    $('.newtag').not('.group_' + cur_group).addClass( "tag_hide" )
	//show the title above
	$("#user_showing").html(username);

    //set the group
    $("#group_showing").html(group_title);
    $("#current_group_id").html(group_id);

    //clearInterval(interval);
    //interval = 0;

    createTagObjects();
    console.log("recreating objects1")

}

// Show specific tags based on group class
function showSpecificToGroup(group_title, group_id){
	$('.newtag').not('.group_' + group_id).addClass( "tag_hide" )

	$("#group_showing").html(group_title);
	$("#current_group_id").html(group_id);
	$("#user_showing").html("All");
	console.log("group function running");
	$('input[name=current_group_input]').val(group_id);
	var cur_group_string = $('input[name=current_group_input]').val();
	//var cur_group_string = $("#current_group_id").html();
	console.log(cur_group_string);
	cur_group = cur_group_string

    $('.newtag').not('.group_' + group_id).addClass( "tag_hide" )
    $('.group_' + group_id).removeClass( "tag_hide" )
	//cur_group = parseInt(cur_group_string)
	console.log (cur_group);
	//cur_group = group_id;
	// adds a random colour to every tab
	//$( ".newtag span" ).each(function( i ) {
 	//$(this).css("border-left-color", getRandomColor);
    createTagObjects();
    console.log("recreating objects2")
    checkGroupMembership(group_id);
    console.log("checking specific to grop");
    $('#user_drop ul.member_drop').remove();
    $('ul.drop_' + group_id).clone().appendTo('#user_drop');

    $('#slides_dropdown li.slide_group').not('.group_' + group_id).addClass( "tag_hide" )
    



}


// Generate colours for tabs
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

//ajax pst for adding a slide to a group
function slideToGroup(slide, group){
    $.ajax({
        url:"connect_slide/", //the end point
        type: "POST", //http method
        data : { slide:slide, group:group }, // data sent with the post
        

        // handle success
        success : function(json){
            console.log("Success")
            var this_slide = $(".slide_"+ slide)
            $("#slide_list").prepend(this_slide);
            
           
        },

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
    $(".join-button").hide();
};

// ajax post for users requesting to join a group
function requestGroup(user, group, access){

console.log(user + group);
    $.ajax({
        url:"request_group/", //the end point
        type: "POST", //http method
        data : { user:user, group:group }, // data sent with the post
        

        // handle success
        success : function(json){
            console.log("Success")
            if (access == 1){
                console.log("Success access 1")
                $('.confirmation').prepend(
                    "<h5> You have joined this group</h5>")
            }

            if (access == 2){
                console.log("Success access 2")
                $('.confirmation').prepend(
                    "<h5> You have requested to join this group</h5>")
            }
           
        },

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
    $(".join-button").hide();
    
};

// ajax post for users requesting to join a group
function tagToCollection(collection, tag){
    $.ajax({
        url:"collect_tag/", //the end point
        type: "POST", //http method
        data : { tag:tag, collection:collection }, // data sent with the post
        

        // handle success
        success : function(json){


            $(".collection_" + collection).remove();
            
            $("#collections_dropdown").prepend("<h5>Added to collection</h5>");
           
        },

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });    
};


// ajax post for invitiing to join a group - just changes the membership status 
function userInvite(member, response){

console.log(member + response);
    $.ajax({
        url:"user_invite/", //the end point
        type: "POST", //http method
        data : { member:member, response:response }, // data sent with the post
        

        // handle success
        // handle success
        success : function(json){


            $('.confirmation').prepend(
                "<h4>User Invited</h4>"+
                "<div>"  + json.user_name +  "</div>" +
                "<div>" + 
                    "<img class= \"user_avatar\" src=\" "+ media_url + json.user_avatar + "  \">" +
                "</div>"
                );
            $(".user-item-" + json.user_id).hide();
        },        
       

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
    
    
};

// ajax post for accepting / declining requests to join a group - just changes the membership status 
function approveDecline(member, response){

console.log(member + response);
    $.ajax({
        url:"confirm_member/", //the end point
        type: "POST", //http method
        data : { member:member, response:response }, // data sent with the post
        

        // handle success
        success : function(json){

            if (response == 5){
                $('.confirmation').prepend(
                    "<h1> You have declined this group</h1>")
            }

            if (response == 2){
                $('.confirmation').prepend(
                    "<h1>Accepted</h1>")
            }

            if (response == 3){
                $('.confirmation').prepend(
                    "<h1>Request to join rejected</h1>")
            }

            $(".membership-item-" + member).hide()

           
        },        

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
        
};

// ajax post for accepting / declining invitations to join a group - just changes the membership status 
function acceptDecline(group, response){

console.log(group + response);
    $.ajax({
        url:"respond_member/", //the end point
        type: "POST", //http method
        data : { group:group, response:response }, // data sent with the post
        

        // handle success
        success : function(json){

            if (response == 5){
                $('.confirmation').prepend(
                    "<h1> You have declined this group</h1>")
            }

            if (response == 2){
                $('.confirmation').prepend(
                    "<h1>Accepted</h1>")
            }

            if (response == 3){
                $('.confirmation').prepend(
                    "<h1>Request to join rejected</h1>")
            }

            $(".membership-item-" + group).hide()

           
        },        

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
        
};

//ajax post for checking seach field - adding users on the group page

$(function(){
    $("#search").keyup(function(){
        $.ajax({
            type:"POST",
            url: "user_search/",
            data: {
                'search_text': $("#search").val(),
                "crsfmiddlewaretoken": $("input[name=crsfmiddlewaretoken]").val
            },
            success: searchSuccess,
            dataType: "html",

            error : function(xhr,errmsg,err){
                $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
                console.log(xhr.status + ": " + xhr.responseText)

        }

        });

    });
});

function searchSuccess(data, textStatus, jqXHR){
    $("#search-results").html(data)
}

//ajax post for checking seach field - adding video on the group page

$(function(){
    $("#search-videos").keyup(function(){
        $.ajax({
            type:"POST",
            url: "video_search/",
            data: {
                'search_text': $("#search-videos").val(),
                "crsfmiddlewaretoken": $("input[name=crsfmiddlewaretoken]").val
            },
            success: searchVideoSuccess,
            dataType: "html",

            error : function(xhr,errmsg,err){
                $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
                console.log(xhr.status + ": " + xhr.responseText)

        }

        });

    });
});
function searchVideoSuccess(data, textStatus, jqXHR){
    $("#search-videos-results").html(data)
}

$(function(){
    $("#search-groups").keyup(function(){
        console.log("hello")
        $.ajax({
            type:"POST",
            url: "group_search/",
            data: {
                'search_text': $("#search-groups").val(),
                "crsfmiddlewaretoken": $("input[name=crsfmiddlewaretoken]").val
            },
            success: searchGroupSuccess,
            dataType: "html",

            error : function(xhr,errmsg,err){
                $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
                console.log(xhr.status + ": " + xhr.responseText)

        }

        });

    });
});
function searchGroupSuccess(data, textStatus, jqXHR){
    $("#search-groups-results").html(data)
}

// function that adds a video to a group - ajax

function addVideoToGroup(video_id){
    console.log(video_id);
    $.ajax({
        url:"link_video_group/", //the end point
        type: "POST", //http method
        data : { video_id:video_id }, // data sent with the post
        

        // handle success
        success : function(json){


            $('#video_list').prepend(
                "<div>"  + json.video_title +  "</div>")
            $(".video-item-" + video_id).hide()

        },        

        // handle non success

        error : function(xhr,errmsg,err){
            $('#results').html("<div class='alert-box alert radius' data-alert> Failed again steve!" +errmsg+ "<a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText)

        }
    });
    
  


}

// Delete tag
function delete_tag(id){
    //if (confirm('Are you sure you want to delete this tag?')==true){
    //  $('#tag_id-'+ tag_primary_key ).hide();
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

// Delete Slide
function delete_slide(id){
    //if (confirm('Are you sure you want to delete this tag?')==true){
    //  $('#tag_id-'+ tag_primary_key ).hide();
    $.ajax({
        type: 'POST',
        url: "delete_slide/",
        data: {slide: id},
        dataType:'json',

        success: slide_delete_confirm,
        error : function(){alert('AJAX ERROR');}
    });
}
// recieve the response from ajax in json
function slide_delete_confirm(response){
    slide_id = JSON.parse(response);//deserialise the data returned from the view
    if (slide_id > 0) {
        console.log("we get the id")
        $('#slide_' + slide_id).remove();
        $('#tag_button_' + slide_id).remove();
    }
}
//this just puts the preview and id into the tag form before the form is saved
function slideToTag(id){
    $("#hidden_slide_id").empty()
    $('#selected_slide').empty()
    
    $(".slide_id_" + id).first().clone().appendTo('#selected_slide');
    
    $("#hidden_slide_id").html(id);
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




