'use strict';

angular.module('clientAPI', ['ajax']);

angular.module('clientAPI').factory('clientAPI', function (Ajax) {

    var api = {};

    api.get_location = function (address) {
        var url = 'http://maps.google.com/maps/api/geocode/json?address=' + address + '&sensor=false';
        return Ajax.get(url);
    };

    api.get_reports = function () {
        var url = '/denuncias/rest/';
        return Ajax.get(url);
    };

    return api;

});