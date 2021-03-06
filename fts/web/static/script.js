function s(selector, all) {
	if (all) {
		return document.querySelectorAll(selector);
	} else {
		return document.querySelector(selector);
	}
}

let hiddenTasks = JSON.parse(localStorage.getItem("hiddenTasks") || "{}");

for (let btn of s(".task .hide-btn", true)) {
	btn.addEventListener("click", () => {
		if (!confirm("Remove this item?")) return;
		
		let content = btn.parentNode.querySelector(".content");
		let id = `${btn.parentNode.parentNode.id}-${content.textContent}`;
		
		hiddenTasks[id] = new Date().toString();
		localStorage.setItem("hiddenTasks", JSON.stringify(hiddenTasks));
		btn.parentNode.parentNode.remove();
	});
}

for (let task of s(".task .content", true)) {
	let id = `${task.parentNode.parentNode.id}-${task.textContent}`;
	
	for (let clas of task.classList) {
		if (clas.startsWith("when-")) {
			let date = new Date(clas.substring(5));
			console.log(`${date.toString().slice(0, 24)} ${task.textContent}`);
			
			if (id in hiddenTasks) {
				if (!task.classList.contains("active-now")) {
					task.parentNode.parentNode.remove();
				} else {					
					if (new Date(hiddenTasks[id]) > date) {
						task.parentNode.parentNode.remove();
					} else {
						delete hiddenTasks[id];
						localStorage.setItem("hiddenTasks", JSON.stringify(hiddenTasks));
					}
				}
			}
		}
	}
}

window.onerror = (msg, url, lineNumber) => {
	alert(`${msg} in ${url} at line ${lineNumber}.`);
	return true;
}
