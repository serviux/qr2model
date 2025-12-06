 function send_request(data) {
	const url = "/qr"
	const headers = {
		"Content-Type": "application/json"	
	}
	fetch(url, {
		method: "POST", 
		headers: headers,
		body: JSON.stringify(dat)
	})
	.then(response.blob())
	.then(blob => {downloadBlob(blob, 'qrcode.stl')})

	
}

function submit_form() {
	let size = document.querySelector("#size").value
	let depth = document.querySelector("#depth").value
	let true_depth = document.querySelector("#true_depth").value
	let message = document.querySelector("#message").value

	if(size === null) {
		size = 1
	}
	if(depth === null) {
		depth = 1
	}	
	if(true_depth === null) {
		true_depth = 1
	}
	if(message === null) {
		return	
	}

	

	let data = {
		"size": size,
		"depth": depth,
		"true_depth": true_depth,
		"message": message

	}

	let resp =  send_request(data)


	
}



