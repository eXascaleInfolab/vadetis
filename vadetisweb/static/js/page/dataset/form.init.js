var DatasetForm = function () {

    // private
    var init = function (anomaly_injection_form_id, format) {

        $('#'+anomaly_injection_form_id).on('submit', function (event) {
            event.preventDefault();
            inject_replace(anomaly_injection_form_id, new FormData(event.target), format);
        });

        IonRangeSliderInitializer.init("normal_range");
        IonRangeSliderInitializer.init("anomaly_range");
        IonRangeSliderInitializer.init("probability");
    }
    return {
        // public
        init: function(anomaly_injection_form_id, format) {
            init(anomaly_injection_form_id, format);
        }
    };
}();