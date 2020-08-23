var RoundSliders = function () {
    return {
        init: function (round_digits) {
            //roundslider does not support ie8 so skip it
            if (!jQuery().roundSlider()) {
                return;
            }

            step_size = 1 / Math.pow(10, round_digits);

            // init
            $(".roundslider.normal").roundSlider({
                sliderType: "min-range",
                radius: 50,
                width: 6,
                value: null,
                step: step_size.toFixed(round_digits),
                handleSize: 0,
                handleShape: "square",
                circleShape: "pie",
                startAngle: 315,
                min: 0,
                max: 1,
                animation: true,
                showTooltip: true,
                editableTooltip: false,
                readOnly: true,
                disabled: true,
                keyboardAction: false,
                mouseScrollAction: false,
                create : function (e) {
                    var roundslider = $("#"+e.id);
                    var title = roundslider.attr("title");
                    roundslider.append('<div class="rs-title" style="position:absolute; bottom:0; width: 100%; text-align:center;"><strong>'+title+'</strong></div>');
                },
                change : function (e) {
                    var value = e.value;
                    if(value <= 0.65){
                        this.control.find(".rs-range-color").css("background", "#FF0000");
                        this.control.find(".rs-border").css("border-color", "#FF0000");

                    } else if(value > 0.65 && value < 0.85 ) {
                        this.control.find(".rs-range-color").css("background", "#D7D700");
                        this.control.find(".rs-border").css("border-color", "#D7D700");

                    } else {
                        this.control.find(".rs-range-color").css("background", "#008000");
                        this.control.find(".rs-border").css("border-color", "#008000");
                    }
                }
            });

            // init
            $(".roundslider.inverse").roundSlider({
                sliderType: "min-range",
                radius: 50,
                width: 6,
                value: null,
                step: step_size.toFixed(round_digits),
                handleSize: 0,
                handleShape: "square",
                circleShape: "pie",
                startAngle: 315,
                min: 0,
                max: 1,
                animation: true,
                showTooltip: true,
                editableTooltip: false,
                readOnly: true,
                disabled: true,
                keyboardAction: false,
                mouseScrollAction: false,
                create : function (e) {
                    var roundslider = $("#"+e.id);
                    var title = roundslider.attr("title");
                    roundslider.append('<div class="rs-title" style="position:absolute; bottom:0; width: 100%; text-align:center;"><strong>'+title+'</strong></div>');
                },
                change : function (e) {
                    var value = e.value;

                    if(value <= 0.15) {
                        this.control.find(".rs-range-color").css("background", "#008000");
                        this.control.find(".rs-border").css("border-color", "#008000");

                    } else if (value > 0.15 && value < 0.35) {
                        this.control.find(".rs-range-color").css("background", "#D7D700");
                        this.control.find(".rs-border").css("border-color", "#D7D700");

                    } else {
                        this.control.find(".rs-range-color").css("background", "#FF0000");
                        this.control.find(".rs-border").css("border-color", "#FF0000");
                    }
                }
            });

            //trigger change event programmatically on setValue

            var _fn1 = $.fn.roundSlider.prototype._setValue;
            $.fn.roundSlider.prototype._setValue = function (e) {
              _fn1.apply(this, arguments);
              this._raiseEvent("change");
            }
        },

        updateValue: function (id, value) {
            $(id).data("roundSlider").setValue(value);
        }
    };
}();
