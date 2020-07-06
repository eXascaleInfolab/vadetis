"use strict";

var DatasetDisplayMap = function () {

    // private
    var init = function (map_html_id) {
        var mymap = L.map(map_html_id).setView([51.505, -0.09], 13);
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'pk.eyJ1IjoidmFkZXRpcyIsImEiOiJja2NiMTB4NW8yMHI2MnRvMHk2aDl6ZG5kIn0.5CarskUSNdP8fWdvSx7Omw'
        }).addTo(mymap);
    }
    return {
        // public
        init: function(map_html_id) {
            init(map_html_id);
        }
    };
}();