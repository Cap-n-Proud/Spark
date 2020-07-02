// * @emits open
// * @emits data
// * @emits close
// * @emits error
// * @alias module:serialport

const serPort = "/dev/ttyACM0"
const serBaud = "38400"


const SerialPort = require('serialport')
const Readline = require('@serialport/parser-readline')
const port = new SerialPort(serPort, { baudRate: Number(serBaud) })


const parser = new Readline()
port.pipe(parser)

//parser.on('data', line => console.log(`> ${line}`))
//port.write('SCM POWER ON\n')

//> ROBOT ONLINE
parser.on('data', function(data) {
//  data = data.toString('utf8');
console.log(line());
  setTimeout(function() {
    port.write("SCMD sdsds");
console.log("===> Command sent");
}, 5000);
});


//sPort.on('data', console.log)
