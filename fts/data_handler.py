import os
import json
from fts.core import FTS
from fts.utils import datetime_now


home_ftsf_path: str  # The path of the home FTSF file.
ftsf_folder_path: str  # The path where the FTSF files are stored.


def initialize_fts() -> FTS:
	global home_ftsf_path
	global ftsf_folder_path
	
	# Load the configuration file.
	with open("config.json") as file:
		config = json.load(file, strict=False)
	
	# Load the data file.
	with open("fts/data/data.json") as file:
		data = json.load(file)
	
	ftsf_folder_path = config.get("ftsf_folder_path") or "data"
	home_ftsf_path = os.path.join(ftsf_folder_path, data["home_ftsf"])
	
	try:
		# Initialize the FTS from the home FTSF file.
		with open(home_ftsf_path) as file:
			return FTS(file.read(), indent_char=config.get("indent_char") or "\t")
	
	# If the home FTS format file doesn't exist, create one.
	except FileNotFoundError:
		os.makedirs(ftsf_folder_path, exist_ok=True)
		
		# Read the default FTSF file.
		with open("fts/data/ftsf/default.ftsf") as file:
			default_ftsf = file.read()
		
		with open(home_ftsf_path, "w") as file:
			file.write(default_ftsf)
			return FTS(default_ftsf, indent_char=config.get("indent_char") or "\t")


def make_backup(fts: FTS) -> None:
	"""Create a data backup of the {FTS}."""
	backup_file_path = os.path.join(
		ftsf_folder_path, str(datetime_now()) + ".ftsf"
	)
	
	with open(backup_file_path, "w") as file:
		file.write(fts.to_string())
