"use strict";

var DatasetSuggestionForm = function () {

    var loadImages = function (portlet_id, info) {
        requestCnfMatrix(portlet_id, portlet_id + "_cnf", info);
        requestPlot(portlet_id, portlet_id + "_plot", info.thresholds, info.detection_threshold_scores);
    }

    var requestRecommendationPortlet = function (portlet_url, portlet_id, callback) {
        var highchart = $('#highcharts_container').highcharts(), scores = getScoresFromColumnChart(highchart);
        if ($("#" + portlet_id).length === 0) {
            var data = {
                id: portlet_id,
                title: "Recommendation",
                scores: JSON.stringify(scores),
            }
            var csrftoken = Cookies.get('csrftoken');
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: portlet_url,
                data: data,
                dataType: "html",
                type: 'POST',
                enctype: "multipart/form-data",
                success: function (data, status, xhr) {
                    callback(data);
                },
                error: function (data, status, xhr) {
                    printMessages([{'message': "Request failed: Could not request rendered HTML."}], "error-request");
                    handleMessages(data);
                }
            });
        }
    }

    var requestSuggestionPortlet = function (portlet_url, portlet_id, title, conf, threshold, callback) {
        var data = {
            id: portlet_id,
            title: title,
            conf: JSON.stringify(conf),
            threshold: threshold,
            img_1_id: portlet_id + "_cnf",
            img_2_id: portlet_id + "_plot",
            content_class: "img-container",
        }
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url: portlet_url,
            data: data,
            dataType: "html",
            type: 'POST',
            enctype: "multipart/form-data",
            success: function (data, status, xhr) {
                var column = '<div class="col-lg-12 col-md-12 col-xs-12 col-sm-12">' + data + '</div>';
                $('#suggestion_portlets').prepend(column);
                callback();
            },
            error: function (data, status, xhr) {
                printMessages([{'message': "Request failed: Could not request rendered HTML."}], "error-request");
                handleMessages(data);
            }
        });
    }

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

    var initSuggestion = function (form_id, suggestion_portlet_url, recommendation_portlet_url) {
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
            if (numRequests === 0) {
                printMessages([{'message': "Form is invalid"}], "error");
                highchart.hideLoading();
                $(":submit").attr("disabled", false);
                return;
            }

            var numResponses = 0;
            var maximizeScore = 'F1-Score';
            for (var entry of formData.entries()) {
                var entryKey = entry[0];
                if (entryKey === 'maximize_score') {
                    maximizeScore = entry[1];
                    break;
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
                                var conf = s.conf;
                                var maximizedScore = conf.maximize_score;
                                var series_data = [
                                    parseFloat((info.accuracy * 100).toFixed(round_digits)),
                                    parseFloat((info.f1_score * 100).toFixed(round_digits)),
                                    parseFloat((info.precision * 100).toFixed(round_digits)),
                                    parseFloat((info.recall * 100).toFixed(round_digits)),
                                ];
                                var existingSeries = getSeriesByName(highchart, responseAlgorithm);
                                if (existingSeries !== undefined) {
                                    existingSeries.update({
                                        custom: {
                                            maximize_score: maximizedScore,
                                        }
                                    }, false);
                                    existingSeries.setData(series_data, true, true);
                                } else {
                                    addColumnSeries(highchart, responseAlgorithm, maximizedScore, series_data);
                                }

                                var portlet_id = makeHtmlId(responseAlgorithm);
                                if ($('#' + portlet_id).length > 0) {
                                    $('#' + portlet_id).remove();
                                }
                                requestSuggestionPortlet(suggestion_portlet_url, portlet_id, responseAlgorithm, conf, info.threshold,
                                    function () {
                                        KTApp.initPortlets();
                                        KTApp.initTooltips();
                                        loadImages(portlet_id, info);
                                    });
                            });
                        },
                        function () {
                            numResponses += 1;
                            if (numResponses === numRequests) {
                                highchart.hideLoading();
                                $(":submit").attr("disabled", false);
                                requestRecommendationPortlet(recommendation_portlet_url, "recommendation_portlet", function (data) {
                                    $('#recommendation_portlet').remove();
                                    $('#form_portlets').append(data);
                                    KTApp.initPortlet();
                                    KTApp.initTooltips();
                                });
                            }
                        });
                }
            }
        });
    }

    // private
    var init = function (suggestion_form_id, suggestion_portlet_url, recommendation_portlet_url) {
        initSuggestion(suggestion_form_id, suggestion_portlet_url, recommendation_portlet_url);
    }

    return {
        // public
        init: function (suggestion_form_id, suggestion_portlet_url, recommendation_portlet_url) {
            init(suggestion_form_id, suggestion_portlet_url, recommendation_portlet_url);
        }
    };
}();