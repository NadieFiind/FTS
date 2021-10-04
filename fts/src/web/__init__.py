from fts.core import FTS, Task
from typing import Text, Optional
from fts import data_handler as dh
from flask import Flask, request, render_template
from fts.data_handler import initialize_fts, make_backup


fts: FTS
app = Flask(__name__)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


@app.route("/send-data", methods=["POST"])
def send_data() -> str:
	if request.json.get("insert_task"):
		parent_id: Optional[str] = request.json.get("parent_id")
		parent: Optional[Task] = fts.get_task_by_id(parent_id) if parent_id else None
		
		make_backup(fts)
		
		fts.add_task(
			content=request.json["insert_task"],
			parent=parent,
			position=request.json["position"]
		)
	
	if request.json.get("edit_task"):
		task = fts.get_task_by_id(request.json["edit_task"])
		
		if task is None:
			return "okn't"
		else:
			make_backup(fts)
			task.content = request.json["content"]
	
	if request.json.get("delete_task"):
		make_backup(fts)
		fts.delete_task_by_id(request.json["delete_task"])
	
	# Save the changes to the home FTSF file.
	with open(dh.home_ftsf_path, "w") as file:
		file.write(fts.to_string())
	
	return "ok"


@app.route("/")
def index() -> Text:
	global fts
	fts = initialize_fts()
	return render_template("index.html", fts=fts)


def main() -> None:
	"""Entry Point"""
	app.run(host="0.0.0.0", port=8080, debug=True)
