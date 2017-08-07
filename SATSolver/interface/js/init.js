const net = require('net');

// Bindings

var perc = new Vue({
  el: '#perc',
  data: {
    percentage: 12
  }
});

var terminal = new Vue({
	el: '#term',
	data : {
		text : "Waiting for solving to start..."
	}
});

var error_log = new Vue({
  el: "#err",
  data : {
    text : "Errors will go here ;)"
  }
});

// Connection

// Create connection and establish callbacks.

let conn = new net.Socket();

if (process.env.SAT_SOLVER_PORT != null) {
  client.connect(process.env.SAT_SOLVER_PORT, '127.0.0.1', function() {
	  console.log('Connected');
  });
}
conn.on('data', function(data) {
	console.log('Received: ' + data);
});
conn.on('close', function() {
	console.log('Connection closed');
});