<script>
	let user_input = '', msg_sent = '', msg_history = [], msg_string = '';
	let msg_received = {}, msg_content = [];
	var username = '';
	// {sender: 'Robson', text: 'adsd'}
	let connected = false;
	var ws;
	function connect(event) {
		if (connected == false) {
			ws = new WebSocket("ws://127.0.0.1:5678/");
			ws.onopen = function(event) {
				console.log('Connected');
				connected = true;
			}
			ws.onmessage = function(event) {
				console.log(event.data);
				if (event.data.indexOf('!') >= 0) { // regular message
					// format: Sender~Text
					msg_content = event.data.split('!'); //! is used as a separator
					msg_received = {sender: msg_content[0], text: msg_content[1]};
					msg_history.push(msg_received);
					msg_history = msg_history;
				} else if (event.data.indexOf('#') >= 0) { // system message
					// format: type~Text
					msg_content = event.data.split('#');
					if (msg_content[0] == 'namechanged') {
						username = msg_content[1];
					} else {
						msg_received = {sender: 'system', text: msg_content[1]};
						msg_history.push(msg_received);
						msg_history = msg_history;
					}
				} else if (event.data.indexOf('~') >= 0) { // private message
					// format: Sender~Receiver~Text
					msg_content = event.data.split('~');
					if (msg_content[1] == username) {
						msg_received = {sender: msg_content[0], text: msg_content[2]};
						msg_history.push(msg_received);
						msg_history = msg_history;
					}
				}
		    }
			ws.onclose = function(event) {
				console.log('Disconnected');
				alert('Desconectado')
				connected = false;
				username = '';
				msg_history = [];
			}
			ws.onerror = function(event) {
				console.log('Failed to connect');
			}
		}
	}

	function sendMessage(event) {
		if (event.keyCode == 13 || event.type == 'click') {
			if (user_input == '') {
				alert('Digite algo!');
			} else {
				let command_name = user_input.indexOf('/nome');
				let command_pm = user_input.indexOf('/pm');
				if (username == '') { // does not have a name
					if (command_name >= 0) { // is trying to set up a name
						msg_string = '!' + user_input;
						ws.send(msg_string);
						console.log('Sent:' + msg_string);
						user_input = '';
					} else {
						alert('Escolha um nome de usuário primeiro.')
						user_input = '';
					}
				} else { // already has a name
					if (command_name >= 0) { // is trying change name
						msg_string = username + '!' + user_input;
						ws.send(msg_string);
						console.log('Sent:' + msg_string);
						user_input = '';
					} else {
						msg_sent = {sender: username, text: user_input};
						msg_history.push(msg_sent);
						msg_history = msg_history;
						msg_string = username + '!' + user_input;
						ws.send(msg_string);
						console.log('Sent:' + msg_string);
						user_input = '';
					}
				}
			}
		}
	}
</script>

<main>
	<h1>Chat room</h1>
	<div id='container'>
		{#if connected == false}
			<p id='wait'>
				Waiting...
			</p>
			<button id='connect' on:click = {connect}>
				Connect
			</button>
		{:else}
			<p id='ready'>
				Connected!
			</p>
		{/if}
		<input id='input' bind:value={user_input} on:keypress={sendMessage}/>
		<button id='send' on:click = {sendMessage}>
			Enviar
		</button>
		<div id='chatbox'>
			<div>
				{#each msg_history as m}
					{#if m.sender == 'system'}
						<p id='system'>Sistema: {m.text}</p>
					{:else if m.sender == username}
						<p id='sent'>Enviado: {m.text}</p>
					{:else}
						<p id='received'>{m.sender}: {m.text}</p>
					{/if}
				{/each}
			</div>
		</div>
	</div>
</main>

<style>
	main {
		text-align: center;
		padding: 5px;
		max-width: 240px;
		margin: 0 auto;
		background-color: #333942;
		height: 100%;
		color: #000000;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	p {
		margin-left: 5%;
		text-align: left;
	}
	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}

	#container {
		background-color: #e0e0e0;
		border-style:double;
		border-color: #333333;
		border-width: 9px;
		border-radius: 10px;
		margin: auto;
		width: 80%;
		max-width: 600px;
		min-width: 40%;
		height: 400px;
		overflow: hidden;
		position: relative;
	}

	#chatbox {
		position: absolute;
		width: 92%;
		left: 4%;
		height: 62%;
		border-style: solid;
		border-width: 3px;
		overflow: auto;
		display: flex;
		flex-direction: column-reverse;
	}

	#send {
		position: absolute;
		bottom: 1px;
		right: 2%;
		border-style: solid;
		border-color: #000000;
		border-width: 1px;
	}

	#input {
		position: absolute;
		bottom: 40px;
		width: 96%;
		left: 2%;
		border-style: solid;
		border-color: #000000;
		border-width: 1px;
	}

	#connect {
		position: absolute;
		top: 10px;
		right: 2%;
		border-style: solid;
		border-color: #000000;
		border-width: 1px;
	}

	#wait {
		color: #e8760c;
		font-weight: 500;
	}

	#ready {
		color: #34e80c;
		font-weight: 500;
	}

	#received {
		color: #2d1ad6;
		margin-top: 0.3em;
		margin-bottom: 0;
		margin-left: 0;
	}

	#sent {
		color: #000000;
		margin-top: 0.3em;
		margin-bottom: 0;
		margin-left: 0;
	}

	#system {
		color: #ffa500;
		margin-top: 0.3em;
		margin-bottom: 0;
		margin-left: 0;
	}
</style>
