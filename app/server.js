const mongo = require('mongodb').MongoClient;
const client = require('socket.io').listen(4000).sockets;

// Establish a MongoDB connection
mongo.connect('mongodb://127.0.0.1/chatapp', function(err, db) {
  // Check for errors and throw
  if(err) {
    throw err;
  }

  console.log('Connected to the database')

  // Create WS connection
  client.on('connection', function() {
    let chat = db.collection('chats');

    // Send status func
    sendStatus = function(s) {
      socket.emit('status', s);
    }

    // Get chat info from mongo
    chat.find().limit(100).sort({_id:1}).toArray(function(err, resp) {
      if(err) {
        throw err;
      }

      // Emit msg to WS
      socket.emit('output', resp)
    });

    // Input event handler
    socket.on('input', function(data) {
      let name = data.name;
      let message = data.message;

      // Does the name and message contain any content?
      if(name == '' || message == '') {
        // Send error status
        sendStatus('You should enter a nickname for this session and a message');

      } else {
        // Insert valid message
        chat.insert({name: name, message: message} function() {
          client.emit('out', [data]);

          // Send success status
          sendStatus({
            message: 'Message sent with success',
            clear: true
          });
        });
      }
    });

    // Clear handler (This app is in it's early stages; the clear will be
    // open to everyone on the running session).

    socket.on('clear', function(data) {
      // Remove all msgs from mongo collection
      chat.remove({}, function() {
        // Emit clear
        socket.emit('cleared')
      });
    });

  });
});
