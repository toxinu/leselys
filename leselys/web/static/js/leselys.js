function addSubscription() {
    var url = $('#urlSubscription').val();
    if (url == '') {
        return false;
    }
    $("ul#menu").append("<li id=\"loadSubscription\">Loading...</li>");
    var i = $("ul#menu li#loadSubscription");
    $.post('/api/add', {url: url}, function(data) {
        if (data.success == true) {
            i.html('<li><a onClick="viewSubscription(&quot;' + data.id + '&quot;)" href="#' + data.id + '">' + data.title + '</a></li>');
        }
    });
    $('#add').popover('hide')
}

function viewSubscription(feedId) {
    $.getJSON('/api/get/' + feedId, function(data) {
        $('#content').html('<div class="accordion" id="accordion2">');
        $.each(data.content, function(i,item){
            var content = '<div class="accordion-group">                                                                                            \
    <div class="accordion-heading">                                                                                                                 \
        <a class="accordion-toggle" data-toggle="collapse" onClick="readEntry(&quot;' + item._id + '&quot)" data-parent="#accordion2" href="#' + item._id + '">' + item.title + '</a>  \
    </div>                                                                                                                                          \
    <div id="' + item._id + '" class="accordion-body collapse">                                                                                     \
        <div class="accordion-inner" id="' + item._id + '"></div>                                                                                   \
    </div>                                                                                                                                          \
</div>';
            $("#content").append(content);
            if (item.read == false) {
                $('#content a[href=#' + item._id + ']').css('font-weight', 'bold');
            }
        });
        $('#content').append('</div>');
        $('#menu a').each(function(index) {
            $(this).css('font-weight', 'normal');
        });
        $('#menu a[href=#' + feedId + ']').css('font-weight', 'bold');
    });

}

function refreshSubscriptions() {
    $.get('/api/refresh'), function(data) {

    }

}

function readEntry(entryId) {
    if ($('a[href=#' + entryId + ']').data('loaded') == true) {
        return true;
    }
    $.getJSON('/api/read/' + entryId, function(data) {
        var header =  '<i class="icon-calendar"></i> ' + data.content.published + ' | <a href="' + data.content.link + '" target="_blank"><i class="icon-share-alt"></i></a>';
        var content = "<div class=\"accordion-inner\"" + header + "<hr>" + data.content.description + "</div>";
        $('#content #' + entryId).html(content);

    });

    $('a[href=#' + entryId + ']').css('font-weight', 'normal').data('loaded', true);
}

$(document).ready(function(){
    var add_content = '<form><fieldset><center>                                      \
    <input id="urlSubscription" type="text" class="input-medium" placeholder="Url…"> \
    <button type="submit" class="btn" onClick="addSubscription()">Submit</button>    \
    </center></fieldset></form>';
    $('#add').popover({title:"<center>New subscription</center>",html:true,content:add_content,placement:"bottom"});
});
