angular.module('brewery')
  .controller('BreweryController', function($scope, $http, $interval, notificationService) {
    $scope.mode = "idle";
    $scope.tRed = "n/a";
    $scope.tBlue = "n/a";
    $scope.tGreen = "n/a";
    $scope.display = 'brew';
    $scope.date = new Date();

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

    function getStatus() {
      $http.get('http://localhost:5000/status', 1000)
        .then(
          function success(data) {
            $scope.mode = data.data.mode;
            $scope.tRed = data.data.sensors[0].tempC < 0 ? "n/a" : data.data.sensors[0].tempC.toFixed(1);
            $scope.tBlue = data.data.sensors[1].tempC < 0 ? "n/a" : data.data.sensors[1].tempC.toFixed(1);
            $scope.tGreen = data.data.sensors[2].tempC < 0 ? "n/a" : data.data.sensors[2].tempC.toFixed(1);
          },
          function error(data) {
            // try again
            console.log("Connection failed - trying again...");
            getStatus();
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

    getStatus();
  });
