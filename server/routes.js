
// Routers
// expose the routes to our app with module.exports
//var server = require('./server_test');

module.exports = function(app) {
{
app.get('/', function(req, res){
  res.render(__dirname + '/wwwroot/index.html' ,{serverADDR: "serverADDR", test: "12345"});
  res.end;
});

app.get('/d3test', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/d3test.html');
  res.end;
});

app.get('/showConfig', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/showConfig.html');
  res.end;
});

app.get('/d3', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/D3.html');
  res.end;
});

app.get('/livedata', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/livedata.html');
  res.end;
});

app.get('/video', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/videoFeed.html');
  res.end;
});


app.get('/serialMonitor', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/serialMonitor.html');
  res.end;
});

app.get('/test', function(req, res) {
  res.sendFile( __dirname  + '/wwwroot/test.html');
  res.end;
});

app.get('/vj', function(req, res) {
  res.sendFile(__dirname + '/wwwroot/vj.html');
  res.end;
});

app.get('/REBOOT', function(req, res) {
  var postData = req.url;
  function puts(error, stdout, stderr) { sys.puts(stdout) }
  exec('sudo reboot now');
  sockets.emit('Info', "Rebooting")
  //console.log(postData);
  res.end;
});

}

    }
