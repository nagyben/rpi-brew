angular.module('brewery')

.factory('httpInterceptor', function($q, notificationService) {
	return {
		response: function(response) {
      // do something on success
			if (response.data.message) {
				notificationService(response.data.message, response.data.messageType, response.data.messageTimeout);
			}
      return response;
    },
		responseError: function(response) {
			if (response.data.message) {
				notificationService(response.data.message, response.data.messageType, response.data.messageTimeout);
			}
			return response || $q.when(response);
		}
	};
});

app.config(function($httpProvider) {
	$httpProvider.interceptors.push('httpInterceptor');
});
