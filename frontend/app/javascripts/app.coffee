##
# Angular application
#
# Displays alerts table and measurements chart.
#
# Author: Antony Ducommun dit Boudry
##

# create the angular module
app = angular.module('app', ['ui.bootstrap'])


# register api service (REST calls)
app.service('api', [
  '$http',
  ($http) ->
    # static list of devices/sensors
    devices = [
        id: 0
        name: 'rpi-nitro'
        sensors: [
            id: 'luminosity'
            name: 'luminosity'
        ]
      ,
        id: 1
        name: 'rpi-piva'
        sensors: [
            id: 'humidity'
            name: 'humidity'
          ,
            id: 'pir'
            name: 'pir'
          ,
            id: 'temperature'
            name: 'temperature'
        ]
    ]

    # public service members
    devices: devices
    getDevice: (deviceId) ->
      for device in devices when device.id == deviceId
        return device
      null
    getCameras: (from, to, offset=0, limit=100) ->
      $http.get(
        '/api/cameras/',
        params:
          from: from.format('YYYY-MM-DD HH:mm:ss')
          to: to.format('YYYY-MM-DD HH:mm:ss')
          offset: offset
          limit: limit
      ).then(
        (response) ->
          response.data
      )
    getHumidity: (deviceId, from, to, offset = 0, limit=100) ->
      $http.get(
        '/api/humidity/' + deviceId,
        params:
          from: from.format('YYYY-MM-DD HH:mm:ss')
          to: to.format('YYYY-MM-DD HH:mm:ss')
          offset: offset
          limit: limit
      ).then(
        (response) ->
          response.data
      )
    getLuminosity: (deviceId, from, to, offset = 0, limit=100) ->
      $http.get(
        '/api/luminosity/' + deviceId,
        params:
          from: from.format('YYYY-MM-DD HH:mm:ss')
          to: to.format('YYYY-MM-DD HH:mm:ss')
          offset: offset
          limit: limit
      ).then(
        (response) ->
          response.data
      )
    getPir: (deviceId, from, to, offset = 0, limit=100) ->
      $http.get(
        '/api/pir/' + deviceId,
        params:
          from: from.format('YYYY-MM-DD HH:mm:ss')
          to: to.format('YYYY-MM-DD HH:mm:ss')
          offset: offset
          limit: limit
      ).then(
        (response) ->
          response.data
      )
    getTemperature: (deviceId, from, to, offset = 0, limit=100) ->
      $http.get(
        '/api/temperature/' + deviceId,
        params:
          from: from.format('YYYY-MM-DD HH:mm:ss')
          to: to.format('YYYY-MM-DD HH:mm:ss')
          offset: offset
          limit: limit
      ).then(
        (response) ->
          response.data
      )
])


# register chart directive (bind amchart in angular)
app.directive('chart',
  [
    ->
      scope:
        data: '='
      link: (scope, el, attrs) ->
        # create chart object
        chart = AmCharts.makeChart(
          el[0],
          type: 'serial'
          categoryField: 'x'
          categoryAxis:
            minPeriod: 'ss'
            parseDates: true
          graphs: [
            type: 'step'
            valueField: 'y'
            fillAlphas: 0.4
            bullet: 'square'
            bulletAlpha: 0
            bulletBorderAlpha: 0
            bulletSize: 3
            balloonText: '[[category]]<br><b>[[value]]</b>'
          ]
          dataProvider: []
        )

        # update chart data on demand
        scope.$watch('data', ->
          return unless scope.data?
          chart.dataProvider = scope.data
          chart.invalidateSize()
          chart.validateData()
        )
  ]
)

# register video directive (embed flash video or real-time iframe)
app.directive('angularVideo',
  [
    ->
      scope:
        row: '='
      link: (scope, el, attrs) ->
        scope.$watch('row', ->
          return unless scope.row?

          if scope.row.stopped_at
            # video is complete, show flash video
            el.html(
              $('<embed></embed>')
                .attr('src', 'http://rpi-nitro/' + scope.row.video_key + '.swf')
                .attr('width', '640')
                .attr('height', '480')
            )
          else
            # video is recording, show real-time camera stream
            el.html(
              $('<iframe></iframe>')
                .attr('src', 'http://rpi-nitro:8081/')
                .attr('width', '100%')
                .attr('height', '500')
                .attr('frameborder', '0')
            )
        )
  ]
)


# the video modal dialog controller
app.controller('VideoController', [
  'api',
  'row',
  class Controller
    constructor: (@api, @row) ->
]);

# the alerts table component controller
app.controller('CameraController', [
  '$scope',
  '$interval',
  '$modal',
  'api',
  class Controller
    constructor: (@$scope, @$interval, @$modal, @api) ->
      @rows = []
      @refresh()

      # refresh data every 5 seconds
      task = @$interval(@refresh, 5000)
      @$scope.$on('$destroy', -> task.cancel())

    refresh: =>
      # asynchronously load alerts
      @currentTime = new Date()
      @api.getCameras(
        moment.utc().subtract(1, 'day'),
        moment.utc(),
        0,
        15
      ).then(
        (rows) =>
          i = 0
          while i < rows.length
            row =
              device_id: rows[i].device_id
              device: @api.getDevice(rows[i].device_id)
              created_at: moment(rows[i].created_at).toDate()
              stopped_at: if rows[i].stopped_at then moment(rows[i].stopped_at).toDate() else null
              video_key: rows[i].video_key
            if i > @rows.length
              @rows.push(row)
            else
              @rows[i] = row
            i++
          @rows.splice(rows.length, rows.length - @rows.length)
      )

    showVideo: (row) ->
      # show video dialog
      @$modal.open(
        templateUrl: 'video.html'
        controller: 'VideoController'
        controllerAs: 'ctrl'
        resolve:
          row: -> row
      )
])

# the chart component controller
app.controller('ChartController', [
  '$scope',
  '$interval',
  'api',
  class Controller
    constructor: (@$scope, @$interval, @api) ->
      @devices = @api.devices
      @currentDevice = null
      @currentSensor = null
      @rows = []
      @loading = false

      # refresh data if device/sensor selection changes
      @$scope.$watchGroup(['ctrl.currentDevice', 'ctrl.currentSensor'], @refresh)

      # refresh data every 10 seconds
      task = @$interval(@refresh, 10000)
      @$scope.$on('$destroy', -> task.cancel())

    refresh: =>
      return if @loading
      return unless @currentDevice? && @currentSensor?

      # find api call
      loader = switch @currentSensor.id
        when 'luminosity'
          @api.getLuminosity

        when 'humidity'
          @api.getHumidity

        when 'pir'
          @api.getPir

        when 'temperature'
          @api.getTemperature

        else
          @rows = []
          null

      # asynchronously load measurements
      if loader?
        @loading = true if @rows.length == 0
        loader(
          @currentDevice.id,
          moment.utc().subtract(6, 'hours'),
          moment.utc(),
          0,
          10000
        ).then(
          (rows) =>
            @loading = false
            @rows = []
            for row in rows
              @rows.push(
                x: moment(row.created_at).toDate()
                y: parseFloat(row.value)
              )
        )
])
