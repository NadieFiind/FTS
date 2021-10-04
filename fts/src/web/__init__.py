import os
import json
from fts.core import FTS, Task
from typing import Text, Optional
from fts.utils import datetime_now
from flask import Flask, request, render_template


home_ftsf_path: str
ftsf_folder_path: str


def initialize_fts() -> FTS:
	global home_ftsf_path
	global ftsf_folder_path
	
	# Open the configuration data.
	with open("config.json") as file:
		config = json.load(file, strict=False)
	
	# Open the data file.
	with open("fts/core/data/data.json") as file:
		data = json.load(file)
	
	ftsf_folder_path = config["ftsf_folder_path"]
	
	# The path of the home FTS format file.
	home_ftsf_path = os.path.join(ftsf_folder_path, data["home_ftsf"])
	
	try:
		# Initialize the {FTS} from the home FTS format file.
		with open(home_ftsf_path) as file:
			return FTS(file.read(), indent_char=config.get("indent_char"))
	
	# If the home FTS format file doesn't exist, create one.
	except FileNotFoundError:
		os.makedirs(config["ftsf_folder_path"], exist_ok=True)
		
		with open("fts/core/data/ftsf/default.ftsf") as file:
			ftsf = file.read()
		
		with open(home_ftsf_path, "w") as file:
			file.write(ftsf)
			return FTS(ftsf, indent_char=config.get("indent_char"))


def make_backup(fts: FTS) -> None:
	backup_file_path = os.path.join(
		ftsf_folder_path, str(datetime_now()) + ".ftsf"
	)
	
	with open(backup_file_path, "w") as file:
		file.write(fts.to_string())


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
	with open(home_ftsf_path, "w") as file:
		file.write(fts.to_string())
	
	return "ok"


@app.route("/")
def index() -> Text:
	return render_template("index.html", fts=fts)


def main() -> None:
	"""Entry Point"""
	global fts
	fts = initialize_fts()
	app.run(host="0.0.0.0", port=8080, debug=True)
