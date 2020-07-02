// * @emits open
// * @emits data
// * @emits close
// * @emits error
// * @alias module:serialport

const serPort = "/dev/ttyACM0"
const serBaud = "38400"


const com = require('serialport')
const Readline = require('@serialport/parser-readline')
const sPort = new com(serPort,{
  baudRate: Number(serBaud)
});

const serialPort = sPort.pipe(new Readline({ delimiter: '\r\n' }))


sPort.on('open',function() {
  console.log('Arduino connected on '+ serPort + ' @' + serBaud)
})

// sPort.on('data', function(data) {
//   data = data.toString('utf8');
// console.log(data.trim());
//   setTimeout(function() {
//     serialPort.write("SCMD sdsds");
//     sPort.write("SCMD sdsds");
// console.log("===> Command sent");
//  }, 2000);
//});

sPort.on('data', console.log.toString('utf8'))
