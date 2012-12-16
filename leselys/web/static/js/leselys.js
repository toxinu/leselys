function addSubscription() {
    var url = $('#urlSubscription').val();
    $("ul#menu").append("<li id=\"loadSubscription\">Loading...</li>");
    var i = $("ul#menu li#loadSubscription");
    $.post('/api/add', {url: url}, function(data) {
        if (data.success == true) {
            i.html("<li><a onClick=\"viewSubscription(&quot;" + data.name + "&quot;)\" href=\"#\">" + data.name + "</a></li>");
        }
    });
    $('#add').popover('hide')
}

function viewSubscription(name) {
    $.getJSON('/api/get/' + name, function(data) {
        $('#content').html('<div class="accordion" id="accordion2"></div>');
        $.each(data.content, function(i,item){
            var header =  '<i class="icon-calendar"></i> ' + item.published + ' | <a href="' + item.link + '" target="_blank"><i class="icon-share-alt"></i></a>';
            var content = '<div class="accordion-group">                                                                                    \
    <div class="accordion-heading">                                                                                                         \
        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapse' + i + '">' + item.title + '</a>       \
    </div>                                                                                                                                  \
    <div id="collapse' + i + '" class="accordion-body collapse">                                                                            \
        <div class="accordion-inner">' + header + "<hr>" + item.description + '</div>                                                       \
    </div>                                                                                                                                  \
</div>';
            $("#content").append(content);
        });
    });
}

$(document).ready(function(){
    var add_content = '<form><fieldset><center>                                      \
    <input id="urlSubscription" type="text" class="input-medium" placeholder="Url…"> \
    <button type="submit" class="btn" onClick="addSubscription()">Submit</button>    \
    </center></fieldset></form>';
    $('#add').popover({title:"New subscription",html:true,content:add_content,placement:"bottom"});

    $('#menu').scrollspy();
});