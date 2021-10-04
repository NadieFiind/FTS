# Flexible Tasks Scheduler
Flexible Tasks Scheduler (FTS) is a program written in Python to make a standard for writing text file-based task lists.
FTS format is very user-friendly, easy to read and write, yet very powerful for managing tasks.
FTS has a parser to read and render FTS format files (`.ftsf`) on different user interfaces *(e.g. Terminal, Browser)*.
It can also act as an editor for FTSF files depending on the interface used.

## FTS Format
- FTSF files have a file extension of `.ftsf`. *(e.g. `my_tasks.ftsf`)*

- Every line in the file except for empty lines is a "task" starting with a character `>`.
  For simplicity, we will call them as "task lines" and "empty lines" for empty or whitespace lines.
  Non-empty lines that don't start with a character `>` is invalid.

- Comments are defined by putting a `~#`. All characters after that will be ignored.
  **Comments are very unstable so it is not recommended to use them right now.**

```
> This is a task line.
  
This is an invalid line.

~# This is a comment line.
```

- Different prefixes can be placed to task lines to modify their behaviour.

### Prefixes
- Task Priority - The priority level of a task can be defined by putting a number enclosed by curly brackets.
  The value of the priority level can be a negative. It defaults to `0` implictly.
  Decimal number is invalid.
```
{2} > This task has a priority level of 2.
> This task has a priority level of 0.
{-4} > This task has a priority level of -4.
{1.2} > This task has an invalid priority level value.
```
- Task Scheduler - A function that schedules tasks intended for specific events and times.
  Task schedulers should be valid Python code because it is evaluated (`eval`) in the FTS program.
  Currently, there are only 2 built-in scheduler functions: `date` and `days`.
  In the future versions, custom scheduler functions can be defined by the user.
  For more information about the built-in scheduler functions,
  read the [code](fts/core/scheduler/builtins.py) KEKW.
```
days("everyday") > This task is scheduled everyday.
date("2022-09-26") > This task is scheduled to start in September 26, 2022.
```
- Subtask - A task line will be considered as a subtask of another task if it is indented.
```
> This is a parent task.
	> This is a child task. (Subtask)
```

#### Prefix Order
The order of the prefixes matters.
Indentation should always goes first, followed by priority level, and followed by scheduler.
```
{2} days("everyday") > Valid FTS format.
days("everyday") {2} > Invalid FTS format.
```

### Subtasks
- If the scheduler of a subtask that doesn't have one is accessed, the scheduler of its parent task will be returned instead.
```py
subtask.scheduler or subtask.parent.scheduler
```
- The priority level of the parent of a subtask will be added to the priority level of the subtask.
```py
subtask.priority = subtask.priority + subtask.parent.priority`
```

## [FTS Config File](config.json)
- `"indent_char"` - The indentation character used in the FTSF files.
- `"ftsf_folder_path"` - The folder path where the FTSF files are saved and stored.

### MORE
- FTS is still in its very early stage of development so it is not guaranteed to work properly.
  And most of its features are not implemented yet.
- Since the parser is very basic and still under development,
  the character `>` will be considered as the start of the task line's content regardless of where it is placed. For example, `{2} scheduler(">") > task`,
  the first occurrence of `>` will be considered as the start of the task line's content.
  And obviously, it will cause an error.
- Comments are very unstable so it is not recommended to use them right now.

## TODO
- Improve task insert on the web user interface src.
- Implement priority editor.
- Implement scheduler editor.
- Improve the documentation.
- Add documentation to the `core`.
- Improve error handling on the `core`.
- Implement a dedicated parser for `.ftsf` files.
