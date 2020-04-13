function loadImage(html_id, url, post_data) {
    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        cache: false,

        success: function (response) {
            $("#" + html_id).html('<img src="data:image/png;base64,' + response + '" style="max-width: 100%;"/>');
            var html_portlet = $("#" + html_id + "_portlet");
            if (!(html_portlet.is(":visible"))) {
                html_portlet.show();
            }
        }
    });
}

function registerAnomalyDetectionForm(form_id) {
    var html_id = '#' + form_id;
    $(html_id).on('submit', function (event) {
        event.preventDefault();
        clear_form_errors(form_id);
        clear_messages();

        var highchart = $('#highcharts_container').highcharts();
        updateTimeRange(highchart, form_id);

        var formData = new FormData(this);
        var dataset_series_json = getDatasetSeriesJson(highchart);
        formData.append('dataset_series_json', JSON.stringify(dataset_series_json));

        $.post({
            url: $(this).attr('action'),
            data: formData,
            type: $(this).attr('method'),
            enctype: $(this).attr('enctype'),
            processData: false,
            contentType: false,
            success: function(data, status, xhr) {
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
                    print_messages(data.responseJSON.messages);
                }
            },
            error: function(data, status, xhr) {
                console.error("Sending asynchronous failed");
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
                    print_messages(data.responseJSON.messages);
                }
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('form_errors')) {
                    print_form_errors(data.responseJSON.form_errors);
                }
            }
        });
    });
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function clear_messages() {
    $('#message-container').empty();
}

function clear_form_errors(formid) {
    form = $("#" + formid);
    form.find(".validated").removeClass("validated");
    form.find(".invalid-feedback").remove();
}

function containsObject(obj, list) {
    return list.some(elem => elem === obj)
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
    grouped_messages.forEach((value, tag) => {
        message_container = $('#message-container');
        html = "<div class=\"messages messages-" + tag + "\">";
        html += html_messages(value);
        html += "</div>";
        message_container.append(html);
    });
}

function html_messages_list(messages) {
    html = "<ul class=\"messages_list\">";
    messages.forEach(error => {
        html += "<li class=\"messages_item\">";
        html += error.message;
        html += "</li>";
    });
    html += "</ul>";
    return html;
}

function html_messages(messages) {
    if (messages.length > 1) {
        return html_messages_list(messages);
    } else if (messages.length === 1) {
        return messages[0].message;
    }
    return "";
}

function print_form_errors(form_errors) {
    for (const [key, val] of Object.entries(form_errors)) {
        input_element = $("[name=" + key + "]");
        html = "<div class=\"invalid-feedback\">" + val[0] + "</div>";
        input_element.parent().addClass("validated");
        input_element.after(html);
    }
}
