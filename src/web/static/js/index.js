const Modes = {
	Viewing: 0,
	Editing: 1,
	Inserting: 2,
	Deleting: 3
}

let current_mode = Modes.Viewing;

function udpateMode(mode) {
	current_mode = mode;
	
	switch (mode) {
		case Modes.Viewing:
			s(".temporary", true).forEach((inputElem) => {
				if (inputElem.value.trim()) {
					TasksEditor.addTask(inputElem);
				}
			});
			
			for (let elem of s(".controls > .btn", true)) {
				elem.classList.remove("active");
			}
			
			for (let taskElem of s(".task-content", true)) {
				taskElem.querySelector(".task-id").style.backgroundColor = "black";
			}
			
			TasksEditor.saveAll();
			break;
		case Modes.Editing:
			s(".controls > .edit-btn").classList.add("active");
			break;
		case Modes.Inserting:
			s(".controls > .insert-btn").classList.add("active");
			
			for (let taskElem of s(".task-content", true)) {
				let linput_elem = createTextInput();
				linput_elem.classList.add("temporary");
				insertElemBefore(linput_elem, taskElem);
			}
			
			break;
		case Modes.Deleting:
			s(".controls > .delete-btn").classList.add("active");
			
			for (let taskElem of s(".task-content", true)) {
				let btn = document.createElement("button");
				btn.classList.add("temporary", "del-btn");
				taskElem.appendChild(btn);
				btn.addEventListener("click", () => {
					TasksEditor.deleteTask(taskElem);
				});
			}
			
			break;
	}
}

function updateControls(isShowingControls) {
	if (isShowingControls) {
		s(".controls").classList.remove("hidden");
	} else {
		s(".controls").classList.add("hidden");
		udpateMode(Modes.Viewing);
	}
}

s("main").addEventListener("click", () => updateControls(true));
s(".controls > .close-btn").addEventListener("click", () => updateControls(false));
s(".controls > .edit-btn").addEventListener("click", () => {
	if (current_mode == Modes.Viewing) {
		udpateMode(Modes.Editing);
	} else {
		udpateMode(Modes.Viewing);
	}
});
s(".controls > .insert-btn").addEventListener("click", () => {
	if (current_mode == Modes.Viewing) {
		udpateMode(Modes.Inserting);
	} else {
		udpateMode(Modes.Viewing);
	}
});
s(".controls > .delete-btn").addEventListener("click", () => {
	if (current_mode == Modes.Viewing) {
		udpateMode(Modes.Deleting);
	} else {
		udpateMode(Modes.Viewing);
	}
});

for (let taskElem of s(".task-content", true)) {
	taskElem.addEventListener("click", (event) => {
		switch (current_mode) {
			case Modes.Editing:
				let new_elem = createTextInput(taskElem.querySelector(".content").textContent);
				taskElem.parentNode.replaceChild(new_elem, taskElem);
				
				TasksEditor.editTask(new_elem);
				break;
		}
	});
}

class TasksEditor {
	static #insertingTasks = [];
	static #editingTasks = [];
	static #deletingTasks = [];
	
	static editTask(elem) {
		this.#editingTasks.push(elem);
	}
	
	static addTask(elem) {
		this.#insertingTasks.push(elem);
	}
	
	static deleteTask(elem) {
		if (this.#deletingTasks.includes(elem)) {
			elem.querySelector(".task-id").style.backgroundColor = "black";
			this.#deletingTasks = this.#deletingTasks.filter((e) => e !== elem)
		} else {
			elem.querySelector(".task-id").style.backgroundColor = "red";
			this.#deletingTasks.push(elem);
		}
	}
	
	static saveAll() {
		for (let taskElem of this.#editingTasks) {
			sendData({
				"edit_task": taskElem.parentNode.id,
				"content": taskElem.value.trim()
			});
		}
		
		for (let inputElem of this.#insertingTasks) {
			sendData({
				"insert_task": inputElem.value.trim(),
				"parent_id": inputElem.parentNode.parentNode.id || null,
				"position": parseInt(inputElem.parentNode.id.slice(-1))
			});
		}
		
		for (let taskElem of this.#deletingTasks) {
			sendData({"delete_task": taskElem.parentNode.id});
		}
		
		s(".temporary", true).forEach((inputElem) => inputElem.remove());
		let shouldReload = false;
		
		if (this.#insertingTasks.length > 0) {
			this.#insertingTasks = [];
			shouldReload = true;
		}
		
		if (this.#editingTasks.length > 0) {
			this.#editingTasks = [];
			shouldReload = true;
		}
		
		if (this.#deletingTasks.length > 0) {
			this.#deletingTasks = [];
			shouldReload = true;
		}
		
		if (shouldReload) {
			location.reload();
		}
	}
}
