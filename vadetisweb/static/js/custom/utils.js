
function loadImage(html_id, url, post_data){
    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        cache: false,

        success: function(response){
            $("#" + html_id).html('<img src="data:image/png;base64,' + response + '" />');
            var html_portlet = $("#" + html_id + "_portlet");
            if(!(html_portlet.is(":visible"))){
                html_portlet.show();
            }
        }
    });
}