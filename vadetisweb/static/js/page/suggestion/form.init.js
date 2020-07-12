"use strict";

var DatasetSuggestionForm = function () {

    var submitSingleSuggestion = function (url, action, method, enctype, algorithm, callbackData, callback) {
        var csrftoken = Cookies.get('csrftoken');
        var formData = new FormData();
        formData.append('algorithm', algorithm);
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url: action,
            data: formData,
            type: method,
            enctype: enctype,
            processData: false,
            contentType: false,
            success: function (data, status, xhr) {
                handleRedirect(data, xhr);
                handleMessages(data);
                callbackData(data);
                callback();
            },
            error: function (data, status, xhr) {
                printMessages([{'message': "Request failed: Could not request suggestions."}], "error-request");
                handleMessages(data);
                callback_fail();
            }
        });
    }

    var initSuggestion = function (form_id) {
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
            var url = form_selector.attr('action'), action = form_selector.attr('action'), method = form_selector.attr('method'),
                enctype = form_selector.attr('enctype');

            var settings = settingsFromCookie();
            var round_digits = settings.round_digits;

            // Iterate through values and send each as own request
            var entries = formData.entries();
            var numRequests = Array.from(formData.entries()).filter(array => array[0] === 'algorithm').length;
            var numResponses = 0;
            for (var pair of entries) {
                var key = pair[0];
                var algorithm = pair[1];
                if (key === 'algorithm') {
                    submitSingleSuggestion(url, action, method, enctype, algorithm, function (data) {
                            var suggestions = data.suggestions
                            suggestions.forEach(s => {
                                var info = s.info;
                                var responseAlgorithm = s.algorithm;
                                var series_data = [
                                    parseFloat((info.accuracy * 100).toFixed(round_digits)),
                                    parseFloat((info.f1_score * 100).toFixed(round_digits)),
                                    parseFloat((info.precision * 100).toFixed(round_digits)),
                                    parseFloat((info.recall * 100).toFixed(round_digits)),
                                ];
                                var existingSeries = getSeriesByName(highchart, responseAlgorithm);
                                if(existingSeries !== undefined) {
                                    existingSeries.setData(series_data, true, true);
                                } else {
                                    addColumnSeries(highchart, s.algorithm, series_data);
                                }
                            });
                        },
                        function () {
                            numResponses += 1;
                            if (numResponses === numRequests) {
                                highchart.hideLoading();
                                $(":submit").attr("disabled", false);
                            }
                        });
                }
            }
        });
    }

    // private
    var init = function (suggestion_form_id) {
        initSuggestion(suggestion_form_id);
    }

    return {
        // public
        init: function (suggestion_form_id) {
            init(suggestion_form_id);
        }
    };
}();