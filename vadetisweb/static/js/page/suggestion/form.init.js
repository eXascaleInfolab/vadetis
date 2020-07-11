"use strict";

var DatasetSuggestionForm = function () {

    var initSuggestion = function(form_id) {

        var html_id = '#' + form_id;
        $(html_id).on('submit', function (event) {
            event.preventDefault();
            $(":submit").attr("disabled", true);
            clearFormErrors(form_id);
            clearMessages();
            var highchart = $('#highcharts_container').highcharts();
            var form_selector = $(html_id), csrftoken = Cookies.get('csrftoken');
            var formData = new FormData(this);
            highchart.showLoading();

            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: form_selector.attr('action'),
                data: formData,
                type: form_selector.attr('method'),
                enctype: form_selector.attr('enctype'),
                processData: false,
                contentType: false,
                success: function (data, status, xhr) {
                    handleRedirect(data, xhr);
                    handleMessages(data);
                    highchart.hideLoading();

                    $(":submit").attr("disabled", false);
                },
                error: function (data, status, xhr) {
                    printMessages([{'message': "Request failed: Could not request suggestions."}], "error-request");
                    handleMessages(data);
                    highchart.hideLoading();
                    $(":submit").attr("disabled", false);
                }
            });
        });
    }

    // private
    var init = function (suggestion_url) {

    }

    return {
        // public
        init: function(suggestion_url) {
            init(suggestion_url);
        }
    };
}();