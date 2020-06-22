
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function insertImg(html_id, imgBlob){
    // use URL context to display image
    var url = window.URL || window.webkitURL;
    $("#" + html_id).html($("<img/>",{src:url.createObjectURL(imgBlob)}));
}

function loadImage(html_id, url, post_data, callback) {
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        type: "POST",
        url: url,
        dataType: 'binary',
        data: post_data,
        success: function (response) {
            insertImg(html_id, response);
            callback();
        },
        error: function(data, status, xhr) {
            printMessages([{'message': "Request failed"}], "error-request");
            callback();
        }
    });
}

function initAjaxFormSubmit(form_id, format) {
    $('#' + form_id).on('submit', function (event) {
        event.preventDefault();
        clearFormErrors(form_id);
        clearMessages();
        var csrftoken = Cookies.get('csrftoken'), url = $(this).attr('action');
        if(format) {
            url += '?format=' + format
        }
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url: url,
            data: new FormData(this),
            type: $(this).attr('method'),
            enctype: $(this).attr('enctype'),
            processData: false,
            contentType: false,
            success: function(data, status, xhr) {
                handleRedirect(data, xhr);
                handleMessages(data);
            },
            error: function(data, status, xhr) {
                handleMessages(data);
            }
        });
    });
}

/**
 * Handles messages contained in an ajax response if available
 * @param data - The data returned from the server
 */
function handleMessages(data) {
    if(data !== undefined) {
        if (data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('messages')) {
            printGroupedMessages(data.responseJSON.messages);
        } else if (data.hasOwnProperty('messages')) {
            printGroupedMessages(data.messages);
        }

        if (data.responseJSON !== undefined && data.responseJSON.hasOwnProperty('form_errors')) {
            printFormErrors(data.responseJSON.form_errors);
        } else if (data.hasOwnProperty('form_errors')) {
            printFormErrors(data.form_errors);
        }
    }
}

/**
 * Handles a window location redirect from response header of an ajax response if available
 * @param xhr - The jqXHR object, which is a superset of the XMLHTTPRequest object
 */
function handleRedirect(data, xhr) {
    if(data !==undefined && data.location) {
         window.location = data.location;
    }
    if (xhr.getResponseHeader('Location')) {
        window.location = xhr.getResponseHeader('Location');
    }
}


function saveData (blob, fileName) {
    let a = document.createElement("a");
    const url = window.URL.createObjectURL(blob);
    a.style = "display: none";
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function clearMessages() {
    $('#message-container').empty();
}

function clearFormErrors(formid) {
    var form = $("#" + formid);
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

function printGroupedMessages(messages) {
    var grouped_messages = groupBy(messages, message => message.level_tag);
    grouped_messages.forEach((value, tag) => printMessages(value, tag));
}

function printMessages(value, tag) {
    var message_container = $('#message-container');
    html = "<div class=\"messages messages-" + tag + "\">";
    html += "<div class=\"message-inner\">";
    html += htmlMessages(value);
    html += "</div>";
    html += "<div class=\"message-button\">";
    html += "<button id=\"messages-" + tag + "-close\" class=\"close btn-msg-close\"><i class=\"mdi mdi-18px mdi-close\"></i></button>";
    html += "</div>";
    html += "</div>";
    message_container.append(html);
    $("#messages-" + tag + "-close").click(function() {
        $(this).parent().parent().fadeOut(800);
    });
}

function htmlMessagesList(messages) {
    var html = "<ul class=\"messages_list\">";
    messages.forEach(msg => {
        html += "<li class=\"messages_item\">";
        html += msg.message;
        html += "</li>";
    });
    html += "</ul>";
    return html;
}

function htmlMessages(messages) {
    if (messages.length > 1) {
        return htmlMessagesList(messages);
    } else if (messages.length === 1) {
        return messages[0].message;
    }
    return "";
}

function printFormErrors(form_errors) {
    for (const [key, val] of Object.entries(form_errors)) {
        input_element = $("[name=" + key + "]");
        html = "<div class=\"invalid-feedback\">" + val[0] + "</div>";
        input_element.parent().addClass("validated");
        input_element.after(html);
    }
}

/**
 * Get settings from Cookie, or set them with default value
 */
function settingsFromCookie() {
    var settings = {};
    _setSettingOrDefault(settings, 'highcharts_height', 750);
    _setSettingOrDefault(settings, 'legend_height', 100);
    _setSettingOrDefault(settings, 'color_outliers', '#FF0000');
    _setSettingOrDefault(settings, 'color_clusters', '#0000FF');
    _setSettingOrDefault(settings, 'color_true_positive', '#008800');
    _setSettingOrDefault(settings, 'color_false_positive', '#FF0000');
    _setSettingOrDefault(settings, 'color_false_negative', '#0000FF');
    _setSettingOrDefault(settings, 'round_digits', 3);
    return settings;
}

function _setSettingOrDefault(setting, cookieName, defaultValue) {
    var cookieValue = Cookies.get(cookieName);
    if(cookieValue === undefined) {
        Cookies.set(cookieName, defaultValue, { sameSite: 'lax' });
        setting[cookieName] = defaultValue
    } else {
        setting[cookieName] = cookieValue;
    }
}

function getSetting(cookieName) {
    return Cookies.get(cookieName);
}
