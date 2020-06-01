"use strict";

var IonRangeDoubleSlider = function () {
    var init = function (input_id, min, max, from, to) {
        $("#" + input_id).ionRangeSlider({
            type: "double",
            grid: true,
            min: min,
            max: max,
            from: from,
            to: to
        });
    };
    return {
        init: function (input_id, min, max, from, to) {
            init(input_id, min, max, from, to);
        }
    };
}();


var IonRangeSingleSlider = function () {
    var init = function (input_id, min, max, from) {
        $("#" + input_id).ionRangeSlider({
            type: "single",
            grid: true,
            min: min,
            max: max,
            from: from,
            step: 0.1
        });
    };
    return {
        init: function (input_id, min, max, from) {
            init(input_id, min, max, from);
        }
    };
}();