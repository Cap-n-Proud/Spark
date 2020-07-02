'use strict';

const fs = require('fs');
const events = require('events');
const eventEmitter = new events.EventEmitter();

let rawdata = fs.readFileSync(__dirname + '/config.json');
let config = JSON.parse(rawdata);

const express = require('express');
const app = express();

var http = require('http').Server(app);
var io = require('socket.io')(http);

//Includes
var functions = require(__dirname + '/lib/functions');

//var videoFeed = require(__dirname + '/lib/video');

// load the routes
app.use(express.static('wwwroot'));
require('./routes')(app);



//SysVars
var serverADDR = functions.findMyIP();


const serPort = config.server.serPort;
const baudRate =  config.server.serBaud;
const serverPort =  config.server.serverPort;
const version =  config.server.version;
var SEPARATOR = config.telemetry.SEPARATOR;
var LogR = 0;
var TelemetryFN = 'N/A';
var prevTel = "";
var prevPitch = "";
var THReceived = 0;

var TelemetryHeader = 'N/A';
var PIDHeader = 'N/A';
var ArduSysHeader;
var Telemetry = {};
var PID = {};
var PIDVal;
var ArduSys = {};
var temperature;

console.log(serPort);
//------------------------- Setup serial port -------------------------//
const com = require('serialport')
const Readline = require('@serialport/parser-readline')
const sPort = new com(serPort, {
    baudRate: Number(baudRate)
});

const serialPort = sPort.pipe(new Readline({ delimiter: '\r\n' }))
sPort.on('open', function() {
    console.log('Arduino connected on ' + serPort + ' @' + baudRate)
})
//------------------------- END Setup serial port -------------------------//

eventEmitter.on('CMDecho', function(data) {
    socket.emit('CMD', data);
});

eventEmitter.on('serialData', function(data) {
    socket.emit('serialData', data);
});

io.on('connection', function(socket){
  var myDate = new Date();
  var startMessage = 'Connected ' + config.server.name + ' v' + config.server.version + ' @' + serverADDR + ':'+ config.server.serverPort;
  console.log(startMessage);
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
    });

  socket.on('connected', function() {


  });
  //Clients emit env_val event to get teh environment variables, server answers with 'connected' event
  socket.on('env_val', function() {
    //Test if an host is alive
    // var robotjURL = 'http://' + serverADDR + ':' + config.server.serverPort +'/vj'
    // ping.sys.probe(host,function(isAlive){var msg = isAlive ? 'true' : 'false';
    // console.log(msg)});

    socket.emit('connected', startMessage, serverADDR, config.server.serverPort, config.video.port);

  });



//  setTimeout(function() {
//      videoFeed.startVideoFeed(socket, videoWidth, videoHeight, fps);
//  }, 2000);


  socket.on('move', function(dX, dY) {
      //serialPort.write('SCMD move ' + Math.round(dX) + ' ' + Math.round(dY) + '\n');
      //console.log('SCMD move ' + Math.round(dX) + ' ' + Math.round(dY));

  });


});


http.listen(config.server.serverPort, function(){

  console.log('listening on: ' + serverADDR + ':'+ config.server.serverPort);
  //Read input from Arduino and stores it into a dictionary
  sPort.on('data', function(data, socket) {
    data = data.toString('utf8');
    console.log(data.trim());
    if (data.indexOf('T') !== -1) {
        var tokenData = data.split(SEPARATOR);
        var j = 0;
        console.log("GOT T");
        for (var i in Telemetry) {
            Telemetry[i] = tokenData[j];
            j++;
            console.log(i + ' ' + Telemetry[i]);
        }
        j = 0;

        //eventEmitter.emit('log', data);

        if (LogR == 1) {
        //    functions.addTelemetryRow(telemetryfilePath, TelemetryFN, TelemetryHeader, data, PIDHeader, PIDVal, SEPARATOR)
        }
    }

});
});
