function addSubscription() {
    var url = $('#urlSubscription').val();
    if (url == '') {
        return false;
    }
    $("ul#menu").append("<li id=\"loadSubscription\">Loading...</li>");
    var i = $("ul#menu li#loadSubscription");
    $.post('/api/add', {url: url}, function(data) {
        if (data.success == true) {
            i.html("<li><a onClick=\"viewSubscription(&quot;" + data.id + "&quot;)\" href=\"#" + data.id + "\">" + data.title + "</a></li>");
        }
    });
    $('#add').popover('hide')
}

function viewSubscription(feedId) {
    $.getJSON('/api/get/' + feedId, function(data) {
        $('#content').html('<div class="accordion" id="accordion2">');
        $.each(data.content, function(i,item){
            var header =  '<i class="icon-calendar"></i> ' + item.published + ' | <a href="' + item.link + '" target="_blank"><i class="icon-share-alt"></i></a>';
            var content = '<div class="accordion-group">                                                                                            \
    <div class="accordion-heading">                                                                                                                 \
        <a class="accordion-toggle" data-toggle="collapse" onClick="readEntry(&quot;' + item._id + '&quot;,&quot;' + feedId + '&quot;)" data-parent="#accordion2" href="#' + feedId + '_' + item._id + '">' + item.title + '</a>  \
    </div>                                                                                                                                          \
    <div id="' + feedId + '_' + item._id + '" class="accordion-body collapse">                                                                      \
        <div class="accordion-inner">' + header + "<hr>" + item.description + '</div>                                                               \
    </div>                                                                                                                                          \
</div>';
            $("#content").append(content);
            if (item.read == false) {
                $('#content a[href=#' + feedId + '_' + item._id + ']').css('font-weight', 'bold');
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

function readEntry(entryId, feedId) {
    $.get('/api/read/' + entryId, function(data) {});
    $('a[href=#' + feedId + '_' + entryId + ']').css('font-weight', 'normal');
}

$(document).ready(function(){
    var add_content = '<form><fieldset><center>                                      \
    <input id="urlSubscription" type="text" class="input-medium" placeholder="Url…"> \
    <button type="submit" class="btn" onClick="addSubscription()">Submit</button>    \
    </center></fieldset></form>';
    $('#add').popover({title:"<center>New subscription</center>",html:true,content:add_content,placement:"bottom"});
});
