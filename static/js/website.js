const urls_to_free = [] 

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
	.then( function(response) {
		if(!response.ok) {
			throw new Error("Bad Requeset")
		}
		return response.blob()
	})
	.then(blob => download_blob(blob))

	
}

function  download_blob(blob) {

	const file_url = URL.createObjectURL(blob)
	urls_to_free.push(file_url)
	const dlink = document.createElement('a')
	dlink.href = file_url	
	dlink.classList.add("dlink")	
	dlink.download = "QR_3D.stl"
	document.body.appendChild(dlink)
	dlink.click()
}


function submit_form() {
	let size = parseInt(document.querySelector("#size").value)
	let depth = parseInt(document.querySelector("#depth").value)
	let true_depth = parseInt(document.querySelector("#true_depth").value)
	const message = document.querySelector("#message").value

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

	

	const data = {
		"size": size,
		"depth": depth,
		"true_depth": true_depth,
		"message": message

	}

	send_request(data)


	
}


function cleanup() {
	document.querySelectorAll(".dlink").forEach(ele => ele.remove(ele))
	urls_to_free.forEach(url => URL.revokeObjectURL(url))
	while (urls_to_free.length) {
		urls_to_free.pop()	
	}
}

setInterval(cleanup, 30000)
