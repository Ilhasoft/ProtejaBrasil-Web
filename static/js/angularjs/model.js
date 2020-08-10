'use strict';

angular.module('appModel', ['clientAPI']);
angular.module('appModel').factory('appModel', function (clientAPI) {

    var model = {
        location: [],
        reports: []
    };

    model.get_location = function (address) {
        clientAPI.get_location(address).success(function (result) {
            if (result.status == 'OK') {
                model.location = result.results[0].geometry.location;
            }
        });
    };

    return model;

});