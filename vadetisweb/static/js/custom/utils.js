function loadImage(html_id, url, post_data) {
    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        cache: false,

        success: function (response) {
            $("#" + html_id).html('<img src="data:image/png;base64,' + response + '" />');
            var html_portlet = $("#" + html_id + "_portlet");
            if (!(html_portlet.is(":visible"))) {
                html_portlet.show();
            }
        }
    });
}

function clear_messages() {
    $('#message-container').empty();
}

function groupBy(list, keyGetter) {
    const map = new Map();
    list.forEach((item) => {
        const key = keyGetter(item);
        const collection = map.get(key);
        if (!collection) {
            map.set(key, [item]);
        } else {
            collection.push(item);
        }
    });
    return map;
}

function print_messages(messages) {
    grouped_messages = groupBy(messages, message => message.level_tag);
    console.log(grouped_messages);
    grouped_messages.forEach((value, key) => {
        $('#message-container').append(html_messages(key, value));
    });
}

function html_messages_list(messages) {
    html += "<ul class=\"messages_list\">";
    messages.forEach(error => {
        html += "<li class=\"messages_item\">";
        html += error.message;
        html += "</li>";
    });
    html += "</ul>";
    return html;
}

function html_messages(tag, messages) {
    html = "<div class=\"messages messages-" + tag + "\">";
    if (messages.length > 1) {
        html += html_messages_list(messages);
    } else if (messages.length === 1) {
        html += messages[0].message;
    }
    html += "</div>";
    return html;
}
