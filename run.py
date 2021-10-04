"""Entry Point"""

import os
import sys
from fts.src import web, shell


def help() -> None:
	print("\nUsage:")
	print("  python run.py {src}")
	print("\nsrc:")
	print("  web")
	print("  shell")


if __name__ == "__main__":
	try:
		arg1 = sys.argv[1]
	except IndexError:
		print("Not enough arguments supplied.")
		help()
		exit()
	
	if arg1 == "web":
		os.environ["FLASK_ENV"] = "development"
		web.main()
	elif arg1 == "shell":
		shell.main()
	else:
		print(f"src '{arg1}' not found.")
		help()
