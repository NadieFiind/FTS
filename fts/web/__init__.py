import json
from fts.core import FTS
from typing import Text, Callable
from flask import Flask, request, render_template, abort


app = Flask(__name__)
app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


def initialize_fts() -> FTS:
	# Load the configuration file.
	with open("config.json") as file:
		config = json.load(file, strict=False)
	
	# Initialize the FTS from the FTSF file.
	with open(config["ftsf_path"]) as file:
		return FTS(file.read(), indent_char=config.get("indent_char") or "\t")


@app.before_request
def limit_remote_addr() -> None:
	if "127.0.0.1" not in request.access_route:
		abort(403)


@app.route("/")
def index() -> Text:
	return render_template("index.html", fts=initialize_fts())
