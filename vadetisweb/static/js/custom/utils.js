
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function loadImage(html_id, url, post_data, callback) {
    // todo replace in other occurrences: get csrf from cookie
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: "POST",
        url: url,
        data: post_data,
        cache: false,
        success: function (response) {
            $("#" + html_id).html('<img src="data:image/png;base64,' + response + '" style="max-width: 100%;"/>');
            callback();
        }
    });
}

function registerThresholdUpdateForm(form_id) {
    var html_id = '#' + form_id;
    $(html_id).on('submit', function (event) {
        event.preventDefault();
        $(":submit").attr("disabled", true);
        clear_form_errors(form_id);
        clear_messages();

        var highchart = $('#highcharts_container').highcharts();
        var formData = new FormData(this);
        var dataset_series_json = getDatasetSeriesJson(highchart);
        formData.append('dataset_series_json', JSON.stringify(dataset_series_json));

        highchart.showLoading();
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
                // update series
                var series_data_json = data['series'];
                setSeriesData(highchart, series_data_json);
                highchart.hideLoading();
                var info = data['info'];

                // scores
                $('#scores_portlet').show();
                updateScores(info);

                // threshold
                updateThreshold(info.threshold);

                // cnf
                requestCnfMatrix("cnf_portlet", "cnf_matrix_img", info);

                // plot
                requestPlot("plot_portlet", "plot_img", info)

                $(":submit").attr("disabled", false);
            },
            error: function(data, status, xhr) {
                console.error("Sending asynchronous failed");
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
                    print_messages(data.responseJSON.messages);
                }
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('form_errors')) {
                    print_form_errors(data.responseJSON.form_errors);
                }
                highchart.hideLoading();

                $('#scores_portlet').hide();
                $('#cnf_portlet').hide();
                $('#plot_portlet').hide();

                $(":submit").attr("disabled", false);
            }
        });
    });
}

function registerAnomalyDetectionForm(form_id) {
    var html_id = '#' + form_id;
    $(html_id).on('submit', function (event) {
        event.preventDefault();
        $(":submit").attr("disabled", true);
        clear_form_errors(form_id);
        clear_messages();

        var highchart = $('#highcharts_container').highcharts();
        updateTimeRange(highchart, form_id);

        var formData = new FormData(this);
        var dataset_series_json = getDatasetSeriesJson(highchart);
        formData.append('dataset_series_json', JSON.stringify(dataset_series_json));

        highchart.showLoading();
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
                // update series
                var series_data_json = data['series'];
                setSeriesData(highchart, series_data_json);
                highchart.hideLoading();
                var info = data['info'];

                // scores
                $('#scores_portlet').show();
                updateScores(info);

                // threshold
                updateThreshold(info.threshold);

                // cnf
                requestCnfMatrix("cnf_portlet", "cnf_matrix_img", info);

                // plot
                requestPlot("plot_portlet", "plot_img", info)

                $(":submit").attr("disabled", false);
            },
            error: function(data, status, xhr) {
                console.error("Sending asynchronous failed");
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
                    print_messages(data.responseJSON.messages);
                }
                if(data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('form_errors')) {
                    print_form_errors(data.responseJSON.form_errors);
                }
                highchart.hideLoading();

                $('#scores_portlet').hide();
                $('#cnf_portlet').hide();
                $('#plot_portlet').hide();

                $(":submit").attr("disabled", false);
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
