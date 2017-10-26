<<<<<<< HEAD
const electron = require('electron')
const path  = require('path');
const url = require('url')

const {app, BrowserWindow} = require('electron');

let mainWindow;

// Wait and listen for the app to be ready
app.on('ready', function() {
  // Create a new Chromium window
  mainWindow = new BrowserWindow({});
  // Loading HTML into the window
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'mainWindow.html'),
    protocol: 'file:',
    slashes: true
  }));
});
=======
const electron = require("electron")
const log = require("electron-log")
const ipcMain = electron.ipcMain

const app = electron.app
const BrowserWindow = electron.BrowserWindow

let mainWindow;

const path = require('path')
const url = require('url')
let autoUpdater = undefined

log.info('Electron started...')
log.info('Version: ' + app.getVersion())
log.transport.file.level = 'info'

const buildDestination = "./ui";

function isDebug() {
  return process.argv.length > 3 && process.argv[2] === 'debug'
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800
  })

  mainWindow.webContents.on('did-finish-load', () => {
    mainWindow.setTitle('ChatApp (' + app.getVersion() + ')')
  })

  global.dirname = __dirname;
  global.userDataPath = app.getPath('userData')

  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, buildDestination + '/index.html'),
    protocol: 'file:',
    slashes: true
  }))

  mainWindow.on('closed', function() {
    mainWindow = null
  })
}

app.on('ready', function() {
  createWindow()
})

app.on('window-all-closed', function() {
  if(process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', function() {
  if(mainWindow === null) {
    createWindow()
  }
})
>>>>>>> 96267f7f5754e634862078fc11a205df0d34eeac
