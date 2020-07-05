var DatasetDetectionForm = function () {

    var initInjection = function(form_id) {

        var html_id = '#' + form_id;
        $(html_id).on('submit', function (event) {
            event.preventDefault();
            $(":submit").attr("disabled", true);
            clearFormErrors(form_id);
            clearMessages();
            var highchart = $('#highcharts_container').highcharts();
            var form_selector = $(html_id), csrftoken = Cookies.get('csrftoken'), dataset_series_json = getDatasetSeriesJson(highchart);

            updateTimeRange(highchart, form_id, "rangeStartInjection", "rangeEndInjection");
            var formData = new FormData(this);
            formData.append('dataset_series_json', JSON.stringify(dataset_series_json));
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
                    var series_data_json = data['series'];
                    setSeriesData(highchart, series_data_json);
                    $(":submit").attr("disabled", false);
                },
                error: function (data, status, xhr) {
                    printMessages([{'message': "Request failed"}], "error-request");
                    handleMessages(data);
                    highchart.hideLoading();
                    $(":submit").attr("disabled", false);
                }
            });
        });
    }

    var registerThresholdUpdateForm = function(form_id) {
        var html_id = '#' + form_id;
        $(html_id).on('submit', function (event) {
            event.preventDefault();
            $(":submit").attr("disabled", true);
            clearFormErrors(form_id);
            clearMessages();
            var highchart = $('#highcharts_container').highcharts(), formData = new FormData(this), dataset_series_json = getDatasetSeriesJson(highchart), csrftoken = Cookies.get('csrftoken');
            formData.append('dataset_series_json', JSON.stringify(dataset_series_json));
            highchart.showLoading();

            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: $(this).attr('action'),
                data: formData,
                type: $(this).attr('method'),
                enctype: $(this).attr('enctype'),
                processData: false,
                contentType: false,
                success: function(data, status, xhr) {
                    handleMessages(data);

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
                    printMessages([{'message': "Request failed"}], "error-request");
                    handleMessages(data);

                    highchart.hideLoading();

                    $('#scores_portlet').hide();
                    $('#cnf_portlet').hide();
                    $('#plot_portlet').hide();

                    $(":submit").attr("disabled", false);
                }
            });
        });
    }

    var requestPortlet = function (portlet_url, portlet_id, title, content_id, content_class, prepend, callback) {
        var data = {
            id: portlet_id,
            title: title,
            content_id: content_id,
            content_class: content_class
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
            success: function(data, status, xhr) {
                var column = '<div class="col-lg-6 col-md-12 col-sm-12 col-xs-12">' + data + '</div>';
                if(prepend) {
                    $('#detection_portlets').prepend(column);
                } else {
                    $('#detection_portlets').append(column);
                }
                callback();
            },
            error: function (data, status, xhr) {
                printMessages([{'message': "Request failed"}], "error-request");
                handleMessages(data);
            }
        });
    }

    var registerAnomalyDetectionForm = function(form_id, portlet_url) {
        var html_id = '#' + form_id;
        $(html_id).on('submit', function (event) {
            event.preventDefault();
            $(":submit").attr("disabled", true);
            clearFormErrors(form_id);
            clearMessages();

            var highchart = $('#highcharts_container').highcharts();
            updateTimeRangeBySelection(highchart, form_id, "rangeStart", "rangeEnd");

            var formData = new FormData(this), dataset_series_json = getDatasetSeriesJson(highchart), csrftoken = Cookies.get('csrftoken');
            formData.append('dataset_series_json', JSON.stringify(dataset_series_json));
            highchart.showLoading();
            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: $(this).attr('action'),
                data: formData,
                type: $(this).attr('method'),
                enctype: $(this).attr('enctype'),
                processData: false,
                contentType: false,
                success: function(data, status, xhr) {
                    handleMessages(data);

                    // update series
                    var series_data_json = data['series'];
                    setSeriesData(highchart, series_data_json);
                    highchart.hideLoading();
                    var info = data['info'];

                    // scores
                    $('#scores_portlet').show();
                    updateScores(info);

                    // threshold
                    $('#threshold_portlet').show();
                    registerThresholdUpdateForm('threshold_form');
                    updateThreshold(info.threshold);

                    // cnf
                    requestPortlet(portlet_url, "cnf_portlet", "Confusion Matrix", "cnf_matrix_img", "img-container", true,
                        function() {
                        requestCnfMatrix("cnf_portlet", "cnf_matrix_img", info);
                    });

                    // plot
                    requestPortlet(portlet_url, "plot_portlet", "Threshold / Score Plot", "plot_img", "img-container", false,
                        function () {
                        requestPlot("plot_portlet", "plot_img", info)
                    });
                    $(":submit").attr("disabled", false);
                },
                error: function(data, status, xhr) {
                    printMessages([{'message': "Request failed"}], "error-request");
                    handleMessages(data);

                    highchart.hideLoading();

                    $('#threshold_portlet').hide();
                    $('#scores_portlet').hide();

                    $('#cnf_portlet').hide();
                    $('#plot_portlet').hide();

                    $(":submit").attr("disabled", false);
                }
            });
        });
    }

    var initOnChangeDetection = function(select_on_change_id, portlet_url) {

        var onChangeSubmit = function(formData, form_id, form_append_container_id) {
            clearFormErrors(form_id);
            clearMessages();
            var form_selector = $("#" + form_id), form_append_container_selector = $("#" + form_append_container_id), csrftoken = Cookies.get('csrftoken');

            $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: form_selector.attr('action'),
                data: new FormData(formData),
                type: form_selector.attr('method'),
                enctype: form_selector.attr('enctype'),
                processData: false,
                contentType: false,
                success: function (data, status, xhr) {
                    handleMessages(data);

                    if (data !== undefined) {
                        var receivedForm = $(data);
                        var receivedFormId = $(receivedForm).filter('form').attr('id');

                        form_append_container_selector.empty();
                        form_append_container_selector.append(receivedForm);
                        $('#' + form_append_container_id + ' [data-toggle="kt-popover"]').each(function () {
                            KTApp.initPopover($(this));
                        });
                        $('#' + form_append_container_id + ' [data-type="single"]').each(function () {
                            IonRangeSliderInitializer.init(this.id);
                        });
                        $('#' + form_append_container_id + ' [data-type="double"]').each(function () {
                            IonRangeSliderInitializer.init(this.id);
                        });
                        registerAnomalyDetectionForm(receivedFormId, portlet_url);
                    } else {
                        form_append_container_selector.empty();
                    }
                },
                error: function (data, status, xhr) {
                    printMessages([{'message': "Request failed"}], "error-request");
                    handleMessages(data);
                    form_append_container_selector.empty();
                }
            });
        }
        $("#" + select_on_change_id).on("change", function () {
            onChangeSubmit(this.form, 'anomaly_algorithm_form', 'form_append_container')
        });
    }

    // private
    var init = function (anomaly_injection_form_id, select_on_change_id, portlet_url) {
        initInjection(anomaly_injection_form_id);
        initOnChangeDetection(select_on_change_id, portlet_url);
    }

    return {
        // public
        init: function(anomaly_injection_form_id, select_on_change_id, portlet_url) {
            init(anomaly_injection_form_id, select_on_change_id, portlet_url);
        }
    };
}();