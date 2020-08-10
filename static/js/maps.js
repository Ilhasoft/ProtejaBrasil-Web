/**
 * Created by teehamaral on 19/10/15.
 */
'use strict';

function marker(map, icon, lat, lng, theme, violation_type, violation_local, frequency, description) {
    var marker = new google.maps.Marker({
        position: {lat: lat, lng: lng},
        map: map,
        icon: icon
    });
    marker.addListener('click', function () {
        map.setZoom(12);
        map.setCenter(marker.getPosition());
        var coordInfoWindow = new google.maps.InfoWindow();
        coordInfoWindow.setContent(createInfoWindowContent(theme, violation_type, violation_local, frequency, description));
        coordInfoWindow.setPosition({lat: lat, lng: lng});
        coordInfoWindow.open(map);
    });
}

function markeraddress(map, icon, address, theme, violation_type, violation_local, frequency, description) {
    $.get('http://maps.google.com/maps/api/geocode/json?address=' + address + '&sensor=false', function (data, status) {
        if (status == 'success') {
            var marker = new google.maps.Marker({
                position: {lat: data.results[0].geometry.location.lat, lng: data.results[0].geometry.location.lng},
                map: map,
                icon: icon
            });
            marker.addListener('click', function () {
                map.setZoom(12);
                map.setCenter(marker.getPosition());
                var coordInfoWindow = new google.maps.InfoWindow();
                coordInfoWindow.setContent(createInfoWindowContent(theme, violation_type, violation_local, frequency, description));
                coordInfoWindow.setPosition({
                    lat: data.results[0].geometry.location.lat,
                    lng: data.results[0].geometry.location.lng
                });
                coordInfoWindow.open(map);
            });
        }
    });
}

function createInfoWindowContent(theme, violation_type, violation_local, frequency, description) {
    var return_;
    if (description != '') {
        return_ = [
            'Descrição: ' + description
        ].join('<br>');
    } else {
        return_ = [
            'Tema: ' + theme,
            'Tipo de violação: ' + violation_type,
            'Localidade: ' + violation_local,
            'Frequência: ' + frequency
        ].join('<br>');
    }
    return return_

}

