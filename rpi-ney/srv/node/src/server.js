/**
 * Nodejs server application to serve frontend
 * static files (html,css,js) and expose rest
 * api endpoints to query data.
 *
 * Author: Antony Ducommun dit Boudry
 */
var express = require('express');
var mysql = require('mysql');


/**
 * Query the MySQL database and write error if any to response.
 *
 */
var execQuery = function(res, query, params, cb) {
  try {
    var connection = mysql.createConnection({
      host     : 'localhost',
      user     : 'root',
      password : '',
      database : 'video_system'
    });

    connection.connect();
    connection.query(query, params, function(err, rows, fields) {
      if (err) {
        console.log(err);
        res.status(500).send();
      } else {
        cb(rows, fields);
      }
    });
    connection.end();
  } catch (e) {
    console.log(err);
    res.status(500).send();
  }
};

/**
 * Query the MySQL database and write rows to response.
 *
 */
var execQueryAsJson = function(res, query, params) {
  execQuery(res, query, params, function(rows, fields) {
    res.status(200).json(rows);
  });
};


/**
 * Express/Connect application.
 *
 * /api/cameras?from=2015-01-01&to=2015-12-31
 *
 *     Query video events table for all devices.
 *
 * /api/camera/:device?from=2015-01-01&to=2015-12-31
 *
 *     Query video events table for given device.
 *
 * /api/humidity/:device?from=2015-01-01&to=2015-12-31
 *
 *     Query humidity events table for given device.
 *
 * /api/temperature/:device?from=2015-01-01&to=2015-12-31
 *
 *     Query temperature events table for given device.
 *
 */
var app = express();

app.use(express.static('/srv/node/assets'));

app.get('/api/cameras', function(req, res) {
  execQueryAsJson(
    res,
    'SELECT `device_id`, `created_at`, `stopped_at`, `video_key` FROM `video_events` WHERE `created_at` BETWEEN ? AND ? ORDER BY `created_at` DESC LIMIT ?, ?',
    [
      req.query.from,
      req.query.to,
      parseInt(req.query.offset || 0),
      parseInt(req.query.limit || 100)
    ]
  );
});

app.get('/api/camera/:device', function(req, res) {
  execQueryAsJson(
    res,
    'SELECT `device_id`, `created_at`, `stopped_at`, `video_key` FROM `video_events` WHERE `device_id` = ? AND `created_at` BETWEEN ? AND ? ORDER BY `created_at` DESC LIMIT ?, ?',
    [
      req.params.device,
      req.query.from,
      req.query.to,
      parseInt(req.query.offset || 0),
      parseInt(req.query.limit || 100)
    ]
  );
});

app.get('/api/humidity/:device', function(req, res) {
  execQueryAsJson(
    res,
    'SELECT `device_id`, `created_at`, `value` FROM `humidity_events` WHERE `device_id` = ? AND `created_at` BETWEEN ? AND ? ORDER BY `created_at` ASC LIMIT ?, ?',
    [
      req.params.device,
      req.query.from,
      req.query.to,
      parseInt(req.query.offset || 0),
      parseInt(req.query.limit || 100)
    ]
  );
});

app.get('/api/luminosity/:device', function(req, res) {
  execQueryAsJson(
    res,
    'SELECT `device_id`, `created_at`, `value` FROM `luminosity_events` WHERE `device_id` = ? AND `created_at` BETWEEN ? AND ? ORDER BY `created_at` ASC LIMIT ?, ?',
    [
      req.params.device,
      req.query.from,
      req.query.to,
      parseInt(req.query.offset || 0),
      parseInt(req.query.limit || 100)
    ]
  );
});

app.get('/api/pir/:device', function(req, res) {
  execQueryAsJson(
    res,
    'SELECT `device_id`, `created_at`, `value` FROM `pir_events` WHERE `device_id` = ? AND `created_at` BETWEEN ? AND ? ORDER BY `created_at` ASC LIMIT ?, ?',
    [
      req.params.device,
      req.query.from,
      req.query.to,
      parseInt(req.query.offset || 0),
      parseInt(req.query.limit || 100)
    ]
  );
});

app.get('/api/temperature/:device', function(req, res) {
  execQueryAsJson(
    res,
    'SELECT `device_id`, `created_at`, `value` FROM `temperature_events` WHERE `device_id` = ? AND `created_at` BETWEEN ? AND ? ORDER BY `created_at` ASC LIMIT ?, ?',
    [
      req.params.device,
      req.query.from,
      req.query.to,
      parseInt(req.query.offset || 0),
      parseInt(req.query.limit || 100)
    ]
  );
});


var server = app.listen(8080, 'localhost', function() {
  console.log('Server started on port 8080...')
});
