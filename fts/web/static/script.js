function s(selector, all) {
	if (all) {
		return document.querySelectorAll(selector);
	} else {
		return document.querySelector(selector);
	}
}

let hiddenTasks = JSON.parse(localStorage.getItem("hiddenTasks") || "[]");

for (let btn of s(".task .hide-btn", true)) {
	btn.addEventListener("click", () => {
		let id = `${btn.parentNode.parentNode.id}-${btn.parentNode.querySelector(".content").textContent}`;
		hiddenTasks.push(id);
		localStorage.setItem("hiddenTasks", JSON.stringify(hiddenTasks));
		btn.parentNode.parentNode.remove();
	});
}

for (let task of s(".task .content", true)) {
	let id = `${task.parentNode.parentNode.id}-${task.textContent}`;
	if (hiddenTasks.includes(id)) {
		task.parentNode.parentNode.remove();
	}
}
