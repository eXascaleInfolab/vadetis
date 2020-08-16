"use strict";

var DatasetDisplayMap = function () {

    // private
    var init = function (url, map_html_id) {
        $('#'+map_html_id).empty();
        var initMap = function(data) {
            var center_latitude = data.meta.center_latitude, center_longitude = data.meta.center_longitude;
            var timeSeriesLocationsMap = L.map(map_html_id).setView([center_latitude, center_longitude], 8);
            L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox/streets-v11',
                tileSize: 512,
                zoomOffset: -1,
                accessToken: 'pk.eyJ1IjoidmFkZXRpcyIsImEiOiJja2NiMTB4NW8yMHI2MnRvMHk2aDl6ZG5kIn0.5CarskUSNdP8fWdvSx7Omw'
            }).addTo(timeSeriesLocationsMap);

            var markerGroup = new L.featureGroup();
            data.points.forEach(function(point) {
                var marker = L.marker([point.latitude, point.longitude])
                    .bindPopup(point.ts + " (" + point.label +")")
                    .addTo(timeSeriesLocationsMap);
                markerGroup.addLayer(marker);
            });
            timeSeriesLocationsMap.fitBounds(markerGroup.getBounds());
        }

        $.ajax({
            url: url,
            dataType: 'json',
            success: function (data, status, xhr) {
                initMap(data);
            },
            error: function (data, status, xhr) {
                printMessages([{'message': "Could not load locations into map"}], "error-request");
                handleMessages(data);
                $('#'+map_html_id).html("<p>Could not load locations.</p>");
            }
        });
    }

    return {
        // public
        init: function (url, map_html_id) {
            init(url, map_html_id);
        }
    };
}();