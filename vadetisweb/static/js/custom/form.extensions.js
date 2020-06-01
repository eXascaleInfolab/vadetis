"use strict";


var IonRangeSliderInitializer = function () {
    var init = function (input_id) {
        $("#" + input_id).ionRangeSlider();
    };
    return {
        init: function (input_id) {
            init(input_id);
        }
    };
}();


function ionSliderRangeValue(input_id){
    var split = $("#" + input_id).val().split(";");
    return {'lower' : parseInt(split[0]),
            'upper' : parseInt(split[1])};
}