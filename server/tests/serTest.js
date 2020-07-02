// * @emits open
// * @emits data
// * @emits close
// * @emits error
// * @alias module:serialport

const serPort = "/dev/ttyACM0"
const serBaud = "38400"


const SerialPort = require('serialport')
const Readline = require('@serialport/parser-readline')
const port = new SerialPort(path, { baudRate: 38400 })


const parser = new Readline()
port.pipe(parser)

parser.on('data', line => console.log(`> ${line}`))
port.write('SCM POWER ON\n')

sPort.on('open',function() {
  console.log('Arduino connected on '+ serPort + ' @' + serBaud)
})
//> ROBOT ONLINE
// sPort.on('data', function(data) {
//   data = data.toString('utf8');
// console.log(data.trim());
//   setTimeout(function() {
//     serialPort.write("SCMD sdsds");
//     sPort.write("SCMD sdsds");
// console.log("===> Command sent");
//  }, 2000);
//});
