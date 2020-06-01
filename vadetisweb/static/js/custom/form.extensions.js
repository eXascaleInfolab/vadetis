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


function ionSliderDoubleRangeToJson(input_id){
    $("#" + input_id)
}