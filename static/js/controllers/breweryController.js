angular.module('brewery')
  .controller('BreweryController', function($scope, $http, $interval, notificationService) {
    $scope.mode = "idle";
    $scope.tRed = "n/a";
    $scope.tBlue = "n/a";
    $scope.tGreen = "n/a";
    $scope.date = new Date();

    $scope.logEnabled = false;
    $scope.controlEnabled = false;

    $scope.prepStartTime;
    $scope.mashStartTime;
    $scope.boilStartTime;
    $scope.fermentStartTime;

    $scope.prepElapsed;
    $scope.mashElapsed;
    $scope.boilElapsed;
    $scope.fermentElapsed;

    $scope.setpoint = 19;

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
            $scope.connected = true;
            $scope.mode = data.data.mode;
            $scope.tRed = data.data.sensors[0].tempC;
            $scope.tBlue = data.data.sensors[1].tempC;
            $scope.tGreen = data.data.sensors[2].tempC;
            $scope.logEnabled = data.data.logEnabled;
            $scope.controlEnabled = data.data.controlEnabled;
            $scope.setpoint = data.data.setpoint;
            $("[name='logEnabled']").bootstrapSwitch('state', $scope.logEnabled);
            $("[name='controlEnabled']").bootstrapSwitch('state', $scope.controlEnabled);
            if (first === true) {
              console.log(data.data);
              $scope.prepStartTime = new Date(data.data.prepStartTime * 1000);
              $scope.mashStartTime = new Date(data.data.mashStartTime * 1000);
              $scope.boilStartTime = new Date(data.data.boilStartTime * 1000);
              $scope.fermentStartTime = data.data.fermentStartTime;
              $scope.redId = data.data.sensors[0].id;
              $scope.blueId = data.data.sensors[1].id;
              $scope.greenId = data.data.sensors[2].id;
              $('input[name="logEnabled"]').on('switchChange.bootstrapSwitch', function(event, state) {
                $http.post('http://localhost:5000/log/' + state);
              });
              $('input[name="controlEnabled"]').on('switchChange.bootstrapSwitch', function(event, state) {
                $http.post('http://localhost:5000/control/' + state);
              });
            }
          },
          function error(data) {
            // try again
            $scope.connected = false;
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
      $("[name='controlEnabled']").bootstrapSwitch('disabled', false);
      $http.post('http://localhost:5000/ferment');
    };

    $scope.stop = function() {
      resetTimers();
      $scope.mode = "idle";
      $("[name='controlEnabled']").bootstrapSwitch('disabled', true);
      $http.post('http://localhost:5000/stop');
    };

    $scope.setControlEnabled = function(control) {
      $http.post('http://localhost:5000/control/' + control?1:0)
      .then(
        function success(data) {
          $scope.controlEnabled = control;
        }
      );
    };

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
    };

    var lazySetpointChange =  _.debounce(function() {$http.post("http://localhost:5000/temp/" + $scope.setpoint);}, 300);

    $scope.setpointChange = function(delta) {
      $scope.setpoint = $scope.setpoint + delta;
      $http.post("http://localhost:5000/temp/" + $scope.setpoint)
      // lazySetpointChange();
    }

    getStatus(true); // true = set first-time values
  });
