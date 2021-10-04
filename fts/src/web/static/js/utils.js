function s(selector, all) {
	if (all) {
		return document.querySelectorAll(selector);
	} else {
		return document.querySelector(selector);
	}
}

function sendData(data) {
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "/send-data");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(JSON.stringify(data));
}

function insertElemBefore(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode);
}

function createTextInput(value) {
	let elem = document.createElement("input");
	elem.setAttribute("type", "text");
	
	if (value) {
		elem.setAttribute("value", value);
	}
	
	return elem;
}
