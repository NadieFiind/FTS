TODO:
fix readme
implement a dedicated parser for .ftsf file
improve error handling
add web interface
add documentation and docstrings to `core` folder

=================================
Snapshot File Syntax:

- every line is a task
the line should start with ">"

- you can put certain prefix to a line
the available prefixes are:
tab - will consider the line as subtask      - 	> this is a subtask
curly brackets with positive interger inside - {3} > this is a task with priority 3, the default is 0
scheduler function call                      - dt(_, "10:30") > this is a task with a schedule
	what is a scheduler function?
	scheduler functions are used for scheduling tasks
	there are different built-in scheduler functions
	you can also define your own scheduler functions (currently not supported)

*the order of the prefixes matter*

- type "#" for comments
=================================
Dat, Time, Day String:

strings should be enclosed by double quotes ("")

time is 24 hour format
hh:mm
example: "18:00"

date is yyyy-mm-dd format
example: "2021-09-26"

date and time is yyyy-mm-dd hh:mm
example: "2021-09-26 18:00"

days are "mon", "tue", "wed", "thu", "fri", "sat", "sun"

=================================
List

lists are collection of values
example, list of strings: ["a", "b", "c"]

=================================
Built-in Scheduler Functions:

parameters that are not given an argument will default to None
Scheduler Functions return a boolean, true if the task is scheduled now, otherwise false
Scheduler Functions have string representation of themselves

date(String start, String end):
	optionally define the start and the end of a task
	
	parameters:
		start - defines the start of a task, should be a valid date or date and time string
		end - defines the end of a task, should be a valid date or date and time string

days(Union[List, str] days, String start, String end):
	if days is str:
		"everyday", "weekdays", "weekends"
	
	optionally define the start and the end of a task, recurring based on the [days]
	
	parameters:
		days - list of days (day string) to occur the task
		start - defines the start of a task, should be a valid time string
		end - defines the end of a task, should be a valid time string
=================================
Subtasks

subtasks inherits the schedule of their parent
if a schedule is defined in a subtask, it will override its parent's schedule
but if the schedule of the subtask overlaps its parent's schedule, an error will occur

=================================
