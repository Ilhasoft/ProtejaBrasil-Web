'use strict';

if (!window.Global) {
    window.Global = {};
}

if (!Global.angular_dependencies) {
    Global.angular_dependencies = ['appModel'];
}

angular.module('clientApp', Global.angular_dependencies);

angular.module('clientApp', Global.angular_dependencies, function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

angular.module('clientApp').config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    delete $httpProvider.defaults.headers.common['X-Requested-With'];
}]);


