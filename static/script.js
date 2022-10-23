$(document).ready(function () {
	$socket = new socket("")

	$("body").on('click', ".navbar-element", function(e){
        window.location.href = '/' + $(e.target).attr("name")
    });
});
 
class socket {
	constructor (endpoint) {
		this.connection = io()//"", {transports: ["websocket"]})
		
		this.connection.on('message', function(msg) {
			alert('<p>Received: ' + msg.token + '</p>');
		});
		
		this.connection.on('auth', function(msg) {
			Cookies.set("token", msg.data.token)
			console.log("auth success")
		});
		
		this.connection.onAny(function(eventName, msg) {
			if (msg.status == 0) {
				window.location.href = '/';
				return
			}
			console.log("UPDATE");

		});
	}
	
	send(event, data) {
		this.connection.emit(event, JSON.stringify(data))
	}
	
	
}

function convertFormToJSON(form) {
	const array = $(form).serializeArray(); // Encodes the set of form elements as an array of names and values.
	const json = {};
	$.each(array, function () {
	  json[this.name] = this.value || "";
	});
	return json;
  }