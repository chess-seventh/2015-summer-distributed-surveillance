(function() {
  var Controller, app,
    bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  app = angular.module('app', ['ui.bootstrap']);

  app.service('api', [
    '$http', function($http) {
      var devices;
      devices = [
        {
          id: 0,
          name: 'rpi-nitro',
          sensors: [
            {
              id: 'luminosity',
              name: 'luminosity'
            }
          ]
        }, {
          id: 1,
          name: 'rpi-piva',
          sensors: [
            {
              id: 'humidity',
              name: 'humidity'
            }, {
              id: 'pir',
              name: 'pir'
            }, {
              id: 'temperature',
              name: 'temperature'
            }
          ]
        }
      ];
      return {
        devices: devices,
        getDevice: function(deviceId) {
          var device, j, len;
          for (j = 0, len = devices.length; j < len; j++) {
            device = devices[j];
            if (device.id === deviceId) {
              return device;
            }
          }
          return null;
        },
        getCameras: function(from, to, offset, limit) {
          if (offset == null) {
            offset = 0;
          }
          if (limit == null) {
            limit = 100;
          }
          return $http.get('/api/cameras/', {
            params: {
              from: from.format('YYYY-MM-DD HH:mm:ss'),
              to: to.format('YYYY-MM-DD HH:mm:ss'),
              offset: offset,
              limit: limit
            }
          }).then(function(response) {
            return response.data;
          });
        },
        getHumidity: function(deviceId, from, to, offset, limit) {
          if (offset == null) {
            offset = 0;
          }
          if (limit == null) {
            limit = 100;
          }
          return $http.get('/api/humidity/' + deviceId, {
            params: {
              from: from.format('YYYY-MM-DD HH:mm:ss'),
              to: to.format('YYYY-MM-DD HH:mm:ss'),
              offset: offset,
              limit: limit
            }
          }).then(function(response) {
            return response.data;
          });
        },
        getLuminosity: function(deviceId, from, to, offset, limit) {
          if (offset == null) {
            offset = 0;
          }
          if (limit == null) {
            limit = 100;
          }
          return $http.get('/api/luminosity/' + deviceId, {
            params: {
              from: from.format('YYYY-MM-DD HH:mm:ss'),
              to: to.format('YYYY-MM-DD HH:mm:ss'),
              offset: offset,
              limit: limit
            }
          }).then(function(response) {
            return response.data;
          });
        },
        getPir: function(deviceId, from, to, offset, limit) {
          if (offset == null) {
            offset = 0;
          }
          if (limit == null) {
            limit = 100;
          }
          return $http.get('/api/pir/' + deviceId, {
            params: {
              from: from.format('YYYY-MM-DD HH:mm:ss'),
              to: to.format('YYYY-MM-DD HH:mm:ss'),
              offset: offset,
              limit: limit
            }
          }).then(function(response) {
            return response.data;
          });
        },
        getTemperature: function(deviceId, from, to, offset, limit) {
          if (offset == null) {
            offset = 0;
          }
          if (limit == null) {
            limit = 100;
          }
          return $http.get('/api/temperature/' + deviceId, {
            params: {
              from: from.format('YYYY-MM-DD HH:mm:ss'),
              to: to.format('YYYY-MM-DD HH:mm:ss'),
              offset: offset,
              limit: limit
            }
          }).then(function(response) {
            return response.data;
          });
        }
      };
    }
  ]);

  app.directive('chart', [
    function() {
      return {
        scope: {
          data: '='
        },
        link: function(scope, el, attrs) {
          var chart;
          chart = AmCharts.makeChart(el[0], {
            type: 'serial',
            categoryField: 'x',
            categoryAxis: {
              minPeriod: 'ss',
              parseDates: true
            },
            graphs: [
              {
                type: 'step',
                valueField: 'y',
                fillAlphas: 0.4,
                bullet: 'square',
                bulletAlpha: 0,
                bulletBorderAlpha: 0,
                bulletSize: 3,
                balloonText: '[[category]]<br><b>[[value]]</b>'
              }
            ],
            dataProvider: []
          });
          return scope.$watch('data', function() {
            if (scope.data == null) {
              return;
            }
            chart.dataProvider = scope.data;
            chart.invalidateSize();
            return chart.validateData();
          });
        }
      };
    }
  ]);

  app.directive('angularVideo', [
    function() {
      return {
        scope: {
          row: '='
        },
        link: function(scope, el, attrs) {
          return scope.$watch('row', function() {
            if (scope.row == null) {
              return;
            }
            if (scope.row.stopped_at) {
              return el.html($('<embed></embed>').attr('src', 'http://rpi-nitro/' + scope.row.video_key + '.swf').attr('width', '640').attr('height', '480'));
            } else {
              return el.html($('<iframe></iframe>').attr('src', 'http://rpi-nitro:8081/').attr('width', '100%').attr('height', '500').attr('frameborder', '0'));
            }
          });
        }
      };
    }
  ]);

  app.controller('VideoController', [
    'api', 'row', Controller = (function() {
      function Controller(api, row1) {
        this.api = api;
        this.row = row1;
      }

      return Controller;

    })()
  ]);

  app.controller('CameraController', [
    '$scope', '$interval', '$modal', 'api', Controller = (function() {
      function Controller($scope, $interval, $modal, api) {
        var task;
        this.$scope = $scope;
        this.$interval = $interval;
        this.$modal = $modal;
        this.api = api;
        this.refresh = bind(this.refresh, this);
        this.rows = [];
        this.refresh();
        task = this.$interval(this.refresh, 5000);
        this.$scope.$on('$destroy', function() {
          return task.cancel();
        });
      }

      Controller.prototype.refresh = function() {
        this.currentTime = new Date();
        return this.api.getCameras(moment.utc().subtract(1, 'day'), moment.utc(), 0, 15).then((function(_this) {
          return function(rows) {
            var i, row;
            i = 0;
            while (i < rows.length) {
              row = {
                device_id: rows[i].device_id,
                device: _this.api.getDevice(rows[i].device_id),
                created_at: moment(rows[i].created_at).toDate(),
                stopped_at: rows[i].stopped_at ? moment(rows[i].stopped_at).toDate() : null,
                video_key: rows[i].video_key
              };
              if (i > _this.rows.length) {
                _this.rows.push(row);
              } else {
                _this.rows[i] = row;
              }
              i++;
            }
            return _this.rows.splice(rows.length, rows.length - _this.rows.length);
          };
        })(this));
      };

      Controller.prototype.showVideo = function(row) {
        return this.$modal.open({
          templateUrl: 'video.html',
          controller: 'VideoController',
          controllerAs: 'ctrl',
          resolve: {
            row: function() {
              return row;
            }
          }
        });
      };

      return Controller;

    })()
  ]);

  app.controller('ChartController', [
    '$scope', '$interval', 'api', Controller = (function() {
      function Controller($scope, $interval, api) {
        var task;
        this.$scope = $scope;
        this.$interval = $interval;
        this.api = api;
        this.refresh = bind(this.refresh, this);
        this.devices = this.api.devices;
        this.currentDevice = null;
        this.currentSensor = null;
        this.rows = [];
        this.loading = false;
        this.$scope.$watchGroup(['ctrl.currentDevice', 'ctrl.currentSensor'], this.refresh);
        task = this.$interval(this.refresh, 10000);
        this.$scope.$on('$destroy', function() {
          return task.cancel();
        });
      }

      Controller.prototype.refresh = function() {
        var loader;
        if (this.loading) {
          return;
        }
        if (!((this.currentDevice != null) && (this.currentSensor != null))) {
          return;
        }
        loader = (function() {
          switch (this.currentSensor.id) {
            case 'luminosity':
              return this.api.getLuminosity;
            case 'humidity':
              return this.api.getHumidity;
            case 'pir':
              return this.api.getPir;
            case 'temperature':
              return this.api.getTemperature;
            default:
              this.rows = [];
              return null;
          }
        }).call(this);
        if (loader != null) {
          if (this.rows.length === 0) {
            this.loading = true;
          }
          return loader(this.currentDevice.id, moment.utc().subtract(6, 'hours'), moment.utc(), 0, 10000).then((function(_this) {
            return function(rows) {
              var j, len, results, row;
              _this.loading = false;
              _this.rows = [];
              results = [];
              for (j = 0, len = rows.length; j < len; j++) {
                row = rows[j];
                results.push(_this.rows.push({
                  x: moment(row.created_at).toDate(),
                  y: parseFloat(row.value)
                }));
              }
              return results;
            };
          })(this));
        }
      };

      return Controller;

    })()
  ]);

}).call(this);

//# sourceMappingURL=app.js.map
