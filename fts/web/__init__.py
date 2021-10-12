import os
import json
from fts.core import FTS
from functools import wraps
from typing import Any, Text, Callable
from flask import Flask, Response, request, render_template


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


def requires_auth(f: Callable) -> Callable:
	@wraps(f)
	def wrapper(*args: Any, **kwargs: Any) -> Response:
		auth = request.authorization
		
		if not auth or not auth.password == os.getenv("PASS"):
			return Response(
				"", 401, {"WWW-Authenticate": "Basic realm='Login Required'"}
			)
		
		return f(*args, **kwargs)
	
	return wrapper


@app.route("/")
@requires_auth
def index() -> Text:
	return render_template("index.html", fts=initialize_fts())
