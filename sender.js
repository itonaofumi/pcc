// network
var net = require('net');
var maya = new net.createConnection('3000');

maya.setEncoding('utf8');

maya.on('error', function(e) {
  console.log('Connection Failed \'' + e + '\'');
  input.closePort();
  process.exit(1);
});

maya.on('connect', function() {
  console.log('Connected - Maya');
});

// send stdin
process.stdin.resume();
process.stdin.on('data', function(data) {
  maya.write(data);
});

maya.on('data', function(data) {
  console.log('Maya: ' + data);
});

maya.on('close', function(data) {
  console.log('Maya: commandPort was closed.');
  input.closePort();
  process.exit(1);
});

// MIDI
var midi = require('midi');
var input = new midi.input();

if (input.getPortCount()) {
  console.log(input.getPortName(0));
  input.openPort(0);
  input.ignoreTypes(false, false, false);
}

input.on('message', function(deltaTime, message) {
  //console.log('m:' + message + ' d:' + deltaTime);
  var msg = parseMessage(message);
  console.log('sender.js: ' + msg);
  maya.write(String(msg));
});

function parseMessage(raw) {
  // 複数のスライダーを同時に動かしたりすると情報が大量に送られ、
  // 連結された状態でMAYAが受け取ってしまうので、
  // MAYA側でsplitしやすいようにstart, endを明示してあげる
  var message = 'start,' + raw[1] + ',' + raw[2] / 127 + ',end';
  return message
}

process.on('SIGINT', () => {
  console.log('Close port.');
  input.closePort();
  process.exit(1);
});
