const electron = require('electron');
const path  = require('path');
const url = require('url');

const {app, BrowserWindow} = electron;

let mainWindow;

// Wait and listen for the app to be ready
app.on('ready', function() {
  // Create a new Chromium window
  mainWindow = new BrowserWindow({});
  // Loading HTML into the window
  mainWindow.loadURL(url.format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }));
  // Quit app when closed
  mainWindow.on('closed', function() {
    app.quit();
  });
});
