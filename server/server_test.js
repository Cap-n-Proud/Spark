'use strict';

const fs = require('fs');

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

});
