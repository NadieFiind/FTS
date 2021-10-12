"""Entry Point"""

if __name__ == "__main__":
	import os
	from fts.web import app
	
	os.environ["FLASK_ENV"] = "development"
	app.run(host="0.0.0.0", port=8080, debug=True)
