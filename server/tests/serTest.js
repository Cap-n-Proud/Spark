// * @emits open
// * @emits data
// * @emits close
// * @emits error
// * @alias module:serialport

const serPort = "/dev/ttyACM0"
const serBaud = "115200"


const com = require('serialport')
const Readline = require('@serialport/parser-readline')
const sPort = new com(serPort,{
  baudRate: Number(serPort)
});

const serialPort = sPort.pipe(new Readline({ delimiter: '\r\n' }))


sPort.on('open',function() {
  console.log('Arduino connected on '+ serPort + ' @' + serBaud)
})

sPort.on('data', console.log)
