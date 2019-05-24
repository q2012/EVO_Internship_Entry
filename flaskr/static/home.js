$( document ).ready(function() {
    document.getElementById("exprires")?document.getElementById("expires").min = (new Date()).toISOString():1==1;
    $("a").each(function() { $(this).text($(this).attr("href").split("__")[3]) });

    $("#upload_form").ajaxForm({
        url: 'upload',
        type: 'post',
        complete: function(response){
            console.log(response);
            if(!response.responseJSON.error)
                ($("#link-container").append('<a href="/' + response.responseJSON.fileurl + '">' + response.responseJSON.filename + '</a>').append('<br>'))
        }
    });

    //
});
