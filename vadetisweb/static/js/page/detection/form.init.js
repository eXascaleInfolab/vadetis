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

    var registerAnomalyDetectionForm = function(form_id) {
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
                    requestCnfMatrix("cnf_portlet", "cnf_matrix_img", info);

                    // plot
                    requestPlot("plot_portlet", "plot_img", info)

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

    var initOnChangeDetection = function(select_on_change_id) {

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
                        registerAnomalyDetectionForm(receivedFormId);
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
    var init = function (anomaly_injection_form_id, select_on_change_id) {
        initInjection(anomaly_injection_form_id);
        initOnChangeDetection(select_on_change_id);
    }

    return {
        // public
        init: function(anomaly_injection_form_id, select_on_change_id) {
            init(anomaly_injection_form_id, select_on_change_id);
        }
    };
}();