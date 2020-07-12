"use strict";

var DatasetSuggestionForm = function () {

    var submitSingleSuggestion = function (url, action, method, enctype, algorithm, maximizeScore, callbackData, callback) {
        var csrftoken = Cookies.get('csrftoken');
        var formData = new FormData();
        formData.append('algorithm', algorithm);
        formData.append('maximize_score', maximizeScore);
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
                callback();
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
            var numRequests = Array.from(formData.entries()).filter(array => array[0] === 'algorithm').length;
            var numResponses = 0;
            var maximizeScore = 'F1-Score';
            for (var entry of formData.entries()) {
                var entryKey = entry[0];
                if (entryKey === 'maximize_score') {
                    maximizeScore = entry[1];
                }
            }
            for (var pair of formData.entries()) {
                var key = pair[0];
                var algorithm = pair[1];
                if (key === 'algorithm') {
                    submitSingleSuggestion(url, action, method, enctype, algorithm, maximizeScore, function (data) {
                            var suggestions = data.suggestions
                            suggestions.forEach(s => {
                                var info = s.info;
                                var responseAlgorithm = s.algorithm;
                                var maximizedScore = s.maximize_score;
                                var series_data = [
                                    parseFloat((info.accuracy * 100).toFixed(round_digits)),
                                    parseFloat((info.f1_score * 100).toFixed(round_digits)),
                                    parseFloat((info.precision * 100).toFixed(round_digits)),
                                    parseFloat((info.recall * 100).toFixed(round_digits)),
                                ];
                                var existingSeries = getSeriesByName(highchart, responseAlgorithm);
                                if(existingSeries !== undefined) {
                                    existingSeries.update({
                                        custom: {
                                            maximize_score: maximizedScore,
                                        }
                                    }, false);
                                    existingSeries.setData(series_data, true, true);
                                } else {
                                    addColumnSeries(highchart, responseAlgorithm, maximizedScore, series_data);
                                }
                            });
                        },
                        function () {
                            numResponses += 1;
                            if (numResponses === numRequests) {
                                highchart.hideLoading();
                                $(":submit").attr("disabled", false);
                            }
                            // todo add legend
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