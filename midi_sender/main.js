const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow

const path = require('path')
const url = require('url')

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({ width: 500, height: 200 })
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  // mainWindow.webContents.openDevTools()

  mainWindow.on('closed', function () {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow()
  }
})

const ipc = require('electron').ipcMain
var maya;

ipc.on('portNum', function (event, arg) {
  const net = require('net');
  maya = new net.createConnection(arg);

  maya.on('error', function (e) {
    console.log(e);
    event.sender.send('connection-reply', e.errno);
  });

  maya.on('connect', function () {
    console.log('Connected - Maya');
    event.sender.send('connection-reply', 'Connected');
  });

  maya.on('data', function (data) {
    console.log('Maya: ' + data);
  });

  maya.on('close', function (data) {
    console.log('Maya: commandPort was closed.');
    event.sender.send('connection-reply', 'commandPort was closed.');
    // app.quit()
  });
});

ipc.on('MIDImessage', function (event, arg) {
  var message = 'start,' + arg[1] + ',' + arg[2] / 127 + ',end';
  maya.write(message);
});