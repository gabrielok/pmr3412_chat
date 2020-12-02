<script>
	var ws = new WebSocket("ws://127.0.0.1:5678/"),
		messages = document.createElement('u1');
	// ws.onmessage = function (event) {
	// 	var messages = document.getElementsByTagName('ul')[0],
    //         message = document.createElement('li'),
    //         content = document.createTextNode(event.data);
    //     message.appendChild(content);
    //     messages.appendChild(message);
    // };
	ws.onopen = function (event) {
		showmessage = true;
		console.log('Connected')
	}
</script>

<main>
	<h1>Hello!</h1>
</main>

<style>
	body {
		background-color: #333942;
	}
	main {
		text-align: center;
		padding: 5px;
		max-width: 240px;
		margin: 0 auto;
		background-color: #333942;
		height: 100%;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	p {
		text-align: center;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
