angular.module('brewery')
  .controller('BreweryController', function($scope, $http, $interval, notificationService) {
    $scope.mode = "idle";
    $scope.tRed = "n/a";
    $scope.tBlue = "n/a";
    $scope.tGreen = "n/a";
    $scope.display = 'brew';
    $scope.date = new Date();

    $scope.logEnabled = true;

    $scope.prepStartTime;
    $scope.mashStartTime;
    $scope.boilStartTime;
    $scope.fermentStartTime;

    $scope.prepElapsed;
    $scope.mashElapsed;
    $scope.boilElapsed;
    $scope.fermentElapsed;

    $interval(updateLoop, 1000);

    function updateLoop() {
      $scope.date = new Date();
      $scope.prepElapsed = calcElapsedMinutesSeconds($scope.prepStartTime);
      $scope.mashElapsed = calcElapsedMinutesSeconds($scope.mashStartTime);
      $scope.boilElapsed = calcElapsedMinutesSeconds($scope.boilStartTime);
      $scope.fermentElapsed = calcElapsedHoursMinutes($scope.fermentStartTime);
      getStatus();
    }

    function calcElapsedMinutesSeconds(startTime) {
      if (startTime > 0) {
        var diffSeconds = Math.floor((new Date() - startTime) / 1000)
        var mins = String("00" + Math.floor(diffSeconds / 60)).slice(-2);
        var seconds = String("00" + diffSeconds % 60).slice(-2);
        return mins.toString() + "m" + seconds.toString() + "s"
      } else {
        return "";
      }
    }

    function calcElapsedHoursMinutes(startTime) {
      if (startTime > 0) {
        var diffSeconds = Math.floor((new Date() - startTime) / 1000);
        var hours = String(Math.floor(diffSeconds / 60 / 60));
        var mins = String("00" + (Math.floor((diffSeconds / 60) % 60))).slice(-2);
        return hours.toString() + "h" + mins.toString() + "m"
      } else {
        return "";
      }
    }

    function resetTimers() {
      $scope.prepStartTime = 0;
      $scope.mashStartTime = 0;
      $scope.boilStartTime = 0;
      $scope.fermentStartTime = 0;
    }

    function getStatus(first) {
      $http.get('http://localhost:5000/status', 1000)
        .then(
          function success(data) {
            $scope.mode = data.data.mode;
            $scope.tRed = data.data.sensors[0].tempC;
            $scope.tBlue = data.data.sensors[1].tempC;
            $scope.tGreen = data.data.sensors[2].tempC;
            $scope.logEnabled = data.data.logEnabled;
            $("[name='logEnabled']").bootstrapSwitch('state', $scope.logEnabled);
            if (first === true) {
              $scope.prepStartTime = data.data.prepStartTime;
              $scope.mashStartTime = data.data.mashStartTime;
              $scope.boilStartTime = data.data.boilStartTime;
              $scope.fermentStartTime = data.data.fermentStartTime;
            }
          },
          function error(data) {
            // try again
            console.log("Connection failed - trying again...");
          }
        );
    }

    $scope.startPrep = function() {
      resetTimers();
      $scope.prepStartTime = new Date();
      $scope.mode = "prep";
      $http.post('http://localhost:5000/prep');
    };

    $scope.startMash = function() {
      resetTimers();
      $scope.mashStartTime = new Date();
      $scope.mode = "mash";
      $http.post('http://localhost:5000/mash');
    };

    $scope.startBoil = function() {
      resetTimers();
      $scope.boilStartTime = new Date();
      $scope.mode = "boil";
      $http.post('http://localhost:5000/boil');
    };

    $scope.startFerment = function() {
      resetTimers();
      $scope.fermentStartTime = new Date();
      $scope.mode = "ferment";
      $http.post('http://localhost:5000/ferment');
    };

    $scope.setControlEnabled = function(control) {
      $http.post('http://localhost:5000/control/' + control?1:0)
      .then(
        function success(data) {
          $scope.controlEnabled = control;
        }
      );
    }

    $scope.updateSensor = function($event) {
      if ($event.originalEvent.keyCode == 13) { // if keyCode == enter
        var name = "";
        switch ($event.currentTarget.id) {
          case 'redId': name = 'red'; break;
          case 'blueId': name = 'blue'; break;
          case 'greenId': name = 'green'; break;
        }
        if (name !== "") {
          $http.post('http://localhost:5000/sensor/' + name + '/' + $event.currentTarget.value);
        }
        // $http.post('http://localhost:5000')
      }
    }

    getStatus(true); // true = set first-time values.

    $("[name='logEnabled']").bootstrapSwitch();
    $('input[name="logEnabled"]').on('switchChange.bootstrapSwitch', function(event, state) {
      $http.post('http://localhost:5000/log/' + state);
    });
  });
