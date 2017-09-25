angular.module('brewery')
	.factory('notificationService', function() {
		return function(msg, timeout) {
			timeout = typeof timeout === 'undefined' ? 5000 : timeout;
			new Noty({
				text: msg,
				type: 'info',
				timeout: timeout,
				theme: 'metroui',
				// layout: 'topCenter'
			}).show();
		};
	})
	.factory('confirmationService', function($q) {
		return {
			show: function(msg, positiveButtonText, negativeButtonText) {

				positiveButtonText = typeof positiveButtonText === 'undefined' ? 'OK' : positiveButtonText;
				negativeButtonText = typeof negativeButtonText === 'undefined' ? 'Cancel' : negativeButtonText;

				var deferred = $q.defer();
				var confirmDialog = noty({
					text: msg,
					type: 'confirm',
					modal: true,
					theme: 'relax',
					layout: 'center',
					timeout: false,
					buttons: [{
						addClass: 'btn btn-primary',
						text: positiveButtonText,
						onClick: function($noty) {
							$noty.close();
							deferred.resolve();
						}
					}, {
						addClass: 'btn btn-danger',
						text: negativeButtonText,
						onClick: function($noty) {
							$noty.close();
							deferred.reject();
						}
					}]
				});
				return deferred.promise;
			}
		};
	});
