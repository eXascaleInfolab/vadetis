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
                },
                error: function (data, status, xhr) {
                    printMessages([{'message': "Request failed"}], "error-request");
                    handleMessages(data);
                    highchart.hideLoading();
                }
            });
        });
    }

    // private
    var init = function (anomaly_injection_form_id) {
        initInjection(anomaly_injection_form_id);
    }

    return {
        // public
        init: function(anomaly_injection_form_id) {
            init(anomaly_injection_form_id);
        }
    };
}();