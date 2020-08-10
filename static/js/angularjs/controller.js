'use strict';

angular.module('clientApp').controller('MainCtrl', function ($scope, appModel) {
    var model = $scope.model = appModel;

    $scope.get_search_address = function () {
        appModel.get_location($scope.address);

        var mapOptions = {
            zoom: 12,
            center: new google.maps.LatLng(model.location.lat, model.location.lng)
        };

        var map = new google.maps.Map(document.getElementById('google-maps'), mapOptions);
    }
});
