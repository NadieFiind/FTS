import sys
from src import shell

if __name__ == "__main__":
	try:
		arg1 = sys.argv[1]
	except IndexError:
		print("Not enough arguments supplied.\n")
		print("Usage:")
		print("  python run.py [src]")
		print("\nsrc:")
		print("  shell - Run an interactive shell.")
		exit()
	
	if arg1 == "shell":
		shell.main()
	else:
		print(f"src '{arg1}' not found.")
