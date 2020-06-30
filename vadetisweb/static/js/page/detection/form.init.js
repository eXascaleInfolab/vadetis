var DatasetForm = function () {

    // private
    var init = function (anomaly_injection_form_id, format) {

        $('#'+anomaly_injection_form_id).on('submit', function (event) {
            event.preventDefault();
            inject_replace_series(anomaly_injection_form_id, new FormData(event.target), format);
        });
    }
    return {
        // public
        init: function(anomaly_injection_form_id, format) {
            init(anomaly_injection_form_id, format);
        }
    };
}();