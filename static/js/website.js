 function send_request(data) {
	const url = "/qr"
	console.log(`url: ${url}`)
	const headers = {
		"Content-Type": "application/json"	
	}
	fetch(url, {
		method: "POST", 
		headers: headers,
		body: JSON.stringify(data)
	})
	.then( resp => resp.blob())
	.then(blob => download_blob(blob))

	
}

function  download_blob(blob) {

	const file_url = URL.createObjectURL(blob)
	const dlink = document.createElement('a')
	dlink.href = file_url	
	dlink.classlist.append(".dlink")	
	dlink.download = "QR_3D.stl"
	document.body.appendChild(dlink)
	dlink.click()
}


function submit_form() {
	let size = parseInt(document.querySelector("#size").value)
	let depth = parseInt(document.querySelector("#depth").value)
	let true_depth = parseInt(document.querySelector("#true_depth").value)
	const message = parseInt(document.querySelector("#message").value)

	//defaults
	if(size <= 0 || size === null) {
		size = 1
	}
	if(depth <= 0 || depth === null) {
		depth = 1
	}	
	if(true_depth <= 0 || true_depth === null) {
		true_depth = 1
	}
	if(message === null) {
		return	
	}

	

	const data = {
		"size": size,
		"depth": depth,
		"true_depth": true_depth,
		"message": message

	}

	const resp =  send_request(data)


	
}


function cleanup() {
}
