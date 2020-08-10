'use strict';

angular.module('ajax', []);
angular.module('ajax').config(
    function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = Global.CSRF_TOKEN;
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
        $httpProvider.defaults.headers.put['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';
    }
);

angular.module('ajax').factory('Ajax', function($http){
    return {
        get: function(url, params){
            if(!params){
                params = {};
            }
            return $http({
                method: 'GET',
                url: url,
                params: params
            });
        },
        post: function(url, params){
            if(!params){
                params = {};
            }
            return $http({
                method: 'POST',
                url: url,
                data: $.param(params)
            });
        },
        delete: function(url, params){
            if(!params){
                params = {};
            }
            return $http({
                method: 'DELETE',
                url: url,
                params: params
            });
        },
        put: function(url, params){
            if(!params){
                params = {};
            }
            return $http({
                method: 'PUT',
                url: url,
                data: $.param(params)
            });
        }
    };
});