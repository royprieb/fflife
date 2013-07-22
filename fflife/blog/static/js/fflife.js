// app specific jquery functions
$(document).ready(function() {
    $('#carTab').click(function() {
        $('#modItem').removeClass("active");
        $('#galleryItem').removeClass("active");
        $('#postsItem').removeClass("active");
        $('#carItem').addClass("active");
        $('#modContent').hide();
        $('#galleryContent').hide();
        $('#postsContent').hide();
        $('#carContent').fadeIn();
        });
    $('#postsTab').click(function() {
        $('#modItem').removeClass("active");
        $('#galleryItem').removeClass("active");
        $('#carItem').removeClass("active");
        $('#postsItem').addClass("active");
        $('#modContent').hide();
        $('#galleryContent').hide();
        $('#carContent').hide();
        $('#postsContent').fadeIn();
        });
    $('#modTab').click(function() {
        $('#galleryItem').removeClass("active");
        $('#postsItem').removeClass("active");
        $('#carItem').removeClass("active");
        $('#modItem').addClass("active");
        $('#galleryContent').hide();
        $('#postsContent').hide();
        $('#carContent').hide();
        $('#modContent').fadeIn();
        });
    $('#galleryTab').click(function() {
        $('#postsItem').removeClass("active");
        $('#modItem').removeClass("active");
        $('#carItem').removeClass("active");
        $('#galleryItem').addClass("active");
        $('#postsContent').hide();
        $('#modContent').hide();
        $('#carContent').hide();
        $('#galleryContent').fadeIn();
        });
});

$(document).ready(function() {  
    $("#usernavbar li").each(function() {            
        if (document.URL.toUpperCase().indexOf($(this).attr('id').toUpperCase()) > -1) 
        {
            $(this).addClass("isSelected");
        }
    });
});

$(document).ready(function() {
    $("#garagelist li").each(function() {
        if (document.URL.toUpperCase().indexOf($(this).attr('id').toUpperCase()) > -1)
        {
            $(this).addClass("isSelected");
        }
    });
});

$(document).ready(function() {
    jQuery.validator.addMethod("noSpace", function(value,element){
        return value.indexOf(" ") < 0 && value != "";
        },"Spaces are not allowed");
    
   $('#newCarForm').validate({
    rules:{
        name: {
            required: true,
            maxlength: 100,
            },
        image: "required",
        make: {
            required: true,
            maxlength:100,
            },
        model: {
            required: true,
            maxlength: 100,
            },
        year: {
            required: true,
            number: true,
        },
    }
    });
   $('#editCarForm').validate({
    rules:{
        name: {
            required: true,
            maxlength: 100,
            },
        make: {
            required: true,
            maxlength: 100,
            },
        model: {
            required: true,
            maxlength: 100,
            },
        year: {
            required: true,
            number: true,
        },
    }
    });
   $('#newPostForm').validate({
    rules:{
        title:{
            required: true,
            maxlength: 100,
            },
    }
    });
   $('#editPostForm').validate({
    rules:{
        title:{
            required: true,
            maxlength: 100,
            },
    }
    });
   $('#newModForm').validate({
    rules:{
        modType: {
            required: true,
            maxlength: 100,
            },
        brand: {
            required: true,
            maxlength: 100,
            },
        part: {
            required: true,
            maxlength: 100,
            },
    }
    });
   $('#editModForm').validate({
    rules:{
        modType: {
            required: true,
            maxlength: 100,
            },
        brand: {
            required: true,
            maxlength: 100,
            },
        part: {
            required: true,
            maxlength: 100,
            },
    }
    });
   $('#newPhotoForm').validate({
    rules:{
        caption:{
            maxlength: 100,
            },
        photo: "required",
    }
    });
   $('#msgForm').validate({
    rules:{
        subject: {
            required: true,
            maxlength: 100,
            },
        message: "required",
    }
    });
   $('#commentForm').validate({
    rules:{
        body: "required",
    }
    });
   $('#newGroupForm').validate({
    rules:{
        title: {
            required: true,
            maxlength: 100,
            },
        description: "required",
    }
    });
   $('#topicForm').validate({
    rules:{
        body: "required",
    }
    });
   $('#topicResponseForm').validate({
    rules:{
        body: "required",
    }
    });
   $('#signInForm').validate({
    rules:{
        username: "required",
        password: "required",
    }
    });
   $('.feedback').validate({
    rules:{
        msg_title:{
            required: true,
            maxlength: 30,
            },
        msg_body:"required",
    }
    });
   $('#newAccountForm').validate({
    rules:{
        username: {
            required: true,
            noSpace: true,
            maxlength: 50,
            },
        email: {
            required: true,
            email: true,
            },
        password: "required",
        photo: "required",
        motto:{
            required: true,
            maxlength: 50,
            },
        city:{
            maxlength: 50,
            },
        state:{
            maxlength: 50,
            },
        country:{
            maxlength: 50,
            },
    }
    });
   $('#editAccountForm').validate({
    rules:{
        username: {
            required: true,
            noSpace: true,
            maxlength: 50,
            },
        email: {
            required: true,
            email: true,
            },
        motto: {
            required: true,
            maxlength: 50,
            },
        city:{
            maxlength: 50,
            },
        state:{
            maxlength: 50,
            },
        country:{
            maxlength: 50,
            },
    }
    });
});

$(document).ready(function() {
    $('.carMakeTypeahead').typeahead({
        source: function(query,process){
            return $.getJSON(
                             '/carmake',
                             { query: query },
                             function (data){
                                return process(data);
                             }
                             );
        }
    });
    $('.carModelTypeahead').typeahead({
        source: function(query,process){
            var make = $('.carMakeTypeahead').val()
            if (make == ''){
                return $.getJSON(
                                 '/carmodel?make=all',
                                 { query: query },
                                 function (data){
                                    return process(data);
                                    }
                                );
                }else{
                return $.getJSON(
                                 '/carmodel?make=' + make,
                                 { query: query },
                                 function (data){
                                    return process(data);
                                    }
                                );
                }
        }
    });
    $('.modTypeTypeahead').typeahead({
        source: function(query,process){
            return $.getJSON(
                             '/modtype',
                             { query: query },
                             function (data){
                                return process(data);
                             }
                             );
        }
    });
    $(".editModLink").click(function(){
        var data = $(this).attr('data');
        var url = "/details/mod/" + data + "/";
        $.getJSON(url, function(mod){
            $("input#id_modType_edit").val(mod['modType']);
            $("input#id_brand_edit").val(mod['brand']);
            $("input#id_part_edit").val(mod['part']);
            $("form#editModForm").attr('action', mod['target']);
            });
    });
});

$(document).ready(function() {
    $("#removePhoto").click(function(){
        $('#gallery').hide();
        $('#gallery_edit').fadeIn();
        $('#removePhoto').hide();
        $('#viewPhotosItem').removeAttr('style');
    });
    $("#viewPhotos").click(function(){
        $('#gallery_edit').hide();
        $('#gallery').fadeIn();
        $('#viewPhotosItem').attr('style','display:none;');
        $('#removePhoto').fadeIn();        
    });
    $("#topblogslink").click(function(){
        $('#recentpostslist').hide();
        $('#topblogslist').fadeIn();
    });
    $("#recentpostslink").click(function(){
        $('#topblogslist').hide();
        $('#recentpostslist').fadeIn();
    });
    $("#mostmemberslink").click(function(){
        $('#mostrecentlist').hide();
        $('#mostmemberslist').fadeIn();
    });
    $("#mostrecentlink").click(function(){
        $('#mostmemberslist').hide();
        $('#mostrecentlist').fadeIn();
    });
    $(".lightBoxLink").click(function(){
        var data = $(this).attr('data');
        var title = $(this).attr('title');
        $('#lightBoxImg').attr('src', data);
        $('#lightboxtitle').text(title);
        $('#downloadlink').attr('href', data);
        $('#downloadlink').attr('download','photo');
    });
    $(".followLink").click(function(){
        var data = $(this).attr('data'); 
        var url = "/journal/" + data + "/follow/";
        $.getJSON(url, function(count){ 
            $("#followcount").text(count['count']); 
            }); 
        $('.followLink').hide();
        $('.unFollowLink').fadeIn();
    }); 
    $(".unFollowLink").click(function(){
        var data = $(this).attr('data');
        var url = "/journal/" + data + "/unfollow/";
        $.getJSON(url, function(count){
            $("#followcount").text(count['count']);
            });
        $('.unFollowLink').attr('style','display:none;');
        $('.followLink').fadeIn();
    });
    $(".votelink").click(function(){
        var url = $(this).attr('data');
        $.getJSON(url, function(count){
            $("#fastvotecount").text(count['fastcount']);
            $("#freshvotecount").text(count['freshcount']);
            });
    });
    $(".likelink").click(function(){
        var url = $(this).attr('data');
        var targetid = $(this).attr('targetid');
        $.getJSON(url, function(count){
            $(targetid).text(count['likecount']);
            });
    });
    $("#deleteGroup").click(function(){
        $('#deleteAlert').fadeIn();
    });
    $("#cancelDelete").click(function(){
        $('#deleteAlert').hide();
    });
    $("#deleteTopic").click(function(){
        $('#topicDeleteAlert').fadeIn();
    });
    $("#cancelTopicDelete").click(function(){
        $('#topicDeleteAlert').hide();
    });
    $(".deleteResponse").click(function(){
        $('#responseDeleteAlert').fadeIn();
        var url = $(this).attr('data');
        $('#responseDeleteLink').attr('href',url);
    });
    $("#cancelResponseDelete").click(function(){
        $('#responseDeleteAlert').hide();
    });
    $("#groupLeave").click(function(){
        $('#groupLeaveAlert').fadeIn();
    });
    $("#cancelGroupLeave").click(function(){
        $('#groupLeaveAlert').hide();
    });
});

$(document).ready(function() {
    $("iframe").attr('width','300');
    $("iframe").attr('height','244');
});

$(document).ready(function() {
    $("#boardSelect").change(function(){
        var title =$("#boardSelect option:selected").text();
        $("#boardTitle").text(title);
        var data =$("#boardSelect option:selected").attr('data');
        var url = '/boardDetails/' + data + '/';
        var action = '/photoboard/' + data + '/upload/'
        $("#newPhoto form").attr('action', action)
        var photos_html = ''
        $.getJSON(url, function(photos){
            for (var i = 0; i < photos.length; i++){
                photos_html += '<li><a href="' + photos[i]['href'] + '"><img src="' + photos[i]['image'] + '"/></a><p class="text-right"><i class="icon-heart"></i> ' + photos[i]['likes'] + '</p></li>';
            }
            $("ul#boardphotos").html(photos_html);
            });       
        });
    $(".likeBoardPhoto").click(function(){
        var url = $(this).attr('data');
        $.getJSON(url, function(count){
            var likecount = count['likecount'];
            like_html = '<i class="icon-heart"></i> ' + likecount;
            $(".likeBoardPhoto").html(like_html);
            });
        });
    $("#deleteBoardPhoto").click(function(){
        $('#deleteBoardPhotoAlert').fadeIn();
    });
    $("#cancelBoardPhotoDelete").click(function(){
        $('#deleteBoardPhotoAlert').hide();
    });
});

$(document).ready(function() {
    $(window).scroll(function(){
        if($(window).scrollTop() == $(document).height() - $(window).height()){
            $('div#loadmoreajaxloader').show();
            var data = $('div#loadmoreajaxloader').attr('data'); 
            var page = $('div#loadmoreajaxloader').attr('page');
            var url = data + '?p=' + page;
            /* set up next page */
            var nextnum = +page + 1;
            var nextpage = nextnum.toString();
            $('div#loadmoreajaxloader').attr('page', nextpage);
            /* load data set */
            $.ajax({
                url: url,
                success: function(html){
                    if(html){
                        $("#postScroll").append(html);
                        $('div#loadmoreajaxloader').hide();
                    } else {
                        $("div#loadmoreajaxloader").html('<center><small>No more posts</small></center>');
                    }
                }
            });
        }
    });
});

$(document).ready(function() {
    $(".postCommentSubmit").click(function(){
        var targetid = $(this).attr('targetid');
        var formid = $(this).attr('formid');
        var formurl = $(this).attr('formurl');
        $.ajax({
            url: formurl,
            type: 'post',
            dataType: 'html',
            data: $(formid).serialize(),
            success: function(html){
                $(targetid).html(html);
            }
        });
    });
    $(".postCommentDelete").click(function(){
        var targetid = $(this).attr('targetid');
        var url = $(this).attr('data');
        $.ajax({
            url: url,
            dataType: 'html',
            success: function(html){
                if(html){
                    $(targetid).html(html);
                }
            }
        });
    });
    $(".commentListToggle").click(function(){
        var targetid = $(this).attr('targetid');
        var state = $(this).attr('state');
        if (state == 'on'){
            $(this).attr('state','off')
            $(targetid).hide()
            }else{
            $(this).attr('state','on')
            $(targetid).show()                
            }
    });
});