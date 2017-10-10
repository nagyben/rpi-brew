angular.module('brewery')
  .controller('BreweryController', function($scope, $http, $interval, $timeout) {
    $scope.mode = "idle";
    $scope.date = new Date();

    $scope.logEnabled = false;
    $scope.controlEnabled = false;

    $scope.setpoint = 19;

    $scope.FG = 1100;
    $scope.ABV = "";

    var chartRed;
    var chartBlue;
    var chartGreen;
    var chartDataRed = [];
    var chartDataBlue = [];
    var chartDataGreen = [];

    var chartFerment;
    $scope.chartDataFerment = [];

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

    var tempIntervalCounter = 0;

    function getStatus(first) {
      $http.get('http://localhost:5000/status', 1000)
        .then(
          function success(data) {
            $scope.connected = true;
            $scope.performanceMetric = data.data.performanceMetric;
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
              $scope.fermentStartTime = new Date(data.data.fermentStartTime * 1000);
              $scope.redId = data.data.sensors[0].id;
              $scope.blueId = data.data.sensors[1].id;
              $scope.greenId = data.data.sensors[2].id;
              $('input[name="logEnabled"]').on('switchChange.bootstrapSwitch', function(event, state) {
                $http.post('http://localhost:5000/log/' + state);
              });
              $('input[name="controlEnabled"]').on('switchChange.bootstrapSwitch', function(event, state) {
                $http.post('http://localhost:5000/control/' + state);
              });
              loadChartData(data);
              $scope.onOGFGChange();
            }

            tempIntervalCounter++;

            if (tempIntervalCounter > 10) {
              tempIntervalCounter = 0;
              if (data.data.sensors[0].tempC) {
                chartDataRed.push({
                  x: new Date(),
                  y: data.data.sensors[0].tempC
                });
              }
              if (data.data.sensors[1].tempC) {
                chartDataBlue.push({
                  x: new Date(),
                  y: data.data.sensors[1].tempC
                });
              }

              if (data.data.sensors[2].tempC) {
                chartDataGreen.push({
                  x: new Date(),
                  y: data.data.sensors[2].tempC
                });
              }
            }
            updateTempCharts();
          },
          function error(data) {
            // try again
            $scope.connected = false;
            console.log("Connection failed - trying again...");
          }
        );
    }

    function calcABV(og, fg) {
      // https://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
      return (76.08 * (og - fg) / (1.775 - og)) * (fg / 0.794);
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
      $http.post('http://localhost:5000/control/' + control ? 1 : 0)
        .then(
          function success(data) {
            $scope.controlEnabled = control;
          }
        );
    };

    $scope.forceUpdate = function() {
      $http.post('http://localhost:5000/force-update')
        .then(
          function success(data) {
            $scope.forceReload();
          }
        )
    }

    $scope.updateSensor = function($event) {
      if ($event.originalEvent.keyCode == 13) { // if keyCode == enter
        var name = "";
        switch ($event.currentTarget.id) {
          case 'redId':
            name = 'red';
            break;
          case 'blueId':
            name = 'blue';
            break;
          case 'greenId':
            name = 'green';
            break;
        }
        if (name !== "") {
          $http.post('http://localhost:5000/sensor/' + name + '/' + $event.currentTarget.value);
        }
        // $http.post('http://localhost:5000')
      }
    };

    $scope.setpointChange = function(delta) {
      $scope.setpoint = $scope.setpoint + delta;
      $http.post("http://localhost:5000/temp/" + $scope.setpoint)
    }

    $scope.onOGFGChange = function() {
      var og = $scope.chartDataFerment[0] ? $scope.chartDataFerment[0].y : 0;
      if (og) {
        if ($scope.FG / 1000 >= 1 && og / 1000 >= 1) {
          $scope.ABV = calcABV(og / 1000, $scope.FG / 1000);
        }
      } else {
        $scope.ABV = 0;
      }
    }

    $scope.forceReload = function() {
      window.location.reload();
    }

    $scope.logGravity = function(gravity) {
      $http.post('http://localhost:5000/sg/' + gravity)
        .then(
          function success(data) {
            $scope.chartDataFerment.push({
              x: new Date(),
              y: gravity
            });
            updateChart();
          }
        )
    }

    $scope.deleteLastGravity = function() {
      $http.delete('http://localhost:5000/sg')
        .then(
          function success(data) {
            $scope.chartDataFerment.pop();
            $scope.onOGFGChange();
            updateChart();
          }
        )
    }

    function updateFermentChart() {
      var data = {
        series: [{
          name: 'sg',
          data: $scope.chartDataFerment
        }]
      };
      chartFerment.update(data);
    }

    function updateTempCharts() {
      chartRed.update({
        series: [{
          data: chartDataRed
        }]
      });

      chartBlue.update({
        series: [{
          data: chartDataBlue
        }]
      });

      chartGreen.update({
        series: [{
          data: chartDataGreen
        }]
      });
    }

    function loadChartData(data) {
      specificGravity = data.data.specificGravity
      for (var i = 0; i < specificGravity.length; i++) {
        $scope.chartDataFerment.push({
          x: new Date(specificGravity[i][0] * 1000),
          y: specificGravity[i][1]
        });
      }
      $scope.FG = $scope.chartDataFerment[0] ? $scope.chartDataFerment[$scope.chartDataFerment.length - 1].y : 1100;
    }

    getStatus(true); // true = set first-time

    $timeout(function() {
      chartFerment = new Chartist.Line('.ct-chart-ferment', {}, {
        axisX: {
          type: Chartist.FixedScaleAxis,
          divisor: 5,
          labelInterpolationFnc: function(value) {
            return moment(value).format('D-MMM');
          },
          showPoint: false
        }
      });
      updateFermentChart();

      chartRed = new Chartist.Line('.ct-chart-red', {}, {
        axisX: {
          type: Chartist.FixedScaleAxis,
          divisor: 5,
          labelInterpolationFnc: function(value) {
            return moment(value).format('hh:mm');
          },
          showPoint: false
        }
      });

      chartGreen = new Chartist.Line('.ct-chart-green', {}, {
        axisX: {
          type: Chartist.FixedScaleAxis,
          divisor: 5,
          labelInterpolationFnc: function(value) {
            return moment(value).format('hh:mm');
          },
          showPoint: false
        }
      });

      chartBlue = new Chartist.Line('.ct-chart-blue', {}, {
        axisX: {
          type: Chartist.FixedScaleAxis,
          divisor: 5,
          labelInterpolationFnc: function(value) {
            return moment(value).format('hh:mm');
          },
          showPoint: false
        }
      });

      updateTempCharts();
    }, 1000);
  });
