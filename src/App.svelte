<script>
	let msg_toSend = '', msg_string = '', msg = [];
	let msg_received = {}, msg_content = [];
	let username = 'Gabriel';
	// {sender: 'Robson', text: 'adsd'}
	let connected = false;

	function connect(event) {
		if (connected == false) {
			let ws = new WebSocket("ws://127.0.0.1:5678/");
			ws.onopen = function(event) {
				console.log('Connected')
				connected = true;
			}
			ws.onmessage = function(event) {
				if (event.data.indexOf('!') >= 0) { // regular message
					msg_content = event.data.split('!') //! is used as a separator
					msg_received = {sender: msg_content[0], text: msg_content[1]}
					msg.push(msg_received);
					console.log(msg);
				} else if (event.data.indexOf('#') >= 0) { // system message
					msg_content = '';
				}
		    }
			ws.onclose = function(event) {
				connected = false;
			}
		}
	}

	function sendMessage(event) {
		if (event.keyCode == 13 || event.type == 'click') {
			if (msg_toSend != '' & 1) {
				// msg.push(msg_toSend);
				// msg_type.push(1);
				// msg_string = msg.join('<br/>');

				console.log(msg_toSend);
				msg_toSend = '';
			}
		}
	}
</script>

<main>
	<h1>Chat room</h1>
	<div id='chatbox'>
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
		<p>{@html msg_string}</p>
		{#each msg as m}
			{#if 1>0}
				<p>1</p>
			{/if}
		{/each}
		<input id='input' name='msg' bind:value={msg_toSend} on:keypress={sendMessage}/>
		<button id='send' on:click = {sendMessage}>
			Enviar
		</button>
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

	#chatbox {
		background-color: #d6d6d6;
		border-style:double;
		border-color: #333333;
		border-width: 9px;
		border-radius: 10px;
		margin: auto;
		width: 80%;
		max-width: 600px;
		min-width: 40%;
		height: 400px;
		overflow: auto;
		position: relative;
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
</style>
